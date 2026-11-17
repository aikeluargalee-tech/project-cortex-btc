"""
Module B — Bearish: Distribution & Breakdown (Phase 2).

Identifies qualified opportunities to convert existing tactical BTC into USDT
without independent execution authority (has_execution_authority = False).
Evaluates three distinct selling mechanisms separately:
  1. PROFIT-TAKING
  2. RISK REDUCTION
  3. DEFENSIVE EXIT
Never authorizes a sale solely on resistance touch, high RSI, or negative Futures CVD alone.
"""

from __future__ import annotations

import uuid
from datetime import timedelta
from typing import Any

from btc_config_loader import get_param
from cortex_core.constants import (
    NOT_CONFIGURED,
    DataStatus,
    ExitClassification,
    ModuleState,
)
from cortex_core.evidence_common import (
    check_data_integrity,
    evaluate_execution_economics,
    field_info,
    summarize_checklist,
)
from cortex_core.models import (
    ConfigurationRecord,
    EvidenceCheckItem,
    MarketSnapshot,
    ModuleAssessment,
)
from cortex_core.time_utils import ensure_utc_iso, parse_utc_timestamp, utc_now


def _evaluate_profit_taking(
    *,
    spot_val: float | None,
    cfg_pt: Any,
    ev: dict[str, Any],
) -> dict[str, Any]:
    if cfg_pt == NOT_CONFIGURED or not isinstance(cfg_pt, dict):
        return {
            "status": NOT_CONFIGURED,
            "qualified": False,
            "rationale": "sell_criteria.profit_taking is NOT CONFIGURED.",
        }
    target_px = cfg_pt.get("target_price_usdt")
    if target_px in (NOT_CONFIGURED, None):
        return {
            "status": NOT_CONFIGURED,
            "qualified": False,
            "rationale": "sell_criteria.profit_taking.target_price_usdt is NOT CONFIGURED.",
        }
    if spot_val is None:
        return {
            "status": "UNAVAILABLE",
            "qualified": False,
            "rationale": "Spot price unavailable for profit-target evaluation.",
        }
    target_hit = float(spot_val) >= float(target_px) or bool(ev.get("profit_target_reached"))
    return {
        "status": "PASS" if target_hit else "FAIL",
        "qualified": target_hit,
        "target_price_usdt": float(target_px),
        "rationale": (
            f"Spot {spot_val:.2f} reached configured profit-taking target {float(target_px):.2f}."
            if target_hit
            else f"Spot {spot_val:.2f} below profit-taking target {float(target_px):.2f}."
        ),
    }


def _evaluate_risk_reduction(
    *,
    cfg_rr: Any,
    status_by_name: dict[str, str],
    bearish_pattern: str | None,
) -> dict[str, Any]:
    if cfg_rr == NOT_CONFIGURED or not isinstance(cfg_rr, dict):
        return {
            "status": NOT_CONFIGURED,
            "qualified": False,
            "rationale": "sell_criteria.risk_reduction is NOT CONFIGURED.",
        }
    required_ok = (
        status_by_name.get("resistance_or_supply_region") == "PASS"
        and status_by_name.get("distribution_or_breakdown_structure") == "PASS"
        and status_by_name.get("spot_cvd_deterioration") == "PASS"
        and status_by_name.get("supply_absorption_and_footprint") == "PASS"
        and status_by_name.get("value_area_loss_or_failed_reclaim") == "PASS"
        and status_by_name.get("anti_mechanical_sell_guard") == "PASS"
        and status_by_name.get("execution_economics") == "PASS"
    )
    return {
        "status": "PASS" if required_ok else "FAIL",
        "qualified": required_ok,
        "bearish_pattern": bearish_pattern,
        "rationale": (
            "Confirmed distribution / spot deterioration qualifies partial RISK REDUCTION."
            if required_ok
            else "Distribution and spot-deterioration gates do not all pass for RISK REDUCTION."
        ),
    }


