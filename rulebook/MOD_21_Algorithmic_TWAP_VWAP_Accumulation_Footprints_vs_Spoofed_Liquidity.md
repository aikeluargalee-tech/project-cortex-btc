# PROJECT CORTEX-BTC — MODULE 21: ALGORITHMIC TWAP/VWAP ACCUMULATION FOOTPRINTS VS. SPOOFED LIQUIDITY
**Waterfall Tier:** Pillar 2 (Microstructure, Order-Book Forensics & Institutional Execution Algorithms) cross-verified with Pillar 1 (Macro Permissions) and Pillar 4 (Portfolio Engineering).
**Empirical Benchmark Anchor:** November 2026 Order-Book & Cohort Telemetry — During the November 9–13 drawdown from **$75,771** down to **$68,450**, exchange order-book depth thinned by 33% to **$72M** with visible limit-book spoofing (large resting bid/ask walls flashing and pulling within seconds), contrasted against steady, time-sliced **TWAP/VWAP accumulation** by `100–10,000 BTC` entities near the **$68,000** liquidity zone.

---

## 1. Machine-Readable State & Routing Block (Python / Hermes / NotebookLM Index)

```yaml
module_id: "MOD_21"
entry_type: "CONDITIONAL_SIGNAL_UNIT"
waterfall_pillar: "PILLAR_2_ALGO_EXECUTION_FORENSICS"
title: "Algorithmic TWAP/VWAP Accumulation Footprints vs. Spoofed Order-Book Liquidity"

# PILLAR 1 MASTER PERMISSION PRE-CHECK
pillar_1_permission_required: true
cash_lock_override: "If Pillar 1 Macro Regime == RISK_OFF_100_CASH, block entries on intraday TWAPs until multi-day VAH reclaim confirms."

# PRIMARY TELEMETRY TRIGGERS (EXECUTION FOOTPRINT SIGNATURES)
base_regime_triggers:
  twap_buy_signature: "Uniformly spaced small-to-medium market buys (every 1m-5m) on Domestic USD venues (Coinbase/Kraken) driving steady upward Spot CVD slope with low variance"
  twap_sell_signature: "Uniformly spaced market/limit-slice selling (especially 14:00-21:00 UTC AP ETF redemption execution) suppressing rebounds at Session VWAP"
  spoof_wall_signature: "Large resting L2 order-book wall (>= 3.0x median depth) appearing within 0.5%-1.5% of spot and vanishing (< 5% filled) as price approaches within 0.15%"
  iceberg_absorption_signature: "Repeated fills at an exact price tick exceeding visible L2 book size by >= 5.0x without price breaking through"

# ANTI-TRAP CIRCUIT BREAKERS
circuit_breakers:
  CB_01_PREMATURE_CLOSE: "NEVER buy or sell based on a visible L2 order-book heatmap wall alone; resting limit orders can be canceled in milliseconds (spoofing)."
  CB_02_VENUE_CONTAMINATION: "Authenticate TWAP/iceberg footprints exclusively on Domestic Fiat (USD) spot books; ignore offshore zero-fee maker-rebate ping-pong."
  CB_03_FORCED_FLOW_STANDDOWN: "Do not step in front of an active institutional TWAP sell program (e.g., multi-hundred-million ETF redemption execution) until the time-slice completes."
  CB_04_SIGNAL_HALF_LIFE: "Intraday TWAP/VWAP footprints govern 2H-24H execution precision; anchor swing invalidation stops to structural Volume Profile VAL/VAH."

# RISK & SIZING CONSTANTS (PILLAR 4)
risk_parameters:
  max_portfolio_risk_pct: 0.75
  leverage_permitted: 1.0 # Strict Unleveraged Spot Only
  exit_protocol: "TWO_STAGE_STRUCTURAL"
```

---

## 2. Protective Circuit Breakers (Mandatory Pre-Execution Filters)

* **Circuit Breaker 1 — The L2 Order-Book Mirage Law (`CB-01`):** Public order-book heatmaps show *intent*, not *commitment*. Spoofing algorithms routinely flash $20M–$50M bid walls below spot to trick retail traders into buying, then cancel the wall milliseconds before price touches it. **Never trust a resting wall until actual executed trades (tape/footprint) prove the wall absorbed volume without pulling.**
* **Circuit Breaker 2 — Iceberg vs. Spoof Distinction:**
  * **Spoof Wall:** Visible size = 500 BTC $\rightarrow$ Price approaches $\rightarrow$ Order canceled $\rightarrow$ Executed volume = 5 BTC. *(Trap — Do Not Trade).*
  * **Institutional Iceberg:** Visible size = 25 BTC $\rightarrow$ Market orders hit it repeatedly $\rightarrow$ Executed volume = 600 BTC at the exact same price level without breaking *(True Absorption — Trade With It)*.
