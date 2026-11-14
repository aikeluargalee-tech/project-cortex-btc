#!/usr/bin/env python3
"""
Project CORTEX-BTC (v3.0) — Deterministic 6-Step Matrix Compiler.

Pipeline:
  MOD 36: Telemetry Trust, 90-min SLA & 3-Venue Quorum Gate
  MOD 31: ICDM 0-100 Fragility Scorer (50% penalty on missing fields)
  MOD 33: 5-Regime Master Radar
  MOD 30: PCF3 Configs A-J Router
  MOD 37: Executable Liquidity, Post-Cost Net R >= 3.0, Heat <= 0.75%,
          and -1.50% Daily / -3.00% Weekly Loss Locks
  MOD 18: 1.0x Unleveraged Spot BTC Position Sizer
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import statistics
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

from cortex_schema_adapter import adapt_telemetry, parse_utc_timestamp

ENGINE_VERSION = "CORTEX-BTC v3.0"
DEFAULT_INPUT_PATH = Path("btc_metrics_latest.json")
DEFAULT_OUTPUT_PATH = Path("cortex_verdict_latest.json")
DEFAULT_PORTFOLIO_PATH = Path("cortex_portfolio_state.json")

SLA_MAX_MINUTES = 90.0
MIN_VENUE_QUORUM = 3
MAX_DISPERSION_WARN_BPS = 150.0
MAX_DISPERSION_HARD_BPS = 500.0
MISSING_FIELD_PENALTY_SCORE = 50.0  # 50% fragility penalty for missing telemetry

MIN_NET_R = 3.0
MAX_PORTFOLIO_HEAT_PCT = 0.75
DAILY_LOSS_LOCK_PCT = -1.50
WEEKLY_LOSS_LOCK_PCT = -3.00
SPOT_FEE_ROUNDTRIP_BPS = 20.0
MAX_SPREAD_BPS = 25.0
MIN_DEPTH_1PCT_USD = 250_000.0
DEFAULT_EQUITY_USD = 10_000.0


def _myt_tz() -> timezone | ZoneInfo:
    try:
        return ZoneInfo("Asia/Kuala_Lumpur")
    except Exception:
        return timezone(timedelta(hours=8), name="MYT")


def _clamp(val: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, val))


def _round_opt(val: float | None, digits: int = 2) -> float | None:
    return round(val, digits) if val is not None else None


# ---------------------------------------------------------------------------
# MOD 36: Telemetry Trust & 90-min SLA / 3-Venue Quorum Gate
# ---------------------------------------------------------------------------

def run_mod36_trust_gate(canonical: dict[str, Any], now_utc: datetime) -> dict[str, Any]:
    reasons: list[str] = []
    ts_dt = parse_utc_timestamp(canonical.get("timestamp_utc"))

    sla_age_min: float | None = None
    sla_passed = False
    if ts_dt is None:
        reasons.append("MISSING_TIMESTAMP")
    else:
        sla_age_min = (now_utc - ts_dt).total_seconds() / 60.0
        if sla_age_min < -5.0:
            reasons.append(f"FUTURE_TIMESTAMP_SKEW({sla_age_min:.1f}m)")
        elif sla_age_min > SLA_MAX_MINUTES:
            reasons.append(f"SLA_EXPIRED({sla_age_min:.1f}m>{SLA_MAX_MINUTES:.0f}m)")
        else:
            sla_passed = True

    venue_prices: dict[str, float] = {
        k: float(v)
        for k, v in (canonical.get("venue_prices") or {}).items()
        if isinstance(v, (int, float)) and v > 0
    }
    quorum_count = len(venue_prices)
    quorum_passed = quorum_count >= MIN_VENUE_QUORUM
    if not quorum_passed:
        reasons.append(f"QUORUM_FAIL({quorum_count}<{MIN_VENUE_QUORUM})")

    median_spot: float | None = None
    dispersion_bps: float | None = None
    dispersion_passed = True
    if venue_prices:
        prices = sorted(venue_prices.values())
        median_spot = statistics.median(prices)
        if median_spot > 0:
            max_dev = max(abs(px - median_spot) / median_spot for px in prices)
            dispersion_bps = round(max_dev * 10000.0, 2)
            if dispersion_bps > MAX_DISPERSION_HARD_BPS:
                dispersion_passed = False
                reasons.append(f"DISPERSION_HALT({dispersion_bps:.1f}bps>{MAX_DISPERSION_HARD_BPS:.0f}bps)")
            elif dispersion_bps > MAX_DISPERSION_WARN_BPS:
                reasons.append(f"DISPERSION_WARN({dispersion_bps:.1f}bps>{MAX_DISPERSION_WARN_BPS:.0f}bps)")
    else:
        median_spot = canonical.get("spot_price")
        if median_spot is None:
            dispersion_passed = False
            reasons.append("NO_SPOT_PRICE")

    trust_passed = sla_passed and quorum_passed and dispersion_passed and (median_spot is not None)
    if trust_passed:
        trust_status = "DEGRADED" if reasons else "TRUSTED"
    else:
        trust_status = "HALT_UNTRUSTED"

    return {
        "module": "MOD 36",
        "trust_passed": trust_passed,
        "trust_status": trust_status,
        "sla_max_min": SLA_MAX_MINUTES,
        "sla_age_min": round(sla_age_min, 2) if sla_age_min is not None else None,
        "sla_passed": sla_passed,
        "min_quorum": MIN_VENUE_QUORUM,
        "quorum_count": quorum_count,
        "quorum_passed": quorum_passed,
        "active_venues": sorted(venue_prices.keys()),
        "venue_prices": venue_prices,
        "median_spot_usd": round(median_spot, 2) if median_spot is not None else None,
        "dispersion_bps": dispersion_bps,
        "gate_reasons": reasons,
    }


# ---------------------------------------------------------------------------
# MOD 31: ICDM 0-100 Fragility Scorer (50% penalty on missing fields)
# ---------------------------------------------------------------------------

def _score_volatility_stress(c: dict[str, Any]) -> tuple[dict[str, float], list[str]]:
    scores: dict[str, float] = {}
    missing: list[str] = []

    atr_pct = c.get("atr_pct")
    if atr_pct is None:
        scores["atr_pct"] = MISSING_FIELD_PENALTY_SCORE
        missing.append("atr_pct")
    else:
        # 1.5% daily ATR = low (15), >= 6.5% = extreme (95)
        scores["atr_pct"] = _clamp((atr_pct - 1.0) / 5.5 * 85.0 + 10.0)

    rvol = c.get("realized_vol_7d_pct")
    if rvol is None:
        scores["realized_vol_7d_pct"] = MISSING_FIELD_PENALTY_SCORE
        missing.append("realized_vol_7d_pct")
    else:
        # 25% annualized = calm (15), 110%+ = crisis (95)
        scores["realized_vol_7d_pct"] = _clamp((rvol - 20.0) / 90.0 * 85.0 + 10.0)

    rsi = c.get("rsi14")
    if rsi is None:
        scores["rsi14"] = MISSING_FIELD_PENALTY_SCORE
        missing.append("rsi14")
    else:
        # Neutral around 52 -> low fragility; extreme oversold (<25) or blow-off (>80) -> high fragility
        dist = abs(rsi - 52.0)
        scores["rsi14"] = _clamp((dist / 35.0) * 85.0)

    return scores, missing


def _score_derivatives_stress(c: dict[str, Any]) -> tuple[dict[str, float], list[str]]:
    scores: dict[str, float] = {}
    missing: list[str] = []

    fr = c.get("funding_rate_pct")
    if fr is None:
        scores["funding_rate_pct"] = MISSING_FIELD_PENALTY_SCORE
        missing.append("funding_rate_pct")
    else:
        # 0.01% per 8h is baseline; >= 0.06% or <= -0.04% signals crowded positioning
        mag = abs(fr - 0.005)
        scores["funding_rate_pct"] = _clamp((mag / 0.06) * 90.0)

    oi_chg = c.get("oi_change_24h_pct")
    if oi_chg is None:
        scores["oi_change_24h_pct"] = MISSING_FIELD_PENALTY_SCORE
        missing.append("oi_change_24h_pct")
    else:
        # Rapid 24h OI expansion or deleveraging (>12% abs move) raises fragility
        scores["oi_change_24h_pct"] = _clamp((abs(oi_chg) / 15.0) * 85.0)

    lsr = c.get("long_short_ratio")
    if lsr is None:
        scores["long_short_ratio"] = MISSING_FIELD_PENALTY_SCORE
        missing.append("long_short_ratio")
    else:
        # Balanced ~1.0-1.4; extreme crowding >2.5 or <0.65 raises fragility
        skew = abs(lsr - 1.2)
        scores["long_short_ratio"] = _clamp((skew / 1.5) * 85.0)

    return scores, missing


def _score_liquidity_flow_stress(c: dict[str, Any]) -> tuple[dict[str, float], list[str]]:
    scores: dict[str, float] = {}
    missing: list[str] = []

    spread = c.get("spread_bps")
    if spread is None:
        scores["spread_bps"] = MISSING_FIELD_PENALTY_SCORE
        missing.append("spread_bps")
    else:
        # <1 bps = 5, >= 20 bps = 95
        scores["spread_bps"] = _clamp((spread / 20.0) * 90.0 + 5.0)

    depth = c.get("depth_1pct_usd")
    if depth is None:
        scores["depth_1pct_usd"] = MISSING_FIELD_PENALTY_SCORE
        missing.append("depth_1pct_usd")
    else:
        # >= $10M 1% depth = low stress (10); <= $500k = high fragility (90)
        if depth >= 10_000_000:
            scores["depth_1pct_usd"] = 10.0
        else:
            scores["depth_1pct_usd"] = _clamp(90.0 - (depth / 10_000_000.0) * 80.0)

    spot_cvd = c.get("spot_cvd_24h_btc")
    perp_cvd = c.get("perp_cvd_24h_btc")
    if spot_cvd is None:
        scores["spot_cvd_24h_btc"] = MISSING_FIELD_PENALTY_SCORE
        missing.append("spot_cvd_24h_btc")
    else:
        # Heavy spot selling (<-5000 BTC) elevates fragility
        scores["spot_cvd_24h_btc"] = _clamp(35.0 - (spot_cvd / 4000.0) * 30.0)

    if perp_cvd is None:
        scores["perp_cvd_24h_btc"] = MISSING_FIELD_PENALTY_SCORE
        missing.append("perp_cvd_24h_btc")
    else:
        scores["perp_cvd_24h_btc"] = _clamp(35.0 - (perp_cvd / 5000.0) * 25.0)

    return scores, missing


def _score_macro_onchain_stress(c: dict[str, Any]) -> tuple[dict[str, float], list[str]]:
    scores: dict[str, float] = {}
    missing: list[str] = []

    vix = c.get("vix")
    if vix is None:
        scores["vix"] = MISSING_FIELD_PENALTY_SCORE
        missing.append("vix")
    else:
        # VIX 13 = calm (10); VIX 35 = crisis (95)
        scores["vix"] = _clamp((vix - 12.0) / 23.0 * 85.0 + 10.0)

    ry = c.get("us10y_real_yield_pct")
    if ry is None:
        scores["us10y_real_yield_pct"] = MISSING_FIELD_PENALTY_SCORE
        missing.append("us10y_real_yield_pct")
    else:
        # Real yield <= 1.0% = easy (15); >= 2.6% = tight (85)
        scores["us10y_real_yield_pct"] = _clamp((ry - 0.8) / 1.8 * 75.0 + 10.0)

    dxy = c.get("dxy")
    if dxy is None:
        scores["dxy"] = MISSING_FIELD_PENALTY_SCORE
        missing.append("dxy")
    else:
        # Broad USD index (DTWEXBGS ~115-132) or DXY (~95-110): handle both scales cleanly
        if dxy >= 112.0:
            scores["dxy"] = _clamp((dxy - 115.0) / 18.0 * 70.0 + 20.0)
        else:
            scores["dxy"] = _clamp((dxy - 97.0) / 13.0 * 70.0 + 20.0)

    fee = c.get("mempool_fastest_fee_sat_vb")
    if fee is None:
        scores["mempool_fastest_fee_sat_vb"] = MISSING_FIELD_PENALTY_SCORE
        missing.append("mempool_fastest_fee_sat_vb")
    else:
        # <= 10 sat/vB = calm (10); >= 150 sat/vB = congested (90)
        scores["mempool_fastest_fee_sat_vb"] = _clamp((fee / 150.0) * 80.0 + 10.0)

    return scores, missing


def run_mod31_icdm(canonical: dict[str, Any], trust_passed: bool) -> dict[str, Any]:
    vol_s, vol_m = _score_volatility_stress(canonical)
    drv_s, drv_m = _score_derivatives_stress(canonical)
    liq_s, liq_m = _score_liquidity_flow_stress(canonical)
    mac_s, mac_m = _score_macro_onchain_stress(canonical)

    vol_avg = sum(vol_s.values()) / len(vol_s)
    drv_avg = sum(drv_s.values()) / len(drv_s)
    liq_avg = sum(liq_s.values()) / len(liq_s)
    mac_avg = sum(mac_s.values()) / len(mac_s)

    # Weighted composite (0-100)
    raw_icdm = 0.30 * vol_avg + 0.25 * drv_avg + 0.25 * liq_avg + 0.20 * mac_avg
    missing_fields = vol_m + drv_m + liq_m + mac_m
    total_factors = len(vol_s) + len(drv_s) + len(liq_s) + len(mac_s)
    missing_ratio = len(missing_fields) / total_factors

    # Trust penalty floor if MOD 36 failed
    icdm_score = raw_icdm if trust_passed else max(raw_icdm, 75.0)
    icdm_score = round(_clamp(icdm_score), 2)

    if icdm_score < 25.0:
        band = "LOW"
    elif icdm_score < 50.0:
        band = "MODERATE"
    elif icdm_score < 70.0:
        band = "ELEVATED"
    elif icdm_score < 85.0:
        band = "SEVERE"
    else:
        band = "CRITICAL"

    confidence = "HIGH" if missing_ratio <= 0.15 else ("MEDIUM" if missing_ratio <= 0.45 else "LOW")

    return {
        "module": "MOD 31",
        "icdm_score": icdm_score,
        "fragility_band": band,
        "confidence": confidence,
        "missing_penalty_value": MISSING_FIELD_PENALTY_SCORE,
        "missing_fields_count": len(missing_fields),
        "total_factors": total_factors,
        "missing_fields_ratio": round(missing_ratio, 3),
        "missing_fields": missing_fields,
        "sub_scores": {
            "volatility_stress": round(vol_avg, 2),
            "derivatives_stress": round(drv_avg, 2),
            "liquidity_flow_stress": round(liq_avg, 2),
            "macro_onchain_stress": round(mac_avg, 2),
        },
        "factor_scores": {**vol_s, **drv_s, **liq_s, **mac_s},
    }


# ---------------------------------------------------------------------------
# MOD 33: 5-Regime Master Radar
# ---------------------------------------------------------------------------

def run_mod33_regime_radar(
    canonical: dict[str, Any],
    mod36: dict[str, Any],
    mod31: dict[str, Any],
) -> dict[str, Any]:
    spot = mod36.get("median_spot_usd") or canonical.get("spot_price")
    sma50 = canonical.get("sma50")
    sma200 = canonical.get("sma200")
    rsi14 = canonical.get("rsi14")
    atr_pct = canonical.get("atr_pct")
    funding = canonical.get("funding_rate_pct")
    vix = canonical.get("vix")
    spot_cvd = canonical.get("spot_cvd_24h_btc")
    icdm = mod31["icdm_score"]

    rationale: list[str] = []
    macro_headwind = bool((vix is not None and vix >= 25.0) or (canonical.get("us10y_real_yield_pct") is not None and canonical["us10y_real_yield_pct"] >= 2.2))

    above_sma50 = spot is not None and sma50 is not None and spot > sma50
    above_sma200 = spot is not None and sma200 is not None and spot > sma200
    below_sma50 = spot is not None and sma50 is not None and spot < sma50
    below_sma200 = spot is not None and sma200 is not None and spot < sma200

    # Priority 1: Crisis / Capitulation or Untrusted Telemetry
    if not mod36["trust_passed"] or icdm >= 75.0 or (vix is not None and vix >= 30.0) or (below_sma200 and rsi14 is not None and rsi14 < 30.0):
        regime_id = "R5_CAPITULATION_CRISIS"
        regime_name = "R5: Capitulation / Crisis Defense"
        trend_bias = "DEFENSIVE"
        if not mod36["trust_passed"]:
            rationale.append("MOD 36 trust gate failed; forced defensive regime")
        if icdm >= 75.0:
            rationale.append(f"ICDM fragility critical ({icdm:.1f} >= 75)")
        if vix is not None and vix >= 30.0:
            rationale.append(f"VIX spike ({vix:.1f} >= 30)")
        if below_sma200 and rsi14 is not None and rsi14 < 30.0:
            rationale.append(f"Spot < SMA200 with capitulation RSI ({rsi14:.1f})")

    # Priority 2: Overheated Euphoria
    elif (above_sma50 and ((rsi14 is not None and rsi14 >= 74.0) or (funding is not None and funding >= 0.04))):
        regime_id = "R3_EUPHORIA_OVERHEATED"
        regime_name = "R3: Euphoria / Overheated Leverage"
        trend_bias = "CAUTIOUS_BULL"
        if rsi14 is not None and rsi14 >= 74.0:
            rationale.append(f"RSI overextended ({rsi14:.1f} >= 74)")
        if funding is not None and funding >= 0.04:
            rationale.append(f"Perp funding elevated ({funding:.4f}%/8h)")

    # Priority 3: Distribution / Correction
    elif (below_sma50 and below_sma200) or (below_sma50 and (icdm >= 52.0 or (spot_cvd is not None and spot_cvd < -1500.0))):
        regime_id = "R4_DISTRIBUTION_CORRECTION"
        regime_name = "R4: Distribution / Correction"
        trend_bias = "BEARISH"
        if below_sma50:
            rationale.append("Spot below SMA50")
        if below_sma200:
            rationale.append("Spot below SMA200")
        if icdm >= 52.0:
            rationale.append(f"Elevated fragility (ICDM {icdm:.1f})")

    # Priority 4: Bull Expansion
    elif above_sma50 and above_sma200 and icdm < 55.0:
        regime_id = "R1_BULL_EXPANSION"
        regime_name = "R1: Bull Trend Expansion"
        trend_bias = "BULLISH"
        rationale.append("Spot > SMA50 and SMA200 with contained fragility")
        if sma50 is not None and sma200 is not None and sma50 > sma200:
            rationale.append("Golden structure (SMA50 > SMA200)")

    # Priority 5: Accumulation / Range
    else:
        regime_id = "R2_ACCUMULATION_RANGE"
        regime_name = "R2: Accumulation / Range Equilibrium"
        trend_bias = "NEUTRAL"
        if atr_pct is not None and atr_pct < 3.5:
            rationale.append(f"Contained ATR% ({atr_pct:.2f}%)")
        if above_sma200:
            rationale.append("Macro floor intact (Spot > SMA200)")
        elif not rationale:
            rationale.append("Mixed structure; range equilibrium assumed")

    return {
        "module": "MOD 33",
        "regime_id": regime_id,
        "regime_name": regime_name,
        "trend_bias": trend_bias,
        "macro_headwind_flag": macro_headwind,
        "above_sma50": above_sma50,
        "above_sma200": above_sma200,
        "rationale": rationale,
    }


# ---------------------------------------------------------------------------
# MOD 30: PCF3 Configs A-J Router
# ---------------------------------------------------------------------------

def run_mod30_pcf3_router(
    canonical: dict[str, Any],
    mod36: dict[str, Any],
    mod31: dict[str, Any],
    mod33: dict[str, Any],
) -> dict[str, Any]:
    regime = mod33["regime_id"]
    icdm = mod31["icdm_score"]
    spot = mod36.get("median_spot_usd") or canonical.get("spot_price")
    rsi14 = canonical.get("rsi14")
    atr_pct = canonical.get("atr_pct")
    funding = canonical.get("funding_rate_pct")
    spot_cvd = canonical.get("spot_cvd_24h_btc")
    r_high = canonical.get("range_high_45d")
    r_low = canonical.get("range_low_45d")

    range_pos: float | None = None
    if spot is not None and r_high is not None and r_low is not None and r_high > r_low:
        range_pos = (spot - r_low) / (r_high - r_low)

    if not mod36["trust_passed"] or icdm >= 85.0:
        cfg = ("J", "Hard Circuit Breaker / Telemetry Halt", "FLAT_LOCKED", 0.0, 1.5, 4.5,
               "MOD 36 trust failure or ICDM >= 85 critical fragility")
    elif regime == "R5_CAPITULATION_CRISIS":
        if rsi14 is not None and rsi14 < 26.0 and (funding is not None and funding < -0.015) and icdm < 85.0:
            cfg = ("I", "Capitulation Bounce Probe", "WATCH", 0.25, 1.2, 4.2,
                   "Extreme oversold RSI + negative funding washout; probe only if Net R >= 3.5")
        else:
            cfg = ("J", "Crisis Preservation Lock", "FLAT_LOCKED", 0.0, 1.5, 4.5,
                   "R5 crisis regime without clean capitulation washout")
    elif regime == "R3_EUPHORIA_OVERHEATED":
        cfg = ("F", "Overheated Trailing / De-Risk", "TRIM", 0.0, 1.0, 3.2,
               "R3 overheated regime; prohibit fresh long entries and protect open gains")
    elif regime == "R4_DISTRIBUTION_CORRECTION":
        if mod33["above_sma200"]:
            cfg = ("G", "Macro / Trend Divergence Caution", "FLAT_CASH", 0.0, 1.2, 3.8,
                   "Spot below SMA50 while holding SMA200; stand aside until reclaim")
        else:
            cfg = ("H", "Bear Trend Capital Preservation", "FLAT_CASH", 0.0, 1.2, 4.0,
                   "Spot below SMA50 & SMA200; full spot capital preservation")
    elif regime == "R1_BULL_EXPANSION":
        if icdm < 35.0 and (rsi14 is None or rsi14 >= 54.0):
            cfg = ("A", "Core Trend Breakout", "LONG_SPOT", 1.00, 1.25, 4.25,
                   "R1 Bull Expansion with low fragility (ICDM < 35)")
        elif spot_cvd is not None and spot_cvd > 0 and (funding is None or funding <= 0.015):
            cfg = ("E", "Carry & Spot-Led Accumulation", "LONG_SPOT", 0.80, 1.20, 4.00,
                   "Spot-led CVD accumulation with healthy funding in R1")
        else:
            cfg = ("B", "Pullback Continuation", "LONG_SPOT", 0.85, 1.20, 4.00,
                   "R1 Bull structure with moderate fragility / consolidation")
    else:  # R2_ACCUMULATION_RANGE
        if spot_cvd is not None and spot_cvd > 0 and (funding is None or funding <= 0.01) and icdm < 50.0:
            cfg = ("E", "Spot-Led Range Accumulation", "LONG_SPOT", 0.75, 1.20, 4.00,
                   "Positive spot CVD with neutral/low funding inside R2 range")
        elif range_pos is not None and range_pos <= 0.35 and icdm < 50.0:
            cfg = ("C", "Range Support Mean-Reversion", "LONG_SPOT", 0.70, 1.15, 3.90,
                   "Lower 35% of 45D range with controlled fragility")
        elif atr_pct is not None and atr_pct < 2.5 and icdm < 50.0:
            cfg = ("D", "Volatility Compression Watch", "WATCH", 0.40, 1.15, 3.80,
                   "Compressed volatility range; await directional expansion")
        else:
            cfg = ("D", "Equilibrium Standby", "WATCH", 0.0, 1.20, 4.00,
                   "Mid-range equilibrium without asymmetric edge")

    config_id, config_name, stance, mult, stop_mult, target_mult, reason = cfg
    return {
        "module": "MOD 30",
        "config_id": config_id,
        "config_name": config_name,
        "stance": stance,
        "risk_multiplier": mult,
        "stop_atr_mult": stop_mult,
        "target_atr_mult": target_mult,
        "range_position_45d": round(range_pos, 3) if range_pos is not None else None,
        "routing_reason": reason,
    }


# ---------------------------------------------------------------------------
# MOD 37: Executable Liquidity, Post-Cost Net R >= 3.0, Heat <= 0.75%, Locks
# ---------------------------------------------------------------------------

def run_mod37_risk_gate(
    canonical: dict[str, Any],
    mod36: dict[str, Any],
    mod30: dict[str, Any],
    equity_usd: float,
    portfolio_state: dict[str, Any],
) -> dict[str, Any]:
    failed_gates: list[str] = []

    daily_pnl = canonical.get("daily_pnl_pct")
    if daily_pnl is None:
        daily_pnl = float(portfolio_state.get("daily_pnl_pct", 0.0))
    weekly_pnl = canonical.get("weekly_pnl_pct")
    if weekly_pnl is None:
        weekly_pnl = float(portfolio_state.get("weekly_pnl_pct", 0.0))
    open_heat = canonical.get("open_portfolio_heat_pct")
    if open_heat is None:
        open_heat = float(portfolio_state.get("open_portfolio_heat_pct", 0.0))

    daily_lock = daily_pnl <= DAILY_LOSS_LOCK_PCT
    weekly_lock = weekly_pnl <= WEEKLY_LOSS_LOCK_PCT
    if daily_lock:
        failed_gates.append(f"DAILY_LOSS_LOCK({daily_pnl:.2f}%<={DAILY_LOSS_LOCK_PCT:.2f}%)")
    if weekly_lock:
        failed_gates.append(f"WEEKLY_LOSS_LOCK({weekly_pnl:.2f}%<={WEEKLY_LOSS_LOCK_PCT:.2f}%)")

    available_heat_pct = max(0.0, MAX_PORTFOLIO_HEAT_PCT - open_heat)
    heat_ok = open_heat < MAX_PORTFOLIO_HEAT_PCT
    if not heat_ok:
        failed_gates.append(f"PORTFOLIO_HEAT_CAP({open_heat:.2f}%>={MAX_PORTFOLIO_HEAT_PCT:.2f}%)")

    spread_bps = canonical.get("spread_bps")
    depth_1pct = canonical.get("depth_1pct_usd")
    liquidity_status = "VERIFIED"
    if spread_bps is None or depth_1pct is None:
        liquidity_status = "UNVERIFIED_CONSERVATIVE"
        eff_spread_bps = spread_bps if spread_bps is not None else 8.0
        slippage_bps = 8.0
    else:
        eff_spread_bps = spread_bps
        est_notional = min(equity_usd, equity_usd * 0.5)
        slippage_bps = min(25.0, (est_notional / max(depth_1pct, 1.0)) * 100.0 + 2.0)
        if spread_bps > MAX_SPREAD_BPS:
            liquidity_status = "FAIL_WIDE_SPREAD"
            failed_gates.append(f"SPREAD_TOO_WIDE({spread_bps:.2f}bps>{MAX_SPREAD_BPS:.0f}bps)")
        if depth_1pct < MIN_DEPTH_1PCT_USD:
            liquidity_status = "FAIL_THIN_DEPTH"
            failed_gates.append(f"THIN_DEPTH(${depth_1pct:,.0f}<${MIN_DEPTH_1PCT_USD:,.0f})")

    total_cost_bps = SPOT_FEE_ROUNDTRIP_BPS + eff_spread_bps + slippage_bps

    entry = mod36.get("median_spot_usd") or canonical.get("spot_price")
    atr14 = canonical.get("atr14")
    stop_usd: float | None = None
    target_usd: float | None = None
    gross_r: float | None = None
    net_r: float | None = None
    net_r_passed = False

    if entry is not None and entry > 0:
        unit_vol = atr14 if (atr14 is not None and atr14 > 0) else (entry * 0.025)
        stop_dist = max(entry * 0.012, min(entry * 0.10, mod30["stop_atr_mult"] * unit_vol))
        target_dist = mod30["target_atr_mult"] * unit_vol
        stop_usd = round(entry - stop_dist, 2)
        target_usd = round(entry + target_dist, 2)

        cost_usd = entry * (total_cost_bps / 10000.0)
        gross_r = round(target_dist / stop_dist, 3)
        net_r = round((target_dist - cost_usd) / (stop_dist + cost_usd), 3)
        net_r_passed = net_r >= MIN_NET_R
        if not net_r_passed and mod30["stance"] == "LONG_SPOT":
            failed_gates.append(f"NET_R_BELOW_MIN({net_r:.2f}<{MIN_NET_R:.1f})")
    else:
        failed_gates.append("NO_ENTRY_PRICE")

    if not mod36["trust_passed"]:
        failed_gates.append("MOD36_TRUST_FAILED")

    stance = mod30["stance"]
    liquidity_ok = liquidity_status in {"VERIFIED", "UNVERIFIED_CONSERVATIVE"}
    execution_allowed = (
        stance == "LONG_SPOT"
        and mod36["trust_passed"]
        and not daily_lock
        and not weekly_lock
        and heat_ok
        and liquidity_ok
        and net_r_passed
    )

    if daily_lock or weekly_lock or not mod36["trust_passed"] or stance == "FLAT_LOCKED":
        verdict_action = "LOCKED_HALT"
    elif execution_allowed:
        verdict_action = "EXECUTE_LONG_SPOT"
    elif stance == "WATCH":
        verdict_action = "HOLD_WATCH"
    else:
        verdict_action = "FLAT_CASH"

    return {
        "module": "MOD 37",
        "execution_allowed": execution_allowed,
        "verdict_action": verdict_action,
        "liquidity_status": liquidity_status,
        "spread_bps": _round_opt(eff_spread_bps, 2),
        "slippage_bps": round(slippage_bps, 2),
        "estimated_cost_bps": round(total_cost_bps, 2),
        "entry_usd": round(entry, 2) if entry is not None else None,
        "stop_usd": stop_usd,
        "target_usd": target_usd,
        "gross_r": gross_r,
        "net_r": net_r,
        "min_net_r": MIN_NET_R,
        "net_r_passed": net_r_passed,
        "open_portfolio_heat_pct": round(open_heat, 3),
        "max_portfolio_heat_pct": MAX_PORTFOLIO_HEAT_PCT,
        "available_heat_pct": round(available_heat_pct, 3),
        "daily_pnl_pct": round(daily_pnl, 3),
        "weekly_pnl_pct": round(weekly_pnl, 3),
        "daily_loss_lock_pct": DAILY_LOSS_LOCK_PCT,
        "weekly_loss_lock_pct": WEEKLY_LOSS_LOCK_PCT,
        "loss_lock_triggered": daily_lock or weekly_lock,
        "failed_gates": failed_gates,
    }


# ---------------------------------------------------------------------------
# MOD 18: 1.0x Unleveraged Spot BTC Position Sizer
# ---------------------------------------------------------------------------

def run_mod18_position_sizer(
    mod30: dict[str, Any],
    mod37: dict[str, Any],
    equity_usd: float,
) -> dict[str, Any]:
    entry = mod37.get("entry_usd")
    stop = mod37.get("stop_usd")
    available_heat = mod37["available_heat_pct"]

    if not mod37["execution_allowed"] or entry is None or stop is None or entry <= stop:
        return {
            "module": "MOD 18",
            "leverage_cap": 1.0,
            "equity_usd": round(equity_usd, 2),
            "risk_budget_pct": 0.0,
            "stop_distance_pct": round(((entry - stop) / entry) * 100.0, 3) if (entry and stop and entry > stop) else None,
            "recommended_alloc_pct": 0.0,
            "recommended_notional_usd": 0.0,
            "recommended_btc_qty": 0.0,
            "max_loss_usd": 0.0,
            "sizing_note": "Zero allocation: execution gate closed or stance non-long.",
        }

    stop_dist_pct = ((entry - stop) / entry) * 100.0
    risk_budget_pct = min(available_heat, MAX_PORTFOLIO_HEAT_PCT * mod30["risk_multiplier"])
    raw_alloc_pct = (risk_budget_pct / stop_dist_pct) * 100.0 if stop_dist_pct > 0 else 0.0

    # Strict 1.0x unleveraged spot cap (<= 100.0% of spot equity)
    alloc_pct = min(100.0, max(0.0, raw_alloc_pct))
    notional_usd = equity_usd * (alloc_pct / 100.0)
    btc_qty = notional_usd / entry
    actual_risk_usd = notional_usd * (stop_dist_pct / 100.0)

    return {
        "module": "MOD 18",
        "leverage_cap": 1.0,
        "equity_usd": round(equity_usd, 2),
        "risk_budget_pct": round(risk_budget_pct, 3),
        "stop_distance_pct": round(stop_dist_pct, 3),
        "recommended_alloc_pct": round(alloc_pct, 2),
        "recommended_notional_usd": round(notional_usd, 2),
        "recommended_btc_qty": round(btc_qty, 6),
        "max_loss_usd": round(actual_risk_usd, 2),
        "sizing_note": "1.0x unleveraged spot BTC cap enforced.",
    }


def _load_json_if_exists(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def compile_cortex_verdict(
    raw_metrics: dict[str, Any],
    equity_usd: float = DEFAULT_EQUITY_USD,
    portfolio_state: dict[str, Any] | None = None,
    now_utc: datetime | None = None,
) -> dict[str, Any]:
    clock_utc = now_utc or datetime.now(timezone.utc)
    clock_myt = clock_utc.astimezone(_myt_tz())
    adapted = adapt_telemetry(raw_metrics)
    canonical = adapted["canonical"]
    pstate = portfolio_state or {}

    mod36 = run_mod36_trust_gate(canonical, clock_utc)
    mod31 = run_mod31_icdm(canonical, mod36["trust_passed"])
    mod33 = run_mod33_regime_radar(canonical, mod36, mod31)
    mod30 = run_mod30_pcf3_router(canonical, mod36, mod31, mod33)
    mod37 = run_mod37_risk_gate(canonical, mod36, mod30, equity_usd, pstate)
    mod18 = run_mod18_position_sizer(mod30, mod37, equity_usd)

    core_payload: dict[str, Any] = {
        "engine_version": ENGINE_VERSION,
        "compiled_at_utc": clock_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "compiled_at_myt": clock_myt.strftime("%Y-%m-%d %H:%M:%S MYT"),
        "source_format": adapted["source_format"],
        "summary": {
            "verdict_action": mod37["verdict_action"],
            "execution_allowed": mod37["execution_allowed"],
            "spot_usd": mod36["median_spot_usd"],
            "trust_status": mod36["trust_status"],
            "icdm_score": mod31["icdm_score"],
            "fragility_band": mod31["fragility_band"],
            "regime_id": mod33["regime_id"],
            "pcf3_config": mod30["config_id"],
            "net_r": mod37["net_r"],
            "alloc_pct_1x": mod18["recommended_alloc_pct"],
        },
        "mod36_trust": mod36,
        "mod31_icdm": mod31,
        "mod33_regime": mod33,
        "mod30_pcf3": mod30,
        "mod37_risk": mod37,
        "mod18_sizing": mod18,
        "canonical_telemetry": canonical,
    }

    digest_input = json.dumps(
        {
            "summary": core_payload["summary"],
            "mod36": mod36,
            "mod31": mod31,
            "mod33": mod33,
            "mod30": mod30,
            "mod37": mod37,
            "mod18": mod18,
        },
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    core_payload["determinism_sha256"] = hashlib.sha256(digest_input).hexdigest()
    return core_payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Project CORTEX-BTC v3.0 Matrix Compiler")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT_PATH)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    parser.add_argument("--portfolio", type=Path, default=DEFAULT_PORTFOLIO_PATH)
    parser.add_argument(
        "--equity-usd",
        type=float,
        default=float(os.environ.get("CORTEX_EQUITY_USD", DEFAULT_EQUITY_USD)),
    )
    args = parser.parse_args()

    raw_metrics = _load_json_if_exists(args.input)
    portfolio_state = _load_json_if_exists(args.portfolio)
    verdict = compile_cortex_verdict(
        raw_metrics=raw_metrics,
        equity_usd=args.equity_usd,
        portfolio_state=portfolio_state,
    )
    args.output.write_text(json.dumps(verdict, indent=2), encoding="utf-8")
    s = verdict["summary"]
    print(
        f"Compiled {args.output} | action={s['verdict_action']} | spot={s['spot_usd']} | "
        f"ICDM={s['icdm_score']} ({s['fragility_band']}) | regime={s['regime_id']} | "
        f"PCF3={s['pcf3_config']} | NetR={s['net_r']} | alloc={s['alloc_pct_1x']}% | "
        f"sha256={verdict['determinism_sha256'][:12]}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
