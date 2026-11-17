"""
Module C — Portfolio Allocation Controller (Phase 3).

Determines current BTC/USDT holdings, tactical vs. protected core separation,
exposure band alignment, and deterministic BUY / SELL sizing using the most
restrictive applicable constraint:
  Permitted size = min(inventory, floor, sleeve/band, risk budget, max tx size).

Never invents unconfigured parameters and never appropriates protected core BTC.
"""

from __future__ import annotations

import math
import uuid
from typing import Any

from btc_config_loader import get_param
from cortex_core.constants import NOT_CONFIGURED, ExitClassification
from cortex_core.models import (
    AllocationAssessment,
    ConfigurationRecord,
    ConstraintLimit,
    ModuleAssessment,
    PortfolioSnapshot,
    SizingBreakdown,
)
from cortex_core.time_utils import ensure_utc_iso, utc_now


def _floor_btc(qty: float) -> float:
    return math.floor(max(0.0, qty) * 1e8) / 1e8


def _lookup_exposure_band(config: ConfigurationRecord, regime_label: str) -> tuple[dict[str, Any], float | None]:
    """Map regime label to configured exposure band without inventing weights."""
    mapping = {
        "DEFENSIVE": "defensive",
        "DISLOCATION / EXTREME RISK": "defensive",
        "CAUTIOUS": "cautious",
        "MIXED / CAUTIOUS": "cautious",
        "NEUTRAL": "neutral",
        "CONSTRUCTIVE": "constructive",
        "STRONGLY CONSTRUCTIVE": "strongly_constructive",
    }
    key = mapping.get(regime_label.upper().strip())
    if key is None:
        return {"btc_pct": NOT_CONFIGURED, "usdt_pct": NOT_CONFIGURED}, None

    band = get_param(config, f"exposure_bands.{key}")
    if not isinstance(band, dict):
        return {"btc_pct": NOT_CONFIGURED, "usdt_pct": NOT_CONFIGURED}, None
    btc_pct = band.get("btc_pct", NOT_CONFIGURED)
    usdt_pct = band.get("usdt_pct", NOT_CONFIGURED)
    if btc_pct in (NOT_CONFIGURED, None) or usdt_pct in (NOT_CONFIGURED, None):
        return {"btc_pct": NOT_CONFIGURED, "usdt_pct": NOT_CONFIGURED}, None
    return {"btc_pct": float(btc_pct), "usdt_pct": float(usdt_pct)}, float(btc_pct)


