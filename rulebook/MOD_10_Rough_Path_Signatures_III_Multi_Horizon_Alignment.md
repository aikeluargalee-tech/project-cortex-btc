# PROJECT CORTEX-BTC — MODULE 10: ROUGH PATH SIGNATURES III — MULTI-HORIZON ALIGNMENT (1H TACTICAL VS. 4H/1D STRUCTURAL)
**Waterfall Tier:** Pillar 2 (Microstructure, Order Flow & Path Geometry) cross-verified with Pillar 1 (Macro Permissions) and Pillar 4 (Portfolio Engineering).
**Empirical Benchmark Anchor:** November 2026 Multi-Timeframe Divergence Telemetry — Short-lived 1H tactical rebounds (e.g., temporary +1% bounces off **$71,218** or **$68,000**) printing localized positive 1H curvature while the **4H and 1D structural drift vectors** remained steeply negative beneath the **$75,600–$75,771** STH cost basis and **$73,000** breakdown shelf.

---

## 1. Machine-Readable State & Routing Block (Python / Hermes / NotebookLM Index)

```yaml
module_id: "MOD_10"
entry_type: "CONDITIONAL_SIGNAL_UNIT"
waterfall_pillar: "PILLAR_2_MULTI_HORIZON_SIGNATURES"
title: "Rough Path Signatures III: Multi-Horizon Alignment (1H Tactical vs. 4H/1D Structural)"

# PILLAR 1 MASTER PERMISSION PRE-CHECK
pillar_1_permission_required: true
cash_lock_override: "If Pillar 1 Macro Regime == RISK_OFF_100_CASH, 4H/1D structural blocks override any bullish 1H tactical verdict."

# PRIMARY TELEMETRY TRIGGERS (FRACTAL SIGNATURE HIERARCHY)
base_regime_triggers:
  tactical_horizon: "1H Rough Path Verdict (Level-1 Drift + Level-2 Signed Areas A_P,V and A_CVD,OI)"
  structural_horizon: "4H and 1D Rough Path Drift Vector + Higher-Timeframe Value Area Position"
  alignment_states:
    FULL_FRACTAL_BULL: "1H Verdict > 0 AND 4H Verdict > 0 AND 1D Verdict >= 0"
    TACTICAL_PULLBACK_IN_UPTREND: "1H Verdict < 0 (into 4H VAL/POC) WHILE 4H > 0 AND 1D > 0"
    COUNTER_TREND_INFLECTION: "1H Verdict >= +1.5 Z WHILE 4H < 0 AND 1D < 0 (Requires Strict HTF Level + Full OI Reset)"
    REGIME_CONFLICT_CHOP: "1H, 4H, and 1D vectors oscillating with opposing signs inside HTF Value Area"

# ANTI-TRAP CIRCUIT BREAKERS
circuit_breakers:
  CB_01_PREMATURE_CLOSE: "NEVER treat a 1H bullish signature flip as a multi-day swing trend until 4H signed area confirms."
  CB_02_VENUE_CONTAMINATION: "All three timeframes (1H, 4H, 1D) must ingest Domestic Fiat (USD) Spot CVD as the primary flow coordinate."
  CB_03_FORCED_FLOW_STANDDOWN: "If 1D structural drift is strongly negative (< -1.5 Z) during active ETF outflows, cap any 1H counter-trend bounce strictly at Stage 1 resistance."
  CB_04_SIGNAL_HALF_LIFE: "Enforce strict signal half-life: a 1H signal expires within 12-24 hours unless promoted into a 4H signature flip."

# RISK & SIZING CONSTANTS (PILLAR 4)
risk_parameters:
  max_portfolio_risk_pct: 0.75
  counter_trend_risk_cap_pct: 0.375 # Half-size (0.375% max risk) for 1H counter-trend inflections against 4H downtrend
  leverage_permitted: 1.0 # Strict Unleveraged Spot Only
  exit_protocol: "TWO_STAGE_STRUCTURAL"
```

---

## 2. Protective Circuit Breakers (Mandatory Pre-Execution Filters)

Before any Scenario in Module 10 can authorize capital deployment, all four circuit breakers must pass:
* **Circuit Breaker 1 — Signal Half-Life Enforcement (`CB-04`):** A 1H Rough Path signature has a predictive half-life of **6 to 24 hours**. Holding a 1H tactical trade into a multi-week swing without 4H/1D signature confirmation violates path-decay physics and exposes capital to higher-timeframe trend resumption.
* **Circuit Breaker 2 — Hierarchy of Drift:** Higher timeframes govern structural drift (`1D > 4H > 1H`), while lower timeframes govern entry precision (`1H / 15m`). Never fight a negative 4H + 1D structural vector with full 0.75% risk size.
* **Circuit Breaker 3 — Counter-Trend Half-Risk Rule:** If taking a high-confluence 1H reversal inflection (`CSU-10C`) at a major HTF support while 4H/1D remain negative, position risk is automatically cut in half (**0.375% maximum portfolio equity risk**) until 4H flips positive.
* **Circuit Breaker 4 — Pillar 1 Macro Gate:** If Pillar 1 is in `RISK_OFF_100_CASH`, all `CSU-10C` counter-trend entries are disabled.

