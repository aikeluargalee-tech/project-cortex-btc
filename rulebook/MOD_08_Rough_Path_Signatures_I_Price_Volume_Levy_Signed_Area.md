# PROJECT CORTEX-BTC — MODULE 08: ROUGH PATH SIGNATURES I — PRICE-VOLUME LÉVY SIGNED AREA (A_P,V)
**Waterfall Tier:** Pillar 2 (Microstructure, Order Flow & Path Geometry) cross-verified with Pillar 1 (Macro Permissions) and Pillar 4 (Portfolio Engineering).
**Empirical Benchmark Anchor:** November 2026 Order-Book & Volatility Telemetry — Order book depth across major exchanges standing at **$72M** (33% below normal) during the November 9–13, 2026 flush from **$75,771** down below **$69,000**, where thin-book price drops exhibited steep negative price-first curvature (`A_P,V < -1.8 Z-score`) before volume climax arrived at **$68,000**.

---

## 1. Machine-Readable State & Routing Block (Python / Hermes / NotebookLM Index)

```yaml
module_id: "MOD_08"
entry_type: "CONDITIONAL_SIGNAL_UNIT"
waterfall_pillar: "PILLAR_2_MICROSTRUCTURE_PATH_GEOMETRY"
title: "Rough Path Signatures I: Price-Volume Lévy Signed Area (A_P,V) Lead-Lag Curvature"

# PILLAR 1 MASTER PERMISSION PRE-CHECK
pillar_1_permission_required: true
cash_lock_override: "If Pillar 1 Macro Regime == RISK_OFF_100_CASH, block all bullish A_P,V swing entries and enforce cash preservation."

# PRIMARY TELEMETRY TRIGGERS (ORDER N <= 2 TRUNCATED SIGNATURE)
base_regime_triggers:
  signature_order: 2
  level_1_increments: "S^(1) = Delta_log_Price, S^(2) = Delta_Normalized_Volume"
  levy_signed_area_formula: "A_P,V = 0.5 * (S^(1,2) - S^(2,1))"
  curvature_zscore_threshold: "Rolling 30-period Z-score of A_P,V >= +1.5 (Volume-Led Markup) or <= -1.5 (Price-Led Thin Move)"
  path_compression_percentile: "Euclidean norm of Level-2 signature <= 15th rolling percentile (Path Flattening)"

# ANTI-TRAP CIRCUIT BREAKERS
circuit_breakers:
  CB_01_PREMATURE_CLOSE: "NEVER enter on a raw price breakout if A_P,V <= -1.0 Z-score (price moving upward ahead of volume participation)."
  CB_02_VENUE_CONTAMINATION: "Compute S^(2) volume increments using spot volume weighted toward Domestic Fiat (USD) venues to prevent offshore wash-volume distortion."
  CB_03_FORCED_FLOW_STANDDOWN: "Stand down 100% during liquidation cascades where A_P,V spikes sharply negative on red candles until signed area curvature stabilizes."
  CB_04_SIGNAL_HALF_LIFE: "1H A_P,V signatures govern 12H-72H tactical swings; require 4H/1D signature alignment (MOD 10) for multi-week holds."

# RISK & SIZING CONSTANTS (PILLAR 4)
risk_parameters:
  max_portfolio_risk_pct: 0.75
  leverage_permitted: 1.0 # Strict Unleveraged Spot Only
  exit_protocol: "TWO_STAGE_STRUCTURAL"
```

---

## 2. Protective Circuit Breakers (Mandatory Pre-Execution Filters)

Before any Scenario in Module 08 can authorize a spot order, all four circuit breakers must pass:
* **Circuit Breaker 1 — Thin-Book Illusion Filter (`CB-01`):** Standard candle charts treat a +3% rally on $72M thin book depth identically to a +3% rally backed by institutional volume. Level-2 Lévy Signed Area (`A_P,V`) mathematically exposes the chronological order: if price rises *before* volume steps in (`A_P,V < -1.0 Z-score`), the rally is a fragile liquidity vacuum trap.
* **Circuit Breaker 2 — Wash-Volume Normalization (`CB-02`):** Normalize volume increments `S^(2)` using rolling median absolute deviation (MAD) across verified USD/institutional spot exchanges so offshore zero-fee maker-rebate churn cannot spoof positive signed area.
* **Circuit Breaker 3 — Liquidation Cascade Freeze (`CB-03`):** During forced margin flushes, price gaps downward before liquidation volume prints (`extreme negative A_P,V`). Freeze all spot entries until signed area curvature inflects back toward zero.
* **Circuit Breaker 4 — Pillar 1 Macro Gate:** Even strong volume-led upward curvature is restricted to tactical profit-taking if Pillar 1 is locked in `RISK_OFF_100_CASH`.

