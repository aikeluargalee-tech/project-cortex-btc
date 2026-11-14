# PROJECT CORTEX-BTC — MODULE 14: SOPR (SPENT OUTPUT PROFIT RATIO) PROFIT/LOSS RESET CYCLES
**Waterfall Tier:** Pillar 5 (On-Chain Cohorts & Realized Spending Behavior) cross-verified with Pillar 1 (Macro Permissions) and Pillar 4 (Portfolio Engineering).
**Empirical Benchmark Anchor:** November 2026 Spent Output Telemetry — Following the breakdown below the **$75,600–$75,771** Short-Term Holder cost basis into the **$68,000–$71,200** zone, Short-Term Holder SOPR (`STH-SOPR`) compressed below the **1.00 equilibrium line** (`0.96–0.98`), confirming net realized loss-taking by recent buyers while Long-Term Holder SOPR (`LTH-SOPR`) remained above `1.0`.

---

## 1. Machine-Readable State & Routing Block (Python / Hermes / NotebookLM Index)

```yaml
module_id: "MOD_14"
entry_type: "CONDITIONAL_SIGNAL_UNIT"
waterfall_pillar: "PILLAR_5_ONCHAIN_COHORTS"
title: "SOPR (Spent Output Profit Ratio) Profit/Loss Reset Cycles (1.0 Equilibrium Bounces vs. Rejections)"

# PILLAR 1 MASTER PERMISSION PRE-CHECK
pillar_1_permission_required: true
cash_lock_override: "If Pillar 1 Macro Regime == RISK_OFF_100_CASH, treat STH-SOPR bounces to 1.00 strictly as breakeven exit resistance—zero Long entries."

# PRIMARY TELEMETRY TRIGGERS (ON-CHAIN REALIZED PROFIT/LOSS RATIO)
base_regime_triggers:
  sopr_formula: "SOPR = Realized_Value_USD / Value_at_Creation_USD (for spent UTXOs)"
  primary_variants: "aSOPR (Entity-Adjusted > 1H) and STH-SOPR (Spent UTXOs < 155 days)"
  bull_reset_zone: "7D EMA of STH-SOPR dips to 0.985 - 1.002 and bounces upward while Price holds >= 200D MA"
  bear_rejection_zone: "7D EMA of STH-SOPR rallies from < 0.96 up to 0.995 - 1.005 and turns back down"
  capitulation_flush_zone: "Daily STH-SOPR <= 0.94 - 0.96 (<= 5th rolling 1Y percentile) with spike in realized loss USD"

# ANTI-TRAP CIRCUIT BREAKERS
circuit_breakers:
  CB_01_PREMATURE_CLOSE: "NEVER buy a single daily print of STH-SOPR < 0.97 while price is still falling; wait for SOPR to curl upward back toward 1.00 with Domestic USD Spot CVD."
  CB_02_VENUE_CONTAMINATION: "Use Entity-Adjusted SOPR (aSOPR) to filter out internal exchange wallet consolidations and intra-custodian transfers."
  CB_03_FORCED_FLOW_STANDDOWN: "When STH-SOPR is trapped below 1.00 for > 14 consecutive days, the 1.00 line acts as a ceiling of breakeven sellers—enforce Cash Lock."
  CB_04_SIGNAL_HALF_LIFE: "SOPR operates on a 24H-14D swing horizon; execute exact entries using Pillar 2 15m/1H Volume Profile VAL/VAH reclaims."

# RISK & SIZING CONSTANTS (PILLAR 4)
risk_parameters:
  max_portfolio_risk_pct: 0.75
  leverage_permitted: 1.0 # Strict Unleveraged Spot Only
  exit_protocol: "TWO_STAGE_STRUCTURAL"
```

---

## 2. Protective Circuit Breakers (Mandatory Pre-Execution Filters)

While `MVRV` (`MOD 13`) measures *unrealized* profit/loss sitting in wallets, **SOPR** measures *actual coins moving on-chain and locking in realized profit or loss*. Before acting on Module 14, four circuit breakers apply:
* **Circuit Breaker 1 — The 1.00 Equilibrium Polarity Rule (`CB-03`):**
  * **In a Bull Regime:** When `STH-SOPR` dips to `1.00`, holders refuse to sell at a loss, drying up spot supply and causing price to bounce immediately off `1.00`.
  * **In a Bear Regime:** When `STH-SOPR` has been below `1.00` for weeks, underwater holders wait anxiously to get back to breakeven. The moment price rallies enough to push `STH-SOPR` back up to `1.00`, they dump at breakeven—capping the rally.
