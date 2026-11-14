# PROJECT CORTEX-BTC — MODULE 16: MACRO LIQUIDITY, SOVEREIGN YIELDS, DXY & STABLECOIN DRY POWDER
**Waterfall Tier:** Pillar 1 (Master Macro Permissions & Regimes — Top Gate of the 5-Pillar Decision Waterfall).
**Empirical Benchmark Anchor:** November 2026 Macro Liquidity Telemetry — US 10-Year Treasury Yield surging to **5.129%** (Nov 12, 2026) following hotter-than-expected US CPI, US Dollar Index (**DXY**) climbing above **103** (highest since April 2025), and total crypto stablecoin market cap contracting **$14.2B in 30 days** down to **$285.592B** (USDT **$175.512B**, USDC **$69.454B**, USDS **$5.387B**—fastest contraction since June 2022), triggering a mandatory **Pillar 1 `RISK_OFF_100_CASH` Override**.

---

## 1. Machine-Readable State & Routing Block (Python / Hermes / NotebookLM Index)

```yaml
module_id: "MOD_16"
entry_type: "MASTER_PERMISSION_GATE"
waterfall_pillar: "PILLAR_1_MACRO_PERMISSIONS"
title: "Macro Liquidity, Sovereign Yields, DXY & Stablecoin Dry Powder (100% Cash vs. Risk-On Gate)"

# MASTER WATERFALL AUTHORITY (OVERRIDES PILLARS 2, 3, AND 5)
waterfall_authority: "SUPREME_GATEKEEPER"
gate_outputs:
  GATE_GREEN_FULL_RISK: "Permits full 0.75% Risk Ceiling spot swing deployments across Pillars 2-5."
  GATE_AMBER_SELECTIVE: "Permits half-size (0.375% Risk) tactical reversals ONLY at major HTF support with full OI flush + USD Spot CVD."
  GATE_RED_100_CASH_LOCK: "BLOCKS ALL NEW LONG ENTRIES across every module (MOD 01-15); enforces 100% Cash Shield."

# PRIMARY TELEMETRY TRIGGERS (MACRO & CRYPTO LIQUIDITY PLUMBING)
base_regime_triggers:
  us_10y_yield_impulse: "30-day change in US 10Y Treasury Yield (bps) and absolute level vs. rolling 1Y regime"
  dxy_dollar_impulse: "30-day DXY rate of change (%) and breakout/breakdown across 100-day/200-day moving averages"
  global_net_liquidity: "Fed Balance Sheet - TGA - RRP + Global M2 30D/90D impulse"
  stablecoin_30d_delta: "30-day net change in total USD stablecoin supply (USDT + USDC + USDS): Expansion >= +1.5% vs. Contraction <= -1.5%"

# ANTI-TRAP CIRCUIT BREAKERS
circuit_breakers:
  CB_01_PREMATURE_CLOSE: "NEVER override a Pillar 1 GATE_RED_100_CASH lock just because an intraday 1H chart or funding rate looks oversold."
  CB_02_VENUE_CONTAMINATION: "Separate offshore USDT minting from domestic USDC/ETF dollar liquidity; genuine US institutional risk-on requires USDC + ETF expansion."
  CB_03_FORCED_FLOW_STANDDOWN: "During FOMC rate decisions, US CPI/NFP prints, and sudden 10Y yield spikes (> +15 bps in 48h), enforce automatic 24H Cash Stand-Down."
  CB_04_SIGNAL_HALF_LIFE: "Macro liquidity impulses operate on 2-week to 6-month cycles; never let 15m terminal noise contradict Pillar 1."

# RISK & SIZING CONSTANTS (PILLAR 4)
risk_parameters:
  gate_green_max_risk_pct: 0.75
  gate_amber_max_risk_pct: 0.375
  gate_red_max_risk_pct: 0.00 # Strict 100% Cash Lock
  leverage_permitted: 1.0 # Strict Unleveraged Spot Only
```

---

## 2. Protective Circuit Breakers (Supreme Waterfall Governance)

