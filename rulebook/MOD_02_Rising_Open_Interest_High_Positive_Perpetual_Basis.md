# PROJECT CORTEX-BTC — MODULE 02: RISING OPEN INTEREST + HIGH POSITIVE PERPETUAL BASIS
**Waterfall Tier:** Pillar 3 (Derivatives & Market Fragility) cross-verified with Pillar 2 (Microstructure & Order Flow) and Pillar 4 (Portfolio Engineering).
**Empirical Benchmark Anchor:** November 2026 Term Structure & Funding Telemetry — Dated quarterly futures term structure trading at **+4.024% to +5.477%** basis (+15.0% to +35.0% annualized) alongside OI-weighted 8-hour perpetual funding spikes above **+0.025% to +0.050%** (> +27% to +54% annualized) on offshore venues (Binance/Bybit/OKX) during leveraged breakout attempts.

---

## 1. Machine-Readable State & Routing Block (Python / Hermes / NotebookLM Index)

```yaml
module_id: "MOD_02"
entry_type: "CONDITIONAL_SIGNAL_UNIT"
waterfall_pillar: "PILLAR_3_DERIVATIVES_FRAGILITY"
title: "Rising Open Interest + High Positive Perpetual Basis (Euphoric Leverage Crowding)"

# PILLAR 1 MASTER PERMISSION PRE-CHECK
pillar_1_permission_required: true
cash_lock_override: "If Pillar 1 Macro Regime == RISK_OFF_100_CASH, block all Long entries and enforce profit protection on existing spot holdings."

# PRIMARY TELEMETRY TRIGGERS (ROLLING PERCENTILE & Z-SCORE NORMALIZED)
base_regime_triggers:
  oi_7d_delta_pct_or_zscore: "OI 7D expansion >= +5% of total OI (or >= +1.5 Z-score)"
  oi_total_btc_percentile: ">= 80th rolling 1Y percentile"
  perp_basis_pct: ">= +0.030% (or >= 90th rolling 1Y historical percentile)"
  funding_8h_rate_pct: ">= +0.020% per 8h (>= +21.9% annualized; or >= +2.0 Z-score)"

# ANTI-TRAP CIRCUIT BREAKERS
circuit_breakers:
  CB_01_PREMATURE_CLOSE: "NEVER chase a breakout daily/4H candle close when Perp Basis is >= 90th percentile unless Domestic USD Spot CVD is leading the move."
  CB_02_VENUE_CONTAMINATION: "Reject bullish breakout signals if OI and funding surge strictly on offshore USDT venues while Coinbase/Kraken USD Spot CVD is flat or negative."
  CB_03_FORCED_FLOW_STANDDOWN: "Stand down 100% from new entries during extreme funding velocity spikes (> +3.0 Z-score) until leverage flushes or funding normalizes."
  CB_04_SIGNAL_HALF_LIFE: "Do not allow short-term 15m perp momentum to override Pillar 1 macro resistance or Pillar 5 LTH distribution bands."

# RISK & SIZING CONSTANTS (PILLAR 4)
risk_parameters:
  max_portfolio_risk_pct: 0.75
  leverage_permitted: 1.0 # Strict Unleveraged Spot Only
  exit_protocol: "TWO_STAGE_STRUCTURAL"
```

---

## 2. Protective Circuit Breakers (Mandatory Pre-Execution Filters)

Before any Scenario in Module 02 can authorize a spot action, all four circuit breakers must pass:
* **Circuit Breaker 1 — Pillar 1 Macro Permission Gate:** Verify that secular macro permissions (200-Day Moving Average, sovereign yields, DXY, and stablecoin supply impulse) permit risk exposure. In a macro contraction regime, high positive basis is strictly a **distribution and long-liquidation trap**.
* **Circuit Breaker 2 — Domestic Fiat (USD) vs. Offshore (USDT) Venue Split:** High positive perpetual basis must be cross-checked against **Domestic Fiat Gateways (Coinbase/Kraken BTC-USD)** and **US Spot ETF creation flows**. If offshore retail traders are paying 30%+ annualized funding while US spot venues show net selling, the rally is paper-driven and fragile.
* **Circuit Breaker 3 — Passive Ask-Wall & Price-Displacement Audit:** If Open Interest and Perpetual CVD are surging upward (`+Delta`) while price stalls below a High-Volume Node (HVN) or Value Area High (VAH), institutional spot holders are using passive limit asks to distribute into retail FOMO longs.
* **Circuit Breaker 4 — Leverage Crowding Ceiling:** When 8-hour funding exceeds the **95th rolling percentile** without a corresponding Spot CVD surge, new spot entries are strictly prohibited; focus shifts exclusively to **protecting open swing gains**.

---

## 3. Core Conditional Signal Units (`Condition A -> Outcome B -> Rule C`)

