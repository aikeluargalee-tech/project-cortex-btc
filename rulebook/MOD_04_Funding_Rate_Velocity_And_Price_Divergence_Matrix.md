### PROJECT CORTEX-BTC — MODULE 04: FUNDING RATE VELOCITY & PRICE DIVERGENCE MATRIX
**Waterfall Tier:** Pillar 3 (Derivatives & Market Fragility) cross-verified with Pillar 2 (Microstructure & Order Flow) and Pillar 4 (Portfolio Engineering). **Empirical Benchmark Anchor:** November 12, 2026 Cross-Venue Funding Telemetry — OI-weighted 8-hour perpetual funding averaging **+0.0073% to +0.0075%** (**8.02%–8.24% APR**), exhibiting sharp cross-venue dispersion between domestic/on-chain venues (**+0.0021% on Hyperliquid**, **+0.0024% on Coinbase CDE**) and offshore retail venues (**+0.0080% on Binance**, **+0.0082% on Bybit**, **+0.0100% / 10.95% APR on OKX**).

--------------------------------------------------------------------------------

#### 1. Machine-Readable State & Routing Block (Python / Hermes / NotebookLM Index)
```yaml
module_id: "MOD_04"
entry_type: "CONDITIONAL_SIGNAL_UNIT"
waterfall_pillar: "PILLAR_3_DERIVATIVES_FRAGILITY"
title: "Funding Rate Velocity & Price Divergence Matrix (Disbelief Rallies vs. Backwardation Panic)"

# PILLAR 1 MASTER PERMISSION PRE-CHECK
pillar_1_permission_required: true
cash_lock_override: "If Pillar 1 Macro Regime == RISK_OFF_100_CASH, block all Long executions regardless of bullish funding divergences."

# PRIMARY TELEMETRY TRIGGERS (ROLLING PERCENTILE & Z-SCORE NORMALIZED)
base_regime_triggers:
  funding_velocity_24h_zscore: "24h-72h rate of change in OI-weighted funding (Delta_F) >= +2.0 Z-score or <= -2.0 Z-score"
  price_funding_correlation_72h: "Rolling 72h correlation between Price Delta and Funding Delta <= -0.50 (Strong Divergence)"
  cross_venue_spread_bps: "Offshore (Binance/OKX) 8h funding minus Domestic/DEX (Coinbase/Hyperliquid) >= +0.0060% (6 bps)"

# ANTI-TRAP CIRCUIT BREAKERS
circuit_breakers:
  CB_01_PREMATURE_CLOSE: "NEVER enter solely because funding turns negative; negative funding in a spot-selling bear trend simply reflects persistent downward pressure."
  CB_02_VENUE_CONTAMINATION: "Always normalize 1-hour funding venues (Coinbase, Hyperliquid) to 8-hour equivalents and weight by BTC Open Interest before computing velocity."
  CB_03_FORCED_FLOW_STANDDOWN: "Stand down during violent funding regime flips accompanied by cascading liquidations until 15m/1H Volume Profile structure stabilizes."
  CB_04_SIGNAL_HALF_LIFE: "Funding velocity is a 12H-7D tactical positioning gauge; never let it override Pillar 1 secular liquidity or Pillar 5 on-chain cost basis."

# RISK & SIZING CONSTANTS (PILLAR 4)
risk_parameters:
  max_portfolio_risk_pct: 0.75
  leverage_permitted: 1.0 # Strict Unleveraged Spot Only
  exit_protocol: "TWO_STAGE_STRUCTURAL"
```

--------------------------------------------------------------------------------

