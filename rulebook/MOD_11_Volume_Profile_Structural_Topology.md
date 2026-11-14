# PROJECT CORTEX-BTC — MODULE 11: VOLUME PROFILE STRUCTURAL TOPOLOGY (VAH, VAL, POC & LVN)
**Waterfall Tier:** Pillar 2 (Microstructure, Order Flow & Auction Market Theory) cross-verified with Pillar 1 (Macro Permissions) and Pillar 4 (Portfolio Engineering).
**Empirical Benchmark Anchor:** November 2026 Auction Structure Telemetry — Price oscillating inside a multi-day Value Area between **$71,218 (VAL)** and **$75,771 (VAH / STH Realized Price)** with Developing POC near **$73,800**, before losing the **$73,000** lower value shelf and traversing a Low-Volume Node (LVN) vacuum down toward the **$68,000** high-volume bid cluster.

---

## 1. Machine-Readable State & Routing Block (Python / Hermes / NotebookLM Index)

```yaml
module_id: "MOD_11"
entry_type: "CONDITIONAL_SIGNAL_UNIT"
waterfall_pillar: "PILLAR_2_VOLUME_PROFILE_TOPOLOGY"
title: "Volume Profile Structural Topology (15m/1H VAH, VAL, POC Reclaims & LVN Breakouts)"

# PILLAR 1 MASTER PERMISSION PRE-CHECK
pillar_1_permission_required: true
cash_lock_override: "If Pillar 1 Macro Regime == RISK_OFF_100_CASH, block all VAH breakout and VAL spring Long entries."

# PRIMARY TELEMETRY TRIGGERS (AUCTION MARKET GEOMETRY)
base_regime_triggers:
  value_area_definition: "70% of rolling session/composite volume bounded by VAL (Value Area Low) and VAH (Value Area High) around POC (Point of Control)"
  acceptance_rule: "Two consecutive 15m closes (or one 1H close) holding outside prior VAH/VAL with positive Domestic USD Spot CVD"
  rejection_spring_rule: "Wick excursion <= -0.5% to -2.0% beyond VAL/VAH followed by immediate 15m close back inside Value Area + CVD absorption"
  lvn_vacuum_rule: "Volume node density <= 20th percentile separating two High-Volume Nodes (HVNs >= 80th percentile)"

# ANTI-TRAP CIRCUIT BREAKERS
circuit_breakers:
  CB_01_PREMATURE_CLOSE: "NEVER buy the first 15m candle poking above VAH; wait for acceptance or a successful pullback retest of VAH as support."
  CB_02_VENUE_CONTAMINATION: "Compute composite Volume Profile and footprint delta using Domestic USD spot + primary institutional liquidity venues."
  CB_03_FORCED_FLOW_STANDDOWN: "Do not fade a VAL breakdown during an active liquidation cascade (MOD 03) until OI stabilizes."
  CB_04_SIGNAL_HALF_LIFE: "Intraday 15m/1H Value Areas govern 6H-48H tactical execution; anchor structural swing stops to 4H/Composite HVNs."

# RISK & SIZING CONSTANTS (PILLAR 4)
risk_parameters:
  max_portfolio_risk_pct: 0.75
  leverage_permitted: 1.0 # Strict Unleveraged Spot Only
  exit_protocol: "TWO_STAGE_STRUCTURAL"
```

---

## 2. Protective Circuit Breakers (Mandatory Pre-Execution Filters)

Before any Scenario in Module 11 can authorize a spot order, all four circuit breakers must pass:
* **Circuit Breaker 1 — Auction Acceptance vs. Sweep Filter (`CB-01`):** In Auction Market Theory, 70%–80% of initial pokes outside a Value Area fail and rotate back to the Point of Control (POC). You must never buy a raw breakout tick; require **acceptance** (retest of VAH holding as support) or a **failed breakdown spring** (reclaim of VAL).
* **Circuit Breaker 2 — HVN Magnet Trap Warning:** Entering a trade directly into an overhead High-Volume Node (HVN) or static POC offers terrible reward-to-risk because HVNs act as two-way liquidity magnets that stall momentum. Entries must launch *away* from HVNs across Low-Volume Nodes (LVNs).
* **Circuit Breaker 3 — Liquidation Cascade Stand-Down (`CB-03`):** If price slices downward through VAL during a liquidation cascade (`OI dropping > -1.5%/hr`), do not place blind limit bids at VAL—wait for `CSU-11C` reclaim confirmation.
* **Circuit Breaker 4 — Pillar 1 Macro Permission Gate:** Confirm secular macro trend permission before trading upside Value Area rotations.

