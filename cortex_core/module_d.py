"""
Module D — Final Decision Authority (Phase 4).

Executes the deterministic 10-Gate reconciliation pipeline across MarketSnapshot,
PortfolioSnapshot, Module A, Module B, and Module C to produce exactly ONE
final verdict (BUY | HOLD | SELL | ABSTAIN) and an audited PortfolioState
transition.

Never executes orders autonomously and never allows Module A or Module B to
issue competing trade authorizations.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from btc_config_loader import get_param
from cortex_core.audit import AuditLogger, canonical_sha256
from cortex_core.constants import (
    NOT_CONFIGURED,
    ACTIVE_RESERVATION_ORDER_STATUSES,
    ExitClassification,
    LoopType,
    ModuleState,
    PortfolioState,
    ReconciliationStatus,
    Verdict,
)
from cortex_core.evidence_common import check_data_integrity, field_info
from cortex_core.ledger import PortfolioLedger
from cortex_core.models import (
    AllocationAssessment,
    ConfigurationRecord,
    DecisionRecord,
    GateResult,
    MarketSnapshot,
    ModuleAssessment,
    OrderRecord,
    PortfolioSnapshot,
)
from cortex_core.module_a import evaluate_module_a
from cortex_core.module_b import evaluate_module_b
from cortex_core.module_c import evaluate_allocation_controller
from cortex_core.time_utils import ensure_utc_iso, utc_now

SOFTWARE_VERSION = "CORTEX-BTC-DIBSE-v1.0"


def classify_market_regime(
    snapshot: MarketSnapshot,
    config: ConfigurationRecord,
    *,
    evidence_inputs: dict[str, Any] | None = None,
) -> tuple[str, str, str]:
    """
    Deterministically classify market regime using configured rules only.
    Returns (regime_label, gate_status, rationale).
    """
    rules = get_param(config, "market_regime_rules")
    if not isinstance(rules, dict) or all(v == NOT_CONFIGURED for v in rules.values()):
        return NOT_CONFIGURED, NOT_CONFIGURED, "market_regime_rules are NOT CONFIGURED."

    ev = evidence_inputs or {}
    spot, _ = field_info(snapshot, "spot_price")
    sma50, _ = field_info(snapshot, "sma50")
    sma200, _ = field_info(snapshot, "sma200")
    rsi14, _ = field_info(snapshot, "rsi14")
    vix, _ = field_info(snapshot, "vix")

    if spot is None:
        return "DATA UNAVAILABLE", "UNAVAILABLE", "Spot price unavailable for regime classification."

    dis_rule = rules.get("dislocation_extreme_risk")
    if isinstance(dis_rule, dict):
        max_vix = dis_rule.get("max_vix")
        min_rsi = dis_rule.get("min_rsi14")
        if ev.get("dislocation_active") or (
            max_vix not in (NOT_CONFIGURED, None) and vix is not None and float(vix) >= float(max_vix)
        ) or (
            min_rsi not in (NOT_CONFIGURED, None)
            and rsi14 is not None
            and sma200 is not None
            and spot < sma200
            and float(rsi14) <= float(min_rsi)
        ):
            return "DISLOCATION / EXTREME RISK", "PASS", "Dislocation / extreme risk thresholds triggered."

    if sma200 is not None and spot < sma200:
        return "DEFENSIVE", "PASS", "Spot below 200D SMA -> DEFENSIVE regime."

    if sma50 is not None and sma200 is not None and spot > sma50 and spot > sma200:
        return "CONSTRUCTIVE", "PASS", "Spot above 50D and 200D SMA -> CONSTRUCTIVE regime."

    return "CAUTIOUS", "PASS", "Mixed moving-average structure -> CAUTIOUS regime."


def evaluate_final_decision(
    *,
    market_snapshot: MarketSnapshot,
    portfolio_snapshot: PortfolioSnapshot,
    module_a: ModuleAssessment,
    module_b: ModuleAssessment,
    config: ConfigurationRecord,
    previous_operating_state: PortfolioState = PortfolioState.USDT_100,
    open_orders: list[OrderRecord] | None = None,
    evidence_inputs: dict[str, Any] | None = None,
    now_utc: str | None = None,
) -> tuple[DecisionRecord, AllocationAssessment]:
    """
    Run the deterministic 10-Gate reconciliation pipeline and return
    (DecisionRecord, AllocationAssessment).
    """
    ts_iso = ensure_utc_iso(now_utc or market_snapshot.retrieved_ts_utc or utc_now(), field_name="now_utc")
    gates: list[GateResult] = []
    reasons: list[str] = []
    active_orders = [o for o in (open_orders or []) if o.status in ACTIVE_RESERVATION_ORDER_STATUSES]

    # ------------------------------------------------------------------
    # Gate 1 — Data Integrity
    # ------------------------------------------------------------------
    data_item, data_halted = check_data_integrity(market_snapshot, config)
    gates.append(
        GateResult(
            gate_number=1,
            gate_name="Data Integrity",
            status="FAIL" if data_halted else "PASS",
            summary=data_item.rationale,
            details=data_item.observed_value,
        )
    )
    if data_halted:
        reasons.append(data_item.rationale)

    # ------------------------------------------------------------------
    # Gate 2 — Portfolio Integrity
    # ------------------------------------------------------------------
    portfolio_ok = (
        portfolio_snapshot.configured
        and portfolio_snapshot.reconciliation_status == ReconciliationStatus.RECONCILED
    )
    if not portfolio_snapshot.configured:
        g2_status = NOT_CONFIGURED
        g2_summary = "Portfolio balances are NOT CONFIGURED."
        reasons.append(g2_summary)
    elif portfolio_snapshot.reconciliation_status != ReconciliationStatus.RECONCILED:
        g2_status = "FAIL"
        g2_summary = f"Portfolio reconciliation status is {portfolio_snapshot.reconciliation_status.value}: {portfolio_snapshot.reconciliation_notes}"
        reasons.append(g2_summary)
    else:
        g2_status = "PASS"
        g2_summary = "BTC/USDT balances, core isolation, and reservations reconciled."

    gates.append(
        GateResult(
            gate_number=2,
            gate_name="Portfolio Integrity",
            status=g2_status,
            summary=g2_summary,
            details={
                "configured": portfolio_snapshot.configured,
                "reconciliation_status": portfolio_snapshot.reconciliation_status.value,
            },
        )
    )

    # ------------------------------------------------------------------
    # Gate 3 — Market Regime
    # ------------------------------------------------------------------
    regime_label, regime_gate_status, regime_rationale = classify_market_regime(
        market_snapshot, config, evidence_inputs=evidence_inputs
    )
    gates.append(
        GateResult(
            gate_number=3,
            gate_name="Market Regime",
            status=regime_gate_status,
            summary=f"Regime={regime_label}: {regime_rationale}",
            details={"regime_label": regime_label},
        )
    )
    if regime_gate_status in {NOT_CONFIGURED, "UNAVAILABLE", "FAIL"}:
        reasons.append(regime_rationale)

    # ------------------------------------------------------------------
    # Gate 4 — Bullish Assessment (Module A)
    # ------------------------------------------------------------------
    gates.append(
        GateResult(
            gate_number=4,
            gate_name="Bullish Assessment (Module A)",
            status="PASS" if module_a.directional_signal == "BUY" else ("FAIL" if module_a.state == ModuleState.DATA_HALT else "PASS"),
            summary=f"Module A state={module_a.state.value}, signal={module_a.directional_signal}.",
            details={
                "state": module_a.state.value,
                "signal": module_a.directional_signal,
                "unconfigured": module_a.unconfigured_thresholds,
            },
        )
    )

    # ------------------------------------------------------------------
    # Gate 5 — Bearish Assessment (Module B)
    # ------------------------------------------------------------------
    gates.append(
        GateResult(
            gate_number=5,
            gate_name="Bearish Assessment (Module B)",
            status="PASS" if module_b.state != ModuleState.DATA_HALT else "FAIL",
            summary=f"Module B state={module_b.state.value}, signal={module_b.directional_signal}, exit={module_b.exit_classification.value if module_b.exit_classification else 'NONE'}.",
            details={
                "state": module_b.state.value,
                "signal": module_b.directional_signal,
                "exit_classification": module_b.exit_classification.value if module_b.exit_classification else None,
            },
        )
    )

    # ------------------------------------------------------------------
    # Gate 6 — Conflict Resolution
    # ------------------------------------------------------------------
    a_wants_buy = module_a.state == ModuleState.ELIGIBLE and module_a.directional_signal == "BUY"
    b_wants_sell = module_b.state == ModuleState.ELIGIBLE and module_b.directional_signal in {"SELL", "REDUCE"}
    b_shows_deterioration = module_b.state in {ModuleState.SETUP, ModuleState.CONFIRMED, ModuleState.ELIGIBLE}
    a_shows_accumulation = module_a.state in {ModuleState.SETUP, ModuleState.CONFIRMED, ModuleState.ELIGIBLE}

    conflict_abstain = False
    conflict_hold = False
    candidate_side: str | None = None

    if a_wants_buy and b_wants_sell:
        conflict_abstain = True
        g6_status = "FAIL"
        g6_summary = "Unresolved conflict: Module A proposes BUY while Module B proposes SELL/REDUCE."
        reasons.append(g6_summary)
    elif a_wants_buy and b_shows_deterioration:
        conflict_hold = True
        g6_status = "FAIL"
        g6_summary = "Module A proposes BUY while Module B detects active distribution/deterioration; BUY blocked."
        reasons.append(g6_summary)
    elif b_wants_sell and a_shows_accumulation and module_b.exit_classification != ExitClassification.DEFENSIVE_EXIT:
        conflict_abstain = True
        g6_status = "FAIL"
        g6_summary = "Module B proposes SELL while Module A identifies active accumulation setup; HUMAN REVIEW required."
        reasons.append(g6_summary)
    elif a_wants_buy and any(o.side == "SELL" for o in active_orders):
        conflict_abstain = True
        g6_status = "FAIL"
        g6_summary = "Module A proposes BUY while open SELL order(s) remain active."
        reasons.append(g6_summary)
    elif b_wants_sell and any(o.side == "BUY" for o in active_orders):
        conflict_abstain = True
        g6_status = "FAIL"
        g6_summary = "Module B proposes SELL while open BUY order(s) remain active."
        reasons.append(g6_summary)
    else:
        g6_status = "PASS"
        if a_wants_buy:
            candidate_side = "BUY"
            g6_summary = "No cross-module conflict; BUY candidate forwarded to Module C."
        elif b_wants_sell:
            candidate_side = "SELL"
            g6_summary = f"No cross-module conflict; SELL ({module_b.exit_classification.value if module_b.exit_classification else 'EXIT'}) candidate forwarded to Module C."
        else:
            g6_summary = "Neither module proposes an eligible trade; no conflict."

    gates.append(
        GateResult(
            gate_number=6,
            gate_name="Conflict Resolution",
            status=g6_status,
            summary=g6_summary,
            details={"candidate_side": candidate_side, "open_orders_count": len(active_orders)},
        )
    )

    # ------------------------------------------------------------------
    # Gate 7 — Allocation & Risk (Module C)
    # ------------------------------------------------------------------
    allocation = evaluate_allocation_controller(
        portfolio=portfolio_snapshot,
        config=config,
        regime_label=regime_label,
        module_a=module_a,
        module_b=module_b,
        preferred_side=candidate_side,
        now_utc=ts_iso,
    )
    dislocation_blocks_buy = candidate_side == "BUY" and regime_label == "DISLOCATION / EXTREME RISK"
    if dislocation_blocks_buy:
        g7_status = "FAIL"
        g7_summary = "DISLOCATION / EXTREME RISK regime prohibits new BUY risk."
        reasons.append(g7_summary)
    elif not portfolio_ok:
        g7_status = g2_status
        g7_summary = "Portfolio integrity gate failed; allocation blocked."
    elif candidate_side is not None and allocation.sizing_status == NOT_CONFIGURED:
        g7_status = NOT_CONFIGURED
        g7_summary = f"Allocation policy incomplete ({allocation.limiting_constraint_name})."
        reasons.append(g7_summary)
    elif not allocation.btc_floor_compliant or not allocation.usdt_floor_compliant or not allocation.core_btc_intact:
        g7_status = "FAIL"
        g7_summary = "Inventory floor or core BTC protection constraint violated."
        reasons.append(g7_summary)
    else:
        g7_status = "PASS"
        g7_summary = "Allocation bands, inventory floors, and core BTC protection satisfied."

    gates.append(
        GateResult(
            gate_number=7,
            gate_name="Allocation & Risk (Module C)",
            status=g7_status,
            summary=g7_summary,
            details={
                "permitted_side": allocation.permitted_side,
                "permitted_quantity_btc": allocation.permitted_quantity_btc,
                "limiting_constraint": allocation.limiting_constraint_name,
            },
        )
    )

    # ------------------------------------------------------------------
    # Gate 8 — Transaction Sizing
    # ------------------------------------------------------------------
    if candidate_side is None:
        g8_status = "PASS"
        g8_summary = "No transaction requested; zero size."
    elif dislocation_blocks_buy or not portfolio_ok:
        g8_status = "FAIL"
        g8_summary = "Transaction sizing blocked by upstream regime/portfolio gate."
    elif allocation.permitted_side == candidate_side and allocation.permitted_quantity_btc > 0:
        g8_status = "PASS"
        g8_summary = f"Permitted {candidate_side} size={allocation.permitted_quantity_btc:.8f} BTC (limited by {allocation.limiting_constraint_name})."
    elif allocation.sizing_status == NOT_CONFIGURED:
        g8_status = NOT_CONFIGURED
        g8_summary = f"Sizing parameters NOT CONFIGURED ({allocation.limiting_constraint_name})."
        reasons.append(g8_summary)
    else:
        g8_status = "FAIL"
        g8_summary = f"Proposed {candidate_side} rejected by sizing constraint: {allocation.limiting_constraint_name}."
        reasons.append(g8_summary)

    gates.append(
        GateResult(
            gate_number=8,
            gate_name="Transaction Sizing",
            status=g8_status,
            summary=g8_summary,
            details={"permitted_qty_btc": allocation.permitted_quantity_btc},
        )
    )

    # ------------------------------------------------------------------
    # Gate 9 — Execution Economics
    # ------------------------------------------------------------------
    if candidate_side is None:
        g9_status = "PASS"
        g9_summary = "No order proposed; execution economics idle."
    else:
        relevant_assessment = module_a if candidate_side == "BUY" else module_b
        exec_check = next((c for c in relevant_assessment.checklist if c.name == "execution_economics"), None)
        if exec_check is None or exec_check.status != "PASS":
            g9_status = exec_check.status if exec_check else "FAIL"
            g9_summary = exec_check.rationale if exec_check else "Execution economics check failed."
            reasons.append(g9_summary)
        else:
            g9_status = "PASS"
            g9_summary = exec_check.rationale

    gates.append(
        GateResult(
            gate_number=9,
            gate_name="Execution Economics",
            status=g9_status,
            summary=g9_summary,
            details={},
        )
    )

    # ------------------------------------------------------------------
    # Gate 10 — Final Verdict & State Transition
    # ------------------------------------------------------------------
    if data_halted:
        final_verdict = Verdict.ABSTAIN
        new_state = PortfolioState.DATA_HALT
        transition_reason = "Gate 1 Data Integrity failed -> ABSTAIN / DATA HALT."
    elif not portfolio_ok:
        final_verdict = Verdict.ABSTAIN
        new_state = PortfolioState.HUMAN_REVIEW
        transition_reason = "Gate 2 Portfolio Integrity failed -> ABSTAIN / HUMAN REVIEW."
    elif conflict_abstain:
        final_verdict = Verdict.ABSTAIN
        new_state = PortfolioState.HUMAN_REVIEW
        transition_reason = "Gate 6 unresolved conflict -> ABSTAIN / HUMAN REVIEW."
    elif (
        candidate_side == "BUY"
        and not conflict_hold
        and regime_gate_status == "PASS"
        and g7_status == "PASS"
        and g8_status == "PASS"
        and g9_status == "PASS"
    ):
        final_verdict = Verdict.BUY
        new_state = (
            PortfolioState.RE_ACCUMULATION
            if previous_operating_state
            in {PortfolioState.USDT_100, PortfolioState.ROTATION_TO_USDT, PortfolioState.BTC_DEFENSIVE}
            else PortfolioState.BTC_ACCUMULATION
        )
        transition_reason = (
            f"All 10 gates passed for BUY {allocation.permitted_quantity_btc:.8f} BTC "
            f"(limiting constraint: {allocation.limiting_constraint_name}). Manual approval required."
        )
    elif (
        candidate_side == "SELL"
        and not conflict_hold
        and regime_gate_status == "PASS"
        and g7_status == "PASS"
        and g8_status == "PASS"
        and g9_status == "PASS"
    ):
        final_verdict = Verdict.SELL
        exit_cls = module_b.exit_classification
        if exit_cls == ExitClassification.DEFENSIVE_EXIT:
            rem_tac = float(portfolio_snapshot.btc_tactical_available or 0.0) - allocation.permitted_quantity_btc
            new_state = PortfolioState.ROTATION_TO_USDT if rem_tac <= 1e-8 else PortfolioState.BTC_DEFENSIVE
        else:
            new_state = PortfolioState.BTC_REDUCTION
        transition_reason = (
            f"All 10 gates passed for SELL ({exit_cls.value if exit_cls else 'EXIT'}) "
            f"{allocation.permitted_quantity_btc:.8f} BTC (limiting constraint: {allocation.limiting_constraint_name}). Manual approval required."
        )
    else:
        final_verdict = Verdict.HOLD
        tac_btc = float(portfolio_snapshot.btc_tactical or 0.0)
        if previous_operating_state in {PortfolioState.DATA_HALT, PortfolioState.HUMAN_REVIEW}:
            new_state = PortfolioState.USDT_100 if tac_btc <= 1e-8 else PortfolioState.BTC_HOLD
        elif previous_operating_state in {
            PortfolioState.BTC_ACCUMULATION,
            PortfolioState.RE_ACCUMULATION,
            PortfolioState.BTC_REDUCTION,
            PortfolioState.BTC_DEFENSIVE,
            PortfolioState.ROTATION_TO_USDT,
        }:
            new_state = PortfolioState.USDT_100 if tac_btc <= 1e-8 else PortfolioState.BTC_HOLD
        else:
            new_state = previous_operating_state
        transition_reason = (
            " ; ".join(dict.fromkeys(reasons))
            if reasons
            else "No qualified BUY or SELL setup; maintaining current inventory."
        )

    proposed_order: dict[str, Any] | None = None
    if final_verdict == Verdict.BUY and allocation.buy_sizing is not None:
        bs = allocation.buy_sizing
        proposed_order = {
            "instrument": "BTC/USDT",
            "order_type": "LIMIT",
            "side": "BUY",
            "loop": LoopType.LOOP_A.value,
            "limit_price": bs.proposed_limit_price,
            "quantity_btc": bs.permitted_qty_btc,
            "notional_usdt": bs.gross_usdt,
            "estimated_fee_usdt": bs.estimated_fee_usdt,
            "total_cost_usdt": bs.net_usdt,
            "invalidation_condition": f"Risk invalidation reference <= {bs.invalidation_price}",
            "expiry_utc": module_a.setup_expiry_utc,
            "execution_note": "PROPOSED ONLY — Manual operator approval and external execution required.",
        }
    elif final_verdict == Verdict.SELL and allocation.sell_sizing is not None:
        ss = allocation.sell_sizing
        proposed_order = {
            "instrument": "BTC/USDT",
            "order_type": "LIMIT",
            "side": "SELL",
            "loop": LoopType.LOOP_B.value,
            "exit_classification": module_b.exit_classification.value if module_b.exit_classification else None,
            "limit_price": ss.proposed_limit_price,
            "quantity_btc": ss.permitted_qty_btc,
            "gross_usdt_proceeds": ss.gross_usdt,
            "estimated_fee_usdt": ss.estimated_fee_usdt,
            "net_usdt_proceeds": ss.net_usdt,
            "invalidation_condition": f"Invalidation reference >= {module_b.invalidation_price}" if module_b.invalidation_price else "Setup invalidated",
            "expiry_utc": module_b.setup_expiry_utc,
            "execution_note": "PROPOSED ONLY — Manual operator approval and external execution required.",
        }

    gates.append(
        GateResult(
            gate_number=10,
            gate_name="Final Verdict",
            status="PASS" if final_verdict != Verdict.ABSTAIN else "FAIL",
            summary=f"Verdict={final_verdict.value} | State={previous_operating_state.value} -> {new_state.value}",
            details={"verdict": final_verdict.value, "new_state": new_state.value},
        )
    )

    plain_summary = (
        f"Verdict: {final_verdict.value} | Operating State: {new_state.value} | "
        f"Regime: {regime_label} | Mode: {config.operating_mode.value} ({config.validation_status}). "
        f"{transition_reason}"
    )

    # Hash deterministic inputs + outcomes (excluding random UUIDs) for reproducible replay
    deterministic_payload = {
        "market_sha256": market_snapshot.snapshot_sha256,
        "portfolio": {
            "configured": portfolio_snapshot.configured,
            "btc_total": portfolio_snapshot.btc_total,
            "btc_tactical_available": portfolio_snapshot.btc_tactical_available,
            "btc_core_protected": portfolio_snapshot.btc_core_protected,
            "usdt_tactical_available": portfolio_snapshot.usdt_tactical_available,
            "reconciliation_status": portfolio_snapshot.reconciliation_status.value,
        },
        "config_version": config.config_version,
        "previous_operating_state": previous_operating_state.value,
        "module_a": {
            "state": module_a.state.value,
            "signal": module_a.directional_signal,
            "checklist": [(c.name, c.status) for c in module_a.checklist],
        },
        "module_b": {
            "state": module_b.state.value,
            "signal": module_b.directional_signal,
            "exit": module_b.exit_classification.value if module_b.exit_classification else None,
            "checklist": [(c.name, c.status) for c in module_b.checklist],
        },
        "gates": [(g.gate_number, g.status) for g in gates],
        "final_verdict": final_verdict.value,
        "new_operating_state": new_state.value,
        "proposed_order": proposed_order,
    }

    decision = DecisionRecord(
        decision_id=f"DEC-{uuid.uuid4().hex[:12].upper()}",
        timestamp_utc=ts_iso,
        market_snapshot_id=market_snapshot.snapshot_id,
        portfolio_snapshot_id=portfolio_snapshot.portfolio_snapshot_id,
        config_version=config.config_version,
        software_version=SOFTWARE_VERSION,
        operating_mode=config.operating_mode,
        validation_status=config.validation_status,
        data_integrity_status=market_snapshot.overall_integrity_status.value,
        regime_label=regime_label,
        gates=gates,
        module_a_assessment_id=module_a.assessment_id,
        module_b_assessment_id=module_b.assessment_id,
        allocation_assessment_id=allocation.allocation_id,
        final_verdict=final_verdict,
        previous_operating_state=previous_operating_state,
        new_operating_state=new_state,
        state_transition_reason=transition_reason,
        proposed_order=proposed_order,
        rejection_or_abstention_reasons=list(dict.fromkeys(reasons)),
        plain_english_summary=plain_summary,
        determinism_sha256=canonical_sha256(deterministic_payload),
    )
    return decision, allocation


def run_decision_cycle(
    *,
    market_snapshot: MarketSnapshot,
    ledger: PortfolioLedger,
    config: ConfigurationRecord,
    previous_operating_state: PortfolioState = PortfolioState.USDT_100,
    evidence_inputs_a: dict[str, Any] | None = None,
    evidence_inputs_b: dict[str, Any] | None = None,
    evidence_inputs_regime: dict[str, Any] | None = None,
    create_proposed_order: bool = False,
    audit_logger: AuditLogger | None = None,
    now_utc: str | None = None,
) -> dict[str, Any]:
    """
    End-to-end deterministic controller invocation:
    1. Evaluate Module A (non-authoritative)
    2. Evaluate Module B (non-authoritative)
    3. Snapshot PortfolioLedger
    4. Run Module C & Module D 10-gate reconciliation
    5. Optionally register a PROPOSED limit order (idempotent by snapshot_id)
    6. Record DecisionRecord & state transition in AuditLogger
    """
    ts_iso = ensure_utc_iso(now_utc or market_snapshot.retrieved_ts_utc or utc_now(), field_name="now_utc")
    mod_a = evaluate_module_a(market_snapshot, config, evidence_inputs=evidence_inputs_a, now_utc=ts_iso)
    mod_b = evaluate_module_b(market_snapshot, config, evidence_inputs=evidence_inputs_b, now_utc=ts_iso)
    prt = ledger.snapshot(spot_price=market_snapshot.spot_price, config_version=config.config_version, now_utc=ts_iso)

    # Idempotency check: if this exact snapshot + config_version already produced an order,
    # reuse the existing OrderRecord and never duplicate orders or reservations.
    existing_order: OrderRecord | None = None
    idem_prefix = f"DECISION:{market_snapshot.snapshot_id}:{config.config_version}:"
    for key, oid in ledger.idempotency_index.items():
        if key.startswith(idem_prefix) and oid in ledger.orders:
            existing_order = ledger.orders[oid]
            break

    decision, allocation = evaluate_final_decision(
        market_snapshot=market_snapshot,
        portfolio_snapshot=prt,
        module_a=mod_a,
        module_b=mod_b,
        config=config,
        previous_operating_state=previous_operating_state,
        open_orders=list(ledger.orders.values()),
        evidence_inputs=evidence_inputs_regime,
        now_utc=ts_iso,
    )

    order_record: OrderRecord | None = existing_order
    if existing_order is None and create_proposed_order and decision.proposed_order is not None:
        po = decision.proposed_order
        idem_key = f"{idem_prefix}{po['side']}"
        order_record = ledger.propose_order(
            idempotency_key=idem_key,
            side=po["side"],
            limit_price=float(po["limit_price"]),
            quantity_btc=float(po["quantity_btc"]),
            estimated_fee_usdt=float(po["estimated_fee_usdt"]),
            loop=LoopType(po["loop"]),
            invalidation_condition=str(po["invalidation_condition"]),
            config=config,
            decision_id=decision.decision_id,
            assessment_id=mod_a.assessment_id if po["side"] == "BUY" else mod_b.assessment_id,
            expiry_utc=po.get("expiry_utc"),
            now_utc=ts_iso,
        )

    logger = audit_logger or ledger.audit_logger
    logger.record(
        "DECISION_RECORDED",
        actor="MODULE_D_AUTHORITY",
        summary=decision.plain_english_summary,
        details=decision.to_dict(),
        timestamp_utc=ts_iso,
    )
    if decision.previous_operating_state != decision.new_operating_state:
        logger.record(
            "PORTFOLIO_STATE_TRANSITION",
            actor="MODULE_D_AUTHORITY",
            summary=f"{decision.previous_operating_state.value} -> {decision.new_operating_state.value}",
            details={
                "previous_state": decision.previous_operating_state.value,
                "new_state": decision.new_operating_state.value,
                "decision_id": decision.decision_id,
                "verdict": decision.final_verdict.value,
                "config_version": config.config_version,
                "reason": decision.state_transition_reason,
            },
            timestamp_utc=ts_iso,
        )

    return {
        "decision": decision,
        "module_a": mod_a,
        "module_b": mod_b,
        "allocation": allocation,
        "portfolio": prt,
        "proposed_order_record": order_record,
    }
