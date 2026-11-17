"""
Dual-Inventory BTC/USDT Ledger, Reservation Engine & DIBSE Cycle Accounting
(Sections 2, 6, 10, 11, 12, and 20 of CORTEX-ANTIGRAVITY-HANDOVER-001).

Spot-only BTC/USDT accounting:
- No borrowing, leverage, margin, futures, or short selling.
- Protected core BTC (Sleeve B) cannot be appropriated by tactical orders.
- Unconfigured balances remain None / NOT CONFIGURED (never silently 0 or $10k).
- Exact Decimal arithmetic prevents floating-point drift on reservations and fills.
- Unconfirmed cancellations never release reservations.
- Same snapshot / idempotency_key cannot create duplicate orders or reservations.
"""

from __future__ import annotations

import json
import uuid
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import Any

from btc_config_loader import get_param
from cortex_core.audit import AuditLogger
from cortex_core.constants import (
    NOT_CONFIGURED,
    CycleStatus,
    LoopType,
    OrderStatus,
    ReconciliationStatus,
)
from cortex_core.models import (
    ConfigurationRecord,
    ConversionCycle,
    FillEvent,
    OrderRecord,
    PortfolioSnapshot,
)
from cortex_core.time_utils import ensure_utc_iso, utc_now

BTC_QUANT = Decimal("0.00000001")
USDT_QUANT = Decimal("0.000001")


class LedgerError(ValueError):
    """Base error for accounting, reservation, or spot-only invariant violations."""


class InsufficientInventoryError(LedgerError):
    """Raised when available tactical BTC or USDT is insufficient."""


class ProtectedCoreViolationError(LedgerError):
    """Raised when an operation attempts to touch protected core BTC (Sleeve B)."""


class ReconciliationDiscrepancyError(LedgerError):
    """Raised when ledger and reported balances disagree."""


class OrderLifecycleError(LedgerError):
    """Raised on invalid order status transition or fill."""


def _d(val: float | int | str | Decimal) -> Decimal:
    return Decimal(str(val))


def _q_btc(val: Decimal) -> Decimal:
    return val.quantize(BTC_QUANT, rounding=ROUND_HALF_UP)


def _q_usdt(val: Decimal) -> Decimal:
    return val.quantize(USDT_QUANT, rounding=ROUND_HALF_UP)


def _f(val: Decimal | None) -> float | None:
    return float(val) if val is not None else None


