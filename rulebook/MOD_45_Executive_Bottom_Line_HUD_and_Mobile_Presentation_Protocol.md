# PROJECT CORTEX-BTC — MODULE 45: EXECUTIVE BOTTOM-LINE HUD & MOBILE PRESENTATION PROTOCOL
**Waterfall Tier:** Tier D (Control-Plane, Output Rendering & Mobile Operator Interface) — governs all Telegram HUD alerts, Hermes Agent responses, GitHub Actions hourly pings, and executive market briefings across Pillars 1–5.
**Empirical Benchmark Anchor:** Codified from the November 15, 2026 BTC Bottom-Line HUD cockpit (mobile-first Samsung Galaxy A55 / Telegram layout) integrated with `MOD 36` Zero-Hallucination (`DATA UNAVAILABLE`) attestation, `MOD 18` `0.75%` spot-only sizing, and `MOD 44` calendar-event gates.

---

## 1. Machine-Readable State & Routing Block (Python / Hermes / NotebookLM Index)

```yaml
module_id: "MOD_45"
entry_type: "OUTPUT_RENDERING_AND_HUD_STANDARD"
waterfall_pillar: "TIER_D_OPERATOR_INTERFACE"
title: "Executive Bottom-Line HUD & Mobile Presentation Protocol"

# INTERFACE & DELIVERY SPECIFICATIONS
delivery_parameters:
  primary_screen_target: "Samsung Galaxy A55 / Telegram Mobile Viewport (No horizontal scrolling)"
  default_timezone: "Asia/Kuala_Lumpur (MYT / UTC+8)"
  price_denomination: "USD primary with optional MYR equivalent"
  default_template: "TEMPLATE_45A_BOTTOM_LINE_HUD"
  hourly_cron_template: "TEMPLATE_45B_COMPACT_HEARTBEAT"
  strike_alert_template: "TEMPLATE_45C_EXECUTION_STRIKE_HUD"

# MANDATORY HUD SECTIONS (IN EXACT ORDER)
required_sections:
  1_header: "Title + Date + Timestamp (MYT)"
  2_regime_badge: "Two-Word Market Regime (e.g., BEARISH / DELEVERAGING or BULLISH / SPOT-LED EXPANSION) + MOD 33 State"
  3_price_ticker: "BTC Spot Price (USD / MYR) + 24H % Change"
  4_telemetry_bullets: "7-8 raw, non-interpolated telemetry metrics (OI, Liquidations, Futures vs Spot CVD, Funding/CB Prem, US Spot ETFs, Fear & Greed, Calendar Gate)"
  5_decision_banner: "Explicit Spot Posture (WAIT — HOLD USDT / 100% CASH LOCK vs. DEPLOY 0.75% SPOT RISK)"
  6_three_conclusions: "Exactly 3 numbered, high-signal conclusions (explicitly labeling unconfirmed bottoms/tops as DATA UNAVAILABLE per MOD 36)"
  7_flip_triggers: "Checklist of exact telemetry conditions required to change the decision"
  8_final_verdict: "One-sentence capital-preservation or execution mandate"

# ANTI-TRAP CIRCUIT BREAKERS
circuit_breakers:
  CB_01_ZERO_NARRATIVE_BLOAT: "NEVER output multi-paragraph essays, rhetorical filler, or speculative storytelling in operational briefings. Every line must be scannable on a mobile screen in under 15 seconds."
  CB_02_DATA_UNAVAILABLE_HONESTY: "Per MOD 36, if a confirmed bottom, top, or missing feed cannot be verified from live telemetry, explicitly print 'DATA UNAVAILABLE' rather than guessing price targets."
  CB_03_ACTION_FIRST_CLARITY: "Every HUD card MUST state an unambiguous binary posture (100% CASH LOCK / HOLD USDT vs. AUTHORIZED 0.75% SPOT ENTRY) before listing conclusions."
  CB_04_RULEBOOK_GROUNDING: "Every flip trigger and conclusion must map directly to active CORTEX-BTC rules (MOD 01–44), enforcing 1.0x Spot Only and <= 0.75% max equity risk."

# RISK & SIZING CONSTANTS (PILLAR 4)
risk_parameters:
  max_portfolio_risk_pct: 0.75
  leverage_permitted: 1.0 # Strict Unleveraged Spot Only
```

