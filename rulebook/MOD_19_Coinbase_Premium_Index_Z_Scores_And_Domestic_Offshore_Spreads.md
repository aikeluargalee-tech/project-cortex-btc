# PROJECT CORTEX-BTC — MODULE 19: COINBASE PREMIUM INDEX Z-SCORES & DOMESTIC-OFFSHORE SPREADS
**Waterfall Tier:** Pillar 2 & Pillar 5 Bridge (US Institutional Spot Demand vs. Offshore Retail/Perp Pricing) cross-verified with Pillar 1 (Macro Permissions) and Pillar 4 (Portfolio Engineering).
**Empirical Benchmark Anchor:** November 13, 2026 CoinGlass Telemetry — Coinbase Bitcoin Premium Index (`(Coinbase BTC-USD - Binance BTC-USDT) / Binance BTC-USDT * 100%`) trading at **-0.13%** (30D average **-0.14%**, 1Y average **-0.06%**, **8.49th rolling 1Y percentile**, **-1.44 Z-score**) across a **49-day negative streak** (since Sept 22, 2026), with November 2026 lows reaching **-0.18% to -0.27%** during the drawdown from **$77,782** down to **$68,450**.

---

## 1. Machine-Readable State & Routing Block (Python / Hermes / NotebookLM Index)

```yaml
module_id: "MOD_19"
entry_type: "CONDITIONAL_SIGNAL_UNIT"
waterfall_pillar: "PILLAR_2_5_VENUE_SPREAD_PURITY"
title: "Coinbase Premium Index Z-Scores & Domestic-Offshore Venue Spreads"

# PILLAR 1 MASTER PERMISSION PRE-CHECK
pillar_1_permission_required: true
cash_lock_override: "If Pillar 1 Macro Regime == RISK_OFF_100_CASH, negative Coinbase Premium confirms institutional distribution—block all Long entries."

# PRIMARY TELEMETRY TRIGGERS (ROLLING 1Y Z-SCORE & PERCENTILE NORMALIZED)
base_regime_triggers:
  coinbase_premium_formula: "CPI_pct = ((Coinbase_BTC_USD - Binance_BTC_USDT) / Binance_BTC_USDT) * 100"
  institutional_bid_zone: "CPI_pct >= +0.05% (or 1Y Z-score >= +1.5; >= 90th percentile)"
  institutional_drain_zone: "CPI_pct <= -0.10% (or 1Y Z-score <= -1.25; <= 10th percentile; benchmark -0.13% at -1.44 Z)"
  bullish_absorption_divergence: "Price makes lower low while CPI_pct inflects sharply upward from <= -1.5 Z back toward >= 0.00% during NY hours (13:30-21:00 UTC)"

# ANTI-TRAP CIRCUIT BREAKERS
circuit_breakers:
  CB_01_PREMATURE_CLOSE: "NEVER buy an offshore USDT rally while Coinbase Premium Z-score is <= -1.25 (US institutions selling into offshore leverage)."
  CB_02_VENUE_CONTAMINATION: "Verify USDT/USD parity before computing CPI_pct; if USDT trades below $0.996, adjust Binance BTC-USDT by live USDT/USD spot rate."
  CB_03_FORCED_FLOW_STANDDOWN: "When CPI_pct stays <= -0.12% for > 14 consecutive days alongside US Spot ETF outflows, restrict swing exposure to 100% Cash."
  CB_04_SIGNAL_HALF_LIFE: "Intraday 15m/1H CPI_pct spikes govern NY session execution; 7D/30D CPI_pct moving averages govern structural institutional regime."

# RISK & SIZING CONSTANTS (PILLAR 4)
risk_parameters:
  max_portfolio_risk_pct: 0.75
  leverage_permitted: 1.0 # Strict Unleveraged Spot Only
  exit_protocol: "TWO_STAGE_STRUCTURAL"
```

---

## 2. Protective Circuit Breakers (Mandatory Pre-Execution Filters)

