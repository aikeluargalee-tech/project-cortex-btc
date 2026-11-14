#!/usr/bin/env python3
"""
Project CORTEX-BTC (v3.0) — Canonical Schema Adapter.

Normalizes raw nested or flat market, macro, derivatives, liquidity, and
on-chain telemetry into canonical CORTEX-BTC keys without ever inventing
missing values. Missing, non-finite, or unparseable fields stay None.
"""

from __future__ import annotations

import math
from datetime import datetime, timedelta, timezone
from typing import Any

CANONICAL_SCALAR_FIELDS: tuple[str, ...] = (
    "spot_price",
    "high_24h",
    "low_24h",
    "price_change_pct_24h",
    "volume_24h_usd",
    "sma50",
    "sma200",
    "rsi14",
    "atr14",
    "atr_pct",
    "range_high_45d",
    "range_low_45d",
    "realized_vol_7d_pct",
    "spread_bps",
    "depth_1pct_usd",
    "oi_btc",
    "oi_change_24h_pct",
    "funding_rate_pct",
    "long_short_ratio",
    "perp_cvd_24h_btc",
    "spot_cvd_24h_btc",
    "mempool_fastest_fee_sat_vb",
    "mempool_vsize_bytes",
    "vix",
    "us10y_yield_pct",
    "us10y_real_yield_pct",
    "dxy",
    "sp500",
    "etf_net_flow_usd_m",
)

ICDM_TRACKED_FIELDS: tuple[str, ...] = (
    "spot_price",
    "sma50",
    "sma200",
    "rsi14",
    "atr_pct",
    "realized_vol_7d_pct",
    "spread_bps",
    "depth_1pct_usd",
    "oi_change_24h_pct",
    "funding_rate_pct",
    "long_short_ratio",
    "perp_cvd_24h_btc",
    "spot_cvd_24h_btc",
    "mempool_fastest_fee_sat_vb",
    "vix",
    "us10y_real_yield_pct",
    "dxy",
)


def to_finite_float(value: Any) -> float | None:
    """Convert value to a finite float, returning None if missing or invalid."""
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, str):
        cleaned = value.strip().replace(",", "")
        if not cleaned or cleaned.lower() in {"null", "none", "nan", "na", "n/a", "."}:
            return None
        value = cleaned
    try:
        num = float(value)
    except (TypeError, ValueError):
        return None
    return num if math.isfinite(num) else None


def parse_utc_timestamp(value: Any) -> datetime | None:
    """Parse ISO-8601, 'YYYY-MM-DD HH:MM:SS UTC', or Unix epoch into UTC datetime."""
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        num = to_finite_float(value)
        if num is None or num <= 0:
            return None
        if num > 1e12:
            num /= 1000.0
        try:
            return datetime.fromtimestamp(num, tz=timezone.utc)
        except (OverflowError, OSError, ValueError):
            return None
    if not isinstance(value, str):
        return None
    text = value.strip()
    if not text:
        return None
    if text.endswith(" UTC"):
        text = text[:-4].strip() + "+00:00"
    elif text.endswith(" MYT"):
        text = text[:-4].strip() + "+08:00"
    elif text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(text)
    except ValueError:
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
            try:
                dt = datetime.strptime(text, fmt).replace(tzinfo=timezone.utc)
                return dt
            except ValueError:
                continue
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _get_nested(data: dict[str, Any], *paths: tuple[str, ...]) -> Any:
    """Return the first non-None value found across candidate nested key paths."""
    for path in paths:
        cur: Any = data
        matched = True
        for key in path:
            if isinstance(cur, dict) and key in cur:
                cur = cur[key]
            else:
                matched = False
                break
        if matched and cur is not None:
            return cur
    return None


