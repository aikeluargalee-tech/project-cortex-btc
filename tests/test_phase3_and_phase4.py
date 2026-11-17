"""
Phase 3 & Phase 4 Verification Suite — Module C (Portfolio Allocation Controller)
& Module D (10-Gate Final Decision Authority).

Covers all Section 20 mandatory acceptance tests for conflict resolution,
data halts, balance reconciliation, core protection, BUY/SELL sizing,
three separate selling mechanisms, 100% USDT holding, idempotency,
and deterministic historical replay.
"""

from __future__ import annotations

from pathlib import Path

from btc_config_loader import initialize_default_config, update_config
from cortex_core.audit import AuditLogger
from cortex_core.constants import (
    NOT_CONFIGURED,
    ExitClassification,
    PortfolioState,
    Verdict,
)
from cortex_core.ledger import PortfolioLedger
from cortex_core.market_data import build_market_snapshot
from cortex_core.module_c import calculate_buy_sizing, calculate_sell_sizing
from cortex_core.module_d import run_decision_cycle


def _full_config(tmp_path: Path, name: str = "cfg"):
    cfg_path = tmp_path / f"{name}.json"
    hist_path = tmp_path / f"{name}_hist.jsonl"
    audit = AuditLogger(tmp_path / f"{name}_audit.jsonl")
    initialize_default_config(cfg_path, hist_path, now_utc="2026-11-17T01:00:00Z", audit_logger=audit)
    cfg = update_config(
        {
            "portfolio_policy": {
                "active_tactical_sleeve_pct": 20.0,
                "min_btc_inventory_floor": 0.0,
                "min_usdt_inventory_floor": 500.0,
                "max_transaction_size_usdt": 10000.0,
                "portfolio_risk_budget_pct": 0.75,
            },
            "exposure_bands": {
                "defensive": {"btc_pct": 0.0, "usdt_pct": 100.0},
                "cautious": {"btc_pct": 25.0, "usdt_pct": 75.0},
                "neutral": {"btc_pct": 50.0, "usdt_pct": 50.0},
                "constructive": {"btc_pct": 75.0, "usdt_pct": 25.0},
                "strongly_constructive": {"btc_pct": 100.0, "usdt_pct": 0.0},
            },
            "data_policy": {
                "spot_price_max_age_minutes": 90,
                "spot_cvd_max_age_minutes": 90,
                "order_book_max_age_minutes": 90,
                "stale_spot_cvd_blocks_decision": True,
            },
            "market_regime_rules": {
                "constructive": {"require_above_sma50_and_sma200": True},
                "cautious": {"mixed_ma": True},
                "defensive": {"below_sma200": True},
                "dislocation_extreme_risk": {"max_vix": 35.0, "min_rsi14": 22.0},
            },
            "buy_criteria": {
                "min_confirmations": 6,
                "cvd_threshold_btc": 0.0,
                "reclaim_rule": "4H_VAH_RECLAIM",
                "max_stop_distance_pct": 5.0,
            },
            "sell_criteria": {
                "profit_taking": {"target_price_usdt": 72000.0, "trim_pct": 25.0},
                "risk_reduction": {"spot_cvd_max_btc": -500.0, "trim_pct": 40.0},
                "defensive_exit": {"spot_cvd_max_btc": -1000.0},
            },
            "execution_assumptions": {
                "order_expiry_minutes": 240,
                "maker_fee_bps": 10.0,
                "taker_fee_bps": 10.0,
                "expected_slippage_bps": 5.0,
            },
        },
        operator_id="op_test",
        change_reason="Configure explicit research rules for Phase 3 & 4 tests",
        config_path=cfg_path,
        history_path=hist_path,
        now_utc="2026-11-17T01:05:00Z",
        audit_logger=audit,
    )
    return cfg, audit