---

## 2. Protective Circuit Breakers (Mandatory Output & Formatting Invariants)

* **Circuit Breaker 1 — Zero Narrative Bloat (`CB-01`):** Mobile execution fails when critical risk signals are buried inside prose paragraphs. All briefings and Telegram HUD cards must use clean visual dividers, bold regime badges, and compact bullet points readable on a single mobile viewport.
* **Circuit Breaker 2 — Strict `DATA UNAVAILABLE` Honesty (`CB-02`):** Never fabricate support floors, cycle bottoms, or missing exchange feeds. Whenever structural bottom/top confirmation is absent or an API feed lags (`MOD 36`), print **`DATA UNAVAILABLE`** explicitly.
* **Circuit Breaker 3 — Action-First Decision Banner (`CB-03`):** Immediately below the 7-bullet telemetry block, display a high-contrast **`DECISION`** banner (`WAIT — HOLD USDT (100% CASH LOCK)` or `DEPLOY 0.75% SPOT RISK`) so there is zero ambiguity during fast markets.
* **Circuit Breaker 4 — Explicit Flip Triggers & Rule Citations (`CB-04`):** Never leave a defensive or bullish call open-ended. Always include the **`WHAT WOULD CHANGE MY DECISION / UNLOCKS RISK`** section listing the exact measurable telemetry shifts (`US Spot ETFs`, `Domestic USD Spot CVD`, `OI stabilization`, `4H VAH reclaim`, `MOD 44` calendar clearance) required to flip posture.

---

## 3. Canonical Bottom-Line HUD Templates (Reference Specifications)

### Template 45A: Standard Executive Bottom-Line HUD Card (Default Reference)
Use this exact layout whenever generating a daily morning brief, on-demand market analysis, or regime-shift summary:

```text
BTC BOTTOM LINE — <DD MONTH YYYY> | <HH:MM MYT>
━━━━━━━━━━━━━━━━━━━━━━
MARKET REGIME
<PRIMARY_BIAS> / <MECHANICAL_STATE> (MOD 33: <REGIME_CODE>)
BTC: $<PRICE_USD> (RM <PRICE_MYR>) | 24H: <PCT_CHANGE>%
━━━━━━━━━━━━━━━━━━━━━━
• Open Interest: <OI_24H_PCT>% (<STATE_TAG>)
• Liquidations: $<LIQ_TOTAL> (<LONG_PCT>% longs / <SHORT_PCT>% shorts)
• Futures net flow: <FUTURES_CVD_DELTA>
• Spot net flow: <SPOT_CVD_DELTA>
• Funding / CB Prem: <FUNDING_STATE> | <CB_PREM_STATE>
• US Spot ETF flows: <ETF_DAILY_NET> (<STREAK_CONTEXT>)
• Fear & Greed: <FNG_SCORE> (<FNG_LABEL>)
• Calendar Gate: <MOD_44_OR_MACRO_STATUS>

SPOT TRADING DECISION
• <POSTURE_BADGE> (e.g., WAIT — HOLD USDT | 100% CASH LOCK | 0.00% RISK)
• <ONE_LINE_OPERATIONAL_DIRECTIVE>

THREE IMPORTANT CONCLUSIONS:
1. <CONCLUSION_1_FLOW_REALITY>
2. <CONCLUSION_2_BOTTOM_OR_TOP_STATUS_WITH_DATA_UNAVAILABLE_DISCIPLINE>
3. <CONCLUSION_3_TRAP_WARNING_OR_STRUCTURAL_EDGE>

WHAT WOULD CHANGE MY DECISION?
<EXACT_TELEMETRY_FLIP_CONDITIONS_WITH_MOD_REFERENCES>

FINAL VERDICT: <ONE_SENTENCE_DISCIPLINED_MANDATE>
```

