# PROJECT CORTEX-BTC — MODULE 06: PASSIVE LIMIT ABSORPTION VS. MARKET TAKER EXHAUSTION
**Waterfall Tier:** Pillar 2 (Microstructure, Order Flow & Path Geometry) cross-verified with Pillar 4 (Portfolio Engineering).
**Core Thesis:** Resolves the fundamental order-book paradox where Cumulative Volume Delta (CVD) only measures aggressive market takers. Quantifies price displacement per unit of net delta ($\Delta P / |\Delta \text{CVD}|$) to detect hidden institutional limit-order walls before price reverses.

---

## 1. Machine-Readable State & Routing Block (Python / Hermes / NotebookLM Index)

```yaml
module_id: "MOD_06"
entry_type: "CONDITIONAL_SIGNAL_UNIT"
waterfall_pillar: "PILLAR_2_MICROSTRUCTURE_ORDER_FLOW"
title: "Passive Limit Absorption vs. Market Taker Exhaustion"

# PILLAR 1 MASTER PERMISSION PRE-CHECK
pillar_1_permission_required: true
cash_lock_override: "If Pillar 1 Macro Regime == RISK_OFF_100_CASH, block all Long executions."

# PRIMARY TELEMETRY TRIGGERS (EFFORT VS. RESULT RATIO)
base_regime_triggers:
  displacement_efficiency_ratio: "E_d = abs(Delta Price %) / abs(CVD Z-score) over 15m/1H/4H window"
  absorption_threshold: "E_d <= 15th rolling percentile (Massive net CVD effort with near-zero price displacement)"
  vacuum_threshold: "E_d >= 85th rolling percentile (Large price displacement on minimal volume/CVD)"
  limit_book_depth_imbalance: "Bid-to-Ask resting liquidity ratio within 1.0%–2.5% of mid-price"

# ANTI-TRAP CIRCUIT BREAKERS
circuit_breakers:
  CB_01_BLIND_LIMIT_WALL_BAN: "NEVER front-run a visible limit bid wall on the DOM/heatmap before taker exhaustion and an upward Absorption-to-Initiation candle print (spoof walls can be pulled in milliseconds)."
  CB_02_PREMATURE_CLOSE_FILTER: "Verify that absorption occurs at a structural Volume Profile node (VAL, VAH, POC, or STH Realized Price), not in the middle of a random Low-Volume Node."
  CB_03_WALL_BREACH_ABORT: "If price slices through an absorption zone on expanding volume, exit immediately—the passive limit wall has been completely filled and exhausted."

# RISK & SIZING CONSTANTS (PILLAR 4)
risk_parameters:
  max_portfolio_risk_pct: 0.75
  leverage_permitted: 1.0
  exit_protocol: "TWO_STAGE_STRUCTURAL"
```

---

## 2. Protective Circuit Breakers (Mandatory Pre-Execution Filters)

* **Circuit Breaker 1 — Anti-Spoofing Verification (Wait for the Initiation Flip):** Large resting limit orders on an order-book heatmap can be spoofed and pulled milliseconds before price touches them. Never buy simply because a resting bid wall appears on a screen. You must wait for **realized absorption** (heavy market selling actually hitting the bid with $\Delta P \approx 0$) followed by an **Absorption-to-Initiation Flip** (market buyers stepping up to reclaim the 15m/1H footprint high).
* **Circuit Breaker 2 — Structural Location Filter:** True institutional limit absorption occurs at pre-defined valuation boundaries (Volume Profile VAL/VAH, 200D MA, or Short-Term Holder Realized Price). Ignore minor 5-minute absorption inside noisy mid-range chop.
* **Circuit Breaker 3 — Hard Invalidation on Wall Depletion:** Even genuine institutional limit walls have a finite BTC budget. If sellers exhaust the entire resting bid wall and push price cleanly below the absorption cluster low, exit immediately with zero hesitation.

---

## 3. Core Conditional Signal Units (`Condition A -> Outcome B -> Rule C`)