---

## 3. Core Conditional Signal Units (`Condition A -> Outcome B -> Rule C`)

### CSU-10A: Full Fractal Resonance ("High-Conviction Multi-Horizon Trend")
* **Trigger Condition A (The Telemetry Scan):**
  1. **1H Tactical Signature:** Positive drift (`S^(1) > 0`) with `A_P,V > 0` and `A_CVD,OI > 0`.
  2. **4H & 1D Structural Signatures:** Both 4H and 1D drift vectors are positive (`>= +1.0 Z-score`), and price is trading above the 4H Volume Profile VAH / 1D POC.
  3. **Pillar 1 & 5 Alignment:** Macro permissions are green and Domestic USD Spot CVD / ETF flows are net positive across multi-day windows.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Institutional accumulation across daily and multi-day horizons is directly reinforced by intraday order-flow momentum—zero cross-timeframe friction.
  * **Probable Trajectory:** Highest-probability multi-day to multi-week swing trend expansion with clean follow-through and minimal deep pullbacks.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Entry Trigger:** Execute **Unleveraged Spot Long** on any 15m/1H pullback to the 1H POC or reclaimed VAH.
  * **Position Sizing Formula (Full 0.75% Risk Ceiling):**
    `Spot Position (BTC) = (0.0075 * Total Portfolio Equity) / (Entry Price - Invalidation Stop Price)`
  * **Hard Structural Invalidation Stop:** Place hard stop below the 4H Volume Profile VAL.
  * **Two-Stage Profit Exit Protocol:**
    * **Stage 1 Exit (50% of Position):** Close 50% at `+2.5R` or upper 1D Garman-Klass volatility fan band; move stop to breakeven.
    * **Stage 2 Exit (Remaining 50%):** Trail behind the 4H VAL until 4H Rough Path Signature flips negative.

### CSU-10B: 1H Counter-Trend Pullback Within 4H/1D Uptrend ("Structural Dip Buy")
* **Trigger Condition A (The Telemetry Scan):**
  1. **4H & 1D Structural Signatures:** Remain firmly **positive (`>= +1.0 Z-score`)** above the 1D POC / 200D MA.
  2. **1H Tactical Signature:** Pulls back negatively (`1H A_P,V < 0` or minor leverage flush) directly into the **4H Volume Profile VAL or Developing POC**.
  3. **15m/1H Re-Alignment:** At the 4H VAL support shelf, 1H `A_CVD,OI` inflects back positive (`Domestic USD Spot CVD absorbs the dip`).
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** A routine intraday leverage shakeout inside an intact institutional bull trend—offering optimal asymmetric entry geometry.
  * **Probable Trajectory:** Resumption of the primary 4H/1D upward vector once 1H weak hands are cleared.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Entry Trigger:** Execute **Unleveraged Spot Long** upon 15m/1H VAL reclaim at the 4H support zone, sized to the full **0.75% Risk Ceiling** with stop directly below the 4H VAL swing low.

### CSU-10C: 1H Early Inflection Against Negative 4H/1D ("Tactical Capitulation Reversal")
* **Trigger Condition A (The Telemetry Scan):**
  1. **4H & 1D Structural Signatures:** Negative (`< -1.0 Z-score`), price has dropped into a major higher-timeframe support / liquidity pool (e.g., `$68,000` bid cluster or realized price band).
  2. **Exhaustion Prerequisite:** `MOD 03` confirms a deep OI wipeout (`>= -8% to -15%`) and `MOD 06` verifies passive limit-bid absorption on the 15m/1H footprint.
  3. **1H Tactical Ignition:** 1H Rough Path Signature (`A_P,V` and `A_CVD,OI`) surges above **`+1.75 Z-score`** and reclaims the 1H VAH.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Intraday institutional buyers are stepping in to catch a major structural sweep, though higher-timeframe overhead supply has not yet been fully cleared.
  * **Probable Trajectory:** Sharp tactical relief rally (`+4% to +10%`) toward the 4H POC / breakdown origin, which will then test whether the 4H regime itself can flip bullish.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Entry Trigger:** Execute **Reduced-Size Unleveraged Spot Long** upon 1H VAH reclaim.
  * **Position Sizing Formula (Half-Risk 0.375% Ceiling):**
    `Spot Position (BTC) = (0.00375 * Total Portfolio Equity) / (Entry Price - Invalidation Stop Price)`
  * **Hard Structural Invalidation Stop:** Strictly below the capitulation liquidity sweep low.
  * **Two-Stage Profit Exit Protocol:**
    * **Stage 1 Exit (70% of Position):** Take 70% profit at the **4H POC / breakdown origin** (respecting the `CB-04` 12H–24H half-life of a 1H signal); move stop to breakeven.
    * **Stage 2 Exit (Remaining 30%):** Hold only if 4H signature promotes to positive (`Mutation M1`); otherwise close 100% at 4H resistance.