#### Canonical Live Reference Instance (November 15, 2026 Benchmark)
```text
BTC BOTTOM LINE — 15 NOVEMBER 2026 | 09:55 MYT
━━━━━━━━━━━━━━━━━━━━━━
MARKET REGIME
BEARISH / DELEVERAGING (MOD 33: R4)
BTC: $62,268.50 (RM 254,784) | 24H: −8.86%
━━━━━━━━━━━━━━━━━━━━━━
• Open Interest: −9.10% (forced deleveraging flush)
• Liquidations: $819.62M (92% longs)
• Futures net selling: −$2.4B (period table)
• Spot net selling: −$441M (Quad 4 aligned outflow)
• Funding / CB Prem: Slightly negative | CB Prem < 0
• US Spot ETF flows: −$185.4M (7-day outflow streak; −$1.91B)
• Fear & Greed: 11 (Extreme Fear)
• Calendar Gate: MOD 44 ACTIVE (ANT Nov 19 + MSCI Nov 30)

SPOT TRADING DECISION
• WAIT — HOLD USDT (100% CASH LOCK | 0.00% RISK)
• No fresh BTC buying until spot demand, ETF flows, and 4H market structure confirm recovery.

THREE IMPORTANT CONCLUSIONS:
1. Selling pressure is broad-based (spot + futures Quad 4), not merely derivatives liquidation.
2. Long liquidation has been substantial, but a confirmed bottom is DATA UNAVAILABLE (MOD 36).
3. A temporary rebound inside the Nov 19–30 liquidity vacuum is possible, but must not be mistaken for a trend reversal (MOD 44 CB-01).

WHAT WOULD CHANGE MY DECISION?
Positive Domestic USD Spot CVD, sustained passive buying absorption (MOD 06A), US Spot ETF outflows halting (>= $0M 3D net), stabilizing OI, and a confirmed 4H higher low / VAH reclaim (4+ 1H bars) with Net R >= 3.0 (MOD 37).

FINAL VERDICT: Protect capital first. Do not catch the falling knife. Wait for evidence of buyers returning.
```

---

### Template 45B: Ultra-Compact Hourly Heartbeat (`:05 MYT` Automated Cron)
Used by `telegram_cortex_alert.py` when `LOCKED_HALT` or current regime remains unchanged:
```text
[CORTEX-BTC | <HH:MM MYT>] <REGIME_BADGE>
BTC: $<PRICE> (<24H_PCT>%) | OI: <OI_PCT>% | Funding: <FUNDING>
Posture: <DECISION_BADGE> | Gate: <ACTIVE_MOD_BLOCKER>
Flip Trigger: <PRIMARY_UNMET_CONDITION>
```

---

### Template 45C: Asymmetric Entry / Exit Strike Card (`Net R >= 3.0` or `MOD 41` Trigger)
Used strictly when all 5 Pillars align (`GATE_GREEN`) or a `MOD 41` / `MOD 18` exit rule fires:
```text
[STRIKE ALERT — <ACTION_TYPE>] <DD MMM YYYY> | <HH:MM MYT>
━━━━━━━━━━━━━━━━━━━━━━
REGIME: <REGIME_BADGE> | TRIGGER: <MOD_AND_CSU_ID>
BTC: $<PRICE> | Entry/Exit Zone: $<ZONE_LOW>–$<ZONE_HIGH>
Hard Stop: $<STOP_PRICE> (<STOP_DIST_PCT>%) | Net R: <NET_R>R
Position Size: <RISK_PCT>% Equity Risk (1.0x Spot Only)
━━━━━━━━━━━━━━━━━━━━━━
AUTHENTICATION CHECKLIST:
✓ Pillar 1 Macro & MOD 44 Calendar: <STATUS>
✓ Domestic USD Spot CVD & ETF Flows: <STATUS>
✓ Volume Profile / Fib Confluence: <STATUS>

VERDICT: <EXECUTION_COMMAND>
```

---

## 4. Core Conditional Signal Units (`Condition A -> Outcome B -> Rule C`)

