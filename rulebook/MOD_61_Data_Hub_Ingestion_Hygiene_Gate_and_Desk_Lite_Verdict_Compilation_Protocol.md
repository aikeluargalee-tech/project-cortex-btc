# PROJECT CORETEX-BTC BRAIN — MODULE 61: DATA HUB INGESTION, HYGIENE GATE & DESK-LITE VERDICT COMPILATION PROTOCOL

**Waterfall Tier:** Tier D (Control-Plane Telemetry Ingestion, Data Hygiene Audit, 5-Function Synthesis & Workstation Verdict Interface) — governs how AI reasoning instances (Gemini, Hermes Agent, or Workstation Co-Pilots) parse consolidated `TAB [D: DATA HUB]` telemetry packets and compile auditable, zero-hallucination verdicts alongside `MOD 36` (Telemetry Trust & Determinism Attestation), `MOD 45` (Executive Bottom-Line HUD), `MOD 54` (500/600/500 Kline Lookback Contract), and `MOD 60` (7-Rank Veto Precedence Ladder).
**Empirical Benchmark Anchor:** Codified from the `TAB [D: DATA HUB]` Consolidated Data-Only Telemetry Report schema (`Sections 1–8`, SQLite closed-`4H` trajectory archive, `500`-bar `1D/4H/1H` swing structure & S/R clusters, and closed OHLCV klines) paired with the **CORTEX BTC DESK LITE v1.0** 3-step execution playbook.
**Governance Posture:** Pure analytical & compilation protocol (`ZERO_STANDALONE_STRATEGY_DRIFT`). Enforces strict data hygiene, non-fabrication of external metrics, and deterministic routing into `100% USDT CASH — NO ENTRY` or `ACTIVE SPOT LONG` (`<= 0.75%` max portfolio risk, `1.0x` unleveraged spot only).

---

#### 1. Machine-Readable State & Routing Block (Python / Hermes / NotebookLM Index)