def _evaluate_defensive_exit(
    *,
    cfg_de: Any,
    status_by_name: dict[str, str],
    ev: dict[str, Any],
    spot_val: float | None,
    sma200: float | None,
) -> dict[str, Any]:
    if cfg_de == NOT_CONFIGURED or not isinstance(cfg_de, dict):
        return {
            "status": NOT_CONFIGURED,
            "qualified": False,
            "rationale": "sell_criteria.defensive_exit is NOT CONFIGURED.",
        }
    htf_invalidated = bool(ev.get("htf_thesis_invalidated")) or bool(
        ev.get("structural_breakdown_confirmed") and spot_val is not None and sma200 is not None and spot_val < sma200
    )
    spot_deteriorating = status_by_name.get("spot_cvd_deterioration") == "PASS"
    exec_ok = status_by_name.get("execution_economics") == "PASS"
    qualified = htf_invalidated and spot_deteriorating and exec_ok
    return {
        "status": "PASS" if qualified else "FAIL",
        "qualified": qualified,
        "htf_thesis_invalidated": htf_invalidated,
        "rationale": (
            "Higher-timeframe thesis invalidated with spot breakdown; DEFENSIVE EXIT assessment triggered (respects core BTC protection)."
            if qualified
            else "Higher-timeframe defensive-exit invalidation criteria not met."
        ),
    }