def _extract_venue_prices(raw: dict[str, Any]) -> tuple[dict[str, float], dict[str, str]]:
    """Extract normalized per-venue spot prices and UTC timestamps without inventing data."""
    venue_prices: dict[str, float] = {}
    venue_timestamps: dict[str, str] = {}

    venues_block = raw.get("venues")
    if isinstance(venues_block, dict):
        for name, item in venues_block.items():
            key = str(name).strip().lower()
            if isinstance(item, dict):
                px = to_finite_float(item.get("price") if "price" in item else item.get("spot"))
                ts = parse_utc_timestamp(item.get("timestamp_utc") or item.get("as_of_utc"))
            else:
                px = to_finite_float(item)
                ts = None
            if px is not None and px > 0:
                venue_prices[key] = px
            if ts is not None:
                venue_timestamps[key] = ts.strftime("%Y-%m-%dT%H:%M:%SZ")

    flat_aliases = {
        "binance": ("binance_price", "binance_spot", "price_binance"),
        "coinbase": ("coinbase_price", "coinbase_spot", "price_coinbase"),
        "coingecko": ("coingecko_price", "coingecko_usd", "price_coingecko"),
        "kraken": ("kraken_price", "kraken_spot", "price_kraken"),
        "okx": ("okx_price", "okx_spot", "price_okx"),
    }
    for venue_name, keys in flat_aliases.items():
        if venue_name not in venue_prices:
            for k in keys:
                px = to_finite_float(raw.get(k))
                if px is not None and px > 0:
                    venue_prices[venue_name] = px
                    break

    return venue_prices, venue_timestamps


def _extract_long_short_ratio(raw: dict[str, Any]) -> float | None:
    direct = to_finite_float(
        _get_nested(
            raw,
            ("long_short_ratio",),
            ("derivatives", "long_short_ratio"),
            ("ls_ratio",),
        )
    )
    if direct is not None:
        return direct

    per_venue = _get_nested(raw, ("derivatives", "long_short_ratio", "per_venue"))
    if isinstance(per_venue, dict):
        vals = []
        for entry in per_venue.values():
            if isinstance(entry, dict):
                v = to_finite_float(entry.get("long_short_account_ratio"))
                if v is not None:
                    vals.append(v)
        if vals:
            return round(sum(vals) / len(vals), 4)
    return None


