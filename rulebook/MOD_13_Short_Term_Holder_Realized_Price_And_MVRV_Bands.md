# PROJECT CORTEX-BTC — MODULE 13: SHORT-TERM HOLDER (STH) REALIZED PRICE & MVRV BANDS
**Waterfall Tier:** Pillar 5 (On-Chain Cohorts & Sovereign Defense) cross-verified with Pillar 1 (Macro Permissions) and Pillar 4 (Portfolio Engineering).
**Empirical Benchmark Anchor:** November 2026 On-Chain Cohort Telemetry — Bitcoin Short-Term Holder (STH, UTXOs `< 155 days`) Realized Price anchored at **$75,600–$75,771** (Glassnode / MacroMicro Nov 9–11, 2026) and True Market Mean at **$77,500**, with spot price breaking below **$75,600** and **$73,000** toward **$68,000**—placing the entire recent buyer cohort into unrealized loss (`STH-MVRV ~ 0.90–0.91`).

---

## 1. Machine-Readable State & Routing Block (Python / Hermes / NotebookLM Index)

```yaml
module_id: "MOD_13"
entry_type: "CONDITIONAL_SIGNAL_UNIT"
waterfall_pillar: "PILLAR_5_ONCHAIN_COHORTS"
title: "Short-Term Holder (STH) Realized Price & MVRV Bands (Cost-Basis Support & Traps)"

# PILLAR 1 MASTER PERMISSION PRE-CHECK
pillar_1_permission_required: true
cash_lock_override: "If Pillar 1 Macro Regime == RISK_OFF_100_CASH, treat STH Realized Price touches from below strictly as resistance—zero Long entries."

# PRIMARY TELEMETRY TRIGGERS (ON-CHAIN COHORT COST BASIS)
base_regime_triggers:
  sth_definition: "All UTXOs aged < 155 days (aggregate on-chain acquisition cost basis)"
  sth_mvrv_formula: "STH_MVRV = Spot_Price / STH_Realized_Price"
  bull_support_zone: "STH_MVRV between 0.98 and 1.03 while 1D/200D trend is positive"
  underwater_trap_zone: "STH_MVRV < 0.97 for >= 3 consecutive daily closes (benchmark < $73,000 against $75,600-$75,771 STH RP)"
  overheated_top_band: "STH_MVRV >= 1.30 to 1.40 (+1.5 to +2.0 SD band)"
  deep_capitulation_band: "STH_MVRV <= 0.80 to 0.85 (-1.5 SD band)"

# ANTI-TRAP CIRCUIT BREAKERS
circuit_breakers:
  CB_01_PREMATURE_CLOSE: "NEVER buy the first touch of STH Realized Price during a sell-off without 15m/1H footprint absorption and Domestic USD Spot CVD confirmation."
  CB_02_VENUE_CONTAMINATION: "Verify that cost-basis reclaims are backed by US Spot ETF inflows and Coinbase USD Spot CVD rather than offshore leveraged bounces."
  CB_03_FORCED_FLOW_STANDDOWN: "When Spot breaks > 3% below STH Realized Price, STH RP flips from support into heavy breakeven overhead supply—block all dip-buying until reclaimed."
  CB_04_SIGNAL_HALF_LIFE: "STH Realized Price is a multi-week structural anchor; combine with Pillar 2 Volume Profile VAH/VAL for exact intraday execution."

# RISK & SIZING CONSTANTS (PILLAR 4)
risk_parameters:
  max_portfolio_risk_pct: 0.75
  leverage_permitted: 1.0 # Strict Unleveraged Spot Only
  exit_protocol: "TWO_STAGE_STRUCTURAL"
```

---

## 2. Protective Circuit Breakers (Mandatory Pre-Execution Filters)

Before any Scenario in Module 13 can authorize a spot decision, all four circuit breakers must pass:
* **Circuit Breaker 1 — The Psychological Polarity Flip (`CB-03`):** Short-Term Holders (`< 155 days`) are the most price-sensitive cohort in Bitcoin. When price trades *above* STH Realized Price (`STH-MVRV > 1.0`), dips to their cost basis trigger defense and buying. Once price closes decisively *below* STH Realized Price (`STH-MVRV < 0.97`), those same holders are trapped underwater and aggressively sell into rallies to exit at breakeven—turning STH Realized Price into a brick wall of resistance.
* **Circuit Breaker 2 — Microstructure Entry Verification (`CB-01`):** On-chain metrics update on daily/hourly block intervals and cannot pinpoint exact stop-loss placement. Always drop down to **Pillar 2 (15m/1H Volume Profile VAL/VAH + USD Spot CVD)** to execute entries at STH bands.
* **Circuit Breaker 3 — Entity-Adjusted / ETF Cohort Calibration (`CB-02`):** Always verify that STH cost-basis reclaims align with positive US Spot ETF netflows and wallet cohort accumulation (`100–10,000 BTC` sharks/whales).
* **Circuit Breaker 4 — Pillar 1 Macro Gate:** In a macro liquidity contraction (`10Y yields > 5.0%`, `DXY > 103`, contracting stablecoins), `STH-MVRV < 1.0` signals prolonged bear-regime underwater stress rather than a quick V-bounce.