def evaluate_module_b(
    snapshot: MarketSnapshot,
    config: ConfigurationRecord,
    *,
    evidence_inputs: dict[str, Any] | None = None,
    now_utc: str | None = None,
) -> ModuleAssessment:
    """
    Deterministically evaluate Module B (Bearish Distribution & Breakdown).

    Returns a non-authoritative ModuleAssessment with state, directional_signal
    ('SELL' | 'REDUCE' | 'HOLD' | 'WAIT'), exit_classification, and per-mechanism
    evaluations.
    """
    ts_iso = ensure_utc_iso(now_utc or snapshot.retrieved_ts_utc or utc_now(), field_name="now_utc")
    ev = evidence_inputs or {}
    checklist: list[EvidenceCheckItem] = []

    # 1. Critical data integrity
    data_item, data_halted = check_data_integrity(snapshot, config)
    checklist.append(data_item)

    spot_val, _ = field_info(snapshot, "spot_price")
    sma50, _ = field_info(snapshot, "sma50")
    sma200, _ = field_info(snapshot, "sma200")
    rsi14, _ = field_info(snapshot, "rsi14")
    r_high, _ = field_info(snapshot, "range_high_45d")
    r_low, _ = field_info(snapshot, "range_low_45d")
    spot_cvd, spot_cvd_st = field_info(snapshot, "spot_cvd_24h_btc")
    perp_cvd, _ = field_info(snapshot, "perp_cvd_24h_btc")
    oi_chg, _ = field_info(snapshot, "oi_change_24h_pct")

    # 2. Resistance / supply region or breakdown context
    upside_sweep = ev.get("upside_sweep_or_resistance_test")
    structural_breakdown = ev.get("structural_breakdown_confirmed")
    resistance_ref = ev.get("resistance_reference_usdt", r_high)
    if upside_sweep is None and structural_breakdown is None:
        checklist.append(
            EvidenceCheckItem(
                name="resistance_or_supply_region",
                status="UNAVAILABLE",
                observed_value={"resistance_reference_usdt": resistance_ref, "spot": spot_val},
                source_status=DataStatus.UNAVAILABLE.value,
                rationale="Upside sweep / resistance test / breakdown structure telemetry unavailable.",
                is_mandatory=True,
            )
        )
    else:
        res_ok = bool(upside_sweep or structural_breakdown)
        checklist.append(
            EvidenceCheckItem(
                name="resistance_or_supply_region",
                status="PASS" if res_ok else "FAIL",
                observed_value={
                    "upside_sweep_or_resistance_test": upside_sweep,
                    "structural_breakdown_confirmed": structural_breakdown,
                    "resistance_reference_usdt": resistance_ref,
                },
                source_status=DataStatus.VERIFIED.value,
                rationale=(
                    "Price tested resistance/supply region or broke established structural support."
                    if res_ok
                    else "No resistance rejection test or structural breakdown observed."
                ),
                is_mandatory=True,
            )
        )

    # 3. Distinguish genuine distribution / breakdown from ordinary consolidation
    failed_reclaim = ev.get("failed_reclaim_confirmed")
    ordinary_consolidation = bool(ev.get("ordinary_uptrend_consolidation", False))
    bearish_pattern: str | None = None
    if structural_breakdown:
        bearish_pattern = "STRUCTURAL_BREAKDOWN"
    elif failed_reclaim and upside_sweep:
        bearish_pattern = "DISTRIBUTION_REVERSAL"

    if failed_reclaim is None and structural_breakdown is None:
        checklist.append(
            EvidenceCheckItem(
                name="distribution_or_breakdown_structure",
                status="UNAVAILABLE",
                observed_value={"failed_reclaim_confirmed": None, "structural_breakdown_confirmed": None},
                source_status=DataStatus.UNAVAILABLE.value,
                rationale="Auction failed-reclaim / breakdown candle confirmation unavailable.",
                is_mandatory=True,
            )
        )
    else:
        dist_ok = bool((failed_reclaim or structural_breakdown) and not ordinary_consolidation)
        checklist.append(
            EvidenceCheckItem(
                name="distribution_or_breakdown_structure",
                status="PASS" if dist_ok else "FAIL",
                observed_value={
                    "bearish_pattern": bearish_pattern,
                    "ordinary_uptrend_consolidation": ordinary_consolidation,
                },
                source_status=DataStatus.VERIFIED.value,
                rationale=(
                    f"Confirmed {bearish_pattern} distinct from ordinary uptrend consolidation."
                    if dist_ok
                    else "Structure reflects ordinary consolidation or unconfirmed rejection."
                ),
                is_mandatory=True,
            )
        )

    # 4. Spot CVD deterioration (separate threshold from Module A)
    cfg_rr = get_param(config, "sell_criteria.risk_reduction")
    cfg_de = get_param(config, "sell_criteria.defensive_exit")
    cfg_pt = get_param(config, "sell_criteria.profit_taking")

    sell_cvd_thresh: Any = NOT_CONFIGURED
    if isinstance(cfg_rr, dict) and cfg_rr.get("spot_cvd_max_btc") not in (NOT_CONFIGURED, None):
        sell_cvd_thresh = cfg_rr["spot_cvd_max_btc"]
    elif isinstance(cfg_de, dict) and cfg_de.get("spot_cvd_max_btc") not in (NOT_CONFIGURED, None):
        sell_cvd_thresh = cfg_de["spot_cvd_max_btc"]

    if spot_cvd is None or spot_cvd_st == DataStatus.UNAVAILABLE:
        checklist.append(
            EvidenceCheckItem(
                name="spot_cvd_deterioration",
                status="UNAVAILABLE",
                observed_value=None,
                source_status=DataStatus.UNAVAILABLE.value,
                rationale="Spot CVD telemetry unavailable.",
                is_mandatory=True,
            )
        )
    elif sell_cvd_thresh == NOT_CONFIGURED:
        checklist.append(
            EvidenceCheckItem(
                name="spot_cvd_deterioration",
                status=NOT_CONFIGURED,
                observed_value=spot_cvd,
                source_status=spot_cvd_st.value,
                rationale="Bearish spot_cvd_max_btc threshold is NOT CONFIGURED.",
                is_mandatory=True,
            )
        )
    else:
        cvd_weak = float(spot_cvd) <= float(sell_cvd_thresh)
        checklist.append(
            EvidenceCheckItem(
                name="spot_cvd_deterioration",
                status="PASS" if cvd_weak else "FAIL",
                observed_value={"spot_cvd_24h_btc": spot_cvd, "threshold": float(sell_cvd_thresh)},
                source_status=spot_cvd_st.value,
                rationale=(
                    f"Spot CVD ({spot_cvd:+.2f} BTC, {spot_cvd_st.value}) <= {float(sell_cvd_thresh):+.2f} BTC."
                    if cvd_weak
                    else f"Spot CVD ({spot_cvd:+.2f} BTC, {spot_cvd_st.value}) has not deteriorated below {float(sell_cvd_thresh):+.2f} BTC."
                ),
                is_mandatory=True,
            )
        )

    # 5. Supply absorption & footprint evidence
    supply_abs = ev.get("supply_absorption_detected")
    if supply_abs is None:
        checklist.append(
            EvidenceCheckItem(
                name="supply_absorption_and_footprint",
                status="UNAVAILABLE",
                observed_value={"supply_absorption_detected": None},
                source_status=DataStatus.UNAVAILABLE.value,
                rationale="Supply absorption / ask-wall footprint telemetry unavailable.",
                is_mandatory=True,
            )
        )
    else:
        checklist.append(
            EvidenceCheckItem(
                name="supply_absorption_and_footprint",
                status="PASS" if bool(supply_abs) else "FAIL",
                observed_value={"supply_absorption_detected": bool(supply_abs)},
                source_status=DataStatus.VERIFIED.value,
                rationale=(
                    "Aggressive buying absorbed by supply without sustained upward displacement."
                    if supply_abs
                    else "No supply absorption evidence detected."
                ),
                is_mandatory=True,
            )
        )

    # 6. Value-area loss or failed reclaim
    va_loss = ev.get("value_area_loss_or_failed_reclaim")
    if va_loss is None:
        checklist.append(
            EvidenceCheckItem(
                name="value_area_loss_or_failed_reclaim",
                status="UNAVAILABLE",
                observed_value={"value_area_loss_or_failed_reclaim": None},
                source_status=DataStatus.UNAVAILABLE.value,
                rationale="Volume-profile value-area loss / failed reclaim telemetry unavailable.",
                is_mandatory=True,
            )
        )
    else:
        checklist.append(
            EvidenceCheckItem(
                name="value_area_loss_or_failed_reclaim",
                status="PASS" if bool(va_loss) else "FAIL",
                observed_value={"value_area_loss_or_failed_reclaim": bool(va_loss)},
                source_status=DataStatus.VERIFIED.value,
                rationale=(
                    "Value-area loss or failed upside reclaim confirmed."
                    if va_loss
                    else "Price holds value-area acceptance."
                ),
                is_mandatory=True,
            )
        )

    # 7. Derivatives context guard: negative Futures CVD or falling OI alone NEVER triggers SELL
    checklist.append(
        EvidenceCheckItem(
            name="derivatives_context_guard",
            status="CONTEXT" if (perp_cvd is not None or oi_chg is not None) else "UNAVAILABLE",
            observed_value={"perp_cvd_24h_btc": perp_cvd, "oi_change_24h_pct": oi_chg},
            source_status=DataStatus.VERIFIED.value if (perp_cvd is not None or oi_chg is not None) else DataStatus.UNAVAILABLE.value,
            rationale="Derivatives telemetry is context only; negative Futures CVD or falling OI alone never authorizes a BTC sale.",
            is_mandatory=False,
        )
    )

    # 8. Anti-mechanical sell guard: resistance touch or high RSI alone never authorizes SELL
    status_by_name = {c.name: c.status for c in checklist}
    spot_and_structure_confirmed = (
        status_by_name.get("distribution_or_breakdown_structure") == "PASS"
        and status_by_name.get("spot_cvd_deterioration") == "PASS"
    )
    checklist.append(
        EvidenceCheckItem(
            name="anti_mechanical_sell_guard",
            status="PASS" if spot_and_structure_confirmed else "FAIL",
            observed_value={"rsi14": rsi14, "spot_and_structure_confirmed": spot_and_structure_confirmed},
            source_status=DataStatus.VERIFIED.value if rsi14 is not None else DataStatus.UNAVAILABLE.value,
            rationale=(
                "Actual spot and structural deterioration confirmed beyond resistance touch / RSI."
                if spot_and_structure_confirmed
                else "Resistance touch, high RSI, or derivatives pressure alone cannot authorize a sale."
            ),
            is_mandatory=True,
        )
    )

    # 9. Execution economics
    proposed_limit = ev.get("proposed_limit_sell_price")
    if proposed_limit is None and spot_val is not None:
        proposed_limit = float(spot_val)
    invalidation_px = ev.get("invalidation_price")
    exec_item = evaluate_execution_economics(
        snapshot,
        config,
        side="SELL",
        proposed_limit_price=proposed_limit,
        invalidation_price=invalidation_px,
    )
    checklist.append(exec_item)

    status_by_name = {c.name: c.status for c in checklist}

    # Evaluate the three separate selling mechanisms independently
    pt_eval = _evaluate_profit_taking(spot_val=spot_val, cfg_pt=cfg_pt, ev=ev)
    rr_eval = _evaluate_risk_reduction(cfg_rr=cfg_rr, status_by_name=status_by_name, bearish_pattern=bearish_pattern)
    de_eval = _evaluate_defensive_exit(
        cfg_de=cfg_de,
        status_by_name=status_by_name,
        ev=ev,
        spot_val=spot_val,
        sma200=sma200,
    )
    mechanism_evaluations = {
        ExitClassification.PROFIT_TAKING.value: pt_eval,
        ExitClassification.RISK_REDUCTION.value: rr_eval,
        ExitClassification.DEFENSIVE_EXIT.value: de_eval,
    }

    qualifying, failed, unavailable, unconfigured = summarize_checklist(checklist)

    # Select exit classification & Module B state/signal (strictly non-authoritative)
    exit_classification: ExitClassification | None = None
    if de_eval["qualified"] and not data_halted:
        exit_classification = ExitClassification.DEFENSIVE_EXIT
    elif rr_eval["qualified"] and not data_halted:
        exit_classification = ExitClassification.RISK_REDUCTION
    elif pt_eval["qualified"] and not data_halted and status_by_name.get("execution_economics") == "PASS":
        exit_classification = ExitClassification.PROFIT_TAKING
        if bearish_pattern is None:
            bearish_pattern = "PROFIT_TARGET"

    expiry_min = get_param(config, "execution_assumptions.order_expiry_minutes")
    setup_expiry_utc: str | None = None
    if expiry_min not in (NOT_CONFIGURED, None):
        dt = parse_utc_timestamp(ts_iso)
        if dt is not None:
            setup_expiry_utc = (dt + timedelta(minutes=float(expiry_min))).strftime("%Y-%m-%dT%H:%M:%SZ")

    if data_halted:
        state = ModuleState.DATA_HALT
        directional_signal = "WAIT"
    elif ev.get("setup_invalidated"):
        state = ModuleState.INVALIDATED
        directional_signal = "HOLD"
    elif exit_classification == ExitClassification.DEFENSIVE_EXIT:
        state = ModuleState.ELIGIBLE
        directional_signal = "SELL"
    elif exit_classification in {ExitClassification.RISK_REDUCTION, ExitClassification.PROFIT_TAKING}:
        state = ModuleState.ELIGIBLE
        directional_signal = "REDUCE"
    elif status_by_name.get("resistance_or_supply_region") == "PASS" and (
        status_by_name.get("spot_cvd_deterioration") == "PASS"
        or status_by_name.get("supply_absorption_and_footprint") == "PASS"
    ):
        state = ModuleState.SETUP
        directional_signal = "WAIT"
    else:
        state = ModuleState.WATCH
        directional_signal = "HOLD" if not failed else "WAIT"

    return ModuleAssessment(
        assessment_id=f"MODB-{uuid.uuid4().hex[:12].upper()}",
        module_name="MODULE_B_DISTRIBUTION",
        setup_id=str(ev.get("setup_id") or f"SETUP-B-{ts_iso[:10]}"),
        timestamp_utc=ts_iso,
        market_snapshot_id=snapshot.snapshot_id,
        config_version=config.config_version,
        state=state,
        directional_signal=directional_signal,
        has_execution_authority=False,
        exit_classification=exit_classification,
        bearish_pattern=bearish_pattern,
        checklist=checklist,
        qualifying_conditions=qualifying,
        failed_conditions=failed,
        unavailable_data=unavailable,
        unconfigured_thresholds=unconfigured,
        mechanism_evaluations=mechanism_evaluations,
        proposed_limit_price=float(proposed_limit) if (exit_classification is not None and proposed_limit is not None) else None,
        invalidation_price=float(invalidation_px) if invalidation_px is not None else None,
        setup_expiry_utc=setup_expiry_utc,
        observed_summary=f"Spot={spot_val}, SMA200={sma200}, RSI14={rsi14}, SpotCVD={spot_cvd} ({spot_cvd_st.value}), PerpCVD={perp_cvd}.",
        interpretation_summary=f"Module B state={state.value}, signal={directional_signal}, exit={exit_classification.value if exit_classification else 'NONE'}.",
    )