#### 2. Protective Circuit Breakers (Mandatory Pre-Execution Filters)
Before any Scenario in Module 04 can authorize a spot decision, all four circuit breakers must pass:
*   **Circuit Breaker 1 — OI-Weighted Normalization (CB-02):** Different exchanges settle funding on different schedules (Binance/Bybit/OKX every 8 hours; Coinbase CDE/Hyperliquid every 1 hour). Always normalize all rates to an **8-hour OI-weighted composite** (Rate_8h = Rate_1h * 8) and track the **spread between offshore retail venues and domestic USD venues**.
*   **Circuit Breaker 2 — Negative Funding Fallacy Filter (CB-01):** A common retail error is assuming negative funding is automatically bullish. Negative funding is only bullish when **Price is holding support or rising** and **Domestic USD Spot CVD is positive** (Disbelief Rally). If Price and Domestic Spot CVD are both falling, negative funding simply confirms an active downtrend.
*   **Circuit Breaker 3 — Pillar 1 Macro Permission Gate:** Even a textbook Disbelief Rally divergence is capped in duration if Pillar 1 (Macro Liquidity & 200D MA) is in a **100% Cash Lock**.
*   **Circuit Breaker 4 — Velocity Exhaustion Filter:** When funding velocity spikes vertically (> +2.5 Z-score in < 24 hours) without matching Spot CVD acceleration, the move is driven by synthetic leverage chasing and is prone to sharp mean reversion.

--------------------------------------------------------------------------------

#### 3. Core Conditional Signal Units (Condition A -> Outcome B -> Rule C)
##### CSU-04A: The Disbelief Rally ("Price Rising While Funding Compresses or Stays Negative")
*   **Trigger Condition A (The Telemetry Scan):**
    1. **Price Slope (Delta_P):** Spot price trends higher over 48–168 hours, printing higher highs and higher lows above the 4H Developing POC.
    2. **Funding Velocity (Delta_F):** OI-weighted 8-hour funding **falls or remains compressed/negative** (<= +0.0030% down to -0.020%, rolling 72h Price-Funding correlation <= -0.50).
    3. **Spot Confirmation:** **Domestic Fiat (USD) Spot CVD** slopes steadily **positive** while Perpetual CVD lags or trends negative (traders are shorting every bounce in futures while unleveraged spot buyers absorb).
    4. **Rough Path Signature (Verdict 0):** Price–Volume Lévy Signed Area confirms volume-backed upward path curvature.
*   **Observed Outcome B (The Mechanical Trajectory):**
    *   **Sovereign Macro Lens:** This is the highest-quality, most sustainable bullish structure in Bitcoin markets. Real spot capital is driving price higher while skeptical futures traders continuously short the rally—creating a self-fueling ladder of trapped short liquidity without any long-side funding overhang.
    *   **Probable Trajectory:** Persistent upward grind punctuated by sharp, sudden short-squeeze candles whenever resistance levels break, continuing until skepticism finally turns into FOMO (funding flips steeply positive).
*   **Execution Rule C (The Non-Negotiable Action):**
    *   **Entry Trigger:** Execute **Unleveraged Spot Long** on any minor pullback to the 1H Volume Profile **POC or VAL** where funding dips further negative and Domestic USD Spot CVD holds firm.
    *   **Position Sizing Formula (0.75% Risk Ceiling):** Spot Position (BTC) = (0.0075 * Total Portfolio Equity) / (Entry Price - Invalidation Stop Price)
    *   **Hard Structural Invalidation Stop:** Place hard stop below the prior 4H swing higher-low / Volume Profile VAL.
    *   **Two-Stage Profit Exit Protocol:**
        *   **Stage 1 Exit (50% of Position):** Hold through the disbelief grind until funding finally capitulates upward (crosses above +0.020%/8h with a sharp short-liquidation spike); close 50% and move stop to breakeven.
        *   **Stage 2 Exit (Remaining 50%):** Exit remaining 50% when funding hits the >= 90th percentile (> +0.035%/8h) and Domestic USD Spot CVD flattens.

##### CSU-04B: Disbelief Dip-Buying ("Price Falling While Funding Spikes Higher")
*   **Trigger Condition A (The Telemetry Scan):**
    1. **Price Slope (Delta_P):** Spot price declines steadily over 24–96 hours, losing key 1H/4H Volume Profile support nodes.
    2. **Funding Velocity (Delta_F):** OI-weighted 8-hour funding **rises sharply** (e.g., from +0.005% to +0.020%+, especially on offshore retail venues like OKX/Binance), with rolling 72h Price-Funding correlation <= -0.50.
    3. **Spot Confirmation:** **Domestic Fiat (USD) Spot CVD** and US Spot ETF netflows are **negative** (spot distribution into leveraged retail dip-buyers).
