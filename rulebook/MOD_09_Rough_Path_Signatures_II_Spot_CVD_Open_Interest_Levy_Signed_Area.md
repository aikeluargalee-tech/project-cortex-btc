# PROJECT CORTEX-BTC — MODULE 09: ROUGH PATH SIGNATURES II — SPOT CVD–OPEN INTEREST LÉVY SIGNED AREA (A_CVD,OI)
**Waterfall Tier:** Pillar 2 & Pillar 3 Bridge (Joint Path Geometry of Unleveraged Spot Flow vs. Leveraged Derivatives Creation) cross-verified with Pillar 4 (Portfolio Engineering).
**Empirical Benchmark Anchor:** November 2026 Joint Flow-Leverage Telemetry — During the November 6–12 window, Perpetual Open Interest surged by **+22,000 BTC** (to **367.4K BTC**) *before* brief 3-day spot buying (**+$269.4M**) appeared, followed by domestic spot outflows (**-$83.3M to -$141.5M** 24H) while offshore perps kept adding leverage—tracing a negative `A_CVD,OI` curvature (`Leverage leading Spot`) that preceded the **$1.41B** long liquidation flush below **$69,000**.

---

## 1. Machine-Readable State & Routing Block (Python / Hermes / NotebookLM Index)

```yaml
module_id: "MOD_09"
entry_type: "CONDITIONAL_SIGNAL_UNIT"
waterfall_pillar: "PILLAR_2_3_JOINT_PATH_GEOMETRY"
title: "Rough Path Signatures II: Spot CVD-Open Interest Lévy Signed Area (A_CVD,OI)"

# PILLAR 1 MASTER PERMISSION PRE-CHECK
pillar_1_permission_required: true
cash_lock_override: "If Pillar 1 Macro Regime == RISK_OFF_100_CASH, block all Long executions even when A_CVD,OI > 0."

# PRIMARY TELEMETRY TRIGGERS (JOINT 2D PATH SIGNATURE)
base_regime_triggers:
  path_coordinates: "X_t = Normalized Domestic USD Spot CVD, Y_t = Normalized Total BTC Open Interest"
  levy_signed_area_formula: "A_CVD,OI = 0.5 * (S^(CVD,OI) - S^(OI,CVD))"
  healthy_spot_lead_threshold: "Rolling Z-score of A_CVD,OI >= +1.5 (Domestic Spot CVD leads OI expansion)"
  fragile_leverage_lead_threshold: "Rolling Z-score of A_CVD,OI <= -1.5 (Leveraged OI expansion leads Spot CVD)"

# ANTI-TRAP CIRCUIT BREAKERS
circuit_breakers:
  CB_01_PREMATURE_CLOSE: "NEVER buy a breakout when A_CVD,OI <= -1.5 Z-score; leverage-led rallies unwind violently on minor spot pauses."
  CB_02_VENUE_CONTAMINATION: "Construct X_t strictly from Domestic Fiat (USD) Spot CVD (Coinbase/Kraken/ETF proxy) so offshore USDT churn cannot fake Spot leadership."
  CB_03_FORCED_FLOW_STANDDOWN: "Stand down 100% when both X_t (Spot CVD) and Y_t (OI) plunge simultaneously (aligned liquidation and spot capitulation)."
  CB_04_SIGNAL_HALF_LIFE: "Use 4H rolling windows for swing trend health and 1H windows for intraday regime flips."

# RISK & SIZING CONSTANTS (PILLAR 4)
risk_parameters:
  max_portfolio_risk_pct: 0.75
  leverage_permitted: 1.0 # Strict Unleveraged Spot Only
  exit_protocol: "TWO_STAGE_STRUCTURAL"
```

---

## 2. Protective Circuit Breakers (Mandatory Pre-Execution Filters)

Before any Scenario in Module 09 can authorize a spot order, all four circuit breakers must pass:
* **Circuit Breaker 1 — Lead-Lag Causal Order (`CB-01`):** Standard correlation treats `(Spot CVD up, OI up)` as one single state. Rough Path Signed Area `A_CVD,OI` measures **which moved first**: did unleveraged spot buyers accumulate *first* and pull futures OI up behind them (`A_CVD,OI > 0`), or did leveraged gamblers pile into futures *first* hoping spot would rescue them (`A_CVD,OI < 0`)?
* **Circuit Breaker 2 — Pure USD Spot Coordinate (`CB-02`):** `X_t` must be built from verified domestic USD spot flows. If offshore USDT spot rises while USD spot falls, `X_t` must reflect the domestic outflow.
* **Circuit Breaker 3 — Dual-Collapse Freeze (`CB-03`):** When both Spot CVD and Open Interest collapse together (`S^(CVD) < 0` and `S^(OI) < 0`), forced liquidations and spot redemptions are compounding. Lock 100% Cash.
* **Circuit Breaker 4 — Pillar 1 Macro Permission Gate:** Verify secular macro permissions before deploying risk on positive `A_CVD,OI` setups.

