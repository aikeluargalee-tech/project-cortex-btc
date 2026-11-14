# PROJECT CORTEX-BTC — MODULE 12: GARMAN-KLASS (OHLC) VOLATILITY SQUEEZE & FAN EXPANSION
**Waterfall Tier:** Pillar 2 & Pillar 4 Bridge (Range-Based Volatility Estimator, Regime Birth & Stop-Distance Calibration) cross-verified with Pillar 1 (Macro Permissions).
**Empirical Benchmark Anchor:** November 2026 Volatility Regime Telemetry — Garman-Klass 24H/7D annualized realized volatility expanding abruptly from bottom-quartile compression (`< 28% annualized`) into top-decile shock expansion (`> 68% annualized`) as Bitcoin broke below **$73,000** toward **$68,000** amid **$1.41B** in forced liquidations.

---

## 1. Machine-Readable State & Routing Block (Python / Hermes / NotebookLM Index)

```yaml
module_id: "MOD_12"
entry_type: "CONDITIONAL_SIGNAL_UNIT"
waterfall_pillar: "PILLAR_2_4_VOLATILITY_RISK_CALIBRATION"
title: "Garman-Klass (OHLC) Volatility Squeeze & Fan Expansion (Stop-Distance & Regime Birth)"

# PILLAR 1 MASTER PERMISSION PRE-CHECK
pillar_1_permission_required: true
cash_lock_override: "If Pillar 1 Macro Regime == RISK_OFF_100_CASH, bottom-decile volatility squeezes are treated strictly as downward breakdown risks—zero Long entries."

# PRIMARY TELEMETRY TRIGGERS (GARMAN-KLASS ESTIMATOR)
base_regime_triggers:
  garman_klass_formula: "sigma_GK^2 = 0.5 * (ln(H/L))^2 - (2*ln(2) - 1) * (ln(C/O))^2"
  squeeze_compression_percentile: "Rolling 30D/90D Garman-Klass Volatility <= 15th percentile (Extreme Compression)"
  expansion_breakout_percentile: "Garman-Klass Volatility crosses from <= 15th percentile above 50th percentile with directional Spot CVD"
  climax_exhaustion_percentile: "Garman-Klass Volatility >= 92nd rolling percentile (Upper/Lower Fan Extreme)"

# ANTI-TRAP CIRCUIT BREAKERS
circuit_breakers:
  CB_01_PREMATURE_CLOSE: "NEVER anticipate the direction of a bottom-decile volatility squeeze before price breaks VAH/VAL with verified Domestic USD Spot CVD."
  CB_02_VENUE_CONTAMINATION: "Compute OHLC bars from a composite domestic USD spot index (Coinbase/Kraken/Bitstamp) to eliminate single-exchange perp scam-wicks."
  CB_03_FORCED_FLOW_STANDDOWN: "When Garman-Klass volatility spikes >= 92nd percentile on red candles, freeze new entries until volatility begins mean-reverting downward."
  CB_04_SIGNAL_HALF_LIFE: "Use GK volatility directly to scale stop distance (1.5x to 2.0x GK expected range), automatically shrinking BTC position size when volatility is high."

# RISK & SIZING CONSTANTS (PILLAR 4)
risk_parameters:
  max_portfolio_risk_pct: 0.75
  leverage_permitted: 1.0 # Strict Unleveraged Spot Only
  exit_protocol: "TWO_STAGE_STRUCTURAL"
```

---

## 2. Protective Circuit Breakers (Mandatory Pre-Execution Filters)

Why **Garman-Klass (GK)** beats standard close-to-close volatility or Bollinger Bands: GK incorporates **intraday High, Low, Open, and Close (`OHLC`)**, capturing hidden intrabar range expansion and wick rejection that close-to-close estimators miss. Before acting on Module 12, four circuit breakers apply:
* **Circuit Breaker 1 — No Pre-Squeeze Guessing (`CB-01`):** A bottom-decile GK volatility squeeze (`<= 15th percentile`) guarantees an upcoming volatility expansion, **not** its direction. Guessing direction inside a squeeze violates deterministic rules; wait for confirmed VAH/VAL breakout + Domestic USD Spot CVD.
* **Circuit Breaker 2 — Volatility-Adjusted Position Sizing (`CB-04`):** Because `Spot Position (BTC) = (0.0075 * Equity) / (Entry - Stop)`, wider GK volatility fans automatically widen your structural stop distance (`1.5x–2.0x GK expected bar range`), which **mathematically forces your BTC position size smaller** during volatile regimes—protecting you from noise stop-outs without ever increasing dollar risk above `0.75%`.
* **Circuit Breaker 3 — Scam-Wick Filtering (`CB-02`):** Use composite USD spot OHLC data so an isolated offshore perp liquidation wick does not falsely inflate your GK volatility fan.
* **Circuit Breaker 4 — Climax Exhaustion Ban (`CB-03`):** Never initiate a momentum breakout entry when GK volatility is already above the **92nd rolling percentile**; at that extreme, volatility is statistically primed to mean-revert rather than expand further.

