"""
Phase 6 Verification Suite — Historical Replay, Backtesting & Walk-Forward Validation.
"""

from __future__ import annotations

from pathlib import Path

from btc_config_loader import initialize_default_config, update_config
from cortex_core.backtest import HistoricalBar, run_backtest, run_walk_forward_validation
from cortex_core.constants import UNVALIDATED


def _bt_config(tmp_path: Path, *, expiry_min: int = 120):
    cfg_path = tmp_path / "bt_cfg.json"
    hist_path = tmp_path / "bt_hist.jsonl"
    initialize_default_config(cfg_path, hist_path, now_utc="2026-11-01T00:00:00Z")
    return update_config(
        {
            "portfolio_policy": {
                "active_tactical_sleeve_pct": 100.0,
                "min_btc_inventory_floor": 0.0,
                "min_usdt_inventory_floor": 0.0,
                "max_transaction_size_usdt": 10000.0,
                "portfolio_risk_budget_pct": 2.0,
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
            },
            "market_regime_rules": {
                "constructive": {"require_above_sma50_and_sma200": True},
                "cautious": {"mixed_ma": True},
                "defensive": {"below_sma200": True},
                "dislocation_extreme_risk": {"max_vix": 40.0},
            },
            "buy_criteria": {
                "min_confirmations": 6,
                "cvd_threshold_btc": 0.0,
                "reclaim_rule": "4H_VAH_RECLAIM",
                "max_stop_distance_pct": 8.0,
            },
            "sell_criteria": {
                "profit_taking": {"target_price_usdt": 68000.0, "trim_pct": 50.0},
                "risk_reduction": {"spot_cvd_max_btc": -400.0, "trim_pct": 50.0},
                "defensive_exit": {"spot_cvd_max_btc": -1000.0},
            },
            "execution_assumptions": {
                "order_expiry_minutes": expiry_min,
                "maker_fee_bps": 10.0,
                "taker_fee_bps": 10.0,
                "expected_slippage_bps": 5.0,
            },
        },
        operator_id="op_bt",
        change_reason="Configure explicit backtest assumptions",
        config_path=cfg_path,
        history_path=hist_path,
        now_utc="2026-11-01T00:05:00Z",
    )


def test_backtest_anti_lookahead_and_unfilled_expiry(tmp_path: Path) -> None:
    cfg = _bt_config(tmp_path, expiry_min=60)
    # Bar 0 proposes BUY limit @ 60000 even though Bar 0 low is 59000 (must NOT fill on Bar 0!)
    # Bar 1 & Bar 2 stay above 61000 -> order expires without fill!
    bars = [
        HistoricalBar(
            timestamp_utc="2026-11-01T01:00:00Z",
            open=61000, high=62000, low=59000, close=61500,
            sma50=60000, sma200=58000, rsi14=45, range_high_45d=68000, range_low_45d=59000,
            spot_cvd_24h_btc=300.0,
            evidence_inputs_a={
                "downside_sweep_detected": True,
                "absorption_detected": True,
                "reclaim_confirmed": True,
                "proposed_limit_buy_price": 60000.0,
                "invalidation_price": 57500.0,
            },
        ),
        HistoricalBar(
            timestamp_utc="2026-11-01T02:00:00Z",
            open=61500, high=62500, low=61200, close=62000,
            sma50=60000, sma200=58000, rsi14=48, range_high_45d=68000, range_low_45d=59000,
            spot_cvd_24h_btc=150.0,
        ),
        HistoricalBar(
            timestamp_utc="2026-11-01T03:00:00Z",
            open=62000, high=63000, low=61500, close=62500,
            sma50=60000, sma200=58000, rsi14=50, range_high_45d=68000, range_low_45d=59000,
            spot_cvd_24h_btc=100.0,
        ),
    ]
    rep = run_backtest(bars, cfg, mode="COMBINED_CORTEX", initial_tactical_usdt=10000.0)
    assert rep.validation_status == UNVALIDATED
    assert rep.proposed_orders_count == 1
    assert rep.filled_orders_count == 0
    assert rep.unfilled_expired_orders_count == 1
    assert rep.final_tactical_btc == 0.0
    assert rep.final_tactical_usdt == 10000.0