### CSU-06A: Passive Limit Bid-Wall Absorption (Bullish Floor Verification)
* **Trigger Condition A (The Telemetry Scan):**
  1. Price tests a major structural support zone (4H/1D Volume Profile VAL, HTF swing low, or STH cost basis).
  2. Net Taker CVD plunges sharply negative (`1H/4H CVD Z-score <= -2.0`), yet **Price Displacement Efficiency ($E_d = |\Delta P| / |\Delta \text{CVD}|$) drops into the bottom 15th percentile** (candles print tight bodies or long lower wicks that refuse to close lower).
  3. **Initiation Trigger:** Following the absorption cluster, a 15m/1H candle closes above the high of the highest-volume absorption bar alongside a positive uptick in **Domestic Fiat (USD) Spot CVD**.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Institutional whales executing passive TWAP/iceberg limit buy orders have absorbed 100% of aggressive market-taker selling without letting price drop.
  * **Probable Trajectory:** Market sellers are now exhausted (out of inventory or maxed out on short margin). As soon as passive buyers switch to market-buying the ask, price springs upward rapidly.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Entry Trigger:** Execute **Unleveraged Spot Long** upon the 15m/1H close above the absorption cluster high (and VAL reclaim).
  * **Position Sizing Formula (0.75% Risk Ceiling):**
    `Spot Position (BTC) = (0.0075 * Total Portfolio Equity) / (Entry Price - Absorption Cluster Low Stop)`
  * **Hard Structural Invalidation Stop:** Place hard stop `0.15% to 0.25%` below the lowest wick of the verified absorption cluster (providing ultra-tight risk geometry and high R-multiples).

### CSU-06B: Passive Limit Ask-Wall Capping (Bearish Ceiling Distribution)
* **Trigger Condition A (The Telemetry Scan):**
  1. Price rallies into a major structural resistance zone (4H/1D Volume Profile VAH or prior distribution HVN).
  2. Net Taker CVD surges strongly positive (`1H/4H CVD Z-score >= +2.0`), yet **Price Displacement Efficiency ($E_d$) compresses into the bottom 15th percentile** (price flattens and prints repeated upper wicks).
  3. Price subsequently breaks below the low of the high-volume capping cluster as Domestic USD Spot CVD turns negative.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Institutional holders are passively unloading huge spot inventory via iceberg limit asks, using aggressive retail market-buyers as liquidity without crashing the price prematurely.
  * **Probable Trajectory:** Once aggressive buyers exhaust their purchasing power against the invisible ask ceiling, price drops sharply back toward the Volume Profile POC and VAL.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Existing Spot Longs:** **Execute Immediate Profit Exit (50% to 100%)** when the 15m/1H candle closes below the ask-wall absorption cluster low.
  * **New Entries:** **Enforce 100% Cash Lock.** Never buy into an active passive ask-wall ceiling.

### CSU-06C: Order-Book Liquidity Vacuum Impulse (Thin-Book Acceleration)
* **Trigger Condition A (The Telemetry Scan):**
  1. **Price Displacement Efficiency ($E_d = |\Delta P| / |\Delta \text{CVD}|$) spikes into the top 85th+ percentile** (price moves rapidly on moderate volume/delta).
  2. Price is traversing a Volume Profile **Low-Volume Node (LVN)** where resting limit-book depth is thin.
* **Observed Outcome B (The Mechanical Trajectory):**
  Because resting limit liquidity has been pulled from the book, even small market orders displace price across wide ranges until the next High-Volume Node (HVN) is reached.
* **Execution Rule C (The Non-Negotiable Action):**
  * **If Bullish Vacuum (Price ↑, Domestic Spot CVD +):** Hold existing spot swing positions untouched until price reaches the next HVN magnet; do not chase mid-LVN with wide stops.
  * **If Bearish Vacuum (Price ↓, Spot/Perp CVD –):** Remain **100% Cash**; do not attempt to bid inside an LVN air pocket.

### CSU-06D: Taker Capitulation Climax (Exhaustion Spike Reversal)
* **Trigger Condition A (The Telemetry Scan):**
  1. A single 15m/1H bar prints a `>= +3.5 Z-score` volume and delta climax at the end of a multi-day trend extension.
  2. Over 60% of the candle's volume occurs in the outer wick tip (footprint node trapped at the extreme), and the candle closes back inside the prior bar's range.