### CSU-02A: Spot-Backed Leveraged Breakout ("Healthy Trend Expansion")
* **Trigger Condition A (The Telemetry Scan):**
  1. 7-day Open Interest expands (`>= +5%` or `+1.5 Z-score`) with Perpetual Basis elevated (`+0.025% to +0.050%`, 85th–92nd percentile), reflecting strong directional demand.
  2. **Domestic Fiat (USD) Spot CVD** and US Spot ETF netflows slope **steeply positive**, outpacing or matching Perpetual CVD slope.
  3. **Rough Path Signature (Verdict 0):** Price–Volume and Spot CVD–OI Lévy Signed Area exhibits positive curvature (`Spot leading OI`), and price holds cleanly above the reclaimed 1H/4H **Value Area High (VAH)**.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Genuine unleveraged institutional capital is bidding spot higher, pulling perpetual futures into a healthy contango premium. Because spot buyers own the underlying float outright, they are immune to margin liquidations on minor pullbacks.
  * **Probable Trajectory:** Sustained multi-day trend expansion toward the next higher-timeframe Low-Volume Node (LVN) or liquidity target, punctuated by brief shallow dips that flush excess leverage without breaking structural spot support.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Entry Trigger:** Execute **Unleveraged Spot Long** only on a verified **15m/1H pullback retest of the reclaimed VAH or Developing POC** where Domestic USD Spot CVD remains positive and initial weak longs have been shaken out. (Never buy the vertical top wick).
  * **Position Sizing Formula (0.75% Risk Ceiling):**
    `Spot Position (BTC) = (0.0075 * Total Portfolio Equity) / (Entry Price - Invalidation Stop Price)`
  * **Hard Structural Invalidation Stop:** Place hard stop immediately below the reclaimed 4H Value Area High (VAH) / breakout origin shelf.
  * **Two-Stage Profit Exit Protocol:**
    * **Stage 1 Exit (50% of Position):** Close 50% when 8-hour funding reaches extreme euphoria (`>= 95th percentile` or `> +0.045%`) and price hits the upper Garman-Klass volatility fan band. Move stop on remaining 50% to breakeven.
    * **Stage 2 Exit (Remaining 50%):** Trail behind the 4H Volume Profile VAL or exit immediately if Domestic USD Spot CVD rolls over negative while Open Interest continues climbing.

### CSU-02B: Exhaustion Long Top at Resistance ("Euphoric Leverage Crowding")
* **Trigger Condition A (The Telemetry Scan):**
  1. Open Interest surges (`>= +5%` 7D) and Perpetual Basis spikes above the **90th historical percentile** (`>= +0.035%`, funding `> +0.025%/8h`).
  2. Price stalls against a major HTF resistance / VAH ceiling—failing to make further upward displacement despite heavy market-buy volume (`Perp CVD rising, Price flat`).
  3. **Domestic Fiat (USD) Spot CVD** flattens or turns **negative**, revealing that unleveraged spot holders are selling into the leveraged futures bid.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Late retail and momentum traders are aggressively opening high-leverage longs at resistance, paying exorbitant funding rates while institutional spot holders distribute inventory to them.
  * **Probable Trajectory:** Because marginal leveraged buyers are exhausted and spot bids are absent underneath, a minor dip triggers a cascading **long-liquidation flush** back through the Volume Profile Value Area.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **BLOCK ALL NEW LONG ENTRIES. LOCK 100% CASH ON SIDELINES.**
  * **Existing Position Management:** If already holding an open Spot Swing Long from a lower entry, immediately execute **Stage 2 Full Profit Exit** (or tighten trailing stop to the 1H Value Area Low) to lock in gains ahead of the forced long flush.

### CSU-02C: Institutional Cash-and-Carry Basis Arbitrage ("Synthetic OI Inflation")
* **Trigger Condition A (The Telemetry Scan):**
  1. Total Open Interest (especially CME and dated quarterly futures) climbs steadily while annualized futures basis sits in the **+12% to +35% APR** arbitrage zone.
  2. **US Spot ETF Net Inflows** or OTC spot purchases rise in lockstep with short futures Open Interest, while perpetual funding remains moderate (`+0.008% to +0.015%/8h`).
  3. Garman-Klass volatility contracts into the bottom quartile; price remains range-bound near the POC.
* **Observed Outcome B (The Mechanical Trajectory):**
  Institutional desks are buying spot BTC (or Spot ETFs) and simultaneously shorting dated/perpetual futures to harvest risk-free basis yield. This inflates headline Open Interest without creating directional liquidation fuel.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **STANDBY / 100% CASH PRESERVATION** for swing capital. Do not mistake arbitrage-driven Open Interest for an imminent directional breakout. Wait for basis compression and a verified directional Volume Profile breakout.