```yaml
module_id: "MOD_61"
entry_type: "CONTROL_PLANE_INGESTION_AND_VERDICT_PLAYBOOK"
waterfall_pillar: "TIER_D_WORKSTATION_INTERFACE"
title: "Data Hub Ingestion, Hygiene Gate & Desk-Lite Verdict Compilation Protocol"

# GOVERNANCE POSITION & PRECEDENCE
governance_priority: 2 # Subordinate to MOD 36 (Rank 0) and MOD 60 (Ranks 0-4 vetoes)
execution_authority: "INGESTION_HYGIENE_AND_VERDICT_SYNTHESIS"
default_posture_on_conflict_or_degradation: "100% USDT CASH — NO ENTRY (0.00% Risk)"

# DATA HUB TELEMETRY PACKET SCHEMA (TAB [D: DATA HUB])
data_hub_sections:
  header_metadata:
    - "Retrieval Time (UTC & MYT / UTC+8)"
    - "Spot Price (BTCUSDT) & Coverage Tally (OK / UNAVAILABLE / STALE / PROXY/STATIC)"
    - "24H Range & Returns (24H / 7D / 30D)"
    - "SQLite Archive Snapshot Count & Last Closed 4H Timestamp"
  section_1: "Price, Trend & Market Structure (Spot/Perp, 1D/4H/1H MAs, VWAP Z, RSI, ADX, ATR, 30D VP, L20/H20/PW/Asia)"
  section_2: "Order Flow, Footprint & Liquidity (15m/1h/4h/24h Spot & Perp CVD, z_S/z_F/D, 15m Delta/Stacks, CB Prem, L2 Depth, OBI, Spread, 7D/24H VP, 30D VA Pos%, SLSP)"
  section_3: "Derivatives, Options & Liquidations (BN OI, Cross-Exch OI [BN+BYB+OKX], OI Delta%, 8H/Ann/90D Pct Funding, Basis, Taker L/S, Deribit P/C & 25d Skew, DVOL/RV20/GK/BBW%, Liq Magnets & LSCE)"
  section_4: "On-Chain, ETF & Stablecoin Flows (MVRV, SOPR/aSOPR, Exchange Netflow & Reserves, USDT+USDC Supply & 7D/30D Net Issuance, Farside ETF Flow, IBIT+FBTC Proxy, Power-Law Fair/DD%, MTF MACD)"
  section_5: "Macro, Credit & US Liquidity (SOFR, Fed ON RRP, HYG/LQD, DXY, US10Y, TIPS Real/BEI, SPX/NDX, VIX, Brent Crude, BTC-SPX Corr, F&G, BTC Dom%, Manual Overrides)"
  section_6: "Quant Features, Feed Health & Archive (4H A_SP Levy Area, Hurst H, Kalman Vel, FracDiff, Hilbert Cycle, TD9, TellTale RV, VCR 72H, TSFM Disp%, FVGs, Sweep FSM, WS Health, Kline Counts, Closed 4H Anchor)"
  section_7: "Recent Closed-4H Snapshot Trajectory (SQLite Archive)"
  section_7a: "500-Bar Market Structure & Historical S/R Zones (1D / 4H / 1H Swings, Pivots, BOS, 1%-Clustered S/R)"
  section_7b: "Recent Closed Klines — OHLCV Price Action (1D x7, 4H x12, 1H x12, Newest First)"

# METRIC LEGEND & DECODING RULES (MANDATORY)
legend_decoding_rules:
  headless_ws_snapshot_rule: "If Warm == YES and WebSocket Feeds reports STALE (no tick) during a scheduled/one-shot REST snapshot, treat as expected headless behavior—verify REST Closed 4H Anchor freshness rather than triggering a REST outage halt."
  partial_venue_oi_rule: "If Cross-Exch Perp OI tags [... X/3 PARTIAL_VENUE] (< 3/3 venues), suppress OI quadrant classification and NEVER interpret the drop as genuine deleveraging."
  funding_90d_pct_rule: "Read 90D Pct strictly as a 0-100 rolling 90-day percentile rank of 8H funding, never as an annualized interest rate."
  va_pos_pct_rule: "30D VA Pos% = (Spot - VAL) / (VAH - VAL) * 100 measured strictly against Macro 30D VAH/VAL (< 0% indicates price trading below 30D VAL)."
  cvd_z_divergence_rule: "z_S and z_F are 30D rolling Z-scores of 24H Spot and Perp CVD; D = z_S - z_F (D > 0 = Spot buying divergence vs. Perps; D < 0 = Spot selling heavier than Perps)."
  kline_floor_harmonization: "Accept >= 500 closed 4H bars (499 closed + 1 forming) for Desk-Lite workstation display while preserving MOD 54's 600-bar 4H floor for master compiler 90D Fib + ATR(14) warm-up runs."
  zero_external_fabrication_rule: "Strictly cite ONLY metrics explicitly present in the active TAB [D: DATA HUB] snapshot; never import external prices, indicators, or unverified claims."

# THREE-STEP WORKSTATION PLAYBOOK (CORTEX BTC DESK LITE)
execution_playbook:
  step_1: "Mandatory Data Hygiene Gate (Coverage tally, UNAVAILABLE/STALE/PROXY isolation, WS headless check, PARTIAL_VENUE audit)"
  step_2: "5-Function Deterministic Synthesis (1. MTF Regime -> 2. Spot Flow & Liquidity -> 3. Derivatives & Squeeze -> 4. Macro/On-Chain/ETF -> 5. Spot-Only Risk Arbiter)"
  step_3: "6-Section Workstation Output Contract (or compressed MOD 45 Template 45A HUD for mobile Telegram)"

# RISK & SIZING CONSTANTS (PILLAR 4)
risk_parameters:
  max_portfolio_risk_pct: 0.75 # 0.375% GATE_AMBER / 0.00% GATE_RED
  chop_adx_floor: 20.0 # ADX < 20 or TRANSITIONAL regime -> 100% USDT CASH — NO ENTRY
  leverage_permitted: 1.0 # Strict 1.0x Unleveraged Spot Only
```

---

#### 2. Protective Circuit Breakers (Workstation Hygiene & Anti-Hallucination Guardrails)