* **Circuit Breaker 3 — Respect Active Institutional TWAP Sellers (`CB-03`):** When an Authorized Participant (AP) or large fund executes a 4-hour TWAP sell program to settle ETF redemptions, trying to catch the bottom mid-program bleeds capital. Wait for the TWAP cadence to stop and Session VWAP to be reclaimed.
* **Circuit Breaker 4 — Domestic Venue Verification (`CB-02`):** True institutional TWAP algorithms execute on regulated USD venues (Coinbase Prime, Kraken, Bitstamp, LMAX) to minimize market impact.

---

## 3. Core Conditional Signal Units (`Condition A -> Outcome B -> Rule C`)

### CSU-21A: Verified Iceberg Bid Absorption + TWAP Buy Ignition ("Institutional Floor & Lift")
* **Trigger Condition A (The Telemetry Scan):**
  1. At a key structural level (Volume Profile VAL, 4H HVN, or STH Realized Price), the 15m footprint records **executed sell volume exceeding visible L2 bid depth by `>= 5x` at a single price band without price breaking lower** (`verified passive iceberg absorption`).
  2. Immediately following absorption, **Coinbase/Kraken USD Spot CVD** begins climbing in a **steady, linear staircase (`TWAP buy algorithm`)**, reclaiming **Session VWAP** and the 15m Developing POC.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** A large institutional buyer first absorbed all panicked market sellers via a hidden iceberg bid, and has now switched to an automated TWAP accumulation algorithm to build a multi-hour/multi-day spot position.
  * **Probable Trajectory:** Steady, relentless upward price grind supported by continuous algorithmic bid replenishment on every minor dip to Session VWAP.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Entry Trigger:** Execute **Unleveraged Spot Long** on a pullback touch of **Session VWAP / 15m Developing POC** while the linear USD Spot CVD staircase remains active.
  * **Position Sizing Formula (0.75% Risk Ceiling):**
    `Spot Position (BTC) = (0.0075 * Total Portfolio Equity) / (Entry Price - Invalidation Stop Price)`
  * **Hard Structural Invalidation Stop:** Place hard stop immediately beneath the **verified iceberg absorption price floor**.
  * **Two-Stage Profit Exit Protocol:**
    * **Stage 1 Exit (50% of Position):** Close 50% at the upper `2.0-Sigma VWAP Standard Deviation Band` / overhead VAH; move stop to breakeven.
    * **Stage 2 Exit (Remaining 50%):** Trail behind Session/Anchored VWAP until the TWAP buy staircase flattens and price closes below VWAP.

### CSU-21B: Institutional TWAP Distribution Suppression ("VWAP Ceiling Pin")
* **Trigger Condition A (The Telemetry Scan):**
  1. **Domestic USD Spot CVD** declines in a smooth, relentless downward staircase (`algorithmic TWAP sell program`), capping every intraday bounce directly at **Session VWAP** or the 1H POC.
  2. Every time price approaches Session VWAP, hidden iceberg ask orders absorb market buys and push price back down (`negative delta at VWAP`).
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Institutional desks or ETF redemption programs are systematically liquidating spot inventory in time-sliced blocks to avoid crashing the book all at once, patiently selling into every retail bounce.
  * **Probable Trajectory:** Grinding downward stair-step breakdown until the TWAP sell quota is completely filled.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **LOCK 100% CASH (Zero Dip-Buying Permitted).** Do not buy any bounce while price remains trapped below a declining Session VWAP with linear negative USD Spot CVD. Wait for `Mutation M1` (TWAP exhaustion + VWAP reclaim).

### CSU-21C: Bid-Wall Spoof Rug-Pull Trap ("Liquidity Mirage Breakdown")
* **Trigger Condition A (The Telemetry Scan):**
  1. Large resting bid walls appear on L2 order books `0.5%–1.5%` below spot (`creating bullish heatmap optics`), attracting retail front-running buyers (`Perp CVD spikes up`).
  2. As spot price drifts down toward the wall, **the resting bid wall is canceled (`pulled`) before absorbing significant volume**, and price slices cleanly through the level on thin volume (`MOD 08D`).
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Market makers or large sellers flashed fake support to induce retail longs to buy higher up, then pulled the bid so they could fill lower or trigger stop-losses.
  * **Probable Trajectory:** Sharp air-pocket drop through the vacated price zone.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **CIRCUIT BREAKER 1 (`CB-01`) ENFORCED: DO NOT ENTER.** If already long, exit immediately if price breaks through the pulled-wall price level.

