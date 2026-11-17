"""
Module A — Bullish: Accumulation & Reversal (Phase 2).

Identifies qualified opportunities to convert USDT into BTC without
independent execution authority (has_execution_authority = False).
Never authorizes a buy solely on price drop, oversold RSI, or lower wicks.
"""

from __future__ import annotations

import uuid
from datetime import timedelta
from typing import Any

from btc_config_loader import get_param
from cortex_core.constants import NOT_CONFIGURED, DataStatus, ModuleState
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


def evaluate_module_a(
    snapshot: MarketSnapshot,
    config: ConfigurationRecord,
    *,
    evidence_inputs: dict[str, Any] | None = None,
    now_utc: str | None = None,
) -> ModuleAssessment:
    """
    Deterministically evaluate Module A (Bullish Accumulation & Reversal).

    Returns a non-authoritative ModuleAssessment with state and directional_signal
    ('BUY' | 'WAIT' | 'REJECTED').
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
    r_low, _ = field_info(snapshot, "range_low_45d")
    r_high, _ = field_info(snapshot, "range_high_45d")
    spot_cvd, spot_cvd_st = field_info(snapshot, "spot_cvd_24h_btc")
    perp_cvd, _ = field_info(snapshot, "perp_cvd_24h_btc")
    oi_chg, _ = field_info(snapshot, "oi_change_24h_pct")

    # 2. Higher-timeframe structure
    if spot_val is None or sma50 is None or sma200 is None:
        checklist.append(
            EvidenceCheckItem(
                name="higher_timeframe_structure",
                status="UNAVAILABLE",
                observed_value={"spot": spot_val, "sma50": sma50, "sma200": sma200},
                source_status=DataStatus.UNAVAILABLE.value,
                rationale="Spot or SMA50/SMA200 structural reference unavailable.",
                is_mandatory=True,
            )
        )
    else:
        above_200 = spot_val > sma200
        near_45d_support = r_low is not None and r_high is not None and r_high > r_low and ((spot_val - r_low) / (r_high - r_low)) <= 0.35
        htf_pass = bool(above_200 or near_45d_support)
        checklist.append(
            EvidenceCheckItem(
                name="higher_timeframe_structure",
                status="PASS" if htf_pass else "FAIL",
                observed_value={
                    "spot": spot_val,
                    "sma50": sma50,
                    "sma200": sma200,
                    "range_low_45d": r_low,
                    "range_high_45d": r_high,
                },
                source_status=DataStatus.VERIFIED.value,
                rationale=(
                    "Higher-timeframe structure supportive or testing verified 45D lower support zone."
                    if htf_pass
                    else "Spot below SMA50/SMA200 without lower-range structural support qualification."
                ),
                is_mandatory=True,
            )
        )

    # 3. Downside liquidity sweep / support test
    sweep_detected = ev.get("downside_sweep_detected")
    support_ref = ev.get("support_reference_usdt", r_low)
    if sweep_detected is None:
        checklist.append(
            EvidenceCheckItem(
                name="downside_sweep_or_support_test",
                status="UNAVAILABLE",
                observed_value={"downside_sweep_detected": None, "support_reference_usdt": support_ref},
                source_status=DataStatus.UNAVAILABLE.value,
                rationale="Intraday sweep/support-test telemetry is unavailable.",
                is_mandatory=True,
            )
        )
    else:
        checklist.append(
            EvidenceCheckItem(
                name="downside_sweep_or_support_test",
                status="PASS" if bool(sweep_detected) else "FAIL",
                observed_value={"downside_sweep_detected": bool(sweep_detected), "support_reference_usdt": support_ref},
                source_status=DataStatus.VERIFIED.value,
                rationale=(
                    f"Verified downside sweep / test near support reference {support_ref}."
                    if sweep_detected
                    else "No qualified downside liquidity sweep or support test observed."
                ),
                is_mandatory=True,
            )
        )

    # 4. Selling pressure exhaustion & demand absorption
    absorption = ev.get("absorption_detected")
    if absorption is None:
        checklist.append(
            EvidenceCheckItem(
                name="selling_exhaustion_and_absorption",
                status="UNAVAILABLE",
                observed_value={"absorption_detected": None},
                source_status=DataStatus.UNAVAILABLE.value,
                rationale="Order-flow absorption / bid replenishment telemetry unavailable.",
                is_mandatory=True,
            )
        )
    else:
        checklist.append(
            EvidenceCheckItem(
                name="selling_exhaustion_and_absorption",
                status="PASS" if bool(absorption) else "FAIL",
                observed_value={"absorption_detected": bool(absorption)},
                source_status=DataStatus.VERIFIED.value,
                rationale=(
                    "Selling pressure absorbed with diminishing downside displacement."
                    if absorption
                    else "Aggressive selling is still producing downward displacement (no absorption)."
                ),
                is_mandatory=True,
            )
        )

    # 5. Spot CVD stabilisation / improvement
    cvd_thresh = get_param(config, "buy_criteria.cvd_threshold_btc")
    if spot_cvd is None or spot_cvd_st == DataStatus.UNAVAILABLE:
        checklist.append(
            EvidenceCheckItem(
                name="spot_cvd_stabilisation",
                status="UNAVAILABLE",
                observed_value=None,
                source_status=DataStatus.UNAVAILABLE.value,
                rationale="Spot CVD telemetry unavailable.",
                is_mandatory=True,
            )
        )
    elif cvd_thresh == NOT_CONFIGURED:
        checklist.append(
            EvidenceCheckItem(
                name="spot_cvd_stabilisation",
                status=NOT_CONFIGURED,
                observed_value=spot_cvd,
                source_status=spot_cvd_st.value,
                rationale="buy_criteria.cvd_threshold_btc is NOT CONFIGURED.",
                is_mandatory=True,
            )
        )
    else:
        cvd_ok = float(spot_cvd) >= float(cvd_thresh)
        checklist.append(
            EvidenceCheckItem(
                name="spot_cvd_stabilisation",
                status="PASS" if cvd_ok else "FAIL",
                observed_value={"spot_cvd_24h_btc": spot_cvd, "threshold": float(cvd_thresh)},
                source_status=spot_cvd_st.value,
                rationale=(
                    f"Spot CVD ({spot_cvd:+.2f} BTC, {spot_cvd_st.value}) >= {float(cvd_thresh):+.2f} BTC."
                    if cvd_ok
                    else f"Spot CVD ({spot_cvd:+.2f} BTC, {spot_cvd_st.value}) remains below {float(cvd_thresh):+.2f} BTC."
                ),
                is_mandatory=True,
            )
        )

    # 6. Value-area / auction-boundary reclaim
    reclaim_rule = get_param(config, "buy_criteria.reclaim_rule")
    reclaim_confirmed = ev.get("reclaim_confirmed")
    if reclaim_confirmed is None:
        checklist.append(
            EvidenceCheckItem(
                name="auction_reclaim",
                status="UNAVAILABLE",
                observed_value={"reclaim_confirmed": None, "vah": ev.get("vah"), "val": ev.get("val")},
                source_status=DataStatus.UNAVAILABLE.value,
                rationale="Volume-profile / auction-boundary reclaim telemetry unavailable.",
                is_mandatory=True,
            )
        )
    elif reclaim_rule == NOT_CONFIGURED:
        checklist.append(
            EvidenceCheckItem(
                name="auction_reclaim",
                status=NOT_CONFIGURED,
                observed_value={"reclaim_confirmed": bool(reclaim_confirmed)},
                source_status=DataStatus.VERIFIED.value,
                rationale="buy_criteria.reclaim_rule is NOT CONFIGURED.",
                is_mandatory=True,
            )
        )
    else:
        rec_ok = bool(reclaim_confirmed)
        checklist.append(
            EvidenceCheckItem(
                name="auction_reclaim",
                status="PASS" if rec_ok else "FAIL",
                observed_value={"reclaim_confirmed": rec_ok, "rule": reclaim_rule},
                source_status=DataStatus.VERIFIED.value,
                rationale=(
                    f"Confirmed reclaim under rule '{reclaim_rule}'."
                    if rec_ok
                    else f"Auction boundary reclaim not yet confirmed under '{reclaim_rule}'."
                ),
                is_mandatory=True,
            )
        )

    # 7. Contextual derivatives (non-mandatory context only)
    checklist.append(
        EvidenceCheckItem(
            name="derivatives_context",
            status="CONTEXT" if (perp_cvd is not None or oi_chg is not None) else "UNAVAILABLE",
            observed_value={"perp_cvd_24h_btc": perp_cvd, "oi_change_24h_pct": oi_chg},
            source_status=DataStatus.VERIFIED.value if (perp_cvd is not None or oi_chg is not None) else DataStatus.UNAVAILABLE.value,
            rationale="Derivatives positioning recorded as corroborating context only.",
            is_mandatory=False,
        )
    )

    # 8. Anti-falling-knife guard: oversold RSI / sharp drop alone cannot authorize BUY
    status_by_name = {c.name: c.status for c in checklist}
    behavior_confirmed = (
        status_by_name.get("downside_sweep_or_support_test") == "PASS"
        and status_by_name.get("selling_exhaustion_and_absorption") == "PASS"
        and status_by_name.get("spot_cvd_stabilisation") == "PASS"
        and status_by_name.get("auction_reclaim") == "PASS"
    )
    checklist.append(
        EvidenceCheckItem(
            name="anti_falling_knife_guard",
            status="PASS" if behavior_confirmed else "FAIL",
            observed_value={"rsi14": rsi14, "behavior_confirmed": behavior_confirmed},
            source_status=DataStatus.VERIFIED.value if rsi14 is not None else DataStatus.UNAVAILABLE.value,
            rationale=(
                "Reversal behavior confirmed beyond price/RSI drop."
                if behavior_confirmed
                else "Price drop or oversold RSI alone cannot authorize BUY without sweep, absorption, spot CVD, and reclaim."
            ),
            is_mandatory=True,
        )
    )

    # 9. Execution economics (proposed limit-buy + invalidation reference)
    proposed_limit = ev.get("proposed_limit_buy_price")
    if proposed_limit is None and spot_val is not None:
        proposed_limit = float(spot_val)
    invalidation_px = ev.get("invalidation_price")
    exec_item = evaluate_execution_economics(
        snapshot,
        config,
        side="BUY",
        proposed_limit_price=proposed_limit,
        invalidation_price=invalidation_px,
    )
    checklist.append(exec_item)

    qualifying, failed, unavailable, unconfigured = summarize_checklist(checklist)
    mandatory_items = [c for c in checklist if c.is_mandatory]
    all_mandatory_pass = all(c.status == "PASS" for c in mandatory_items)

    # Setup expiry if configured
    expiry_min = get_param(config, "execution_assumptions.order_expiry_minutes")
    setup_expiry_utc: str | None = None
    if expiry_min not in (NOT_CONFIGURED, None):
        dt = parse_utc_timestamp(ts_iso)
        if dt is not None:
            setup_expiry_utc = (dt + timedelta(minutes=float(expiry_min))).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Determine ModuleState & directional_signal (without execution authority)
    if data_halted:
        state = ModuleState.DATA_HALT
        directional_signal = "WAIT"
    elif ev.get("setup_invalidated"):
        state = ModuleState.INVALIDATED
        directional_signal = "REJECTED"
    elif all_mandatory_pass:
        state = ModuleState.ELIGIBLE
        directional_signal = "BUY"
    elif status_by_name.get("downside_sweep_or_support_test") == "PASS" and (
        status_by_name.get("selling_exhaustion_and_absorption") == "PASS"
        or status_by_name.get("spot_cvd_stabilisation") == "PASS"
    ):
        state = ModuleState.SETUP
        directional_signal = "WAIT"
    else:
        state = ModuleState.WATCH
        directional_signal = "WAIT"

    return ModuleAssessment(
        assessment_id=f"MODA-{uuid.uuid4().hex[:12].upper()}",
        module_name="MODULE_A_ACCUMULATION",
        setup_id=str(ev.get("setup_id") or f"SETUP-A-{ts_iso[:10]}"),
        timestamp_utc=ts_iso,
        market_snapshot_id=snapshot.snapshot_id,
        config_version=config.config_version,
        state=state,
        directional_signal=directional_signal,
        has_execution_authority=False,
        exit_classification=None,
        bearish_pattern=None,
        checklist=checklist,
        qualifying_conditions=qualifying,
        failed_conditions=failed,
        unavailable_data=unavailable,
        unconfigured_thresholds=unconfigured,
        mechanism_evaluations={},
        proposed_limit_price=float(proposed_limit) if (all_mandatory_pass and proposed_limit is not None) else None,
        invalidation_price=float(invalidation_px) if invalidation_px is not None else None,
        setup_expiry_utc=setup_expiry_utc,
        observed_summary=f"Spot={spot_val}, SMA200={sma200}, RSI14={rsi14}, SpotCVD={spot_cvd} ({spot_cvd_st.value}).",
        interpretation_summary=f"Module A state={state.value}, signal={directional_signal} ({len(qualifying)} pass, {len(failed)} fail, {len(unavailable)} unavailable, {len(unconfigured)} unconfigured).",
    )
