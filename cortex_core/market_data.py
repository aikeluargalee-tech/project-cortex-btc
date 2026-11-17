"""
Market Data Normalisation, Provenance & Data-Integrity Layer (Section 13).

Consumes raw telemetry (such as btc_metrics_latest.json emitted by
btc_data_fetcher.py) without modifying existing fetchers, and builds an
immutable, UTC-timestamped MarketSnapshot with explicit DataStatus tags.
"""

from __future__ import annotations

import statistics
import uuid
from datetime import datetime
from typing import Any

from btc_config_loader import get_param
from cortex_core.audit import canonical_sha256
from cortex_core.constants import NOT_CONFIGURED, DataStatus
from cortex_core.models import ConfigurationRecord, DataFieldRecord, MarketSnapshot
from cortex_core.time_utils import parse_utc_timestamp, to_utc_iso, utc_now
from cortex_schema_adapter import adapt_telemetry, to_finite_float


def _classify_freshness(
    event_ts_utc: str | None,
    reference_now: datetime,
    max_age_minutes: Any,
) -> tuple[str, bool]:
    """
    Evaluate freshness against a configured limit (in minutes).
    Never invents a threshold when max_age_minutes is NOT CONFIGURED.
    Returns (freshness_status, is_stale).
    """
    if event_ts_utc is None:
        return "UNAVAILABLE", False
    if max_age_minutes == NOT_CONFIGURED or max_age_minutes is None:
        return NOT_CONFIGURED, False
    try:
        limit_min = float(max_age_minutes)
    except (TypeError, ValueError):
        return NOT_CONFIGURED, False
    dt = parse_utc_timestamp(event_ts_utc)
    if dt is None:
        return "UNAVAILABLE", False
    age_min = (reference_now - dt).total_seconds() / 60.0
    if age_min < -5.0:
        return "FUTURE_SKEW", True
    if age_min > limit_min:
        return "STALE", True
    return "FRESH", False


def _make_field(
    *,
    field_name: str,
    value: Any,
    source: str,
    exchange_or_provider: str,
    instrument: str,
    timeframe: str,
    source_event_ts_utc: str | None,
    retrieved_ts_utc: str,
    reference_now: datetime,
    max_age_minutes: Any,
    base_status: DataStatus,
    notes: str = "",
) -> DataFieldRecord:
    if value is None:
        return DataFieldRecord(
            field_name=field_name,
            value=None,
            source=source,
            exchange_or_provider=exchange_or_provider,
            instrument=instrument,
            timeframe=timeframe,
            source_event_ts_utc=source_event_ts_utc,
            retrieved_ts_utc=retrieved_ts_utc,
            last_successful_update_utc=None,
            validation_status=DataStatus.UNAVAILABLE,
            freshness_status="UNAVAILABLE",
            notes=notes or "Value missing from telemetry feed.",
        )

    freshness_status, is_stale = _classify_freshness(
        source_event_ts_utc, reference_now, max_age_minutes
    )
    status = DataStatus.STALE if is_stale else base_status
    if source_event_ts_utc is None and status == DataStatus.VERIFIED:
        status = DataStatus.PARTIALLY_VERIFIED

    return DataFieldRecord(
        field_name=field_name,
        value=value,
        source=source,
        exchange_or_provider=exchange_or_provider,
        instrument=instrument,
        timeframe=timeframe,
        source_event_ts_utc=source_event_ts_utc,
        retrieved_ts_utc=retrieved_ts_utc,
        last_successful_update_utc=source_event_ts_utc or retrieved_ts_utc,
        validation_status=status,
        freshness_status=freshness_status,
        notes=notes,
    )


