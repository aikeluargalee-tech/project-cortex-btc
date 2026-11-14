# PROJECT CORTEX-BTC — MODULE 01: RISING OPEN INTEREST + EXTREME NEGATIVE PERPETUAL BASIS
**Waterfall Tier:** Pillar 3 (Derivatives & Market Fragility) cross-verified with Pillar 2 (Microstructure & Order Flow) and Pillar 4 (Portfolio Engineering).
**Empirical Benchmark Anchor:** November 12, 2026 Telemetry — Open Interest at **367.4K BTC** (**+22,000 BTC** 7-day expansion), Perpetual Basis at **-0.047%** across **156 consecutive hours** (bottom **1%** historical percentile), with exchange-level perpetual basis reaching **-0.058%** on Binance and **-0.048%** on OKX/Bybit alongside **-$1.1B** in 7-day futures net taker selling versus **+$32.5M** in 7-day spot net taker buying.

---

## 1. Machine-Readable State & Routing Block (Python / Hermes / NotebookLM Index)

```yaml
module_id: "MOD_01"
entry_type: "CONDITIONAL_SIGNAL_UNIT"
waterfall_pillar: "PILLAR_3_DERIVATIVES_FRAGILITY"
title: "Rising Open Interest + Extreme Negative Perpetual Basis (The Coiled Spring)"

# PILLAR 1 MASTER PERMISSION PRE-CHECK
pillar_1_permission_required: true
cash_lock_override: "If Pillar 1 Macro Regime == RISK_OFF_100_CASH, block all Long executions in Mod 01."

# PRIMARY TELEMETRY TRIGGERS (ROLLING PERCENTILE & Z-SCORE NORMALIZED)
base_regime_triggers:
  oi_7d_delta_pct_or_zscore: "OI 7D expansion >= +5% of total OI (or >= +1.5 Z-score; benchmark +22,000 BTC)"
  oi_total_btc_percentile: ">= 75th rolling 1Y percentile"
  perp_basis_pct: "<= -0.025% (or <= 5th historical percentile; benchmark -0.047% at 1st percentile)"
  perp_basis_streak_hours: ">= 72 consecutive hours below spot (benchmark 156 hours)"

# ANTI-TRAP CIRCUIT BREAKERS
circuit_breakers:
  CB_01_PREMATURE_CLOSE: "NEVER buy a daily/4H candle close without verified limit-book bid absorption and domestic USD Spot CVD divergence."
  CB_02_VENUE_CONTAMINATION: "Reject positive Aggregate Spot CVD if driven solely by offshore USDT pairs while Coinbase/Kraken USD Spot CVD and CME/ETF flows are negative."
  CB_03_FORCED_FLOW_STANDDOWN: "Stand down 100% during active cascading long liquidations or passive index rebalancing windows until 15m OI stabilizes."

# RISK & SIZING CONSTANTS (PILLAR 4)
risk_parameters:
  max_portfolio_risk_pct: 0.75
  leverage_permitted: 1.0 # Strict Unleveraged Spot Only
  exit_protocol: "TWO_STAGE_STRUCTURAL"
```

---

## 2. Protective Circuit Breakers (Mandatory Pre-Execution Filters)

Before any Scenario in Module 01 can authorize a spot entry, all four circuit breakers must pass:
* **Circuit Breaker 1 — Pillar 1 Macro Permission Gate:** Verify that secular macro permissions (200-Day Moving Average regime, sovereign yield impulse, and DXY trajectory) allow risk deployment. If Pillar 1 is in a **100% Cash Lock**, Module 01 signals are restricted strictly to **Defensive Stand-Down** or **Existing Position Exit**.
* **Circuit Breaker 2 — Domestic Fiat (USD) vs. Offshore (USDT) Venue Split:** Offshore spot positive CVD alone is insufficient. Verify that **Domestic Fiat Gateways (Coinbase/Kraken BTC-USD)** exhibit positive Spot CVD or a rising positive Coinbase Premium alongside net spot taker buying, and verify that CME Open Interest is not collapsing against offshore leverage expansion.
* **Circuit Breaker 3 — Order-Book Absorption Verification:** Do not buy a candle close simply because basis is in the bottom 1% of history. Limit-order absorption must be confirmed on the 15-minute/1-hour footprint (selling volume failing to displace price downward at Value Area Low or high-volume support nodes).
* **Circuit Breaker 4 — Forced-Liquidation Stand-Down:** If Open Interest is actively puking downward on red candles (long liquidation cascade in progress), all spot buy orders are frozen until Open Interest contraction decelerates and funding/basis volatility stabilizes.

---

## 3. Core Conditional Signal Units (`Condition A -> Outcome B -> Rule C`)

