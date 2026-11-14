# MOD 42 — Classical Structural Shapes & Liquidity-Pool Authentication Engine (Pillar 2)

*Source File: `MOD_42_Classical_Structural_Shapes_and_Liquidity_Pool_Authentication.md`*

---

# PROJECT CORTEX-BTC — MODULE 42: CLASSICAL STRUCTURAL SHAPES & LIQUIDITY-POOL AUTHENTICATION ENGINE
**Waterfall Tier:** Pillar 2 (Microstructure, Order Flow & Path Geometry) integrated with Pillar 1 (Macro) and Pillar 4 (Portfolio Engineering).
**Empirical Benchmark Anchor:** Classical chart patterns (Head & Shoulders, Double Tops/Bottoms, Wedges, Flags) are visual maps of resting liquidity pools, not standalone execution triggers. They must be authenticated by order-flow and rough-path filters to distinguish institutional execution from retail traps.

---

## 1. Machine-Readable State & Routing Block (Python / Hermes / NotebookLM Index)

```yaml
module_id: "MOD_42"
entry_type: "CONDITIONAL_SIGNAL_UNIT"
waterfall_pillar: "PILLAR_2_STRUCTURAL_SHAPES"
title: "Classical Structural Shapes & Liquidity-Pool Authentication Engine"

# PILLAR 1 MASTER PERMISSION PRE-CHECK
pillar_1_permission_required: true
cash_lock_override: "If Pillar 1 Macro Regime == RISK_OFF_100_CASH, block all Bull Flag and Double Bottom breakouts. Only Rising Wedge and Head & Shoulders breakdowns are actionable."

# PRIMARY TELEMETRY TRIGGERS (STRUCTURAL SHAPES & AUTHENTICATION)
base_regime_triggers:
  reversal_shapes: ["Head & Shoulders", "Inverse Head & Shoulders", "Double Top", "Double Bottom", "Wyckoff Spring"]
  continuation_shapes: ["Bull Flag", "Bear Flag", "Rising Wedge", "Falling Wedge"]
  authentication_requirements:
    volume_profile: "15m/1H VAH/VAL/POC interaction"
    order_flow: "Domestic USD Spot CVD (MOD 05/07)"
    rough_path: "Levy Signed Areas A_P,V and A_CVD,OI (MOD 08/09)"
    bar_count_discipline: "1-3 completed 1H bars (or 1-2 4H bars) for sweep-and-reclaim; 4+ 1H closes (or 2+ 4H closes) for structural breakdown (MOD 00C)"

# ANTI-TRAP CIRCUIT BREAKERS
circuit_breakers:
  CB_01_PREMATURE_CLOSE: "NEVER trade a classical shape on visual appearance alone. A neckline or wedge boundary is meaningless without volume/delta authentication."
  CB_02_VENUE_CONTAMINATION: "Validate shape breakouts using Domestic USD Spot CVD; offshore-only perp breakouts are usually traps."
  CB_03_FORCED_FLOW_STANDDOWN: "During active liquidation cascades (MOD 03), disregard all bullish shapes (e.g., Bull Flags) until OI stabilizes."
  CB_04_SIGNAL_HALF_LIFE: "Structural shapes on 1H/4H timeframes govern 1-3 day swing execution; anchor stops to structural Volume Profile nodes, not diagonal trendlines."

# RISK & SIZING CONSTANTS (PILLAR 4)
risk_parameters:
  max_portfolio_risk_pct: 0.75
  leverage_permitted: 1.0 # Strict Unleveraged Spot Only
  exit_protocol: "TWO_STAGE_STRUCTURAL"
```

---

## 2. Protective Circuit Breakers (Mandatory Pre-Execution Filters)

Before any Scenario in Module 42 can authorize a spot decision, all four circuit breakers must pass:

