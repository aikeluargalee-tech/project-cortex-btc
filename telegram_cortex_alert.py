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


def format_hud_card(verdict: dict[str, Any]) -> str:
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
    parser.add_argument("--dry-run", action="store_true", help="Print formatted HTML card without sending.")
    args = parser.parse_args()

    if not args.input.exists():
        raise FileNotFoundError(f"Missing verdict file: {args.input}")

    verdict = json.loads(args.input.read_text(encoding="utf-8"))
    html_card = format_hud_card(verdict)

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