def _raw_market(
    *,
    spot: float = 65000.0,
    sma50: float = 64000.0,
    sma200: float = 62000.0,
    rsi14: float = 48.0,
    spot_cvd: float = 300.0,
    vix: float = 18.0,
    ts: str = "2026-11-17T02:00:00Z",
) -> dict:
    return {
        "as_of_utc": ts,
        "spot_price": spot,
        "venues": {
            "binance": {"price": spot, "timestamp_utc": ts},
            "coinbase": {"price": spot - 5.0, "timestamp_utc": ts},
            "coingecko": {"price": spot - 2.0, "timestamp_utc": ts},
            "okx": {"price": spot + 4.0, "timestamp_utc": ts},
        },
        "price": {
            "spot": spot,
            "sma50": sma50,
            "sma200": sma200,
            "rsi14": rsi14,
            "range_high_45d": 70000.0,
            "range_low_45d": 60000.0,
        },
        "liquidity": {"spread_bps": 0.5, "depth_1pct_usd": 12_000_000.0},
        "derivatives": {
            "open_interest": {"current_btc": 30000.0, "change_24h_pct": -1.5},
            "funding_rate_pct": 0.005,
            "long_short_ratio": 1.2,
            "perp_cvd": {"24h": {"cvd_btc": 100.0}},
        },
        "order_flow": {"spot_cvd_binance": {"24h": {"cvd_btc": spot_cvd}}},
        "macro": {"vix": {"value": vix, "as_of_utc": "2026-11-16", "source": "FRED:VIXCLS"}},
    }


def _buy_ok_evidence(limit_px: float = 65000.0, stop_px: float = 63000.0) -> dict:
    return {
        "downside_sweep_detected": True,
        "absorption_detected": True,
        "reclaim_confirmed": True,
        "proposed_limit_buy_price": limit_px,
        "invalidation_price": stop_px,
    }


def _sell_rr_evidence(limit_px: float = 69500.0) -> dict:
    return {
        "upside_sweep_or_resistance_test": True,
        "failed_reclaim_confirmed": True,
        "supply_absorption_detected": True,
        "value_area_loss_or_failed_reclaim": True,
        "proposed_limit_sell_price": limit_px,
    }


def test_module_c_buy_and_sell_sizing_lowest_constraint_and_core_protection(tmp_path: Path) -> None:
    cfg, audit = _full_config(tmp_path)
    ledger = PortfolioLedger(state_path=tmp_path / "ledger.json", audit_logger=audit)
    ledger.configure_balances(
        btc_core_protected=1.00,  # $65,000 protected core
        btc_tactical=0.10,        # $6,500 tactical BTC
        usdt_tactical=6500.0,     # $6,500 tactical USDT
        operator_id="op_test",
        reason="Init",
        now_utc="2026-11-17T01:10:00Z",
    )
    prt = ledger.snapshot(spot_price=65000.0, config_version=cfg.config_version, now_utc="2026-11-17T02:00:00Z")

    # BUY sizing: total equity = $78,000; 0.75% risk = $585. Stop dist = 2000 + ~97.5 fee/slip -> ~0.278 BTC
    # Tactical sleeve = $13,000; 75% target = $9,750 -> headroom $3,250 = 0.05 BTC -> band limits!
    buy_s = calculate_buy_sizing(
        portfolio=prt,
        config=cfg,
        limit_price=65000.0,
        invalidation_price=63000.0,
        target_btc_pct=75.0,
    )
    assert buy_s.sizing_status == "ELIGIBLE"
    assert buy_s.limiting_constraint_name == "target_exposure_band"
    assert buy_s.permitted_qty_btc == 0.05
    assert buy_s.core_btc_intact is True
    assert buy_s.inventory_floor_compliant is True

    # SELL sizing: PROFIT-TAKING trims 25% of 0.10 tactical = 0.025 BTC (core 1.00 untouched)
    pt_s = calculate_sell_sizing(
        portfolio=prt,
        config=cfg,
        limit_price=72000.0,
        exit_classification=ExitClassification.PROFIT_TAKING,
    )
    assert pt_s.sizing_status == "ELIGIBLE"
    assert pt_s.limiting_constraint_name == "profit_taking_trim_cap"
    assert pt_s.permitted_qty_btc == 0.025
    assert pt_s.core_btc_intact is True

    # SELL sizing: DEFENSIVE EXIT permits 100% of tactical (0.10 BTC), still never touches 1.00 core!
    de_s = calculate_sell_sizing(
        portfolio=prt,
        config=cfg,
        limit_price=59000.0,
        exit_classification=ExitClassification.DEFENSIVE_EXIT,
    )
    assert de_s.sizing_status == "ELIGIBLE"
    assert de_s.permitted_qty_btc == 0.10
    assert de_s.remaining_available_btc == 0.0
    assert de_s.core_btc_intact is True


