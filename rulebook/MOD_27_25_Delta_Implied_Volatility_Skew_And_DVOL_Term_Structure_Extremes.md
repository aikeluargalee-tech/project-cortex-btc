# PROJECT CORTEX-BTC — MODULE 27: 25-DELTA IMPLIED VOLATILITY SKEW & DVOL TERM STRUCTURE EXTREMES
**Waterfall Tier:** Pillar 3 (Options Fear/Greed Pricing, Tail-Risk Hedging Extremes & Volatility Term Structure) cross-verified with Pillar 1 (Macro) and Pillar 4 (Portfolio Engineering).
**Empirical Benchmark Anchor:** November 10–13, 2026 Deribit Volatility Surface Telemetry — Deribit 30-day Implied Volatility Index (**DVOL**) compressed in a multi-year low band at **39.8** (front-expiry ATM IV at **37.3**, pricing only a `+/- 3.0%` 1-SD move) prior to the macro CPI shock, demonstrating how **underpriced tail protection (`low DVOL + complacent skew`)** leaves the market unhedged and vulnerable to violent air-pocket drops when shocks hit.

---

## 1. Machine-Readable State & Routing Block (Python / Hermes / NotebookLM Index)

```yaml
module_id: "MOD_27"
entry_type: "CONDITIONAL_SIGNAL_UNIT"
waterfall_pillar: "PILLAR_3_OPTIONS_VOLATILITY_SURFACE"
title: "25-Delta Implied Volatility Skew & DVOL Term Structure Extremes"

# PILLAR 1 MASTER PERMISSION PRE-CHECK
pillar_1_permission_required: true
cash_lock_override: "If Pillar 1 Macro Regime == RISK_OFF_100_CASH, extreme put skew confirms institutional hedging panic—wait for skew mean-reversion + USD Spot CVD before entering."

# PRIMARY TELEMETRY TRIGGERS (OPTIONS VOLATILITY SURFACE)
base_regime_triggers:
  skew_25d_formula: "Skew_25D = IV(25_Delta_Put) - IV(25_Delta_Call) [Positive = Puts more expensive than Calls]"
  panic_put_skew_extreme: "30D Skew_25D >= +7.0% to +12.0%+ (or >= 92nd rolling 1Y percentile — extreme institutional crash-hedging demand)"
  euphoric_call_skew_extreme: "30D Skew_25D <= -4.0% to -8.0% (or <= 8th rolling 1Y percentile — calls priced far above puts; FOMO upside chasing)"
  term_structure_inversion: "Front-Month ATM IV minus Back-Month (90D) ATM IV >= +5.0 vol points (Volatility Backwardation = acute near-term panic)"
  dvol_complacency_squeeze: "Deribit DVOL <= 10th rolling 1Y percentile (benchmark DVOL ~39.8) ahead of major macro/market catalysts"

# ANTI-TRAP CIRCUIT BREAKERS
circuit_breakers:
  CB_01_PREMATURE_CLOSE: "NEVER buy a falling market just because 25-Delta Put Skew hits +8%; put skew can spike to +15% during a cascade. Wait for skew to peak and curl downward with Domestic USD Spot CVD."
  CB_02_VENUE_CONTAMINATION: "Standardize sign convention (Put IV minus Call IV) using constant-maturity 7D and 30D Deribit implied volatility surfaces."
  CB_03_FORCED_FLOW_STANDDOWN: "When Volatility Term Structure flips into steep backwardation (Front IV > Back IV by >= +8 pts), market makers are pricing acute short-term crash risk—enforce 100% Cash Lock."
  CB_04_SIGNAL_HALF_LIFE: "7D Skew captures immediate 48H-7D panic/euphoria inflection points; 30D Skew & DVOL govern multi-week structural positioning."

# RISK & SIZING CONSTANTS (PILLAR 4)
risk_parameters:
  max_portfolio_risk_pct: 0.75
  leverage_permitted: 1.0 # Strict Unleveraged Spot Only
  exit_protocol: "TWO_STAGE_STRUCTURAL"
```

---

## 2. Protective Circuit Breakers (Mandatory Pre-Execution Filters)

* **Circuit Breaker 1 — Sign Convention Standardization (`CB-02`):** Different analytics dashboards display 25-Delta Skew with opposite signs (`Put IV - Call IV` vs. `Call IV - Put IV`). In **Project CORTEX-BTC**, we standardize strictly on **`Skew_25D = IV(25Δ Put) − IV(25Δ Call)`**:
  * **High Positive (`+7% to +15%`):** Downside puts are vastly more expensive than upside calls (**Institutional Fear / Crash Hedging**).
  * **Deep Negative (`-4% to -10%`):** Upside calls are vastly more expensive than downside puts (**Retail/Fund Call FOMO Euphoria**).
