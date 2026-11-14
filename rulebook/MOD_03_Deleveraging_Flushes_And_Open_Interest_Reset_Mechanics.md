# PROJECT CORTEX-BTC — MODULE 03: DELEVERAGING FLUSHES & OPEN INTEREST RESET MECHANICS
**Waterfall Tier:** Pillar 3 (Derivatives & Market Fragility) cross-verified with Pillar 2 (Microstructure & Order Flow) and Pillar 4 (Portfolio Engineering).
**Empirical Benchmark Anchor:** November 12–13, 2026 & Historical Reset Benchmarks — Binance BTC futures Open Interest contracting **~17%** from **$10.6B down to $8.8B** (echoing the June 2026 reset below **$60,000** that preceded a **+45%** expansion above **$87,000**), alongside intra-day liquidation cascades reaching **$304.50M (87% Longs)** on the flush from **$74,771.4** to **$71,218.1**.

---

## 1. Machine-Readable State & Routing Block (Python / Hermes / NotebookLM Index)

```yaml
module_id: "MOD_03"
entry_type: "CONDITIONAL_SIGNAL_UNIT"
waterfall_pillar: "PILLAR_3_DERIVATIVES_FRAGILITY"
title: "Deleveraging Flushes & Open Interest Reset Mechanics (Partial vs. Full Wipeouts)"

# PILLAR 1 MASTER PERMISSION PRE-CHECK
pillar_1_permission_required: true
cash_lock_override: "If Pillar 1 Macro Regime == RISK_OFF_100_CASH, block all post-flush Long entries until secular MA/liquidity gates recover."

# PRIMARY TELEMETRY TRIGGERS (ROLLING PERCENTILE & Z-SCORE NORMALIZED)
base_regime_triggers:
  oi_contraction_pct: "Rapid 24h-72h OI drop >= -6% (or multi-week structural OI reset >= -12% to -20%)"
  liquidation_spike_zscore: "24h/4h forced liquidations >= +2.5 Z-score (>= 95th rolling percentile)"
  liquidation_skew_pct: "Single-sided liquidation dominance >= 80% (Longs or Shorts)"
  funding_basis_compression: "Perp basis/funding collapses from extreme (>= +0.025% or <= -0.025%) back toward 0.00% neutral"

# ANTI-TRAP CIRCUIT BREAKERS
circuit_breakers:
  CB_01_PREMATURE_CLOSE: "NEVER buy the first red liquidation candle close; wait for OI contraction to decelerate and 15m footprint absorption to print."
  CB_02_VENUE_CONTAMINATION: "Verify that post-flush buying comes from Domestic Fiat (USD) Spot CVD rather than offshore leveraged dip-gamblers reloading perps."
  CB_03_FORCED_FLOW_STANDDOWN: "Mandatory 100% Cash freeze while 1H OI is still falling > -1.5% per hour (active margin cascade in progress)."
  CB_04_SIGNAL_HALF_LIFE: "Distinguish between a 4H tactical liquidation bounce and a true multi-week structural OI reset."

# RISK & SIZING CONSTANTS (PILLAR 4)
risk_parameters:
  max_portfolio_risk_pct: 0.75
  leverage_permitted: 1.0 # Strict Unleveraged Spot Only
  exit_protocol: "TWO_STAGE_STRUCTURAL"
```

---

## 2. Protective Circuit Breakers (Mandatory Pre-Execution Filters)

Before any Scenario in Module 03 can authorize a spot entry after a flush, all four circuit breakers must pass:
* **Circuit Breaker 1 — Active Cascade Freeze (`CB-03`):** Never catch a falling knife while Open Interest is still contracting sharply (`> -1.5% per hour`) and forced liquidations are accelerating. You only act **after** the liquidation engine finishes clearing weak hands.
* **Circuit Breaker 2 — Partial vs. Full Reset Audit:** A shallow `-2% to -4%` OI dip leaves 95% of crowded leverage intact and frequently leads to a **second, deeper liquidation wave**. High-conviction post-flush entries require either a rapid `-8% to -12%+` cascade wipeout or a multi-week `-15%+` structural OI reset.
* **Circuit Breaker 3 — Post-Flush Domestic Spot Verification (`CB-02`):** After a long liquidation flush, observe *who* buys the bounce. If Open Interest immediately surges back up while **Domestic USD Spot CVD** stays negative, offshore gamblers are reloading leverage—a classic dead-cat bounce trap.
* **Circuit Breaker 4 — Pillar 1 Macro Regime Check:** In a confirmed bear-market macro contraction (below 200D MA with contracting global liquidity), post-flush bounces are short-lived relief rallies rather than multi-week trend reversals.

---

## 3. Core Conditional Signal Units (`Condition A -> Outcome B -> Rule C`)

