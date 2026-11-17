"""
Phase 2 Verification Suite — Module A (Bullish Accumulation) & Module B (Bearish Distribution).

Verifies independent, non-symmetric evidence matrices, strict non-authoritative
posture (has_execution_authority=False), NOT CONFIGURED / DATA UNAVAILABLE
honesty, anti-falling-knife / anti-mechanical-sell guards, and separate evaluation
of the three selling mechanisms (PROFIT-TAKING, RISK REDUCTION, DEFENSIVE EXIT).
"""

from __future__ import annotations

import json
from pathlib import Path

from btc_config_loader import initialize_default_config, update_config
from cortex_core.constants import NOT_CONFIGURED, ExitClassification, ModuleState
from cortex_core.market_data import build_market_snapshot
from cortex_core.module_a import evaluate_module_a
from cortex_core.module_b import evaluate_module_b


def _base_raw_metrics(
    *,
    spot: float = 65000.0,
    sma50: float = 64000.0,
    sma200: float = 62000.0,
    rsi14: float = 48.0,
    spot_cvd: float = 250.0,
    perp_cvd: float = -1200.0,
    oi_chg: float = -2.0,
) -> dict:
    return {
        "as_of_utc": "2026-11-17T02:00:00Z",
        "spot_price": spot,
        "venues": {
            "binance": {"price": spot, "timestamp_utc": "2026-11-17T01:59:50Z"},
            "coinbase": {"price": spot - 10.0, "timestamp_utc": "2026-11-17T01:59:51Z"},
            "coingecko": {"price": spot - 5.0, "timestamp_utc": "2026-11-17T01:59:00Z"},
            "okx": {"price": spot + 5.0, "timestamp_utc": "2026-11-17T01:59:52Z"},
        },
        "price": {
            "spot": spot,
            "sma50": sma50,
            "sma200": sma200,
            "rsi14": rsi14,
            "range_high_45d": 70000.0,
            "range_low_45d": 60000.0,
        },
        "liquidity": {"spread_bps": 0.5, "depth_1pct_usd": 10_000_000.0},
        "derivatives": {
            "open_interest": {"current_btc": 30000.0, "change_24h_pct": oi_chg},
            "funding_rate_pct": 0.005,
            "long_short_ratio": 1.3,
            "perp_cvd": {"24h": {"cvd_btc": perp_cvd}},
        },
        "order_flow": {"spot_cvd_binance": {"24h": {"cvd_btc": spot_cvd}}},
    }