* **Circuit Breaker 1 — The Diagonal Fallacy (`CB-01`):** Diagonal trendlines and geometric shapes have no causal force. Institutional algorithms execute based on horizontal liquidity pools (Volume Profile VAH/VAL/POC) and order-book depth. Treat classical shapes strictly as *maps* of where retail liquidity is resting, and wait for order-flow authentication.
* **Circuit Breaker 2 — Bar-Count Discipline (`CB-04`):** A neckline or wedge break requires **1–3 completed 1H bars** (or **1–2 completed 4H bars**) for a sweep-and-reclaim. **4+ consecutive 1H closes** (or **2+ consecutive 4H closes**) below support confirms a true structural breakdown.
* **Circuit Breaker 3 — Liquidation Contagion (`CB-03`):** Never attempt to trade a Bull Flag or Double Bottom during an active liquidation cascade (`MOD 03`). Wait for OI contraction to decelerate and 15m footprint absorption to print.
* **Circuit Breaker 4 — Pillar 1 Macro Gate:** Verify secular macro permissions before trading bullish reversal or continuation shapes.

---

## 3. Core Conditional Signal Units (`Condition A -> Outcome B -> Rule C`)

### CSU-42A: Double Top / Head & Shoulders Breakdown ("Retail Exhaustion & Distribution")
* **Trigger Condition A (The Telemetry Scan):**
  1. Price forms equal highs or a marginal higher high (`+1%` to `+6%` flat exhaustion per `MOD 41`), followed by a drop below the **Horizontal Neckline / 4H VAL**.
  2. **Authentication:** Breakdown is accompanied by **aligned Spot + Perp outflow (`Quad 4` / `MOD 05D`)** and negative Rough Path curvature (`A_P,V <= -1.5 Z`).
  3. Bar-count discipline confirms **4+ consecutive 1H closes** below the neckline.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Institutional sellers used the initial peaks to distribute inventory into retail FOMO; the neckline breakdown confirms exhaustion of bid liquidity.
  * **Probable Trajectory:** Sustained markdown toward the next major lower-timeframe Volume Profile POC or Liquidation Cluster.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **ENFORCE 100% CASH LOCK.** If holding an active Spot Swing Long, execute immediate Stage 2 Full Profit Exit.

### CSU-42B: Double Bottom / Inverse H&S / Wyckoff Spring ("Liquidity Sweep Reversal")
* **Trigger Condition A (The Telemetry Scan):**
  1. Price sweeps equal lows or the left shoulder trough, triggering retail stop-losses (`Wyckoff Spring` / `MOD 11A` VAL sweep).
  2. **Authentication:** 15m/1H footprint shows **passive limit-bid absorption (`MOD 06A`)**, and **Domestic USD Spot CVD** turns sharply positive. Price reclaims the **15m/1H Neckline / VAH**.
  3. `MOD 03A` confirms a post-flush OI reset.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Institutional buyers engineered a liquidity sweep to fill large spot bids at a discount, trapping late breakout shorts.
  * **Probable Trajectory:** High-probability V-shaped or U-shaped mean-reversion rally.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Entry Trigger:** Execute **Unleveraged Spot Long** upon verified 15m/1H Neckline / VAH reclaim with positive USD Spot CVD.
  * **Position Sizing Formula:** Size strictly via the **0.75% Risk Ceiling** with hard stop beneath the Spring / Double Bottom wick low.

### CSU-42C: Rising Wedge Breakdown ("Leveraged Long Crowding Trap")
* **Trigger Condition A (The Telemetry Scan):**
  1. Price grinds higher within converging upward trendlines into overhead supply (e.g., 4H/1D VAH or 200D MA).
  2. **Authentication:** Volume contracts (`A_P,V` rolling negative), **Domestic USD Spot CVD flattens/falls**, and **offshore Perp OI + funding climb (`MOD 02B` / `Quad 3`)**.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** The rally is driven entirely by fragile paper leverage rather than genuine spot demand; institutional sellers are capping the advance.
  * **Probable Trajectory:** High vulnerability to a cascading long-liquidation flush once momentum stalls.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **BLOCK NEW LONG ENTRIES. LOCK 100% CASH.** Treat Rising Wedges strictly as top warnings. Exit active tactical longs immediately.