def adapt_telemetry(raw: dict[str, Any] | None) -> dict[str, Any]:
    """
    Normalize nested or flat raw market/macro/on-chain telemetry into
    canonical CORTEX-BTC keys without inventing missing values.
    """
    if not isinstance(raw, dict) or not raw:
        empty_canonical: dict[str, Any] = {k: None for k in CANONICAL_SCALAR_FIELDS}
        empty_canonical.update(
            {
                "timestamp_utc": None,
                "as_of_myt": None,
                "venue_prices": {},
                "venue_timestamps": {},
                "daily_pnl_pct": None,
                "weekly_pnl_pct": None,
                "open_portfolio_heat_pct": None,
            }
        )
        return {
            "source_format": "empty",
            "canonical": empty_canonical,
            "field_status": {k: "missing" for k in ICDM_TRACKED_FIELDS},
            "missing_fields": list(ICDM_TRACKED_FIELDS),
            "present_count": 0,
            "total_tracked": len(ICDM_TRACKED_FIELDS),
        }

    has_nested = any(
        isinstance(raw.get(k), dict)
        for k in ("price", "derivatives", "macro", "onchain", "liquidity", "venues")
    )
    has_flat = any(
        k in raw
        for k in ("spot_price", "rsi14", "funding_rate_pct", "vix", "dxy", "mempool_fastest_fee_sat_vb")
    )
    source_format = "mixed" if (has_nested and has_flat) else ("nested" if has_nested else "flat")

    ts_dt = (
        parse_utc_timestamp(raw.get("generated_at_epoch"))
        or parse_utc_timestamp(raw.get("as_of_utc"))
        or parse_utc_timestamp(raw.get("timestamp_utc"))
        or parse_utc_timestamp(raw.get("timestamp"))
        or parse_utc_timestamp(raw.get("as_of_myt"))
    )
    timestamp_utc = ts_dt.strftime("%Y-%m-%dT%H:%M:%SZ") if ts_dt else None
    as_of_myt = (
        (ts_dt + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S MYT")
        if ts_dt
        else (str(raw["as_of_myt"]) if isinstance(raw.get("as_of_myt"), str) else None)
    )

    venue_prices, venue_timestamps = _extract_venue_prices(raw)

    spot_price = to_finite_float(
        _get_nested(raw, ("spot_price",), ("price", "spot"), ("btc_price",), ("last_price",))
    )
    if spot_price is not None and spot_price <= 0:
        spot_price = None

    high_24h = to_finite_float(
        _get_nested(raw, ("high_24h",), ("price", "high_24h"), ("core_24h", "high_24h"))
    )
    low_24h = to_finite_float(
        _get_nested(raw, ("low_24h",), ("price", "low_24h"), ("core_24h", "low_24h"))
    )
    price_change_pct_24h = to_finite_float(
        _get_nested(
            raw,
            ("price_change_pct_24h",),
            ("price", "price_change_pct_24h"),
            ("core_24h", "price_change_pct_24h"),
        )
    )
    volume_24h_usd = to_finite_float(
        _get_nested(
            raw,
            ("volume_24h_usd",),
            ("price", "volume_24h_usd"),
            ("core_24h", "volume_quote_usdt_24h"),
        )
    )

    sma50 = to_finite_float(_get_nested(raw, ("sma50",), ("price", "sma50")))
    sma200 = to_finite_float(_get_nested(raw, ("sma200",), ("price", "sma200")))
    rsi14 = to_finite_float(_get_nested(raw, ("rsi14",), ("price", "rsi14")))
    atr14 = to_finite_float(_get_nested(raw, ("atr14",), ("price", "atr14")))
    atr_pct = to_finite_float(_get_nested(raw, ("atr_pct",), ("price", "atr_pct")))
    if atr_pct is None and atr14 is not None and spot_price is not None and spot_price > 0:
        atr_pct = round((atr14 / spot_price) * 100.0, 4)

    range_high_45d = to_finite_float(_get_nested(raw, ("range_high_45d",), ("price", "range_high_45d")))
    range_low_45d = to_finite_float(_get_nested(raw, ("range_low_45d",), ("price", "range_low_45d")))
    realized_vol_7d_pct = to_finite_float(
        _get_nested(raw, ("realized_vol_7d_pct",), ("price", "realized_vol_7d_pct"))
    )

    spread_bps = to_finite_float(
        _get_nested(raw, ("spread_bps",), ("liquidity", "spread_bps"))
    )
    depth_1pct_usd = to_finite_float(
        _get_nested(raw, ("depth_1pct_usd",), ("liquidity", "depth_1pct_usd"))
    )

    oi_btc = to_finite_float(
        _get_nested(
            raw,
            ("oi_btc",),
            ("derivatives", "open_interest", "current_btc"),
            ("derivatives", "open_interest_aggregated", "total_btc"),
        )
    )
    oi_change_24h_pct = to_finite_float(
        _get_nested(
            raw,
            ("oi_change_24h_pct",),
            ("derivatives", "open_interest", "change_24h_pct"),
        )
    )
    funding_rate_pct = to_finite_float(
        _get_nested(
            raw,
            ("funding_rate_pct",),
            ("derivatives", "funding_rate_pct"),
            ("derivatives", "funding_rates", "average_pct"),
        )
    )
    long_short_ratio = _extract_long_short_ratio(raw)
    perp_cvd_24h_btc = to_finite_float(
        _get_nested(
            raw,
            ("perp_cvd_24h_btc",),
            ("derivatives", "perp_cvd", "24h", "cvd_btc"),
        )
    )
    spot_cvd_24h_btc = to_finite_float(
        _get_nested(
            raw,
            ("spot_cvd_24h_btc",),
            ("order_flow", "spot_cvd_binance", "24h", "cvd_btc"),
        )
    )

    mempool_fastest_fee_sat_vb = to_finite_float(
        _get_nested(
            raw,
            ("mempool_fastest_fee_sat_vb",),
            ("onchain", "fastest_fee_sat_vb"),
        )
    )
    mempool_vsize_bytes = to_finite_float(
        _get_nested(
            raw,
            ("mempool_vsize_bytes",),
            ("onchain", "mempool_vsize_bytes"),
        )
    )

    vix = to_finite_float(_get_nested(raw, ("vix",), ("macro", "vix", "value")))
    us10y_yield_pct = to_finite_float(
        _get_nested(raw, ("us10y_yield_pct",), ("macro", "us10y_yield_pct", "value"))
    )
    us10y_real_yield_pct = to_finite_float(
        _get_nested(
            raw,
            ("us10y_real_yield_pct",),
            ("macro", "us10y_real_yield_pct", "value"),
            ("macro", "real_yield_10y", "value_pct"),
        )
    )
    dxy = to_finite_float(_get_nested(raw, ("dxy",), ("macro", "dxy", "value")))
    sp500 = to_finite_float(_get_nested(raw, ("sp500",), ("macro", "sp500", "value")))
    etf_net_flow_usd_m = to_finite_float(
        _get_nested(
            raw,
            ("etf_net_flow_usd_m",),
            ("etf_flows", "daily_aggregate", "total_net_flow_usd_m"),
            ("etf_flows", "total_net_flow_usd_m"),
        )
    )

    daily_pnl_pct = to_finite_float(
        _get_nested(raw, ("daily_pnl_pct",), ("portfolio", "daily_pnl_pct"))
    )
    weekly_pnl_pct = to_finite_float(
        _get_nested(raw, ("weekly_pnl_pct",), ("portfolio", "weekly_pnl_pct"))
    )
    open_portfolio_heat_pct = to_finite_float(
        _get_nested(raw, ("open_portfolio_heat_pct",), ("portfolio", "open_portfolio_heat_pct"))
    )

    canonical: dict[str, Any] = {
        "timestamp_utc": timestamp_utc,
        "as_of_myt": as_of_myt,
        "venue_prices": venue_prices,
        "venue_timestamps": venue_timestamps,
        "spot_price": spot_price,
        "high_24h": high_24h,
        "low_24h": low_24h,
        "price_change_pct_24h": price_change_pct_24h,
        "volume_24h_usd": volume_24h_usd,
        "sma50": sma50,
        "sma200": sma200,
        "rsi14": rsi14,
        "atr14": atr14,
        "atr_pct": atr_pct,
        "range_high_45d": range_high_45d,
        "range_low_45d": range_low_45d,
        "realized_vol_7d_pct": realized_vol_7d_pct,
        "spread_bps": spread_bps,
        "depth_1pct_usd": depth_1pct_usd,
        "oi_btc": oi_btc,
        "oi_change_24h_pct": oi_change_24h_pct,
        "funding_rate_pct": funding_rate_pct,
        "long_short_ratio": long_short_ratio,
        "perp_cvd_24h_btc": perp_cvd_24h_btc,
        "spot_cvd_24h_btc": spot_cvd_24h_btc,
        "mempool_fastest_fee_sat_vb": mempool_fastest_fee_sat_vb,
        "mempool_vsize_bytes": mempool_vsize_bytes,
        "vix": vix,
        "us10y_yield_pct": us10y_yield_pct,
        "us10y_real_yield_pct": us10y_real_yield_pct,
        "dxy": dxy,
        "sp500": sp500,
        "etf_net_flow_usd_m": etf_net_flow_usd_m,
        "daily_pnl_pct": daily_pnl_pct,
        "weekly_pnl_pct": weekly_pnl_pct,
        "open_portfolio_heat_pct": open_portfolio_heat_pct,
    }

    field_status: dict[str, str] = {}
    missing_fields: list[str] = []
    for field in ICDM_TRACKED_FIELDS:
        if canonical.get(field) is None:
            field_status[field] = "missing"
            missing_fields.append(field)
        else:
            field_status[field] = "present"

    return {
        "source_format": source_format,
        "canonical": canonical,
        "field_status": field_status,
        "missing_fields": missing_fields,
        "present_count": len(ICDM_TRACKED_FIELDS) - len(missing_fields),
        "total_tracked": len(ICDM_TRACKED_FIELDS),
    }