* **Circuit Breaker 2 — Volatility Term Structure Backwardation Lock (`CB-03`):** Normally, 90-day IV is higher than 7-day IV (`Contango`). When 7-day ATM IV spikes sharply *above* 90-day ATM IV (`Backwardation`), options dealers are pricing immediate near-term crisis risk. Lock **100% Cash** until front-end IV cools back down.
* **Circuit Breaker 3 — Skew Peak Inflection Law (`CB-01`):** Extreme put skew (`>= +8%`) identifies a crowded hedge, **not** an instant entry. You enter *only* when put skew stops making higher highs and begins rolling over downward alongside positive **Domestic USD Spot CVD**.

---

## 3. Core Conditional Signal Units (`Condition A -> Outcome B -> Rule C`)

### CSU-27A: Extreme Put-Skew Panic Inflection ("Over-Hedged Capitulation Bottom")
* **Trigger Condition A (The Telemetry Scan):**
  1. `7D / 30D Skew_25D` spikes into the **`>= 92nd rolling percentile` (`+7.5% to +14.0%+`)** and Term Structure enters backwardation (`Front IV > Back IV`), reflecting panic institutional put buying at the lows.
  2. **Inflection Proof:** `Skew_25D` peaks and turns **downward (`dropping >= -2.0 vol points off peak`)** while price sweeps HTF support (`MOD 03A / 11A`) and **Domestic Fiat (USD) Spot CVD** turns positive.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Institutional funds have finished buying downside crash insurance; as spot stabilizes, put-option decay (`Vanna & Charm` dealer flows) forces market makers to **buy back short futures hedges**, fueling a powerful reflexive rebound.
  * **Probable Trajectory:** Sharp multi-day relief rally (`+6% to +14%`) powered by Vanna/Charm dealer short-covering and spot accumulation.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Entry Trigger:** Execute **Unleveraged Spot Long** upon confirmed **15m/1H VAL or VAH reclaim** coinciding with `Skew_25D` rolling downward off its panic peak and positive USD Spot CVD.
  * **Position Sizing Formula (0.75% Risk Ceiling):**
    `Spot Position (BTC) = (0.0075 * Total Portfolio Equity) / (Entry Price - Invalidation Stop Price)`
  * **Two-Stage Profit Exit Protocol:**
    * **Stage 1 Exit (50% of Position):** Close 50% once `Skew_25D` normalizes back to neutral (`+2% to +3%`) and Term Structure returns to contango; move stop to breakeven.
    * **Stage 2 Exit (Remaining 50%):** Trail behind 4H Volume Profile VAL.

### CSU-27B: Euphoric Call-Skew Blow-Off ("Upside Tail-Chasing Ceiling")
* **Trigger Condition A (The Telemetry Scan):**
  1. `7D / 30D Skew_25D` plunges into deep negative territory (**`<= -4.5% to -8.0%`**, `<= 8th rolling percentile`—calls trading at massive implied volatility premiums over puts).
  2. Coincides with high positive perp funding (`MOD 02B`) and flattening **Domestic USD Spot CVD** at overhead resistance / Call Wall.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Speculators are aggressively buying out-of-the-money calls to chase upside leverage while downside protection is completely neglected.
  * **Probable Trajectory:** High probability of a sharp mean-reversion pullback (`-6% to -15%`) that crushes call premiums and flushes late longs.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **EXECUTE STAGE 2 FULL PROFIT EXIT (100% OF OPEN SPOT SWING).** Lock Cash and ban new long entries until call skew normalizes.

### CSU-27C: Multi-Year DVOL Compression Complacency ("Unhedged Air-Pocket Warning")
* **Trigger Condition A (The Telemetry Scan):**
  1. **Deribit DVOL** compresses into the **`<= 10th rolling 1Y percentile` (`e.g., DVOL ~38–42`, benchmark 39.8 in Nov 2026)** with complacent low put skew (`< +2.5%`), **while** Pillar 1 macro catalysts (CPI, FOMC, rising 10Y yields) are approaching.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** The market is asleep and under-pricing macro tail risk; because dealers and funds carry minimal downside option protection, any negative macro surprise will trigger frantic spot/futures hedging sales (`gap-down air pocket`).
  * **Probable Trajectory:** Explosive upcoming volatility expansion (`DVOL surge from ~40 toward 55–65+`).
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **DO NOT CHASE LOW-VOLATILITY BREAKOUTS AHEAD OF MACRO PRINTS.** Enforce `MOD 12A` discipline—wait for the DVOL expansion move to print and confirm direction via Domestic USD Spot CVD before deploying capital.