*   **Circuit Breaker 1 — Mandatory Pre-Scoring Data Hygiene Gate (`CB-01`):** Never compute a directional regime or execution posture before auditing the `Coverage` header (`OK / UNAVAILABLE / STALE / PROXY/STATIC`). Every missing feed (`UNAVAILABLE`) or proxy metric (`[PROXY]`) must be explicitly logged in Section 2 of the verdict and treated as non-confirming (`MOD 36` `DATA UNAVAILABLE` honesty).
*   **Circuit Breaker 2 — Headless Snapshot vs. Live Stream Disambiguation (`CB-02`):** Scheduled GitHub Actions or one-shot cron runs execute a single REST warmup (`Warm:YES`) without a persistent WebSocket daemon. When `WebSocket Feeds & Warmup` displays `STALE (no tick)` alongside `Warm:YES` and a current `Closed 4H Anchor` timestamp, classify it as an expected headless snapshot—not a corrupted REST feed (`MOD 36 M2` partial-feed awareness).
*   **Circuit Breaker 3 — Partial-Venue OI & Proxy-ETF Quarantine (`CB-03`):** Whenever `Cross-Exch Perp OI` or Section `7` archive rows display `[... X/3 PARTIAL_VENUE]` (`< 3/3` exchanges), ban any deleveraging or short-squeeze claim derived from OI contraction. Similarly, when primary `US Spot ETF Flow (Farside)` is `UNAVAILABLE` and only `IBIT+FBTC [PROXY]` volume/flow is available, downgrade ETF confirmation to `PROXY/CAUTION` (`MOD 31 M7`) until primary settlement data arrives (`MOD 38`).
*   **Circuit Breaker 4 — Below-`1D SMA 200` & `ADX < 20` Cash Shield (`CB-04`):** Enforce **`100% USDT CASH — NO ENTRY`** whenever `1D` closes below `1D SMA 200` (`MOD 17` / `MOD 57 M4`) while `4H` exhibits an active `DOWNTREND (LH/LL)` or broken structure, when `ADX < 20` / `TRANSITIONAL` chop prevails, or when any `MOD 60` `Rank 0–4` veto (`MOD 44` IPO/MSCI vacuum, `MOD 58` Trinity Lock, `ICDM >= 60`) is active.
*   **Circuit Breaker 5 — Dual-Viewport Rendering Bridge (`CB-05`):** When operating in desktop/workstation mode, output the full **6-Section Workstation Audit Contract** (`Step 3`). When operating on mobile Telegram (`Samsung Galaxy A55`) or generating automated hourly cron alerts, compress the compiled verdict strictly into **`MOD 45` Template `45A` or `45B` HUD** without dropping any `DATA UNAVAILABLE` flags.

---

#### 3. Core Conditional Signal Units (Condition A -> Outcome B -> Rule C)

##### CSU-61A: Step 1 — Mandatory Data Hygiene Gate (`Coverage` & Feed Integrity Audit)
*   **Trigger Condition A (The Telemetry Scan):**
    1. Operator or automated pipeline supplies a consolidated `TAB [D: DATA HUB]` telemetry report.
*   **Observed Outcome B (The Mechanical Trajectory):**
    *   **Control-Plane Lens:** Raw multi-tab telemetry mixes live REST endpoints, daily on-chain/macro prints, proxy volume estimates, and headless WebSocket flags. Scoring without hygiene filtering produces false confidence or false outage alarms.
*   **Execution Rule C (The Non-Negotiable Action):**
    *   **Action:** Execute the 5-point Hygiene Check before any market synthesis:
        1. Log exact `OK / UNAVAILABLE / STALE / PROXY/STATIC` counts.
        2. Check `Warm:YES` to separate expected headless `WS STALE (no tick)` from true REST staleness.
        3. Verify `[BN+BYB+OKX 3/3]` venue quorum on Cross-Exch OI (quarantine if `< 3/3`).
        4. Confirm `90D Pct` is read as `0–100` rank, `30D VA Pos%` against Macro 30D VAH/VAL, and `ATR(14)` per matching timeframe (`1D/4H/1H`).
        5. Lock strict zero-hallucination boundary (zero external prices or unlogged metrics permitted).

##### CSU-61B: Step 2 — 5-Function Deterministic Synthesis Pipeline
*   **Trigger Condition A (The Telemetry Scan):**
    1. `CSU-61A` Data Hygiene Gate completes and isolates valid vs. degraded feeds.