---

## 3. Core Conditional Signal Units (`Condition A -> Outcome B -> Rule C`)

### CSU-13A: Bull Market Cost-Basis Defense ("STH-MVRV = 1.00 Support Rebound")
* **Trigger Condition A (The Telemetry Scan):**
  1. Primary macro regime is bullish (`Price > 200D MA`, Pillar 1 grants risk permission).
  2. Price pulls back into the **STH Realized Price band (`STH-MVRV = 0.98 to 1.02`)** following a local rally.
  3. **Order-Flow Absorption:** At the STH cost-basis zone, 15m/1H Volume Profile VAL holds, **Domestic Fiat (USD) Spot CVD** turns sharply positive, and `MOD 03` confirms excess perp leverage has been flushed.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Recent bull-market entrants refuse to sell at a loss; instead, fresh spot buyers step in at aggregate breakeven to defend the structural uptrend.
  * **Probable Trajectory:** High-probability cyclical higher-low formation launching the next multi-week leg toward the `+1.0 SD` to `+1.5 SD` STH-MVRV band (`1.25–1.35`).
* **Execution Rule C (The Non-Negotiable Action):**
  * **Entry Trigger:** Execute **Unleveraged Spot Long** upon a confirmed **15m/1H VAH or Developing POC reclaim** directly above the STH Realized Price band.
  * **Position Sizing Formula (0.75% Risk Ceiling):**
    `Spot Position (BTC) = (0.0075 * Total Portfolio Equity) / (Entry Price - Invalidation Stop Price)`
  * **Hard Structural Invalidation Stop:** Place hard stop `2.5% to 3.5%` below STH Realized Price (beneath the 4H absorption swing low).
  * **Two-Stage Profit Exit Protocol:**
    * **Stage 1 Exit (50% of Position):** Close 50% at prior swing high / `STH-MVRV = 1.20`; move stop to breakeven.
    * **Stage 2 Exit (Remaining 50%):** Trail behind 4H VAL or exit fully at the `STH-MVRV >= 1.32` overheated band.

### CSU-13B: Cost-Basis Loss & Underwater Trap ("STH-MVRV Breakdown Below 0.97")
* **Trigger Condition A (The Telemetry Scan):**
  1. Spot price breaks decisively below **STH Realized Price** (`STH-MVRV < 0.97` for `>= 3 consecutive daily closes`, e.g., losing `$75,600` and breaking below `$73,000`).
  2. **Domestic Fiat (USD) Spot CVD** and US Spot ETF netflows are negative, and rallies back toward STH Realized Price stall with negative spot delta (`breakeven selling`).
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** The entire `< 155-day` buyer cohort is now underwater. Every bounce toward their cost basis meets automated limit-sell walls from trapped traders trying to get out even.
  * **Probable Trajectory:** Multi-week corrective markdown or range compression beneath STH Realized Price until weak hands capitulate down toward the True Market Mean or `-1.5 SD` STH band (`STH-MVRV ~ 0.80–0.85`).
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **LOCK 100% CASH (Zero Spot Swing Exposure).** Do not buy rallies into STH Realized Price from below. Wait either for a high-volume **Reclaim (`Mutation M1`)** or deep capitulation into **`CSU-13D`**.

### CSU-13C: Overheated Cohort Euphoria ("STH-MVRV >= +1.5 SD Distribution Band")
* **Trigger Condition A (The Telemetry Scan):**
  1. `STH-MVRV` surges into the **`1.30 to 1.40+` zone** (`>= 90th historical percentile`), meaning the average `< 155-day` holder is sitting on `+30% to +40%` unrealized profit.
  2. Long-Term Holder (LTH) spending accelerates (`MOD 15`) and perpetual funding spikes above `+0.030%/8h` (`MOD 02`).
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Unrealized profit temptation across short-term speculators reaches statistical saturation, triggering heavy profit-taking into late retail FOMO.
  * **Probable Trajectory:** High probability of a sharp `-10% to -20%` mean-reversion flush back toward the STH Realized Price (`MVRV = 1.0`).
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **EXECUTE STAGE 2 FULL PROFIT EXIT (100% OF TACTICAL SWING).** Lock Cash and refuse all new entries until `STH-MVRV` cools back toward `1.00–1.05`.