### CSU-03A: Full Capitulation Flush & V-Bottom Absorption ("Complete Leverage Reset")
* **Trigger Condition A (The Telemetry Scan):**
  1. Open Interest suffers a deep, decisive wipeout (`>= -8% to -15%` rapid cascade or `>= -15% to -20%` structural contraction, e.g., Binance OI dropping `-17%` from `$10.6B` to `$8.8B`), accompanied by `>= 85%` long liquidation dominance (`>= +2.5 Z-score`).
  2. Perpetual funding and basis reset completely from overheated levels back to **neutral (`0.00%`) or slightly negative**.
  3. **OI Contraction Halts:** Open Interest flattens out for `>= 2 to 4 hours` (proving forced selling is finished), while **Domestic Fiat (USD) Spot CVD** turns sharply **positive** at a higher-timeframe support or Volume Profile VAL.
  4. **Price Reclaim:** Price sweeps a major liquidity low (capitulation wick) and reclaims the 15m/1H **Value Area Low (VAL)** or Developing POC.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** The derivatives market has been purged of weak, over-leveraged speculators, transferring coins from forced sellers into unleveraged institutional spot hands at discounted valuations (mirroring the June 2026 reset below `$60,000` prior to the `+45%` rally).
  * **Probable Trajectory:** With overhead forced-selling supply exhausted and clean order books above, modest spot accumulation drives a sustained, low-resistance structural recovery.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Entry Trigger:** Execute **Unleveraged Spot Long** upon the confirmed **15m/1H VAL reclaim** backed by rising Domestic USD Spot CVD and flat/low Open Interest.
  * **Position Sizing Formula (0.75% Risk Ceiling):**
    `Spot Position (BTC) = (0.0075 * Total Portfolio Equity) / (Entry Price - Invalidation Stop Price)`
  * **Hard Structural Invalidation Stop:** Place hard stop strictly below the **capitulation liquidation wick low**. (If the wick is wide, reduce BTC position size proportionally so maximum dollar loss never exceeds `0.75%` of portfolio equity).
  * **Two-Stage Profit Exit Protocol:**
    * **Stage 1 Exit (50% of Position):** Close 50% at the prior breakdown origin / mid-range Volume Profile POC (`+1.5R to +2.5R`). Move stop on remaining 50% to breakeven.
    * **Stage 2 Exit (Remaining 50%):** Trail behind the 4H Volume Profile VAL or exit if Open Interest rebuilds too rapidly with negative USD Spot CVD.

### CSU-03B: Partial Flush Dead-Cat Bounce ("Unfinished Deleveraging Trap")
* **Trigger Condition A (The Telemetry Scan):**
  1. Price drops sharply into support, triggering a **small/partial OI contraction (`only -2% to -4.5%`)**, leaving total Open Interest still above the **75th rolling percentile**.
  2. Price bounces 1%–3%, and **Open Interest immediately spikes back upward** (`new leveraged longs jumping back in`) while **Perpetual Basis remains elevated** (`> +0.015%`).
  3. **Domestic Fiat (USD) Spot CVD** continues sloping **negative** during the bounce (`Aligned Outflow` across 1H/4H/24H windows).
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** The initial drop failed to clear out the crowded leverage; instead, retail dip-buyers immediately added fresh leverage on top of an un-reset market while spot holders continued distributing.
  * **Probable Trajectory:** High probability of a **secondary, deeper liquidation leg** that takes out the initial wick low to finish the deleveraging process.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **LOCK 100% CASH (Zero Spot Long Exposure).** Do not buy the first bounce. Wait for the secondary flush to complete and satisfy `CSU-03A` full reset criteria.

### CSU-03C: Short-Cover Blow-Off Climax ("Upside Deleveraging Exhaustion")
* **Trigger Condition A (The Telemetry Scan):**
  1. Price spikes vertically upward while **Open Interest drops sharply (`-5% to -12%`)** and **Short Liquidations exceed 85%–95%** of total liquidations (`e.g., 4H liquidations 97% Shorts at $29.44M vs. $954K Longs`).
  2. Perpetual basis surges from deep negative into positive territory (`> +0.020%`), while **Domestic USD Spot CVD flattens or turns negative** at the top of the spike.
* **Observed Outcome B (The Mechanical Trajectory):**
  The vertical rally was fueled almost entirely by **forced short covering** rather than organic new spot demand. Once the last trapped short is liquidated, the mechanical bid vanishes abruptly.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **DO NOT CHASE / EXECUTE PROFIT TAKING.** If holding an existing Spot Swing Long from a squeeze setup (`MOD 01`), execute **Stage 1 or Stage 2 Profit Exit** directly into the short-liquidation climax. Lock Cash and wait for a post-squeeze pullback retest.