def calculate_buy_sizing(
    *,
    portfolio: PortfolioSnapshot,
    config: ConfigurationRecord,
    limit_price: float | None,
    invalidation_price: float | None,
    target_btc_pct: float | None,
) -> SizingBreakdown:
    """Calculate maximum permitted spot BTC purchase strictly constrained by lowest limit."""
    if not portfolio.configured or portfolio.usdt_tactical_available is None or portfolio.btc_tactical is None:
        return SizingBreakdown(
            side="BUY",
            proposed_limit_price=limit_price,
            permitted_qty_btc=0.0,
            gross_usdt=0.0,
            estimated_fee_usdt=0.0,
            estimated_slippage_usdt=0.0,
            net_usdt=0.0,
            remaining_available_btc=portfolio.btc_available,
            remaining_available_usdt=portfolio.usdt_available,
            resulting_btc_allocation_pct=portfolio.btc_exposure_pct,
            resulting_usdt_allocation_pct=portfolio.usdt_exposure_pct,
            invalidation_price=invalidation_price,
            distance_to_invalidation_pct=None,
            estimated_risk_at_invalidation_usdt=None,
            inventory_floor_compliant=False,
            core_btc_intact=True,
            limiting_constraint_name="PORTFOLIO_NOT_CONFIGURED",
            constraints_evaluated=[],
            sizing_status=NOT_CONFIGURED,
            rejection_reason="Portfolio balances are NOT CONFIGURED.",
        )

    maker_fee_bps = get_param(config, "execution_assumptions.maker_fee_bps")
    slippage_bps = get_param(config, "execution_assumptions.expected_slippage_bps")
    risk_budget_pct = get_param(config, "portfolio_policy.portfolio_risk_budget_pct")
    if maker_fee_bps == NOT_CONFIGURED or slippage_bps == NOT_CONFIGURED or risk_budget_pct == NOT_CONFIGURED:
        return SizingBreakdown(
            side="BUY",
            proposed_limit_price=limit_price,
            permitted_qty_btc=0.0,
            gross_usdt=0.0,
            estimated_fee_usdt=0.0,
            estimated_slippage_usdt=0.0,
            net_usdt=0.0,
            remaining_available_btc=portfolio.btc_available,
            remaining_available_usdt=portfolio.usdt_available,
            resulting_btc_allocation_pct=portfolio.btc_exposure_pct,
            resulting_usdt_allocation_pct=portfolio.usdt_exposure_pct,
            invalidation_price=invalidation_price,
            distance_to_invalidation_pct=None,
            estimated_risk_at_invalidation_usdt=None,
            inventory_floor_compliant=True,
            core_btc_intact=True,
            limiting_constraint_name="RISK_OR_FEE_POLICY_NOT_CONFIGURED",
            constraints_evaluated=[],
            sizing_status=NOT_CONFIGURED,
            rejection_reason="maker_fee_bps, expected_slippage_bps, or portfolio_risk_budget_pct is NOT CONFIGURED.",
        )

    if limit_price is None or limit_price <= 0 or invalidation_price is None or invalidation_price >= limit_price:
        return SizingBreakdown(
            side="BUY",
            proposed_limit_price=limit_price,
            permitted_qty_btc=0.0,
            gross_usdt=0.0,
            estimated_fee_usdt=0.0,
            estimated_slippage_usdt=0.0,
            net_usdt=0.0,
            remaining_available_btc=portfolio.btc_available,
            remaining_available_usdt=portfolio.usdt_available,
            resulting_btc_allocation_pct=portfolio.btc_exposure_pct,
            resulting_usdt_allocation_pct=portfolio.usdt_exposure_pct,
            invalidation_price=invalidation_price,
            distance_to_invalidation_pct=None,
            estimated_risk_at_invalidation_usdt=None,
            inventory_floor_compliant=True,
            core_btc_intact=True,
            limiting_constraint_name="INVALID_PRICE_OR_STOP",
            constraints_evaluated=[],
            sizing_status="REJECTED",
            rejection_reason="Valid limit_price and protective invalidation_price (< limit_price) are required.",
        )

    fee_rate = float(maker_fee_bps) / 10000.0
    slip_rate = float(slippage_bps) / 10000.0
    avail_usdt = float(portfolio.usdt_tactical_available)
    total_val = float(portfolio.total_portfolio_value_usdt or 0.0)
    sleeve_val = float(portfolio.active_sleeve_value_usdt or 0.0)

    constraints: list[ConstraintLimit] = []

    # 1. Available tactical USDT (including fee)
    max_by_usdt = _floor_btc(avail_usdt / (limit_price * (1.0 + fee_rate)))
    constraints.append(
        ConstraintLimit(
            name="available_tactical_usdt",
            max_qty_btc=max_by_usdt,
            max_notional_usdt=round(max_by_usdt * limit_price, 2),
            details=f"Available tactical USDT = {avail_usdt:.2f} (incl. {float(maker_fee_bps):.1f} bps fee).",
        )
    )

    # 2. Minimum USDT inventory floor
    min_usdt_floor = get_param(config, "portfolio_policy.min_usdt_inventory_floor")
    floor_compliant = True
    if min_usdt_floor not in (NOT_CONFIGURED, None):
        spendable = max(0.0, avail_usdt - float(min_usdt_floor))
        max_by_floor = _floor_btc(spendable / (limit_price * (1.0 + fee_rate)))
        constraints.append(
            ConstraintLimit(
                name="min_usdt_inventory_floor",
                max_qty_btc=max_by_floor,
                max_notional_usdt=round(max_by_floor * limit_price, 2),
                details=f"Retains >= {float(min_usdt_floor):.2f} USDT floor.",
            )
        )

    # 3. Active tactical sleeve cap / target BTC allocation band (applied to sleeve)
    if target_btc_pct is not None and sleeve_val > 0:
        cur_tac_btc_val = float(portfolio.btc_tactical) * limit_price
        target_tac_btc_val = sleeve_val * (target_btc_pct / 100.0)
        headroom_usdt = max(0.0, target_tac_btc_val - cur_tac_btc_val)
        max_by_band = _floor_btc(headroom_usdt / limit_price)
        constraints.append(
            ConstraintLimit(
                name="target_exposure_band",
                max_qty_btc=max_by_band,
                max_notional_usdt=round(max_by_band * limit_price, 2),
                details=f"Caps tactical sleeve BTC exposure at {target_btc_pct:.1f}%.",
            )
        )

    # 4. Portfolio risk budget at invalidation reference
    stop_dist = limit_price - invalidation_price
    dist_pct = (stop_dist / limit_price) * 100.0
    if total_val > 0:
        max_risk_usdt = total_val * (float(risk_budget_pct) / 100.0)
        risk_per_btc = stop_dist + limit_price * (fee_rate + slip_rate)
        max_by_risk = _floor_btc(max_risk_usdt / risk_per_btc) if risk_per_btc > 0 else 0.0
        constraints.append(
            ConstraintLimit(
                name="portfolio_risk_budget",
                max_qty_btc=max_by_risk,
                max_notional_usdt=round(max_by_risk * limit_price, 2),
                details=f"Risk <= {float(risk_budget_pct):.3f}% equity (${max_risk_usdt:.2f}) at invalidation {invalidation_price:.2f}.",
            )
        )

    # 5. Max single transaction size
    max_tx_usdt = get_param(config, "portfolio_policy.max_transaction_size_usdt")
    if max_tx_usdt not in (NOT_CONFIGURED, None):
        max_by_tx_u = _floor_btc(float(max_tx_usdt) / limit_price)
        constraints.append(
            ConstraintLimit(
                name="max_transaction_size_usdt",
                max_qty_btc=max_by_tx_u,
                max_notional_usdt=round(max_by_tx_u * limit_price, 2),
                details=f"Single order notional cap ${float(max_tx_usdt):,.2f}.",
            )
        )
    max_tx_btc = get_param(config, "portfolio_policy.max_transaction_size_btc")
    if max_tx_btc not in (NOT_CONFIGURED, None):
        max_by_tx_b = _floor_btc(float(max_tx_btc))
        constraints.append(
            ConstraintLimit(
                name="max_transaction_size_btc",
                max_qty_btc=max_by_tx_b,
                max_notional_usdt=round(max_by_tx_b * limit_price, 2),
                details=f"Single order BTC cap {float(max_tx_btc):.6f} BTC.",
            )
        )

    limiting = min(constraints, key=lambda c: c.max_qty_btc)
    qty = limiting.max_qty_btc
    gross = round(qty * limit_price, 6)
    fee_usdt = round(gross * fee_rate, 6)
    slip_usdt = round(gross * slip_rate, 6)
    total_cost = round(gross + fee_usdt, 6)
    rem_usdt = round(max(0.0, avail_usdt - total_cost), 6)
    if min_usdt_floor not in (NOT_CONFIGURED, None) and rem_usdt + 1e-6 < float(min_usdt_floor):
        floor_compliant = False

    new_btc_total = float(portfolio.btc_total or 0.0) + qty
    new_usdt_total = max(0.0, float(portfolio.usdt_total or 0.0) - total_cost)
    new_total_val = new_btc_total * limit_price + new_usdt_total
    res_btc_pct = round((new_btc_total * limit_price / new_total_val) * 100.0, 2) if new_total_val > 0 else None
    res_usdt_pct = round((new_usdt_total / new_total_val) * 100.0, 2) if new_total_val > 0 else None
    est_risk_usdt = round(qty * (stop_dist + limit_price * (fee_rate + slip_rate)), 2)

    status = "ELIGIBLE" if (qty > 0 and floor_compliant) else "REJECTED"
    reason = "" if status == "ELIGIBLE" else f"Permitted BUY quantity is zero due to {limiting.name}."

    return SizingBreakdown(
        side="BUY",
        proposed_limit_price=limit_price,
        permitted_qty_btc=qty,
        gross_usdt=gross,
        estimated_fee_usdt=fee_usdt,
        estimated_slippage_usdt=slip_usdt,
        net_usdt=total_cost,
        remaining_available_btc=portfolio.btc_available,
        remaining_available_usdt=rem_usdt,
        resulting_btc_allocation_pct=res_btc_pct,
        resulting_usdt_allocation_pct=res_usdt_pct,
        invalidation_price=invalidation_price,
        distance_to_invalidation_pct=round(dist_pct, 3),
        estimated_risk_at_invalidation_usdt=est_risk_usdt,
        inventory_floor_compliant=floor_compliant,
        core_btc_intact=True,
        limiting_constraint_name=limiting.name,
        constraints_evaluated=constraints,
        sizing_status=status,
        rejection_reason=reason,
    )


