# PROJECT CORTEX-BTC — MODULE 05: THE 4-QUADRANT SPOT CVD VS. PERPETUAL CVD MATRIX
**Waterfall Tier:** Pillar 2 (Microstructure, Order Flow & Path Geometry) cross-verified with Pillar 3 (Derivatives) and Pillar 4 (Portfolio Engineering).
**Empirical Benchmark Anchor:** November 2026 Multi-Window Order Flow — Distinguishing 3D/7D "Spot Absorbing" regimes (Spot net taker inflow `+$32.5M` to `+$269.4M` vs. Futures net taker outflow `-$1.1B` to `-$1.2B`) from 1H–24H "Aligned Outflow" breakdown regimes (Futures `-$722.5M to -$1.2B` + Spot `-$83.3M to -$141.5M`).

---

## 1. Machine-Readable State & Routing Block (Python / Hermes / NotebookLM Index)

```yaml
module_id: "MOD_05"
entry_type: "CONDITIONAL_SIGNAL_UNIT"
waterfall_pillar: "PILLAR_2_MICROSTRUCTURE_ORDER_FLOW"
title: "The 4-Quadrant Spot CVD vs. Perpetual CVD Matrix"

# PILLAR 1 MASTER PERMISSION PRE-CHECK
pillar_1_permission_required: true
cash_lock_override: "If Pillar 1 Macro Regime == RISK_OFF_100_CASH, Quad 1 and Quad 2 Long entries are blocked."

# PRIMARY TELEMETRY TRIGGERS (ROLLING PERCENTILE & Z-SCORE NORMALIZED)
base_regime_triggers:
  domestic_spot_cvd_slope: "1H/4H/24H Cumulative Volume Delta slope on USD Fiat Gateways (Coinbase, Kraken, Bitstamp)"
  offshore_spot_cvd_slope: "1H/4H/24H Cumulative Volume Delta slope on USDT pairs (Binance, OKX, Bybit)"
  perp_cvd_slope: "1H/4H/24H Cumulative Volume Delta slope across aggregate Perpetual Futures"
  cvd_zscore_divergence: "Z-score spread between Normalized Spot CVD and Normalized Perp CVD"

# ANTI-TRAP CIRCUIT BREAKERS
circuit_breakers:
  CB_01_PERP_LED_PUMP_BAN: "NEVER buy when Perp CVD is rising steeply while Domestic USD Spot CVD is falling (Quad 3 Bearish Trap)."
  CB_02_VENUE_PURITY_GATE: "Domestic USD Spot CVD overrides Offshore USDT Spot CVD in every conflict."
  CB_03_MULTI_WINDOW_ALIGNMENT: "A 3D/7D 'Spot Absorbing' reading is INVALID for immediate entry if the 1H, 4H, and 24H windows have mutated into 'Aligned Outflow'."

# RISK & SIZING CONSTANTS (PILLAR 4)
risk_parameters:
  max_portfolio_risk_pct: 0.75
  leverage_permitted: 1.0
  exit_protocol: "TWO_STAGE_STRUCTURAL"
```

---

## 2. Protective Circuit Breakers (Mandatory Pre-Execution Filters)

* **Circuit Breaker 1 — The Perp-Led Pump Ban:** Perpetual futures volume is 5x to 10x larger than spot volume, but perpetual buyers use borrowed margin that must eventually be closed. Unleveraged **Domestic USD Spot CVD** is the only capital that permanently removes Bitcoin supply from the float. Never buy a rally driven solely by Perp CVD (`Quad 3`).
* **Circuit Breaker 2 — Multi-Timeframe Window Cascade Check (`1H / 4H / 24H` vs. `3D / 7D`):** Higher-timeframe absorption (`3D/7D Spot CVD > 0`) can fail if short-term windows (`1H/4H/24H`) flip into **Aligned Outflow**. Both the tactical (`1H/4H`) and structural (`24H/3D`) Domestic Spot CVD slopes must be positive before authorizing an entry.
* **Circuit Breaker 3 — Price Displacement Confirmation:** Positive Spot CVD must eventually produce upward price displacement (reclaiming 15m/1H VAH). If Spot CVD rises steeply while price falls, passive limit sellers are overwhelming spot market buyers (see Module 06).

---

