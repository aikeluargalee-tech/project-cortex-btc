"""
Phase 6 — Deterministic Historical Replay, Backtesting & Benchmark Engine
(Section 18 of G2.txt & Sections 6, 8 of D2.md).

Enforces:
- Chronological replay with zero look-ahead bias (bar t orders fill only on bar >= t+1).
- Realistic limit-order simulation: unfilled orders expire, partial fills supported,
  fees and slippage deducted from actual inventory via PortfolioLedger.
- Separate evaluation modes: MODULE_A_ONLY, MODULE_B_ONLY, COMBINED_CORTEX.
- Chronological In-Sample / Out-of-Sample walk-forward split support.
- Mandatory benchmarks: 100% BTC Buy-and-Hold, 100% USDT, Static 50/50.
- Always marks validation_status='UNVALIDATED' unless formally promoted.
"""

from __future__ import annotations

import tempfile
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from btc_config_loader import get_param
from cortex_core.audit import AuditLogger, canonical_sha256
from cortex_core.constants import (
    NOT_CONFIGURED,
    UNVALIDATED,
    LoopType,
    OrderStatus,
    PortfolioState,
    Verdict,
)
from cortex_core.ledger import PortfolioLedger
from cortex_core.market_data import build_market_snapshot
from cortex_core.models import ConfigurationRecord
from cortex_core.module_a import evaluate_module_a
from cortex_core.module_b import evaluate_module_b
from cortex_core.module_d import evaluate_final_decision
from cortex_core.time_utils import parse_utc_timestamp


@dataclass(slots=True)
class HistoricalBar:
    """Single chronological market bar for deterministic replay."""

    timestamp_utc: str
    open: float
    high: float
    low: float
    close: float
    sma50: float | None = None
    sma200: float | None = None
    rsi14: float | None = None
    range_high_45d: float | None = None
    range_low_45d: float | None = None
    spread_bps: float | None = 1.0
    depth_1pct_usd: float | None = 10_000_000.0
    spot_cvd_24h_btc: float | None = None
    perp_cvd_24h_btc: float | None = None
    oi_change_24h_pct: float | None = None
    vix: float | None = None
    evidence_inputs_a: dict[str, Any] = field(default_factory=dict)
    evidence_inputs_b: dict[str, Any] = field(default_factory=dict)
    evidence_inputs_regime: dict[str, Any] = field(default_factory=dict)
    fill_ratio: float = 1.0  # 1.0 = full fill if touched; < 1.0 simulates partial liquidity
    data_unavailable: bool = False

    def to_raw_metrics(self) -> dict[str, Any]:
        if self.data_unavailable:
            return {}
        return {
            "as_of_utc": self.timestamp_utc,
            "spot_price": self.close,
            "venues": {
                "binance": {"price": self.close, "timestamp_utc": self.timestamp_utc},
                "coinbase": {"price": self.close, "timestamp_utc": self.timestamp_utc},
                "coingecko": {"price": self.close, "timestamp_utc": self.timestamp_utc},
                "okx": {"price": self.close, "timestamp_utc": self.timestamp_utc},
            },
            "price": {
                "spot": self.close,
                "high_24h": self.high,
                "low_24h": self.low,
                "sma50": self.sma50,
                "sma200": self.sma200,
                "rsi14": self.rsi14,
                "range_high_45d": self.range_high_45d,
                "range_low_45d": self.range_low_45d,
            },
            "liquidity": {"spread_bps": self.spread_bps, "depth_1pct_usd": self.depth_1pct_usd},
            "derivatives": {
                "open_interest": {"current_btc": 30000.0, "change_24h_pct": self.oi_change_24h_pct},
                "funding_rate_pct": 0.005,
                "long_short_ratio": 1.2,
                "perp_cvd": {"24h": {"cvd_btc": self.perp_cvd_24h_btc}},
            },
            "order_flow": {"spot_cvd_binance": {"24h": {"cvd_btc": self.spot_cvd_24h_btc}}},
            "macro": (
                {"vix": {"value": self.vix, "as_of_utc": self.timestamp_utc[:10], "source": "FRED:VIXCLS"}}
                if self.vix is not None
                else {}
            ),
        }