* **Circuit Breaker 2 — Entity-Adjusted Filtering (`CB-02`):** Always use **Entity-Adjusted SOPR (`aSOPR`)** and `STH-SOPR` so internal exchange cold-to-hot wallet sweeps do not distort realized profit/loss ratios.
* **Circuit Breaker 3 — Capitulation Timing Filter (`CB-01`):** A deep `STH-SOPR` reading (`0.95`) tells you people are panicking *today*, not that the bottom is finished. Wait for `STH-SOPR` to stop making lower lows and confirm absorption on Pillar 2 order flow.
* **Circuit Breaker 4 — Pillar 1 Macro Permission Gate:** Verify secular liquidity and 200D MA status before trading a `1.00` SOPR reset bounce.

---

## 3. Core Conditional Signal Units (`Condition A -> Outcome B -> Rule C`)

### CSU-14A: Bullish SOPR Reset ("1.00 Equilibrium Supply Exhaustion Bounce")
* **Trigger Condition A (The Telemetry Scan):**
  1. Primary macro trend is bullish (Pillar 1 grants risk permission; price above 200D MA).
  2. Following a multi-day pullback, **7D EMA `STH-SOPR` (and `aSOPR`) compresses down to `0.985–1.002`** (brief minor loss-taking shakeout) and **curls upward back above `1.00`**.
  3. **Order-Flow Confirmation:** **Domestic Fiat (USD) Spot CVD** turns positive at 4H Volume Profile VAL, and `MOD 03` shows perp funding has normalized.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Weak short-term hands have finished flushing out at breakeven/slight loss; remaining holders refuse to sell below cost basis, creating an immediate on-chain supply vacuum.
  * **Probable Trajectory:** High-probability swing trend resumption upward as fresh spot demand meets depleted sell-side liquidity.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Entry Trigger:** Execute **Unleveraged Spot Long** upon a verified **15m/1H Volume Profile VAH or Developing POC reclaim** coinciding with `STH-SOPR` crossing back above `1.00`.
  * **Position Sizing Formula (0.75% Risk Ceiling):**
    `Spot Position (BTC) = (0.0075 * Total Portfolio Equity) / (Entry Price - Invalidation Stop Price)`
  * **Hard Structural Invalidation Stop:** Place hard stop beneath the 4H swing low where `STH-SOPR` bottomed.
  * **Two-Stage Profit Exit Protocol:**
    * **Stage 1 Exit (50% of Position):** Close 50% when `STH-SOPR` expands above `1.05–1.08` at overhead resistance; move stop to breakeven.
    * **Stage 2 Exit (Remaining 50%):** Trail behind 4H VAL or exit if `STH-SOPR` prints a bearish divergence (`price higher high, SOPR lower high`).

### CSU-14B: Bearish SOPR Rejection ("1.00 Breakeven Resistance Ceiling")
* **Trigger Condition A (The Telemetry Scan):**
  1. `STH-SOPR` has been depressed below `1.00` (`0.95–0.98`) for `>= 10–14 days` during a structural downtrend.
  2. Price stages a relief bounce, lifting **7D EMA `STH-SOPR` back up to `0.995–1.005`**, where it stalls and **turns back downward below `0.99`**.
  3. **Domestic Fiat (USD) Spot CVD** turns sharply negative at the bounce peak (`breakeven distribution`).
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Trapped short-term buyers used the relief rally to exit at breakeven, overwhelming intraday spot demand.
  * **Probable Trajectory:** Rejection of the relief rally and resumption of the downward leg toward lower liquidity pools.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **LOCK 100% CASH (Zero Spot Swing Exposure).** If holding any tactical bounce trade from lower levels, close 100% immediately as `STH-SOPR` hits `1.00` and stalls.

### CSU-14C: Profit-Taking Absorption ("Sustained High SOPR With Rising Price")
* **Trigger Condition A (The Telemetry Scan):**
  1. `aSOPR` and `LTH-SOPR` remain elevated (`1.05 to 1.15+`) for weeks as older coins realize substantial profits.
  2. **Absorption Proof:** Despite heavy on-chain profit realization, **price continues making higher highs**, **US Spot ETF inflows / Domestic USD Spot CVD** absorb every wave of profit-taking, and dips never break `STH-SOPR = 0.99`.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Bull-market wealth transfer is healthy—new institutional capital is large enough to absorb Long-Term Holder profit-taking without breaking market structure.
  * **Probable Trajectory:** Continued structural bull advance until either institutional inflows dry up (`Mutation M3`) or retail leverage overheats (`MOD 02`).
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **HOLD CORE SPOT SWING POSITION.** Continue trailing stops behind 4H Volume Profile VALs; do not prematurely exit a bull trend solely because `SOPR > 1.05` while price and USD Spot CVD keep climbing.