def test_section20_conflict_handling_no_contradictory_or_forced_trades(tmp_path: Path) -> None:
    cfg, audit = _full_config(tmp_path)
    ledger = PortfolioLedger(state_path=tmp_path / "ledger.json", audit_logger=audit)
    ledger.configure_balances(
        btc_core_protected=0.80,
        btc_tactical=0.10,
        usdt_tactical=8000.0,
        operator_id="op_test",
        reason="Init",
        now_utc="2026-11-17T01:10:00Z",
    )

    # Case A: Module A reports BUY while Module B reports SETUP deterioration -> NO independent BUY
    snap = build_market_snapshot(_raw_market(spot=65000.0, spot_cvd=200.0), config=cfg, now_utc="2026-11-17T02:00:00Z")
    res_conflict_a = run_decision_cycle(
        market_snapshot=snap,
        ledger=ledger,
        config=cfg,
        previous_operating_state=PortfolioState.BTC_HOLD,
        evidence_inputs_a=_buy_ok_evidence(),
        evidence_inputs_b={
            "upside_sweep_or_resistance_test": True,
            "supply_absorption_detected": True,
            "failed_reclaim_confirmed": False,
            "value_area_loss_or_failed_reclaim": False,
        },
        now_utc="2026-11-17T02:00:00Z",
    )
    assert res_conflict_a["decision"].final_verdict == Verdict.HOLD
    assert res_conflict_a["decision"].proposed_order is None

    # Case B: Module B reports SELL while Module A identifies accumulation SETUP -> ABSTAIN / HUMAN REVIEW
    snap_sell = build_market_snapshot(_raw_market(spot=69500.0, spot_cvd=-800.0), config=cfg, now_utc="2026-11-17T02:01:00Z")
    res_conflict_b = run_decision_cycle(
        market_snapshot=snap_sell,
        ledger=ledger,
        config=cfg,
        previous_operating_state=PortfolioState.BTC_HOLD,
        evidence_inputs_a={
            "downside_sweep_detected": True,
            "absorption_detected": True,
            "reclaim_confirmed": False,
        },
        evidence_inputs_b=_sell_rr_evidence(),
        now_utc="2026-11-17T02:01:00Z",
    )
    assert res_conflict_b["decision"].final_verdict == Verdict.ABSTAIN
    assert res_conflict_b["decision"].new_operating_state == PortfolioState.HUMAN_REVIEW
    assert res_conflict_b["decision"].proposed_order is None


def test_section20_data_halt_and_balance_reconciliation_abstain(tmp_path: Path) -> None:
    cfg, audit = _full_config(tmp_path)
    ledger = PortfolioLedger(state_path=tmp_path / "ledger.json", audit_logger=audit)
    ledger.configure_balances(
        btc_core_protected=0.80,
        btc_tactical=0.10,
        usdt_tactical=8000.0,
        operator_id="op_test",
        reason="Init",
        now_utc="2026-11-17T01:10:00Z",
    )

    # 1. Stale Spot CVD -> Gate 1 fails -> ABSTAIN / DATA HALT
    stale_snap = build_market_snapshot(
        _raw_market(ts="2026-11-17T02:00:00Z"),
        config=cfg,
        now_utc="2026-11-17T04:00:00Z",
    )
    res_stale = run_decision_cycle(
        market_snapshot=stale_snap,
        ledger=ledger,
        config=cfg,
        previous_operating_state=PortfolioState.BTC_HOLD,
        evidence_inputs_a=_buy_ok_evidence(),
        now_utc="2026-11-17T04:00:00Z",
    )
    assert res_stale["decision"].final_verdict == Verdict.ABSTAIN
    assert res_stale["decision"].new_operating_state == PortfolioState.DATA_HALT

    # 2. Critical spot unavailable -> ABSTAIN / DATA HALT
    empty_snap = build_market_snapshot({}, config=cfg, now_utc="2026-11-17T02:00:00Z")
    res_empty = run_decision_cycle(
        market_snapshot=empty_snap,
        ledger=ledger,
        config=cfg,
        previous_operating_state=PortfolioState.BTC_HOLD,
        now_utc="2026-11-17T02:00:00Z",
    )
    assert res_empty["decision"].final_verdict == Verdict.ABSTAIN
    assert res_empty["decision"].new_operating_state == PortfolioState.DATA_HALT

    # 3. Balance reconciliation mismatch -> ABSTAIN / HUMAN REVIEW
    ledger.reconcile_balances(
        reported_btc_total=0.75,  # mismatch vs 0.90
        reported_usdt_total=8000.0,
        source="exchange_check",
        now_utc="2026-11-17T02:05:00Z",
    )
    ok_snap = build_market_snapshot(_raw_market(), config=cfg, now_utc="2026-11-17T02:06:00Z")
    res_rec = run_decision_cycle(
        market_snapshot=ok_snap,
        ledger=ledger,
        config=cfg,
        previous_operating_state=PortfolioState.BTC_HOLD,
        evidence_inputs_a=_buy_ok_evidence(),
        now_utc="2026-11-17T02:06:00Z",
    )
    assert res_rec["decision"].final_verdict == Verdict.ABSTAIN
    assert res_rec["decision"].new_operating_state == PortfolioState.HUMAN_REVIEW