## 3. Core Conditional Signal Units: The 4 Quadrants (`Condition A -> Outcome B -> Rule C`)

### CSU-05A (Quadrant 1): Spot CVD Rising (+) / Perp CVD Falling (–) — "Spot Absorbing Perp Shorts"
* **Trigger Condition A (The Telemetry Scan):**
  1. **Domestic Fiat (USD) Spot CVD** slopes positively (`Z-score >= +1.0`) across the 1H, 4H, and 24H windows.
  2. **Perpetual CVD** slopes negatively (`Z-score <= -1.0`), accompanied by rising Open Interest and negative Perp Basis.
  3. Price holds flat above a 1H/4H Volume Profile VAL or prints higher lows despite heavy perpetual market-selling.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Institutional unleveraged spot buyers are accumulating directly into the panic/aggression of leveraged perpetual short sellers.
  * **Probable Trajectory:** Once perpetual selling exhausts, the absence of spot sellers combined with trapped perp shorts drives an asymmetric upward expansion (`Module 01 / CSU-01A` confluence).
* **Execution Rule C (The Non-Negotiable Action):**
  * **Entry Trigger:** Execute **Unleveraged Spot Long** upon a verified 15m/1H **Value Area High (VAH) reclaim** under the **0.75% Risk Ceiling**:
    `Spot Position (BTC) = (0.0075 * Total Portfolio Equity) / (Entry Price - Absorption VAL Stop)`
  * **Two-Stage Profit Exit:** Close 50% when Perp CVD spikes positive on short covering (`Basis > 0`); trail the remaining 50% behind the 4H VAL.

### CSU-05B (Quadrant 2): Spot CVD Rising (+) / Perp CVD Rising (+) — "Aligned Institutional Markup"
* **Trigger Condition A (The Telemetry Scan):**
  1. Both **Domestic USD Spot CVD** and **Perpetual CVD** slope positively across 1H, 4H, and 24H windows.
  2. **Rough Path Signature (`A_SpotCVD,PerpCVD`)** confirms that Domestic Spot CVD initiated the upward turn *before* Perp CVD followed.
  3.Perpetual Basis remains moderate (`< +0.02%`, below the 85th percentile overheating threshold).
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Broad-based institutional and momentum trend expansion where spot demand leads and derivatives follow in healthy alignment.
  * **Probable Trajectory:** Sustained directional trend through Low-Volume Nodes (LVNs) toward higher HTF valuation bands.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** Hold existing spot swing positions or enter on 15m/1H pullbacks to Developing POC/VAH at **0.75% maximum portfolio risk**. Monitor for **Mutation M2** (when Perp CVD accelerates far ahead of Spot CVD at resistance).

### CSU-05C (Quadrant 3): Spot CVD Falling (–) / Perp CVD Rising (+) — "Perp-Led Bull Trap / Spot Distribution"
* **Trigger Condition A (The Telemetry Scan):**
  1. **Perpetual CVD** slopes strongly positive (leveraged takers aggressively buying breakouts or dips) and Open Interest rises.
  2. **Domestic Fiat (USD) Spot CVD** slopes **negative** (Coinbase/Kraken net taker selling and/or Spot ETF outflows).
  3. Price struggles to hold above 1H VAH or prints bearish CVD divergences at local highs.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** The classic retail leverage trap. Unleveraged spot whales and institutions are dumping physical Bitcoin into the bids created by leveraged perpetual futures buyers.
  * **Probable Trajectory:** As soon as perpetual buying slows down, the weight of spot distribution breaks the floor and triggers a long-liquidation cascade downward.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **STRICT 100% CASH LOCK (CB-01 Tripped).** If holding an open spot swing position, execute an immediate protective exit. Never hold spot when institutions are selling spot into perpetual leverage.

### CSU-05D (Quadrant 4): Spot CVD Falling (–) / Perp CVD Falling (–) — "Aligned Structural Markdown"
* **Trigger Condition A (The Telemetry Scan):**
  1. Both **Domestic USD Spot CVD** and **Perpetual CVD** slope negatively across the 1H, 4H, 12H, and 24H windows (e.g., 24H Futures `-$722.5M to -$1.2B` alongside 24H Spot `-$83.3M to -$141.5M`).
  2. Price breaks below 1H/4H Volume Profile VAL and trades below the 1H/4H Developing POC.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Synchronized capital exit across both unleveraged spot holders and leveraged futures traders. There is no active buyer of last resort on the tape.
  * **Probable Trajectory:** Sustained markdown and support failure until a major HTF liquidity pool is swept and Quadrant 1 (`Spot CVD + / Perp CVD -`) re-emerges.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **LOCK 100% CASH.** Zero dip-buying is permitted while all tactical windows (`1H/4H/24H`) remain in Quadrant 4 Aligned Outflow.

