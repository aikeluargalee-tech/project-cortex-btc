# PROJECT CORTEX-BTC — MODULE 55: DUAL-STAGE DISRUPTION TELEMETRY & RECOVERY RADAR ENGINE

**Waterfall Tier:** Pillar 2 & Pillar 3 Bridge (Microstructure & Derivatives Fragility).
**Empirical Benchmark Anchor:** Bridges the stateless cloud-based "Tell Tale Candle" (Stage 1: 5m/15m spot shock alarm) with the stateful local "BTC Liquidation Flush Detector" (Stage 2: 4H post-flush stabilization radar). Replaces standalone execution logic with pure read-only forensic telemetry, ensuring zero trade signal contamination.

---

#### 1. Machine-Readable State & Routing Block (Python / Hermes / NotebookLM Index)

```yaml
module_id: "MOD_55"
entry_type: "CONTROL_PLANE_TELEMETRY_ENGINE"
waterfall_pillar: "PILLAR_2_AND_3_BRIDGE"
title: "Dual-Stage Disruption Telemetry & Recovery Radar Engine"

# TELEMETRY BOUNDARIES & BASELINES
telemetry_parameters:
  stage_1_tell_tale_candle:
    execution: "Stateless Cloud (GitHub Actions cron */15)"
    timeframes: ["5m", "15m"]
    triggers:
      relvol_min: 5.0
      body_range_min: 0.65
      direction: "bearish (red)"
  stage_2_liquidation_radar:
    execution: "Stateful Local (Binance USDⓈ-M WebSocket + SQLite)"
    baseline_warmup_fallback_usd: 30000000
    baseline_30d_median_required: true
    thresholds:
      elevated_flush: ">= 1.5x daily baseline"
      extreme_flush: ">= 2.0x daily baseline"

# OUTPUT CONTRACT
output_contract:
  execution_authority: "ZERO_TRADE_SIGNALS_GUARANTEED"
  integration_target: "Feeds MOD 33 (Master Radar) to evaluate Regime 5 transition"
```

---

#### 2. Protective Circuit Breakers (Mandatory Pre-Execution Filters)

*   **Circuit Breaker 1 — Zero Trade Signals Invariant (CB-01):** The output of this module is strictly *read-only telemetry*. A `STABILISATION CONFIRMED` state from Stage 2 is a **necessary, but not sufficient** condition for execution. It must feed into **MOD 33 (Unified 5-Regime Master Radar)** to transition out of `TRAP & CHOP`, requiring full MOD 18 waterfall clearance.
*   **Circuit Breaker 2 — Fail-Closed Baseline Warm-Up (CB-02):** The local SQLite WAL requires 30 UTC days to establish a valid median baseline. During warm-up, it transparently falls back to a `$30,000,000` daily baseline. If the WebSocket disconnects and misses >90 minutes of data, it emits `TRUST_DEGRADED` (UNKNOWN), tripping the **MOD 36** circuit breaker and enforcing a **100% Cash Lock**.
*   **Circuit Breaker 3 — The Single-Venue Limitation Ban (CB-03):** The `!forceOrder@arr` stream monitors Binance only. A `STABILISATION CONFIRMED` flag must be cross-verified by **MOD 07 (Domestic USD Spot CVD)** before any capital is deployed to ensure offshore derivatives aren't trapping the system.
*   **Circuit Breaker 4 — Hawkes Process Intersection (CB-04):** Stage 1 Tell Tale Candle spikes serve as early-warning precursors to **MOD 53 Hawkes Point Processes**. If Stage 1 fires, it immediately activates the **MOD 53 CB-01 8-hour cooling freeze**, physically blocking breakdown chasing before the Stage 2 radar begins its 4H stabilization scan.

---

#### 3. Core Conditional Signal Units (Condition A -> Outcome B -> Rule C)

##### CSU-55A: Stage 1 Cloud Shock Detection (Tell Tale Candle Detonation)
*   **Trigger Condition A (The Telemetry Scan):**
    1. The GitHub Actions cloud monitor detects simultaneous `5m` and `15m` bearish candles with relative volume `>= 5.0x` and body-to-range ratio `>= 0.65`.
*   **Observed Outcome B (The Mechanical Trajectory):**
    *   **Microstructure Lens:** An abnormal, high-velocity downside impulse has breached normal auction parameters. Liquidation cascades are likely initiating.
*   **Execution Rule C (The Non-Negotiable Action):**
    *   **Action:** Push Telegram/Discord `DISRUPTION FLAG` alert. Immediately trigger the **MOD 53 8-Hour Hawkes Cooling Freeze**. Halt all automated breakout entries.

##### CSU-55B: Stage 2 Local Stabilization Confirmed (Liquidation Radar)
*   **Trigger Condition A (The Telemetry Scan):**
    1. The local SQLite radar registers an `ELEVATED` (>= 1.5x) or `EXTREME` (>= 2.0x) flush.
    2. Post-flush 4H structure sequentially confirms: Halted lower lows -> Higher low formed -> Structure break -> Spot volume expansion.
*   **Observed Outcome B (The Mechanical Trajectory):**
    *   **Microstructure Lens:** The forced selling cascade has fully exhausted its leverage fuel, and early spot buyers are forming a structural floor.
*   **Execution Rule C (The Non-Negotiable Action):**
    *   **Action:** Emit `STABILISATION CONFIRMED`. Pass state to **MOD 33** to unlock Regime 5 (Capitulation Exhaustion & Reset) evaluation, contingent on MOD 07 Domestic USD Spot CVD verification.

##### CSU-55C: Stage 2 Baseline Trust Degraded (Fail-Closed)
*   **Trigger Condition A (The Telemetry Scan):**
    1. Local daemon experiences a WebSocket outage, system crash, or network failure resulting in >90 minutes of missing `!forceOrder@arr` data.
*   **Observed Outcome B (The Mechanical Trajectory):**
    *   **Control-Plane Lens:** The engine is blind to internal leverage states and cannot accurately gauge flush magnitude or baseline adherence.
*   **Execution Rule C (The Non-Negotiable Action):**
    *   **Action:** Emit `TRUST_DEGRADED`. Trigger **MOD 36 UNKNOWN (DATA UNAVAILABLE)**. Lock portfolio to 100% Cash until the database is rebuilt or gracefully re-baselines.