---

## 3. Core Conditional Signal Units (`Condition A -> Outcome B -> Rule C`)

### CSU-12A: Bottom-Decile Volatility Squeeze -> Spot-Backed Trend Birth
* **Trigger Condition A (The Telemetry Scan):**
  1. **Compression Phase:** Rolling Garman-Klass volatility compresses into the **`<= 15th percentile`** for `>= 24 to 72 hours` while price coils inside a tight Volume Profile Value Area.
  2. **Expansion Ignition:** Price breaks decisively above the **Value Area High (VAH)** and upper **1-Sigma GK Volatility Fan**, pushing GK volatility upward out of compression (`> 35th percentile`).
  3. **Flow & Path Confirmation:** **Domestic Fiat (USD) Spot CVD** surges positive (`>= +1.5 Z-score`) and Rough Path `A_P,V` confirms volume-led upward curvature.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Market makers and options dealers who were short gamma inside the quiet range are forced to chase spot inventory as price breaks the volatility fan, fueling a multi-day trend leg.
  * **Probable Trajectory:** Sustained directional expansion (`+5% to +15%`) as realized volatility expands from bottom decile toward upper quartile.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Entry Trigger:** Execute **Unleveraged Spot Long** on the first 15m/1H pullback retest of the **reclaimed VAH / upper GK squeeze lip** (or immediately if `Mutation M2` head-fake already occurred).
  * **Position Sizing Formula (GK-Calibrated 0.75% Risk Ceiling):**
    `Stop Distance = max(VAH_to_POC_Distance, 1.75 * GK_1H_Expected_Range)`
    `Spot Position (BTC) = (0.0075 * Total Portfolio Equity) / Stop Distance`
  * **Two-Stage Profit Exit Protocol:**
    * **Stage 1 Exit (50% of Position):** Close 50% when price reaches the **2.5-Sigma Upper GK Volatility Fan** (`GK percentile >= 85th`); move stop to breakeven.
    * **Stage 2 Exit (Remaining 50%):** Trail behind the 4H VAL or lower 1-Sigma GK channel until volatility peaks and rolls over.

### CSU-12B: The Head-Fake Initial Expansion ("Stop-Hunt Squeeze Reversal")
* **Trigger Condition A (The Telemetry Scan):**
  1. From a **`<= 15th percentile` GK Volatility Squeeze**, price initially breaks **downward** below VAL, sweeping obvious retail stop-losses.
  2. **Failure of Follow-Through:** Within 1 to 3 hours, Open Interest drops (`short-term longs flushed`), **Domestic Fiat (USD) Spot CVD surges positive** (absorbing the sweep), and price violently snaps back through the POC and breaks **above the squeeze VAH**.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Classic liquidity-engineering maneuver: market makers expanded volatility downward just enough to clear leveraged long stops and trigger breakout shorts before reversing into the true institutional upward impulse.
  * **Probable Trajectory:** Explosive upside trend expansion fueled by both institutional spot accumulation and trapped breakout shorts.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Entry Trigger:** Execute **Unleveraged Spot Long** immediately upon the **15m/1H close back above the squeeze POC/VAH**, sized strictly to the **0.75% Risk Ceiling** with hard stop beneath the head-fake sweep wick low.

### CSU-12C: Top-Percentile Volatility Climax ("Mean-Reversion Exhaustion")
* **Trigger Condition A (The Telemetry Scan):**
  1. Garman-Klass volatility spikes into the **`>= 92nd rolling percentile`** (extreme vertical candle ranges and wide upper/lower wicks).
  2. **Upside Climax:** Price hits the **3-Sigma Upper GK Fan** while 8H perpetual funding spikes `> 90th percentile` and **Domestic USD Spot CVD flattens/diverges negatively**.
  3. **Downside Climax:** Price hits the **3-Sigma Lower GK Fan** on `> 85%` long liquidations (`MOD 03`), followed by immediate 15m limit-bid absorption.