### CSU-21D: Ask-Wall Spoof & Stop-Hunt Breakout ("Upward Liquidity Sweep")
* **Trigger Condition A (The Telemetry Scan):**
  1. Large resting ask walls sit just above resistance (`VAH`), suppressing price while **Domestic USD Spot CVD quietly accumulates below the wall**.
  2. Suddenly, the ask wall is **pulled** (or eaten in a single institutional sweep) and price explodes through VAH on surge volume (`MOD 11B`).
* **Observed Outcome B (The Mechanical Trajectory):**
  Accumulating institutions used a resting ask wall to cap price while filling their TWAP orders below resistance; once filled, they removed the cap and let price reprice higher.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Entry Trigger:** Execute **Unleveraged Spot Long** on the first 15m pullback retest of the **cleared ask-wall / VAH level** (now acting as support), sized strictly to the **0.75% Risk Ceiling**.

---

## 4. Dynamic Regime Mutation Lookup Matrix (`M1` through `M8`)

| Mutation ID | Initial State | Telemetry Mutation Observed (`Condition A'`) | Mechanical Meaning (`Outcome B'`) | Mandatory Execution Override (`Rule C'`) |
| :--- | :--- | :--- | :--- | :--- |
| **M1: TWAP Sell Program Completion** | `CSU-21B` (TWAP Selling) | Linear negative USD Spot CVD abruptly **flattens at a round hour (`e.g., 16:00 or 21:00 UTC`)**, selling vanishes, and price reclaims **Session VWAP**. | Institutional time-sliced sell order finished its quota; overhead suppression is gone. | Lift `CSU-21B` lock; evaluate `0.375%–0.75% Risk` Spot Long upon 15m/1H VWAP + VAL reclaim. |
| **M2: TWAP Buy Program Exhaustion** | `CSU-21A` (TWAP Buying) | Steady upward USD Spot CVD staircase stops abruptly, price loses **Session VWAP**, and `15m` delta turns negative. | Institutional accumulation tranche is complete; support bid has stepped away. | **Execute Stage 2 Profit Exit (Close remaining 50% Spot Swing)** immediately upon VWAP loss. |
| **M3: Iceberg Floor Overwhelmed** | `CSU-21A` (Iceberg Support) | After absorbing `500+ BTC` at a fixed price, the iceberg bid finally breaks downward on a heavy volume spike (`delta plunge`). | Buyer's entire reserve quota was filled and sellers still have excess inventory to dump. | **Hard Stop Triggered / Enforce 100% Cash Lock.** Never re-bid a broken iceberg level. |
| **M4: Multi-Day Anchored VWAP (AVWAP) Reclaim** | Structural Correction | Price reclaims the **Anchored VWAP** anchored to the major breakdown high (e.g., `$75,771` Nov 9 high) with positive USD Spot CVD. | Average buyer since the breakdown is back in profit; institutional trend control shifted bullish. | High-conviction structural confirmation; authorize full `0.75% Risk` Spot Long on AVWAP retest. |
| **M5: Thin-Book Slippage Spike** | Thin Depth (`< $80M`) | Single market orders of `50–100 BTC` move spot price by `> 0.5%` (extreme order-book fragility). | Market makers have widened spreads and pulled depth; high stop-hunting hazard. | **Widen Stop Distance via Garman-Klass (`MOD 12`)** and shrink BTC notional size to preserve `0.75%` cap. |
| **M6: Round-Number Psychological Magnet** | Any Intraday Move | Massive clusters of resting orders sit at major round figures (`$70,000`, `$68,000`, `$65,000`) with heavy footprint battles. | Institutional option strikes (`MOD 25/26`) and psychological liquidity pools converge. | Never place stops *at* round numbers; place stops `0.5%–1.0%` *beyond* the round-number sweep zone. |
| **M7: Offshore Wash-TWAP Filter** | `CSU-21A` (False Signal) | Offshore USDT exchanges show rhythmic small trades, but **Coinbase/Kraken USD Spot CVD is flat/negative**. | Offshore volume-bot churn—zero real institutional accumulation. | **Circuit Breaker 2 Tripped: Ignore Signal.** Lock 100% Cash. |
| **M8: End-of-Day MOC / ETF Basket Spike** | `20:45–21:00 UTC` | Sudden volume surge in the final 15 minutes of US equity trading pushing price sharply away from Session VWAP. | Market-on-Close (MOC) institutional rebalancing / ETF share creation settlement. | Wait 15 minutes after `21:00 UTC` to verify whether Asia session accepts or fades the MOC move. |