*   **Observed Outcome B (The Mechanical Trajectory):**
    *   **Sovereign Macro Lens:** As price drops, retail futures traders aggressively buy the dip with high leverage, bidding perpetual futures *above* the falling spot price and paying high funding rates to institutional spot sellers who are offloading inventory.
    *   **Probable Trajectory:** Extremely fragile structure. Because dip-buyers are using margin rather than unleveraged spot, continued spot selling forces those leveraged dip-buyers into margin calls—accelerating the downtrend via cascading long liquidations.
*   **Execution Rule C (The Non-Negotiable Action):**
    *   **Action:** **LOCK 100% CASH (Strict Ban on Dip-Buying).** Do not deploy spot capital while retail funding is rising into a falling price tape. Wait until funding breaks downward (capitulation flip) and Module 03 (CSU-03A) confirms leveraged dip-buyers have been liquidated.

##### CSU-04C: Contango Carry Bleed ("Stagnant Price With Sustained High Positive Funding")
*   **Trigger Condition A (The Telemetry Scan):**
    1. **Price Slope (Delta_P):** Price is trapped in a tight horizontal range (Garman-Klass volatility < 25th percentile) for >= 72 hours.
    2. **Funding Level:** OI-weighted 8-hour funding stays elevated at **+0.015% to +0.035%+ (16%–38% APR)** with elevated Open Interest.
    3. **Cross-Venue Spread:** Offshore retail funding (Binance/OKX/Bybit) trades >= +6 to +10 bps higher per 8h than domestic/institutional venues (Coinbase/CME).
*   **Observed Outcome B (The Mechanical Trajectory):** Leveraged longs are bleeding heavy funding payments every 8 hours without receiving any upward price appreciation. Eventually, funding fatigue forces leveraged longs to close at market, triggering a sharp downward stop-hunt wick through the bottom of the range.
*   **Execution Rule C (The Non-Negotiable Action):**
    *   **Action:** **STANDBY / 100% CASH PRESERVATION.** Avoid holding unhedged tactical longs inside high-funding range chop. Wait for the inevitable downward funding-fatigue wick (Mutation M4) to sweep range lows and reset funding before evaluating entry.

##### CSU-04D: Backwardation Panic Inflection ("Funding Velocity Crash Into Deep Negative Territory")
*   **Trigger Condition A (The Telemetry Scan):**
    1. **Funding Velocity (Delta_F):** OI-weighted 8-hour funding plunges rapidly (<= -2.5 Z-score, crashing from positive into **-0.015% to -0.050%**) within 12–36 hours following a sharp price drop.
    2. **Order-Book & Spot Audit:** Price hits a major higher-timeframe Volume Profile VAL or On-Chain STH Realized Price band, and **Domestic Fiat (USD) Spot CVD** shows immediate passive limit-bid absorption (price stops falling despite heavy market selling).
*   **Observed Outcome B (The Mechanical Trajectory):** Panic hedging and late-bottom shorting have reached a crescendo at structural support. Market makers and spot institutions are absorbing the panic futures selling at a discount.
*   **Execution Rule C (The Non-Negotiable Action):**
    *   **Entry Trigger:** Authorize **Unleveraged Spot Long** only once 15m/1H price reclaims the local Developing POC with positive Domestic USD Spot CVD (confirming panic sellers are trapped). Size strictly via the **0.75% Risk Formula** with hard stop beneath the panic wick low.

--------------------------------------------------------------------------------