### CSU-42D: Bull Flag / Falling Wedge Breakout ("Volatility Squeeze Continuation")
* **Trigger Condition A (The Telemetry Scan):**
  1. Price consolidates in a parallel downward channel (Flag) or converging downward lines (Wedge) following a strong bullish impulse.
  2. **Authentication:** **Garman-Klass volatility squeezes (`MOD 12A`)** and leverage voluntarily bleeds (`MOD 03D`: OI drifting down while funding resets), while **Domestic USD Spot CVD holds steady**.
  3. Price breaks above the 15m/1H Flag VAH with **`A_P,V >= +1.5 Z` (`MOD 08A`)**.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Orderly digestion of a prior impulse; weak hands are shaking out while institutions quietly re-accumulate.
  * **Probable Trajectory:** Explosive upside continuation once the volatility squeeze releases.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Entry Trigger:** Execute **Unleveraged Spot Long** on the first 15m/1H pullback retest of the reclaimed **Flag VAH** with positive USD Spot CVD. Size strictly to the **0.75% Risk Ceiling**.

---

## 4. Dynamic Regime Mutation Lookup Matrix (`M1` through `M8`)

| Mutation ID | Initial State | Telemetry Mutation Observed (`Condition A'`) | Mechanical Meaning (`Outcome B'`) | Mandatory Execution Override (`Rule C'`) |
| :--- | :--- | :--- | :--- | :--- |
| **M1: Head & Shoulders Right Shoulder Failure** | `CSU-42A` (H&S Formation) | Price forms the right shoulder but fails to break the neckline; instead, it reclaims the 1H/4H VAH with surging USD Spot CVD. | Bearish distribution pattern invalidated; institutional buyers absorbed the sell pressure. | **Block Cash Lock; Evaluate `0.75% Risk` Spot Long** on VAH reclaim. |
| **M2: Inverse H&S False Breakout** | `CSU-42B` (iH&S Breakout) | Price breaks above the iH&S neckline but immediately drops back below with negative USD Spot CVD and `A_P,V <= -1.5 Z`. | Bullish reversal trap; sellers overwhelmed the breakout liquidity. | **Hard Stop Triggered / Enforce 100% Cash Lock.** |
| **M3: Bull Flag Liquidation Cascade** | `CSU-42D` (Bull Flag) | During the Flag consolidation, OI collapses (`> -1.5%/hr`) and price slices through the Flag VAL on heavy volume. | Orderly consolidation mutated into a forced deleveraging waterfall. | **Enforce Immediate 100% Cash Lock (`CB-03`).** |
| **M4: Rising Wedge Blow-Off** | `CSU-42C` (Rising Wedge) | Price breaks *upward* out of the Rising Wedge on extreme funding (`> +0.05%/8h`) and `Skew_25D <= -5%`. | Terminal retail leverage blow-off top (`MOD 27B`). | **Execute Stage 2 Full Profit Exit (100% Cash).** |
| **M5: Symmetrical Triangle Compression** | Range Consolidation | Price forms a symmetrical triangle with decreasing volume; Garman-Klass volatility drops `< 15th percentile`. | Coiling energy for an imminent regime birth (`MOD 12A`). | Prepare breakout triggers; enter **only** in the direction where `A_P,V` breaks `>= +1.5 Z` with USD Spot CVD. |
| **M6: Cup & Handle Accumulation** | `CSU-42B` (U-Shape Recovery) | Price forms a rounded "Cup" recovery, followed by a tight "Handle" consolidation near VAH with steady USD Spot CVD. | Sustained institutional accumulation; overhead supply is being absorbed smoothly. | **Authorize `0.75% Risk` Spot Long** on Handle VAH breakout. |
| **M7: Offshore-Only Shape Breakout** | `CSU-42D` (Flag Breakout) | Bull Flag breaks upward on Binance USDT volume, but Coinbase USD Spot CVD remains negative. | Breakout lacks real spot backing; high probability of a head-fake. | **Circuit Breaker 2 Tripped: Reject Signal.** Lock 100% Cash. |
| **M8: Structural Shape Resonance** | Multi-Timeframe | 1H Double Bottom aligns perfectly with 4H Inverse Head & Shoulders and 1D Rising Trendline support. | Fractal institutional accumulation across tactical and structural horizons. | **Highest-Conviction Swing Trigger:** Deploy full `0.75% Risk` Spot allocation on neckline/VAH reclaim. |