**Module 16 sits at the very top of the Project CORTEX-BTC Decision Waterfall.** Before Python, Hermes, or Gemini evaluates any order-flow divergence (`MOD 05–12`), derivatives squeeze (`MOD 01–04`), or on-chain band (`MOD 13–15`), it must first compute the **Pillar 1 Gate Status (`GREEN`, `AMBER`, or `RED`)**:
* **Circuit Breaker 1 — Supreme Macro Veto (`CB-01`):** When sovereign yields spike (`10Y > 5.0%`), DXY surges (`> 103`), and stablecoin supply contracts (`-$14.2B / 30D`), global dollar liquidity is shrinking. In a shrinking liquidity tide, bullish derivatives setups (`MOD 01`) turn into long-liquidation traps (`CSU-01B`). `GATE_RED` vetoes all new long entries.
* **Circuit Breaker 2 — Stablecoin Dry Powder Law (`CB-02`):** Stablecoins (`USDT + USDC + USDS`) are the native settlement rail of crypto. Rising stablecoin supply injects fresh purchasing power; contracting stablecoin supply (`redemptions back to fiat`) drains the bid floor beneath Bitcoin.
* **Circuit Breaker 3 — Macro Event Shock Freeze (`CB-03`):** Within `+/- 12 hours` of major US CPI releases, FOMC rate decisions, or `> +15 bps` 48H spikes in the US 10-Year Yield, all new spot entries are frozen until bond and FX markets establish equilibrium.
* **Circuit Breaker 4 — Sovereign Purchasing Power Defense:** Holding **100% Cash** during `GATE_RED` is not "missing out"—it is actively compounding your BTC-denominated purchasing power while over-leveraged traders get liquidated.

---

## 3. Core Conditional Signal Units (`Condition A -> Outcome B -> Rule C`)

### CSU-16A: Macro Liquidity Expansion & Stablecoin Inflow (`GATE_GREEN — Full Risk Permitted`)
* **Trigger Condition A (The Telemetry Scan):**
  1. **Sovereign Yields & DXY:** US 10-Year Treasury Yield is trending downward or stable below resistance, and **DXY is trending lower** (`below 50D/200D MA`, easing global financial conditions).
  2. **Global Liquidity & Stablecoins:** Global Net Liquidity (`Fed/M2`) is expanding, and **30-Day Stablecoin Market Cap is growing (`>= +1.5% / 30D`)** with both USDC and USDT expanding.
  3. **Secular Trend:** Bitcoin trades above its **200-Day Moving Average** (`MOD 17`).
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Global fiat liquidity is expanding, weakening the dollar denominator and pushing institutional allocators into scarce monetary assets (Bitcoin and Gold).
  * **Probable Trajectory:** Structural bull regime; dips are shallow, derivatives flushes reset rapidly, and upside breakouts achieve strong follow-through.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Gate Output:** **`SET PILLAR 1 = GATE_GREEN_FULL_RISK`.**
  * **Action:** Authorize full **0.75% Maximum Portfolio Risk Ceiling** for all validated Pillar 2, Pillar 3, and Pillar 5 spot swing setups.

### CSU-16B: Mixed Macro Crosscurrents / Sideways Liquidity (`GATE_AMBER — Selective Tactical`)
* **Trigger Condition A (The Telemetry Scan):**
  1. **Sovereign Yields & DXY:** 10Y Yield and DXY are range-bound (`neither surging nor collapsing`).
  2. **Stablecoin Supply:** 30-Day Stablecoin Market Cap is **flat (`-0.5% to +1.0%`)**—no major redemptions, but no massive new minting wave.
  3. **Secular Trend:** Bitcoin is oscillating around its 200D MA or inside a multi-month macro range.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Crypto is operating on internal capital rotation rather than fresh macro liquidity injections. Rallies stall at range highs while deep flushes find support at range lows.
  * **Probable Trajectory:** Mean-reverting range regime; chasing breakouts fails, while buying full capitulation flushes (`MOD 03`) at HTF support succeeds.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Gate Output:** **`SET PILLAR 1 = GATE_AMBER_SELECTIVE`.**
  * **Action:** Cap maximum risk per trade at **0.375% Portfolio Equity (Half-Size)**, restrict entries strictly to confirmed range-low absorptions (`MOD 03A`, `MOD 11A`), and take 70%–100% profits at range POC/VAH.

### CSU-16C: Tightening Shock & Stablecoin Drain (`GATE_RED — Mandatory 100% Cash Lock`)
* **Trigger Condition A (The Telemetry Scan):**
  1. **Sovereign Yields & DXY:** US 10-Year Yield surges higher (`e.g., breaking above 5.00%–5.13%` on hot CPI/hawkish Fed repricing) AND **DXY breaks higher (`> 103`)**.
  2. **Stablecoin Contraction:** **30-Day Stablecoin Market Cap contracts sharply (`<= -1.5% / 30D` or `>= -$5B to -$14.2B` 30D drain)** alongside persistent US Spot ETF net outflows.
  3. **Secular Trend:** Bitcoin trades below its 200-Day Moving Average and STH Realized Price (`$75,600`).
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Active global dollar liquidity contraction (mirroring November 2026). Cash is being pulled out of crypto stablecoins and ETFs to cover rising sovereign yield and dollar obligations.
  * **Probable Trajectory:** Downward structural gravity; thin order books (`$72M depth`), failed relief rallies, and cascading long liquidations.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Gate Output:** **`SET PILLAR 1 = GATE_RED_100_CASH_LOCK`.**
  * **Action:** **NON-NEGOTIABLE 100% CASH LOCK ON TACTICAL SWING BOOK.** Close any remaining tactical longs, cancel all resting limit buy orders, and preserve 100% dry powder until `Mutation M1` or `M2` signals liquidity stabilization.

