"""
Structured domain records for CORTEX-BTC (Section 17 of CORTEX-ANTIGRAVITY-HANDOVER-001).

All internal timestamps are stored as UTC ISO-8601 strings ('...Z').
Unconfigured or unavailable fields are explicitly preserved as None /
NOT CONFIGURED / DATA UNAVAILABLE / UNVALIDATED — never fabricated.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from cortex_core.constants import (
    DATA_UNAVAILABLE,
    NOT_CONFIGURED,
    UNVALIDATED,
    CycleStatus,
    DataStatus,
    ExitClassification,
    LoopType,
    ModuleState,
    OperatingMode,
    OrderStatus,
    PortfolioState,
    ReconciliationStatus,
    Verdict,
)


@dataclass(slots=True)
class DataFieldRecord:
    """Provenance, timestamp, and classification metadata for a single market field."""

    field_name: str
    value: Any
    source: str
    exchange_or_provider: str
    instrument: str
    timeframe: str
    source_event_ts_utc: str | None
    retrieved_ts_utc: str
    last_successful_update_utc: str | None
    validation_status: DataStatus
    freshness_status: str  # "FRESH" | "STALE" | "NOT CONFIGURED" | "UNAVAILABLE"
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        out = asdict(self)
        out["validation_status"] = self.validation_status.value
        return out


@dataclass(slots=True)
class MarketSnapshot:
    """Section 17 MarketSnapshot with explicit source provenance and data classification."""

    snapshot_id: str
    retrieved_ts_utc: str
    source_event_ts_utc: str | None
    instrument: str
    timeframe: str
    overall_integrity_status: DataStatus
    spot_price: float | None
    venue_prices: dict[str, dict[str, Any]]
    fields: dict[str, DataFieldRecord]
    missing_or_unavailable_fields: list[str] = field(default_factory=list)
    stale_fields: list[str] = field(default_factory=list)
    conflicting_fields: list[str] = field(default_factory=list)
    proxy_fields: list[str] = field(default_factory=list)
    raw_errors: list[str] = field(default_factory=list)
    snapshot_sha256: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "retrieved_ts_utc": self.retrieved_ts_utc,
            "source_event_ts_utc": self.source_event_ts_utc,
            "instrument": self.instrument,
            "timeframe": self.timeframe,
            "overall_integrity_status": self.overall_integrity_status.value,
            "spot_price": self.spot_price,
            "venue_prices": self.venue_prices,
            "fields": {k: v.to_dict() for k, v in self.fields.items()},
            "missing_or_unavailable_fields": list(self.missing_or_unavailable_fields),
            "stale_fields": list(self.stale_fields),
            "conflicting_fields": list(self.conflicting_fields),
            "proxy_fields": list(self.proxy_fields),
            "raw_errors": list(self.raw_errors),
            "snapshot_sha256": self.snapshot_sha256,
        }


@dataclass(slots=True)
class PortfolioSnapshot:
    """
    Section 17 PortfolioSnapshot.

    Unconfigured balances remain None with display_status='NOT CONFIGURED / DATA UNAVAILABLE'
    so an unconfigured balance is never misrepresented as zero.
    """

    portfolio_snapshot_id: str
    timestamp_utc: str
    config_version: int
    configured: bool
    btc_total: float | None
    btc_available: float | None
    btc_reserved: float | None
    btc_core_protected: float | None
    btc_tactical: float | None
    btc_tactical_available: float | None
    btc_loop_a_committed: float | None
    btc_loop_b_committed: float | None
    usdt_total: float | None
    usdt_available: float | None
    usdt_reserved: float | None
    usdt_core_protected: float | None
    usdt_tactical: float | None
    usdt_tactical_available: float | None
    usdt_loop_a_committed: float | None
    usdt_loop_b_proceeds: float | None
    valuation_spot_price: float | None
    total_portfolio_value_usdt: float | None
    active_sleeve_value_usdt: float | None
    protected_core_btc_value_usdt: float | None
    btc_exposure_pct: float | None
    usdt_exposure_pct: float | None
    reconciliation_status: ReconciliationStatus
    reconciliation_notes: str = ""
    realised_usdt_pnl: float = 0.0
    realised_delta_btc: float = 0.0
    total_fees_paid_usdt: float = 0.0
    total_fees_paid_btc: float = 0.0

    def display_field(self, field_name: str) -> Any:
        """Return explicit NOT CONFIGURED / DATA UNAVAILABLE string when value is None."""
        val = getattr(self, field_name)
        if val is None:
            return NOT_CONFIGURED if not self.configured else DATA_UNAVAILABLE
        return val

    def to_dict(self) -> dict[str, Any]:
        out = asdict(self)
        out["reconciliation_status"] = self.reconciliation_status.value
        return out


@dataclass(slots=True)
class FillEvent:
    """Verified manual execution fill event for an OrderRecord."""

    fill_id: str
    order_id: str
    timestamp_utc: str
    fill_qty_btc: float
    fill_price_usdt: float
    gross_usdt: float
    fee_asset: str
    fee_amount: float
    exchange_fill_ref: str
    recorded_by: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class OrderRecord:
    """
    Section 17 OrderRecord tracking manual limit-order lifecycle and reservations.

    Autonomous execution is prohibited; status transitions reflect verified
    operator records only.
    """

    order_id: str
    idempotency_key: str
    decision_id: str | None
    assessment_id: str | None
    cycle_id: str | None
    loop: LoopType
    portfolio_snapshot_id: str
    config_version: int
    instrument: str
    order_type: str  # "LIMIT"
    side: str  # "BUY" | "SELL"
    limit_price: float
    requested_qty_btc: float
    notional_usdt: float
    reserved_asset: str  # "USDT" for BUY | "BTC" for SELL
    reserved_amount: float
    remaining_reserved_amount: float
    estimated_fee_usdt: float
    filled_qty_btc: float
    avg_fill_price: float | None
    actual_fees_usdt: float
    actual_fees_btc: float
    status: OrderStatus
    expiry_utc: str | None
    invalidation_condition: str
    exchange_order_ref: str | None
    cancel_requested_utc: str | None
    created_at_utc: str
    updated_at_utc: str
    fill_events: list[FillEvent] = field(default_factory=list)
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        out = asdict(self)
        out["loop"] = self.loop.value
        out["status"] = self.status.value
        out["fill_events"] = [f.to_dict() for f in self.fill_events]
        return out

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "OrderRecord":
        fills = [FillEvent(**f) for f in data.get("fill_events", [])]
        return cls(
            order_id=data["order_id"],
            idempotency_key=data["idempotency_key"],
            decision_id=data.get("decision_id"),
            assessment_id=data.get("assessment_id"),
            cycle_id=data.get("cycle_id"),
            loop=LoopType(data["loop"]),
            portfolio_snapshot_id=data["portfolio_snapshot_id"],
            config_version=int(data["config_version"]),
            instrument=data["instrument"],
            order_type=data["order_type"],
            side=data["side"],
            limit_price=float(data["limit_price"]),
            requested_qty_btc=float(data["requested_qty_btc"]),
            notional_usdt=float(data["notional_usdt"]),
            reserved_asset=data["reserved_asset"],
            reserved_amount=float(data["reserved_amount"]),
            remaining_reserved_amount=float(data["remaining_reserved_amount"]),
            estimated_fee_usdt=float(data["estimated_fee_usdt"]),
            filled_qty_btc=float(data["filled_qty_btc"]),
            avg_fill_price=float(data["avg_fill_price"]) if data.get("avg_fill_price") is not None else None,
            actual_fees_usdt=float(data.get("actual_fees_usdt", 0.0)),
            actual_fees_btc=float(data.get("actual_fees_btc", 0.0)),
            status=OrderStatus(data["status"]),
            expiry_utc=data.get("expiry_utc"),
            invalidation_condition=data["invalidation_condition"],
            exchange_order_ref=data.get("exchange_order_ref"),
            cancel_requested_utc=data.get("cancel_requested_utc"),
            created_at_utc=data["created_at_utc"],
            updated_at_utc=data["updated_at_utc"],
            fill_events=fills,
            notes=data.get("notes", ""),
        )


@dataclass(slots=True)
class ConversionCycle:
    """Section 17 ConversionCycle for independent Loop A and Loop B accounting."""

    cycle_id: str
    loop: LoopType
    starting_asset: str  # "USDT" for Loop A | "BTC" for Loop B
    starting_qty: float
    original_setup_ref: str
    entry_order_ids: list[str] = field(default_factory=list)
    exit_order_ids: list[str] = field(default_factory=list)
    entry_filled_btc: float = 0.0
    entry_filled_usdt: float = 0.0
    exit_filled_btc: float = 0.0
    exit_filled_usdt: float = 0.0
    total_fees_usdt: float = 0.0
    total_fees_btc: float = 0.0
    realised_net_usdt: float | None = None
    delta_btc: float | None = None
    status: CycleStatus = CycleStatus.OPEN
    created_at_utc: str = ""
    completed_at_utc: str | None = None

    def to_dict(self) -> dict[str, Any]:
        out = asdict(self)
        out["loop"] = self.loop.value
        out["status"] = self.status.value
        return out

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ConversionCycle":
        return cls(
            cycle_id=data["cycle_id"],
            loop=LoopType(data["loop"]),
            starting_asset=data["starting_asset"],
            starting_qty=float(data["starting_qty"]),
            original_setup_ref=data.get("original_setup_ref", ""),
            entry_order_ids=list(data.get("entry_order_ids", [])),
            exit_order_ids=list(data.get("exit_order_ids", [])),
            entry_filled_btc=float(data.get("entry_filled_btc", 0.0)),
            entry_filled_usdt=float(data.get("entry_filled_usdt", 0.0)),
            exit_filled_btc=float(data.get("exit_filled_btc", 0.0)),
            exit_filled_usdt=float(data.get("exit_filled_usdt", 0.0)),
            total_fees_usdt=float(data.get("total_fees_usdt", 0.0)),
            total_fees_btc=float(data.get("total_fees_btc", 0.0)),
            realised_net_usdt=float(data["realised_net_usdt"]) if data.get("realised_net_usdt") is not None else None,
            delta_btc=float(data["delta_btc"]) if data.get("delta_btc") is not None else None,
            status=CycleStatus(data["status"]),
            created_at_utc=data["created_at_utc"],
            completed_at_utc=data.get("completed_at_utc"),
        )


@dataclass(slots=True)
class ConfigurationRecord:
    """Section 17 ConfigurationRecord with explicit audit trail and UNVALIDATED marker."""

    config_version: int
    operating_mode: OperatingMode
    validation_status: str  # Always UNVALIDATED until backtested & approved
    instrument: str
    spot_only: bool
    autonomous_execution: bool
    parameters: dict[str, Any]
    previous_values: dict[str, Any]
    new_values: dict[str, Any]
    operator_id: str
    change_reason: str
    operator_acknowledged: bool
    changed_at_utc: str

    def to_dict(self) -> dict[str, Any]:
        out = asdict(self)
        out["operating_mode"] = self.operating_mode.value
        return out

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ConfigurationRecord":
        return cls(
            config_version=int(data["config_version"]),
            operating_mode=OperatingMode(data.get("operating_mode", OperatingMode.RESEARCH.value)),
            validation_status=data.get("validation_status", UNVALIDATED),
            instrument=data.get("instrument", "BTC/USDT"),
            spot_only=bool(data.get("spot_only", True)),
            autonomous_execution=bool(data.get("autonomous_execution", False)),
            parameters=dict(data.get("parameters", {})),
            previous_values=dict(data.get("previous_values", {})),
            new_values=dict(data.get("new_values", {})),
            operator_id=data.get("operator_id", NOT_CONFIGURED),
            change_reason=data.get("change_reason", ""),
            operator_acknowledged=bool(data.get("operator_acknowledged", False)),
            changed_at_utc=data["changed_at_utc"],
        )


@dataclass(slots=True)
class EvidenceCheckItem:
    """Single evidence row inside Module A or Module B assessment."""

    name: str
    status: str  # "PASS" | "FAIL" | "UNAVAILABLE" | "NOT CONFIGURED" | "CONTEXT"
    observed_value: Any
    source_status: str
    rationale: str
    is_mandatory: bool = True

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ModuleAssessment:
    """
    Section 17 ModuleAssessment (non-authoritative input to Module C / Module D).

    Neither Module A nor Module B can authorize a transaction independently.
    """

    assessment_id: str
    module_name: str  # "MODULE_A_ACCUMULATION" | "MODULE_B_DISTRIBUTION"
    setup_id: str
    timestamp_utc: str
    market_snapshot_id: str
    config_version: int
    state: ModuleState
    directional_signal: str  # Module A: BUY|WAIT|REJECTED; Module B: SELL|REDUCE|HOLD|WAIT
    has_execution_authority: bool  # Always False
    exit_classification: ExitClassification | None
    bearish_pattern: str | None  # DISTRIBUTION_REVERSAL | STRUCTURAL_BREAKDOWN | PROFIT_TARGET | None
    checklist: list[EvidenceCheckItem]
    qualifying_conditions: list[str]
    failed_conditions: list[str]
    unavailable_data: list[str]
    unconfigured_thresholds: list[str]
    mechanism_evaluations: dict[str, dict[str, Any]] = field(default_factory=dict)
    proposed_limit_price: float | None = None
    invalidation_price: float | None = None
    setup_expiry_utc: str | None = None
    observed_summary: str = ""
    interpretation_summary: str = ""

    def to_dict(self) -> dict[str, Any]:
        out = asdict(self)
        out["state"] = self.state.value
        out["exit_classification"] = self.exit_classification.value if self.exit_classification else None
        out["checklist"] = [item.to_dict() for item in self.checklist]
        return out


@dataclass(slots=True)
class ConstraintLimit:
    """Single sizing limit evaluated by Module C."""

    name: str
    max_qty_btc: float
    max_notional_usdt: float
    details: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class SizingBreakdown:
    """Transparent BUY or SELL sizing calculation from Module C."""

    side: str  # "BUY" | "SELL"
    proposed_limit_price: float | None
    permitted_qty_btc: float
    gross_usdt: float
    estimated_fee_usdt: float
    estimated_slippage_usdt: float
    net_usdt: float  # Total USDT cost for BUY; Net USDT proceeds for SELL
    remaining_available_btc: float | None
    remaining_available_usdt: float | None
    resulting_btc_allocation_pct: float | None
    resulting_usdt_allocation_pct: float | None
    invalidation_price: float | None
    distance_to_invalidation_pct: float | None
    estimated_risk_at_invalidation_usdt: float | None
    inventory_floor_compliant: bool
    core_btc_intact: bool
    limiting_constraint_name: str
    constraints_evaluated: list[ConstraintLimit]
    sizing_status: str  # "ELIGIBLE" | "REJECTED" | "NOT CONFIGURED" | "UNAVAILABLE"
    rejection_reason: str = ""

    def to_dict(self) -> dict[str, Any]:
        out = asdict(self)
        out["constraints_evaluated"] = [c.to_dict() for c in self.constraints_evaluated]
        return out


@dataclass(slots=True)
class AllocationAssessment:
    """Section 17 AllocationAssessment produced by Module C."""

    allocation_id: str
    timestamp_utc: str
    portfolio_snapshot_id: str
    config_version: int
    regime_label: str
    current_btc_pct: float | None
    current_usdt_pct: float | None
    permitted_exposure_band: dict[str, Any]
    proposed_target_btc_pct: float | None
    exposure_delta_pct: float | None
    estimated_qty_to_target_btc: float | None
    btc_floor_compliant: bool
    usdt_floor_compliant: bool
    core_btc_intact: bool
    buy_sizing: SizingBreakdown | None
    sell_sizing: SizingBreakdown | None
    permitted_side: str  # "BUY" | "SELL" | "NONE"
    permitted_quantity_btc: float
    limiting_constraint_name: str
    sizing_status: str
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        out = asdict(self)
        out["buy_sizing"] = self.buy_sizing.to_dict() if self.buy_sizing else None
        out["sell_sizing"] = self.sell_sizing.to_dict() if self.sell_sizing else None
        return out


@dataclass(slots=True)
class GateResult:
    """Single deterministic gate outcome inside Module D's 10-gate pipeline."""

    gate_number: int
    gate_name: str
    status: str  # "PASS" | "FAIL" | "UNAVAILABLE" | "NOT CONFIGURED" | "SKIPPED"
    summary: str
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class DecisionRecord:
    """Section 17 DecisionRecord produced by Module D (Final Decision Authority)."""

    decision_id: str
    timestamp_utc: str
    market_snapshot_id: str
    portfolio_snapshot_id: str
    config_version: int
    software_version: str
    operating_mode: OperatingMode
    validation_status: str
    data_integrity_status: str
    regime_label: str
    gates: list[GateResult]
    module_a_assessment_id: str
    module_b_assessment_id: str
    allocation_assessment_id: str
    final_verdict: Verdict
    previous_operating_state: PortfolioState
    new_operating_state: PortfolioState
    state_transition_reason: str
    proposed_order: dict[str, Any] | None
    rejection_or_abstention_reasons: list[str]
    plain_english_summary: str
    determinism_sha256: str = ""

    def to_dict(self) -> dict[str, Any]:
        out = asdict(self)
        out["operating_mode"] = self.operating_mode.value
        out["final_verdict"] = self.final_verdict.value
        out["previous_operating_state"] = self.previous_operating_state.value
        out["new_operating_state"] = self.new_operating_state.value
        out["gates"] = [g.to_dict() for g in self.gates]
        return out


@dataclass(slots=True)
class AuditEvent:
    """Immutable UTC-timestamped audit log entry."""

    event_id: str
    event_type: str
    timestamp_utc: str
    actor: str
    summary: str
    details: dict[str, Any]
    event_sha256: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