def build_market_snapshot(
    raw_metrics: dict[str, Any] | None,
    *,
    config: ConfigurationRecord | None = None,
    now_utc: datetime | str | None = None,
) -> MarketSnapshot:
    """
    Build a structured MarketSnapshot from raw telemetry JSON.

    Strictly preserves source event timestamps separate from retrieval timestamps,
    tags proxy/derived fields honestly, and never fabricates missing fields.
    """
    ref_now = parse_utc_timestamp(now_utc) if now_utc is not None else utc_now()
    if ref_now is None:
        ref_now = utc_now()
    ref_now_iso = ref_now.strftime("%Y-%m-%dT%H:%M:%SZ")

    raw = raw_metrics if isinstance(raw_metrics, dict) else {}
    adapted = adapt_telemetry(raw)
    canonical = adapted["canonical"]

    retrieved_ts_utc = (
        to_utc_iso(raw.get("as_of_utc"))
        or to_utc_iso(raw.get("generated_at_epoch"))
        or ref_now_iso
    )

    spot_max_age = get_param(config, "data_policy.spot_price_max_age_minutes") if config else NOT_CONFIGURED
    cvd_max_age = get_param(config, "data_policy.spot_cvd_max_age_minutes") if config else NOT_CONFIGURED
    ob_max_age = get_param(config, "data_policy.order_book_max_age_minutes") if config else NOT_CONFIGURED
    drv_max_age = get_param(config, "data_policy.derivatives_context_max_age_minutes") if config else NOT_CONFIGURED
    macro_max_days = get_param(config, "data_policy.macro_context_max_age_days") if config else NOT_CONFIGURED
    macro_max_age = (
        float(macro_max_days) * 1440.0
        if macro_max_days not in (NOT_CONFIGURED, None)
        else NOT_CONFIGURED
    )
    max_disp_bps = get_param(config, "data_policy.max_venue_dispersion_bps") if config else NOT_CONFIGURED

    raw_venues = raw.get("venues") if isinstance(raw.get("venues"), dict) else {}
    binance_ts = to_utc_iso((raw_venues.get("binance") or {}).get("timestamp_utc"))
    coinbase_ts = to_utc_iso((raw_venues.get("coinbase") or {}).get("timestamp_utc"))
    coingecko_ts = to_utc_iso((raw_venues.get("coingecko") or {}).get("timestamp_utc"))
    kraken_ts_raw = to_utc_iso((raw_venues.get("kraken") or {}).get("timestamp_utc"))
    okx_ts = to_utc_iso((raw_venues.get("okx") or {}).get("timestamp_utc"))

    # Kraken ticker in btc_data_fetcher.py has no exchange timestamp and emits now_iso;
    # do not treat retrieval time as a verified exchange event timestamp.
    kraken_event_ts = None if (kraken_ts_raw and kraken_ts_raw == retrieved_ts_utc) else kraken_ts_raw

    venue_specs = {
        "binance": ("BTC/USDT", "binance", binance_ts, DataStatus.VERIFIED, "Observed Binance spot BTCUSDT"),
        "coinbase": ("BTC/USD", "coinbase", coinbase_ts, DataStatus.PARTIALLY_VERIFIED, "USD quote reference (not USDT)"),
        "coingecko": ("BTC/USD", "coingecko", coingecko_ts, DataStatus.PROXY, "Aggregated USD price index"),
        "kraken": ("BTC/USD", "kraken", kraken_event_ts, DataStatus.PARTIALLY_VERIFIED, "Kraken ticker lacks source event timestamp"),
        "okx": ("BTC/USDT", "okx", okx_ts, DataStatus.VERIFIED, "Observed OKX spot BTC-USDT"),
    }

    fields: dict[str, DataFieldRecord] = {}
    venue_prices_out: dict[str, dict[str, Any]] = {}
    positive_prices: list[float] = []

    for vname, (inst, exch, v_ts, base_stat, note) in venue_specs.items():
        v_price = to_finite_float((raw_venues.get(vname) or {}).get("price"))
        if v_price is not None and v_price <= 0:
            v_price = None
        if v_price is not None:
            positive_prices.append(v_price)
        rec = _make_field(
            field_name=f"{vname}_spot_price",
            value=v_price,
            source="btc_data_fetcher",
            exchange_or_provider=exch,
            instrument=inst,
            timeframe="spot_tick",
            source_event_ts_utc=v_ts,
            retrieved_ts_utc=retrieved_ts_utc,
            reference_now=ref_now,
            max_age_minutes=spot_max_age,
            base_status=base_stat,
            notes=note,
        )
        fields[rec.field_name] = rec
        venue_prices_out[vname] = {
            "price": v_price,
            "instrument": inst,
            "source_event_ts_utc": v_ts,
            "validation_status": rec.validation_status.value,
            "freshness_status": rec.freshness_status,
        }

    # Check cross-venue price dispersion conflict if threshold configured
    dispersion_bps: float | None = None
    venue_conflict = False
    if len(positive_prices) >= 2:
        med = statistics.median(positive_prices)
        if med > 0:
            dispersion_bps = round(max(abs(p - med) / med for p in positive_prices) * 10000.0, 2)
            if max_disp_bps not in (NOT_CONFIGURED, None):
                try:
                    if dispersion_bps > float(max_disp_bps):
                        venue_conflict = True
                except (TypeError, ValueError):
                    pass

    primary_spot = canonical.get("spot_price")
    fields["spot_price"] = _make_field(
        field_name="spot_price",
        value=primary_spot,
        source="btc_data_fetcher",
        exchange_or_provider="binance",
        instrument="BTC/USDT",
        timeframe="spot_tick",
        source_event_ts_utc=binance_ts,
        retrieved_ts_utc=retrieved_ts_utc,
        reference_now=ref_now,
        max_age_minutes=spot_max_age,
        base_status=DataStatus.CONFLICTING if venue_conflict else DataStatus.VERIFIED,
        notes=(
            f"Cross-venue dispersion {dispersion_bps} bps exceeds configured limit."
            if venue_conflict
            else "Primary spot reference (Binance BTC/USDT)."
        ),
    )

    # Spot OHLCV / technicals (derived from Binance 1D klines)
    ohlcv_present = all(
        canonical.get(k) is not None
        for k in ("sma50", "sma200", "rsi14", "range_high_45d", "range_low_45d")
    )
    fields["spot_ohlcv"] = _make_field(
        field_name="spot_ohlcv",
        value=(
            {
                "sma50": canonical.get("sma50"),
                "sma200": canonical.get("sma200"),
                "rsi14": canonical.get("rsi14"),
                "range_high_45d": canonical.get("range_high_45d"),
                "range_low_45d": canonical.get("range_low_45d"),
            }
            if ohlcv_present
            else None
        ),
        source="btc_data_fetcher",
        exchange_or_provider="binance",
        instrument="BTC/USDT",
        timeframe="1d",
        source_event_ts_utc=binance_ts,
        retrieved_ts_utc=retrieved_ts_utc,
        reference_now=ref_now,
        max_age_minutes=spot_max_age,
        base_status=DataStatus.PARTIALLY_VERIFIED,
        notes="1D OHLCV aggregate indicators present (intraday multi-bar series partial).",
    )

    for fname, base_st, note in [
        ("sma50", DataStatus.VERIFIED, "Calculated from Binance 1D klines"),
        ("sma200", DataStatus.VERIFIED, "Calculated from Binance 1D klines"),
        ("rsi14", DataStatus.VERIFIED, "Calculated from Binance 1D klines"),
        ("atr14", DataStatus.VERIFIED, "Calculated from Binance 1D klines"),
        ("range_high_45d", DataStatus.VERIFIED, "45D high from Binance 1D klines"),
        ("range_low_45d", DataStatus.VERIFIED, "45D low from Binance 1D klines"),
        ("realized_vol_7d_pct", DataStatus.VERIFIED, "7D annualized realized volatility from Binance 1D klines"),
        ("volume_24h_usd", DataStatus.VERIFIED, "Binance 24h quote volume"),
    ]:
        fields[fname] = _make_field(
            field_name=fname,
            value=canonical.get(fname),
            source="btc_data_fetcher",
            exchange_or_provider="binance",
            instrument="BTC/USDT",
            timeframe="1d",
            source_event_ts_utc=binance_ts,
            retrieved_ts_utc=retrieved_ts_utc,
            reference_now=ref_now,
            max_age_minutes=spot_max_age,
            base_status=base_st,
            notes=note,
        )

    # Spot CVD (derived proxy from 15m kline taker-buy volume)
    fields["spot_cvd_24h_btc"] = _make_field(
        field_name="spot_cvd_24h_btc",
        value=canonical.get("spot_cvd_24h_btc"),
        source="btc_data_fetcher",
        exchange_or_provider="binance",
        instrument="BTC/USDT",
        timeframe="15m_24h_agg",
        source_event_ts_utc=binance_ts,
        retrieved_ts_utc=retrieved_ts_utc,
        reference_now=ref_now,
        max_age_minutes=cvd_max_age,
        base_status=DataStatus.PROXY,
        notes="Derived from 15m kline taker-buy volume (proxy for tick-level spot CVD).",
    )

    # Order book metrics (observed depth snapshot, not guaranteed fill liquidity)
    for fname, note in [
        ("spread_bps", "Observed top-of-book bid/ask spread in bps"),
        ("depth_1pct_usd", "Observed +/-1% order-book depth (not guaranteed fill liquidity)"),
    ]:
        fields[fname] = _make_field(
            field_name=fname,
            value=canonical.get(fname),
            source="btc_data_fetcher",
            exchange_or_provider="binance",
            instrument="BTC/USDT",
            timeframe="orderbook_snapshot",
            source_event_ts_utc=binance_ts,
            retrieved_ts_utc=retrieved_ts_utc,
            reference_now=ref_now,
            max_age_minutes=ob_max_age,
            base_status=DataStatus.VERIFIED,
            notes=note,
        )

    # Contextual derivatives (OKX BTC-USDT-SWAP — telemetry context only, never traded)
    for fname in ("oi_btc", "oi_change_24h_pct", "funding_rate_pct", "long_short_ratio", "perp_cvd_24h_btc"):
        fields[fname] = _make_field(
            field_name=fname,
            value=canonical.get(fname),
            source="btc_data_fetcher",
            exchange_or_provider="okx",
            instrument="BTC-USDT-SWAP (CONTEXT ONLY)",
            timeframe="24h_context",
            source_event_ts_utc=okx_ts,
            retrieved_ts_utc=retrieved_ts_utc,
            reference_now=ref_now,
            max_age_minutes=drv_max_age,
            base_status=DataStatus.VERIFIED,
            notes="Derivatives contextual telemetry only (spot-only system).",
        )

    # Macro contextual feeds (FRED)
    raw_macro = raw.get("macro") if isinstance(raw.get("macro"), dict) else {}
    macro_specs = [
        ("us10y_yield_pct", DataStatus.VERIFIED, "FRED:DGS10"),
        ("us10y_real_yield_pct", DataStatus.VERIFIED, "FRED:DFII10"),
        ("dxy", DataStatus.PROXY, "FRED:DTWEXBGS broad trade-weighted USD proxy"),
        ("vix", DataStatus.VERIFIED, "FRED:VIXCLS"),
        ("sp500", DataStatus.VERIFIED, "FRED:SP500"),
    ]
    for fname, base_st, note in macro_specs:
        m_block = raw_macro.get(fname) if isinstance(raw_macro.get(fname), dict) else {}
        m_ts = to_utc_iso(m_block.get("as_of_utc"))
        fields[fname] = _make_field(
            field_name=fname,
            value=canonical.get(fname),
            source=str(m_block.get("source") or "FRED"),
            exchange_or_provider="FRED",
            instrument="MACRO_CONTEXT",
            timeframe="1d",
            source_event_ts_utc=m_ts,
            retrieved_ts_utc=retrieved_ts_utc,
            reference_now=ref_now,
            max_age_minutes=macro_max_age,
            base_status=base_st,
            notes=note,
        )

    # Known missing Phase 2+ telemetry fields explicitly marked UNAVAILABLE when absent
    for missing_name, note in [
        ("etf_net_flow_usd_m", "Spot ETF daily net flow not yet ingested."),
        ("confirmed_liquidations", "Confirmed liquidation feed not yet ingested."),
        ("volume_profile", "Volume profile (VAH/VAL/POC) not yet computed."),
        ("order_book_imbalance_series", "Order-book replenishment history not yet ingested."),
    ]:
        val = canonical.get(missing_name) if missing_name in canonical else None
        fields[missing_name] = _make_field(
            field_name=missing_name,
            value=val,
            source="UNCONFIGURED_FEED",
            exchange_or_provider="NONE",
            instrument="BTC/USDT",
            timeframe="N/A",
            source_event_ts_utc=None,
            retrieved_ts_utc=retrieved_ts_utc,
            reference_now=ref_now,
            max_age_minutes=NOT_CONFIGURED,
            base_status=DataStatus.UNAVAILABLE,
            notes=note,
        )

    missing_list = [k for k, v in fields.items() if v.validation_status == DataStatus.UNAVAILABLE]
    stale_list = [k for k, v in fields.items() if v.validation_status == DataStatus.STALE]
    conflict_list = [k for k, v in fields.items() if v.validation_status == DataStatus.CONFLICTING]
    proxy_list = [k for k, v in fields.items() if v.validation_status == DataStatus.PROXY]

    # Determine overall integrity status conservatively
    mandatory_feeds = (
        get_param(config, "data_policy.mandatory_feeds", ["binance_spot_price"])
        if config
        else ["binance_spot_price"]
    )
    if not isinstance(mandatory_feeds, list):
        mandatory_feeds = ["binance_spot_price"]

    if fields["spot_price"].validation_status == DataStatus.UNAVAILABLE or any(
        f in fields and fields[f].validation_status == DataStatus.UNAVAILABLE for f in mandatory_feeds
    ):
        overall_status = DataStatus.UNAVAILABLE
    elif conflict_list:
        overall_status = DataStatus.CONFLICTING
    elif stale_list:
        overall_status = DataStatus.STALE
    elif missing_list or proxy_list or any(
        v.validation_status == DataStatus.PARTIALLY_VERIFIED for v in fields.values()
    ):
        overall_status = DataStatus.PARTIALLY_VERIFIED
    else:
        overall_status = DataStatus.VERIFIED

    snap_id = f"MKT-{uuid.uuid4().hex[:12].upper()}"
    body_for_hash = {
        "retrieved_ts_utc": retrieved_ts_utc,
        "source_event_ts_utc": binance_ts,
        "spot_price": primary_spot,
        "venue_prices": venue_prices_out,
        "overall_integrity_status": overall_status.value,
        "missing": missing_list,
        "stale": stale_list,
        "conflicting": conflict_list,
    }
    return MarketSnapshot(
        snapshot_id=snap_id,
        retrieved_ts_utc=retrieved_ts_utc,
        source_event_ts_utc=binance_ts,
        instrument="BTC/USDT",
        timeframe="multi",
        overall_integrity_status=overall_status,
        spot_price=primary_spot,
        venue_prices=venue_prices_out,
        fields=fields,
        missing_or_unavailable_fields=missing_list,
        stale_fields=stale_list,
        conflicting_fields=conflict_list,
        proxy_fields=proxy_list,
        raw_errors=list(raw.get("errors") or []),
        snapshot_sha256=canonical_sha256(body_for_hash),
    )
