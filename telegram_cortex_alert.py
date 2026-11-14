#!/usr/bin/env python3
"""
Project CORTEX-BTC (v3.0) — Telegram Mobile HUD Dispatcher.

Reads cortex_verdict_latest.json, formats an HTML-safe mobile HUD card in
Asia/Kuala_Lumpur (MYT / UTC+8) time, and dispatches it via Telegram Bot API
using TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

VERDICT_PATH = Path("cortex_verdict_latest.json")
METRICS_PATH = Path("btc_metrics_latest.json")
TELEGRAM_API_BASE = "https://api.telegram.org"


def _myt_tz() -> timezone | ZoneInfo:
    try:
        return ZoneInfo("Asia/Kuala_Lumpur")
    except Exception:
        return timezone(timedelta(hours=8), name="MYT")


def _esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def _fmt_num(val: Any, prefix: str = "", suffix: str = "", decimals: int = 2) -> str:
    if val is None or not isinstance(val, (int, float)):
        return "N/A"
    return f"{prefix}{val:,.{decimals}f}{suffix}"


def _format_myt_timestamp(verdict: dict[str, Any]) -> str:
    tz_myt = _myt_tz()
    raw_utc = verdict.get("compiled_at_utc")
    if isinstance(raw_utc, str) and raw_utc:
        try:
            dt = datetime.fromisoformat(raw_utc.replace("Z", "+00:00"))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.astimezone(tz_myt).strftime("%Y-%m-%d %H:%M MYT (UTC+8)")
        except ValueError:
            pass
    return datetime.now(tz_myt).strftime("%Y-%m-%d %H:%M MYT (UTC+8)")


def _num(val: Any) -> float | None:
    if val is None or isinstance(val, bool):
        return None
    try:
        out = float(val)
    except (TypeError, ValueError):
        return None
    return out


def extract_active_drivers(
    verdict: dict[str, Any],
    metrics: dict[str, Any] | None = None,
) -> list[str]:
    """
    Deterministically identify the top 2-3 rulebook modules (MOD 01-MOD 40)
    driving the current CORTEX-BTC verdict using verdict + raw metrics keys.
    """
    m36 = verdict.get("mod36_trust") or {}
    m31 = verdict.get("mod31_icdm") or {}
    m33 = verdict.get("mod33_regime") or {}
    m30 = verdict.get("mod30_pcf3") or {}
    m37 = verdict.get("mod37_risk") or {}
    canon = verdict.get("canonical_telemetry") or {}
    raw = metrics or {}

    # Merge canonical telemetry with raw btc_metrics_latest.json fallbacks
    raw_venues = raw.get("venues") or {}
    verdict_venues = m36.get("venue_prices") or canon.get("venue_prices") or {}
    cb_px = _num(verdict_venues.get("coinbase") or (raw_venues.get("coinbase") or {}).get("price"))
    bn_px = _num(verdict_venues.get("binance") or (raw_venues.get("binance") or {}).get("price"))

    raw_macro = raw.get("macro") or {}
    raw_deriv = raw.get("derivatives") or {}
    raw_onchain = raw.get("onchain") or {}
    raw_etf = raw.get("etf_flows") or {}
    raw_flow = raw.get("order_flow") or {}
    raw_price = raw.get("price") or {}

    real_yield = _num(canon.get("us10y_real_yield_pct") or (raw_macro.get("us10y_real_yield_pct") or {}).get("value"))
    nom_yield = _num(canon.get("us10y_yield_pct") or (raw_macro.get("us10y_yield_pct") or {}).get("value"))
    dxy = _num(canon.get("dxy") or (raw_macro.get("dxy") or {}).get("value"))
    vix = _num(canon.get("vix") or (raw_macro.get("vix") or {}).get("value"))

    oi_chg = _num(canon.get("oi_change_24h_pct") or (raw_deriv.get("open_interest") or {}).get("change_24h_pct"))
    funding = _num(canon.get("funding_rate_pct") or raw_deriv.get("funding_rate_pct"))
    ls_ratio = _num(canon.get("long_short_ratio") or raw_deriv.get("long_short_ratio"))
    perp_cvd = _num(canon.get("perp_cvd_24h_btc") or ((raw_deriv.get("perp_cvd") or {}).get("24h") or {}).get("cvd_btc"))
    spot_cvd = _num(canon.get("spot_cvd_24h_btc") or ((raw_flow.get("spot_cvd_binance") or {}).get("24h") or {}).get("cvd_btc"))

    fee_sat = _num(canon.get("mempool_fastest_fee_sat_vb") or raw_onchain.get("fastest_fee_sat_vb"))
    etf_flow = _num(canon.get("etf_net_flow_usd_m") or (raw_etf.get("daily_aggregate") or {}).get("total_net_flow_usd_m"))
    rsi14 = _num(canon.get("rsi14") or raw_price.get("rsi14"))
    spot = _num(m36.get("median_spot_usd") or canon.get("spot_price") or raw.get("spot_price"))
    sma200 = _num(canon.get("sma200") or raw_price.get("sma200"))

    # Candidate tuple: (priority_score, -mod_num, label)
    candidates: dict[int, tuple[float, str]] = {}

    def _add(mod_num: int, score: float, label: str) -> None:
        prev = candidates.get(mod_num)
        if prev is None or score > prev[0]:
            candidates[mod_num] = (score, label)

    # MOD 36: Telemetry Trust / SLA / Quorum
    sla_age = _num(m36.get("sla_age_min"))
    quorum_cnt = _num(m36.get("quorum_count"))
    disp_bps = _num(m36.get("dispersion_bps"))
    if not m36.get("trust_passed", True):
        _add(36, 99.0, "MOD 36 SLA/Quorum")
    elif (sla_age is not None and sla_age > 90.0) or (quorum_cnt is not None and quorum_cnt < 3):
        _add(36, 99.0, "MOD 36 SLA/Quorum")
    elif disp_bps is not None and disp_bps > 150.0:
        _add(36, 78.0, "MOD 36 Venue Disp")

    # MOD 37: Risk / Net-R / Heat / Loss Locks / Liquidity
    if m37.get("loss_lock_triggered"):
        _add(37, 98.0, "MOD 37 Loss-Lock")
    elif (
        _num(m37.get("open_portfolio_heat_pct")) is not None
        and _num(m37.get("max_portfolio_heat_pct")) is not None
        and float(m37["open_portfolio_heat_pct"]) >= float(m37["max_portfolio_heat_pct"])
    ):
        _add(37, 95.0, "MOD 37 Heat Cap")
    elif str(m37.get("liquidity_status") or "").startswith("FAIL_"):
        _add(37, 93.0, "MOD 37 Exec Liq")
    else:
        net_r = _num(m37.get("net_r"))
        min_r = _num(m37.get("min_net_r")) or 3.0
        if net_r is not None and (not m37.get("net_r_passed", True) or net_r < min_r):
            _add(37, 89.0, "MOD 37 Net-R")

    # MOD 17: 200D MA Secular Gate
    if spot is not None and sma200 is not None and spot < sma200:
        sec_score = 90.0 if (rsi14 is not None and rsi14 < 30.0) else 76.0
        _add(17, sec_score, "MOD 17 200D Gate")

    # MOD 16: Macro Liquidity / Real Yields / DXY
    macro_score = 0.0
    if real_yield is not None and real_yield >= 2.0:
        macro_score = max(macro_score, min(96.0, 74.0 + (real_yield - 2.0) * 20.0))
    if nom_yield is not None and nom_yield >= 4.75:
        macro_score = max(macro_score, 74.0)
    if dxy is not None and ((dxy >= 120.0) or (104.0 <= dxy < 112.0)):
        macro_score = max(macro_score, 72.0)
    if m33.get("macro_headwind_flag"):
        macro_score = max(macro_score, 80.0)
    if macro_score > 0.0:
        _add(16, macro_score, "MOD 16 Macro")

    # MOD 29: Equity / VIX Volatility Shock
    if vix is not None and vix >= 25.0:
        _add(29, min(94.0, 70.0 + (vix - 25.0) * 2.0), "MOD 29 VIX Shock")

    # MOD 19: Coinbase Premium Spread
    if cb_px is not None and bn_px is not None and bn_px > 0:
        cb_prem_bps = ((cb_px - bn_px) / bn_px) * 10000.0
        if abs(cb_prem_bps) >= 8.0:
            sign = "+" if cb_prem_bps > 0 else "-"
            _add(19, min(88.0, 62.0 + abs(cb_prem_bps) * 1.2), f"MOD 19 CB Prem({sign})")

    # MOD 01-04: Derivatives OI / Basis / Funding / Crowding
    if oi_chg is not None and oi_chg <= -5.0:
        _add(3, min(90.0, 66.0 + abs(oi_chg) * 2.0), "MOD 03 OI Flush")
    elif oi_chg is not None and oi_chg >= 4.0 and funding is not None and funding <= -0.005:
        _add(1, 84.0, "MOD 01 Short Sqz")
    elif (oi_chg is not None and oi_chg >= 4.0 and funding is not None and funding >= 0.025) or (
        ls_ratio is not None and ls_ratio >= 2.5
    ):
        _add(2, 82.0, "MOD 02 Long Crowd")
    if funding is not None and abs(funding) >= 0.03:
        _add(4, min(86.0, 70.0 + abs(funding) * 200.0), "MOD 04 Funding")

    # MOD 05: Spot CVD vs Perp CVD Matrix
    if (spot_cvd is not None and abs(spot_cvd) >= 500.0) or (perp_cvd is not None and abs(perp_cvd) >= 5000.0):
        cvd_score = 78.0 if (perp_cvd is not None and abs(perp_cvd) >= 50000.0) else 68.0
        _add(5, cvd_score, "MOD 05 CVD")

    # MOD 13-15: On-Chain & ETF Flow Pressure
    if etf_flow is not None and abs(etf_flow) >= 100.0:
        _add(15, min(85.0, 68.0 + abs(etf_flow) / 50.0), "MOD 15 ETF Flow")
    if fee_sat is not None and fee_sat >= 40.0:
        _add(13, min(80.0, 62.0 + (fee_sat - 40.0) * 0.25), "MOD 13-15 OnChain")

    # MOD 31: ICDM Fragility / Missing Penalty
    icdm_score = _num(m31.get("icdm_score"))
    missing_cnt = _num(m31.get("missing_fields_count")) or 0.0
    if (icdm_score is not None and icdm_score >= 65.0) or missing_cnt >= 4.0:
        _add(31, max(72.0, icdm_score or 0.0), "MOD 31 ICDM")

    # MOD 30: Active PCF3 Router Config (always eligible as execution/stance anchor)
    cfg_id = str(m30.get("config_id") or "").strip()
    if cfg_id:
        cfg_score = 85.0 if m30.get("stance") == "LONG_SPOT" else 65.0
        _add(30, cfg_score, f"MOD 30 PCF3-{cfg_id}")

    ranked = sorted(
        ((score, -mod_num, label) for mod_num, (score, label) in candidates.items()),
        reverse=True,
    )
    selected = [label for _, _, label in ranked[:3]]
    if len(selected) < 2 and cfg_id and f"MOD 30 PCF3-{cfg_id}" not in selected:
        selected.append(f"MOD 30 PCF3-{cfg_id}")
    return selected


def format_hud_card(
    verdict: dict[str, Any],
    metrics: dict[str, Any] | None = None,
) -> str:
    summary = verdict.get("summary") or {}
    m36 = verdict.get("mod36_trust") or {}
    m31 = verdict.get("mod31_icdm") or {}
    m33 = verdict.get("mod33_regime") or {}
    m30 = verdict.get("mod30_pcf3") or {}
    m37 = verdict.get("mod37_risk") or {}
    m18 = verdict.get("mod18_sizing") or {}
    canon = verdict.get("canonical_telemetry") or {}

    action = str(summary.get("verdict_action") or "FLAT_CASH")
    badge_map = {
        "EXECUTE_LONG_SPOT": "🟢 LONG SPOT",
        "HOLD_WATCH": "🟡 WATCH / STANDBY",
        "FLAT_CASH": "⚪ FLAT CASH",
        "LOCKED_HALT": "🔴 HALT / LOCKED",
    }
    badge = badge_map.get(action, f"⚪ {action}")

    spot_str = _fmt_num(summary.get("spot_usd"), prefix="$", decimals=2)
    chg_24h = canon.get("price_change_pct_24h")
    chg_str = f"{chg_24h:+.2f}%" if isinstance(chg_24h, (int, float)) else "N/A"
    myt_time = _format_myt_timestamp(verdict)

    sla_age = m36.get("sla_age_min")
    sla_str = f"{sla_age:.1f}m" if isinstance(sla_age, (int, float)) else "N/A"
    quorum_str = f"{m36.get('quorum_count', 0)}/{len(m36.get('venue_prices') or {}) or 5} (min {m36.get('min_quorum', 3)})"
    disp_str = _fmt_num(m36.get("dispersion_bps"), suffix=" bps", decimals=1)

    icdm_score = _fmt_num(m31.get("icdm_score"), suffix="/100", decimals=1)
    icdm_band = str(m31.get("fragility_band") or "N/A")
    missing_cnt = m31.get("missing_fields_count", 0)
    total_cnt = m31.get("total_factors", 0)

    regime_name = str(m33.get("regime_name") or m33.get("regime_id") or "N/A")
    cfg_id = str(m30.get("config_id") or "?")
    cfg_name = str(m30.get("config_name") or "N/A")

    net_r_str = _fmt_num(m37.get("net_r"), suffix="R", decimals=2)
    cost_str = _fmt_num(m37.get("estimated_cost_bps"), suffix=" bps", decimals=1)
    heat_str = (
        f"{_fmt_num(m37.get('open_portfolio_heat_pct'), suffix='%', decimals=2)}"
        f" / {_fmt_num(m37.get('max_portfolio_heat_pct'), suffix='%', decimals=2)}"
    )
    lock_flag = "TRIGGERED" if m37.get("loss_lock_triggered") else "CLEAR"

    alloc_str = _fmt_num(m18.get("recommended_alloc_pct"), suffix="%", decimals=2)
    qty_str = _fmt_num(m18.get("recommended_btc_qty"), suffix=" BTC", decimals=5)
    entry_str = _fmt_num(m37.get("entry_usd"), prefix="$", decimals=0)
    stop_str = _fmt_num(m37.get("stop_usd"), prefix="$", decimals=0)
    target_str = _fmt_num(m37.get("target_usd"), prefix="$", decimals=0)

    failed_gates = m37.get("failed_gates") or m36.get("gate_reasons") or []
    if failed_gates:
        notes_line = ", ".join(str(x) for x in failed_gates[:4])
    elif action != "EXECUTE_LONG_SPOT" and m30.get("routing_reason"):
        notes_line = str(m30["routing_reason"])
    else:
        notes_line = "All gates nominal"

    active_drivers = extract_active_drivers(verdict, metrics=metrics)
    drivers_line = " + ".join(active_drivers) if active_drivers else "MOD 30 PCF3"

    sha_short = str(verdict.get("determinism_sha256") or "")[:12] or "none"

    lines = [
        f"<b>CORTEX-BTC v3.0</b> | <b>{_esc(badge)}</b>",
        f"🕒 <code>{_esc(myt_time)}</code>",
        f"₿ Spot: <b>{_esc(spot_str)}</b> (24h: <code>{_esc(chg_str)}</code>)",
        "",
        "<b>[MOD 36] Trust &amp; Quorum</b>",
        f"• Status: <b>{_esc(m36.get('trust_status', 'UNKNOWN'))}</b> | Quorum: <code>{_esc(quorum_str)}</code>",
        f"• SLA Age: <code>{_esc(sla_str)}</code> | Disp: <code>{_esc(disp_str)}</code>",
        "",
        "<b>[MOD 31] ICDM Fragility</b>",
        f"• Score: <b>{_esc(icdm_score)}</b> (<code>{_esc(icdm_band)}</code>)",
        f"• Missing Penalty (50%): <code>{_esc(missing_cnt)}/{_esc(total_cnt)}</code> fields",
        "",
        "<b>[MOD 33 / 30] Radar &amp; PCF3 Router</b>",
        f"• Regime: <code>{_esc(regime_name)}</code>",
        f"• Config <b>{_esc(cfg_id)}</b>: {_esc(cfg_name)}",
        "",
        "<b>[MOD 37] Liquidity &amp; Risk Gates</b>",
        f"• Net R: <b>{_esc(net_r_str)}</b> (min 3.0R | Cost: <code>{_esc(cost_str)}</code>)",
        f"• Heat: <code>{_esc(heat_str)}</code> | Locks: <code>{_esc(lock_flag)}</code>",
        f"• Gate Note: <i>{_esc(notes_line)}</i>",
        f"• Active Drivers: <code>{_esc(drivers_line)}</code>",
        "",
        "<b>[MOD 18] 1.0x Spot Sizer</b>",
        f"• Alloc: <b>{_esc(alloc_str)}</b> (<code>{_esc(qty_str)}</code>)",
        f"• Plan: E <code>{_esc(entry_str)}</code> | SL <code>{_esc(stop_str)}</code> | TP <code>{_esc(target_str)}</code>",
        "",
        f"<code>SHA256: {_esc(sha_short)}</code>",
    ]
    return "\n".join(lines)


def send_telegram_message(token: str, chat_id: str, html_text: str) -> dict[str, Any]:
    url = f"{TELEGRAM_API_BASE}/bot{token}/sendMessage"
    payload = json.dumps(
        {
            "chat_id": chat_id,
            "text": html_text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        method="POST",
        headers={"Content-Type": "application/json; charset=utf-8"},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return json.loads(body)
    except urllib.error.HTTPError as exc:
        err_body = exc.read().decode("utf-8", errors="replace")
        safe_msg = err_body.replace(token, "***REDACTED***")
        raise RuntimeError(f"Telegram API HTTP {exc.code}: {safe_msg}") from None
    except urllib.error.URLError as exc:
        safe_reason = str(exc.reason).replace(token, "***REDACTED***")
        raise RuntimeError(f"Telegram network error: {safe_reason}") from None


def main() -> int:
    parser = argparse.ArgumentParser(description="Project CORTEX-BTC Telegram HUD Alert")
    parser.add_argument("--input", type=Path, default=VERDICT_PATH)
    parser.add_argument("--metrics", type=Path, default=METRICS_PATH)
    parser.add_argument("--dry-run", action="store_true", help="Print formatted HTML card without sending.")
    args = parser.parse_args()

    if not args.input.exists():
        raise FileNotFoundError(f"Missing verdict file: {args.input}")

    verdict = json.loads(args.input.read_text(encoding="utf-8"))
    metrics: dict[str, Any] | None = None
    if args.metrics.exists():
        try:
            loaded = json.loads(args.metrics.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                metrics = loaded
        except Exception:
            metrics = None
    html_card = format_hud_card(verdict, metrics=metrics)

    if args.dry_run:
        print(html_card)
        return 0

    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    if not token or not chat_id:
        raise RuntimeError("Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID environment variables.")

    result = send_telegram_message(token=token, chat_id=chat_id, html_text=html_card)
    if not result.get("ok"):
        raise RuntimeError(f"Telegram API returned ok=false: {result}")
    msg_id = (result.get("result") or {}).get("message_id")
    print(f"Telegram HUD sent successfully (message_id={msg_id}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
