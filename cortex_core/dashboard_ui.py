"""
Single-screen Unified Command Centre HTML/CSS/JS UI for CORTEX-BTC (Phase 5).
"""

from __future__ import annotations

DASHBOARD_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>CORTEX-BTC // Bidirectional Spot Rotation Command Centre</title>
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
    --blue: #3b82f6;
    --gray: #64748b;
    --mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    --sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Inter, sans-serif;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    background: var(--bg);
    color: var(--text);
    font-family: var(--sans);
    font-size: 14px;
    line-height: 1.45;
  }
  .wrap { max-width: 1420px; margin: 0 auto; padding: 16px 20px 40px; }
  .topbar {
    display: flex; flex-wrap: wrap; gap: 10px; align-items: center; justify-content: space-between;
    background: var(--panel); border: 1px solid var(--border); border-radius: 10px;
    padding: 12px 16px; margin-bottom: 14px;
  }
  .brand { font-weight: 700; font-size: 16px; letter-spacing: 0.4px; }
  .badges { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; }
  .badge {
    display: inline-block; padding: 3px 9px; border-radius: 999px; font-size: 11px;
    font-weight: 700; font-family: var(--mono); border: 1px solid var(--border); background: var(--panel-alt);
  }
  .b-warn { color: var(--amber); border-color: rgba(245, 183, 59, 0.45); background: rgba(245, 183, 59, 0.1); }
  .b-green { color: var(--green); border-color: rgba(22, 199, 132, 0.45); background: rgba(22, 199, 132, 0.1); }
  .b-red { color: var(--red); border-color: rgba(234, 57, 67, 0.45); background: rgba(234, 57, 67, 0.12); }
  .b-blue { color: #7cb3ff; border-color: rgba(59, 130, 246, 0.45); background: rgba(59, 130, 246, 0.12); }
  .b-muted { color: var(--muted); }
  .tabs { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 14px; }
  .tab-btn {
    background: var(--panel); color: var(--muted); border: 1px solid var(--border);
    padding: 8px 14px; border-radius: 8px; cursor: pointer; font-weight: 600; font-size: 13px;
  }
  .tab-btn.active { color: var(--text); border-color: var(--blue); background: rgba(59, 130, 246, 0.15); }
  .tab-pane { display: none; }
  .tab-pane.active { display: block; }
  .card {
    background: var(--panel); border: 1px solid var(--border); border-radius: 10px;
    padding: 14px 16px; margin-bottom: 14px;
  }
  .card h2, .card h3 { margin: 0 0 10px; font-size: 14px; text-transform: uppercase; letter-spacing: 0.6px; color: var(--muted); }
  .grid-2 { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; }
  .grid-4 { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; }
  @media (max-width: 960px) { .grid-2, .grid-4 { grid-template-columns: 1fr; } }
  .hero {
    display: grid; grid-template-columns: 280px 1fr; gap: 16px; align-items: stretch;
  }
  @media (max-width: 860px) { .hero { grid-template-columns: 1fr; } }
  .verdict-box {
    border-radius: 10px; padding: 18px; display: flex; flex-direction: column;
    justify-content: center; align-items: center; text-align: center;
    border: 2px solid var(--border); background: var(--panel-alt);
  }
  .v-BUY { border-color: var(--green); background: rgba(22, 199, 132, 0.1); }
  .v-SELL { border-color: var(--red); background: rgba(234, 57, 67, 0.12); }
  .v-HOLD { border-color: var(--amber); background: rgba(245, 183, 59, 0.08); }
  .v-ABSTAIN { border-color: var(--gray); background: rgba(100, 116, 139, 0.16); }
  .verdict-word { font-size: 36px; font-weight: 800; font-family: var(--mono); letter-spacing: 1px; }
  .kv { display: flex; justify-content: space-between; gap: 8px; padding: 5px 0; border-bottom: 1px solid rgba(255,255,255,0.05); }
  .kv:last-child { border-bottom: none; }
  .k { color: var(--muted); font-size: 12px; }
  .v { font-family: var(--mono); font-size: 13px; text-align: right; }
  .stat-tile { background: var(--panel-alt); border: 1px solid var(--border); border-radius: 8px; padding: 10px 12px; }
  .stat-label { color: var(--muted); font-size: 11px; text-transform: uppercase; }
  .stat-val { font-family: var(--mono); font-size: 16px; font-weight: 700; margin-top: 3px; }
  table { width: 100%; border-collapse: collapse; font-size: 12px; }
  th, td { text-align: left; padding: 7px 8px; border-bottom: 1px solid var(--border); vertical-align: top; }
  th { color: var(--muted); font-weight: 600; font-size: 11px; text-transform: uppercase; }
  .mono { font-family: var(--mono); }
  .btn {
    background: var(--blue); color: #fff; border: none; border-radius: 7px;
    padding: 7px 12px; font-size: 12px; font-weight: 600; cursor: pointer;
  }
  .btn-sec { background: var(--panel-alt); color: var(--text); border: 1px solid var(--border); }
  .btn-warn { background: rgba(245, 183, 59, 0.2); color: var(--amber); border: 1px solid rgba(245, 183, 59, 0.5); }
  .btn-red { background: rgba(234, 57, 67, 0.2); color: #ff8e94; border: 1px solid rgba(234, 57, 67, 0.5); }
  .btn:disabled { opacity: 0.45; cursor: not-allowed; }
  .form-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 8px; margin-bottom: 8px; }
  input, select, textarea {
    width: 100%; background: var(--bg); color: var(--text); border: 1px solid var(--border);
    border-radius: 6px; padding: 7px 9px; font-family: var(--mono); font-size: 12px;
  }
  .notice { padding: 8px 12px; border-radius: 7px; font-size: 12px; margin-top: 8px; border: 1px solid var(--border); background: var(--panel-alt); }
  .st-PASS { color: var(--green); font-weight: 700; }
  .st-FAIL, .st-STALE, .st-CONFLICTING { color: var(--red); font-weight: 700; }
  .st-UNAVAILABLE, .st-NOT\ CONFIGURED { color: var(--amber); font-weight: 700; }
  .st-PROXY, .st-PARTIALLY\ VERIFIED, .st-CONTEXT { color: #7cb3ff; font-weight: 700; }
</style>
</head>
<body>
<div class="wrap">
  <div class="topbar">
    <div>
      <div class="brand">CORTEX-BTC // Bidirectional Spot Portfolio Decision System</div>
      <div class="b-muted mono" style="font-size:11px; margin-top:2px;" id="tsLine">Loading timestamps...</div>
    </div>
    <div class="badges" id="bannerBadges"></div>
    <div style="display:flex; gap:8px; align-items:center;">
      <button class="btn" onclick="refreshState(false)">Refresh Decision</button>
    </div>
  </div>

  <div class="tabs">
    <button class="tab-btn active" onclick="showTab('cmd', this)">1. Command Centre</button>
    <button class="tab-btn" onclick="showTab('port', this)">2. Portfolio, Orders &amp; Cycles</button>
    <button class="tab-btn" onclick="showTab('tel', this)">3. Telemetry &amp; Provenance</button>
    <button class="tab-btn" onclick="showTab('cfg', this)">4. Config &amp; Audit Trail</button>
  </div>

  <!-- TAB 1: COMMAND CENTRE -->
  <div id="tab-cmd" class="tab-pane active">
    <div class="card hero">
      <div class="verdict-box" id="verdictBox">
        <div class="b-muted" style="font-size:11px; text-transform:uppercase;">Module D Final Verdict</div>
        <div class="verdict-word" id="verdictWord">--</div>
        <div class="mono" style="font-size:12px; margin-top:6px;" id="opStateBadge">--</div>
        <div class="b-muted mono" style="font-size:11px; margin-top:6px;" id="regimeBadge">--</div>
      </div>
      <div>
        <h2>Decision &amp; Plain-English Rationale</h2>
        <div id="plainSummary" style="font-size:14px; margin-bottom:10px;">Loading...</div>
        <div class="grid-4" id="portfolioTiles"></div>
        <div id="proposedOrderBox" class="notice" style="display:none; margin-top:10px;"></div>
      </div>
    </div>

    <div class="grid-2">
      <div class="card">
        <h2>Module A — Bullish: Accumulation &amp; Reversal <span class="badge b-muted">NO EXECUTION AUTHORITY</span></h2>
        <div id="modASummary" class="mono" style="font-size:12px; margin-bottom:8px;"></div>
        <table><thead><tr><th>Evidence Check</th><th>Status</th><th>Source</th><th>Rationale</th></tr></thead><tbody id="modABody"></tbody></table>
      </div>
      <div class="card">
        <h2>Module B — Bearish: Distribution &amp; Breakdown <span class="badge b-muted">NO EXECUTION AUTHORITY</span></h2>
        <div id="modBSummary" class="mono" style="font-size:12px; margin-bottom:8px;"></div>
        <div id="modBMechanisms" class="notice" style="margin-bottom:8px;"></div>
        <table><thead><tr><th>Evidence Check</th><th>Status</th><th>Source</th><th>Rationale</th></tr></thead><tbody id="modBBody"></tbody></table>
      </div>
    </div>

    <div class="card">
      <h2>Module C &amp; Module D — 10-Gate Deterministic Reconciliation</h2>
      <div id="allocSummary" class="mono" style="font-size:12px; margin-bottom:10px;"></div>
      <table><thead><tr><th>#</th><th>Gate</th><th>Status</th><th>Summary</th></tr></thead><tbody id="gatesBody"></tbody></table>
    </div>
  </div>

  <!-- TAB 2: PORTFOLIO, ORDERS & CYCLES -->
  <div id="tab-port" class="tab-pane">
    <div class="grid-2">
      <div class="card">
        <h2>Configure Verified Spot Balances</h2>
        <div class="form-row">
          <div><label class="k">Core Protected BTC (Sleeve B)</label><input id="inCoreBtc" type="number" step="0.00000001" placeholder="0.80" /></div>
          <div><label class="k">Tactical BTC (Sleeve A)</label><input id="inTacBtc" type="number" step="0.00000001" placeholder="0.10" /></div>
          <div><label class="k">Tactical USDT (Sleeve A)</label><input id="inTacUsdt" type="number" step="0.01" placeholder="5000.00" /></div>
        </div>
        <div class="form-row">
          <div><label class="k">Operator ID</label><input id="inBalOp" placeholder="operator" /></div>
          <div><label class="k">Reason</label><input id="inBalReason" placeholder="Manual wallet verification" /></div>
        </div>
        <button class="btn" onclick="submitBalances()">Save Verified Balances</button>
        <div id="balFeedback" class="notice" style="display:none;"></div>
      </div>

      <div class="card">
        <h2>Reconcile Against External Exchange Balances</h2>
        <div class="form-row">
          <div><label class="k">Reported Total BTC</label><input id="inRecBtc" type="number" step="0.00000001" /></div>
          <div><label class="k">Reported Total USDT</label><input id="inRecUsdt" type="number" step="0.01" /></div>
          <div><label class="k">Source</label><input id="inRecSource" value="manual_exchange_check" /></div>
        </div>
        <button class="btn btn-sec" onclick="submitReconcile()">Run Reconciliation Check</button>
        <div id="recFeedback" class="notice" style="display:none;"></div>
      </div>
    </div>

    <div class="card">
      <h2>Unified Order Lifecycle (Manual Execution Only)</h2>
      <table>
        <thead><tr><th>Order ID</th><th>Loop / Side</th><th>Limit Px</th><th>Qty BTC</th><th>Filled</th><th>Reserved</th><th>Status</th><th>Updated (MYT)</th><th>Manual Actions</th></tr></thead>
        <tbody id="ordersBody"></tbody>
      </table>
      <div id="orderFeedback" class="notice" style="display:none;"></div>
    </div>

    <div class="card">
      <h2>DIBSE Conversion Cycles (Loop A: Net USDT | Loop B: ΔBTC)</h2>
      <div class="form-row" style="max-width:650px;">
        <select id="inCycLoop"><option value="LOOP_A">LOOP_A (USDT → BTC → USDT)</option><option value="LOOP_B">LOOP_B (BTC → USDT → BTC)</option></select>
        <input id="inCycQty" type="number" step="0.00000001" placeholder="Starting qty" />
        <input id="inCycRef" placeholder="Setup ref" value="MANUAL_CYCLE" />
        <button class="btn btn-sec" onclick="openCycle()">Open Cycle</button>
      </div>
      <table>
        <thead><tr><th>Cycle ID</th><th>Loop</th><th>Start</th><th>Entry Fill</th><th>Exit Fill</th><th>Fees</th><th>Realised Result</th><th>Status</th></tr></thead>
        <tbody id="cyclesBody"></tbody>
      </table>
    </div>
  </div>

  <!-- TAB 3: TELEMETRY & PROVENANCE -->
  <div id="tab-tel" class="tab-pane">
    <div class="card">
      <h2>Market Telemetry &amp; Data Classification</h2>
      <table>
        <thead><tr><th>Field</th><th>Value</th><th>Instrument</th><th>Source</th><th>Event Time (MYT)</th><th>Status</th><th>Freshness</th><th>Notes</th></tr></thead>
        <tbody id="telBody"></tbody>
      </table>
    </div>
  </div>

  <!-- TAB 4: CONFIG & AUDIT TRAIL -->
  <div id="tab-cfg" class="tab-pane">
    <div class="grid-2">
      <div class="card">
        <h2>Controlled Configuration Update (JSON Patch)</h2>
        <div class="b-muted" style="font-size:12px; margin-bottom:8px;">
          Unestablished parameters stay <span class="mono">NOT CONFIGURED</span>. Invariants (spot-only, no leverage, manual execution) cannot be disabled.
        </div>
        <textarea id="inCfgJson" rows="10">{
  "data_policy": { "spot_price_max_age_minutes": 90, "spot_cvd_max_age_minutes": 90 },
  "portfolio_policy": { "active_tactical_sleeve_pct": 20.0, "portfolio_risk_budget_pct": 0.75 },
  "execution_assumptions": { "maker_fee_bps": 10.0, "expected_slippage_bps": 5.0 }
}</textarea>
        <div class="form-row" style="margin-top:8px;">
          <input id="inCfgOp" placeholder="Operator ID" />
          <input id="inCfgReason" placeholder="Reason for parameter update" />
        </div>
        <label style="display:flex; gap:8px; align-items:center; font-size:12px; margin:8px 0;">
          <input id="inCfgAck" type="checkbox" style="width:auto;" /> I acknowledge this audited configuration version change.
        </label>
        <button class="btn" onclick="submitConfig()">Apply Versioned Update</button>
        <div id="cfgFeedback" class="notice" style="display:none;"></div>
      </div>

      <div class="card">
        <h2>Active Configuration Snapshot</h2>
        <pre id="cfgCurrent" class="mono" style="font-size:11px; white-space:pre-wrap; max-height:330px; overflow:auto;"></pre>
      </div>
    </div>

    <div class="card">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
        <h2 style="margin:0;">Audit &amp; Decision Trail</h2>
        <div style="display:flex; gap:8px;">
          <a class="btn btn-sec" href="/api/export/csv" style="text-decoration:none;">Export CSV</a>
          <a class="btn btn-sec" href="/api/export/json" style="text-decoration:none;">Export JSON</a>
        </div>
      </div>
      <table>
        <thead><tr><th>Event ID</th><th>Type</th><th>Time (MYT)</th><th>Actor</th><th>Summary</th></tr></thead>
        <tbody id="auditBody"></tbody>
      </table>
    </div>
  </div>
</div>

<script>
let CURRENT_STATE = null;

function esc(v) {
  if (v === null || v === undefined) return '';
  return String(v)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;')
    .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function showTab(id, btn) {
  document.querySelectorAll('.tab-pane').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
  document.getElementById('tab-' + id).classList.add('active');
  if (btn) btn.classList.add('active');
}

async function api(url, method = 'GET', body = null) {
  const opts = { method, headers: {} };
  if (body !== null) {
    opts.headers['Content-Type'] = 'application/json';
    opts.body = JSON.stringify(body);
  }
  const resp = await fetch(url, opts);
  const data = await resp.json();
  if (!resp.ok) throw new Error(data.error || ('HTTP ' + resp.status));
  return data;
}

function showNotice(elId, msg, ok = true) {
  const el = document.getElementById(elId);
  el.style.display = 'block';
  el.style.borderColor = ok ? 'rgba(22,199,132,0.5)' : 'rgba(234,57,67,0.6)';
  el.textContent = msg;
}

function renderState(s) {
  CURRENT_STATE = s;
  const b = s.banner;
  const d = s.decision;
  const p = s.portfolio_display;

  document.getElementById('tsLine').textContent =
    `Market Event: ${b.market_ts_myt} (UTC: ${b.market_ts_utc}) | Updated: ${b.last_update_myt}`;

  const integClass = b.data_integrity === 'VERIFIED' ? 'b-green' :
    (b.data_integrity === 'UNAVAILABLE' || b.data_integrity === 'STALE' || b.data_integrity === 'CONFLICTING' ? 'b-red' : 'b-warn');

  const spotTxt = typeof b.spot_price_usdt === 'number' ? '$' + b.spot_price_usdt.toLocaleString(undefined, {minimumFractionDigits:2, maximumFractionDigits:2}) : b.spot_price_usdt;

  document.getElementById('bannerBadges').innerHTML = `
    <span class="badge b-blue">${esc(b.instrument)}</span>
    <span class="badge b-warn">${esc(b.validation_status)}</span>
    <span class="badge b-muted">${esc(b.operating_mode)}</span>
    <span class="badge b-muted">${esc(b.execution_mode)}</span>
    <span class="badge ${integClass}">DATA: ${esc(b.data_integrity)}</span>
    <span class="badge b-green">BTC: ${esc(spotTxt)}</span>
  `;

  const vbox = document.getElementById('verdictBox');
  vbox.className = 'verdict-box v-' + d.final_verdict;
  document.getElementById('verdictWord').textContent = d.final_verdict;
  document.getElementById('opStateBadge').textContent = 'STATE: ' + d.new_operating_state;
  document.getElementById('regimeBadge').textContent = 'REGIME: ' + d.regime_label + ' | CFG v' + d.config_version;
  document.getElementById('plainSummary').textContent = d.plain_english_summary;

  const fmtVal = (val, suffix='') => (typeof val === 'number' ? val.toLocaleString(undefined, {maximumFractionDigits:6}) + suffix : String(val));
  document.getElementById('portfolioTiles').innerHTML = `
    <div class="stat-tile"><div class="stat-label">Total Portfolio (USDT)</div><div class="stat-val">${esc(fmtVal(p.total_portfolio_value_usdt))}</div></div>
    <div class="stat-tile"><div class="stat-label">Tactical BTC / Avail</div><div class="stat-val">${esc(fmtVal(p.btc_tactical))} / ${esc(fmtVal(p.btc_tactical_available))}</div></div>
    <div class="stat-tile"><div class="stat-label">Tactical USDT / Avail</div><div class="stat-val">${esc(fmtVal(p.usdt_tactical))} / ${esc(fmtVal(p.usdt_tactical_available))}</div></div>
    <div class="stat-tile"><div class="stat-label">Protected Core BTC (Sleeve B)</div><div class="stat-val">${esc(fmtVal(p.btc_core_protected))}</div></div>
  `;

  const poBox = document.getElementById('proposedOrderBox');
  if (d.proposed_order) {
    const po = d.proposed_order;
    poBox.style.display = 'block';
    poBox.innerHTML = `
      <strong>PROPOSED LIMIT ${esc(po.side)} (${esc(po.loop)}):</strong>
      ${esc(po.quantity_btc)} BTC @ $${esc(po.limit_price)} USDT
      | ${esc(po.execution_note)}
      <button class="btn" style="margin-left:10px;" onclick="refreshState(true)">Create Proposed Order Ticket in Ledger</button>
    `;
  } else {
    poBox.style.display = 'none';
  }

  // Module A & B
  const ma = s.module_a;
  document.getElementById('modASummary').textContent = `State: ${ma.state} | Signal: ${ma.directional_signal} | ${ma.observed_summary}`;
  document.getElementById('modABody').innerHTML = ma.checklist.map(c => `
    <tr><td class="mono">${esc(c.name)}</td><td class="st-${esc(c.status)}">${esc(c.status)}</td><td class="mono">${esc(c.source_status)}</td><td>${esc(c.rationale)}</td></tr>
  `).join('');

  const mb = s.module_b;
  document.getElementById('modBSummary').textContent =
    `State: ${mb.state} | Signal: ${mb.directional_signal} | Exit: ${mb.exit_classification || 'NONE'} | Pattern: ${mb.bearish_pattern || 'NONE'}`;
  const mechs = Object.entries(mb.mechanism_evaluations || {}).map(([k, v]) =>
    `<strong>${esc(k)}</strong>: <span class="st-${esc(v.status)}">${esc(v.status)}</span> (${esc(v.rationale)})`
  ).join('<br/>');
  document.getElementById('modBMechanisms').innerHTML = mechs || 'No mechanism data.';
  document.getElementById('modBBody').innerHTML = mb.checklist.map(c => `
    <tr><td class="mono">${esc(c.name)}</td><td class="st-${esc(c.status)}">${esc(c.status)}</td><td class="mono">${esc(c.source_status)}</td><td>${esc(c.rationale)}</td></tr>
  `).join('');

  // Allocation & Gates
  const al = s.allocation;
  document.getElementById('allocSummary').textContent =
    `Permitted Side: ${al.permitted_side} | Qty: ${al.permitted_quantity_btc} BTC | Limiting Constraint: ${al.limiting_constraint_name} | Exposure Band: BTC ${al.permitted_exposure_band.btc_pct}% / USDT ${al.permitted_exposure_band.usdt_pct}% | Recon: ${p.reconciliation_status}`;
  document.getElementById('gatesBody').innerHTML = d.gates.map(g => `
    <tr><td class="mono">${g.gate_number}</td><td><strong>${esc(g.gate_name)}</strong></td><td class="st-${esc(g.status)}">${esc(g.status)}</td><td>${esc(g.summary)}</td></tr>
  `).join('');

  // Orders
  document.getElementById('ordersBody').innerHTML = (s.orders || []).map(o => `
    <tr>
      <td class="mono">${esc(o.order_id)}</td>
      <td class="mono">${esc(o.loop)} / ${esc(o.side)}</td>
      <td class="mono">$${esc(o.limit_price)}</td>
      <td class="mono">${esc(o.requested_qty_btc)}</td>
      <td class="mono">${esc(o.filled_qty_btc)}</td>
      <td class="mono">${esc(o.remaining_reserved_amount)} ${esc(o.reserved_asset)}</td>
      <td class="mono">${esc(o.status)}</td>
      <td class="mono">${esc(o.updated_at_myt)}</td>
      <td>
        ${o.status === 'PROPOSED' ? `<button class="btn" onclick="orderAction('${esc(o.order_id)}','APPROVE')">Approve</button>` : ''}
        ${o.status === 'APPROVED' ? `<button class="btn btn-sec" onclick="promptSubmit('${esc(o.order_id)}')">Mark Submitted</button>` : ''}
        ${['APPROVED','SUBMITTED','WORKING','PARTIALLY FILLED'].includes(o.status) ? `<button class="btn btn-warn" onclick="promptFill('${esc(o.order_id)}', ${o.limit_price})">Record Fill</button>` : ''}
        ${['PROPOSED','APPROVED','SUBMITTED','WORKING','PARTIALLY FILLED'].includes(o.status) ? `<button class="btn btn-red" onclick="orderAction('${esc(o.order_id)}','CANCELLED')">Confirm Cancel</button>` : ''}
      </td>
    </tr>
  `).join('') || '<tr><td colspan="9" class="b-muted">No orders recorded.</td></tr>';

  // Cycles
  document.getElementById('cyclesBody').innerHTML = (s.cycles || []).map(c => `
    <tr>
      <td class="mono">${esc(c.cycle_id)}</td>
      <td class="mono">${esc(c.loop)}</td>
      <td class="mono">${esc(c.starting_qty)} ${esc(c.starting_asset)}</td>
      <td class="mono">${esc(c.entry_filled_btc)} BTC / $${esc(c.entry_filled_usdt)}</td>
      <td class="mono">${esc(c.exit_filled_btc)} BTC / $${esc(c.exit_filled_usdt)}</td>
      <td class="mono">$${esc(c.total_fees_usdt)} | ${esc(c.total_fees_btc)} BTC</td>
      <td class="mono">${c.loop === 'LOOP_A' ? (c.realised_net_usdt !== null ? '$' + c.realised_net_usdt : 'OPEN') : (c.delta_btc !== null ? c.delta_btc + ' BTC' : 'OPEN')}</td>
      <td class="mono">${esc(c.status)}</td>
    </tr>
  `).join('') || '<tr><td colspan="8" class="b-muted">No conversion cycles opened.</td></tr>';

  // Telemetry
  const fields = Object.values(s.market_snapshot.fields || {});
  document.getElementById('telBody').innerHTML = fields.map(f => `
    <tr>
      <td class="mono">${esc(f.field_name)}</td>
      <td class="mono">${esc(typeof f.display_value === 'object' ? JSON.stringify(f.display_value) : f.display_value)}</td>
      <td class="mono">${esc(f.instrument)}</td>
      <td class="mono">${esc(f.exchange_or_provider)}</td>
      <td class="mono">${esc(f.source_event_ts_myt)}</td>
      <td class="st-${esc(f.validation_status)}">${esc(f.validation_status)}</td>
      <td class="mono">${esc(f.freshness_status)}</td>
      <td>${esc(f.notes)}</td>
    </tr>
  `).join('');

  // Config & Audit
  document.getElementById('cfgCurrent').textContent = JSON.stringify(s.config, null, 2);
  document.getElementById('auditBody').innerHTML = (s.audit_events || []).map(ev => `
    <tr><td class="mono">${esc(ev.event_id)}</td><td class="mono">${esc(ev.event_type)}</td><td class="mono">${esc(ev.timestamp_myt)}</td><td class="mono">${esc(ev.actor)}</td><td>${esc(ev.summary)}</td></tr>
  `).join('');
}

async function refreshState(createOrder = false) {
  const data = await api('/api/state' + (createOrder ? '?propose=1' : ''));
  renderState(data);
}

async function submitBalances() {
  try {
    await api('/api/portfolio/configure', 'POST', {
      btc_core_protected: parseFloat(document.getElementById('inCoreBtc').value),
      btc_tactical: parseFloat(document.getElementById('inTacBtc').value),
      usdt_tactical: parseFloat(document.getElementById('inTacUsdt').value),
      operator_id: document.getElementById('inBalOp').value,
      reason: document.getElementById('inBalReason').value,
    });
    showNotice('balFeedback', 'Balances verified & saved.', true);
    await refreshState(false);
  } catch (e) { showNotice('balFeedback', e.message, false); }
}

async function submitReconcile() {
  try {
    const res = await api('/api/portfolio/reconcile', 'POST', {
      reported_btc_total: parseFloat(document.getElementById('inRecBtc').value),
      reported_usdt_total: parseFloat(document.getElementById('inRecUsdt').value),
      source: document.getElementById('inRecSource').value,
    });
    showNotice('recFeedback', `${res.reconciliation_status}: ${res.notes}`, res.reconciliation_status === 'RECONCILED');
    await refreshState(false);
  } catch (e) { showNotice('recFeedback', e.message, false); }
}

async function orderAction(orderId, action, extra = {}) {
  try {
    await api('/api/orders/action', 'POST', { order_id: orderId, action, operator_id: 'operator', ...extra });
    showNotice('orderFeedback', `Order ${orderId} updated (${action}).`, true);
    await refreshState(false);
  } catch (e) { showNotice('orderFeedback', e.message, false); }
}

function promptSubmit(orderId) {
  const ref = prompt('Enter external exchange order reference:');
  if (ref) orderAction(orderId, 'SUBMIT', { exchange_order_ref: ref });
}

function promptFill(orderId, defaultPx) {
  const qty = parseFloat(prompt('Enter filled BTC quantity:'));
  const px = parseFloat(prompt('Enter actual fill price (USDT):', String(defaultPx)));
  const fee = parseFloat(prompt('Enter actual fee (USDT):', '0'));
  if (!isNaN(qty) && !isNaN(px)) {
    orderAction(orderId, 'FILL', { fill_qty_btc: qty, fill_price_usdt: px, fee_asset: 'USDT', fee_amount: isNaN(fee) ? 0 : fee });
  }
}

async function openCycle() {
  await api('/api/cycles/open', 'POST', {
    loop: document.getElementById('inCycLoop').value,
    starting_qty: parseFloat(document.getElementById('inCycQty').value),
    original_setup_ref: document.getElementById('inCycRef').value,
  });
  await refreshState(false);
}

async function submitConfig() {
  try {
    const updates = JSON.parse(document.getElementById('inCfgJson').value);
    await api('/api/config/update', 'POST', {
      updates,
      operator_id: document.getElementById('inCfgOp').value,
      change_reason: document.getElementById('inCfgReason').value,
      operator_acknowledged: document.getElementById('inCfgAck').checked,
    });
    showNotice('cfgFeedback', 'Configuration version updated and audited.', true);
    await refreshState(false);
  } catch (e) { showNotice('cfgFeedback', e.message, false); }
}

refreshState(false);
</script>
</body>
</html>
"""