### CSU-14D: Capitulation Realized-Loss Climax ("STH-SOPR <= 0.94–0.96 Exhaustion")
* **Trigger Condition A (The Telemetry Scan):**
  1. Daily `STH-SOPR` plunges to **`<= 0.94–0.96`** (`<= 5th rolling percentile`), accompanied by a massive spike in net realized losses (`USD`).
  2. **Reversal Confirmation:** Within 24–72 hours, `STH-SOPR` prints a sharp **higher low** even as price retests or marginally sweeps the low, while **Domestic USD Spot CVD** turns positive and `MOD 03` confirms a full OI wipeout.
* **Observed Outcome B (The Mechanical Trajectory):**
  Panic sellers have dumped their coins at steep realized losses into institutional limit bids; marginal sellers at these prices are exhausted.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Entry Trigger:** Authorize **Unleveraged Spot Long** upon 15m/1H **VAL or Developing POC reclaim** following the `STH-SOPR` higher-low divergence, sized strictly to the **0.75% Risk Ceiling**.

---

## 4. Dynamic Regime Mutation Lookup Matrix (`M1` through `M8`)

| Mutation ID | Initial State | Telemetry Mutation Observed (`Condition A'`) | Mechanical Meaning (`Outcome B'`) | Mandatory Execution Override (`Rule C'`) |
| :--- | :--- | :--- | :--- | :--- |
| **M1: Bear-to-Bull 1.00 Breakout** | `CSU-14B` (Below 1.00) | `STH-SOPR` punches decisively **above `1.015`** and holds above `1.00` for `>= 5 days` alongside **positive US Spot ETF inflows + USD Spot CVD**. | Market absorbed all breakeven sellers; SOPR regime has flipped from bear ceiling to bull floor. | **Lift 100% Cash Lock.** Authorize `0.75% Risk` Spot Long on first pullback to `STH-SOPR = 1.00`. |
| **M2: Bull-to-Bear 1.00 Breakdown** | `CSU-14A` (1.00 Support) | `STH-SOPR` drops below `1.00`, attempts a bounce, **fails at `1.00`**, and plunges below **`0.975`** on negative USD Spot CVD. | Bull-market support reset failed and mutated into a `CSU-14B` underwater bear trap. | **Hard Stop Triggered / Enforce 100% Cash Lock.** |
| **M3: Profit-Absorption Failure** | `CSU-14C` (High SOPR Bull) | `LTH-SOPR` stays high (`> 1.10`), but **US Spot ETF inflows flip to multi-day outflows** and price breaks below 4H VAL. | Institutional demand can no longer absorb Long-Term Holder profit-taking. | **Execute Stage 2 Full Profit Exit (100% of Swing).** Lock Cash. |
| **M4: Multi-Day Compression at 1.00** | `CSU-14A` (Reset) | `STH-SOPR` hovers tightly between `0.998` and `1.002` for `>= 5 days` while Garman-Klass volatility squeezes below 15th percentile. | Extreme equilibrium between profit-takers and loss-refusers—imminent volatility expansion. | Prepare `MOD 11/12` VAH breakout trigger with USD Spot CVD confirmation. |
| **M5: STH Panic vs. LTH Inactivity** | `CSU-14D` (Capitulation) | `STH-SOPR` crashes to `0.95` while **`LTH-SOPR` stays completely flat (`~1.0–1.2` on tiny LTH volume)**. | Pure short-term tourist shakeout; veteran sovereign holders are refusing to sell a single coin. | High-conviction `CSU-14D` bottom setup; prepare `0.75% Risk` Spot Long on 15m/1H VAL reclaim. |
| **M6: LTH Capitulation Contagion** | `CSU-14D` (Severe Crash) | Both `STH-SOPR < 0.94` AND **`LTH-SOPR < 0.95`** (veteran holders selling at a loss on heavy volume). | Rare macro bear-market bottom capitulation (`cycle floor territory`), but extreme short-term volatility. | Stand down until `LTH-SOPR` reclaims `1.00`, then initiate sovereign cold-storage accumulation. |
| **M7: SOPR Bearish Divergence** | `CSU-14C` (Uptrend) | Price makes a higher high, but **`aSOPR` makes a sharp lower high** while USD Spot CVD flattens. | Fewer coins are able to realize profits on new highs—upside momentum is thinning out. | **Execute Stage 1 (50%) Profit Exit**; tighten trailing stop on remainder to 1H VAL. |
| **M8: Double-Bottom SOPR Curl** | `CSU-14D` (Capitulation) | Price makes a lower low (`e.g., $71.2K -> $68.0K`), while **`STH-SOPR` prints a higher low (`0.95 -> 0.975`)** with USD Spot CVD absorption. | Marginal loss-realization pressure is shrinking rapidly into the second sweep. | **Authorize `0.75% Risk` Spot Long** upon 15m/1H VAL reclaim. |
