# PROJECT CORTEX-BTC — MODULE 43: ALGORITHMIC FIBONACCI CONFLUENCE & HARMONIC IMPULSE MEASUREMENT

**Waterfall Tier:** Pillar 2 (Microstructure & Path Geometry) and Pillar 3 (Execution Matrix).  
**Empirical Benchmark Anchor:** Replaces subjective retail technical analysis (arbitrary wave counting and discretionary Fibonacci drawing) with strict algorithmic anchors. Fibonacci retracements are mapped exclusively from deterministic Lookback Extremes (e.g., 90D Absolute High to 90D Absolute Low). Wave theory is digitized into Average True Range (ATR) harmonic impulses paired with a ZigZag algorithm.

---

## 1. Machine-Readable State & Routing Block (Python / Hermes / NotebookLM Index)

```yaml
module_id: "MOD_43"
entry_type: "CONDITIONAL_SIGNAL_UNIT"
waterfall_pillar: "PILLAR_2_PATH_GEOMETRY"
title: "Algorithmic Fibonacci Confluence & Harmonic Impulse Measurement"

# ALGORITHMIC ANCHORS
computational_parameters:
  fibonacci_anchors:
    tactical_lookback: "Rolling 30-Day Absolute High to 30-Day Absolute Low"
    structural_lookback: "Rolling 90-Day Absolute High to 90-Day Absolute Low"
    secular_lookback: "Cycle ATH to Cycle Bear Low (or First-Week Flush Wick)"
  valid_retracement_ratios: [0.382, 0.500, 0.618, 0.786]
  valid_extension_ratios: [1.272, 1.618, 2.618]
  wave_measurement_engine:
    algorithm: "ZigZag (Depth: 5%, Deviation: 5%) paired with 14-period ATR"
    impulse_definition: "Unidirectional thrust >= 2.0 ATR without a counter-close > 1.0 ATR"

# ANTI-TRAP CIRCUIT BREAKERS
circuit_breakers:
  CB_01_NO_SUBJECTIVE_ANCHORS: "Never draw Fibonacci levels from intermediate swing highs/lows. Anchors must be the absolute extremes of the defined deterministic lookback period."
  CB_02_THE_ISOLATION_BAN: "A Fibonacci level (e.g., 0.618) has zero causal power alone. It MUST fall within 1% of a Volume Profile node (VAH/VAL/POC) and show Limit-Bid Absorption (MOD 06A) to be actionable."
  CB_03_ATR_WAVE_REPLACEMENT: "Never use subjective Elliott Wave nomenclature (Wave 1-5, A-B-C). Use 'Harmonic Impulse Leg 1, 2, 3' defined strictly by ATR expansion/contraction limits."
  CB_04_MACRO_TREND_FILTER: "Never buy a 0.618 retracement if Pillar 1 Macro Regime is RISK_OFF_100_CASH or ICDM >= 60. Wait for the 0.786 or a Wyckoff Spring sweep."

# RISK & SIZING CONSTANTS (PILLAR 4)
risk_parameters:
  max_portfolio_risk_pct: 0.75
  leverage_permitted: 1.0 # Strict Unleveraged Spot Only
  stop_loss_placement: "1.0 ATR below the confluent Fib/Volume node"
```

---

## 2. Protective Circuit Breakers (Mandatory Pre-Execution Filters)

Before any Fibonacci or Harmonic Impulse signal can authorize a spot decision, all four circuit breakers must pass:

* **Circuit Breaker 1 — No Subjective Anchors (`CB-01`):** Python exclusively dictates the Fib pulls. It queries the 30D or 90D high/low and calculates the sequence. Manual, human-drawn levels adjusting to fit a narrative are blocked.
* **Circuit Breaker 2 — The Isolation Ban (`CB-02`):** A `.618` Golden Ratio means nothing if the order book is empty. The calculated Fib level must intersect within `1%` of a dense Volume Profile node (`MOD 11`) AND exhibit live passive absorption (`MOD 06A`) on the 15m footprint.
* **Circuit Breaker 3 — ATR Wave Replacement (`CB-03`):** Ban "Elliott Wave" guessing. An impulse is only recognized if the ZigZag algorithm records a move `>= 2.0 ATR` without a single daily/4H close retracing `> 1.0 ATR`.
* **Circuit Breaker 4 — Macro Trend Filter (`CB-04`):** Deep retracements (`.786`) are for bear-market loading; shallow retracements (`.382` / `.500`) are for secular bull continuations. Apply the exact level appropriate to the active `MOD 33` Radar regime.

---

## 3. Core Conditional Signal Units (`Condition A -> Outcome B -> Rule C`)