### CSU-27D: Healthy Bull-Trend Skew Equilibrium ("Balanced Contango Drift")
* **Trigger Condition A (The Telemetry Scan):**
  1. `DVOL` sits in a moderate `45–60` range, Volatility Term Structure is in smooth **Contango** (`Back IV > Front IV` by `+2 to +5 pts`), and `Skew_25D` holds steady between **`-1.5% and +2.5%`**.
* **Observed Outcome B (The Mechanical Trajectory):**
  Balanced institutional hedging and organic spot demand—zero panic or blow-off distortion.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** Operate standard Pillar 2 & 3 swing triggers (`0.75% Risk Ceiling`) without volatility-surface penalties.

---

## 4. Dynamic Regime Mutation Lookup Matrix (`M1` through `M8`)

| Mutation ID | Initial State | Telemetry Mutation Observed (`Condition A'`) | Mechanical Meaning (`Outcome B'`) | Mandatory Execution Override (`Rule C'`) |
| :--- | :--- | :--- | :--- | :--- |
| **M1: Vanna/Charm Post-Event Crush** | `CSU-27A` (Panic Skew) | Macro event (CPI/FOMC) passes without catastrophe; **7D ATM IV drops `> -10 vol pts` in 6 hours** and `Skew_25D` drops from `+9%` to `+4%`. | Dealers unwind massive downside put hedges, mechanically buying spot/futures (`Vanna rally`). | **Authorize Immediate `0.75% Risk` Spot Long** upon 15m/1H VAH reclaim + USD Spot CVD. |
| **M2: Secondary Skew Spike (False Bottom)** | `CSU-27A` (Early Curl) | `Skew_25D` dips slightly from `+8%` to `+6.5%`, then **surges to a new high of `+11%+`** as price loses 1H VAL and USD Spot CVD turns negative. | Initial put-hedging pause was temporary; a second wave of institutional panic hedging just hit. | **Hard Stop Triggered / Enforce 100% Cash Lock.** |
| **M3: Complacent DVOL Breakdown Shock** | `CSU-27C` (Low DVOL ~40) | From `DVOL < 42`, a macro shock hits: **DVOL explodes `+12 vol pts` in 24h**, Term Structure flips into backwardation, and price loses 4H VAL. | Unhedged market caught off-guard; frantic scramble for downside protection accelerates selling. | **Immediate 100% Cash Lock (`CB-03`)** until DVOL peaks above `60+`. |
| **M4: Call-Overwriting Ceiling** | `CSU-27D` (Range) | `Skew_25D` drifts steadily more positive (`+3% to +5%`) even as spot price rises slowly—without panic. | Institutional spot holders are systematically selling covered calls (`overwrite programs`) into strength. | Expect dampened upside velocity; take **Stage 1 (50%) profits** conservatively at resistance. |
| **M5: Extreme Call-Skew + High Funding Sync** | `MOD 27B` + `MOD 02B` | `Skew_25D <= -5.0%` (calls wildly overpriced) AND 8H perp funding `> +0.035%` while USD Spot CVD diverges downward. | Double leverage blow-off top across both options and perpetual futures. | **Maximum Urgency Full Profit Exit (100% Cash).** |
| **M6: Term Structure Re-Steepening** | `CSU-27A` (Backwardation) | Front-month IV drops back below 90D IV (`Term Structure flips from Backwardation back to Contango`) while price holds above 4H VAL. | Acute crisis regime has officially transitioned back into normal market functioning. | Upgrade risk permission; trail remaining `Stage 2` swing runner confidently. |
| **M7: Whale Put-Spread Floor** | Downside Correction | Large block trades on Deribit sell downside puts (`e.g., $65K–$68K puts`) while buying upside calls (`Risk Reversal reversal`), flattening `Skew_25D`. | Institutional desks are underwriting a hard floor and positioning for a rebound. | Confirm with Domestic USD Spot CVD (`MOD 19`); prepare `0.75% Risk` Spot Long on VAL reclaim. |
| **M8: Weekend IV Decay Trap** | Friday `16:00 UTC` -> Sun | Market makers mark down weekend IV (`apparent DVOL dip`), creating a false sense of calm before Sunday `22:00 UTC` reopen. | Artificial weekend volatility markdown (`calendar decay`), not structural calm. | Do not treat Saturday DVOL dips as `M1` Vanna bullish signals; wait for Monday NY session. |