---

## 4. Dynamic Regime Mutation Lookup Matrix (`M1` through `M8`)

| Mutation ID | Initial State | Telemetry Mutation Observed (`Condition A'`) | Mechanical Meaning (`Outcome B'`) | Mandatory Execution Override (`Rule C'`) |
| :--- | :--- | :--- | :--- | :--- |
| **M1: Quad 1 to Quad 2 Ignition** | `CSU-05A` (Quad 1) | Price breaks above 1H VAH and Perp CVD flips from negative to sharply positive while USD Spot CVD stays positive. | Short sellers have capitulated and flipped to market buyers alongside continuing spot demand. | **Hold Spot Long;** trail stop to breakeven and prepare Stage 1 profit take when Basis exceeds `+0.02%`. |
| **M2: Quad 2 to Quad 3 Hand-Off** | `CSU-05B` (Quad 2) | After a rally, USD Spot CVD rolls over and turns negative while Perp CVD keeps rising vertically at the highs. | Smart spot money is handing the bag to late leveraged perpetual buyers at resistance. | **Execute Immediate Stage 2 Full Exit (100% Cash).** |
| **M3: Quad 1 to Quad 4 Collapse** | `CSU-05A` (Quad 1) | A 3D/7D "Spot Absorbing" state mutates as 1H, 4H, and 24H USD Spot CVD flip negative alongside Perp CVD (`Aligned Outflow`). | Spot buyers gave up defending the floor and joined perpetual sellers in liquidating positions. | **Circuit Breaker 3 Tripped: Abort Long Watch / Exit to 100% Cash Immediately.** |
| **M4: Quad 4 to Quad 1 Bottom** | `CSU-05D` (Quad 4) | After a sharp markdown, Perp CVD continues making new lows, but 1H/4H Coinbase USD Spot CVD prints higher lows and turns positive at HTF support. | Unleveraged institutional spot buyers have stepped in to absorb the tail end of the perp markdown. | **Arm `CSU-05A` Entry Watch:** Execute 0.75%-risk Spot Long upon 15m/1H VAL reclaim. |
| **M5: Quad 3 to Quad 4 Flush** | `CSU-05C` (Quad 3) | Perp CVD abruptly snaps from rising (+) to plunging (–) while Spot CVD remains negative. | Trapped leveraged perp buyers from Quad 3 are now being forcibly liquidated into a spot-selling vacuum. | **Stay 100% Cash** until Module 03 (`>= 8%–12%` OI flush) completes. |
| **M6: Offshore USDT Fakeout** | `CSU-05D` (Quad 4) | Binance USDT Spot CVD turns positive on a bounce, while Coinbase USD Spot CVD and Perp CVD remain negative. | Offshore tether market-maker rotation is painting a false spot bounce while fiat gateways continue selling. | **CB-02 Active: Ignore Bounce.** Keep 100% Cash Lock until Coinbase USD Spot CVD turns positive. |
| **M7: Spot Taker Exhaustion** | `CSU-05B` (Quad 2) | USD Spot CVD surges to a `+3.0 Z-score` climax at HTF resistance, but price fails to break VAH and prints a shooting-star wick. | Even unleveraged spot takers have run into a massive institutional limit sell wall (`Module 06`). | **Take 50%–100% Tactical Profits** unless price reclaims the wick high within 2 candles. |
| **M8: Session Handoff Flip** | `CSU-05C` (Asia/London) | Asia/London sessions print Quad 3 (Perp-led bounce), then at 09:30 EST (NY Open) Coinbase USD Spot CVD surges positive and takes the lead. | US institutional spot inflows validated and rescued an initially fragile overnight perp move. | **Upgrade from Standby to `CSU-05B`** — permit tactical entry if 1H VAH holds after first 60 minutes of NY open. |
