"""Shared deterministic evidence evaluation helpers for Module A and Module B."""

from __future__ import annotations

from typing import Any

from btc_config_loader import get_param
from cortex_core.constants import DATA_UNAVAILABLE, NOT_CONFIGURED, DataStatus
from cortex_core.models import ConfigurationRecord, EvidenceCheckItem, MarketSnapshot


def field_info(snapshot: MarketSnapshot, name: str) -> tuple[Any, DataStatus]:
    """Safely extract (value, DataStatus) from a MarketSnapshot."""
    rec = snapshot.fields.get(name)
    if rec is None:
        return None, DataStatus.UNAVAILABLE
    return rec.value, rec.validation_status


def check_data_integrity(
    snapshot: MarketSnapshot,
    config: ConfigurationRecord,
) -> tuple[EvidenceCheckItem, bool]:
    """
    Evaluate whether critical spot data satisfies configured integrity & freshness policy.
    Returns (EvidenceCheckItem, is_halted).
    """
    spot_val, spot_status = field_info(snapshot, "spot_price")
    cvd_val, cvd_status = field_info(snapshot, "spot_cvd_24h_btc")
    stale_cvd_blocks = bool(get_param(config, "data_policy.stale_spot_cvd_blocks_decision", True))

    reasons: list[str] = []
    if snapshot.overall_integrity_status in {DataStatus.UNAVAILABLE, DataStatus.CONFLICTING}:
        reasons.append(f"overall_integrity={snapshot.overall_integrity_status.value}")
    if spot_val is None or spot_status in {DataStatus.UNAVAILABLE, DataStatus.STALE, DataStatus.CONFLICTING}:
        reasons.append(f"spot_price={spot_status.value}")
    if stale_cvd_blocks and cvd_status in {DataStatus.STALE, DataStatus.CONFLICTING}:
        reasons.append(f"spot_cvd_24h_btc={cvd_status.value}")

    mandatory = get_param(config, "data_policy.mandatory_feeds", ["binance_spot_price"])
    if isinstance(mandatory, list):
        for fname in mandatory:
            val, st = field_info(snapshot, fname)
            if val is None or st in {DataStatus.UNAVAILABLE, DataStatus.STALE, DataStatus.CONFLICTING}:
                reasons.append(f"{fname}={st.value}")

    # Deduplicate while preserving order
    unique_reasons = list(dict.fromkeys(reasons))
    halted = bool(unique_reasons)
    item = EvidenceCheckItem(
        name="data_integrity",
        status="FAIL" if halted else "PASS",
        observed_value={
            "overall_integrity": snapshot.overall_integrity_status.value,
            "spot_price": spot_val,
            "spot_cvd_status": cvd_status.value,
            "spot_cvd_value": cvd_val,
        },
        source_status=snapshot.overall_integrity_status.value,
        rationale=(
            f"Critical data gate failed: {', '.join(unique_reasons)}."
            if halted
            else "Critical spot telemetry passed integrity checks."
        ),
        is_mandatory=True,
    )
    return item, halted


