#!/usr/bin/env python3
"""
Project CORTEX-BTC (v3.0) — Zero-Dependency Public Telemetry Fetcher.

Fetches live BTC spot, derivatives, order-book liquidity, on-chain mempool,
and macro telemetry using only the Python 3 standard library.
Never invents missing values: failed endpoints yield null (None) and append
a concise diagnostic to errors[].
"""

from __future__ import annotations

import csv
import io
import json
import math
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

OUTPUT_PATH = Path("btc_metrics_latest.json")
USER_AGENT = "CORTEX-BTC/3.0 (+https://github.com/aikeluargalee-tech/project-cortex-btc)"
DEFAULT_TIMEOUT = 10


def _myt_tz() -> timezone | ZoneInfo:
    try:
        return ZoneInfo("Asia/Kuala_Lumpur")
    except Exception:
        return timezone(timedelta(hours=8), name="MYT")


def _http_get_text(url: str, timeout: int = DEFAULT_TIMEOUT) -> tuple[str | None, str | None]:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/json, text/csv, text/plain;q=0.9, */*;q=0.8",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            return raw, None
    except urllib.error.HTTPError as exc:
        return None, f"HTTP {exc.code} on {url.split('?')[0]}"
    except urllib.error.URLError as exc:
        return None, f"URL error ({exc.reason}) on {url.split('?')[0]}"
    except Exception as exc:
        return None, f"Request failed ({type(exc).__name__}) on {url.split('?')[0]}"


def _http_get_json(url: str, timeout: int = DEFAULT_TIMEOUT) -> tuple[Any | None, str | None]:
    text, err = _http_get_text(url, timeout=timeout)
    if err is not None or text is None:
        return None, err
    try:
        return json.loads(text), None
    except json.JSONDecodeError as exc:
        return None, f"JSON decode error ({exc.msg}) on {url.split('?')[0]}"


def _to_float(val: Any) -> float | None:
    if val is None or isinstance(val, bool):
        return None
    try:
        num = float(val)
    except (TypeError, ValueError):
        return None
    return num if math.isfinite(num) else None


def _compute_sma(values: list[float], period: int) -> float | None:
    if len(values) < period:
        return None
    return sum(values[-period:]) / period


def _compute_rsi(closes: list[float], period: int = 14) -> float | None:
    if len(closes) < period + 1:
        return None
    gains: list[float] = []
    losses: list[float] = []
    for idx in range(1, len(closes)):
        delta = closes[idx] - closes[idx - 1]
        gains.append(max(delta, 0.0))
        losses.append(max(-delta, 0.0))
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    for idx in range(period, len(gains)):
        avg_gain = (avg_gain * (period - 1) + gains[idx]) / period
        avg_loss = (avg_loss * (period - 1) + losses[idx]) / period
    if avg_loss == 0.0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100.0 - (100.0 / (1.0 + rs))


def _compute_atr(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    period: int = 14,
) -> float | None:
    if len(closes) < period + 1:
        return None
    trs: list[float] = []
    for idx in range(1, len(closes)):
        tr = max(
            highs[idx] - lows[idx],
            abs(highs[idx] - closes[idx - 1]),
            abs(lows[idx] - closes[idx - 1]),
        )
        trs.append(tr)
    return sum(trs[-period:]) / period


def _compute_realized_vol_7d(closes: list[float]) -> float | None:
    if len(closes) < 8:
        return None
    window = closes[-8:]
    rets: list[float] = []
    for idx in range(1, len(window)):
        if window[idx - 1] > 0 and window[idx] > 0:
            rets.append(math.log(window[idx] / window[idx - 1]))
    if len(rets) < 2:
        return None
    mean_r = sum(rets) / len(rets)
    var = sum((r - mean_r) ** 2 for r in rets) / (len(rets) - 1)
    return math.sqrt(var) * math.sqrt(365.0) * 100.0


def fetch_binance_spot(errors: list[str], now_iso: str) -> dict[str, Any]:
    base = "https://data-api.binance.vision"
    result: dict[str, Any] = {
        "venue": "binance",
        "price": None,
        "high_24h": None,
        "low_24h": None,
        "price_change_pct_24h": None,
        "volume_base_btc_24h": None,
        "volume_quote_usdt_24h": None,
        "sma50": None,
        "sma200": None,
        "rsi14": None,
        "atr14": None,
        "range_high_45d": None,
        "range_low_45d": None,
        "realized_vol_7d_pct": None,
        "spot_cvd_24h_btc": None,
        "spread_bps": None,
        "depth_1pct_usd": None,
        "timestamp_utc": None,
    }

    ticker_24h, err = _http_get_json(f"{base}/api/v3/ticker/24hr?symbol=BTCUSDT")
    if err:
        errors.append(f"binance_24h: {err}")
    elif isinstance(ticker_24h, dict):
        result["price"] = _to_float(ticker_24h.get("lastPrice"))
        result["high_24h"] = _to_float(ticker_24h.get("highPrice"))
        result["low_24h"] = _to_float(ticker_24h.get("lowPrice"))
        result["price_change_pct_24h"] = _to_float(ticker_24h.get("priceChangePercent"))
        result["volume_base_btc_24h"] = _to_float(ticker_24h.get("volume"))
        result["volume_quote_usdt_24h"] = _to_float(ticker_24h.get("quoteVolume"))
        close_ms = _to_float(ticker_24h.get("closeTime"))
        if close_ms is not None:
            dt = datetime.fromtimestamp(close_ms / 1000.0, tz=timezone.utc)
            result["timestamp_utc"] = dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        else:
            result["timestamp_utc"] = now_iso

    klines_1d, err = _http_get_json(f"{base}/api/v3/klines?symbol=BTCUSDT&interval=1d&limit=250")
    if err:
        errors.append(f"binance_1d: {err}")
    elif isinstance(klines_1d, list) and klines_1d:
        highs = [_to_float(row[2]) for row in klines_1d if len(row) > 4]
        lows = [_to_float(row[3]) for row in klines_1d if len(row) > 4]
        closes = [_to_float(row[4]) for row in klines_1d if len(row) > 4]
        if all(x is not None for x in highs) and all(x is not None for x in lows) and all(x is not None for x in closes):
            h_f = [float(x) for x in highs if x is not None]
            l_f = [float(x) for x in lows if x is not None]
            c_f = [float(x) for x in closes if x is not None]
            result["sma50"] = _compute_sma(c_f, 50)
            result["sma200"] = _compute_sma(c_f, 200)
            result["rsi14"] = _compute_rsi(c_f, 14)
            result["atr14"] = _compute_atr(h_f, l_f, c_f, 14)
            result["realized_vol_7d_pct"] = _compute_realized_vol_7d(c_f)
            if len(h_f) >= 45 and len(l_f) >= 45:
                result["range_high_45d"] = max(h_f[-45:])
                result["range_low_45d"] = min(l_f[-45:])

    klines_15m, err = _http_get_json(f"{base}/api/v3/klines?symbol=BTCUSDT&interval=15m&limit=96")
    if err:
        errors.append(f"binance_15m: {err}")
    elif isinstance(klines_15m, list) and klines_15m:
        cvd_24h = 0.0
        valid_bars = 0
        for row in klines_15m:
            if len(row) > 9:
                vol = _to_float(row[5])
                taker_buy = _to_float(row[9])
                if vol is not None and taker_buy is not None:
                    taker_sell = max(0.0, vol - taker_buy)
                    cvd_24h += taker_buy - taker_sell
                    valid_bars += 1
        if valid_bars > 0:
            result["spot_cvd_24h_btc"] = round(cvd_24h, 4)

    depth, err = _http_get_json(f"{base}/api/v3/depth?symbol=BTCUSDT&limit=500")
    if err:
        errors.append(f"binance_depth: {err}")
    elif isinstance(depth, dict):
        bids = depth.get("bids") or []
        asks = depth.get("asks") or []
        if bids and asks:
            best_bid = _to_float(bids[0][0])
            best_ask = _to_float(asks[0][0])
            if best_bid and best_ask and best_bid > 0 and best_ask >= best_bid:
                mid = 0.5 * (best_bid + best_ask)
                result["spread_bps"] = round(((best_ask - best_bid) / mid) * 10000.0, 3)
                low_bound = mid * 0.99
                high_bound = mid * 1.01
                bid_usd = sum(
                    float(p) * float(q)
                    for p, q in bids
                    if _to_float(p) is not None and _to_float(q) is not None and float(p) >= low_bound
                )
                ask_usd = sum(
                    float(p) * float(q)
                    for p, q in asks
                    if _to_float(p) is not None and _to_float(q) is not None and float(p) <= high_bound
                )
                result["depth_1pct_usd"] = round(bid_usd + ask_usd, 2)

    return result


def fetch_coinbase_spot(errors: list[str], now_iso: str) -> dict[str, Any]:
    data, err = _http_get_json("https://api.exchange.coinbase.com/products/BTC-USD/ticker")
    if err or not isinstance(data, dict):
        errors.append(f"coinbase: {err or 'invalid payload'}")
        return {"venue": "coinbase", "price": None, "timestamp_utc": None}
    price = _to_float(data.get("price"))
    bid = _to_float(data.get("bid"))
    ask = _to_float(data.get("ask"))
    spread_bps = None
    if bid and ask and bid > 0 and ask >= bid:
        mid = 0.5 * (bid + ask)
        spread_bps = round(((ask - bid) / mid) * 10000.0, 3)
    ts_raw = data.get("time")
    ts_iso = now_iso
    if isinstance(ts_raw, str) and ts_raw:
        try:
            dt = datetime.fromisoformat(ts_raw.replace("Z", "+00:00")).astimezone(timezone.utc)
            ts_iso = dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            ts_iso = now_iso
    return {
        "venue": "coinbase",
        "price": price,
        "spread_bps": spread_bps,
        "timestamp_utc": ts_iso if price is not None else None,
    }


def fetch_coingecko_spot(errors: list[str], now_iso: str) -> dict[str, Any]:
    url = (
        "https://api.coingecko.com/api/v3/simple/price"
        "?ids=bitcoin&vs_currencies=usd&include_24hr_vol=true"
        "&include_24hr_change=true&include_last_updated_at=true"
    )
    data, err = _http_get_json(url)
    if err or not isinstance(data, dict) or not isinstance(data.get("bitcoin"), dict):
        errors.append(f"coingecko: {err or 'invalid payload'}")
        return {"venue": "coingecko", "price": None, "timestamp_utc": None}
    btc = data["bitcoin"]
    price = _to_float(btc.get("usd"))
    updated_at = _to_float(btc.get("last_updated_at"))
    ts_iso = now_iso
    if updated_at is not None:
        ts_iso = datetime.fromtimestamp(updated_at, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {
        "venue": "coingecko",
        "price": price,
        "volume_24h_usd": _to_float(btc.get("usd_24h_vol")),
        "price_change_pct_24h": _to_float(btc.get("usd_24h_change")),
        "timestamp_utc": ts_iso if price is not None else None,
    }


def fetch_kraken_spot(errors: list[str], now_iso: str) -> dict[str, Any]:
    data, err = _http_get_json("https://api.kraken.com/0/public/Ticker?pair=XBTUSD")
    if err or not isinstance(data, dict):
        errors.append(f"kraken: {err or 'invalid payload'}")
        return {"venue": "kraken", "price": None, "timestamp_utc": None}
    result = data.get("result")
    if not isinstance(result, dict) or not result:
        errors.append("kraken: empty result")
        return {"venue": "kraken", "price": None, "timestamp_utc": None}
    pair_data = next(iter(result.values()))
    if not isinstance(pair_data, dict):
        return {"venue": "kraken", "price": None, "timestamp_utc": None}
    last_list = pair_data.get("c") or []
    price = _to_float(last_list[0]) if last_list else None
    return {
        "venue": "kraken",
        "price": price,
        "timestamp_utc": now_iso if price is not None else None,
    }


def fetch_okx_derivatives(errors: list[str], now_iso: str) -> dict[str, Any]:
    okx = "https://www.okx.com"
    out: dict[str, Any] = {
        "venue": "OKX BTC-USDT-SWAP",
        "spot_or_swap_price": None,
        "oi_btc": None,
        "oi_change_24h_pct": None,
        "funding_rate_pct": None,
        "long_short_ratio": None,
        "perp_cvd_24h_btc": None,
        "timestamp_utc": None,
    }

    ticker, err = _http_get_json(f"{okx}/api/v5/market/ticker?instId=BTC-USDT")
    if err:
        errors.append(f"okx_spot_ticker: {err}")
    elif isinstance(ticker, dict) and ticker.get("data"):
        row = ticker["data"][0]
        out["spot_or_swap_price"] = _to_float(row.get("last"))
        ts_ms = _to_float(row.get("ts"))
        if ts_ms is not None:
            out["timestamp_utc"] = datetime.fromtimestamp(ts_ms / 1000.0, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        else:
            out["timestamp_utc"] = now_iso

    oi_data, err = _http_get_json(f"{okx}/api/v5/public/open-interest?instType=SWAP&instId=BTC-USDT-SWAP")
    if err:
        errors.append(f"okx_oi: {err}")
    elif isinstance(oi_data, dict) and oi_data.get("data"):
        out["oi_btc"] = _to_float(oi_data["data"][0].get("oiCcy"))

    oi_hist, err = _http_get_json(f"{okx}/api/v5/rubik/stat/contracts/open-interest-history?instId=BTC-USDT-SWAP&period=1H")
    if err:
        errors.append(f"okx_oi_hist: {err}")
    elif isinstance(oi_hist, dict) and isinstance(oi_hist.get("data"), list) and len(oi_hist["data"]) >= 25:
        newest = _to_float(oi_hist["data"][0][1])
        ago_24h = _to_float(oi_hist["data"][24][1])
        if newest is not None and ago_24h is not None and ago_24h > 0:
            out["oi_change_24h_pct"] = round(((newest - ago_24h) / ago_24h) * 100.0, 3)

    fr_data, err = _http_get_json(f"{okx}/api/v5/public/funding-rate?instId=BTC-USDT-SWAP")
    if err:
        errors.append(f"okx_funding: {err}")
    elif isinstance(fr_data, dict) and fr_data.get("data"):
        fr = _to_float(fr_data["data"][0].get("fundingRate"))
        if fr is not None:
            out["funding_rate_pct"] = round(fr * 100.0, 5)

    ls_data, err = _http_get_json(f"{okx}/api/v5/rubik/stat/contracts/long-short-account-ratio?ccy=BTC&period=1H")
    if err:
        errors.append(f"okx_ls_ratio: {err}")
    elif isinstance(ls_data, dict) and ls_data.get("data"):
        out["long_short_ratio"] = _to_float(ls_data["data"][0][1])

    taker_data, err = _http_get_json(f"{okx}/api/v5/rubik/stat/taker-volume-contract?instId=BTC-USDT-SWAP&period=1H&unit=1")
    if err:
        errors.append(f"okx_taker_cvd: {err}")
    elif isinstance(taker_data, dict) and isinstance(taker_data.get("data"), list) and taker_data["data"]:
        bars = taker_data["data"][:24]
        cvd = 0.0
        count = 0
        for bar in bars:
            if len(bar) >= 3:
                sell_v = _to_float(bar[1])
                buy_v = _to_float(bar[2])
                if sell_v is not None and buy_v is not None:
                    cvd += buy_v - sell_v
                    count += 1
        if count > 0:
            out["perp_cvd_24h_btc"] = round(cvd, 4)

    return out


def fetch_mempool_onchain(errors: list[str]) -> dict[str, Any]:
    base = "https://mempool.space/api"
    out: dict[str, Any] = {
        "source": "mempool.space",
        "fastest_fee_sat_vb": None,
        "half_hour_fee_sat_vb": None,
        "hour_fee_sat_vb": None,
        "minimum_fee_sat_vb": None,
        "mempool_tx_count": None,
        "mempool_vsize_bytes": None,
        "block_height": None,
    }

    fees, err = _http_get_json(f"{base}/v1/fees/recommended")
    if err:
        errors.append(f"mempool_fees: {err}")
    elif isinstance(fees, dict):
        out["fastest_fee_sat_vb"] = _to_float(fees.get("fastestFee"))
        out["half_hour_fee_sat_vb"] = _to_float(fees.get("halfHourFee"))
        out["hour_fee_sat_vb"] = _to_float(fees.get("hourFee"))
        out["minimum_fee_sat_vb"] = _to_float(fees.get("minimumFee"))

    pool, err = _http_get_json(f"{base}/mempool")
    if err:
        errors.append(f"mempool_stats: {err}")
    elif isinstance(pool, dict):
        out["mempool_tx_count"] = _to_float(pool.get("count"))
        out["mempool_vsize_bytes"] = _to_float(pool.get("vsize"))

    tip_text, err = _http_get_text(f"{base}/blocks/tip/height")
    if err:
        errors.append(f"mempool_tip: {err}")
    elif tip_text is not None:
        tip = _to_float(tip_text.strip())
        if tip is not None:
            out["block_height"] = int(tip)

    return out


def fetch_fred_series(series_id: str, errors: list[str]) -> dict[str, Any]:
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={urllib.parse.quote(series_id)}"
    text, err = _http_get_text(url, timeout=10)
    if err or not text:
        errors.append(f"fred_{series_id}: {err or 'empty response'}")
        return {"value": None, "as_of_utc": None, "source": f"FRED:{series_id}", "status": "unavailable"}

    reader = csv.reader(io.StringIO(text))
    rows = list(reader)
    for row in reversed(rows[1:]):
        if len(row) >= 2:
            val = _to_float(row[1])
            if val is not None:
                return {
                    "value": val,
                    "as_of_utc": row[0].strip(),
                    "source": f"FRED:{series_id}",
                    "status": "ok",
                }
    errors.append(f"fred_{series_id}: no numeric observations")
    return {"value": None, "as_of_utc": None, "source": f"FRED:{series_id}", "status": "unavailable"}


def collect_metrics() -> dict[str, Any]:
    now_utc = datetime.now(timezone.utc)
    now_myt = now_utc.astimezone(_myt_tz())
    now_iso = now_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
    errors: list[str] = []

    binance = fetch_binance_spot(errors, now_iso)
    coinbase = fetch_coinbase_spot(errors, now_iso)
    coingecko = fetch_coingecko_spot(errors, now_iso)
    kraken = fetch_kraken_spot(errors, now_iso)
    okx = fetch_okx_derivatives(errors, now_iso)
    mempool = fetch_mempool_onchain(errors)

    macro = {
        "us10y_yield_pct": fetch_fred_series("DGS10", errors),
        "us10y_real_yield_pct": fetch_fred_series("DFII10", errors),
        "dxy": fetch_fred_series("DTWEXBGS", errors),
        "vix": fetch_fred_series("VIXCLS", errors),
        "sp500": fetch_fred_series("SP500", errors),
    }

    venues: dict[str, dict[str, Any]] = {
        "binance": {
            "price": binance.get("price"),
            "timestamp_utc": binance.get("timestamp_utc"),
        },
        "coinbase": {
            "price": coinbase.get("price"),
            "timestamp_utc": coinbase.get("timestamp_utc"),
        },
        "coingecko": {
            "price": coingecko.get("price"),
            "timestamp_utc": coingecko.get("timestamp_utc"),
        },
        "kraken": {
            "price": kraken.get("price"),
            "timestamp_utc": kraken.get("timestamp_utc"),
        },
        "okx": {
            "price": okx.get("spot_or_swap_price"),
            "timestamp_utc": okx.get("timestamp_utc"),
        },
    }

    primary_spot = (
        binance.get("price")
        or coinbase.get("price")
        or coingecko.get("price")
        or kraken.get("price")
        or okx.get("spot_or_swap_price")
    )

    spread_bps = binance.get("spread_bps") or coinbase.get("spread_bps")
    volume_24h_usd = binance.get("volume_quote_usdt_24h") or coingecko.get("volume_24h_usd")
    pct_24h = binance.get("price_change_pct_24h")
    if pct_24h is None:
        pct_24h = coingecko.get("price_change_pct_24h")

    return {
        "schema_version": "cortex-telemetry-v3.0",
        "as_of_utc": now_iso,
        "as_of_myt": now_myt.strftime("%Y-%m-%d %H:%M:%S MYT"),
        "generated_at_epoch": int(now_utc.timestamp()),
        "spot_price": primary_spot,
        "venues": venues,
        "price": {
            "spot": primary_spot,
            "high_24h": binance.get("high_24h"),
            "low_24h": binance.get("low_24h"),
            "price_change_pct_24h": pct_24h,
            "volume_24h_usd": volume_24h_usd,
            "sma50": binance.get("sma50"),
            "sma200": binance.get("sma200"),
            "rsi14": binance.get("rsi14"),
            "atr14": binance.get("atr14"),
            "range_high_45d": binance.get("range_high_45d"),
            "range_low_45d": binance.get("range_low_45d"),
            "realized_vol_7d_pct": binance.get("realized_vol_7d_pct"),
        },
        "liquidity": {
            "spread_bps": spread_bps,
            "depth_1pct_usd": binance.get("depth_1pct_usd"),
        },
        "derivatives": {
            "open_interest": {
                "current_btc": okx.get("oi_btc"),
                "change_24h_pct": okx.get("oi_change_24h_pct"),
                "venue": okx.get("venue"),
            },
            "funding_rate_pct": okx.get("funding_rate_pct"),
            "long_short_ratio": okx.get("long_short_ratio"),
            "perp_cvd": {
                "24h": {
                    "cvd_btc": okx.get("perp_cvd_24h_btc"),
                }
            },
        },
        "order_flow": {
            "spot_cvd_binance": {
                "24h": {
                    "cvd_btc": binance.get("spot_cvd_24h_btc"),
                }
            }
        },
        "onchain": mempool,
        "macro": macro,
        "errors": errors,
    }


def main() -> int:
    payload = collect_metrics()
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    valid_venues = sum(1 for v in payload["venues"].values() if v.get("price") is not None)
    print(
        f"Wrote {OUTPUT_PATH} | as_of_myt={payload['as_of_myt']} | "
        f"spot={payload['spot_price']} | venues={valid_venues}/5 | errors={len(payload['errors'])}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