---

## 3. Core Conditional Signal Units (`Condition A -> Outcome B -> Rule C`)

### CSU-09A: Spot-Led Leverage Expansion ("Self-Sustaining Bull Curvature")
* **Trigger Condition A (The Telemetry Scan):**
  1. Both Domestic USD Spot CVD (`S^(CVD) > 0`) and Open Interest (`S^(OI) > 0`) are expanding over the 24H–72H window.
  2. **Joint Lévy Signed Area `A_CVD,OI >= +1.5 Z-score` (`>= 85th rolling percentile`)**, confirming chronologically that **unleveraged domestic spot accumulation initiated the move** and derivatives Open Interest expanded afterward as trend followers joined.
  3. Price holds cleanly above the 1H/4H Volume Profile POC/VAH.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Institutional spot buyers own the underlying coins outright and set the structural floor; derivatives leverage is riding *behind* real capital inflows rather than front-running thin liquidity.
  * **Probable Trajectory:** Durable multi-day trend expansion where shallow leverage shakeouts are rapidly bought up by the underlying spot bid.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Entry Trigger:** Execute **Unleveraged Spot Long** on a 15m/1H pullback to the Volume Profile **VAH or Developing POC** while `A_CVD,OI` remains positive (`>= +0.75 Z-score`).
  * **Position Sizing Formula (0.75% Risk Ceiling):**
    `Spot Position (BTC) = (0.0075 * Total Portfolio Equity) / (Entry Price - Invalidation Stop Price)`
  * **Hard Structural Invalidation Stop:** Place hard stop beneath the prior 4H swing low / VAL where domestic spot accumulation began.
  * **Two-Stage Profit Exit Protocol:**
    * **Stage 1 Exit (50% of Position):** Close 50% if `A_CVD,OI` crosses below `0.0` into negative territory (meaning leverage has overtaken spot leadership); move stop to breakeven.
    * **Stage 2 Exit (Remaining 50%):** Trail behind 4H VAL or exit completely if `A_CVD,OI` drops below `-1.5 Z-score`.

### CSU-09B: Leverage-Led Speculative Overextension ("Fragile Paper Tower")
* **Trigger Condition A (The Telemetry Scan):**
  1. Price is rising or holding near resistance while Open Interest surges (`S^(OI) >> 0`).
  2. **Joint Lévy Signed Area `A_CVD,OI <= -1.5 Z-score` (`<= 15th rolling percentile`)**, proving mathematically that **leveraged futures contracts expanded first** while Domestic USD Spot CVD lagged, stayed flat, or turned negative.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** The rally is built on borrowed margin rather than sovereign spot demand (precisely matching the November 2026 setup where offshore OI jumped +22K BTC while spot demand failed to sustain follow-through).
  * **Probable Trajectory:** High vulnerability to an abrupt **long-liquidation air pocket** the moment momentum stalls.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **BLOCK ALL NEW LONG ENTRIES. LOCK 100% CASH.** If holding an existing Spot Long from lower prices, execute **Stage 2 Full Profit Exit** immediately.

### CSU-09C: Spot Buying Into Open Interest Unwind ("Cleanest Structural Reversal")
* **Trigger Condition A (The Telemetry Scan):**
  1. Open Interest contracts steadily (`S^(OI) < 0`, deleveraging flush or voluntary unwind) while **Domestic USD Spot CVD rises sharply (`S^(CVD) > 0`)**.
  2. **Joint Lévy Signed Area `A_CVD,OI >= +1.5 Z-score`**, showing spot accumulation stepping in aggressively as leveraged weak hands are flushed out of the system.
  3. Price sweeps a higher-timeframe liquidity low and reclaims the 15m/1H Volume Profile VAL.
* **Observed Outcome B (The Mechanical Trajectory):**
  Coins are transferring directly from liquidated margin gamblers to unleveraged institutional spot wallets. Overhead liquidation risk is purged while a genuine spot floor forms.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Entry Trigger:** Execute **Unleveraged Spot Long** upon 15m/1H **VAL or Developing POC reclaim**, sized strictly to the **0.75% Risk Ceiling** with hard stop below the flush wick low.