---

## 3. Core Conditional Signal Units (`Condition A -> Outcome B -> Rule C`)

### CSU-11A: Look-Below-and-Fail Spring ("VAL Liquidity Sweep & Reclaim")
* **Trigger Condition A (The Telemetry Scan):**
  1. Price breaks downward below the multi-day or session **Value Area Low (VAL)**, sweeping resting retail stop-losses sitting beneath support.
  2. **Rejection & Reclaim:** Within 1 to 4 bars (15m/1H), price fails to build volume below VAL, snaps back **inside the Value Area**, and closes firmly above **VAL**.
  3. **Order-Flow Verification:** **Domestic Fiat (USD) Spot CVD** prints a clear bullish absorption divergence on the sweep (`passive limit bids absorbing market sells`), and Rough Path `A_P,V` inflects positive.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Institutional buyers used the stop-loss liquidity pool below VAL to fill large spot bids at a discount without pushing price up prematurely.
  * **Probable Trajectory:** Under the **80% Auction Rotation Rule**, once price re-enters and accepts inside a Value Area after a failed breakdown, it rotates across the entire distribution—first to the **POC** and then to the **Value Area High (VAH)**.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Entry Trigger:** Execute **Unleveraged Spot Long** upon the confirmed **15m/1H close back above VAL** (or immediate retest of VAL from above) with positive Domestic USD Spot CVD.
  * **Position Sizing Formula (0.75% Risk Ceiling):**
    `Spot Position (BTC) = (0.0075 * Total Portfolio Equity) / (Entry Price - Invalidation Stop Price)`
  * **Hard Structural Invalidation Stop:** Place hard stop strictly beneath the **failed breakdown swing wick low** (typically `0.5%–1.5%` below VAL).
  * **Two-Stage Profit Exit Protocol:**
    * **Stage 1 Exit (50% of Position):** Close 50% at the composite **Point of Control (POC)** (the primary high-volume magnet); move stop on remaining 50% to breakeven.
    * **Stage 2 Exit (Remaining 50%):** Close remaining 50% at the **Value Area High (VAH)** unless `CSU-11B` breakout acceptance triggers.

### CSU-11B: Low-Volume Node (LVN) Fast-Traverse Breakout ("Initiation Away From Value")
* **Trigger Condition A (The Telemetry Scan):**
  1. Price breaks above the **Value Area High (VAH)** and enters a **Low-Volume Node (LVN)** air pocket (`volume density <= 20th percentile`).
  2. **Acceptance Verification:** Price holds above VAH for `>= 2 consecutive 15m closes` (or 1H close), Developing POC (`dPOC`) migrates upward toward the breakout zone, and **Domestic USD Spot CVD** + Rough Path `A_P,V` (`>= +1.5 Z`) surge upward.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Market participants have rejected the prior lower value range and are aggressively repricing Bitcoin upward to establish a new equilibrium.
  * **Probable Trajectory:** Because LVNs contain minimal historical resting liquidity, price traverses the LVN rapidly until it reaches the next overhead **High-Volume Node (HVN)** or HTF Value Area.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Entry Trigger:** Execute **Unleveraged Spot Long** on a shallow 15m pullback to the **reclaimed VAH / LVN entry lip** where sellers fail to push price back into the old Value Area. Size strictly via the **0.75% Risk Formula** with hard stop just inside the old Value Area (`below VAH`).
  * **Two-Stage Profit Exit Protocol:**
    * **Stage 1 Exit (50% of Position):** Close 50% upon reaching the base of the next overhead **High-Volume Node (HVN)**; move stop to breakeven.
    * **Stage 2 Exit (Remaining 50%):** Trail behind the rising 1H Developing POC (`dPOC`).

### CSU-11C: Look-Above-and-Fail ("VAH Sweep Rejection & Downward Rotation")
* **Trigger Condition A (The Telemetry Scan):**
  1. Price pokes above the **Value Area High (VAH)**, sweeping breakout buyers and short stops.
  2. Price fails to hold above VAH, closes back **below VAH** on the 15m/1H chart, while **Domestic USD Spot CVD** diverges negatively (`Perp CVD positive, USD Spot CVD negative`) and `A_P,V <= -1.25 Z-score`.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Institutional spot sellers used the breakout liquidity above VAH to distribute inventory into late breakout chasers.
  * **Probable Trajectory:** High-probability rotation downward through the **POC** toward the **Value Area Low (VAL)**.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **BLOCK ALL LONG ENTRIES. LOCK 100% CASH.** If holding an existing Spot Long from lower inside the range, immediately execute **Stage 2 Full Profit Exit** upon the close back below VAH.