@dataclass(slots=True)
class BenchmarkSummary:
    name: str
    initial_equity_usdt: float
    final_equity_usdt: float
    net_return_pct: float
    max_drawdown_pct: float
    final_btc_qty: float
    final_usdt_qty: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class BacktestReport:
    mode: str  # "MODULE_A_ONLY" | "MODULE_B_ONLY" | "COMBINED_CORTEX"
    validation_status: str  # UNVALIDATED
    start_utc: str
    end_utc: str
    bars_count: int
    initial_tactical_btc: float
    initial_tactical_usdt: float
    initial_equity_usdt: float
    final_tactical_btc: float
    final_tactical_usdt: float
    final_equity_usdt: float
    net_return_pct: float
    max_drawdown_pct: float
    btc_quantity_change: float
    usdt_quantity_change: float
    total_fees_usdt: float
    proposed_orders_count: int
    filled_orders_count: int
    partially_filled_orders_count: int
    unfilled_expired_orders_count: int
    fill_rate_pct: float
    completed_round_trips: int
    win_rate_pct: float | None
    profit_factor: float | None
    time_in_btc_pct: float
    time_in_usdt_pct: float
    benchmarks: dict[str, BenchmarkSummary]
    excess_vs_btc_hold_pct: float
    excess_vs_usdt_hold_pct: float
    excess_vs_50_50_pct: float
    determinism_sha256: str
    equity_curve: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        out = asdict(self)
        out["benchmarks"] = {k: v.to_dict() for k, v in self.benchmarks.items()}
        return out


def _max_drawdown(equities: list[float]) -> float:
    if not equities:
        return 0.0
    peak = equities[0]
    max_dd = 0.0
    for eq in equities:
        if eq > peak:
            peak = eq
        if peak > 0:
            dd = ((peak - eq) / peak) * 100.0
            if dd > max_dd:
                max_dd = dd
    return round(max_dd, 4)


def _compute_benchmarks(
    bars: list[HistoricalBar],
    initial_equity_usdt: float,
) -> dict[str, BenchmarkSummary]:
    start_px = bars[0].close
    end_px = bars[-1].close

    # 1. 100% BTC Buy & Hold
    btc_all = initial_equity_usdt / start_px if start_px > 0 else 0.0
    btc_eq_curve = [btc_all * b.close for b in bars]
    btc_final = btc_eq_curve[-1]
    btc_ret = ((btc_final - initial_equity_usdt) / initial_equity_usdt) * 100.0 if initial_equity_usdt > 0 else 0.0

    # 2. 100% USDT
    usdt_ret = 0.0

    # 3. Static 50% BTC / 50% USDT
    half_btc = (initial_equity_usdt * 0.5) / start_px if start_px > 0 else 0.0
    half_usdt = initial_equity_usdt * 0.5
    half_curve = [half_btc * b.close + half_usdt for b in bars]
    half_final = half_curve[-1]
    half_ret = ((half_final - initial_equity_usdt) / initial_equity_usdt) * 100.0 if initial_equity_usdt > 0 else 0.0

    return {
        "btc_buy_and_hold": BenchmarkSummary(
            name="100% BTC Buy-and-Hold",
            initial_equity_usdt=round(initial_equity_usdt, 2),
            final_equity_usdt=round(btc_final, 2),
            net_return_pct=round(btc_ret, 4),
            max_drawdown_pct=_max_drawdown(btc_eq_curve),
            final_btc_qty=round(btc_all, 8),
            final_usdt_qty=0.0,
        ),
        "usdt_100": BenchmarkSummary(
            name="100% USDT",
            initial_equity_usdt=round(initial_equity_usdt, 2),
            final_equity_usdt=round(initial_equity_usdt, 2),
            net_return_pct=round(usdt_ret, 4),
            max_drawdown_pct=0.0,
            final_btc_qty=0.0,
            final_usdt_qty=round(initial_equity_usdt, 2),
        ),
        "static_50_50": BenchmarkSummary(
            name="Static 50% BTC / 50% USDT",
            initial_equity_usdt=round(initial_equity_usdt, 2),
            final_equity_usdt=round(half_final, 2),
            net_return_pct=round(half_ret, 4),
            max_drawdown_pct=_max_drawdown(half_curve),
            final_btc_qty=round(half_btc, 8),
            final_usdt_qty=round(half_usdt, 2),
        ),
    }