### CSU-09D: Spot Selling Into Open Interest Build-Up ("Institutional Hedging / Distribution Markdown")
* **Trigger Condition A (The Telemetry Scan):**
  1. **Domestic USD Spot CVD plunges (`S^(CVD) << 0`)** while **Open Interest expands (`S^(OI) > 0`)**, generating a steep negative signed area **`A_CVD,OI <= -2.0 Z-score`** on a downward price trajectory.
* **Observed Outcome B (The Mechanical Trajectory):**
  Institutional spot holders and ETFs are actively selling spot while aggressive short sellers pile into futures (or passive retail longs catch falling knives on leverage).
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **STRICT 100% CASH LOCK.** Zero dip-buying permitted until Domestic USD Spot CVD stops bleeding and `CSU-09C` curvature emerges.

---

## 4. Dynamic Regime Mutation Lookup Matrix (`M1` through `M8`)

| Mutation ID | Initial State | Telemetry Mutation Observed (`Condition A'`) | Mechanical Meaning (`Outcome B'`) | Mandatory Execution Override (`Rule C'`) |
| :--- | :--- | :--- | :--- | :--- |
| **M1: Spot-to-Leverage Hand-Off** | `CSU-09A` (Spot-Led) | Price pushes higher, but **`A_CVD,OI` rotates clockwise from `+1.8 Z` down to `-1.2 Z`** as OI accelerates and USD Spot CVD plateaus. | Leadership just passed from institutional spot buyers to late leveraged chasers. | **Execute Stage 1 (50%) or Stage 2 (100%) Profit Exit** into strength. |
| **M2: Leverage Flush Into Spot Bid** | `CSU-09B` (Paper Tower) | Price drops `-4% to -8%`, OI plunges (`S^(OI) << 0`), and **`A_CVD,OI` snaps sharply upward above `+1.5 Z`** as USD Spot CVD surges at VAL. | Paper leverage was wiped out and real spot buyers absorbed the flush. | Transition directly to **`CSU-09C`**; authorize `0.75% Risk` Spot Long on 15m VAL reclaim. |
| **M3: Spot Bid Abandonment** | `CSU-09C` (Spot Into Unwind) | OI stabilizes, but **Domestic USD Spot CVD rolls over negative** (`A_CVD,OI` drops below `-1.0 Z`) before price reclaims 1H VAH. | Spot absorbers stepped back; bounce lacked follow-through demand. | **Abort Spot Long Watch / Exit at Breakeven.** Lock 100% Cash. |
| **M4: Counter-Clockwise Accumulation Loop** | Range Chop | `(Spot CVD, OI)` traces repeated counter-clockwise loops (`A_CVD,OI > +1.0 Z`) while price holds flat above HTF VAL. | Quiet institutional spot accumulation while derivatives traders churn in place. | Prepare `0.75% Risk` Spot Long entry on range VAH breakout. |
| **M5: Clockwise Distribution Loop** | Range Top | `(Spot CVD, OI)` traces clockwise loops (`A_CVD,OI < -1.0 Z`)—OI rises on every small bounce while USD Spot CVD makes lower highs. | Institutional spot distribution into retail leveraged bounces at range highs. | **Enforce 100% Cash Lock.** Exit any open tactical longs immediately. |
| **M6: Double-Negative Capitulation** | `CSU-09D` (Markdown) | Both `S^(CVD)` and `S^(OI)` drop at `> 2.5 Z-score` simultaneously as price breaks multi-week support. | Simultaneous spot ETF redemption and futures liquidation cascade. | **Circuit Breaker 3 Freeze:** Hold 100% Cash until both slopes flatten for `>= 4 hours`. |
| **M7: Offshore-Domestic Path Divergence** | `CSU-09A` (False Signal) | Offshore USDT `A_CVD,OI` reads `+1.6 Z`, while **Coinbase/Kraken USD `A_CVD,OI` reads `-1.5 Z`**. | Offshore tether flow is masking domestic institutional distribution. | **Circuit Breaker 2 Tripped: Reject Signal.** Lock 100% Cash. |
| **M8: Full 3D Signature Alignment** | `CSU-09A` + `MOD 08` | Both **`A_P,V >= +1.5 Z`** (MOD 08) and **`A_CVD,OI >= +1.5 Z`** (MOD 09) fire simultaneously on 1H and 4H. | Volume leads price AND domestic spot leads leverage—maximum structural purity. | **Highest-Conviction Swing Trigger:** Deploy full `0.75% Risk` Spot allocation. |