---

## 3. Core Conditional Signal Units (`Condition A -> Outcome B -> Rule C`)

### CSU-08A: Volume-Led Markup Curvature ("Institutional Impulse Birth")
* **Trigger Condition A (The Telemetry Scan):**
  1. First-order price increment `S^(1) > 0` (price breaking above 1H/4H Volume Profile POC or VAH).
  2. **Level-2 Lévy Signed Area `A_P,V >= +1.5 Z-score` (`>= 85th rolling percentile`)**, proving mathematically that **volume expansion preceded and drove price displacement** chronologically within the path window.
  3. **Domestic Fiat (USD) Spot CVD** confirms positive net taker buying and Pillar 1 grants risk permission.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Real capital committed size at the bid *before* price cleared overhead liquidity, absorbing resting supply rather than chasing thin air.
  * **Probable Trajectory:** High-persistence directional trend leg with strong structural support at the impulse origin, as institutional buyers defend their volume-weighted entry zone.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Entry Trigger:** Execute **Unleveraged Spot Long** upon a verified 15m/1H pullback retest of the reclaimed **VAH or impulse POC** while `A_P,V` remains positive (`> +0.5 Z-score`).
  * **Position Sizing Formula (0.75% Risk Ceiling):**
    `Spot Position (BTC) = (0.0075 * Total Portfolio Equity) / (Entry Price - Invalidation Stop Price)`
  * **Hard Structural Invalidation Stop:** Place hard stop immediately beneath the volume-led impulse origin / 1H VAL.
  * **Two-Stage Profit Exit Protocol:**
    * **Stage 1 Exit (50% of Position):** Close 50% when `A_P,V` begins rolling over from peak (`> +2.5 Z-score` decelerating below `+1.0 Z-score`) at upper Garman-Klass volatility bands; move stop to breakeven.
    * **Stage 2 Exit (Remaining 50%):** Trail behind 4H Volume Profile VAL or exit immediately if `A_P,V` flips negative (`< -1.0 Z-score`) while price makes marginal new highs.

### CSU-08B: Price-Led Thin Vacuum Rally ("Bull Trap Curvature")
* **Trigger Condition A (The Telemetry Scan):**
  1. First-order price increment `S^(1) > 0` (price pushes into resistance or sweeps a prior swing high).
  2. **Level-2 Lévy Signed Area `A_P,V <= -1.5 Z-score` (`<= 15th rolling percentile`)**, proving that **price jumped first on thin order-book liquidity and volume only appeared at the top** (late retail chasing / passive institutional ask absorption).
  3. Domestic USD Spot CVD is flat or negative.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Market makers pulled offers in a thin book (such as $72M depth regimes), allowing price to float up effortlessly before institutional sellers unloaded into late momentum buyers at the peak.
  * **Probable Trajectory:** Rapid mean-reversion failure back through the entire thin-volume gap ("look-above-and-fail").
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **BLOCK ALL LONG ENTRIES. LOCK 100% CASH.** If holding an existing Spot Swing Long from lower levels, immediately execute **Stage 2 Profit Exit** into the thin-book spike.

### CSU-08C: Volume-Backed Accumulation Loop ("Counter-Clockwise Bottom Curvature")
* **Trigger Condition A (The Telemetry Scan):**
  1. Net price change over the window is near zero (`S^(1) ~ 0`), oscillating inside a tight Volume Profile Value Area at higher-timeframe support.
  2. **Level-2 Lévy Signed Area `A_P,V` cycles strongly positive (`>= +1.25 Z-score`)** across repeated intraday sweeps of VAL—showing heavy volume surges on dips and quiet, low-volume rebounds.
  3. Domestic USD Spot CVD prints higher lows while price prints equal or slightly lower lows.
* **Observed Outcome B (The Mechanical Trajectory):**
  The joint `(Price, Volume)` path is tracing an institutional absorption loop: large passive buyers are soaking up every wave of market selling at the bottom of the range without letting price break down.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Entry Trigger:** Authorize **Unleveraged Spot Long** upon a verified 15m/1H **VAH or Developing POC reclaim** exiting the accumulation loop, sized strictly to the **0.75% Risk Ceiling** with stop beneath the loop's lowest absorption wick.