def calculate_sell_sizing(
    *,
    portfolio: PortfolioSnapshot,
    config: ConfigurationRecord,
    limit_price: float | None,
    exit_classification: ExitClassification | None,
) -> SizingBreakdown:
    """
    Calculate maximum permitted tactical BTC sale strictly constrained by lowest limit.
    Never exceeds available tactical BTC and never touches protected core BTC.
    """
    if not portfolio.configured or portfolio.btc_tactical_available is None or portfolio.usdt_tactical is None:
        return SizingBreakdown(
            side="SELL",
            proposed_limit_price=limit_price,
            permitted_qty_btc=0.0,
            gross_usdt=0.0,
            estimated_fee_usdt=0.0,
            estimated_slippage_usdt=0.0,
            net_usdt=0.0,
            remaining_available_btc=portfolio.btc_available,
            remaining_available_usdt=portfolio.usdt_available,
            resulting_btc_allocation_pct=portfolio.btc_exposure_pct,
            resulting_usdt_allocation_pct=portfolio.usdt_exposure_pct,
            invalidation_price=None,
            distance_to_invalidation_pct=None,
            estimated_risk_at_invalidation_usdt=None,
            inventory_floor_compliant=False,
            core_btc_intact=True,
            limiting_constraint_name="PORTFOLIO_NOT_CONFIGURED",
            constraints_evaluated=[],
            sizing_status=NOT_CONFIGURED,
            rejection_reason="Portfolio balances are NOT CONFIGURED.",
        )

    maker_fee_bps = get_param(config, "execution_assumptions.maker_fee_bps")
    slippage_bps = get_param(config, "execution_assumptions.expected_slippage_bps")
    if maker_fee_bps == NOT_CONFIGURED or slippage_bps == NOT_CONFIGURED:
        return SizingBreakdown(
            side="SELL",
            proposed_limit_price=limit_price,
            permitted_qty_btc=0.0,
            gross_usdt=0.0,
            estimated_fee_usdt=0.0,
            estimated_slippage_usdt=0.0,
            net_usdt=0.0,
            remaining_available_btc=portfolio.btc_available,
            remaining_available_usdt=portfolio.usdt_available,
            resulting_btc_allocation_pct=portfolio.btc_exposure_pct,
            resulting_usdt_allocation_pct=portfolio.usdt_exposure_pct,
            invalidation_price=None,
            distance_to_invalidation_pct=None,
            estimated_risk_at_invalidation_usdt=None,
            inventory_floor_compliant=True,
            core_btc_intact=True,
            limiting_constraint_name="FEE_POLICY_NOT_CONFIGURED",
            constraints_evaluated=[],
            sizing_status=NOT_CONFIGURED,
            rejection_reason="maker_fee_bps or expected_slippage_bps is NOT CONFIGURED.",
        )

    if limit_price is None or limit_price <= 0 or exit_classification is None:
        return SizingBreakdown(
            side="SELL",
            proposed_limit_price=limit_price,
            permitted_qty_btc=0.0,
            gross_usdt=0.0,
            estimated_fee_usdt=0.0,
            estimated_slippage_usdt=0.0,
            net_usdt=0.0,
            remaining_available_btc=portfolio.btc_available,
            remaining_available_usdt=portfolio.usdt_available,
            resulting_btc_allocation_pct=portfolio.btc_exposure_pct,
            resulting_usdt_allocation_pct=portfolio.usdt_exposure_pct,
            invalidation_price=None,
            distance_to_invalidation_pct=None,
            estimated_risk_at_invalidation_usdt=None,
            inventory_floor_compliant=True,
            core_btc_intact=True,
            limiting_constraint_name="NO_QUALIFIED_EXIT",
            constraints_evaluated=[],
            sizing_status="REJECTED",
            rejection_reason="Valid limit_price and exit_classification are required for SELL sizing.",
        )

    fee_rate = float(maker_fee_bps) / 10000.0
    slip_rate = float(slippage_bps) / 10000.0
    avail_tac_btc = float(portfolio.btc_tactical_available)
    constraints: list[ConstraintLimit] = [
        ConstraintLimit(
            name="available_tactical_btc",
            max_qty_btc=_floor_btc(avail_tac_btc),
            max_notional_usdt=round(avail_tac_btc * limit_price, 2),
            details=f"Tactical BTC available = {avail_tac_btc:.8f} BTC (core {float(portfolio.btc_core_protected or 0.0):.8f} BTC protected).",
        )
    ]

    # Minimum BTC floor (applied within tactical sleeve)
    min_btc_floor = get_param(config, "portfolio_policy.min_btc_inventory_floor")
    if min_btc_floor not in (NOT_CONFIGURED, None):
        sellable_above_floor = _floor_btc(max(0.0, avail_tac_btc - float(min_btc_floor)))
        constraints.append(
            ConstraintLimit(
                name="min_btc_inventory_floor",
                max_qty_btc=sellable_above_floor,
                max_notional_usdt=round(sellable_above_floor * limit_price, 2),
                details=f"Retains >= {float(min_btc_floor):.6f} BTC tactical floor.",
            )
        )

    # Exit mechanism trim limit
    if exit_classification == ExitClassification.PROFIT_TAKING:
        trim_pct = (get_param(config, "sell_criteria.profit_taking") or {}).get("trim_pct", NOT_CONFIGURED)
        if trim_pct in (NOT_CONFIGURED, None):
            return SizingBreakdown(
                side="SELL",
                proposed_limit_price=limit_price,
                permitted_qty_btc=0.0,
                gross_usdt=0.0,
                estimated_fee_usdt=0.0,
                estimated_slippage_usdt=0.0,
                net_usdt=0.0,
                remaining_available_btc=portfolio.btc_available,
                remaining_available_usdt=portfolio.usdt_available,
                resulting_btc_allocation_pct=portfolio.btc_exposure_pct,
                resulting_usdt_allocation_pct=portfolio.usdt_exposure_pct,
                invalidation_price=None,
                distance_to_invalidation_pct=None,
                estimated_risk_at_invalidation_usdt=None,
                inventory_floor_compliant=True,
                core_btc_intact=True,
                limiting_constraint_name="PROFIT_TAKING_TRIM_NOT_CONFIGURED",
                constraints_evaluated=constraints,
                sizing_status=NOT_CONFIGURED,
                rejection_reason="sell_criteria.profit_taking.trim_pct is NOT CONFIGURED.",
            )
        mech_cap = _floor_btc(avail_tac_btc * (float(trim_pct) / 100.0))
        constraints.append(
            ConstraintLimit(
                name="profit_taking_trim_cap",
                max_qty_btc=mech_cap,
                max_notional_usdt=round(mech_cap * limit_price, 2),
                details=f"Profit-taking trims up to {float(trim_pct):.1f}% of tactical BTC.",
            )
        )
    elif exit_classification == ExitClassification.RISK_REDUCTION:
        trim_pct = (get_param(config, "sell_criteria.risk_reduction") or {}).get("trim_pct", NOT_CONFIGURED)
        if trim_pct in (NOT_CONFIGURED, None):
            return SizingBreakdown(
                side="SELL",
                proposed_limit_price=limit_price,
                permitted_qty_btc=0.0,
                gross_usdt=0.0,
                estimated_fee_usdt=0.0,
                estimated_slippage_usdt=0.0,
                net_usdt=0.0,
                remaining_available_btc=portfolio.btc_available,
                remaining_available_usdt=portfolio.usdt_available,
                resulting_btc_allocation_pct=portfolio.btc_exposure_pct,
                resulting_usdt_allocation_pct=portfolio.usdt_exposure_pct,
                invalidation_price=None,
                distance_to_invalidation_pct=None,
                estimated_risk_at_invalidation_usdt=None,
                inventory_floor_compliant=True,
                core_btc_intact=True,
                limiting_constraint_name="RISK_REDUCTION_TRIM_NOT_CONFIGURED",
                constraints_evaluated=constraints,
                sizing_status=NOT_CONFIGURED,
                rejection_reason="sell_criteria.risk_reduction.trim_pct is NOT CONFIGURED.",
            )
        mech_cap = _floor_btc(avail_tac_btc * (float(trim_pct) / 100.0))
        constraints.append(
            ConstraintLimit(
                name="risk_reduction_trim_cap",
                max_qty_btc=mech_cap,
                max_notional_usdt=round(mech_cap * limit_price, 2),
                details=f"Risk reduction trims up to {float(trim_pct):.1f}% of tactical BTC.",
            )
        )
    else:
        # DEFENSIVE EXIT permits up to 100% of available tactical BTC (subject to floor; core untouched)
        constraints.append(
            ConstraintLimit(
                name="defensive_exit_tactical_cap",
                max_qty_btc=_floor_btc(avail_tac_btc),
                max_notional_usdt=round(avail_tac_btc * limit_price, 2),
                details="Defensive exit permits up to 100% of available tactical BTC (core BTC remains protected).",
            )
        )

    max_tx_usdt = get_param(config, "portfolio_policy.max_transaction_size_usdt")
    if max_tx_usdt not in (NOT_CONFIGURED, None):
        max_by_tx_u = _floor_btc(float(max_tx_usdt) / limit_price)
        constraints.append(
            ConstraintLimit(
                name="max_transaction_size_usdt",
                max_qty_btc=max_by_tx_u,
                max_notional_usdt=round(max_by_tx_u * limit_price, 2),
                details=f"Single order notional cap ${float(max_tx_usdt):,.2f}.",
            )
        )
    max_tx_btc = get_param(config, "portfolio_policy.max_transaction_size_btc")
    if max_tx_btc not in (NOT_CONFIGURED, None):
        max_by_tx_b = _floor_btc(float(max_tx_btc))
        constraints.append(
            ConstraintLimit(
                name="max_transaction_size_btc",
                max_qty_btc=max_by_tx_b,
                max_notional_usdt=round(max_by_tx_b * limit_price, 2),
                details=f"Single order BTC cap {float(max_tx_btc):.6f} BTC.",
            )
        )

    limiting = min(constraints, key=lambda c: c.max_qty_btc)
    qty = limiting.max_qty_btc
    gross = round(qty * limit_price, 2)
    fee_usdt = round(gross * fee_rate, 4)
    slip_usdt = round(gross * slip_rate, 4)
    net_proceeds = round(max(0.0, gross - fee_usdt), 4)
    rem_tac_btc = round(max(0.0, avail_tac_btc - qty), 8)
    floor_compliant = True
    if min_btc_floor not in (NOT_CONFIGURED, None) and rem_tac_btc < float(min_btc_floor):
        floor_compliant = False

    new_btc_total = max(0.0, float(portfolio.btc_total or 0.0) - qty)
    new_usdt_total = float(portfolio.usdt_total or 0.0) + net_proceeds
    new_total_val = new_btc_total * limit_price + new_usdt_total
    res_btc_pct = round((new_btc_total * limit_price / new_total_val) * 100.0, 2) if new_total_val > 0 else None
    res_usdt_pct = round((new_usdt_total / new_total_val) * 100.0, 2) if new_total_val > 0 else None

    status = "ELIGIBLE" if (qty > 0 and floor_compliant) else "REJECTED"
    reason = "" if status == "ELIGIBLE" else f"Permitted SELL quantity is zero due to {limiting.name}."

    return SizingBreakdown(
        side="SELL",
        proposed_limit_price=limit_price,
        permitted_qty_btc=qty,
        gross_usdt=gross,
        estimated_fee_usdt=fee_usdt,
        estimated_slippage_usdt=slip_usdt,
        net_usdt=net_proceeds,
        remaining_available_btc=rem_tac_btc,
        remaining_available_usdt=portfolio.usdt_available,
        resulting_btc_allocation_pct=res_btc_pct,
        resulting_usdt_allocation_pct=res_usdt_pct,
        invalidation_price=None,
        distance_to_invalidation_pct=None,
        estimated_risk_at_invalidation_usdt=None,
        inventory_floor_compliant=floor_compliant,
        core_btc_intact=True,
        limiting_constraint_name=limiting.name,
        constraints_evaluated=constraints,
        sizing_status=status,
        rejection_reason=reason,
    )