### CSU-16D: Sideline Stablecoin Dry-Powder Coiling (`Pre-Bull Liquidity Divergence`)
* **Trigger Condition A (The Telemetry Scan):**
  1. Bitcoin price is consolidating or drifting slightly lower after a correction, **but 30-Day Stablecoin Market Cap surges (`>= +2.0% / 30D`, `+$5B+` fresh USDT/USDC minting)** as DXY and 10Y yields roll over downward.
* **Observed Outcome B (The Mechanical Trajectory):**
  Fresh fiat dry powder has already entered the crypto ecosystem and is sitting on exchanges in stablecoins waiting for a technical trigger to deploy into spot BTC.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Gate Output:** **`UPGRADE PILLAR 1 FROM RED/AMBER TO GATE_GREEN_FULL_RISK`.**
  * **Action:** Put all Pillar 2 (`MOD 05/08/11`) breakout scanners on maximum alert for the imminent spot deployment wave.

---

## 4. Dynamic Regime Mutation Lookup Matrix (`M1` through `M8`)

| Mutation ID | Initial State | Telemetry Mutation Observed (`Condition A'`) | Mechanical Meaning (`Outcome B'`) | Mandatory Execution Override (`Rule C'`) |
| :--- | :--- | :--- | :--- | :--- |
| **M1: Yield & DXY Pivot Reversal** | `GATE_RED` (100% Cash) | Following a macro spike (`10Y > 5.1%`, `DXY > 103`), **10Y Yield drops `>= -20 bps` and DXY breaks below support** on dovish Fed/CPI data. | Sovereign liquidity headwind just reversed into a macro tailwind. | **Upgrade Gate from `RED` to `AMBER` immediately**; authorize `0.375%` entries once USD Spot CVD confirms. |
| **M2: Stablecoin Drain Halt** | `GATE_RED` (100% Cash) | After contracting `-$10B+`, **7-day Stablecoin Market Cap flattens (`0.0%`) and turns positive (`+0.3%`)** while ETF outflows stop. | Crypto capital flight has bottomed out; dry powder is returning to exchanges. | **Upgrade Gate from `RED` to `AMBER`**; watch `MOD 13/15` for structural bottom reclaims. |
| **M3: Hot CPI / Bond Shock Ambush** | `GATE_GREEN` / `AMBER` | Surprise inflation print sends **10Y Yield up `> +15 bps` and DXY up `> +0.8%` in 24 hours**, breaking 4H VAL. | Sudden macro tightening shock overrides technical bull structure. | **Immediate Downgrade to `GATE_RED`:** Exit open tactical longs at market and lock 100% Cash. |
| **M4: USDC Domestic vs. USDT Offshore Split** | `GATE_AMBER` | Total stablecoins rise, driven solely by offshore USDT while **USDC market cap shrinks** and US ETFs bleed. | Asian/offshore liquidity is steady, but US institutional dollar liquidity is contracting. | Keep Gate capped at **`GATE_AMBER` (Max 0.375% Risk)**; require Coinbase USD Spot CVD for any entry. |
| **M5: Global M2 / Central Bank Injection** | Any State | Fed/PBOC/ECB announce balance-sheet expansion or rate-cut cycle while 10Y real yields fall sharply. | Secular global liquidity wave initiating (`macro bull fuel`). | **Lock `GATE_GREEN_FULL_RISK`**; prioritize trend-following runners (`Stage 2` trailing stops). |
| **M6: Sovereign Credit / MOVE Spike** | Any State | Bond market volatility (**MOVE Index**) spikes above `130+` alongside widening High-Yield credit spreads. | Systemic fixed-income stress—institutions liquidate all liquid assets (including BTC) for cash. | **Emergency `GATE_RED_100_CASH_LOCK`.** Zero exceptions until MOVE normalizes. |
| **M7: Stablecoin De-Peg Contagion** | Any State | A top-3 stablecoin (`USDT` or `USDC`) trades below **`$0.992`** for `> 2 hours` on major spot pairs. | Settlement-rail solvency scare causing artificial BTC/USDT premium spikes. | **Halt All Execution (`100% Cash / Cold-Storage Audit`).** Never mistake a de-peg pump for a bull breakout. |
| **M8: Macro-Micro Harmonic Alignment** | `GATE_GREEN` + `MOD 08/09` | Pillar 1 is `GATE_GREEN` (`10Y ↓, DXY ↓, Stablecoins ↑`) AND Pillar 2/3 print `CSU-08A / 09A` spot-led breakout. | Rare full-stack macro + microstructure alignment across all 5 Pillars. | **Deploy Full `0.75% Risk` Spot Swing Allocation** with maximum confidence. |