* **Circuit Breaker 1 — USDT De-Peg Adjustment (`CB-02`):** Because Coinbase quotes in true US Dollars (`BTC-USD`) and Binance/Bybit quote in Tether (`BTC-USDT`), any stablecoin peg deviation distorts raw spreads. Always normalize `CPI_adjusted = (Coinbase_USD - (Binance_USDT * USDT_USD)) / Coinbase_USD`.
* **Circuit Breaker 2 — Offshore Pump Veto (`CB-01`):** Whenever Bitcoin rallies on offshore perps while `CPI_pct <= -0.10%` (`Z <= -1.25`), US spot desks and ETF Authorized Participants are using offshore liquidity to sell. All long breakout signals are vetoed.
* **Circuit Breaker 3 — NY Session Weighting (`CB-04`):** Coinbase Premium carries maximum predictive weight during **US institutional hours (13:30–21:00 UTC)**. Overnight weekend or Asia-hour spread noise must be confirmed at the NY open.
* **Circuit Breaker 4 — Pillar 1 Macro Permission Gate:** Even a sharp positive spike in Coinbase Premium must pass Pillar 1 (`MOD 16`) before deploying full `0.75%` risk.

---

## 3. Core Conditional Signal Units (`Condition A -> Outcome B -> Rule C`)

### CSU-19A: US Institutional Spot Leadership ("Positive Coinbase Premium Breakout")
* **Trigger Condition A (The Telemetry Scan):**
  1. `CPI_pct` surges above **`+0.05%` (`1Y Z-score >= +1.5`, `>= 90th percentile`)** during NY institutional hours (`13:30–21:00 UTC`).
  2. Price breaks above 1H/4H Volume Profile **VAH** with rising **Domestic USD Spot CVD** (`MOD 05/07`) while offshore perp funding stays moderate (`< +0.015%/8h`).
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** US institutional buyers, corporate treasuries, and Spot ETF creation desks are aggressively lifting offers on Coinbase faster than offshore exchanges can arbitrage the spread.
  * **Probable Trajectory:** High-persistence directional trend expansion as offshore market makers are forced to buy perps/spot to close the arbitrage gap.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Entry Trigger:** Execute **Unleveraged Spot Long** on a 15m/1H pullback retest of the reclaimed **VAH** while `CPI_pct` holds above `+0.02%`.
  * **Position Sizing Formula (0.75% Risk Ceiling):**
    `Spot Position (BTC) = (0.0075 * Total Portfolio Equity) / (Entry Price - Invalidation Stop Price)`
  * **Two-Stage Profit Exit Protocol:**
    * **Stage 1 Exit (50% of Position):** Close 50% if `CPI_pct` spikes into extreme euphoria (`>= +0.20%`) while offshore perp funding jumps above `+0.030%/8h`; move stop to breakeven.
    * **Stage 2 Exit (Remaining 50%):** Trail behind 4H VAL or exit if `CPI_pct` flips negative (`< -0.05%`) during NY hours.

### CSU-19B: Stealth US Accumulation Into Offshore Panic ("Bullish Premium Divergence")
* **Trigger Condition A (The Telemetry Scan):**
  1. Bitcoin sweeps a major support low on heavy offshore perp selling (`MOD 01/03`), printing a marginal lower price low.
  2. **Divergence Inflection:** While price makes a lower low, **`CPI_pct` prints a sharp higher low**—jumping from deep negative (`<= -0.15%`, `-1.5 Z`) back into **positive territory (`>= +0.01%`)** as Coinbase USD limit bids absorb the dump.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Offshore leveraged traders are panic-selling into the hole while US institutional buyers quietly soak up the discounted coins on Coinbase.
  * **Probable Trajectory:** Violent mean-reversion squeeze upward once offshore selling exhausts.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Entry Trigger:** Execute **Unleveraged Spot Long** upon confirmed 15m/1H **VAL or Developing POC reclaim** paired with positive `CPI_pct`, sized strictly to the **0.75% Risk Ceiling** (`0.375%` if Pillar 1 is `GATE_AMBER`).

### CSU-19C: Persistent US Institutional Drain ("Negative Premium Streak Lock")
* **Trigger Condition A (The Telemetry Scan):**
  1. `CPI_pct` remains entrenched below **`-0.10%` (`1Y Z-score <= -1.25`)** for `>= 7 consecutive days` (benchmark: Nov 2026 49-day negative streak at `-0.13%` / `-1.44 Z`).
  2. US Spot ETF netflows are negative and intraday bounces during Asia/London hours repeatedly see `CPI_pct` drop deeper negative at the `13:30 UTC` NY open.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Relentless US institutional distribution and ETF redemption selling—every offshore bounce is used as exit liquidity by domestic desks.
  * **Probable Trajectory:** Downward structural grind and failed breakout traps until `CPI_pct` reclaims `0.00%`.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **ENFORCE 100% CASH LOCK.** Zero long entries permitted until `Mutation M1` breaks the negative premium streak.

