# PROJECT CORTEX-BTC — MODULE 54: MULTI-TIMEFRAME ALGORITHMIC MARKET STRUCTURE, KLINE LOOKBACK CONTRACT & UI EXPLAINABILITY SCHEMA

**Waterfall Tier:** Pillar 2 (Microstructure & Path Geometry) integrated directly with Tier D (Control-Plane Trust & Output Rendering).
**Empirical Benchmark Anchor:** Fills the deterministic gap between visual classical shapes (MOD 42) and raw exchange data (MOD 36). Establishes absolute mathematical floors for candlestick lookbacks to guarantee indicator stabilization (ATR, VWAP, S/R), enforces strict 3-venue quorum on all fractal pivots, and formats the output string for the *BTC Magnet Monitor* UI to prevent subjective chart interpretation.

---

#### 1. Machine-Readable State & Routing Block (Python / Hermes / NotebookLM Index)

```yaml
module_id: "MOD_54"
entry_type: "CONTROL_PLANE_DATA_CONTRACT_AND_STRUCTURAL_CLASSIFIER"
waterfall_pillar: "PILLAR_2_AND_TIER_D_BRIDGE"
title: "Multi-Timeframe Algorithmic Market Structure & Kline Lookback Contract"

# KLINE FETCH & WARM-UP CONTRACT (FAIL-CLOSED)
kline_fetch_parameters:
  1D_daily_lookback_floor: 500 # Supports 200D MA (MOD 17) & 90D Structural Fibs (MOD 43)
  4H_lookback_floor: 600 # 100 days total: Covers 90D Structural limit + 60-bar ATR(14) warm-up
  1H_lookback_floor: 500 # ~20.8 days: Supports tactical VAH/VAL and multi-day POC shifts
  enforcement_action: "If API returns < floor, trigger MOD 36 DATA UNAVAILABLE (UNKNOWN) and lock 100% Cash."

# ALGORITHMIC FRACTAL MARKET STRUCTURE (HH/HL/LH/LL)
fractal_pivot_parameters:
  left_bars: 5
  right_bars: 5
  bos_authentication_gate: "Domestic USD Spot CVD (MOD 07) MUST align with the directional break."
  bar_close_confirmation_requirement: "4+ consecutive closes on 1H OR 2+ consecutive closes on 4H (per MOD 00C)."

# UI EXPLAINABILITY & HERMES TELEGRAM SCHEMA
ui_explainability_schema:
  required_json_keys: ["timeframe", "current_state", "latest_confirmed_pivot", "bos_status", "classification_reason"]
  classification_reason_template: "{timeframe} {state}: Confirmed {pivot_type} at ${price} followed by {close_count} closes {direction} {previous_pivot} with {cvd_state} USD Spot CVD."
```

---

#### 2. Protective Circuit Breakers (Mandatory Pre-Execution Filters)

*   **Circuit Breaker 1 — The Single-Venue Ban (CB-01):** Fractal pivots (Swing High/Low) and Break of Structure (BOS) levels are highly susceptible to offshore scam-wicks. Pivot arrays must be computed using the **3-venue USD/USDT spot quorum** (MOD 36). If cross-venue dispersion exceeds `35 bps`, freeze BOS logic.
*   **Circuit Breaker 2 — Unauthenticated BOS Ban (CB-02):** A raw pivot break is merely a candidate sweep. It cannot be classified as a valid structural BOS unless authenticated by **both** bar-count close discipline (4+ 1H closes or 2+ 4H closes) **and** aligned Domestic USD Spot CVD. Unauthenticated breaks default to MOD 11 / MOD 42 Liquidity Sweeps.
*   **Circuit Breaker 3 — Indicator Initialization Drift Ban (CB-03):** Never compute `ATR(14)`, `VWAP`, or Volume Profile `POC` on truncated datasets. The engine must ingest the full `500/600/500` kline block into memory to stabilize recursive moving averages before emitting the live metric to the waterfall.

---

#### 3. Core Conditional Signal Units (Condition A -> Outcome B -> Rule C)