def _configured_research_cfg(tmp_path: Path):
    cfg_path = tmp_path / "cfg.json"
    hist_path = tmp_path / "hist.jsonl"
    initialize_default_config(cfg_path, hist_path, now_utc="2026-11-17T01:00:00Z")
    return update_config(
        {
            "data_policy": {
                "spot_price_max_age_minutes": 90,
                "spot_cvd_max_age_minutes": 90,
                "order_book_max_age_minutes": 90,
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
        change_reason="Configure explicit research criteria for Phase 2 testing",
        config_path=cfg_path,
        history_path=hist_path,
        now_utc="2026-11-17T01:05:00Z",
    )


def test_unconfigured_thresholds_never_emit_buy_or_sell(tmp_path: Path) -> None:
    cfg = initialize_default_config(tmp_path / "c.json", tmp_path / "h.jsonl")
    snap = build_market_snapshot(_base_raw_metrics(), config=cfg, now_utc="2026-11-17T02:00:00Z")

    mod_a = evaluate_module_a(snap, cfg, now_utc="2026-11-17T02:00:00Z")
    mod_b = evaluate_module_b(snap, cfg, now_utc="2026-11-17T02:00:00Z")

    assert mod_a.has_execution_authority is False
    assert mod_b.has_execution_authority is False
    assert mod_a.directional_signal == "WAIT"
    assert mod_b.directional_signal in {"WAIT", "HOLD"}
    assert len(mod_a.unconfigured_thresholds) >= 2
    assert len(mod_b.unconfigured_thresholds) >= 2
    assert mod_b.mechanism_evaluations[ExitClassification.PROFIT_TAKING.value]["status"] == NOT_CONFIGURED


def test_data_halt_on_missing_or_stale_critical_feeds(tmp_path: Path) -> None:
    cfg = _configured_research_cfg(tmp_path)
    # Stale spot CVD (> 90 min old)
    stale_snap = build_market_snapshot(
        _base_raw_metrics(),
        config=cfg,
        now_utc="2026-11-17T04:00:00Z",
    )
    mod_a = evaluate_module_a(stale_snap, cfg, now_utc="2026-11-17T04:00:00Z")
    mod_b = evaluate_module_b(stale_snap, cfg, now_utc="2026-11-17T04:00:00Z")

    assert mod_a.state == ModuleState.DATA_HALT
    assert mod_b.state == ModuleState.DATA_HALT
    assert mod_a.directional_signal == "WAIT"
    assert mod_b.directional_signal == "WAIT"


def test_anti_falling_knife_and_qualified_module_a(tmp_path: Path) -> None:
    cfg = _configured_research_cfg(tmp_path)
    # Sharp drop + oversold RSI=20 without absorption/reclaim/positive CVD -> MUST NOT qualify BUY
    knife_snap = build_market_snapshot(
        _base_raw_metrics(spot=58000.0, sma50=66000.0, sma200=62000.0, rsi14=20.0, spot_cvd=-1500.0),
        config=cfg,
        now_utc="2026-11-17T02:01:00Z",
    )
    knife_res = evaluate_module_a(
        knife_snap,
        cfg,
        evidence_inputs={
            "downside_sweep_detected": True,
            "absorption_detected": False,
            "reclaim_confirmed": False,
            "proposed_limit_buy_price": 58000.0,
            "invalidation_price": 56500.0,
        },
        now_utc="2026-11-17T02:01:00Z",
    )
    assert knife_res.directional_signal == "WAIT"
    assert knife_res.state != ModuleState.ELIGIBLE

    # Fully qualified accumulation setup
    ok_snap = build_market_snapshot(
        _base_raw_metrics(spot=63500.0, sma50=64000.0, sma200=62000.0, rsi14=42.0, spot_cvd=450.0),
        config=cfg,
        now_utc="2026-11-17T02:02:00Z",
    )
    ok_res = evaluate_module_a(
        ok_snap,
        cfg,
        evidence_inputs={
            "downside_sweep_detected": True,
            "absorption_detected": True,
            "reclaim_confirmed": True,
            "proposed_limit_buy_price": 63500.0,
            "invalidation_price": 61800.0,
        },
        now_utc="2026-11-17T02:02:00Z",
    )
    assert ok_res.state == ModuleState.ELIGIBLE
    assert ok_res.directional_signal == "BUY"
    assert ok_res.has_execution_authority is False
    assert ok_res.proposed_limit_price == 63500.0
    assert ok_res.invalidation_price == 61800.0


def test_anti_mechanical_sell_and_three_selling_mechanisms(tmp_path: Path) -> None:
    cfg = _configured_research_cfg(tmp_path)

    # 1. Resistance touch + high RSI + negative Perp CVD WITHOUT spot deterioration -> NO SELL
    res_touch_snap = build_market_snapshot(
        _base_raw_metrics(spot=70000.0, rsi14=79.0, spot_cvd=200.0, perp_cvd=-15000.0, oi_chg=-8.0),
        config=cfg,
        now_utc="2026-11-17T02:01:00Z",
    )
    no_sell = evaluate_module_b(
        res_touch_snap,
        cfg,
        evidence_inputs={
            "upside_sweep_or_resistance_test": True,
            "failed_reclaim_confirmed": False,
            "ordinary_uptrend_consolidation": True,
            "supply_absorption_detected": False,
            "value_area_loss_or_failed_reclaim": False,
        },
        now_utc="2026-11-17T02:01:00Z",
    )
    assert no_sell.directional_signal in {"HOLD", "WAIT"}
    assert no_sell.exit_classification is None

    # 2. PROFIT-TAKING (target 72,000 hit without structural breakdown)
    pt_snap = build_market_snapshot(
        _base_raw_metrics(spot=72500.0, rsi14=68.0, spot_cvd=300.0),
        config=cfg,
        now_utc="2026-11-17T02:02:00Z",
    )
    pt_res = evaluate_module_b(
        pt_snap,
        cfg,
        evidence_inputs={"proposed_limit_sell_price": 72500.0},
        now_utc="2026-11-17T02:02:00Z",
    )
    assert pt_res.state == ModuleState.ELIGIBLE
    assert pt_res.directional_signal == "REDUCE"
    assert pt_res.exit_classification == ExitClassification.PROFIT_TAKING
    assert pt_res.mechanism_evaluations[ExitClassification.RISK_REDUCTION.value]["qualified"] is False
    assert pt_res.mechanism_evaluations[ExitClassification.DEFENSIVE_EXIT.value]["qualified"] is False

    # 3. RISK REDUCTION (confirmed distribution + spot CVD deterioration)
    rr_snap = build_market_snapshot(
        _base_raw_metrics(spot=69500.0, rsi14=58.0, spot_cvd=-850.0),
        config=cfg,
        now_utc="2026-11-17T02:03:00Z",
    )
    rr_res = evaluate_module_b(
        rr_snap,
        cfg,
        evidence_inputs={
            "upside_sweep_or_resistance_test": True,
            "failed_reclaim_confirmed": True,
            "supply_absorption_detected": True,
            "value_area_loss_or_failed_reclaim": True,
            "proposed_limit_sell_price": 69500.0,
        },
        now_utc="2026-11-17T02:03:00Z",
    )
    assert rr_res.state == ModuleState.ELIGIBLE
    assert rr_res.directional_signal == "REDUCE"
    assert rr_res.exit_classification == ExitClassification.RISK_REDUCTION
    assert rr_res.bearish_pattern == "DISTRIBUTION_REVERSAL"

    # 4. DEFENSIVE EXIT (HTF thesis invalidated below SMA200 + structural breakdown)
    de_snap = build_market_snapshot(
        _base_raw_metrics(spot=59000.0, sma50=66000.0, sma200=62000.0, rsi14=33.0, spot_cvd=-1800.0),
        config=cfg,
        now_utc="2026-11-17T02:04:00Z",
    )
    de_res = evaluate_module_b(
        de_snap,
        cfg,
        evidence_inputs={
            "structural_breakdown_confirmed": True,
            "failed_reclaim_confirmed": True,
            "supply_absorption_detected": True,
            "value_area_loss_or_failed_reclaim": True,
            "htf_thesis_invalidated": True,
            "proposed_limit_sell_price": 59000.0,
        },
        now_utc="2026-11-17T02:04:00Z",
    )
    assert de_res.state == ModuleState.ELIGIBLE
    assert de_res.directional_signal == "SELL"
    assert de_res.exit_classification == ExitClassification.DEFENSIVE_EXIT
    assert de_res.bearish_pattern == "STRUCTURAL_BREAKDOWN"
    assert de_res.has_execution_authority is False


def test_real_metrics_smoke_for_both_modules(tmp_path: Path) -> None:
    metrics_path = Path(__file__).resolve().parent.parent / "btc_metrics_latest.json"
    if not metrics_path.exists():
        return
    raw = json.loads(metrics_path.read_text(encoding="utf-8"))
    cfg = initialize_default_config(tmp_path / "c.json", tmp_path / "h.jsonl")
    snap = build_market_snapshot(raw, config=cfg, now_utc=raw.get("as_of_utc"))

    mod_a = evaluate_module_a(snap, cfg, now_utc=raw.get("as_of_utc"))
    mod_b = evaluate_module_b(snap, cfg, now_utc=raw.get("as_of_utc"))
    assert mod_a.has_execution_authority is False
    assert mod_b.has_execution_authority is False
    assert mod_a.directional_signal == "WAIT"
    assert mod_b.directional_signal in {"WAIT", "HOLD"}