def evaluate_execution_economics(
    snapshot: MarketSnapshot,
    config: ConfigurationRecord,
    *,
    side: str,
    proposed_limit_price: float | None,
    invalidation_price: float | None,
) -> EvidenceCheckItem:
    """
    Assess limit-order execution feasibility (spread, depth, fees/slippage, stop distance).
    Never invents missing liquidity data or unconfigured fee/slippage assumptions.
    """
    spread_bps, spread_st = field_info(snapshot, "spread_bps")
    depth_usd, depth_st = field_info(snapshot, "depth_1pct_usd")
    maker_fee = get_param(config, "execution_assumptions.maker_fee_bps")
    slippage = get_param(config, "execution_assumptions.expected_slippage_bps")

    if spread_st == DataStatus.UNAVAILABLE or depth_st == DataStatus.UNAVAILABLE:
        return EvidenceCheckItem(
            name="execution_economics",
            status="UNAVAILABLE",
            observed_value={"spread_bps": spread_bps, "depth_1pct_usd": depth_usd},
            source_status=DataStatus.UNAVAILABLE.value,
            rationale="Order-book spread or +/-1% depth is unavailable.",
            is_mandatory=True,
        )

    if spread_st in {DataStatus.STALE, DataStatus.CONFLICTING} or depth_st in {
        DataStatus.STALE,
        DataStatus.CONFLICTING,
    }:
        return EvidenceCheckItem(
            name="execution_economics",
            status="FAIL",
            observed_value={"spread_bps": spread_bps, "depth_1pct_usd": depth_usd},
            source_status=DataStatus.STALE.value,
            rationale="Order-book liquidity snapshot is stale or conflicting.",
            is_mandatory=True,
        )

    if maker_fee == NOT_CONFIGURED or slippage == NOT_CONFIGURED:
        return EvidenceCheckItem(
            name="execution_economics",
            status=NOT_CONFIGURED,
            observed_value={
                "spread_bps": spread_bps,
                "depth_1pct_usd": depth_usd,
                "maker_fee_bps": maker_fee,
                "expected_slippage_bps": slippage,
            },
            source_status=DataStatus.VERIFIED.value,
            rationale="Fee or expected slippage assumptions are NOT CONFIGURED.",
            is_mandatory=True,
        )

    if proposed_limit_price is None or proposed_limit_price <= 0:
        return EvidenceCheckItem(
            name="execution_economics",
            status="FAIL",
            observed_value={"proposed_limit_price": proposed_limit_price},
            source_status=DataStatus.VERIFIED.value,
            rationale="Valid proposed limit price is absent.",
            is_mandatory=True,
        )

    if side == "BUY":
        max_stop_pct = get_param(config, "buy_criteria.max_stop_distance_pct")
        if max_stop_pct == NOT_CONFIGURED:
            return EvidenceCheckItem(
                name="execution_economics",
                status=NOT_CONFIGURED,
                observed_value={"max_stop_distance_pct": NOT_CONFIGURED},
                source_status=DataStatus.VERIFIED.value,
                rationale="buy_criteria.max_stop_distance_pct is NOT CONFIGURED.",
                is_mandatory=True,
            )
        if invalidation_price is None or invalidation_price >= proposed_limit_price:
            return EvidenceCheckItem(
                name="execution_economics",
                status="FAIL",
                observed_value={
                    "proposed_limit_price": proposed_limit_price,
                    "invalidation_price": invalidation_price,
                },
                source_status=DataStatus.VERIFIED.value,
                rationale="BUY setup lacks valid protective invalidation price below limit-buy price.",
                is_mandatory=True,
            )
        stop_dist_pct = ((proposed_limit_price - invalidation_price) / proposed_limit_price) * 100.0
        if stop_dist_pct > float(max_stop_pct):
            return EvidenceCheckItem(
                name="execution_economics",
                status="FAIL",
                observed_value={"stop_distance_pct": round(stop_dist_pct, 3), "max_stop_pct": float(max_stop_pct)},
                source_status=DataStatus.VERIFIED.value,
                rationale=f"Invalidation distance {stop_dist_pct:.2f}% exceeds max {float(max_stop_pct):.2f}%.",
                is_mandatory=True,
            )

    return EvidenceCheckItem(
        name="execution_economics",
        status="PASS",
        observed_value={
            "proposed_limit_price": proposed_limit_price,
            "invalidation_price": invalidation_price,
            "spread_bps": spread_bps,
            "depth_1pct_usd": depth_usd,
            "maker_fee_bps": maker_fee,
            "expected_slippage_bps": slippage,
        },
        source_status=DataStatus.VERIFIED.value,
        rationale=f"Limit {side} economics verified (spread {spread_bps} bps, depth ${depth_usd:,.0f}).",
        is_mandatory=True,
    )


def summarize_checklist(
    checklist: list[EvidenceCheckItem],
) -> tuple[list[str], list[str], list[str], list[str]]:
    """Split checklist items into qualifying, failed, unavailable, and unconfigured lists."""
    qualifying: list[str] = []
    failed: list[str] = []
    unavailable: list[str] = []
    unconfigured: list[str] = []

    for item in checklist:
        if item.status == "PASS":
            qualifying.append(f"{item.name}: {item.rationale}")
        elif item.status == "FAIL":
            failed.append(f"{item.name}: {item.rationale}")
        elif item.status == "UNAVAILABLE":
            unavailable.append(f"{item.name}: {item.rationale}")
        elif item.status == NOT_CONFIGURED:
            unconfigured.append(f"{item.name}: {item.rationale}")
    return qualifying, failed, unavailable, unconfigured