### CSU-10D: Multi-Timeframe Regime Conflict ("Cross-Horizon Chop / Cash Lock")
* **Trigger Condition A (The Telemetry Scan):**
  1. 1H, 4H, and 1D Rough Path signatures oscillate with conflicting signs inside a wide multi-day Volume Profile Value Area (`1H positive, 4H negative, 1D flat`).
  2. Garman-Klass volatility is erratic and Domestic USD Spot CVD shows no net multi-day trend.
* **Observed Outcome B (The Mechanical Trajectory):**
  Unresolved battle between intraday mean-reversion bots and higher-timeframe distribution/accumulation—a classic chop-zone designed to bleed premature entries.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **ENFORCE 100% CASH LOCK.** Zero capital deployment until at least 1H and 4H signatures achieve directional resonance (`CSU-10A` or `CSU-10B`).

---

## 4. Dynamic Regime Mutation Lookup Matrix (`M1` through `M8`)

| Mutation ID | Initial State | Telemetry Mutation Observed (`Condition A'`) | Mechanical Meaning (`Outcome B'`) | Mandatory Execution Override (`Rule C'`) |
| :--- | :--- | :--- | :--- | :--- |
| **M1: 1H-to-4H Trend Promotion** | `CSU-10C` (Tactical Bounce) | Price holds above 4H POC and **4H Rough Path Signature (`A_P,V` & `A_CVD,OI`) flips above `+1.0 Z-score`**. | Tactical 1H bottom has successfully propagated into a structural 4H trend reversal. | Promote remaining 30% runner into a full swing hold; add second `0.375% Risk` tranche on 4H VAH retest. |
| **M2: 1H Bounce Crushed by 4H Supply** | `CSU-10C` (Tactical Bounce) | Price reaches 4H POC, 1H `A_CVD,OI` rolls over negative, and 4H sellers reject price back below 1H VAL. | Higher-timeframe structural downtrend reasserted control at resistance. | **Close 100% of Tactical Position Immediately; enforce 100% Cash Lock.** |
| **M3: 1H Lead Breakdown in Uptrend** | `CSU-10A` (Fractal Bull) | While 1D stays positive, **1H and 4H signatures both flip below `-1.25 Z-score`** and lose 4H VAL. | Multi-day uptrend is mutating into a deeper structural correction. | **Execute Stage 2 Full Exit** on open swing; step aside to cash until 4H/1D reset. |
| **M4: Half-Life Expiration Stall** | `CSU-10C` (Tactical Bounce) | 24 hours pass after 1H entry without price breaking 4H POC; 1H `A_P,V` decays back to `0.0`. | Signal half-life (`CB-04`) has expired without structural promotion. | **Exit at Market (Time Stop)** to avoid sitting in dead-money chop. |
| **M5: Macro-1D Veto Override** | `CSU-10A` / `10B` | 1D Rough Path Drift plunges below **`-2.0 Z-score`** on macro yield/ETF outflow shock. | Secular daily regime turned hostile; intraday signals are now traps. | **Immediate 100% Cash Lock across all timeframes.** |
| **M6: 15m-1H-4H Squeeze Cascade** | `CSU-10B` (Dip Buy) | From 4H VAL support, 15m, 1H, and 4H signatures all spike above `+1.5 Z` simultaneously with short liquidations (`MOD 01`). | Synchronized multi-timeframe squeeze ignition. | Hold full `0.75% Risk` position; execute Stage 1 exit only after perp basis crosses `0.00%`. |
| **M7: False 4H Breakout (1H Divergence)** | `CSU-10A` (False Signal) | Price pokes above 4H VAH, but **1H `A_CVD,OI` is steeply negative (`< -1.5 Z`)** (offshore perps chasing while USD spot sells). | Intraday order flow is contradicting the 4H candle breakout ("look-above-and-fail"). | **Block Entry / Tighten Stop to 1H VAL.** |
| **M8: Weekend Thin-Horizon Distortion** | Any State (Sat–Sun) | 1H signature spikes on low weekend liquidity while CME/ETF venues are closed (`1D volume < 30th percentile`). | Illiquid weekend path distortion prone to Sunday-night CME open mean reversion. | **Ignore Weekend 1H Breakout Signals; wait for Monday NY session confirmation (`MOD 17`).** |