##### CSU-54A: Authenticated Bullish Break of Structure (BOS)
*   **Trigger Condition A (The Telemetry Scan):**
    1. Python detects a local `leftBars=5, rightBars=5` Swing High pivot.
    2. Price breaches the pivot and confirms with **2+ consecutive 4H closes** (or 4+ 1H closes).
    3. **Authentication:** Domestic USD Spot CVD surges positively alongside the break, and the 600-kline 4H array confirms no missing data.
*   **Observed Outcome B (The Mechanical Trajectory):**
    *   **Microstructure Lens:** Spot-driven absorption of overhead supply. The break is mathematically clean across venues and backed by actual fiat inflows.
*   **Execution Rule C (The Non-Negotiable Action):**
    *   **Action:** Update structural state to `BULLISH`. Format `classification_reason` for Hermes UI. Pass execution clearance to MOD 18 (authorizing up to **0.75% Spot Risk** on the subsequent VAH/VWAP pullback).

##### CSU-54B: Authenticated Bearish Break of Structure (BOS)
*   **Trigger Condition A (The Telemetry Scan):**
    1. Price breaches a confirmed Swing Low (HL) and prints **2+ consecutive 4H closes** below it.
    2. **Authentication:** Quad 4 alignment (MOD 05) or negative Domestic USD Spot CVD confirms the markdown is real spot distribution, not just leveraged long flushing.
*   **Observed Outcome B (The Mechanical Trajectory):**
    *   **Microstructure Lens:** Institutional fiat off-ramping. The support floor has been permanently broken on the primary timeframe.
*   **Execution Rule C (The Non-Negotiable Action):**
    *   **Action:** Update structural state to `BEARISH`. Format `classification_reason` for Hermes UI. **Enforce 100% Cash Lock** (MOD 33). Evaluate shorts only if building a separate dual-inventory module, otherwise zero exposure.

##### CSU-54C: Truncated / Stale Kline Fetch (Fail-Closed)
*   **Trigger Condition A (The Telemetry Scan):**
    1. The `btc_data_fetcher.py` queries the Binance/Coinbase API, but the payload returns `490` klines on the 1D, or `200` klines on the 4H due to a pagination error or API rate-limit.
*   **Observed Outcome B (The Mechanical Trajectory):**
    *   **Control-Plane Lens:** Data ingestion is mathematically compromised. Any subsequent ATR, VWAP, or Swing pivot calculation will carry initialization drift, risking false triggers.
*   **Execution Rule C (The Non-Negotiable Action):**
    *   **Action:** Discard the array. Emit **MOD 36 UNKNOWN (DATA UNAVAILABLE)**. Lock portfolio to 100% Cash until the next top-of-hour cron sequence successfully validates the `500/600/500` contract.

---

#### 4. Dynamic Regime Mutation Lookup Matrix (M1 through M3)

| Mutation ID | Initial State | Telemetry Mutation Observed (Condition A') | Mechanical Meaning (Outcome B') | Mandatory Execution Override (Rule C') |
| :--- | :--- | :--- | :--- | :--- |
| **M1: Unconfirmed Liquidity Sweep** | CSU-54A / 54B Attempt | Price breaches the `5/5` pivot but immediately snaps back, failing to print the required 1H/4H closes, OR Spot CVD diverges against the break. | Trap engineered to trigger retail breakout algorithms. The prior structure holds. | **Revert to Prior Structure.** Treat strictly as a MOD 11A VAL Spring or MOD 11C VAH Look-Above-and-Fail. |
| **M2: Timeframe Structural Conflict** | Routine Scan | `1H` prints a confirmed Bullish BOS, but the `4H` and `1D` remain structurally Bearish. | Tactical counter-trend bounce within a macro downtrend. | **Apply MOD 33 / MOD 18 Gate:** Cap all spot entries at `0.375%` risk until the `4H` timeframe structurally aligns with the `1H`. |
| **M3: Anchor Decoupling** | Active Uptrend | Price prints a new `HH`, but VWAP/POC migrates downwards due to heavy off-book OTC settlement. | Surface price is rising, but core institutional value is actively lowering. | **Halt Breakout Entries.** Hold existing spot swings but tighten trailing stops to the nearest algorithmic pivot. |
