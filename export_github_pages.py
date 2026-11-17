#!/usr/bin/env python3
"""
CORTEX-BTC — Static GitHub Pages Read-Only Market Viewer Exporter.

Reads btc_metrics_latest.json (and optionally cortex_verdict_latest.json)
and writes static mobile-friendly files into docs/:
  - docs/market_state.json
  - docs/index.html

Strictly read-only market telemetry only:
- Never reads or exports personal portfolio balances, private keys, or order records.
- Never invents missing metrics or unconfigured thresholds.
- Displays operating time in Malaysia Time (MYT, UTC+8) alongside UTC.
"""

from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path
from typing import Any

from btc_config_loader import initialize_default_config
from cortex_core.constants import DATA_UNAVAILABLE, UNVALIDATED
from cortex_core.market_data import build_market_snapshot
from cortex_core.module_a import evaluate_module_a
from cortex_core.module_b import evaluate_module_b
from cortex_core.time_utils import format_myt, utc_now

PAGES_HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
<title>CORTEX-BTC // Mobile Market Viewer</title>
<style>
  :root {
    --bg: #0b0f17;
    --panel: #121826;
    --panel-alt: #171f30;
    --border: #253047;
    --text: #e6edf7;
    --muted: #8b9bb4;
    --green: #16c784;
    --red: #ea3943;
    --amber: #f5b73b;
    --blue: #5da0ff;
    --mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    --sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Inter, sans-serif;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0; background: var(--bg); color: var(--text);
    font-family: var(--sans); font-size: 14px; line-height: 1.45;
  }
  .wrap { max-width: 1080px; margin: 0 auto; padding: 14px 14px 36px; }
  .header {
    background: var(--panel); border: 1px solid var(--border); border-radius: 12px;
    padding: 14px; margin-bottom: 12px;
  }
  .title-row { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 8px; }
  .title { font-weight: 800; font-size: 17px; letter-spacing: 0.4px; }
  .badges { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 8px; }
  .badge {
    font-family: var(--mono); font-size: 11px; font-weight: 700; padding: 3px 8px;
    border-radius: 999px; border: 1px solid var(--border); background: var(--panel-alt);
  }
  .b-warn { color: var(--amber); border-color: rgba(245, 183, 59, 0.45); background: rgba(245, 183, 59, 0.1); }
  .b-green { color: var(--green); border-color: rgba(22, 199, 132, 0.45); background: rgba(22, 199, 132, 0.1); }
  .b-red { color: var(--red); border-color: rgba(234, 57, 67, 0.45); background: rgba(234, 57, 67, 0.12); }
  .b-blue { color: var(--blue); border-color: rgba(93, 160, 255, 0.45); background: rgba(93, 160, 255, 0.12); }
  .b-muted { color: var(--muted); }
  .card {
    background: var(--panel); border: 1px solid var(--border); border-radius: 12px;
    padding: 14px; margin-bottom: 12px;
  }
  .card h2 {
    margin: 0 0 10px; font-size: 12px; text-transform: uppercase; letter-spacing: 0.7px; color: var(--muted);
  }
  .grid-2 { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }
  .grid-3 { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px; }
  @media (max-width: 780px) { .grid-2, .grid-3 { grid-template-columns: 1fr; } }
  .tile {
    background: var(--panel-alt); border: 1px solid var(--border); border-radius: 9px; padding: 10px 12px;
  }
  .tile-k { font-size: 11px; color: var(--muted); text-transform: uppercase; }
  .tile-v { font-family: var(--mono); font-size: 17px; font-weight: 700; margin-top: 3px; }
  .mono { font-family: var(--mono); }
  .muted { color: var(--muted); }
  .btn {
    background: #2563eb; color: #fff; border: none; border-radius: 8px; padding: 7px 12px;
    font-size: 12px; font-weight: 600; cursor: pointer;
  }
  table { width: 100%; border-collapse: collapse; font-size: 12px; }
  th, td { text-align: left; padding: 7px 6px; border-bottom: 1px solid var(--border); vertical-align: top; }
  th { color: var(--muted); font-size: 11px; text-transform: uppercase; }
  .table-wrap { overflow-x: auto; }
  .st-PASS, .st-VERIFIED, .st-TRUSTED { color: var(--green); font-weight: 700; }
  .st-FAIL, .st-STALE, .st-CONFLICTING, .st-HALT_UNTRUSTED { color: var(--red); font-weight: 700; }
  .st-UNAVAILABLE, .st-NOT\ CONFIGURED { color: var(--amber); font-weight: 700; }
  .st-PROXY, .st-PARTIALLY\ VERIFIED, .st-CONTEXT { color: var(--blue); font-weight: 700; }