### CSU-13D: Deep Cohort Capitulation ("STH-MVRV <= 0.80–0.85 Extreme Discount")
* **Trigger Condition A (The Telemetry Scan):**
  1. `STH-MVRV` plunges to **`<= 0.80–0.85`** (`-1.5 SD` band, i.e., `15%–20%` below aggregate short-term cost basis) alongside extreme fear (`Fear & Greed <= 20`).
  2. Forced liquidation cascades complete (`MOD 03`), `100–10,000 BTC` whale/shark wallets shift to net accumulation, and **Domestic USD Spot CVD** prints a multi-day bullish divergence at HTF support.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Short-term capitulation is statistically exhausted; weak coins have been flushed into strong sovereign hands at a deep structural discount.
  * **Probable Trajectory:** Formation of a major macro bottom and asymmetric multi-month recovery back toward STH Realized Price (`MVRV = 1.0`).
* **Execution Rule C (The Non-Negotiable Action):**
  * **Entry Trigger:** Authorize **Unleveraged Spot Long** upon confirmed 4H/1D **Volume Profile VAL reclaim** backed by Domestic USD Spot CVD, sized strictly to the **0.75% Risk Ceiling** with stop beneath the capitulation low.

---

## 4. Dynamic Regime Mutation Lookup Matrix (`M1` through `M8`)

| Mutation ID | Initial State | Telemetry Mutation Observed (`Condition A'`) | Mechanical Meaning (`Outcome B'`) | Mandatory Execution Override (`Rule C'`) |
| :--- | :--- | :--- | :--- | :--- |
| **M1: Structural Cost-Basis Reclaim** | `CSU-13B` (Underwater Trap) | After trading below STH Realized Price, Bitcoin surges back above **STH RP (`STH-MVRV > 1.01`)** on **positive US Spot ETF inflows + USD Spot CVD**. | Underwater cohort has been absorbed; overhead resistance just flipped back into structural bull support. | **Lift `CSU-13B` Cash Lock.** Enter `0.75% Risk` Spot Long on the first 4H pullback retest of STH RP. |
| **M2: Failed Reclaim Rejection** | `CSU-13B` (Underwater Trap) | Price rallies directly up to STH Realized Price (`MVRV = 0.99–1.00`), prints heavy ask absorption, and **USD Spot CVD turns sharply negative**. | Trapped short-term holders dumped at breakeven; bears defended the resistance ceiling. | **Maintain Strict 100% Cash Lock.** Prepare for next leg down toward `-1.0 SD` band. |
| **M3: Bull Support Slice-Through** | `CSU-13A` (Support Test) | Price touches STH Realized Price, bounces weakly for 24h, then **breaks below `STH-MVRV = 0.97` on rising OI and ETF outflows**. | Bull-market cost-basis defense failed; regime has mutated into `CSU-13B` underwater trap. | **Hard Stop Triggered / Exit Immediately.** Lock 100% Cash. |
| **M4: True Market Mean Cushion** | `CSU-13B` (Underwater Trap) | Price loses STH Realized Price (`$75.6K`) but finds massive **Domestic USD Spot CVD absorption** at the **True Market Mean** (`active investor cost basis`). | Long-horizon active capital stepped in to catch the dip between STH RP and deep capitulation. | Monitor 1H/4H VAH reclaim at True Market Mean for a tactical `0.375%–0.75%` swing entry. |
| **M5: Cohort Aging Reset** | `CSU-13B` (Sideways Chop) | Price chops sideways below STH RP for 60–120 days without crashing; **STH Realized Price drifts downward** to meet spot price (`MVRV -> 1.0`). | Underwater coins aged past 155 days into LTH status, removing overhead breakeven sell pressure via time. | Watch for VAH breakout with USD Spot CVD once `STH-MVRV` crosses cleanly above `1.00`. |
| **M6: Mid-Bull Band Walk** | `CSU-13A` (Uptrend) | Price rides steadily between `STH-MVRV = 1.08` and `1.22` for weeks with steady US Spot ETF inflows and neutral funding. | Healthy institutional bull expansion without speculative blow-off excess. | **Hold Core Spot Swing Position**; trail stops beneath 4H VALs. |
| **M7: Double-Top MVRV Divergence** | `CSU-13C` (Overheated) | Price makes a marginal higher high, but **`STH-MVRV` prints a lower high** (because rapid churn raised the STH cost basis near the top). | Average buyer cost basis is now dangerously close to spot price—tiny dip puts everyone underwater. | **Execute Immediate 100% Profit Exit.** Extreme fragility warning. |
| **M8: Sovereign Cold-Storage Tranche** | `CSU-13D` (Deep Discount) | `STH-MVRV <= 0.82` coincides with `200W MA` / Realized Price touch and Pillar 1 macro stabilization. | Generational sovereign accumulation window. | Execute tactical `0.75% Risk` swing entry AND allocate sovereign cold-storage capital (`MOD 18`). |