### CSU-01A: The Spot-Backed Short Squeeze ("The August 19 Precedent")
* **Trigger Condition A (The Telemetry Scan):**
  1. 7-day Open Interest expands significantly (`>= +5%` or `+1.5 Z-score`; benchmark `+22,000 BTC`) while Perpetual Basis remains in the bottom 1st–5th historical percentile (`<= -0.025%` to `-0.06%`) for `>= 72 hours`.
  2. **Perpetual CVD** slopes steeply negative (7-day futures net taker flow deeply negative, e.g., `-$1.1B`), confirming aggressive leveraged shorting.
  3. **Domestic Fiat (USD) Spot CVD** and net spot taker flow remain positive (spot absorbing futures selling), and price holds flat or prints higher lows above the 15m/1H Volume Profile Value Area Low (VAL).
  4. **Rough Path Signature (Verdict 0):** Price–Volume and Spot CVD–OI Lévy Signed Area confirms spot flow is leading contract creation with positive upward path curvature.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Unleveraged institutional spot buyers are absorbing every market-sell order fired by leveraged perpetual short sellers. Because every perpetual contract requires a 1:1 counterparty, the Open Interest surge consists of trapped leveraged shorts sitting underwater against a rising spot floor.
  * **Probable Trajectory:** Any upward spot catalyst forces sequential short margin breaches and automated market-buy liquidations (mirroring the August 19 precedent at `$69,335` that drove a `+14%` 7-day rally).
* **Execution Rule C (The Non-Negotiable Action):**
  * **Entry Trigger:** Execute **Unleveraged Spot Long** upon a verified 15-minute/1-hour footprint **Value Area High (VAH) reclaim** (or Developing POC breakout) accompanied by positive Domestic USD Spot CVD.
  * **Position Sizing Formula (0.75% Risk Ceiling):**
    `Spot Position (BTC) = (0.0075 * Total Portfolio Equity) / (Entry Price - Invalidation Stop Price)`
  * **Hard Structural Invalidation Stop:** Place hard stop immediately below the absorption swing low / Volume Profile VAL where limit bid absorption was verified.
  * **Two-Stage Profit Exit Protocol:**
    * **Stage 1 Exit (50% of Position):** Close 50% into the short-squeeze vertical impulse when **Perpetual Basis crosses above 0.00% into positive territory** AND **Open Interest drops by 5% to 8%** (confirming trapped shorts have been forcibly covered). Move stop on remaining 50% to breakeven.
    * **Stage 2 Exit (Remaining 50%):** Trail behind the 4H Volume Profile VAL or close fully if Domestic USD Spot CVD diverges negatively while Perp Basis spikes into overheated positive territory (`> +0.03%`).

### CSU-01B: The Passive Long-Trap Cascade ("Adler Correction Risk")
* **Trigger Condition A (The Telemetry Scan):**
  1. 7-day Open Interest expands (`>= +5%` or `+1.5 Z-score`) with Perpetual Basis negative (`<= -0.025%`) for `>= 72 hours`.
  2. **Domestic Fiat (USD) Spot CVD** slopes **negative or flat** (both spot and futures show aligned net taker outflows, e.g., 24H futures `-$1.2B` and spot `-$83.3M`, or CME OI drops while offshore OI rises).
  3. Price fails to reclaim the 1H Developing POC and breaks below the multi-day Volume Profile Value Area Low (VAL) on expanding volume.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Institutional spot buyers have stepped aside. The 1:1 long side of the Open Interest build-up is held by **offshore leveraged passive futures limit-buyers** borrowing into a falling market to catch a falling knife.
  * **Probable Trajectory:** With no genuine domestic spot bid floor beneath the market, aggressive perp selling pushes price below the margin maintenance threshold of passive futures longs, triggering a cascading **long-liquidation flush**.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **LOCK 100% CASH (Zero Spot Long Exposure).** If holding an existing spot swing position, execute an immediate protective exit upon the loss of the 1H VAL accompanied by negative Domestic Spot CVD.
  * **Knife-Catching Ban:** Do not place resting spot limit bids during the breakdown. Wait for **Module 03 (Deleveraging Flush & OI Reset)** conditions—specifically an Open Interest wipeout of `> 8% to 12%` and verified post-flush Domestic USD Spot CVD step-in.

### CSU-01C: Institutional Delta-Neutral Basis Compression (Synthetic Chop)
* **Trigger Condition A (The Telemetry Scan):**
  1. Open Interest rises steadily while Perpetual Basis sits moderately negative (`-0.01%` to `-0.035%`), while dated quarterly/CME futures maintain a standard money-market contango premium (`+5.3%` to `+5.7%` annualized).
  2. Spot ETF netflows or OTC spot purchases match the notional increase in short futures Open Interest.
  3. Garman-Klass (OHLC) volatility compresses into the bottom 20th percentile; price oscillates tightly around the Volume Profile Point of Control (POC).
* **Observed Outcome B (The Mechanical Trajectory):**
  The Open Interest expansion is driven by delta-neutral institutional hedging or cross-venue basis arbitrage rather than directional speculation. Upward price ticks will not trigger panic short-covering cascades because short futures legs are hedged by spot holdings.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **STANDBY / 100% CASH PRESERVATION.** Do not deploy swing capital inside a delta-neutral POC chop zone. Wait for a Garman-Klass volatility expansion paired with a directional Rough Path Signature breakout above VAH or below VAL.