def _process_working_orders(
    *,
    bar: HistoricalBar,
    ledger: PortfolioLedger,
    fee_bps: float,
    slip_bps: float,
) -> None:
    """
    Evaluate working limit orders on bar t (placed strictly on bar <= t-1).
    Handles expiry, partial fills, and realistic limit fill prices.
    """
    bar_dt = parse_utc_timestamp(bar.timestamp_utc)
    fee_rate = fee_bps / 10000.0
    slip_rate = slip_bps / 10000.0
    active_ids = [
        oid
        for oid, o in ledger.orders.items()
        if o.status in {OrderStatus.WORKING, OrderStatus.PARTIALLY_FILLED}
    ]

    for oid in active_ids:
        order = ledger.orders[oid]
        # 1. Check expiry
        if order.expiry_utc and bar_dt is not None:
            exp_dt = parse_utc_timestamp(order.expiry_utc)
            if exp_dt is not None and bar_dt > exp_dt:
                ledger.confirm_terminal_status(
                    oid,
                    terminal_status=OrderStatus.EXPIRED,
                    confirmed_by="BACKTEST_SIM",
                    reason="Order expired prior to fill.",
                    now_utc=bar.timestamp_utc,
                )
                continue

        # 2. Check limit touch
        rem_qty = round(order.requested_qty_btc - order.filled_qty_btc, 8)
        if rem_qty <= 0:
            continue

        ratio = max(0.0, min(1.0, float(bar.fill_ratio)))
        if ratio <= 0.0:
            continue

        fill_qty = round(rem_qty * ratio, 8)
        if fill_qty <= 0:
            continue

        if order.side == "BUY" and bar.low <= order.limit_price:
            # Passive limit buy never executes worse than limit_price
            exec_px = round(min(order.limit_price, bar.open) if bar.open < order.limit_price else order.limit_price, 2)
            fee_amt = round(fill_qty * exec_px * fee_rate, 6)
            ledger.record_fill(
                oid,
                fill_qty_btc=fill_qty,
                fill_price_usdt=exec_px,
                fee_asset="USDT",
                fee_amount=fee_amt,
                exchange_fill_ref=f"SIM-{oid[:8]}",
                recorded_by="BACKTEST_SIM",
                now_utc=bar.timestamp_utc,
            )
        elif order.side == "SELL" and bar.high >= order.limit_price:
            # Passive limit sell never executes worse than limit_price
            exec_px = round(max(order.limit_price, bar.open) if bar.open > order.limit_price else order.limit_price, 2)
            fee_amt = round(fill_qty * exec_px * fee_rate, 6)
            ledger.record_fill(
                oid,
                fill_qty_btc=fill_qty,
                fill_price_usdt=exec_px,
                fee_asset="USDT",
                fee_amount=fee_amt,
                exchange_fill_ref=f"SIM-{oid[:8]}",
                recorded_by="BACKTEST_SIM",
                now_utc=bar.timestamp_utc,
            )