* **Observed Outcome B (The Mechanical Trajectory):**
  Volatility has reached statistical exhaustion; market makers widen spreads and stop chasing directional momentum, causing price to snap back toward the session VWAP / POC.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action (Upside Climax):** **EXECUTE STAGE 2 FULL PROFIT EXIT (100% OF OPEN SPOT SWING).** Lock Cash.
  * **Action (Downside Climax):** **HOLD 100% CASH** during the spike; authorize a reduced-size (`0.375%–0.75%` risk) mean-reversion Spot Long *only* after GK volatility ticks downward for 2 consecutive 1H bars and 15m VAL is reclaimed with USD Spot CVD.

### CSU-12D: Grinding Low-Volatility Uptrend ("Quiet Institutional Drift")
* **Trigger Condition A (The Telemetry Scan):**
  1. Price trends steadily higher over 7–21 days while Garman-Klass volatility drifts downward into the **20th–35th percentile** (small, orderly green candles with minimal wicks).
  2. **Domestic Fiat (USD) Spot CVD** and US Spot ETF netflows climb steadily while perpetual funding stays neutral (`+0.005% to +0.010%`).
* **Observed Outcome B (The Mechanical Trajectory):**
  Pure institutional TWAP/VWAP spot accumulation without retail leverage mania—the healthiest possible wealth-compounding regime.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **HOLD CORE SPOT SWING POSITION.** Because GK volatility is low, tighten trailing stops closer (`1.5x GK range` below 4H VAL) to maximize capital efficiency while keeping risk locked at `<= 0.75%`.

---

## 4. Dynamic Regime Mutation Lookup Matrix (`M1` through `M8`)

| Mutation ID | Initial State | Telemetry Mutation Observed (`Condition A'`) | Mechanical Meaning (`Outcome B'`) | Mandatory Execution Override (`Rule C'`) |
| :--- | :--- | :--- | :--- | :--- |
| **M1: Squeeze Break Without Spot** | `CSU-12A` (False Break) | Price breaks above squeeze VAH and GK volatility expands, but **Domestic USD Spot CVD is flat/negative** (perp-only push). | Breakout lacks real spot backing; high probability of mutating into a `CSU-12B` downward head-fake. | **Block Entry (`CB-01`).** Wait for USD Spot CVD confirmation or VAH retest. |
| **M2: Downward Squeeze Breakdown** | `<= 15th pct` Squeeze | Price breaks **below squeeze VAL**, GK volatility surges above 50th percentile, and **USD Spot CVD + Perp CVD both plunge**. | Squeeze resolved downward into an institutional distribution / liquidation leg. | **Enforce Immediate 100% Cash Lock.** Exit any remaining spot exposure. |
| **M3: Volatility Fan Rejection** | `CSU-12A` (Active Trend) | Price pierces the **2.5-Sigma Upper GK Fan** and prints a long upper wick closing back inside the 1.5-Sigma band with falling USD Spot CVD. | Intraday volatility expansion hit institutional supply limits. | **Execute Stage 1 (50%) Profit Exit Immediately**; trail stop on remainder. |
| **M4: Post-Climax Volatility Crush** | `CSU-12C` (Climax Spike) | Following a `>= 92nd pct` spike, GK volatility drops by `> 40%` over 6–12 hours as price forms an inside-bar coil at support. | Panic/euphoria has subsided; market is transitioning into a fresh base. | Prepare new `CSU-12A` squeeze breakout triggers at the new range boundaries. |
| **M5: Stop-Distance Recalibration** | Active Swing Trade | GK volatility doubles mid-trade (`e.g., from 30% to 60% APR`) while price trends in your favor. | Noise amplitude has doubled; a tight stop will get wicked out prematurely. | **Bank Stage 1 (50%) Profit** to lock gains, then widen trailing stop on remaining 50% to `2.0x` new GK range. |
| **M6: Macro Shock Volatility Regime** | Any State | GK volatility spikes `>= 95th percentile` triggered by US 10Y yield spike (`> 5.10%`) or CPI/FOMC shock (Pillar 1 breach). | Exogenous macro repricing event; historical technical bands temporarily lose containment. | **Pillar 1 Override: Lock 100% Cash** until macro volatility settles below 60th percentile. |
| **M7: Multi-Day Inside-Day Coil** | `<= 15th pct` Squeeze | Three consecutive daily candles print narrower ranges (`GK < 10th percentile`) right below a major HTF VAH / 200D MA. | Maximum coiling energy at a secular inflection point. | Set automated alerts on VAH breakout + USD Spot CVD; prepare full `0.75% Risk` deployment. |
| **M8: Weekend Low-GK Drift** | Sat–Sun Session | GK volatility drops to `< 5th percentile` over weekend with zero institutional flow. | Artificial weekend illiquidity—not a true structural squeeze. | **Ignore Weekend GK Readings** until Sunday 22:00 UTC / Monday Asia-NY handoff (`MOD 17`). |