def test_section20_unfunded_buy_unsupported_sell_and_100pct_usdt_hold(tmp_path: Path) -> None:
    cfg, audit = _full_config(tmp_path)
    ledger = PortfolioLedger(state_path=tmp_path / "ledger.json", audit_logger=audit)
    # 1.00 core BTC protected, 0.00 tactical BTC, 400 USDT (< 500 USDT floor!)
    ledger.configure_balances(
        btc_core_protected=1.00,
        btc_tactical=0.0,
        usdt_tactical=400.0,
        operator_id="op_test",
        reason="Edge inventory",
        now_utc="2026-11-17T01:10:00Z",
    )

    # Qualified BUY, but USDT <= min_usdt_inventory_floor (500) -> HOLD (never unfunded BUY)
    snap_buy = build_market_snapshot(_raw_market(spot=65000.0, spot_cvd=300.0), config=cfg, now_utc="2026-11-17T02:00:00Z")
    res_no_usdt = run_decision_cycle(
        market_snapshot=snap_buy,
        ledger=ledger,
        config=cfg,
        previous_operating_state=PortfolioState.USDT_100,
        evidence_inputs_a=_buy_ok_evidence(),
        now_utc="2026-11-17T02:00:00Z",
    )
    assert res_no_usdt["decision"].final_verdict == Verdict.HOLD
    assert res_no_usdt["decision"].proposed_order is None
    assert res_no_usdt["decision"].new_operating_state == PortfolioState.USDT_100

    # Qualified SELL, but 0.0 tactical BTC (only 1.00 protected core BTC) -> HOLD (never touches core)
    snap_sell = build_market_snapshot(_raw_market(spot=69500.0, spot_cvd=-800.0), config=cfg, now_utc="2026-11-17T02:01:00Z")
    res_no_btc = run_decision_cycle(
        market_snapshot=snap_sell,
        ledger=ledger,
        config=cfg,
        previous_operating_state=PortfolioState.USDT_100,
        evidence_inputs_b=_sell_rr_evidence(),
        now_utc="2026-11-17T02:01:00Z",
    )
    assert res_no_btc["decision"].final_verdict == Verdict.HOLD
    assert res_no_btc["decision"].proposed_order is None
    assert res_no_btc["decision"].new_operating_state == PortfolioState.USDT_100