### CSU-02D: Pre-Cascade Spot Bid Pull ("Thin Book Liquidation Setup")
* **Trigger Condition A (The Telemetry Scan):**
  1. Open Interest sits at extreme highs (`>= 85th percentile`) with elevated positive funding (`>= +0.020%/8h`).
  2. Order-book depth within `-1% to -2%` below spot thins out sharply (`Spot bid liquidity pulled`), and **Domestic USD Spot CVD** breaks down into negative territory (`aligned spot + futures outflow`).
  3. Price loses the 1H Developing POC on rising sell volume.
* **Observed Outcome B (The Mechanical Trajectory):**
  With resting spot bids removed beneath an over-leveraged long book, market makers step down their quotes. Once price breaches the first cluster of leveraged long stop-losses, forced market-sell liquidations cascade rapidly downward.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **ENFORCE 100% CASH LOCK.** Exit any remaining spot exposure immediately. Transition scanner to **Module 03 (Deleveraging Flushes & OI Reset Mechanics)** and wait for a verified > 8%–12% OI wipeout before evaluating re-entry.

---

## 4. Dynamic Regime Mutation Lookup Matrix (`M1` through `M8`)

| Mutation ID | Initial State | Telemetry Mutation Observed (`Condition A'`) | Mechanical Meaning (`Outcome B'`) | Mandatory Execution Override (`Rule C'`) |
| :--- | :--- | :--- | :--- | :--- |
| **M1: Healthy Funding Cool-Off** | `CSU-02A` (Spot Breakout) | Price consolidates sideways above 1H VAH, **8h funding drops by > 50%** toward neutral (`+0.005%`), OI dips `-2% to -4%`, and **USD Spot CVD stays positive**. | Weak over-leveraged longs exited peacefully while spot holders held firm—resetting fuel for the next leg up. | **Hold Spot Long** (or enter on VAH retest under `0.75% Risk Formula`). |
| **M2: Blow-Off Euphoria Spike** | `CSU-02A` (Spot Breakout) | Price goes vertical, 8h funding spikes above **+0.050% (> 50% APR)**, OI jumps `+5%` in 24h, and **USD Spot CVD diverges downward**. | Trend has mutated from institutional spot-led into a terminal retail leverage blow-off top. | **Execute Immediate Full Exit (100% of Spot Swing)** into strength; lock Cash. |
| **M3: Resistance Absorption Stall** | `CSU-02B` (Crowded Top) | Perp CVD keeps rising at resistance, OI climbs, but price fails to break VAH for `>= 4 hours` and prints upper rejection wicks. | Passive institutional ask walls are absorbing all leveraged long market buys. | **Strict 100% Cash Lock.** Prepare for imminent downward long-squeeze flush. |
| **M4: Long-Liquidation Cascade** | `CSU-02B` / `02D` | Price breaks 1H VAL + **OI drops sharply (`-5% to -15%`)** + Long liquidations exceed **85% of total liquidations**. | Over-crowded longs are being forcibly wiped out in a cascading margin flush. | **Stand Down 100% in Cash.** Ban all knife-catching until Module 03 OI reset confirms. |
| **M5: Short-Squeeze Continuation** | `CSU-02A` (Spot Breakout) | Despite positive basis, aggressive counter-trend shorts step in at resistance (`Perp CVD drops`), funding dips, and **USD Spot CVD surges** through VAH. | Counter-trend shorts just provided fresh squeeze fuel on top of an active spot uptrend. | **Hold Remaining 50% Spot Long**; trail stop tightly beneath the newly reclaimed VAH. |
| **M6: Offshore-Only Pump Trap** | `CSU-02A` (False Signal) | Binance/Bybit/OKX OI and funding spike while **CME OI falls** and **Coinbase USD Spot CVD is negative**. | Leveraged offshore speculation without US institutional spot backing. | **Circuit Breaker 2 Tripped: Abort Long Bias.** Treat as `CSU-02B` (Trap). |
| **M7: Arbitrage Unwind Pressure** | `CSU-02C` (Cash-and-Carry) | Basis compresses rapidly toward `0.00%` alongside **US Spot ETF net outflows** (`e.g., -$299.8M`) and falling CME OI. | Institutional arbitrage desks are closing short futures and selling underlying spot ETFs simultaneously. | **Maintain 100% Cash Lock.** Spot ETF selling creates sustained headwind until outflows halt. |
| **M8: Post-Flush Basis Reset Reclaim** | `M4` (Long Cascade) | After a sharp long liquidation flush wipes out excess OI (`-8% to -17%`), funding resets to `<= +0.005%` and **USD Spot CVD steps in** at HTF VAL. | Excess leverage has been purged; market structure is clean again for unleveraged spot accumulation. | Transition to **Module 03 (`CSU-03A`)** and evaluate `0.75% Risk` Spot Long entry upon 15m VAL reclaim. |