### CSU-19D: Parity Equilibrium Compression ("Arbitrage Neutrality")
* **Trigger Condition A (The Telemetry Scan):**
  1. `CPI_pct` oscillates tightly within **`-0.02% to +0.02%` (`|Z-score| < 0.5`)** with low Garman-Klass volatility (`MOD 12`).
* **Observed Outcome B (The Mechanical Trajectory):**
  Global spot liquidity is balanced across US and offshore venues; direction will be decided by the next macro or order-flow catalyst.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **STANDBY IN CASH** until `CPI_pct` breaks above `+0.05%` (`CSU-19A`) or below `-0.10%` (`CSU-19C`).

---

## 4. Dynamic Regime Mutation Lookup Matrix (`M1` through `M8`)

| Mutation ID | Initial State | Telemetry Mutation Observed (`Condition A'`) | Mechanical Meaning (`Outcome B'`) | Mandatory Execution Override (`Rule C'`) |
| :--- | :--- | :--- | :--- | :--- |
| **M1: Negative Streak Break** | `CSU-19C` (Negative Streak) | After `>= 14 days` negative, **`CPI_pct` closes above `+0.03%` for 2 consecutive NY sessions** alongside positive US ETF inflows. | US institutional selling regime has officially flipped back to net accumulation. | **Lift `CSU-19C` Cash Lock.** Authorize `0.75% Risk` Spot Long on 4H VAH/POC reclaim. |
| **M2: NY Open Premium Rug-Pull** | Asia/London Rally | Price rallies overnight with flat `CPI_pct`, then at **`13:30–14:30 UTC` `CPI_pct` plunges below `-0.15%`**. | US ETF Authorized Participants dumped redemption baskets directly into the NY open. | **Immediate Exit of Any Open Tactical Long; Enforce 100% Cash Lock.** |
| **M3: Euphoric Top Premium Spike** | `CSU-19A` (Bull Trend) | `CPI_pct` spikes above **`+0.22%` (`+2.5 Z`)** on a vertical candle while 1H `A_P,V` turns negative (`thin chase`). | Retail/institutional FOMO climax on Coinbase into thin overhead liquidity. | **Execute Stage 1 (50%) or Stage 2 (100%) Profit Exit** into the spike. |
| **M4: Offshore Liquidation Discount** | `CSU-19B` (Flash Crash) | Offshore perp liquidations (`MOD 03`) briefly push Binance `2%` below Coinbase (`CPI_pct` spikes to `+0.50%` for `< 15 mins`), then snaps back. | Temporary offshore liquidation wick distortion rather than sustained US buying. | **Wait 30 minutes** for `CPI_pct` to normalize before evaluating `CSU-19B` VAL reclaim. |
| **M5: Double-Bottom Premium Curl** | `CSU-19C` (Downtrend) | Price makes a lower low (`e.g., $71.2K -> $68.4K`), while **`CPI_pct` prints a higher low (`-0.27% -> -0.13% -> -0.04%`)**. | US institutional sell pressure is visibly exhausting itself across consecutive lows. | Prepare `CSU-19B` entry trigger; enter `0.375%–0.75% Risk` Spot Long once `CPI_pct >= 0.00%` + 1H VAL reclaim. |
| **M6: USDT De-Peg Mirage** | Any State | Raw `CPI_pct` jumps to `+0.30%`, but `USDT/USD` is trading at `$0.997` (adjusted `CPI_pct` is `0.00%`). | Stablecoin discount masquerading as Coinbase spot demand. | **Circuit Breaker 2 Tripped: Ignore Raw Spread.** |
| **M7: ETF Creation Surge Sync** | `CSU-19A` (Uptrend) | Sustained `+0.06% to +0.12%` `CPI_pct` during `14:00–20:00 UTC` paired with `> $300M` daily US Spot ETF inflows. | Institutional TWAP accumulation wave running across multiple sessions. | **Hold Core Swing Runner (`Stage 2`)**; trail stop beneath 4H VAL. |
| **M8: Friday Close Premium Fade** | Friday `19:00–21:00 UTC` | `CPI_pct` turns negative into the Friday equity close after a strong week. | Pre-weekend institutional risk reduction / profit-taking before CME closes. | **Bank Stage 1 (50%) Profit** ahead of weekend thin liquidity (`MOD 20`). |