class PortfolioLedger:
    """
    Persistent dual-inventory BTC/USDT ledger with reservation isolation,
    core/tactical separation, manual order lifecycle, and Loop A/B cycle tracking.
    """

    def __init__(
        self,
        state_path: Path = Path("data/portfolio_ledger.json"),
        audit_logger: AuditLogger | None = None,
    ) -> None:
        self.state_path = Path(state_path)
        self.audit_logger = audit_logger or AuditLogger(self.state_path.parent / "cortex_audit.jsonl")

        self.configured: bool = False
        self.btc_core_protected: Decimal | None = None
        self.btc_tactical: Decimal | None = None
        self.btc_reserved: Decimal = Decimal("0")
        self.usdt_core_protected: Decimal | None = None
        self.usdt_tactical: Decimal | None = None
        self.usdt_reserved: Decimal = Decimal("0")

        self.realised_usdt_pnl: Decimal = Decimal("0")
        self.realised_delta_btc: Decimal = Decimal("0")
        self.total_fees_paid_usdt: Decimal = Decimal("0")
        self.total_fees_paid_btc: Decimal = Decimal("0")

        self.reconciliation_status: ReconciliationStatus = ReconciliationStatus.NOT_CONFIGURED
        self.reconciliation_notes: str = "Portfolio balances have not been configured."
        self.last_reconciled_utc: str | None = None

        self.orders: dict[str, OrderRecord] = {}
        self.idempotency_index: dict[str, str] = {}
        self.cycles: dict[str, ConversionCycle] = {}

        if self.state_path.exists():
            self.load()

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def save(self) -> None:
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "configured": self.configured,
            "btc_core_protected": str(self.btc_core_protected) if self.btc_core_protected is not None else None,
            "btc_tactical": str(self.btc_tactical) if self.btc_tactical is not None else None,
            "btc_reserved": str(self.btc_reserved),
            "usdt_core_protected": str(self.usdt_core_protected) if self.usdt_core_protected is not None else None,
            "usdt_tactical": str(self.usdt_tactical) if self.usdt_tactical is not None else None,
            "usdt_reserved": str(self.usdt_reserved),
            "realised_usdt_pnl": str(self.realised_usdt_pnl),
            "realised_delta_btc": str(self.realised_delta_btc),
            "total_fees_paid_usdt": str(self.total_fees_paid_usdt),
            "total_fees_paid_btc": str(self.total_fees_paid_btc),
            "reconciliation_status": self.reconciliation_status.value,
            "reconciliation_notes": self.reconciliation_notes,
            "last_reconciled_utc": self.last_reconciled_utc,
            "orders": {oid: o.to_dict() for oid, o in self.orders.items()},
            "idempotency_index": dict(self.idempotency_index),
            "cycles": {cid: c.to_dict() for cid, c in self.cycles.items()},
        }
        tmp = self.state_path.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        tmp.replace(self.state_path)

    def load(self) -> None:
        data = json.loads(self.state_path.read_text(encoding="utf-8"))
        self.configured = bool(data.get("configured", False))
        self.btc_core_protected = _d(data["btc_core_protected"]) if data.get("btc_core_protected") is not None else None
        self.btc_tactical = _d(data["btc_tactical"]) if data.get("btc_tactical") is not None else None
        self.btc_reserved = _d(data.get("btc_reserved", "0"))
        self.usdt_core_protected = _d(data["usdt_core_protected"]) if data.get("usdt_core_protected") is not None else None
        self.usdt_tactical = _d(data["usdt_tactical"]) if data.get("usdt_tactical") is not None else None
        self.usdt_reserved = _d(data.get("usdt_reserved", "0"))
        self.realised_usdt_pnl = _d(data.get("realised_usdt_pnl", "0"))
        self.realised_delta_btc = _d(data.get("realised_delta_btc", "0"))
        self.total_fees_paid_usdt = _d(data.get("total_fees_paid_usdt", "0"))
        self.total_fees_paid_btc = _d(data.get("total_fees_paid_btc", "0"))
        self.reconciliation_status = ReconciliationStatus(
            data.get("reconciliation_status", ReconciliationStatus.NOT_CONFIGURED.value)
        )
        self.reconciliation_notes = data.get("reconciliation_notes", "")
        self.last_reconciled_utc = data.get("last_reconciled_utc")
        self.orders = {oid: OrderRecord.from_dict(od) for oid, od in data.get("orders", {}).items()}
        self.idempotency_index = dict(data.get("idempotency_index", {}))
        self.cycles = {cid: ConversionCycle.from_dict(cd) for cid, cd in data.get("cycles", {}).items()}

    # ------------------------------------------------------------------
    # Balance Configuration & Core Protection
    # ------------------------------------------------------------------

    def configure_balances(
        self,
        *,
        btc_core_protected: float,
        btc_tactical: float,
        usdt_tactical: float,
        usdt_core_protected: float = 0.0,
        operator_id: str,
        reason: str,
        now_utc: str | None = None,
    ) -> PortfolioSnapshot:
        """
        Explicitly set operator-verified BTC and USDT holdings.
        Never silently assumes balances; requires non-empty operator & reason.
        """
        if not operator_id.strip() or not reason.strip():
            raise LedgerError("operator_id and reason are required to configure balances.")
        if self.btc_reserved > 0 or self.usdt_reserved > 0:
            raise LedgerError("Cannot overwrite balances while active reservations exist.")

        b_core = _q_btc(_d(btc_core_protected))
        b_tac = _q_btc(_d(btc_tactical))
        u_tac = _q_usdt(_d(usdt_tactical))
        u_core = _q_usdt(_d(usdt_core_protected))
        if b_core < 0 or b_tac < 0 or u_tac < 0 or u_core < 0:
            raise LedgerError("Negative balances are prohibited in a spot-only portfolio.")

        ts_iso = ensure_utc_iso(now_utc or utc_now(), field_name="now_utc")
        self.configured = True
        self.btc_core_protected = b_core
        self.btc_tactical = b_tac
        self.usdt_tactical = u_tac
        self.usdt_core_protected = u_core
        self.btc_reserved = Decimal("0")
        self.usdt_reserved = Decimal("0")
        self.reconciliation_status = ReconciliationStatus.RECONCILED
        self.reconciliation_notes = f"Balances configured by {operator_id.strip()}."
        self.last_reconciled_utc = ts_iso

        self.save()
        self.audit_logger.record(
            "PORTFOLIO_BALANCES_CONFIGURED",
            actor=operator_id.strip(),
            summary=f"Configured BTC/USDT balances: {reason.strip()}",
            details={
                "btc_core_protected": float(b_core),
                "btc_tactical": float(b_tac),
                "usdt_tactical": float(u_tac),
                "usdt_core_protected": float(u_core),
            },
            timestamp_utc=ts_iso,
        )
        return self.snapshot()

    def update_core_mandate(
        self,
        *,
        new_btc_core_protected: float,
        new_btc_tactical: float,
        operator_id: str,
        reason: str,
        operator_acknowledged: bool = True,
        now_utc: str | None = None,
    ) -> PortfolioSnapshot:
        """
        Explicitly reclassify core vs tactical BTC (e.g., if operator changes mandate).
        Preserves total BTC and forbids touching reserved tactical BTC.
        """
        if not self.configured or self.btc_core_protected is None or self.btc_tactical is None:
            raise LedgerError("Portfolio balances are NOT CONFIGURED.")
        if not operator_acknowledged or not operator_id.strip() or not reason.strip():
            raise ProtectedCoreViolationError(
                "Core BTC mandate change requires explicit operator_id, reason, and acknowledgement."
            )
        new_core = _q_btc(_d(new_btc_core_protected))
        new_tac = _q_btc(_d(new_btc_tactical))
        if new_core < 0 or new_tac < 0:
            raise LedgerError("Core and tactical BTC cannot be negative.")
        if new_core + new_tac != self.btc_core_protected + self.btc_tactical:
            raise ProtectedCoreViolationError(
                "Mandate reclassification must conserve total BTC unless recorded as balance adjustment."
            )
        if new_tac < self.btc_reserved:
            raise ProtectedCoreViolationError(
                "Cannot reduce tactical BTC below currently reserved BTC."
            )

        ts_iso = ensure_utc_iso(now_utc or utc_now(), field_name="now_utc")
        prev = {"btc_core_protected": float(self.btc_core_protected), "btc_tactical": float(self.btc_tactical)}
        self.btc_core_protected = new_core
        self.btc_tactical = new_tac
        self.save()
        self.audit_logger.record(
            "CORE_MANDATE_UPDATED",
            actor=operator_id.strip(),
            summary=f"Core BTC mandate updated: {reason.strip()}",
            details={
                "previous": prev,
                "new": {"btc_core_protected": float(new_core), "btc_tactical": float(new_tac)},
            },
            timestamp_utc=ts_iso,
        )
        return self.snapshot()

    # ------------------------------------------------------------------
    # Derived Balance Helpers
    # ------------------------------------------------------------------

    @property
    def btc_total(self) -> Decimal | None:
        if not self.configured or self.btc_core_protected is None or self.btc_tactical is None:
            return None
        return _q_btc(self.btc_core_protected + self.btc_tactical)

    @property
    def usdt_total(self) -> Decimal | None:
        if not self.configured or self.usdt_core_protected is None or self.usdt_tactical is None:
            return None
        return _q_usdt(self.usdt_core_protected + self.usdt_tactical)

    @property
    def btc_tactical_available(self) -> Decimal | None:
        if not self.configured or self.btc_tactical is None:
            return None
        return _q_btc(self.btc_tactical - self.btc_reserved)

    @property
    def usdt_tactical_available(self) -> Decimal | None:
        if not self.configured or self.usdt_tactical is None:
            return None
        return _q_usdt(self.usdt_tactical - self.usdt_reserved)

    def _active_commitments(self) -> tuple[Decimal, Decimal, Decimal, Decimal]:
        """Compute committed/proceeds quantities across open cycles & active orders."""
        btc_loop_a = Decimal("0")
        btc_loop_b = Decimal("0")
        usdt_loop_a = Decimal("0")
        usdt_loop_b = Decimal("0")
        for order in self.orders.values():
            rem_qty = _d(order.requested_qty_btc) - _d(order.filled_qty_btc)
            if order.status in {
                OrderStatus.PROPOSED,
                OrderStatus.APPROVED,
                OrderStatus.SUBMITTED,
                OrderStatus.WORKING,
                OrderStatus.PARTIALLY_FILLED,
            }:
                if order.side == "BUY" and order.loop == LoopType.LOOP_A:
                    usdt_loop_a += _d(order.remaining_reserved_amount)
                elif order.side == "SELL" and order.loop == LoopType.LOOP_B:
                    btc_loop_b += _d(order.remaining_reserved_amount)
                elif order.side == "SELL" and order.loop == LoopType.LOOP_A:
                    btc_loop_a += _d(order.remaining_reserved_amount)
                elif order.side == "BUY" and order.loop == LoopType.LOOP_B:
                    usdt_loop_b += _d(order.remaining_reserved_amount)
            _ = rem_qty
        return _q_btc(btc_loop_a), _q_btc(btc_loop_b), _q_usdt(usdt_loop_a), _q_usdt(usdt_loop_b)

    def snapshot(
        self,
        *,
        spot_price: float | None = None,
        config_version: int = 1,
        now_utc: str | None = None,
    ) -> PortfolioSnapshot:
        ts_iso = ensure_utc_iso(now_utc or utc_now(), field_name="now_utc")
        snap_id = f"PRT-{uuid.uuid4().hex[:12].upper()}"

        if not self.configured:
            return PortfolioSnapshot(
                portfolio_snapshot_id=snap_id,
                timestamp_utc=ts_iso,
                config_version=config_version,
                configured=False,
                btc_total=None,
                btc_available=None,
                btc_reserved=None,
                btc_core_protected=None,
                btc_tactical=None,
                btc_tactical_available=None,
                btc_loop_a_committed=None,
                btc_loop_b_committed=None,
                usdt_total=None,
                usdt_available=None,
                usdt_reserved=None,
                usdt_core_protected=None,
                usdt_tactical=None,
                usdt_tactical_available=None,
                usdt_loop_a_committed=None,
                usdt_loop_b_proceeds=None,
                valuation_spot_price=spot_price,
                total_portfolio_value_usdt=None,
                active_sleeve_value_usdt=None,
                protected_core_btc_value_usdt=None,
                btc_exposure_pct=None,
                usdt_exposure_pct=None,
                reconciliation_status=self.reconciliation_status,
                reconciliation_notes=self.reconciliation_notes,
            )

        assert self.btc_total is not None and self.usdt_total is not None
        assert self.btc_core_protected is not None and self.btc_tactical is not None
        assert self.usdt_core_protected is not None and self.usdt_tactical is not None

        btc_avail_total = _q_btc(self.btc_total - self.btc_reserved)
        usdt_avail_total = _q_usdt(self.usdt_total - self.usdt_reserved)
        btc_la, btc_lb, usdt_la, usdt_lb = self._active_commitments()

        total_val: float | None = None
        sleeve_val: float | None = None
        core_btc_val: float | None = None
        btc_exp: float | None = None
        usdt_exp: float | None = None

        if spot_price is not None and spot_price > 0:
            px = _d(spot_price)
            btc_val = self.btc_total * px
            total_dec = btc_val + self.usdt_total
            sleeve_dec = self.btc_tactical * px + self.usdt_tactical
            core_dec = self.btc_core_protected * px
            total_val = round(float(total_dec), 2)
            sleeve_val = round(float(sleeve_dec), 2)
            core_btc_val = round(float(core_dec), 2)
            if total_dec > 0:
                btc_exp = round(float((btc_val / total_dec) * Decimal("100")), 4)
                usdt_exp = round(float((self.usdt_total / total_dec) * Decimal("100")), 4)

        return PortfolioSnapshot(
            portfolio_snapshot_id=snap_id,
            timestamp_utc=ts_iso,
            config_version=config_version,
            configured=True,
            btc_total=_f(self.btc_total),
            btc_available=_f(btc_avail_total),
            btc_reserved=_f(self.btc_reserved),
            btc_core_protected=_f(self.btc_core_protected),
            btc_tactical=_f(self.btc_tactical),
            btc_tactical_available=_f(self.btc_tactical_available),
            btc_loop_a_committed=_f(btc_la),
            btc_loop_b_committed=_f(btc_lb),
            usdt_total=_f(self.usdt_total),
            usdt_available=_f(usdt_avail_total),
            usdt_reserved=_f(self.usdt_reserved),
            usdt_core_protected=_f(self.usdt_core_protected),
            usdt_tactical=_f(self.usdt_tactical),
            usdt_tactical_available=_f(self.usdt_tactical_available),
            usdt_loop_a_committed=_f(usdt_la),
            usdt_loop_b_proceeds=_f(usdt_lb),
            valuation_spot_price=spot_price,
            total_portfolio_value_usdt=total_val,
            active_sleeve_value_usdt=sleeve_val,
            protected_core_btc_value_usdt=core_btc_val,
            btc_exposure_pct=btc_exp,
            usdt_exposure_pct=usdt_exp,
            reconciliation_status=self.reconciliation_status,
            reconciliation_notes=self.reconciliation_notes,
            realised_usdt_pnl=float(self.realised_usdt_pnl),
            realised_delta_btc=float(self.realised_delta_btc),
            total_fees_paid_usdt=float(self.total_fees_paid_usdt),
            total_fees_paid_btc=float(self.total_fees_paid_btc),
        )

    # ------------------------------------------------------------------
    # Balance Reconciliation
    # ------------------------------------------------------------------

    def reconcile_balances(
        self,
        *,
        reported_btc_total: float,
        reported_usdt_total: float,
        source: str,
        now_utc: str | None = None,
        btc_tolerance: float = 1e-8,
        usdt_tolerance: float = 1e-4,
    ) -> ReconciliationStatus:
        """
        Compare internal ledger balances against external / manually reported balances.
        Flags DISCREPANCY and blocks new order proposals on mismatch.
        """
        if not self.configured or self.btc_total is None or self.usdt_total is None:
            raise LedgerError("Cannot reconcile balances when portfolio is NOT CONFIGURED.")

        ts_iso = ensure_utc_iso(now_utc or utc_now(), field_name="now_utc")
        rep_btc = _q_btc(_d(reported_btc_total))
        rep_usdt = _q_usdt(_d(reported_usdt_total))
        btc_diff = abs(rep_btc - self.btc_total)
        usdt_diff = abs(rep_usdt - self.usdt_total)

        if btc_diff > _d(btc_tolerance) or usdt_diff > _d(usdt_tolerance):
            self.reconciliation_status = ReconciliationStatus.DISCREPANCY
            self.reconciliation_notes = (
                f"Discrepancy vs {source}: BTC diff={btc_diff} (ledger={self.btc_total}, reported={rep_btc}); "
                f"USDT diff={usdt_diff} (ledger={self.usdt_total}, reported={rep_usdt})."
            )
            self.save()
            self.audit_logger.record(
                "BALANCE_RECONCILIATION_DISCREPANCY",
                actor=source,
                summary=self.reconciliation_notes,
                details={
                    "ledger_btc": float(self.btc_total),
                    "reported_btc": float(rep_btc),
                    "ledger_usdt": float(self.usdt_total),
                    "reported_usdt": float(rep_usdt),
                },
                timestamp_utc=ts_iso,
            )
            return self.reconciliation_status

        self.reconciliation_status = ReconciliationStatus.RECONCILED
        self.reconciliation_notes = f"Reconciled cleanly against {source} at {ts_iso}."
        self.last_reconciled_utc = ts_iso
        self.save()
        self.audit_logger.record(
            "BALANCE_RECONCILIATION_OK",
            actor=source,
            summary=self.reconciliation_notes,
            details={"btc_total": float(self.btc_total), "usdt_total": float(self.usdt_total)},
            timestamp_utc=ts_iso,
        )
        return self.reconciliation_status

    # ------------------------------------------------------------------
    # Order Proposal & Reservation (Manual Execution Lifecycle)
    # ------------------------------------------------------------------

    def propose_order(
        self,
        *,
        idempotency_key: str,
        side: str,
        limit_price: float,
        quantity_btc: float,
        estimated_fee_usdt: float,
        loop: LoopType,
        invalidation_condition: str,
        config: ConfigurationRecord,
        decision_id: str | None = None,
        assessment_id: str | None = None,
        cycle_id: str | None = None,
        expiry_utc: str | None = None,
        order_type: str = "LIMIT",
        instrument: str = "BTC/USDT",
        now_utc: str | None = None,
        notes: str = "",
    ) -> OrderRecord:
        """
        Create a PROPOSED limit order and reserve required tactical USDT (BUY) or
        tactical BTC (SELL). Never touches protected core BTC and never borrows.

        Idempotency: If idempotency_key was already processed with identical core
        parameters, returns the existing OrderRecord without duplicating reservations.
        """
        if not idempotency_key or not idempotency_key.strip():
            raise LedgerError("idempotency_key is required to prevent duplicate snapshot orders.")

        if idempotency_key in self.idempotency_index:
            existing = self.orders[self.idempotency_index[idempotency_key]]
            if (
                existing.side != side.upper()
                or abs(existing.limit_price - float(limit_price)) > 1e-8
                or abs(existing.requested_qty_btc - float(quantity_btc)) > 1e-8
            ):
                raise LedgerError(
                    f"Idempotency key '{idempotency_key}' already used for a different order specification."
                )
            return existing

        if not self.configured:
            raise LedgerError("Portfolio balances are NOT CONFIGURED; cannot propose order.")
        if self.reconciliation_status != ReconciliationStatus.RECONCILED:
            raise ReconciliationDiscrepancyError(
                f"Balance reconciliation status is {self.reconciliation_status.value}; resolve before proposing orders."
            )
        if instrument != "BTC/USDT":
            raise LedgerError(f"Unsupported instrument '{instrument}'; only spot BTC/USDT is permitted.")
        if order_type.upper() != "LIMIT":
            raise LedgerError(f"Only LIMIT orders are permitted by default; got '{order_type}'.")

        side_norm = side.upper().strip()
        if side_norm not in {"BUY", "SELL"}:
            raise LedgerError(f"Invalid spot order side '{side}'; expected BUY or SELL.")

        px = _d(limit_price)
        qty = _q_btc(_d(quantity_btc))
        fee_est = _q_usdt(_d(estimated_fee_usdt))
        if px <= 0 or qty <= 0 or fee_est < 0:
            raise LedgerError("limit_price and quantity_btc must be positive, and estimated_fee_usdt >= 0.")

        notional = _q_usdt(qty * px)
        ts_iso = ensure_utc_iso(now_utc or utc_now(), field_name="now_utc")
        exp_iso = ensure_utc_iso(expiry_utc, field_name="expiry_utc") if expiry_utc else None

        assert self.btc_tactical_available is not None and self.usdt_tactical_available is not None
        assert self.btc_core_protected is not None and self.btc_tactical is not None

        if side_norm == "BUY":
            reserve_amt = _q_usdt(notional + fee_est)
            avail_usdt = self.usdt_tactical_available
            if reserve_amt > avail_usdt:
                raise InsufficientInventoryError(
                    f"Proposed BUY requires {reserve_amt} USDT (incl. fee) > available tactical USDT {avail_usdt}."
                )
            min_usdt_floor = get_param(config, "portfolio_policy.min_usdt_inventory_floor")
            if min_usdt_floor not in (NOT_CONFIGURED, None):
                floor_dec = _q_usdt(_d(min_usdt_floor))
                if avail_usdt - reserve_amt < floor_dec:
                    raise InsufficientInventoryError(
                        f"Proposed BUY violates min_usdt_inventory_floor ({floor_dec} USDT)."
                    )
            reserved_asset = "USDT"
            self.usdt_reserved = _q_usdt(self.usdt_reserved + reserve_amt)
            reserved_float = float(reserve_amt)
        else:
            reserve_amt_btc = qty
            avail_btc = self.btc_tactical_available
            if reserve_amt_btc > avail_btc:
                total_with_core = avail_btc + self.btc_core_protected
                if reserve_amt_btc <= total_with_core:
                    raise ProtectedCoreViolationError(
                        f"Proposed SELL ({reserve_amt_btc} BTC) exceeds available tactical BTC ({avail_btc}) "
                        f"and would intrude on protected core BTC ({self.btc_core_protected})."
                    )
                raise InsufficientInventoryError(
                    f"Proposed SELL ({reserve_amt_btc} BTC) exceeds available tactical BTC ({avail_btc})."
                )
            min_btc_floor = get_param(config, "portfolio_policy.min_btc_inventory_floor")
            if min_btc_floor not in (NOT_CONFIGURED, None):
                floor_btc = _q_btc(_d(min_btc_floor))
                if avail_btc - reserve_amt_btc < floor_btc:
                    raise InsufficientInventoryError(
                        f"Proposed SELL violates min_btc_inventory_floor ({floor_btc} BTC)."
                    )
            reserved_asset = "BTC"
            self.btc_reserved = _q_btc(self.btc_reserved + reserve_amt_btc)
            reserved_float = float(reserve_amt_btc)

        snap = self.snapshot(spot_price=float(px), config_version=config.config_version, now_utc=ts_iso)
        order_id = f"ORD-{uuid.uuid4().hex[:12].upper()}"
        order = OrderRecord(
            order_id=order_id,
            idempotency_key=idempotency_key.strip(),
            decision_id=decision_id,
            assessment_id=assessment_id,
            cycle_id=cycle_id,
            loop=loop,
            portfolio_snapshot_id=snap.portfolio_snapshot_id,
            config_version=config.config_version,
            instrument="BTC/USDT",
            order_type="LIMIT",
            side=side_norm,
            limit_price=float(px),
            requested_qty_btc=float(qty),
            notional_usdt=float(notional),
            reserved_asset=reserved_asset,
            reserved_amount=reserved_float,
            remaining_reserved_amount=reserved_float,
            estimated_fee_usdt=float(fee_est),
            filled_qty_btc=0.0,
            avg_fill_price=None,
            actual_fees_usdt=0.0,
            actual_fees_btc=0.0,
            status=OrderStatus.PROPOSED,
            expiry_utc=exp_iso,
            invalidation_condition=invalidation_condition,
            exchange_order_ref=None,
            cancel_requested_utc=None,
            created_at_utc=ts_iso,
            updated_at_utc=ts_iso,
            fill_events=[],
            notes=notes,
        )
        self.orders[order_id] = order
        self.idempotency_index[idempotency_key.strip()] = order_id
        self.save()
        self.audit_logger.record(
            "ORDER_PROPOSED",
            actor="CORTEX_LEDGER",
            summary=f"Proposed {side_norm} LIMIT {qty} BTC @ {px} USDT (reserved {reserved_float} {reserved_asset}).",
            details=order.to_dict(),
            timestamp_utc=ts_iso,
        )
        return order

    def _get_order(self, order_id: str) -> OrderRecord:
        if order_id not in self.orders:
            raise OrderLifecycleError(f"Unknown order_id '{order_id}'.")
        return self.orders[order_id]

    def approve_order(self, order_id: str, *, operator_id: str, now_utc: str | None = None) -> OrderRecord:
        if self.reconciliation_status != ReconciliationStatus.RECONCILED:
            raise ReconciliationDiscrepancyError("Cannot approve order while balance reconciliation has a discrepancy.")
        order = self._get_order(order_id)
        if order.status != OrderStatus.PROPOSED:
            raise OrderLifecycleError(f"Order {order_id} must be PROPOSED to approve (current: {order.status.value}).")
        ts_iso = ensure_utc_iso(now_utc or utc_now(), field_name="now_utc")
        order.status = OrderStatus.APPROVED
        order.updated_at_utc = ts_iso
        self.save()
        self.audit_logger.record(
            "ORDER_APPROVED",
            actor=operator_id,
            summary=f"Operator approved order {order_id}.",
            details={"order_id": order_id},
            timestamp_utc=ts_iso,
        )
        return order

    def mark_submitted(
        self,
        order_id: str,
        *,
        operator_id: str,
        exchange_order_ref: str,
        now_utc: str | None = None,
    ) -> OrderRecord:
        order = self._get_order(order_id)
        if order.status != OrderStatus.APPROVED:
            raise OrderLifecycleError(f"Order {order_id} must be APPROVED before SUBMITTED.")
        if not exchange_order_ref.strip():
            raise OrderLifecycleError("exchange_order_ref is required when recording external submission.")
        ts_iso = ensure_utc_iso(now_utc or utc_now(), field_name="now_utc")
        order.status = OrderStatus.SUBMITTED
        order.exchange_order_ref = exchange_order_ref.strip()
        order.updated_at_utc = ts_iso
        self.save()
        self.audit_logger.record(
            "ORDER_SUBMITTED",
            actor=operator_id,
            summary=f"Operator recorded external submission for {order_id} (ref={exchange_order_ref.strip()}).",
            details={"order_id": order_id, "exchange_order_ref": exchange_order_ref.strip()},
            timestamp_utc=ts_iso,
        )
        return order

    def mark_working(self, order_id: str, *, operator_id: str, now_utc: str | None = None) -> OrderRecord:
        order = self._get_order(order_id)
        if order.status != OrderStatus.SUBMITTED:
            raise OrderLifecycleError(f"Order {order_id} must be SUBMITTED before WORKING.")
        ts_iso = ensure_utc_iso(now_utc or utc_now(), field_name="now_utc")
        order.status = OrderStatus.WORKING
        order.updated_at_utc = ts_iso
        self.save()
        self.audit_logger.record(
            "ORDER_WORKING",
            actor=operator_id,
            summary=f"Order {order_id} marked WORKING.",
            details={"order_id": order_id},
            timestamp_utc=ts_iso,
        )
        return order

    def record_fill(
        self,
        order_id: str,
        *,
        fill_qty_btc: float,
        fill_price_usdt: float,
        fee_asset: str,
        fee_amount: float,
        exchange_fill_ref: str,
        recorded_by: str,
        now_utc: str | None = None,
    ) -> OrderRecord:
        """
        Record a verified partial or full fill.
        Only the executed quantity changes inventory; unfilled remainder stays reserved.
        """
        order = self._get_order(order_id)
        if order.status not in {
            OrderStatus.APPROVED,
            OrderStatus.SUBMITTED,
            OrderStatus.WORKING,
            OrderStatus.PARTIALLY_FILLED,
        }:
            raise OrderLifecycleError(f"Cannot record fill on order {order_id} in status {order.status.value}.")

        fill_qty = _q_btc(_d(fill_qty_btc))
        fill_px = _d(fill_price_usdt)
        fee_dec = _d(fee_amount)
        fee_asset_norm = fee_asset.upper().strip()
        if fee_asset_norm not in {"USDT", "BTC"}:
            raise OrderLifecycleError(f"fee_asset must be USDT or BTC; got {fee_asset!r}.")
        if fill_qty <= 0 or fill_px <= 0 or fee_dec < 0:
            raise OrderLifecycleError("fill_qty_btc and fill_price_usdt must be > 0, and fee_amount >= 0.")

        prev_filled = _q_btc(_d(order.filled_qty_btc))
        req_qty = _q_btc(_d(order.requested_qty_btc))
        remaining_qty = _q_btc(req_qty - prev_filled)
        if fill_qty > remaining_qty:
            raise OrderLifecycleError(
                f"Fill quantity {fill_qty} BTC exceeds remaining unfilled quantity {remaining_qty} BTC."
            )

        assert self.btc_tactical is not None and self.usdt_tactical is not None
        ts_iso = ensure_utc_iso(now_utc or utc_now(), field_name="now_utc")
        gross_usdt = _q_usdt(fill_qty * fill_px)
        new_filled = _q_btc(prev_filled + fill_qty)
        is_fully_filled = new_filled == req_qty

        if order.side == "BUY":
            usdt_out = _q_usdt(gross_usdt + (_q_usdt(fee_dec) if fee_asset_norm == "USDT" else Decimal("0")))
            if usdt_out > self.usdt_tactical:
                raise InsufficientInventoryError(
                    f"Fill debit {usdt_out} USDT exceeds tactical USDT balance {self.usdt_tactical}."
                )
            btc_in = fill_qty - (_q_btc(fee_dec) if fee_asset_norm == "BTC" else Decimal("0"))
            if btc_in <= 0:
                raise LedgerError("BTC fee cannot exceed filled BTC quantity.")

            rem_res = _q_usdt(_d(order.remaining_reserved_amount))
            if is_fully_filled:
                res_release = rem_res
            else:
                res_release = min(rem_res, usdt_out)

            self.usdt_reserved = _q_usdt(max(Decimal("0"), self.usdt_reserved - res_release))
            self.usdt_tactical = _q_usdt(self.usdt_tactical - usdt_out)
            self.btc_tactical = _q_btc(self.btc_tactical + btc_in)
            order.remaining_reserved_amount = float(_q_usdt(rem_res - res_release))
        else:
            # SELL
            if fill_qty > self.btc_tactical or fill_qty > self.btc_reserved:
                raise InsufficientInventoryError("SELL fill exceeds tactical or reserved BTC balance.")
            usdt_in = _q_usdt(gross_usdt - (_q_usdt(fee_dec) if fee_asset_norm == "USDT" else Decimal("0")))
            if usdt_in < 0:
                raise LedgerError("USDT fee cannot exceed gross USDT proceeds.")

            rem_res_btc = _q_btc(_d(order.remaining_reserved_amount))
            res_release_btc = rem_res_btc if is_fully_filled else min(rem_res_btc, fill_qty)
            self.btc_reserved = _q_btc(max(Decimal("0"), self.btc_reserved - res_release_btc))
            self.btc_tactical = _q_btc(self.btc_tactical - fill_qty)
            self.usdt_tactical = _q_usdt(self.usdt_tactical + usdt_in)
            order.remaining_reserved_amount = float(_q_btc(rem_res_btc - res_release_btc))

        if fee_asset_norm == "USDT":
            fee_u = _q_usdt(fee_dec)
            order.actual_fees_usdt = float(_q_usdt(_d(order.actual_fees_usdt) + fee_u))
            self.total_fees_paid_usdt = _q_usdt(self.total_fees_paid_usdt + fee_u)
        else:
            fee_b = _q_btc(fee_dec)
            order.actual_fees_btc = float(_q_btc(_d(order.actual_fees_btc) + fee_b))
            self.total_fees_paid_btc = _q_btc(self.total_fees_paid_btc + fee_b)

        # Weighted average fill price
        prev_cost = _d(order.avg_fill_price or 0.0) * prev_filled
        order.avg_fill_price = float((prev_cost + gross_usdt) / new_filled)
        order.filled_qty_btc = float(new_filled)
        order.status = OrderStatus.FILLED if is_fully_filled else OrderStatus.PARTIALLY_FILLED
        order.updated_at_utc = ts_iso

        fill_event = FillEvent(
            fill_id=f"FIL-{uuid.uuid4().hex[:10].upper()}",
            order_id=order_id,
            timestamp_utc=ts_iso,
            fill_qty_btc=float(fill_qty),
            fill_price_usdt=float(fill_px),
            gross_usdt=float(gross_usdt),
            fee_asset=fee_asset_norm,
            fee_amount=float(fee_dec),
            exchange_fill_ref=exchange_fill_ref,
            recorded_by=recorded_by,
        )
        order.fill_events.append(fill_event)

        if order.cycle_id and order.cycle_id in self.cycles:
            self._recalculate_cycle(order.cycle_id, ts_iso)

        self.save()
        self.audit_logger.record(
            "ORDER_FILL_RECORDED",
            actor=recorded_by,
            summary=f"Recorded fill {fill_qty} BTC @ {fill_px} USDT on {order_id} ({order.status.value}).",
            details=fill_event.to_dict(),
            timestamp_utc=ts_iso,
        )
        return order

    def request_cancellation(self, order_id: str, *, operator_id: str, now_utc: str | None = None) -> OrderRecord:
        """
        Record that cancellation was requested externally.
        Does NOT release inventory reservation until confirm_terminal_status() is called.
        """
        order = self._get_order(order_id)
        if order.status in {OrderStatus.FILLED, OrderStatus.CANCELLED, OrderStatus.EXPIRED, OrderStatus.REJECTED}:
            raise OrderLifecycleError(f"Order {order_id} is already terminal ({order.status.value}).")
        ts_iso = ensure_utc_iso(now_utc or utc_now(), field_name="now_utc")
        order.cancel_requested_utc = ts_iso
        order.updated_at_utc = ts_iso
        self.save()
        self.audit_logger.record(
            "ORDER_CANCEL_REQUESTED",
            actor=operator_id,
            summary=f"Cancellation requested for {order_id}; reservation retained pending confirmation.",
            details={"order_id": order_id, "remaining_reserved_amount": order.remaining_reserved_amount},
            timestamp_utc=ts_iso,
        )
        return order

    def confirm_terminal_status(
        self,
        order_id: str,
        *,
        terminal_status: OrderStatus,
        confirmed_by: str,
        reason: str = "",
        now_utc: str | None = None,
    ) -> OrderRecord:
        """
        Confirm CANCELLED, EXPIRED, or REJECTED status and release remaining unfilled reservation.
        """
        if terminal_status not in {OrderStatus.CANCELLED, OrderStatus.EXPIRED, OrderStatus.REJECTED}:
            raise OrderLifecycleError(
                f"confirm_terminal_status only accepts CANCELLED, EXPIRED, or REJECTED; got {terminal_status.value}."
            )
        order = self._get_order(order_id)
        if order.status in {OrderStatus.FILLED, OrderStatus.CANCELLED, OrderStatus.EXPIRED, OrderStatus.REJECTED}:
            raise OrderLifecycleError(f"Order {order_id} is already terminal ({order.status.value}).")

        ts_iso = ensure_utc_iso(now_utc or utc_now(), field_name="now_utc")
        if order.reserved_asset == "USDT":
            rem = _q_usdt(_d(order.remaining_reserved_amount))
            self.usdt_reserved = _q_usdt(max(Decimal("0"), self.usdt_reserved - rem))
        else:
            rem_btc = _q_btc(_d(order.remaining_reserved_amount))
            self.btc_reserved = _q_btc(max(Decimal("0"), self.btc_reserved - rem_btc))

        released = order.remaining_reserved_amount
        order.remaining_reserved_amount = 0.0
        order.status = terminal_status
        order.updated_at_utc = ts_iso
        if reason:
            order.notes = f"{order.notes} | {reason}".strip(" |")

        self.save()
        self.audit_logger.record(
            f"ORDER_{terminal_status.value}",
            actor=confirmed_by,
            summary=f"Confirmed {terminal_status.value} for {order_id}; released {released} {order.reserved_asset}.",
            details={"order_id": order_id, "released_amount": released, "asset": order.reserved_asset, "reason": reason},
            timestamp_utc=ts_iso,
        )
        return order

    # ------------------------------------------------------------------
    # Independent Conversion Cycle Accounting (Loop A & Loop B)
    # ------------------------------------------------------------------

    def open_cycle(
        self,
        *,
        loop: LoopType,
        starting_qty: float,
        original_setup_ref: str,
        now_utc: str | None = None,
    ) -> ConversionCycle:
        if starting_qty <= 0:
            raise LedgerError("starting_qty must be positive.")
        ts_iso = ensure_utc_iso(now_utc or utc_now(), field_name="now_utc")
        cycle_id = f"CYC-{loop.value[-1]}-{uuid.uuid4().hex[:10].upper()}"
        starting_asset = "USDT" if loop == LoopType.LOOP_A else "BTC"
        cycle = ConversionCycle(
            cycle_id=cycle_id,
            loop=loop,
            starting_asset=starting_asset,
            starting_qty=float(starting_qty),
            original_setup_ref=original_setup_ref,
            status=CycleStatus.OPEN,
            created_at_utc=ts_iso,
        )
        self.cycles[cycle_id] = cycle
        self.save()
        self.audit_logger.record(
            "CONVERSION_CYCLE_OPENED",
            actor="CORTEX_LEDGER",
            summary=f"Opened {loop.value} cycle {cycle_id} starting with {starting_qty} {starting_asset}.",
            details=cycle.to_dict(),
            timestamp_utc=ts_iso,
        )
        return cycle

    def link_order_to_cycle(self, cycle_id: str, order_id: str, *, leg: str) -> ConversionCycle:
        if cycle_id not in self.cycles:
            raise LedgerError(f"Unknown cycle_id '{cycle_id}'.")
        order = self._get_order(order_id)
        cycle = self.cycles[cycle_id]
        if order.loop != cycle.loop:
            raise LedgerError(f"Order loop {order.loop.value} does not match cycle loop {cycle.loop.value}.")
        leg_norm = leg.upper().strip()
        if leg_norm not in {"ENTRY", "EXIT"}:
            raise LedgerError("leg must be ENTRY or EXIT.")
        target_list = cycle.entry_order_ids if leg_norm == "ENTRY" else cycle.exit_order_ids
        if order_id not in target_list:
            target_list.append(order_id)
        order.cycle_id = cycle_id
        self._recalculate_cycle(cycle_id, order.updated_at_utc)
        self.save()
        return cycle

    def _recalculate_cycle(self, cycle_id: str, ts_iso: str) -> None:
        cycle = self.cycles[cycle_id]
        entry_btc = Decimal("0")
        entry_usdt = Decimal("0")
        entry_fees_usdt = Decimal("0")
        entry_fees_btc = Decimal("0")
        exit_btc = Decimal("0")
        exit_usdt = Decimal("0")
        exit_fees_usdt = Decimal("0")
        exit_fees_btc = Decimal("0")

        terminal_statuses = {
            OrderStatus.FILLED,
            OrderStatus.CANCELLED,
            OrderStatus.EXPIRED,
            OrderStatus.REJECTED,
        }
        all_entry_terminal = bool(cycle.entry_order_ids) and all(
            self.orders[oid].status in terminal_statuses for oid in cycle.entry_order_ids
        )
        all_exit_terminal = bool(cycle.exit_order_ids) and all(
            self.orders[oid].status in terminal_statuses for oid in cycle.exit_order_ids
        )

        for oid in cycle.entry_order_ids:
            o = self.orders[oid]
            for f in o.fill_events:
                entry_btc += _d(f.fill_qty_btc)
                entry_usdt += _d(f.gross_usdt)
            entry_fees_usdt += _d(o.actual_fees_usdt)
            entry_fees_btc += _d(o.actual_fees_btc)

        for oid in cycle.exit_order_ids:
            o = self.orders[oid]
            for f in o.fill_events:
                exit_btc += _d(f.fill_qty_btc)
                exit_usdt += _d(f.gross_usdt)
            exit_fees_usdt += _d(o.actual_fees_usdt)
            exit_fees_btc += _d(o.actual_fees_btc)

        total_fees_usdt = entry_fees_usdt + exit_fees_usdt
        total_fees_btc = entry_fees_btc + exit_fees_btc

        cycle.entry_filled_btc = float(_q_btc(entry_btc))
        cycle.entry_filled_usdt = float(_q_usdt(entry_usdt))
        cycle.exit_filled_btc = float(_q_btc(exit_btc))
        cycle.exit_filled_usdt = float(_q_usdt(exit_usdt))
        cycle.total_fees_usdt = float(_q_usdt(total_fees_usdt))
        cycle.total_fees_btc = float(_q_btc(total_fees_btc))

        # Determine completion strictly from actual fills on terminal entry+exit orders
        # (never from proposed/open orders)
        if cycle.loop == LoopType.LOOP_A:
            if entry_btc > 0 and exit_btc > 0 and all_entry_terminal and all_exit_terminal:
                net_usdt = (exit_usdt - exit_fees_usdt) - (entry_usdt + entry_fees_usdt)
                cycle.realised_net_usdt = float(_q_usdt(net_usdt))
                cycle.status = CycleStatus.COMPLETED
                cycle.completed_at_utc = ts_iso
            elif entry_btc > 0 or exit_btc > 0:
                cycle.status = CycleStatus.PARTIALLY_CONVERTED
                cycle.realised_net_usdt = None
                cycle.completed_at_utc = None
            else:
                cycle.status = CycleStatus.OPEN
                cycle.realised_net_usdt = None
                cycle.completed_at_utc = None
        else:
            # LOOP_B: BTC -> USDT -> BTC; delta_btc = BTC repurchased (net of exit BTC fee) - BTC sold
            if entry_btc > 0 and exit_btc > 0 and all_entry_terminal and all_exit_terminal:
                net_btc_repurchased = exit_btc - exit_fees_btc
                net_btc_sold = entry_btc + entry_fees_btc
                delta_btc = net_btc_repurchased - net_btc_sold
                cycle.delta_btc = float(_q_btc(delta_btc))
                cycle.status = CycleStatus.COMPLETED
                cycle.completed_at_utc = ts_iso
            elif entry_btc > 0 or exit_btc > 0:
                cycle.status = CycleStatus.PARTIALLY_CONVERTED
                cycle.delta_btc = None
                cycle.completed_at_utc = None
            else:
                cycle.status = CycleStatus.OPEN
                cycle.delta_btc = None
                cycle.completed_at_utc = None

        # Recompute cumulative realised Loop A USDT PnL and Loop B delta BTC idempotently
        self.realised_usdt_pnl = _q_usdt(
            sum(
                (_d(c.realised_net_usdt) for c in self.cycles.values() if c.loop == LoopType.LOOP_A and c.realised_net_usdt is not None),
                Decimal("0"),
            )
        )
        self.realised_delta_btc = _q_btc(
            sum(
                (_d(c.delta_btc) for c in self.cycles.values() if c.loop == LoopType.LOOP_B and c.delta_btc is not None),
                Decimal("0"),
            )
        )