### CSU-08D: Climax Distribution & Vacuum Breakdown ("Markdown Acceleration")
* **Trigger Condition A (The Telemetry Scan):**
  1. First-order price increment `S^(1) < 0` (breaking below 1H/4H VAL) while **`A_P,V <= -2.0 Z-score`** on red candles (price dropping rapidly through air pockets *before* panicked liquidation volume hits at the lows).
  2. Domestic USD Spot CVD and Perpetual CVD are both negative (`Aligned Outflow`).
* **Observed Outcome B (The Mechanical Trajectory):**
  Bid liquidity has vanished beneath price; sellers are hitting air pockets, triggering delayed stop-losses and forced margin liquidations lower down the book.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **ENFORCE 100% CASH LOCK.** Stand down completely until `A_P,V` stops accelerating negatively and `CSU-08C` accumulation curvature reappears at lower HTF support.

---

## 4. Dynamic Regime Mutation Lookup Matrix (`M1` through `M8`)

| Mutation ID | Initial State | Telemetry Mutation Observed (`Condition A'`) | Mechanical Meaning (`Outcome B'`) | Mandatory Execution Override (`Rule C'`) |
| :--- | :--- | :--- | :--- | :--- |
| **M1: Curvature Flip at Resistance** | `CSU-08A` (Markup) | Price makes a marginal higher high, but **`A_P,V` flips from `+1.8 Z` down to `-1.2 Z`** on the final push. | Institutional volume leadership ended; the final leg up is thin retail FOMO chasing. | **Execute Stage 1 (50%) or Stage 2 (100%) Profit Exit immediately.** |
| **M2: Path Compression Coil** | Any Range State | Level-2 signature norm drops below the **10th percentile** (`A_P,V -> 0.0`) alongside Garman-Klass volatility squeeze. | Market has reached equilibrium; path energy is coiling for an imminent regime birth. | Prepare breakout triggers; enter **only** in the direction where `A_P,V` breaks `>= +1.5 Z` with USD Spot CVD. |
| **M3: Absorption-to-Breakout Ignition** | `CSU-08C` (Accumulation Loop) | Price breaks above range VAH and **`A_P,V` surges above `+2.0 Z-score`** with expanding USD Spot CVD. | Passive accumulators have finished filling orders and switched to aggressive market-lifting. | **Enter/Hold Spot Long** under `0.75% Risk Formula`; place stop beneath reclaimed VAH. |
| **M4: Failed Loop Breakdown** | `CSU-08C` (Accumulation Loop) | Price breaks below range VAL and **`A_P,V` plunges below `-2.0 Z-score`** as USD Spot CVD breaks down. | Passive bid wall was pulled or overwhelmed; accumulation loop mutated into markdown. | **Hard Stop Triggered / Enforce 100% Cash Lock.** |
| **M5: Thin-Spike Mean Reversion** | `CSU-08B` (Thin Vacuum) | After spiking on `A_P,V <= -1.5 Z`, price falls back below 1H POC and **`A_P,V` stays negative** on the drop. | Confirms complete absence of structural spot support beneath the thin-book pump. | **Maintain 100% Cash Lock**; watch lower HTF VAL for potential `CSU-08C` reset. |
| **M6: Capitulation Volume Inflection** | `CSU-08D` (Markdown) | After a `-2.5 Z` vacuum drop, a massive volume spike hits at HTF support while price stops falling, flipping **`A_P,V` sharply upward toward `0.0`**. | Panic sellers just dumped into a major institutional limit bid wall at the lows. | Lift active crash freeze; monitor 15m footprint for `CSU-08C` / `MOD 03` V-bottom reclaim. |
| **M7: Offshore Volume Spoof** | `CSU-08A` (False Signal) | Aggregate `A_P,V` reads `+1.8 Z` due to offshore USDT volume spike, but **USD-only `A_P,V` is negative (`< -0.5 Z`)**. | Offshore wash volume is masking weak domestic spot participation. | **Circuit Breaker 2 Tripped: Abort Long Entry.** Lock 100% Cash. |
| **M8: Multi-Timeframe Signature Resonance** | `CSU-08A` (1H Markup) | Both **1H `A_P,V` (`>= +1.5 Z`)** and **4H `A_P,V` (`>= +1.5 Z`)** align positively above 4H VAH. | Fractal institutional volume leadership across tactical and structural horizons. | **Authorize Full `0.75% Risk` Spot Swing Allocation** with extended Stage 2 trailing target. |