### CSU-03D: Quiet Time-Correction Leverage Bleed ("Voluntary Position Unwind")
* **Trigger Condition A (The Telemetry Scan):**
  1. Over 7 to 21 days of sideways price consolidation, Open Interest drifts steadily downward by **`-10% to -18%`** *without* single-day liquidation spikes (`liquidations < 50th percentile`).
  2. Funding rates normalize to baseline (`+0.005% to +0.010%/8h`), Garman-Klass volatility compresses into the bottom decile, and **Domestic USD Spot CVD** slowly accumulates higher lows.
* **Observed Outcome B (The Mechanical Trajectory):**
  Impatient leveraged speculators are voluntarily closing positions due to boredom and funding decay, while quiet institutional spot accumulation absorbs the supply without moving price. This creates the cleanest, lowest-fragility launchpad for a new macro impulse.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Entry Trigger:** Prepare **Unleveraged Spot Long** entry upon a Garman-Klass volatility squeeze breakout above the multi-week Volume Profile **VAH** confirmed by positive Rough Path Signature (`Verdict 0`) and Domestic USD Spot CVD. Size strictly to the **0.75% Risk Ceiling**.

---

## 4. Dynamic Regime Mutation Lookup Matrix (`M1` through `M8`)

| Mutation ID | Initial State | Telemetry Mutation Observed (`Condition A'`) | Mechanical Meaning (`Outcome B'`) | Mandatory Execution Override (`Rule C'`) |
| :--- | :--- | :--- | :--- | :--- |
| **M1: Cascade Deceleration** | Active Long Flush | Hourly OI drop slows from `-3%/hr` to `< -0.3%/hr`, liquidation volume drops by `> 70%`, and 15m footprint prints high-volume bid absorption. | Forced margin selling has exhausted available trapped longs at this price tier. | Lift `CB-03` freeze; move to **High-Alert Watch** for `CSU-03A` 15m VAL reclaim. |
| **M2: Secondary Waterfall Leg** | `CSU-03B` (Partial Flush) | Price fails to reclaim 1H POC, breaks below the initial flush wick low, and **OI drops another `-5% to -10%`**. | The partial flush mutated into a full two-stage capitulation cascade. | **Stay 100% Cash** during the second drop; re-evaluate `CSU-03A` only after the new low stabilizes. |
| **M3: Leverage Reload Trap** | `CSU-03A` (Post-Flush) | Immediately after a flush, **OI jumps `+4%` in 4 hours** and funding spikes above `+0.025%` while **USD Spot CVD stays flat/negative**. | Offshore gamblers are front-running the bottom with fresh leverage without spot support. | **Abort Spot Long Entry.** Market remains fragile and vulnerable to another stop-hunt sweep. |
| **M4: Spot-Led Organic Recovery** | `CSU-03A` (Post-Flush) | Price rallies `+5% to +10%` off the flush low while **OI stays flat or rises slowly** and **Domestic USD Spot CVD leads upward**. | Healthy, spot-driven structural recovery with low liquidation fragility. | **Hold Spot Long**; execute **Stage 1 (50%) exit** at first HTF resistance and trail remainder. |
| **M5: Short-Cover Dead Cat** | `CSU-03C` (Short Spike) | 4H short liquidations hit `> 90%`, price hits 1H VAH, then **USD Spot CVD turns negative** and price falls back inside the range. | Bounce was purely a mechanical short-cover spike inside a broader downtrend. | **Exit any tactical swing immediately; enforce 100% Cash Lock.** |
| **M6: Multi-Week Reset Completion** | `CSU-03D` (Time Bleed) | Total OI reaches a multi-month low (`-15% to -20%` off peak), Spot ETF outflows flip to net inflows, and price reclaims 200D MA / HTF POC. | Full macro-derivatives reset complete; structural bull regime is re-initializing. | **Authorize Full Tier-1 Spot Swing Allocation** (capped at `0.75%` stop risk per entry). |
| **M7: Contagion / Solvency Shock** | Any Flush State | OI drops `> -20%` alongside stablecoin de-pegging, extreme negative basis (`< -0.15%`), and widening credit/yield stress (Pillar 1 breach). | Systemic market-structure shock rather than routine leverage cleanup. | **Pillar 1 Override: Lock 100% Cash & Verify Sovereign Cold-Storage Custody.** |
| **M8: Silent Spot Divergence** | `CSU-03D` (Time Bleed) | Price makes a marginal lower low on declining OI, while **Domestic USD Spot CVD prints a clear higher low** (bullish divergence). | Institutional spot buyers are quietly absorbing the final trickle of forced/voluntary sellers. | Prepare `0.75% Risk` Spot Long entry upon 15m/1H Developing POC reclaim. |