</style>
</head>
<body>
<div class="wrap">
  <div class="header">
    <div class="title-row">
      <div>
        <div class="title">CORTEX-BTC // Public Market Viewer</div>
        <div class="muted mono" style="font-size:11px; margin-top:3px;" id="tsLine">Loading...</div>
      </div>
      <button class="btn" onclick="loadLatest()">Reload Latest</button>
    </div>
    <div class="badges" id="badges"></div>
  </div>

  <div class="card">
    <h2>Market Snapshot &amp; Matrix Context</h2>
    <div class="grid-3" id="summaryTiles"></div>
    <div class="muted" style="font-size:12px; margin-top:10px;" id="publicNotice"></div>
  </div>

  <div class="grid-2">
    <div class="card">
      <h2>Module A — Bullish Evidence (Read-Only)</h2>
      <div class="mono" style="font-size:12px; margin-bottom:8px;" id="modASum"></div>
      <div class="table-wrap"><table><thead><tr><th>Check</th><th>Status</th><th>Source</th><th>Detail</th></tr></thead><tbody id="modABody"></tbody></table></div>
    </div>
    <div class="card">
      <h2>Module B — Bearish Evidence (Read-Only)</h2>
      <div class="mono" style="font-size:12px; margin-bottom:8px;" id="modBSum"></div>
      <div class="table-wrap"><table><thead><tr><th>Check</th><th>Status</th><th>Source</th><th>Detail</th></tr></thead><tbody id="modBBody"></tbody></table></div>
    </div>
  </div>

  <div class="card">
    <h2>Cross-Venue Spot Quorum</h2>
    <div class="table-wrap"><table><thead><tr><th>Venue</th><th>Instrument</th><th>Price</th><th>Event Time (MYT)</th><th>Status</th><th>Freshness</th></tr></thead><tbody id="venuesBody"></tbody></table></div>
  </div>

  <div class="card">
    <h2>Full Telemetry Provenance</h2>
    <div class="table-wrap"><table><thead><tr><th>Field</th><th>Value</th><th>Provider</th><th>Instrument</th><th>Event Time (MYT)</th><th>Status</th></tr></thead><tbody id="fieldsBody"></tbody></table></div>
  </div>
</div>