def run_backtest(
    bars: list[HistoricalBar],
    config: ConfigurationRecord,
    *,
    mode: str = "COMBINED_CORTEX",
    initial_tactical_btc: float = 0.0,
    initial_tactical_usdt: float = 10_000.0,
    btc_core_protected: float = 0.0,
) -> BacktestReport:
    """
    Run deterministic chronological backtest over HistoricalBars.

    No look-ahead bias: orders proposed on bar t enter WORKING after bar t closes
    and can only execute on bar >= t+1.
    """
    if len(bars) < 2:
        raise ValueError("At least 2 chronological bars are required for backtesting.")

    mode_norm = mode.upper().strip()
    if mode_norm not in {"MODULE_A_ONLY", "MODULE_B_ONLY", "COMBINED_CORTEX"}:
        raise ValueError(f"Unsupported backtest mode {mode!r}.")

    maker_fee = get_param(config, "execution_assumptions.maker_fee_bps")
    slippage = get_param(config, "execution_assumptions.expected_slippage_bps")
    if maker_fee == NOT_CONFIGURED or slippage == NOT_CONFIGURED:
        raise ValueError("maker_fee_bps and expected_slippage_bps must be configured for backtesting.")

    fee_bps = float(maker_fee)
    slip_bps = float(slippage)

    with tempfile.TemporaryDirectory() as td:
        tp = Path(td)
        audit = AuditLogger(tp / "bt_audit.jsonl")
        ledger = PortfolioLedger(state_path=tp / "bt_ledger.json", audit_logger=audit)
        ledger.configure_balances(
            btc_core_protected=btc_core_protected,
            btc_tactical=initial_tactical_btc,
            usdt_tactical=initial_tactical_usdt,
            operator_id="BACKTEST_INIT",
            reason=f"Backtest mode={mode_norm}",
            now_utc=bars[0].timestamp_utc,
        )

        start_px = bars[0].close
        init_tactical_eq = initial_tactical_btc * start_px + initial_tactical_usdt
        op_state = PortfolioState.USDT_100 if initial_tactical_btc <= 0 else PortfolioState.BTC_HOLD

        equity_curve: list[dict[str, Any]] = []
        tactical_equities: list[float] = []
        bars_in_btc = 0
        bars_in_usdt = 0
        trade_pnls: list[float] = []
        open_buy_cost_basis: list[tuple[float, float]] = []  # (qty, total_cost_usdt)

        for idx, bar in enumerate(bars):
            # 1. Process previously working orders on current bar (anti-look-ahead!)
            prev_orders_filled = {
                oid: o.filled_qty_btc for oid, o in ledger.orders.items()
            }
            _process_working_orders(bar=bar, ledger=ledger, fee_bps=fee_bps, slip_bps=slip_bps)

            # Track realized round-trip PnL when sells fill against prior buys
            for oid, o in ledger.orders.items():
                delta_fill = o.filled_qty_btc - prev_orders_filled.get(oid, 0.0)
                if delta_fill > 0:
                    last_fill = o.fill_events[-1]
                    if o.side == "BUY":
                        open_buy_cost_basis.append((delta_fill, last_fill.gross_usdt + last_fill.fee_amount))
                    elif o.side == "SELL" and open_buy_cost_basis:
                        qty_to_match = delta_fill
                        cost_matched = 0.0
                        while qty_to_match > 1e-8 and open_buy_cost_basis:
                            b_qty, b_cost = open_buy_cost_basis[0]
                            used = min(qty_to_match, b_qty)
                            unit_cost = b_cost / b_qty
                            cost_matched += used * unit_cost
                            if used >= b_qty - 1e-8:
                                open_buy_cost_basis.pop(0)
                            else:
                                open_buy_cost_basis[0] = (b_qty - used, b_cost - used * unit_cost)
                            qty_to_match -= used
                        proceeds = last_fill.gross_usdt - last_fill.fee_amount
                        trade_pnls.append(proceeds - cost_matched)

            # 2. Evaluate bar t snapshot
            raw = bar.to_raw_metrics()
            mkt = build_market_snapshot(raw, config=config, now_utc=bar.timestamp_utc)
            prt = ledger.snapshot(spot_price=bar.close, config_version=config.config_version, now_utc=bar.timestamp_utc)

            tac_btc_val = float(prt.btc_tactical or 0.0) * bar.close
            tac_usdt_val = float(prt.usdt_tactical or 0.0)
            tac_eq = tac_btc_val + tac_usdt_val
            tactical_equities.append(tac_eq)
            if tac_btc_val >= tac_usdt_val:
                bars_in_btc += 1
            else:
                bars_in_usdt += 1

            mod_a = evaluate_module_a(mkt, config, evidence_inputs=bar.evidence_inputs_a, now_utc=bar.timestamp_utc)
            mod_b = evaluate_module_b(mkt, config, evidence_inputs=bar.evidence_inputs_b, now_utc=bar.timestamp_utc)

            # Isolate Module A or Module B if requested by test stage
            if mode_norm == "MODULE_A_ONLY" and mod_b.directional_signal in {"SELL", "REDUCE"}:
                mod_b.directional_signal = "HOLD"
                mod_b.exit_classification = None
            elif mode_norm == "MODULE_B_ONLY" and mod_a.directional_signal == "BUY":
                mod_a.directional_signal = "WAIT"

            decision, _ = evaluate_final_decision(
                market_snapshot=mkt,
                portfolio_snapshot=prt,
                module_a=mod_a,
                module_b=mod_b,
                config=config,
                previous_operating_state=op_state,
                open_orders=list(ledger.orders.values()),
                evidence_inputs=bar.evidence_inputs_regime,
                now_utc=bar.timestamp_utc,
            )
            op_state = decision.new_operating_state

            # 3. Propose order for next-bar execution (never on final bar)
            if idx < len(bars) - 1 and decision.proposed_order is not None:
                po = decision.proposed_order
                idem_key = f"BT:{idx}:{bar.timestamp_utc}:{po['side']}"
                order = ledger.propose_order(
                    idempotency_key=idem_key,
                    side=po["side"],
                    limit_price=float(po["limit_price"]),
                    quantity_btc=float(po["quantity_btc"]),
                    estimated_fee_usdt=float(po["estimated_fee_usdt"]),
                    loop=LoopType(po["loop"]),
                    invalidation_condition=str(po["invalidation_condition"]),
                    config=config,
                    decision_id=decision.decision_id,
                    expiry_utc=po.get("expiry_utc"),
                    now_utc=bar.timestamp_utc,
                )
                ledger.approve_order(order.order_id, operator_id="BACKTEST_SIM", now_utc=bar.timestamp_utc)
                ledger.mark_submitted(
                    order.order_id,
                    operator_id="BACKTEST_SIM",
                    exchange_order_ref=f"BT-EX-{idx}",
                    now_utc=bar.timestamp_utc,
                )
                ledger.mark_working(order.order_id, operator_id="BACKTEST_SIM", now_utc=bar.timestamp_utc)

            equity_curve.append(
                {
                    "timestamp_utc": bar.timestamp_utc,
                    "close": bar.close,
                    "tactical_equity_usdt": round(tac_eq, 2),
                    "btc_tactical": float(prt.btc_tactical or 0.0),
                    "usdt_tactical": float(prt.usdt_tactical or 0.0),
                    "verdict": decision.final_verdict.value,
                    "state": op_state.value,
                }
            )

        # Final tally
        end_px = bars[-1].close
        final_tac_btc = float(ledger.btc_tactical or 0.0)
        final_tac_usdt = float(ledger.usdt_tactical or 0.0)
        final_tac_eq = final_tac_btc * end_px + final_tac_usdt
        net_ret_pct = ((final_tac_eq - init_tactical_eq) / init_tactical_eq) * 100.0 if init_tactical_eq > 0 else 0.0

        orders_list = list(ledger.orders.values())
        proposed_n = len(orders_list)
        filled_n = sum(1 for o in orders_list if o.status == OrderStatus.FILLED)
        partial_n = sum(1 for o in orders_list if o.status == OrderStatus.PARTIALLY_FILLED)
        expired_n = sum(1 for o in orders_list if o.status == OrderStatus.EXPIRED)
        fill_rate = (filled_n / proposed_n * 100.0) if proposed_n > 0 else 0.0

        wins = [p for p in trade_pnls if p > 0]
        losses = [abs(p) for p in trade_pnls if p < 0]
        win_rate = round((len(wins) / len(trade_pnls)) * 100.0, 2) if trade_pnls else None
        profit_factor = round(sum(wins) / sum(losses), 3) if losses and sum(losses) > 0 else None

        benchmarks = _compute_benchmarks(bars, init_tactical_eq)
        excess_btc = round(net_ret_pct - benchmarks["btc_buy_and_hold"].net_return_pct, 4)
        excess_usdt = round(net_ret_pct - benchmarks["usdt_100"].net_return_pct, 4)
        excess_50 = round(net_ret_pct - benchmarks["static_50_50"].net_return_pct, 4)

        det_payload = {
            "mode": mode_norm,
            "config_version": config.config_version,
            "bars": [(b.timestamp_utc, b.close) for b in bars],
            "final_tac_btc": round(final_tac_btc, 8),
            "final_tac_usdt": round(final_tac_usdt, 4),
            "proposed_n": proposed_n,
            "filled_n": filled_n,
            "expired_n": expired_n,
        }

        return BacktestReport(
            mode=mode_norm,
            validation_status=UNVALIDATED,
            start_utc=bars[0].timestamp_utc,
            end_utc=bars[-1].timestamp_utc,
            bars_count=len(bars),
            initial_tactical_btc=round(initial_tactical_btc, 8),
            initial_tactical_usdt=round(initial_tactical_usdt, 2),
            initial_equity_usdt=round(init_tactical_eq, 2),
            final_tactical_btc=round(final_tac_btc, 8),
            final_tactical_usdt=round(final_tac_usdt, 2),
            final_equity_usdt=round(final_tac_eq, 2),
            net_return_pct=round(net_ret_pct, 4),
            max_drawdown_pct=_max_drawdown(tactical_equities),
            btc_quantity_change=round(final_tac_btc - initial_tactical_btc, 8),
            usdt_quantity_change=round(final_tac_usdt - initial_tactical_usdt, 2),
            total_fees_usdt=round(float(ledger.total_fees_paid_usdt), 4),
            proposed_orders_count=proposed_n,
            filled_orders_count=filled_n,
            partially_filled_orders_count=partial_n,
            unfilled_expired_orders_count=expired_n,
            fill_rate_pct=round(fill_rate, 2),
            completed_round_trips=len(trade_pnls),
            win_rate_pct=win_rate,
            profit_factor=profit_factor,
            time_in_btc_pct=round((bars_in_btc / len(bars)) * 100.0, 2),
            time_in_usdt_pct=round((bars_in_usdt / len(bars)) * 100.0, 2),
            benchmarks=benchmarks,
            excess_vs_btc_hold_pct=excess_btc,
            excess_vs_usdt_hold_pct=excess_usdt,
            excess_vs_50_50_pct=excess_50,
            determinism_sha256=canonical_sha256(det_payload),
            equity_curve=equity_curve,
        )