### CSU-11D: High-Volume Node (HVN) Equilibrium Chop ("POC Balance Lock")
* **Trigger Condition A (The Telemetry Scan):**
  1. Price oscillates tightly within `+/- 0.75%` of a multi-day **High-Volume Node / Point of Control (POC)**.
  2. Developing POC (`dPOC`) remains stationary, Garman-Klass volatility compresses below the 20th percentile, and Spot/Perp CVD slopes are flat.
* **Observed Outcome B (The Mechanical Trajectory):**
  Two-sided institutional liquidity is in complete equilibrium; market makers are harvesting bid-ask spread while directional traders get chopped to pieces.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **STANDBY / 100% CASH PRESERVATION.** Zero trades allowed inside an HVN magnet zone. Wait for price to reach an edge (`VAL` or `VAH`) and trigger `CSU-11A` or `CSU-11B`.

---

## 4. Dynamic Regime Mutation Lookup Matrix (`M1` through `M8`)

| Mutation ID | Initial State | Telemetry Mutation Observed (`Condition A'`) | Mechanical Meaning (`Outcome B'`) | Mandatory Execution Override (`Rule C'`) |
| :--- | :--- | :--- | :--- | :--- |
| **M1: Developing POC (dPOC) Migration** | `CSU-11B` (LVN Breakout) | Following a VAH breakout, the session **`dPOC` jumps upward** above the old VAH and holds as support. | Volume acceptance has officially shifted higher; old resistance is now confirmed institutional value. | **Hold Spot Long**; raise hard invalidation stop directly beneath the newly established `dPOC`. |
| **M2: Failed Acceptance Re-Entry** | `CSU-11B` (LVN Breakout) | Within 1–3 hours of breaking VAH, price loses the `dPOC`, drops back **below VAH**, and USD Spot CVD turns negative. | Breakout mutated into a `CSU-11C` "Look-Above-and-Fail" bull trap. | **Exit Spot Long Immediately at Market; enforce 100% Cash Lock.** |
| **M3: VAL Spring Stall at POC** | `CSU-11A` (VAL Reclaim) | Price rotates from VAL up to the **POC**, prints heavy ask absorption (`CVD rising, price flat`), and `dPOC` locks at the middle. | Rotation ran out of steam at the primary volume magnet rather than reaching VAH. | **Stage 1 (50%) already banked at POC**; tighten remaining 50% stop to breakeven immediately. |
| **M4: VAL Breakdown Acceptance** | `CSU-11A` (False Spring) | Price pokes below VAL, attempts a weak bounce that **fails at VAL from below**, and `dPOC` migrates downward below VAL. | Market accepted lower prices; downward LVN air pocket is now open. | **Hard Stop Triggered / Lock 100% Cash.** Do not re-bid until next lower HTF HVN/VAL. |
| **M5: Single-Print Tail Defense** | `CSU-11A` / `11B` | Impulse leaves behind a **15m/1H single-print tail** (thin vertical volume column) and subsequent dips bounce *before* filling half the tail. | Aggressive institutional buyers are defending the impulse front-run without letting price retest. | **Trail Stop Beneath Single-Print Tail Midpoint** to lock in asymmetrical trend gains. |
| **M6: Naked POC (nPOC) Magnet Hit** | Any Trend Leg | Price traverses an LVN and hits an untouched historical **Naked POC (`nPOC`)** with `A_P,V` climaxing (`> +2.5 Z`). | Untested historical high-volume liquidity pool triggers automatic institutional profit-taking/rebalancing. | **Execute Stage 1 (50%) or Stage 2 (100%) Profit Exit** directly into the `nPOC` touch. |
| **M7: Triple-Drive Exhaustion at VAH** | `CSU-11A` (Rotation to VAH) | Price tests VAH three times with progressively **lower USD Spot CVD** and shrinking volume on each push. | Buying pressure is exhausted at the upper boundary of value; sellers are absorbing. | **Close Remaining Spot Long at VAH**; do not wait for a breakout. |
| **M8: Composite Range Expansion** | `CSU-11D` (HVN Chop) | After days of tight POC balance, price sweeps VAL (`CSU-11A`), reclaims POC, and breaks VAH (`CSU-11B`) in one session. | Classic "outside-day" auction expansion following volatility compression. | Execute `CSU-11A` at VAL, bank 50% at POC, and trail remaining 50% through VAH breakout. |