#### 4. Dynamic Regime Mutation Lookup Matrix (M1 through M8)
| Mutation ID | Initial State | Telemetry Mutation Observed (Condition A') | Mechanical Meaning (Outcome B') | Mandatory Execution Override (Rule C') |
| ------ | ------ | ------ | ------ | ------ |
| **M1: Disbelief-to-FOMO Flip** | CSU-04A (Disbelief Rally) | After rallying for days on negative/low funding, 8h funding suddenly spikes above **+0.025%** on a breakout candle while **USD Spot CVD flattens**. | Skeptical shorts have capitulated; retail FOMO longs are now chasing the move at highs. | **Execute Stage 1 (50%) or Stage 2 (100%) Profit Exit** into the funding spike. |
| **M2: Dip-Buyer Capitulation** | CSU-04B (Disbelief Dip) | Price drops sharply, long liquidations spike, and **8h funding crashes from +0.020% down to <= 0.000%** in under 12 hours. | Leveraged dip-buyers have finally been wiped out, removing the overhead long-liquidation overhang. | Lift CSU-04B ban; transition to **Module 03 (CSU-03A)** to watch for post-flush USD Spot CVD step-in. |
| **M3: Offshore-Domestic Divergence** | Any State | Offshore funding (OKX/Binance) spikes to +0.010%–0.025% while **Coinbase/Hyperliquid funding stays near 0.000%** and Coinbase Spot CVD is negative. | Retail offshore leverage is diverging from flat/distributing US institutional flow. | **Circuit Breaker 2 Warning:** Do not trust offshore funding optimism; tighten stops or remain in **100% Cash**. |
| **M4: Contango Fatigue Flush** | CSU-04C (Carry Bleed) | After days of stagnant price and high funding, price breaks range VAL, **OI drops -5% to -10%**, and funding resets to <= +0.005%. | Leveraged longs finally capitulated under funding bleed, sweeping range liquidity. | **Wait 1–2 hours for OI to stabilize**; if USD Spot CVD reclaims range VAL, enter 0.75% Risk Spot Long. |
| **M5: Failed Backwardation Bounce** | CSU-04D (Panic Inflection) | Funding plunges deep negative (< -0.030%), price bounces weakly for 2 hours, then **breaks the panic low** as **USD Spot CVD turns negative**. | Institutional spot buyers pulled bids; backwardation reflects genuine structural liquidation rather than a bottom. | **Hard Stop Triggered / Enforce 100% Cash Lock.** Do not re-enter until higher-timeframe support holds. |
| **M6: Funding-Neutral Trend** | CSU-04A (Disbelief Rally) | Price climbs steadily for weeks while funding remains pinned in the **+0.005% to +0.010%** baseline band and USD Spot CVD rises smoothly. | Ideal institutional accumulation trend—zero leverage excess and steady spot demand. | **Maintain Core Spot Swing Position**; trail stops smoothly below 4H Volume Profile VALs. |
| **M7: Arbitrage Basis Compression** | CSU-04C (Carry Bleed) | Perpetual funding drops to 0.000% alongside dated futures basis compressing below +4% APR and **US Spot ETF outflows**. | Institutional cash-and-carry desks are unwinding long spot / short futures spreads. | **Maintain 100% Cash Lock** until ETF outflows stabilize and basis stops compressing. |
| **M8: Double-Divergence Bottom** | CSU-04D (Panic Inflection) | Price prints a marginally lower low, but **8h funding prints a higher low** (less negative) while **Domestic USD Spot CVD prints a higher low**. | Aggressive short-selling pressure is exhausting itself while domestic spot absorption strengthens. | **High-Conviction Reversal Signal:** Execute 0.75% Risk Spot Long upon 15m/1H VAH reclaim. |

--------------------------------------------------------------------------------

#### 5. Empirical Horizon Reconciliation Note (`MOD 68.1` Cross-Link)
Per **`MOD 68.1`** (299 non-overlapping weeks, `2021-01-08` → `2026-09-30`), a full-week negative funding average paired with rising Open Interest has **`0 / 299` occurrences above the 200-Day SMA**. Consequently, in secular uptrends (`> 200D SMA`), **`CSU-04A` (The Disbelief Rally)** operates strictly on **short-window (`48h–72h`) funding compression (`<= +0.0030%/8h`) or brief 8-hour negative dips** driven by Spot CVD leadership—never waiting for a full weekly negative funding regime, which empirically occurs exclusively below the 200D SMA.