def evaluate_allocation_controller(
    *,
    portfolio: PortfolioSnapshot,
    config: ConfigurationRecord,
    regime_label: str,
    module_a: ModuleAssessment,
    module_b: ModuleAssessment,
    preferred_side: str | None = None,
    now_utc: str | None = None,
) -> AllocationAssessment:
    """
    Evaluate Module C (Portfolio Allocation Controller).

    Calculates current vs. permitted tactical exposure, evaluates BUY and/or SELL
    sizing independently, and reports the single limiting constraint.
    """
    ts_iso = ensure_utc_iso(now_utc or portfolio.timestamp_utc or utc_now(), field_name="now_utc")
    band, target_btc_pct = _lookup_exposure_band(config, regime_label)

    notes: list[str] = []
    spot = portfolio.valuation_spot_price
    current_tac_btc_pct: float | None = None
    delta_pct: float | None = None
    est_qty_to_target: float | None = None

    if (
        portfolio.configured
        and spot is not None
        and spot > 0
        and portfolio.active_sleeve_value_usdt is not None
        and portfolio.active_sleeve_value_usdt > 0
        and portfolio.btc_tactical is not None
    ):
        tac_btc_val = float(portfolio.btc_tactical) * spot
        current_tac_btc_pct = round((tac_btc_val / float(portfolio.active_sleeve_value_usdt)) * 100.0, 2)
        if target_btc_pct is not None:
            delta_pct = round(target_btc_pct - current_tac_btc_pct, 2)
            target_val = float(portfolio.active_sleeve_value_usdt) * (target_btc_pct / 100.0)
            est_qty_to_target = round((target_val - tac_btc_val) / spot, 6)
    else:
        notes.append("Tactical exposure delta unavailable (portfolio unconfigured or spot missing).")

    buy_sizing: SizingBreakdown | None = None
    sell_sizing: SizingBreakdown | None = None

    if module_a.directional_signal == "BUY" or preferred_side == "BUY":
        buy_sizing = calculate_buy_sizing(
            portfolio=portfolio,
            config=config,
            limit_price=module_a.proposed_limit_price or spot,
            invalidation_price=module_a.invalidation_price,
            target_btc_pct=target_btc_pct,
        )

    if module_b.directional_signal in {"SELL", "REDUCE"} or preferred_side == "SELL":
        sell_sizing = calculate_sell_sizing(
            portfolio=portfolio,
            config=config,
            limit_price=module_b.proposed_limit_price or spot,
            exit_classification=module_b.exit_classification,
        )

    permitted_side = "NONE"
    permitted_qty = 0.0
    limiting_name = "NO_PROPOSED_TRANSACTION"
    sizing_status = "HOLD"

    if preferred_side == "BUY" and buy_sizing is not None:
        if buy_sizing.sizing_status == "ELIGIBLE":
            permitted_side = "BUY"
            permitted_qty = buy_sizing.permitted_qty_btc
        limiting_name = buy_sizing.limiting_constraint_name
        sizing_status = buy_sizing.sizing_status
    elif preferred_side == "SELL" and sell_sizing is not None:
        if sell_sizing.sizing_status == "ELIGIBLE":
            permitted_side = "SELL"
            permitted_qty = sell_sizing.permitted_qty_btc
        limiting_name = sell_sizing.limiting_constraint_name
        sizing_status = sell_sizing.sizing_status
    elif buy_sizing is not None and sell_sizing is None:
        if buy_sizing.sizing_status == "ELIGIBLE":
            permitted_side = "BUY"
            permitted_qty = buy_sizing.permitted_qty_btc
        limiting_name = buy_sizing.limiting_constraint_name
        sizing_status = buy_sizing.sizing_status
    elif sell_sizing is not None and buy_sizing is None:
        if sell_sizing.sizing_status == "ELIGIBLE":
            permitted_side = "SELL"
            permitted_qty = sell_sizing.permitted_qty_btc
        limiting_name = sell_sizing.limiting_constraint_name
        sizing_status = sell_sizing.sizing_status

    min_btc_floor = get_param(config, "portfolio_policy.min_btc_inventory_floor")
    min_usdt_floor = get_param(config, "portfolio_policy.min_usdt_inventory_floor")
    btc_floor_ok = True
    usdt_floor_ok = True
    if portfolio.configured and portfolio.btc_tactical_available is not None and min_btc_floor not in (NOT_CONFIGURED, None):
        btc_floor_ok = float(portfolio.btc_tactical_available) >= float(min_btc_floor)
    if portfolio.configured and portfolio.usdt_tactical_available is not None and min_usdt_floor not in (NOT_CONFIGURED, None):
        usdt_floor_ok = float(portfolio.usdt_tactical_available) >= float(min_usdt_floor)

    return AllocationAssessment(
        allocation_id=f"MODC-{uuid.uuid4().hex[:12].upper()}",
        timestamp_utc=ts_iso,
        portfolio_snapshot_id=portfolio.portfolio_snapshot_id,
        config_version=config.config_version,
        regime_label=regime_label,
        current_btc_pct=portfolio.btc_exposure_pct,
        current_usdt_pct=portfolio.usdt_exposure_pct,
        permitted_exposure_band=band,
        proposed_target_btc_pct=target_btc_pct,
        exposure_delta_pct=delta_pct,
        estimated_qty_to_target_btc=est_qty_to_target,
        btc_floor_compliant=btc_floor_ok,
        usdt_floor_compliant=usdt_floor_ok,
        core_btc_intact=True,
        buy_sizing=buy_sizing,
        sell_sizing=sell_sizing,
        permitted_side=permitted_side,
        permitted_quantity_btc=permitted_qty,
        limiting_constraint_name=limiting_name,
        sizing_status=sizing_status,
        notes=notes,
    )