*   **Observed Outcome B (The Mechanical Trajectory):**
    *   **Architectural Lens:** Sequential evaluation across all five core pillars (`MOD 18` + `MOD 60` precedence ladder) prevents single-indicator bias (such as mistaking a `1H` bounce for a `1D` trend reversal).
*   **Execution Rule C (The Non-Negotiable Action):**
    *   **Action:** Execute the 5 deterministic functions in strict order:
        1. **Function 1 — Multi-Timeframe Regime Classifier:** Integrate Section `1` (`1D SMA 200` & slope, `1D/4H` EMAs, `ADX(14)`, `RSI(14)`), Section `6` (`Hurst H`, `VCR 72H`), Section `7A` (`1D/4H/1H` swing structure & latest `BOS`), and Section `7B` closed OHLCV bars -> classify into `UPTREND`, `DOWNTREND`, `RANGE-BOUND`, or `TRANSITIONAL`.
        2. **Function 2 — Spot Flow & Liquidity Inspector:** Evaluate Section `2` (`15m/1h/4h/24h` Spot vs. Perp CVD, `z_S / z_F / D`, `15m` delta/stacks, `Coinbase Premium $/%/Z`, `L2 Depth ±1%/±2%`, `OBI`, `Spread`, `30D VA Pos%`, `SLSP`) + Section `6` (`4H A_SP` Lévy area) + Section `7A` S/R clusters -> classify true spot accumulation vs. distribution or passive absorption.
        3. **Function 3 — Derivatives & Squeeze Risk Profiler:** Evaluate Section `3` (`BN OI`, `3/3` Cross-Exch OI, `OI Δ%` & Quad, `8H/Ann/90D Pct` funding, `Perp Basis`, `DVOL`, `RV20`, `GK`, `25d Skew`, `Upper/Lower Liq Magnets`, `Pull Ratio`, `LSCE`, `Liquidations`) -> quantify leverage fragility and squeeze asymmetry.
        4. **Function 4 — Macro, On-Chain & ETF Gatekeeper:** Synthesize Section `4` (`MVRV`, `SOPR`, `Exchange Netflow/Reserves`, `USDT+USDC` `7D/30D` net issuance, `Farside` / `IBIT+FBTC` proxy, `MTF MACD`) + Section `5` (`SOFR`, `ON RRP`, `HYG/LQD`, `DXY`, `US10Y`, `TIPS Real`, `SPX/NDX`, `VIX`, `Brent`, `BTC-SPX Corr`, `F&G`, `Manual Overrides`) + active `MOD 44`/`58` calendar gates -> assign macro backdrop (`Tailwind`, `Neutral`, or `Headwind`).
        5. **Function 5 — Spot-Only Risk & Decision Arbiter:** Apply `MOD 60` `Ranks 0–4` vetoes and `CB-04` gates. If `1D < 1D SMA 200` + `4H DOWNTREND`, or `ADX < 20` / `TRANSITIONAL`, or multi-gate conviction fails, enforce **`100% USDT CASH — NO ENTRY`**. Otherwise size `ACTIVE SPOT LONG` strictly at `<= 0.75%` portfolio risk (`1.0x` spot only, `Net R >= 3.0` per `MOD 37`).

##### CSU-61C: Step 3 — 6-Section Workstation Output Contract & `MOD 45` Mobile Bridge
*   **Trigger Condition A (The Telemetry Scan):**
    1. `CSU-61B` completes all 5 synthesis functions and resolves final posture + confidence score (`/100`).
*   **Observed Outcome B (The Mechanical Trajectory):**
    *   **Operator Interface Lens:** Provides full institutional traceability on desktop while maintaining 15-second scannability on mobile Telegram (`MOD 45`).