<script id="fallback-state" type="application/json">__FALLBACK_JSON__</script>
<script>
function esc(v) {
  if (v === null || v === undefined) return '';
  return String(v).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

function formatMytNow() {
  const now = new Date();
  const fmt = new Intl.DateTimeFormat('sv-SE', {
    timeZone: 'Asia/Kuala_Lumpur',
    year: 'numeric', month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false
  });
  return fmt.format(now) + ' MYT (UTC+8)';
}

function render(s, liveSpot = null) {
  const b = s.banner;
  const mktMs = Date.parse(b.market_ts_utc);
  const ageMin = Number.isFinite(mktMs) ? Math.max(0, Math.round((Date.now() - mktMs) / 60000)) : null;
  const ageLabel = ageMin === null ? 'AGE: UNKNOWN' : (ageMin > 90 ? `STALE (${ageMin}m > 90m)` : `FRESH (${ageMin}m)`);
  const ageCls = ageMin === null || ageMin > 90 ? 'b-red' : 'b-green';

  document.getElementById('tsLine').textContent =
    `Pipeline Snapshot: ${b.market_ts_myt} | Page Exported: ${b.exported_at_myt}`;

  const integCls = b.data_integrity === 'VERIFIED' ? 'b-green' :
    (['UNAVAILABLE','STALE','CONFLICTING'].includes(b.data_integrity) ? 'b-red' : 'b-warn');
  const spotTxt = typeof b.spot_price_usdt === 'number'
    ? '$' + b.spot_price_usdt.toLocaleString(undefined, {minimumFractionDigits:2, maximumFractionDigits:2})
    : b.spot_price_usdt;
  const liveTxt = liveSpot && typeof liveSpot.price === 'number'
    ? '$' + liveSpot.price.toLocaleString(undefined, {minimumFractionDigits:2, maximumFractionDigits:2})
    : 'CHECKING...';

  document.getElementById('badges').innerHTML = `
    <span class="badge b-blue">${esc(b.instrument)}</span>
    <span class="badge b-warn">${esc(b.validation_status)}</span>
    <span class="badge ${ageCls}">SNAPSHOT: ${esc(ageLabel)}</span>
    <span class="badge ${integCls}">DATA: ${esc(b.data_integrity)}</span>
    <span class="badge b-green">LIVE SPOT: ${esc(liveTxt)}</span>
  `;

  const lv = s.legacy_matrix_summary || {};
  const spotChg = lv.price_change_pct_24h !== null && lv.price_change_pct_24h !== undefined
    ? `${lv.price_change_pct_24h >= 0 ? '+' : ''}${Number(lv.price_change_pct_24h).toFixed(2)}%`
    : 'DATA UNAVAILABLE';
  const liveChg = liveSpot && typeof liveSpot.chgPct === 'number'
    ? `${liveSpot.chgPct >= 0 ? '+' : ''}${liveSpot.chgPct.toFixed(2)}%`
    : '';

  document.getElementById('summaryTiles').innerHTML = `
    <div class="tile"><div class="tile-k">Live Binance Spot (Browser)</div><div class="tile-v">${esc(liveTxt)} <span class="muted" style="font-size:12px;">${esc(liveChg)}</span></div><div class="muted mono" style="font-size:10px; margin-top:3px;">${esc(liveSpot ? liveSpot.timeMyt : '')}</div></div>
    <div class="tile"><div class="tile-k">Pipeline Spot / Regime</div><div class="tile-v" style="font-size:14px;">${esc(spotTxt)} (${esc(spotChg)})</div><div class="muted mono" style="font-size:11px; margin-top:3px;">${esc(lv.regime_id || 'DATA UNAVAILABLE')} | ICDM ${esc(lv.icdm_score ?? 'N/A')}</div></div>
    <div class="tile"><div class="tile-k">Legacy Matrix Action / Net R</div><div class="tile-v" style="font-size:14px;">${esc(lv.verdict_action || 'DATA UNAVAILABLE')} | ${esc(lv.net_r ?? 'N/A')}R</div><div class="muted mono" style="font-size:11px; margin-top:3px;">Snapshot Age: ${esc(ageLabel)}</div></div>
  `;

  document.getElementById('publicNotice').textContent = s.public_notice;

  const ma = s.module_a;
  document.getElementById('modASum').textContent = `State: ${ma.state} | Signal: ${ma.directional_signal} | ${ma.observed_summary}`;
  document.getElementById('modABody').innerHTML = ma.checklist.map(c =>
    `<tr><td class="mono">${esc(c.name)}</td><td class="st-${esc(c.status)}">${esc(c.status)}</td><td class="mono">${esc(c.source_status)}</td><td>${esc(c.rationale)}</td></tr>`
  ).join('');

  const mb = s.module_b;
  document.getElementById('modBSum').textContent = `State: ${mb.state} | Signal: ${mb.directional_signal} | Exit: ${mb.exit_classification || 'NONE'}`;
  document.getElementById('modBBody').innerHTML = mb.checklist.map(c =>
    `<tr><td class="mono">${esc(c.name)}</td><td class="st-${esc(c.status)}">${esc(c.status)}</td><td class="mono">${esc(c.source_status)}</td><td>${esc(c.rationale)}</td></tr>`
  ).join('');

  document.getElementById('venuesBody').innerHTML = Object.entries(s.venues || {}).map(([name, v]) => `
    <tr>
      <td class="mono">${esc(name)}</td>
      <td class="mono">${esc(v.instrument)}</td>
      <td class="mono">${v.price !== null && v.price !== undefined ? '$' + Number(v.price).toLocaleString(undefined,{minimumFractionDigits:2, maximumFractionDigits:2}) : 'DATA UNAVAILABLE'}</td>
      <td class="mono">${esc(v.source_event_ts_myt)}</td>
      <td class="st-${esc(v.validation_status)}">${esc(v.validation_status)}</td>
      <td class="mono">${esc(v.freshness_status)}</td>
    </tr>
  `).join('');

  document.getElementById('fieldsBody').innerHTML = Object.values(s.fields || {}).map(f => `
    <tr>
      <td class="mono">${esc(f.field_name)}</td>
      <td class="mono">${esc(typeof f.display_value === 'object' ? JSON.stringify(f.display_value) : f.display_value)}</td>
      <td class="mono">${esc(f.exchange_or_provider)}</td>
      <td class="mono">${esc(f.instrument)}</td>
      <td class="mono">${esc(f.source_event_ts_myt)}</td>
      <td class="st-${esc(f.validation_status)}">${esc(f.validation_status)}</td>
    </tr>
  `).join('');
}

async function fetchLiveBinanceSpot() {
  try {
    const r = await fetch('https://data-api.binance.vision/api/v3/ticker/24hr?symbol=BTCUSDT', { cache: 'no-store' });
    if (!r.ok) return null;
    const d = await r.json();
    const px = parseFloat(d.lastPrice);
    const chg = parseFloat(d.priceChangePercent);
    if (!Number.isFinite(px)) return null;
    return { price: px, chgPct: Number.isFinite(chg) ? chg : null, timeMyt: formatMytNow() };
  } catch (e) {
    return null;
  }
}

async function loadLatest() {
  let stateObj = null;
  try {
    const resp = await fetch('./market_state.json?ts=' + Date.now(), { cache: 'no-store' });
    if (resp.ok) stateObj = await resp.json();
  } catch (e) {}
  if (!stateObj) {
    stateObj = JSON.parse(document.getElementById('fallback-state').textContent);
  }
  render(stateObj, null);
  const live = await fetchLiveBinanceSpot();
  if (live) render(stateObj, live);
}

loadLatest();
</script>
</body>
</html>
"""


def build_public_market_state(
    *,
    metrics_path: Path = Path("btc_metrics_latest.json"),
    verdict_path: Path = Path("cortex_verdict_latest.json"),
) -> dict[str, Any]:
    """Assemble strictly public, read-only market state with zero personal balances."""
    raw_metrics: dict[str, Any] = {}
    if metrics_path.exists():
        loaded = json.loads(metrics_path.read_text(encoding="utf-8"))
        if isinstance(loaded, dict):
            raw_metrics = loaded

    legacy_verdict: dict[str, Any] = {}
    if verdict_path.exists():
        loaded_v = json.loads(verdict_path.read_text(encoding="utf-8"))
        if isinstance(loaded_v, dict):
            legacy_verdict = loaded_v

    with tempfile.TemporaryDirectory() as td:
        tp = Path(td)
        cfg = initialize_default_config(tp / "cfg.json", tp / "hist.jsonl")

    now_iso = utc_now().strftime("%Y-%m-%dT%H:%M:%SZ")
    mkt = build_market_snapshot(raw_metrics, config=cfg, now_utc=raw_metrics.get("as_of_utc") or now_iso)
    mod_a = evaluate_module_a(mkt, cfg, now_utc=mkt.retrieved_ts_utc)
    mod_b = evaluate_module_b(mkt, cfg, now_utc=mkt.retrieved_ts_utc)

    venues_out: dict[str, Any] = {}
    for vname, vinfo in mkt.venue_prices.items():
        vcopy = dict(vinfo)
        vcopy["source_event_ts_myt"] = format_myt(vinfo.get("source_event_ts_utc"))
        venues_out[vname] = vcopy

    fields_out: dict[str, Any] = {}
    for fname, frec in mkt.fields.items():
        fdict = frec.to_dict()
        fdict["source_event_ts_myt"] = format_myt(frec.source_event_ts_utc)
        fdict["display_value"] = DATA_UNAVAILABLE if frec.value is None else frec.value
        fields_out[fname] = fdict

    lv_summary = legacy_verdict.get("summary") or {}
    lv_canon = legacy_verdict.get("canonical_telemetry") or {}

    return {
        "banner": {
            "system_name": "CORTEX-BTC",
            "instrument": "BTC/USDT SPOT ONLY",
            "validation_status": UNVALIDATED,
            "view_mode": "READ-ONLY PUBLIC PAGES VIEW",
            "spot_price_usdt": mkt.spot_price if mkt.spot_price is not None else DATA_UNAVAILABLE,
            "market_ts_utc": mkt.source_event_ts_utc or DATA_UNAVAILABLE,
            "market_ts_myt": format_myt(mkt.source_event_ts_utc),
            "exported_at_utc": now_iso,
            "exported_at_myt": format_myt(now_iso),
            "data_integrity": mkt.overall_integrity_status.value,
        },
        "public_notice": (
            "Read-only market telemetry view exported by GitHub Actions. "
            "No portfolio balances, private keys, or manual order records are stored or published here. "
            "All strategy outputs remain UNVALIDATED; manual execution only."
        ),
        "legacy_matrix_summary": {
            "verdict_action": lv_summary.get("verdict_action", DATA_UNAVAILABLE),
            "regime_id": lv_summary.get("regime_id", DATA_UNAVAILABLE),
            "icdm_score": lv_summary.get("icdm_score"),
            "fragility_band": lv_summary.get("fragility_band", DATA_UNAVAILABLE),
            "pcf3_config": lv_summary.get("pcf3_config", DATA_UNAVAILABLE),
            "net_r": lv_summary.get("net_r"),
            "price_change_pct_24h": lv_canon.get("price_change_pct_24h"),
            "compiled_at_myt": legacy_verdict.get("compiled_at_myt", DATA_UNAVAILABLE),
        },
        "module_a": mod_a.to_dict(),
        "module_b": mod_b.to_dict(),
        "venues": venues_out,
        "fields": fields_out,
    }


def export_pages(
    *,
    metrics_path: Path = Path("btc_metrics_latest.json"),
    verdict_path: Path = Path("cortex_verdict_latest.json"),
    output_dir: Path = Path("docs"),
) -> tuple[Path, Path]:
    """Generate static docs/market_state.json and docs/index.html."""
    state = build_public_market_state(metrics_path=metrics_path, verdict_path=verdict_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    json_path = output_dir / "market_state.json"
    html_path = output_dir / "index.html"

    state_json = json.dumps(state, indent=2)
    json_path.write_text(state_json, encoding="utf-8")

    # Escape '</' inside embedded script JSON to prevent premature script tag closure
    safe_inline_json = json.dumps(state, separators=(",", ":")).replace("</", "<\\/")
    html_content = PAGES_HTML_TEMPLATE.replace("__FALLBACK_JSON__", safe_inline_json)
    html_path.write_text(html_content, encoding="utf-8")
    return html_path, json_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Export read-only CORTEX-BTC GitHub Pages viewer.")
    parser.add_argument("--metrics", type=Path, default=Path("btc_metrics_latest.json"))
    parser.add_argument("--verdict", type=Path, default=Path("cortex_verdict_latest.json"))
    parser.add_argument("--output-dir", type=Path, default=Path("docs"))
    args = parser.parse_args()

    html_path, json_path = export_pages(
        metrics_path=args.metrics,
        verdict_path=args.verdict,
        output_dir=args.output_dir,
    )
    print(f"Exported {html_path} and {json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