def test_section20_idempotent_decision_and_deterministic_replay(tmp_path: Path) -> None:
    cfg, audit = _full_config(tmp_path)
    ledger = PortfolioLedger(state_path=tmp_path / "ledger.json", audit_logger=audit)
    ledger.configure_balances(
        btc_core_protected=0.80,
        btc_tactical=0.05,
        usdt_tactical=8000.0,
        operator_id="op_test",
        reason="Init",
        now_utc="2026-11-17T01:10:00Z",
    )
    snap = build_market_snapshot(_raw_market(spot=65000.0, spot_cvd=350.0), config=cfg, now_utc="2026-11-17T02:00:00Z")

    # Run identical snapshot twice with create_proposed_order=True
    r1 = run_decision_cycle(
        market_snapshot=snap,
        ledger=ledger,
        config=cfg,
        previous_operating_state=PortfolioState.USDT_100,
        evidence_inputs_a=_buy_ok_evidence(),
        create_proposed_order=True,
        now_utc="2026-11-17T02:00:00Z",
    )
    assert r1["decision"].final_verdict == Verdict.BUY
    assert r1["decision"].new_operating_state == PortfolioState.RE_ACCUMULATION
    assert r1["proposed_order_record"] is not None
    orders_count_after_first = len(ledger.orders)
    reserved_after_first = float(ledger.usdt_reserved)

    # Second run on same snapshot creates NO duplicate order or duplicated reservation
    r2 = run_decision_cycle(
        market_snapshot=snap,
        ledger=ledger,
        config=cfg,
        previous_operating_state=PortfolioState.USDT_100,
        evidence_inputs_a=_buy_ok_evidence(),
        create_proposed_order=True,
        now_utc="2026-11-17T02:00:00Z",
    )
    assert len(ledger.orders) == orders_count_after_first == 1
    assert float(ledger.usdt_reserved) == reserved_after_first
    assert r2["proposed_order_record"].order_id == r1["proposed_order_record"].order_id

    # Replay from scratch in a separate ledger -> exact same verdict, state, and determinism_sha256
    cfg2, audit2 = _full_config(tmp_path, name="cfg_replay")
    ledger2 = PortfolioLedger(state_path=tmp_path / "ledger2.json", audit_logger=audit2)
    ledger2.configure_balances(
        btc_core_protected=0.80,
        btc_tactical=0.05,
        usdt_tactical=8000.0,
        operator_id="op_test",
        reason="Replay",
        now_utc="2026-11-17T01:10:00Z",
    )
    snap2 = build_market_snapshot(_raw_market(spot=65000.0, spot_cvd=350.0), config=cfg2, now_utc="2026-11-17T02:00:00Z")
    r_replay = run_decision_cycle(
        market_snapshot=snap2,
        ledger=ledger2,
        config=cfg2,
        previous_operating_state=PortfolioState.USDT_100,
        evidence_inputs_a=_buy_ok_evidence(),
        create_proposed_order=False,
        now_utc="2026-11-17T02:00:00Z",
    )
    assert r_replay["decision"].final_verdict == r1["decision"].final_verdict
    assert r_replay["decision"].new_operating_state == r1["decision"].new_operating_state
    assert r_replay["decision"].determinism_sha256 == r1["decision"].determinism_sha256


def test_defensive_exit_rotates_tactical_to_usdt_while_preserving_core(tmp_path: Path) -> None:
    cfg, audit = _full_config(tmp_path)
    ledger = PortfolioLedger(state_path=tmp_path / "ledger.json", audit_logger=audit)
    ledger.configure_balances(
        btc_core_protected=0.80,
        btc_tactical=0.10,
        usdt_tactical=2000.0,
        operator_id="op_test",
        reason="Init",
        now_utc="2026-11-17T01:10:00Z",
    )
    snap = build_market_snapshot(
        _raw_market(spot=59000.0, sma50=66000.0, sma200=62000.0, rsi14=32.0, spot_cvd=-1500.0),
        config=cfg,
        now_utc="2026-11-17T02:00:00Z",
    )
    res = run_decision_cycle(
        market_snapshot=snap,
        ledger=ledger,
        config=cfg,
        previous_operating_state=PortfolioState.BTC_HOLD,
        evidence_inputs_b={
            "structural_breakdown_confirmed": True,
            "failed_reclaim_confirmed": True,
            "supply_absorption_detected": True,
            "value_area_loss_or_failed_reclaim": True,
            "htf_thesis_invalidated": True,
            "proposed_limit_sell_price": 59000.0,
        },
        create_proposed_order=True,
        now_utc="2026-11-17T02:00:00Z",
    )
    assert res["decision"].final_verdict == Verdict.SELL
    assert res["decision"].new_operating_state == PortfolioState.ROTATION_TO_USDT
    assert res["decision"].proposed_order["quantity_btc"] == 0.10
    assert res["decision"].proposed_order["exit_classification"] == ExitClassification.DEFENSIVE_EXIT.value
    # Core BTC remains 0.80 untouched!
    assert float(ledger.btc_core_protected) == 0.80
    assert float(ledger.btc_reserved) == 0.10