*   **Execution Rule C (The Non-Negotiable Action):**
    *   **Action:** Render the exact 6-section workstation report:
        1. **EXECUTIVE SUMMARY & DESK POSTURE** (Spot Price, Regime State, Binary Posture: `ACTIVE SPOT LONG` or `100% USDT CASH — NO ENTRY`, Confidence `/100`).
        2. **DATA HYGIENE AUDIT** (Exact `OK / UNAVAILABLE / STALE / PROXY` tally, headless WS clarification, `PARTIAL_VENUE` check, degraded-signal list).
        3. **MULTI-TIMEFRAME REGIME & FLOW SYNTHESIS** (Price/EMA/ADX/Hurst structure vs. Spot CVD, `z_S/z_F/D`, Coinbase Premium, `4H A_SP`, and SQLite Section `7` + `7A/7B` trajectory).
        4. **DERIVATIVES, LIQUIDITY & MACRO CONTEXT** (OI venue-integrity check, funding `90D Pct`, options `25d` skew, liquidation magnets, macro/ETF/stablecoin headwind vs. tailwind).
        5. **CRITICAL LEVELS MAP** (Immediate & Major Support, Immediate & Major Resistance, Hard Invalidation Levels anchored strictly to `7A/7B`, `30D/7D/24H VP`, and `SLSP`).
        6. **SPOT EXECUTION PLAN (OR NO-ENTRY GATE)** (Exact Entry Zone, Hard Stop Loss, Two-Stage Take Profit Targets, Position Size at `<= 0.75%` portfolio risk, and explicit Multi-Gate Validation Triggers required to flip posture).
    *   *(Mobile Bridge Rule: If requested for Telegram/mobile or hourly cron, emit `MOD 45` Template `45A` / `45B` directly from this compiled output).*

---

#### 4. Dynamic Regime Mutation Lookup Matrix (M1 through M5)

| Mutation ID | Initial State | Telemetry Mutation Observed (Condition A') | Mechanical Meaning (Outcome B') | Mandatory Execution Override (Rule C') |
| :--- | :--- | :--- | :--- | :--- |
| **M1: Headless One-Shot REST Snapshot** | `CSU-61A` Hygiene Gate | `WebSocket Feeds & Warmup` prints `STALE (no tick)` while `Warm:YES` and `Closed 4H Anchor` matches the latest completed `4H` bar. | Expected behavior of stateless GitHub Actions / cron REST snapshots; REST feeds are fresh. | **Do Not Trip `MOD 36` REST Halt:** Note headless WS status in Section 2 and proceed normally. |
| **M2: Partial-Venue OI Anomaly** | `CSU-61B` Function 3 | `Cross-Exch Perp OI` or Section `7` archive row flags `[... 1/3 or 2/3 PARTIAL_VENUE]` with a sharp apparent OI drop. | Missing exchange feed created an artificial OI contraction reading (`MOD 36 CB-03`). | **Suppress OI Quadrant & Deleveraging Tag:** Treat OI delta as degraded until `[BN+BYB+OKX 3/3]` restores. |
| **M3: Primary ETF Feed Unavailable (`PROXY` Only)** | `CSU-61B` Function 4 | `US Spot ETF Flow (Farside)` reports `UNAVAILABLE` while `IBIT+FBTC [PROXY]` reports heavy negative 5D flow. | Official primary settlement is pending (`MOD 38`), while secondary ETF tape confirms outflow pressure. | **Log `Farside = DATA UNAVAILABLE`;** use `IBIT+FBTC [PROXY]` strictly as a conservative headwind filter, never as a bullish unlock trigger. |
| **M4: Tactical `1H` BOS Inside `4H/1D` Downtrend** | `CSU-61B` Function 1 | Section `7A` shows `1H` printing `BOS Up` while `1D` (`< 1D SMA 200`) and `4H` remain `DOWNTREND (LH/LL)` with negative `24H Spot CVD` and `4H A_SP < 0`. | Short-term tactical relief bounce inside a structurally bearish higher-timeframe regime (`MOD 54 M2`). | **Enforce `100% USDT CASH — NO ENTRY` (`CB-04`):** Require `4H` structure reclaim + positive `24H` Domestic USD Spot CVD before authorizing even `0.375%` probe risk. |
| **M5: Mobile Telegram Compression Request** | `CSU-61C` Output | Operator requests a mobile HUD card or runs on `Samsung Galaxy A55` / Telegram (`MOD 45 M1`). | Full 6-section workstation report exceeds single-screen mobile viewport ergonomics. | **Auto-Compress to `MOD 45` Template `45A` HUD** while preserving exact `DATA UNAVAILABLE` tags and flip triggers.