def test_backtest_combined_rotation_benchmarks_and_determinism(tmp_path: Path) -> None:
    cfg = _bt_config(tmp_path, expiry_min=240)
    bars = [
        # Bar 0: Qualified BUY @ 62000
        HistoricalBar(
            timestamp_utc="2026-11-01T01:00:00Z",
            open=62500, high=63000, low=61800, close=62500,
            sma50=61000, sma200=59000, rsi14=44, range_high_45d=69000, range_low_45d=61000,
            spot_cvd_24h_btc=300.0,
            evidence_inputs_a={
                "downside_sweep_detected": True,
                "absorption_detected": True,
                "reclaim_confirmed": True,
                "proposed_limit_buy_price": 62000.0,
                "invalidation_price": 59500.0,
            },
        ),
        # Bar 1: Dips to 61800 -> BUY fills at Bar 1
        HistoricalBar(
            timestamp_utc="2026-11-01T02:00:00Z",
            open=62400, high=64000, low=61800, close=63800,
            sma50=61000, sma200=59000, rsi14=52, range_high_45d=69000, range_low_45d=61000,
            spot_cvd_24h_btc=400.0,
        ),
        # Bar 2: Data unavailable -> ABSTAIN / DATA HALT, no crash
        HistoricalBar(
            timestamp_utc="2026-11-01T03:00:00Z",
            open=65000, high=66000, low=64500, close=65500,
            data_unavailable=True,
        ),
        # Bar 3: Rally to 68500 -> Profit-taking SELL proposed @ 68500
        HistoricalBar(
            timestamp_utc="2026-11-01T04:00:00Z",
            open=66000, high=68600, low=65800, close=68500,
            sma50=62000, sma200=59500, rsi14=70, range_high_45d=69000, range_low_45d=61000,
            spot_cvd_24h_btc=100.0,
            evidence_inputs_b={"proposed_limit_sell_price": 68500.0},
        ),
        # Bar 4: High reaches 69000 -> SELL fills
        HistoricalBar(
            timestamp_utc="2026-11-01T05:00:00Z",
            open=68500, high=69000, low=67500, close=68000,
            sma50=62000, sma200=59500, rsi14=66, range_high_45d=69000, range_low_45d=61000,
            spot_cvd_24h_btc=50.0,
        ),
    ]

    rep1 = run_backtest(bars, cfg, mode="COMBINED_CORTEX", initial_tactical_usdt=10000.0)
    rep2 = run_backtest(bars, cfg, mode="COMBINED_CORTEX", initial_tactical_usdt=10000.0)

    assert rep1.validation_status == UNVALIDATED
    assert rep1.filled_orders_count == 2
    assert rep1.completed_round_trips == 1
    assert rep1.total_fees_usdt > 0
    assert rep1.final_equity_usdt > 10000.0
    assert "btc_buy_and_hold" in rep1.benchmarks
    assert "usdt_100" in rep1.benchmarks
    assert "static_50_50" in rep1.benchmarks
    assert rep1.equity_curve[2]["verdict"] == "ABSTAIN"
    assert rep1.determinism_sha256 == rep2.determinism_sha256


def test_walk_forward_validation_all_three_stages(tmp_path: Path) -> None:
    cfg = _bt_config(tmp_path, expiry_min=240)
    bars = [
        HistoricalBar(
            timestamp_utc=f"2026-11-0{i+1}T01:00:00Z",
            open=62000 + i * 500,
            high=63000 + i * 500,
            low=61500 + i * 500,
            close=62500 + i * 500,
            sma50=61000,
            sma200=59000,
            rsi14=50,
            range_high_45d=70000,
            range_low_45d=60000,
            spot_cvd_24h_btc=200.0,
        )
        for i in range(6)
    ]
    wf = run_walk_forward_validation(bars, cfg, in_sample_ratio=0.5, initial_tactical_btc=0.1, initial_tactical_usdt=5000.0)
    assert wf["validation_status"] == UNVALIDATED
    assert set(wf["stages"].keys()) == {"MODULE_A_ONLY", "MODULE_B_ONLY", "COMBINED_CORTEX"}
    assert wf["in_sample_window"]["bars"] == 3
    assert wf["out_of_sample_window"]["bars"] == 3