### CSU-45A: Defensive / Cash-Lock Bottom-Line HUD
* **Trigger Condition A:** Any daily morning briefing, user analysis request, or regime alert while `Pillar 1 == GATE_RED`, `MOD 44` calendar drain is active, or `Net R < 3.0`.
* **Observed Outcome B:** High risk of emotional bottom-fishing or premature counter-trend entries during macro/liquidity drawdowns.
* **Execution Rule C:** Render **Template 45A** with `WAIT — HOLD USDT (100% CASH LOCK | 0.00% RISK)`, explicitly tag unconfirmed bottoms as `DATA UNAVAILABLE`, and list exact telemetry flip triggers.

### CSU-45B: Asymmetric Spot-Entry / Harvest Strike HUD
* **Trigger Condition A:** All 5 Pillars pass (`GATE_GREEN`), `Domestic USD Spot CVD` confirms, and post-cost `Net R >= 3.0` (`MOD 37`)—or a `MOD 41` / `MOD 18` profit-harvest trigger fires.
* **Observed Outcome B:** Actionable spot execution window requiring exact price levels, stop distance, and `<= 0.75%` equity risk sizing.
* **Execution Rule C:** Render **Template 45C** immediately followed by **Template 45A** for full situational awareness.

### CSU-45C: Missing-Telemetry Degraded HUD (`MOD 36` Enforcement)
* **Trigger Condition A:** One or more upstream feeds (`ETF flows`, `CVD`, `OI`, or `Funding`) fail staleness SLA (`MOD 36`) or return null values.
* **Observed Outcome B:** Risk of hallucinated metrics or false confidence.
* **Execution Rule C:** Render **Template 45A**, populate missing fields strictly with **`DATA UNAVAILABLE`**, and lock posture to `WAIT — HOLD USDT (100% CASH LOCK)` until telemetry recovers.

---

## 5. Dynamic Regime Mutation Lookup Matrix (`M1` through `M6`)

| Mutation ID | Initial State | Telemetry Mutation Observed (`Condition A'`) | Mechanical Meaning (`Outcome B'`) | Mandatory Execution Override (`Rule C'`) |
| :--- | :--- | :--- | :--- | :--- |
| **M1: User Requests "Bottom Line" / "Summary"** | Any Query | User asks for a market check, bottom line, or daily brief on mobile/Telegram/chat. | Operator wants instant scannable decision clarity without narrative clutter. | **Default to Template 45A** automatically without needing to be reminded. |
| **M2: Hourly Cron Unchanged Regime** | `LOCKED_HALT` | Hourly `:05 MYT` check confirms BTC remains inside an active `MOD 44` or `GATE_RED` block with no new `Net R >= 3.0` setup. | No action required; avoid notification fatigue on Samsung Galaxy A55. | **Emit Template 45B** (4-line compact heartbeat) instead of full card. |
| **M3: Regime Flip (`R4` -> `R2/R1` Reclaim)** | `WAIT — HOLD USDT` | All items in `WHAT WOULD CHANGE MY DECISION?` flip green simultaneously (`ETF >= $0M`, `USD Spot CVD` higher low, `4H VAH` reclaim, `Net R >= 3.0`). | Defensive cash lock has officially transitioned into a valid spot swing setup. | **Fire Template 45C Strike Alert** immediately with `0.75%` risk sizing. |
| **M4: Missing / Stale Feed (`MOD 36`)** | Any Active Scan | An exchange API or ETF tracker lags beyond SLA or returns missing fields. | Telemetry integrity is degraded (`UNKNOWN` state). | Print **`DATA UNAVAILABLE`** on affected bullet(s) and enforce `100% CASH LOCK`. |
| **M5: Screenshot / Chart Audit Request** | User Uploads Chart | User shares a TradingView or Coinglass screenshot asking for a verdict. | Visual pattern (`MOD 42/43`) must be graded against live order-flow rules. | Audit chart shapes under `MOD 42/43`, then summarize strictly inside **Template 45A**. |
| **M6: Multi-Asset / Altcoin Noise Attempt** | Out-of-Scope Query | Incoming feed or prompt includes altcoin liquidations or non-BTC trade ideas. | Violates Project CORTEX-BTC strict `BTC-USD 1.0x Spot Only` charter. | Strip altcoin execution recommendations; keep HUD locked exclusively on **BTC spot**. |