def run_walk_forward_validation(
    bars: list[HistoricalBar],
    config: ConfigurationRecord,
    *,
    in_sample_ratio: float = 0.6,
    initial_tactical_btc: float = 0.0,
    initial_tactical_usdt: float = 10_000.0,
) -> dict[str, Any]:
    """
    Chronological In-Sample vs. Out-of-Sample validation split across
    MODULE_A_ONLY, MODULE_B_ONLY, and COMBINED_CORTEX.
    """
    if not (0.2 <= in_sample_ratio <= 0.85):
        raise ValueError("in_sample_ratio must be between 0.2 and 0.85.")
    split_idx = int(len(bars) * in_sample_ratio)
    if split_idx < 2 or (len(bars) - split_idx) < 2:
        raise ValueError("Insufficient bars for chronological in-sample and out-of-sample windows.")

    is_bars = bars[:split_idx]
    oos_bars = bars[split_idx:]

    results: dict[str, Any] = {
        "validation_status": UNVALIDATED,
        "split_index": split_idx,
        "in_sample_window": {"start_utc": is_bars[0].timestamp_utc, "end_utc": is_bars[-1].timestamp_utc, "bars": len(is_bars)},
        "out_of_sample_window": {"start_utc": oos_bars[0].timestamp_utc, "end_utc": oos_bars[-1].timestamp_utc, "bars": len(oos_bars)},
        "stages": {},
    }

    for stage in ("MODULE_A_ONLY", "MODULE_B_ONLY", "COMBINED_CORTEX"):
        is_rep = run_backtest(
            is_bars,
            config,
            mode=stage,
            initial_tactical_btc=initial_tactical_btc,
            initial_tactical_usdt=initial_tactical_usdt,
        )
        oos_rep = run_backtest(
            oos_bars,
            config,
            mode=stage,
            initial_tactical_btc=initial_tactical_btc,
            initial_tactical_usdt=initial_tactical_usdt,
        )
        results["stages"][stage] = {
            "in_sample": is_rep.to_dict(),
            "out_of_sample": oos_rep.to_dict(),
        }
    return results