* **Observed Outcome B (The Mechanical Trajectory):**
  The final wave of forced liquidations and late emotional market orders has been completely absorbed at the wick extreme, leaving zero follow-through takers remaining.
* **Execution Rule C (The Non-Negotiable Action):**
  * **At Climax Highs:** Close 100% of tactical spot longs immediately.
  * **At Climax Lows:** Prepare **CSU-06A** spot long entry upon confirmation of the next 1H candle holding above the trapped-seller footprint node, sized strictly to **0.75% max equity risk**.

---

## 4. Dynamic Regime Mutation Lookup Matrix (`M1` through `M8`)

| Mutation ID | Initial State | Telemetry Mutation Observed (`Condition A'`) | Mechanical Meaning (`Outcome B'`) | Mandatory Execution Override (`Rule C'`) |
| :--- | :--- | :--- | :--- | :--- |
| **M1: Absorption to Initiation Flip** | `CSU-06A` (Passive Bid) | After absorbing heavy selling at VAL, Domestic USD Spot CVD turns sharply positive and price breaks the absorption range high. | Passive institutional limit buyers have finished filling their resting bids and switched to aggressive market buying. | **Execute Full 0.75%-Risk Spot Long Immediately.** |
| **M2: Bid-Wall Exhaustion Breach** | `CSU-06A` (Passive Bid) | Sellers continue pounding the bid wall until a 15m/1H candle closes cleanly below the absorption cluster low on high volume. | The institutional limit buy order was completely filled and overwhelmed by even larger macro supply. | **CB-03 Active: Trigger Hard Invalidation Stop Immediately** (max `-0.75%` portfolio impact) and lock 100% Cash. |
| **M3: Ask-Wall Absorption Breakthrough** | `CSU-06B` (Passive Ask) | Despite heavy ask-wall capping at VAH, Domestic USD Spot CVD keeps accelerating until price closes cleanly *above* the capping wick highs. | Spot buyers successfully chewed through the entire overhead institutional sell wall. | **Flip Bias to Bullish Breakout (`CSU-02C` / `Mod 11`)** — enter Spot Long on the first 15m/1H retest of the broken ask-wall level. |
| **M4: Spoof Wall Pull** | `CSU-06A` (Unverified) | A large visible bid wall on the DOM disappears as price gets within `0.3%` of it, and price slices lower on low volume (`E_d` spikes high). | The bid wall was synthetic spoof liquidity designed to lure front-running longs. | **CB-01 Validated: Remain 100% Cash.** Never enter before realized delta absorption prints on the tape. |
| **M5: Stepping Iceberg Trail** | `CSU-06A` -> `M1` | After initial bid absorption at VAL, a new passive bid absorption cluster forms `+1.5%` higher at the Developing POC. | The institutional buyer is laddering their iceberg limit floor upward to defend their newly accumulated position. | **Trail Hard Invalidation Stop Upward** directly underneath the new higher absorption cluster, locking in risk-free equity. |
| **M6: Dual-Sided Compression Pin** | `CSU-06A` + `06B` | Both upper wicks and lower wicks show high-volume absorption within a `< 1.5%` price band around the POC. | Market makers (or options gamma dealers) are absorbing takers on both sides to pin price ahead of settlement. | **Standby in 100% Cash** (or hold existing position untouched) until one side of the compression pin breaks with displacement. |
| **M7: Perp Absorption vs. Spot Dump** | `CSU-06B` (Ceiling) | Price stalls at resistance as Perp CVD is positive (`+$500M`), while Coinbase USD Spot CVD is negative (`-$80M`). | Unleveraged spot institutions are the passive ask wall capping leveraged perpetual buyers. | **High-Conviction Exit Signal:** Close 100% of spot swing exposure ahead of the inevitable perp long unwind. |
| **M8: Retest of Trapped Footprint Node** | `CSU-06D` (Climax) | After a V-bottom absorption reversal, price pulls back on low volume (`E_d` low) to retest the exact price level of the prior trapped-seller footprint cluster. | Former trapped shorts are defending/covering at breakeven while passive spot bids reload at the same node. | **High-Probability Secondary Entry / Add** (keeping total combined position risk strictly `<= 0.75%` of portfolio equity). |