### CSU-01D: Orderly Deleveraging & Mean Reversion (Signal Reset)
* **Trigger Condition A (The Telemetry Scan):**
  1. Perpetual Basis rises from its extreme discount back to `0.00%` or slightly positive.
  2. Total Open Interest contracts gradually by `5% to 8%+` over 48–96 hours **without** a violent price spike or crash.
* **Observed Outcome B (The Mechanical Trajectory):**
  Both leveraged longs and shorts have voluntarily closed their positions into neutral liquidity. The coiled spring has been disarmed without a liquidation cascade.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **DEACTIVATE MODULE 01 WATCH.** Cancel all squeeze-dependent pending triggers and transition the scanner to **Module 05 (Spot vs. Perp CVD Matrix)** and **Module 11 (Volume Profile Topology)** for standard trend evaluation.

---

## 4. Dynamic Regime Mutation Lookup Matrix (`M1` through `M8`)

| Mutation ID | Initial State | Telemetry Mutation Observed (`Condition A'`) | Mechanical Meaning (`Outcome B'`) | Mandatory Execution Override (`Rule C'`) |
| :--- | :--- | :--- | :--- | :--- |
| **M1: Squeeze Ignition** | `CSU-01A` (Accumulation) | Price reclaims 1H VAH + OI starts **dropping** (-2% to -5%) + Perp CVD spikes vertically **positive** + Basis jumps toward **0%**. | Trapped perp shorts have hit liquidation thresholds; forced market-buy covering is underway. | Hold Spot Long; prepare **Stage 1 Profit Exit (50%)** as Basis crosses **0.00%** and OI unwind reaches **-5% to -8%**. |
| **M2: Late-Long Hand-Off Trap** | `M1` (Active Squeeze) | Price rallies +8% to +14%, Basis flips **highly positive (> +0.025%)**, and **OI starts rising again** at the highs while USD Spot CVD flattens. | Shorts are gone; retail FOMO longs are opening high-leverage longs at the top while spot buyers stop bidding. | **Execute Stage 2 Exit (Close remaining 50% Spot Long immediately).** Transition to Module 02 (Crowded Positive Basis Warning). |
| **M3: Spot Bid Exhaustion** | `CSU-01A` (Accumulation) | Basis stays negative and OI stays high, but **Domestic USD Spot CVD flips negative** over a 4H/24H window (aligned spot + futures outflow). | Institutional spot absorbers have pulled their resting limit bids; perp sellers are about to overwhelm the book. | **Abort `CSU-01A` Watch.** If already in a Spot Long, exit at market ahead of the structural stop to preserve capital. |
| **M4: Long-Trap Breakdown** | `CSU-01B` (Fragile Floor) | Price breaks VAL + **OI drops sharply** (-5% to -12%) + Long liquidations exceed **85% of total liquidations**. | Passive leveraged futures longs are being forcibly liquidated into a thin spot order book. | **Enforce 100% Cash Lock.** Block all dip-buying until OI contraction halts and 15m footprint shows verified bid absorption. |
| **M5: Short-Pile-On Breakdown** | `CSU-01B` (Fragile Floor) | Price breaks support, Basis drops even deeper (**below -0.06%**), and **OI continues rising** into the breakdown. | Breakdown is driven by aggressive new momentum shorts piling in at the lows rather than long liquidations. | Stay **100% Cash** during initial impulse, but put **CSU-01A** on high alert: if Domestic USD Spot CVD steps in at lower HTF support, late breakdown shorts become massive squeeze fuel. |
| **M6: Premature Basis Flip** | `CSU-01A` / `01B` (Range Chop) | Price has **not** broken out, OI remains elevated, yet Basis/Funding flips **positive** mid-range. | Perp traders have flipped net long inside the chop before any short squeeze occurred—eliminating short-squeeze fuel. | **Cancel Bullish Squeeze Bias.** High OI + positive basis inside a stagnant range increases downside long-flush vulnerability. |
| **M7: Offshore Spoof Divergence** | `CSU-01A` (False Signal) | Aggregate Spot CVD or OI rises on **offshore USDT venues**, while **Coinbase USD Spot CVD**, **CME OI (-15%)**, and **Spot ETF netflows (-$299.8M)** are negative. | Offshore tether churn and retail dip-borrowing are masking domestic institutional exit. | **Circuit Breaker 2 Tripped: DO NOT ENTER.** Treat setup as `CSU-01B` (Downside Correction Risk) until USD gateways turn positive. |
| **M8: Post-Flush V-Bottom Reclaim** | `M4` (Long Cascade) | After a **> 8%** OI flush, price sweeps a major HTF liquidity low, reclaims VAL on the 15m chart, Basis stays deeply negative, and **USD Spot CVD surges**. | Weak leveraged longs have been wiped out; late panic shorts at the bottom are now trapped by institutional spot buyers. | **Authorize Spot Long Entry** under the **0.75% Risk Formula**, placing the invalidation stop below the capitulation wick low. |
