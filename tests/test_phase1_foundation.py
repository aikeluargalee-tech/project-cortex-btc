"""
Phase 1 Foundation & Portfolio Ledger Verification Suite.

Covers configuration versioning, fail-closed market data classification,
UTC/MYT timestamp discipline, dual-inventory BTC/USDT ledger accounting,
reservations, core-holding protection, partial fills, unconfirmed
cancellations, balance reconciliation, idempotency, and Loop A/B cycles.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from btc_config_loader import (
    ConfigValidationError,
    get_param,
    initialize_default_config,
    load_config,
    read_config_history,
    update_config,
)
from cortex_core.audit import AuditLogger
from cortex_core.constants import (
    DATA_UNAVAILABLE,
    NOT_CONFIGURED,
    UNVALIDATED,
    CycleStatus,
    DataStatus,
    LoopType,
    OrderStatus,
    ReconciliationStatus,
)
from cortex_core.ledger import (
    InsufficientInventoryError,
    LedgerError,
    OrderLifecycleError,
    PortfolioLedger,
    ProtectedCoreViolationError,
    ReconciliationDiscrepancyError,
)
from cortex_core.market_data import build_market_snapshot
from cortex_core.time_utils import format_myt, parse_utc_timestamp, to_utc_iso


# ---------------------------------------------------------------------------
# 1. Configuration & Governance Tests
# ---------------------------------------------------------------------------

def test_default_config_marks_unestablished_params_not_configured(tmp_path: Path) -> None:
    cfg_path = tmp_path / "config.json"
    hist_path = tmp_path / "history.jsonl"
    audit = AuditLogger(tmp_path / "audit.jsonl")

    cfg = initialize_default_config(cfg_path, hist_path, now_utc="2026-11-17T02:00:00Z", audit_logger=audit)

    assert cfg.config_version == 1
    assert cfg.validation_status == UNVALIDATED
    assert cfg.spot_only is True
    assert cfg.autonomous_execution is False
    assert cfg.instrument == "BTC/USDT"
    assert get_param(cfg, "portfolio_policy.active_tactical_sleeve_pct") == NOT_CONFIGURED
    assert get_param(cfg, "portfolio_policy.min_btc_inventory_floor") == NOT_CONFIGURED
    assert get_param(cfg, "data_policy.spot_price_max_age_minutes") == NOT_CONFIGURED
    assert get_param(cfg, "execution_assumptions.maker_fee_bps") == NOT_CONFIGURED
    assert len(read_config_history(hist_path)) == 1


def test_config_updates_are_versioned_audited_and_protect_invariants(tmp_path: Path) -> None:
    cfg_path = tmp_path / "config.json"
    hist_path = tmp_path / "history.jsonl"
    audit = AuditLogger(tmp_path / "audit.jsonl")
    initialize_default_config(cfg_path, hist_path, now_utc="2026-11-17T02:00:00Z", audit_logger=audit)

    updated = update_config(
        {
            "data_policy": {"spot_price_max_age_minutes": 90, "spot_cvd_max_age_minutes": 90},
            "portfolio_policy": {"active_tactical_sleeve_pct": 20.0},
        },
        operator_id="operator_aikel",
        change_reason="Set initial telemetry freshness limits and 20% tactical sleeve.",
        config_path=cfg_path,
        history_path=hist_path,
        now_utc="2026-11-17T02:10:00Z",
        audit_logger=audit,
    )

    assert updated.config_version == 2
    assert updated.previous_values["data_policy.spot_price_max_age_minutes"] == NOT_CONFIGURED
    assert updated.new_values["data_policy.spot_price_max_age_minutes"] == 90
    assert updated.operator_id == "operator_aikel"
    assert updated.changed_at_utc == "2026-11-17T02:10:00Z"
    assert len(read_config_history(hist_path)) == 2

    # Attempting to enable leverage, futures, shorting, or autonomous execution fails
    for forbidden_key, forbidden_val in [
        ("leverage_allowed", True),
        ("margin_allowed", True),
        ("futures_execution_allowed", True),
        ("short_selling_allowed", True),
        ("autonomous_execution", True),
    ]:
        with pytest.raises(ConfigValidationError):
            update_config(
                {"invariants": {forbidden_key: forbidden_val}},
                operator_id="operator_aikel",
                change_reason="Attempt forbidden invariant override",
                config_path=cfg_path,
                history_path=hist_path,
            )

    # Reloaded config remains at v2
    reloaded = load_config(cfg_path)
    assert reloaded.config_version == 2


# ---------------------------------------------------------------------------
# 2. Timezone & Market Data Integrity Tests
# ---------------------------------------------------------------------------

def test_utc_storage_and_myt_display() -> None:
    utc_str = to_utc_iso("2026-11-16T18:18:55Z")
    assert utc_str == "2026-11-16T18:18:55Z"
    assert format_myt(utc_str) == "2026-11-17 02:18:55 MYT (UTC+8)"
    assert format_myt(None) == DATA_UNAVAILABLE
    assert parse_utc_timestamp(NOT_CONFIGURED) is None


def test_market_snapshot_preserves_provenance_and_flags_stale_or_missing(tmp_path: Path) -> None:
    cfg_path = tmp_path / "config.json"
    hist_path = tmp_path / "history.jsonl"
    initialize_default_config(cfg_path, hist_path, now_utc="2026-11-16T18:00:00Z")

    raw_sample = {
        "as_of_utc": "2026-11-16T18:19:00Z",
        "spot_price": 64907.78,
        "venues": {
            "binance": {"price": 64907.78, "timestamp_utc": "2026-11-16T18:18:55Z"},
            "coinbase": {"price": 64843.38, "timestamp_utc": "2026-11-16T18:18:56Z"},
            "coingecko": {"price": 64894.0, "timestamp_utc": "2026-11-16T18:17:45Z"},
            "kraken": {"price": 64841.9, "timestamp_utc": "2026-11-16T18:19:00Z"},  # equals retrieval time
            "okx": {"price": 64905.3, "timestamp_utc": "2026-11-16T18:18:57Z"},
        },
        "price": {
            "spot": 64907.78,
            "sma50": 79452.48,
            "sma200": 72921.28,
            "rsi14": 23.74,
            "range_high_45d": 86999.11,
            "range_low_45d": 62006.0,
        },
        "order_flow": {"spot_cvd_binance": {"24h": {"cvd_btc": -403.05}}},
        "macro": {"dxy": {"value": 121.88, "as_of_utc": "2026-11-06", "source": "FRED:DTWEXBGS"}},
    }

    # With unconfigured freshness limits -> freshness_status is NOT CONFIGURED
    cfg_v1 = load_config(cfg_path)
    snap_v1 = build_market_snapshot(raw_sample, config=cfg_v1, now_utc="2026-11-16T18:20:00Z")
    assert snap_v1.fields["binance_spot_price"].freshness_status == NOT_CONFIGURED
    assert snap_v1.fields["kraken_spot_price"].source_event_ts_utc is None  # did not substitute retrieval ts
    assert snap_v1.fields["spot_cvd_24h_btc"].validation_status == DataStatus.PROXY
    assert snap_v1.fields["dxy"].validation_status == DataStatus.PROXY
    assert snap_v1.fields["etf_net_flow_usd_m"].validation_status == DataStatus.UNAVAILABLE
    assert snap_v1.fields["confirmed_liquidations"].validation_status == DataStatus.UNAVAILABLE

    # Configure strict 15-min SLA -> 45-min old data becomes STALE
    cfg_v2 = update_config(
        {"data_policy": {"spot_price_max_age_minutes": 15, "spot_cvd_max_age_minutes": 15}},
        operator_id="op",
        change_reason="Enable 15m spot SLA",
        config_path=cfg_path,
        history_path=hist_path,
    )
    snap_stale = build_market_snapshot(raw_sample, config=cfg_v2, now_utc="2026-11-16T19:05:00Z")
    assert snap_stale.fields["binance_spot_price"].validation_status == DataStatus.STALE
    assert snap_stale.fields["spot_cvd_24h_btc"].validation_status == DataStatus.STALE
    assert snap_stale.overall_integrity_status == DataStatus.STALE

    # Missing spot price -> UNAVAILABLE
    snap_missing = build_market_snapshot({}, config=cfg_v2, now_utc="2026-11-16T18:20:00Z")
    assert snap_missing.spot_price is None
    assert snap_missing.overall_integrity_status == DataStatus.UNAVAILABLE


# ---------------------------------------------------------------------------
# 3. Dual-Inventory Ledger, Reservation & Section 20 Safety Tests
# ---------------------------------------------------------------------------

def _setup_ledger(tmp_path: Path) -> tuple[PortfolioLedger, object]:
    cfg_path = tmp_path / "config.json"
    hist_path = tmp_path / "history.jsonl"
    audit = AuditLogger(tmp_path / "audit.jsonl")
    initialize_default_config(cfg_path, hist_path, now_utc="2026-11-17T01:00:00Z", audit_logger=audit)
    cfg = update_config(
        {
            "portfolio_policy": {
                "active_tactical_sleeve_pct": 20.0,
                "min_btc_inventory_floor": 0.0,
                "min_usdt_inventory_floor": 0.0,
            }
        },
        operator_id="op_1",
        change_reason="Configure baseline sleeve and zero floor for testing",
        config_path=cfg_path,
        history_path=hist_path,
        audit_logger=audit,
    )
    ledger = PortfolioLedger(state_path=tmp_path / "ledger.json", audit_logger=audit)
    return ledger, cfg


def test_unconfigured_ledger_never_invents_zero_or_10k_balances(tmp_path: Path) -> None:
    ledger, cfg = _setup_ledger(tmp_path)
    snap = ledger.snapshot(spot_price=65000.0, config_version=cfg.config_version)
    assert snap.configured is False
    assert snap.btc_total is None
    assert snap.usdt_total is None
    assert snap.total_portfolio_value_usdt is None
    assert snap.reconciliation_status == ReconciliationStatus.NOT_CONFIGURED
    assert snap.display_field("btc_total") == NOT_CONFIGURED
    assert snap.display_field("usdt_total") == NOT_CONFIGURED


def test_spot_only_limits_reservations_and_core_protection(tmp_path: Path) -> None:
    ledger, cfg = _setup_ledger(tmp_path)
    ledger.configure_balances(
        btc_core_protected=0.80,
        btc_tactical=0.10,
        usdt_tactical=5000.0,
        operator_id="op_1",
        reason="Initial manual verification",
        now_utc="2026-11-17T01:05:00Z",
    )

    # 1. Proposed BUY exceeding available USDT -> rejected
    with pytest.raises(InsufficientInventoryError):
        ledger.propose_order(
            idempotency_key="snap-buy-over",
            side="BUY",
            limit_price=60000.0,
            quantity_btc=0.10,  # 6000 USDT > 5000 available
            estimated_fee_usdt=6.0,
            loop=LoopType.LOOP_A,
            invalidation_condition="Close < 58000",
            config=cfg,
            now_utc="2026-11-17T01:06:00Z",
        )

    # 2. Proposed SELL touching protected core BTC (0.80 core vs 0.10 tactical) -> rejected
    with pytest.raises(ProtectedCoreViolationError):
        ledger.propose_order(
            idempotency_key="snap-sell-core",
            side="SELL",
            limit_price=70000.0,
            quantity_btc=0.20,  # <= 0.90 total, but > 0.10 tactical
            estimated_fee_usdt=14.0,
            loop=LoopType.LOOP_B,
            invalidation_condition="Reclaim > 72000",
            config=cfg,
            now_utc="2026-11-17T01:07:00Z",
        )

    # 3. Proposed SELL > total BTC -> rejected
    with pytest.raises(InsufficientInventoryError):
        ledger.propose_order(
            idempotency_key="snap-sell-borrow",
            side="SELL",
            limit_price=70000.0,
            quantity_btc=1.50,
            estimated_fee_usdt=10.0,
            loop=LoopType.LOOP_B,
            invalidation_condition="Reclaim > 72000",
            config=cfg,
            now_utc="2026-11-17T01:08:00Z",
        )

    # 4. Double reservation of same BTC -> second rejected
    o_sell_1 = ledger.propose_order(
        idempotency_key="snap-sell-1",
        side="SELL",
        limit_price=70000.0,
        quantity_btc=0.06,
        estimated_fee_usdt=4.2,
        loop=LoopType.LOOP_B,
        invalidation_condition="Reclaim > 72000",
        config=cfg,
        now_utc="2026-11-17T01:09:00Z",
    )
    assert float(ledger.btc_tactical_available) == 0.04
    with pytest.raises(ProtectedCoreViolationError):
        ledger.propose_order(
            idempotency_key="snap-sell-2",
            side="SELL",
            limit_price=71000.0,
            quantity_btc=0.06,  # only 0.04 tactical BTC remains unreserved
            estimated_fee_usdt=4.26,
            loop=LoopType.LOOP_B,
            invalidation_condition="Reclaim > 73000",
            config=cfg,
            now_utc="2026-11-17T01:10:00Z",
        )

    # 5. Double reservation of same USDT -> second rejected
    o_buy_1 = ledger.propose_order(
        idempotency_key="snap-buy-1",
        side="BUY",
        limit_price=60000.0,
        quantity_btc=0.05,  # 3000 + 3 = 3003 USDT reserved
        estimated_fee_usdt=3.0,
        loop=LoopType.LOOP_A,
        invalidation_condition="Close < 58000",
        config=cfg,
        now_utc="2026-11-17T01:11:00Z",
    )
    assert float(ledger.usdt_tactical_available) == 1997.0
    with pytest.raises(InsufficientInventoryError):
        ledger.propose_order(
            idempotency_key="snap-buy-2",
            side="BUY",
            limit_price=60000.0,
            quantity_btc=0.04,  # 2400 > 1997 remaining
            estimated_fee_usdt=2.4,
            loop=LoopType.LOOP_A,
            invalidation_condition="Close < 58000",
            config=cfg,
            now_utc="2026-11-17T01:12:00Z",
        )

    # 6. Idempotency: processing the same snapshot twice creates no duplicate order/reservation
    o_buy_dup = ledger.propose_order(
        idempotency_key="snap-buy-1",
        side="BUY",
        limit_price=60000.0,
        quantity_btc=0.05,
        estimated_fee_usdt=3.0,
        loop=LoopType.LOOP_A,
        invalidation_condition="Close < 58000",
        config=cfg,
        now_utc="2026-11-17T01:13:00Z",
    )
    assert o_buy_dup.order_id == o_buy_1.order_id
    assert len(ledger.orders) == 2
    assert float(ledger.usdt_reserved) == 3003.0
    assert o_sell_1.status == OrderStatus.PROPOSED


def test_partial_fills_and_unconfirmed_cancellation_rules(tmp_path: Path) -> None:
    ledger, cfg = _setup_ledger(tmp_path)
    ledger.configure_balances(
        btc_core_protected=0.50,
        btc_tactical=0.10,
        usdt_tactical=0.0,
        operator_id="op_1",
        reason="Test partial fills & unconfirmed cancel",
        now_utc="2026-11-17T02:00:00Z",
    )

    order = ledger.propose_order(
        idempotency_key="snap-partial-sell",
        side="SELL",
        limit_price=70000.0,
        quantity_btc=0.10,
        estimated_fee_usdt=7.0,
        loop=LoopType.LOOP_B,
        invalidation_condition="Invalidated > 72000",
        config=cfg,
        now_utc="2026-11-17T02:01:00Z",
    )
    ledger.approve_order(order.order_id, operator_id="op_1", now_utc="2026-11-17T02:02:00Z")
    ledger.mark_submitted(order.order_id, operator_id="op_1", exchange_order_ref="EX-1001", now_utc="2026-11-17T02:03:00Z")
    ledger.mark_working(order.order_id, operator_id="op_1", now_utc="2026-11-17T02:04:00Z")

    # Partial fill of 0.04 BTC -> only 0.04 leaves BTC inventory; 0.06 remains reserved
    updated = ledger.record_fill(
        order.order_id,
        fill_qty_btc=0.04,
        fill_price_usdt=70000.0,
        fee_asset="USDT",
        fee_amount=2.8,
        exchange_fill_ref="FIL-1",
        recorded_by="op_1",
        now_utc="2026-11-17T02:05:00Z",
    )
    assert updated.status == OrderStatus.PARTIALLY_FILLED
    assert float(ledger.btc_tactical) == 0.06
    assert float(ledger.btc_reserved) == 0.06
    assert float(ledger.btc_tactical_available) == 0.0
    assert float(ledger.usdt_tactical) == 2797.2

    # Request cancel WITHOUT confirmation -> reservation MUST NOT be released
    ledger.request_cancellation(order.order_id, operator_id="op_1", now_utc="2026-11-17T02:06:00Z")
    assert float(ledger.btc_reserved) == 0.06
    assert float(ledger.btc_tactical_available) == 0.0

    # Confirm cancellation -> remaining 0.06 BTC reservation released
    cancelled = ledger.confirm_terminal_status(
        order.order_id,
        terminal_status=OrderStatus.CANCELLED,
        confirmed_by="op_1",
        reason="Exchange confirmed cancel",
        now_utc="2026-11-17T02:07:00Z",
    )
    assert cancelled.status == OrderStatus.CANCELLED
    assert float(ledger.btc_reserved) == 0.0
    assert float(ledger.btc_tactical_available) == 0.06


def test_balance_reconciliation_discrepancy_blocks_new_orders(tmp_path: Path) -> None:
    ledger, cfg = _setup_ledger(tmp_path)
    ledger.configure_balances(
        btc_core_protected=0.50,
        btc_tactical=0.10,
        usdt_tactical=4000.0,
        operator_id="op_1",
        reason="Init",
        now_utc="2026-11-17T03:00:00Z",
    )

    status = ledger.reconcile_balances(
        reported_btc_total=0.55,  # mismatch vs 0.60
        reported_usdt_total=4000.0,
        source="manual_exchange_check",
        now_utc="2026-11-17T03:05:00Z",
    )
    assert status == ReconciliationStatus.DISCREPANCY

    with pytest.raises(ReconciliationDiscrepancyError):
        ledger.propose_order(
            idempotency_key="blocked-by-reconcile",
            side="BUY",
            limit_price=60000.0,
            quantity_btc=0.01,
            estimated_fee_usdt=0.6,
            loop=LoopType.LOOP_A,
            invalidation_condition="Close < 58000",
            config=cfg,
            now_utc="2026-11-17T03:06:00Z",
        )


def test_loop_a_and_loop_b_independent_cycle_accounting_and_audit_export(tmp_path: Path) -> None:
    ledger, cfg = _setup_ledger(tmp_path)
    ledger.configure_balances(
        btc_core_protected=0.50,
        btc_tactical=0.10,
        usdt_tactical=7000.0,
        operator_id="op_1",
        reason="Init cycle test",
        now_utc="2026-11-17T04:00:00Z",
    )

    # Loop A: USDT -> BTC -> USDT (0.10 BTC bought @ 60k, sold @ 65k, fees 6 + 6.5 = 12.5 USDT)
    cyc_a = ledger.open_cycle(loop=LoopType.LOOP_A, starting_qty=6006.0, original_setup_ref="MOD_A_01", now_utc="2026-11-17T04:01:00Z")
    buy_a = ledger.propose_order(
        idempotency_key="cyc-a-buy",
        side="BUY",
        limit_price=60000.0,
        quantity_btc=0.10,
        estimated_fee_usdt=6.0,
        loop=LoopType.LOOP_A,
        cycle_id=cyc_a.cycle_id,
        invalidation_condition="Stop < 58000",
        config=cfg,
        now_utc="2026-11-17T04:02:00Z",
    )
    ledger.link_order_to_cycle(cyc_a.cycle_id, buy_a.order_id, leg="ENTRY")
    assert ledger.cycles[cyc_a.cycle_id].status == CycleStatus.OPEN

    ledger.approve_order(buy_a.order_id, operator_id="op_1", now_utc="2026-11-17T04:03:00Z")
    ledger.record_fill(
        buy_a.order_id,
        fill_qty_btc=0.10,
        fill_price_usdt=60000.0,
        fee_asset="USDT",
        fee_amount=6.0,
        exchange_fill_ref="FA-1",
        recorded_by="op_1",
        now_utc="2026-11-17T04:04:00Z",
    )
    assert ledger.cycles[cyc_a.cycle_id].status == CycleStatus.PARTIALLY_CONVERTED

    sell_a = ledger.propose_order(
        idempotency_key="cyc-a-sell",
        side="SELL",
        limit_price=65000.0,
        quantity_btc=0.10,
        estimated_fee_usdt=6.5,
        loop=LoopType.LOOP_A,
        cycle_id=cyc_a.cycle_id,
        invalidation_condition="Target hit",
        config=cfg,
        now_utc="2026-11-17T04:05:00Z",
    )
    ledger.link_order_to_cycle(cyc_a.cycle_id, sell_a.order_id, leg="EXIT")
    ledger.approve_order(sell_a.order_id, operator_id="op_1", now_utc="2026-11-17T04:06:00Z")
    ledger.record_fill(
        sell_a.order_id,
        fill_qty_btc=0.10,
        fill_price_usdt=65000.0,
        fee_asset="USDT",
        fee_amount=6.5,
        exchange_fill_ref="FA-2",
        recorded_by="op_1",
        now_utc="2026-11-17T04:07:00Z",
    )
    assert ledger.cycles[cyc_a.cycle_id].status == CycleStatus.COMPLETED
    assert ledger.cycles[cyc_a.cycle_id].realised_net_usdt == 487.5

    # Loop B: BTC -> USDT -> BTC (sell 0.10 BTC @ 70k = 7000 USDT - 7 fee = 6993 USDT;
    # repurchase 0.11 BTC @ 63k = 6930 USDT + 6.93 fee) -> delta_btc = +0.01 BTC
    cyc_b = ledger.open_cycle(loop=LoopType.LOOP_B, starting_qty=0.10, original_setup_ref="MOD_B_01", now_utc="2026-11-17T05:00:00Z")
    sell_b = ledger.propose_order(
        idempotency_key="cyc-b-sell",
        side="SELL",
        limit_price=70000.0,
        quantity_btc=0.10,
        estimated_fee_usdt=7.0,
        loop=LoopType.LOOP_B,
        cycle_id=cyc_b.cycle_id,
        invalidation_condition="Reclaim > 72k",
        config=cfg,
        now_utc="2026-11-17T05:01:00Z",
    )
    ledger.link_order_to_cycle(cyc_b.cycle_id, sell_b.order_id, leg="ENTRY")
    ledger.approve_order(sell_b.order_id, operator_id="op_1", now_utc="2026-11-17T05:02:00Z")
    ledger.record_fill(
        sell_b.order_id,
        fill_qty_btc=0.10,
        fill_price_usdt=70000.0,
        fee_asset="USDT",
        fee_amount=7.0,
        exchange_fill_ref="FB-1",
        recorded_by="op_1",
        now_utc="2026-11-17T05:03:00Z",
    )

    buy_b = ledger.propose_order(
        idempotency_key="cyc-b-buy",
        side="BUY",
        limit_price=63000.0,
        quantity_btc=0.11,
        estimated_fee_usdt=6.93,
        loop=LoopType.LOOP_B,
        cycle_id=cyc_b.cycle_id,
        invalidation_condition="Breakdown < 60k",
        config=cfg,
        now_utc="2026-11-17T05:04:00Z",
    )
    ledger.link_order_to_cycle(cyc_b.cycle_id, buy_b.order_id, leg="EXIT")
    ledger.approve_order(buy_b.order_id, operator_id="op_1", now_utc="2026-11-17T05:05:00Z")
    ledger.record_fill(
        buy_b.order_id,
        fill_qty_btc=0.11,
        fill_price_usdt=63000.0,
        fee_asset="USDT",
        fee_amount=6.93,
        exchange_fill_ref="FB-2",
        recorded_by="op_1",
        now_utc="2026-11-17T05:06:00Z",
    )
    assert ledger.cycles[cyc_b.cycle_id].status == CycleStatus.COMPLETED
    assert ledger.cycles[cyc_b.cycle_id].delta_btc == 0.01

    # Reload from disk & verify persistence
    reloaded = PortfolioLedger(state_path=tmp_path / "ledger.json", audit_logger=ledger.audit_logger)
    assert float(reloaded.realised_usdt_pnl) == 487.5
    assert float(reloaded.realised_delta_btc) == 0.01
    assert float(reloaded.btc_core_protected) == 0.50
    assert float(reloaded.btc_tactical) == 0.11

    # Export audit log to CSV and JSON
    json_out = ledger.audit_logger.export_json(tmp_path / "audit_export.json")
    csv_out = ledger.audit_logger.export_csv(tmp_path / "audit_export.csv")
    assert json_out.exists() and len(json.loads(json_out.read_text(encoding="utf-8"))) > 0
    assert csv_out.exists() and "ORDER_FILL_RECORDED" in csv_out.read_text(encoding="utf-8")


def test_core_mandate_protection_and_explicit_update(tmp_path: Path) -> None:
    ledger, cfg = _setup_ledger(tmp_path)
    ledger.configure_balances(
        btc_core_protected=0.80,
        btc_tactical=0.20,
        usdt_tactical=1000.0,
        operator_id="op_1",
        reason="Init",
        now_utc="2026-11-17T06:00:00Z",
    )
    with pytest.raises(ProtectedCoreViolationError):
        ledger.update_core_mandate(
            new_btc_core_protected=0.50,
            new_btc_tactical=0.50,
            operator_id="op_1",
            reason="Unacknowledged attempt",
            operator_acknowledged=False,
        )
    snap = ledger.update_core_mandate(
        new_btc_core_protected=0.70,
        new_btc_tactical=0.30,
        operator_id="op_1",
        reason="Explicitly authorized sleeve expansion",
        operator_acknowledged=True,
        now_utc="2026-11-17T06:05:00Z",
    )
    assert snap.btc_core_protected == 0.70
    assert snap.btc_tactical == 0.30
    assert snap.btc_total == 1.0


def test_real_btc_metrics_latest_snapshot_parsing(tmp_path: Path) -> None:
    from cortex_core.cli import build_phase1_status_report

    metrics_path = Path(__file__).resolve().parent.parent / "btc_metrics_latest.json"
    if not metrics_path.exists():
        pytest.skip("btc_metrics_latest.json not present")
    raw = json.loads(metrics_path.read_text(encoding="utf-8"))
    cfg = initialize_default_config(tmp_path / "c.json", tmp_path / "h.jsonl")
    snap = build_market_snapshot(raw, config=cfg, now_utc=raw.get("as_of_utc"))
    assert snap.spot_price == raw["spot_price"]
    assert snap.fields["spot_cvd_24h_btc"].validation_status == DataStatus.PROXY
    assert snap.fields["etf_net_flow_usd_m"].validation_status == DataStatus.UNAVAILABLE
    assert snap.overall_integrity_status == DataStatus.PARTIALLY_VERIFIED

    report = build_phase1_status_report(
        metrics_path=metrics_path,
        config_path=tmp_path / "cli_cfg.json",
        history_path=tmp_path / "cli_hist.jsonl",
        ledger_path=tmp_path / "cli_ledger.json",
    )
    assert report["validation_status"] == UNVALIDATED
    assert report["spot_only"] is True
    assert report["autonomous_execution"] is False
    assert report["portfolio_snapshot"]["btc_total"] == NOT_CONFIGURED
    assert report["market_snapshot"]["source_event_ts_myt"].endswith("MYT (UTC+8)")