### CSU-43A: Golden Confluence Retracement (The "0.618 + POC" Strike)
* **Trigger Condition A (The Telemetry Scan):**
  1. Python computes the tactical 30D or structural 90D Absolute High-to-Low Fibonacci grid.
  2. Price retraces to the `.500` or `.618` ratio.
  3. **Authentication:** The `.618` level sits within `1%` of the **Volume Profile POC or VAL**.
  4. **Order Flow:** 15m Domestic USD Spot CVD prints positive divergence (`MOD 05A`) and Rough Path `A_P,V >= +1.5 Z`.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** High-frequency algorithms and institutional TWAP engines are front-running the Golden Ratio because it perfectly overlaps with a historical heavy-volume liquidity pool.
  * **Probable Trajectory:** Asymmetric mean-reversion bounce in the direction of the primary macro trend.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Entry Trigger:** Execute **Unleveraged Spot Long** precisely at the confluence band.
  * **Risk:** Cap at `0.75%`, with a hard stop `1.0 ATR` below the `.618` support.

### CSU-43B: Harmonic Impulse Measurement (The "Wave 3" ATR Thrust)
* **Trigger Condition A (The Telemetry Scan):**
  1. Following a consolidation or CSU-43A bounce, price initiates a unidirectional thrust.
  2. **Authentication:** The thrust exceeds **2.0 ATR** (14-period) over consecutive 4H/1D candles without a counter-close exceeding `1.0 ATR`.
  3. Spot CVD and Perp CVD are aligned positive (`Quad 1`).
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** A true, algorithmic "Wave 3" equivalent. Pure momentum expansion fueled by spot accumulation and short-covering.
  * **Probable Trajectory:** Continued upward price discovery until momentum curvature (`A_P,V`) flattens and funding overheats.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** DO NOT sell into the thrust. Trail stop-losses tightly (`1.5 ATR` behind price) and wait for the `MOD 12A` Garman-Klass volatility expansion to peak. Execute Stage 1 profit taking (50%) when the thrust hits the `1.272` Fibonacci Extension.

### CSU-43C: Deep Discount Liquidation Trap (The "0.786 / 0.886" Sweep)
* **Trigger Condition A (The Telemetry Scan):**
  1. Price slices through the `.618` support, triggering mass retail stop-losses.
  2. Price wicks into the **.786 or .886 Fibonacci Retracement**.
  3. **Authentication:** Massive OI wipeout (`MOD 03A`), negative funding, and heavy 15m limit-bid absorption at the `.786`.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** The "Wave 2" or deep mid-cycle shakeout (equivalent to the `-30%` to `-55%` drop mapped in `MOD 41`). Institutions swept the `.618` liquidity pool to fill orders at the deeper `.786` discount.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** Deploy sovereign multi-sig accumulation tranches (`MOD 18D`) or maximum `0.75%` Spot Swing allocation on the V-shaped reclaim of the `.786`.

---

## 4. Dynamic Regime Mutation Lookup Matrix (`M1` through `M5`)

| Mutation ID | Initial State | Telemetry Mutation Observed (`Condition A'`) | Mechanical Meaning (`Outcome B'`) | Mandatory Execution Override (`Rule C'`) |
| :--- | :--- | :--- | :--- | :--- |
| **M1: Dead-Cat Bounce** | `CSU-43A` (.618 Retrace) | Price bounces off the `.618`, but the bounce fails to exceed `1.0 ATR` before turning lower on negative USD Spot CVD. | Failed impulsive structure (A-B-C flat correction); sellers are still in control. | **Enforce 100% Cash Lock**; stop-loss triggered on breakdown. |
| **M2: Extension Blow-Off** | `CSU-43B` (ATR Thrust) | Price blasts through the `1.618` extension and approaches the `2.618` extension with extreme funding and peaking OI. | Terminal impulse (Wave 5 exhaustion); market is heavily over-leveraged. | **Execute Stage 2 Full Profit Exit.** Arm `MOD 41` Rule 1 countdown. |
| **M3: Choppy Consolidation** | Any | ZigZag records multiple direction changes `< 1.0 ATR`. No clear structural extremes are set. | Complex corrective wave; market is searching for liquidity. | **Hold Cash / Do Not Re-calculate Fibs.** Wait for a clean `>= 2.0 ATR` impulse to anchor a new sequence. |
| **M4: The 0.382 Secular Hold** | Minor Retracement | Price corrects but refuses to dip below the `.382` Fib. Spot CVD remains highly positive throughout the shallow dip. | Extreme bullish strength; sellers cannot force a mean reversion. | Enter **0.75% Risk Spot Long** on the breakout of the local high; trailing stop at the `.382`. |
| **M5: Offshore-Only Confluence** | `CSU-43A` (.618 Retrace) | Price hits the `.618` and POC, but limit-bid absorption is strictly on Binance USDT (offshore) with zero USD Spot CVD. | Weak structural foundation; high risk of support failure. | **Circuit Breaker 2 Tripped: Reject Signal.** Stand down and maintain 100% Cash Lock. |
