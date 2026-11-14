# PROJECT CORTEX-BTC — MODULE 36: TELEMETRY TRUST, STALENESS SLA & DETERMINISM ATTESTATION
**Waterfall Tier:** Tier D Supreme Control-Plane Gate (Sits *above* `MOD 33` Master Regime Radar and `MOD 18` Sizing Engine to enforce fail-closed data integrity, cross-venue price quorum, cron heartbeat verification, and bit-for-bit replay determinism).
**Provenance & Empirical Benchmark Anchor:** Synthesized from the November 13, 2026 Cross-Model Architecture Audit (ChatGPT, Qwen, Perplexity) — addressing GitHub Actions `schedule` best-effort top-of-hour queue delays/drops, stale API feeds, cross-venue price outliers, and strict separation between NotebookLM qualitative research and the deterministic pure-Python compiler (`cortex_matrix_engine.py`).

---

## 1. Machine-Readable State & Routing Block (Python / Hermes / NotebookLM Index)

```yaml
module_id: "MOD_36"
entry_type: "CONTROL_PLANE_TRUST_ATTESTATION"
waterfall_pillar: "TIER_D_SUPREME_TELEMETRY_TRUST_GATE"
title: "Telemetry Trust, Staleness SLA & Determinism Attestation"

# SUPREME HIERARCHY POSITION
governance_priority: 1 # Overrides MOD 33 Regime Permission and MOD 18 Entry Sizing
icdm_contribution_mode: "BINARY_FAIL_CLOSED_GATE" # Does not add ICDM points; emits GREEN / AMBER / RED / UNKNOWN

# MANDATORY MODULE OUTPUT CONTRACT (APPLIES TO ALL MODULES)
common_module_contract:
  required_timestamps: ["event_timestamp_utc", "publication_timestamp_utc", "ingestion_timestamp_utc", "as_of_timestamp_utc"]
  required_hashes: ["ruleset_yaml_sha256", "input_snapshot_sha256", "decision_replay_sha256"]
  allowed_states: ["GREEN", "AMBER", "RED", "UNKNOWN"]
  zero_hallucination_rule: "UNKNOWN (missing/stale/unverified) MUST NEVER be coerced to 0 or GREEN."

# TELEMETRY SLA & QUORUM THRESHOLDS
sla_and_quorum_thresholds:
  feed_staleness_multiplier_max: 2.0 # Feed age > 2.0x declared cadence -> UNKNOWN / TRUST_DEGRADED
  cron_heartbeat_max_gap_minutes: 90 # GitHub Actions hourly schedule dead-man switch
  venue_quorum_min_sources: 3 # Minimum independent spot venues (e.g., Coinbase, Binance, Kraken/Bitstamp)
  venue_quorum_max_dispersion_bps: 35.0 # Max mid-price spread across quorum venues before outlier freeze
  ntp_clock_skew_max_ms: 2000 # Max local clock drift vs UTC NTP reference
  rearm_clean_cycles_required: 2 # Consecutive clean cycles required to lift TRUST_DEGRADED lock

# RISK & SIZING CONSTANTS (PILLAR 4)
risk_parameters:
  max_portfolio_risk_pct: 0.75
  degraded_trust_max_risk_pct: 0.00 # Strict Fail-Closed Cash / Freeze
  leverage_permitted: 1.0 # Strict Unleveraged Spot Only
```

---

## 2. Protective Circuit Breakers (Control-Plane Data Invariants)

* **Circuit Breaker 1 — Fail-Closed `UNKNOWN` Law (`CB-01`):** Missing, stale, or unverified telemetry must be tagged `UNKNOWN`—never defaulted to `0.0` or `GREEN`. While `RED` logs a verified adverse market event and `UNKNOWN` logs an unverified telemetry state, **both block all new spot entries**.
* **Circuit Breaker 2 — GitHub Actions Cron Dead-Man Switch (`CB-02`):** Because GitHub Actions `schedule` triggers (`cron: "5 * * * *"`) are best-effort and subject to top-of-hour queue delays or drops under load, an independent watchdog checks `ingestion_timestamp_utc`. If no attested pipeline heartbeat arrives within **`90 minutes`**, new entries lock automatically until **2 consecutive clean cycles** pass.
* **Circuit Breaker 3 — Three-Venue Price Quorum (`CB-03`):** Spot reference price and stop-loss triggers must be validated across at least **3 independent spot venues** (e.g., Coinbase USD, Binance USDT, Kraken/Bitstamp USD). If dispersion exceeds **`35 bps`**, freeze execution to prevent single-venue API glitches or flash-wick anomalies from triggering false entries or premature stops.
* **Circuit Breaker 4 — Bit-for-Bit Compiler Determinism (`CB-04`):** NotebookLM and LLM summaries are strictly research/audit layers and **never** enter the live execution path. `cortex_matrix_engine.py` must log `ruleset_yaml_sha256` + `input_snapshot_sha256` so any decision can be replayed bit-for-bit during `MOD 28` Live Autopsies.

---

## 3. Core Conditional Signal Units (`Condition A -> Outcome B -> Rule C`)

### CSU-36A: Critical Feed Staleness or Cron Heartbeat Lapse (`TRUST_DEGRADED — Fail-Closed`)
* **Trigger Condition A (The Telemetry Scan):**
  1. Any critical input feed (`spot price`, `USD/Perp CVD`, `OI/funding`, or `order-book depth`) exceeds **`2.0x` its declared cadence SLA**, **OR** `as_of_timestamp_utc` lags current UTC time by **`> 90 minutes`** (missed/delayed cron heartbeat).
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Control-Plane Lens:** The engine is blind to current market state; computing entries on stale data creates unpriced tail exposure.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **SET `MOD_36_STATE = UNKNOWN (TRUST_DEGRADED)`.** Override `MOD 33` to block all new spot entries; manage any existing open swing strictly from the last attested pre-computed stop/target levels; send `CRITICAL` Telegram HUD warning.

### CSU-36B: Cross-Venue Quorum Dispersion Breach ("Single-Venue Feed Anomaly")
* **Trigger Condition A (The Telemetry Scan):**
  1. Fewer than **`3` independent spot venues** respond within timeout, **OR** the max-minus-min mid-price spread across active quorum venues exceeds **`35 bps`** (`0.35%`) outside a verified `MOD 32` exchange solvency event.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Control-Plane Lens:** One venue is experiencing an API freeze, order-book outage, or localized stablecoin de-peg distortion.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **FREEZE NEW ENTRIES & SUPPRESS VENUE-SPECIFIC STOP TRIGGERS** until cross-venue dispersion compresses back below `35 bps` across `>= 3` venues.

### CSU-36C: Determinism Replay or Rule-Hash Drift Violation ("Governance Halt")
* **Trigger Condition A (The Telemetry Scan):**
  1. `ruleset_yaml_sha256` does not match the version-controlled GitHub configuration hash, **OR** deterministic replay of `input_snapshot_sha256` fails to reproduce the logged `MOD 18 / MOD 33` verdict bit-for-bit.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Control-Plane Lens:** Unlogged manual override, schema-adapter mismatch, or race condition compromised audit reproducibility.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **IMMEDIATE EXECUTION HALT (`0.00%` New Risk).** Route snapshot to `MOD 28` Live Autopsy and require manual operator hash reconciliation before re-arming.

### CSU-36D: Full Telemetry Attestation Passed (`TRUST_VERIFIED = GREEN`)
* **Trigger Condition A (The Telemetry Scan):**
  1. All critical feeds fresh (`<= 2.0x` SLA), `>= 3` venues within `<= 35 bps` quorum, NTP clock skew `< 2000 ms`, and `ruleset_yaml_sha256` verified.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Control-Plane Lens:** Input state is verified, reproducible, and safe for downstream `MOD 33` regime evaluation.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **EMIT `MOD_36_STATE = GREEN` (`TRUST_VERIFIED`).** Pass control downstream to `MOD 33` Master Radar (`GREEN` does not raise risk above `0.75%`).

---

## 4. Dynamic Regime Mutation Lookup Matrix (`M1` through `M8`)

| Mutation ID | Initial State | Telemetry Mutation Observed (`Condition A'`) | Mechanical Meaning (`Outcome B'`) | Mandatory Execution Override (`Rule C'`) |
| :--- | :--- | :--- | :--- | :--- |
| **M1: Top-of-Hour GitHub Cron Delay** | `GREEN` (Hourly Cron) | Scheduled `:05` UTC GitHub Actions job queues for `> 45 min` during peak load, pushing heartbeat gap past `90 min`. | Pipeline running on stale prior-hour snapshot. | **Flip to `UNKNOWN` at `90 min` mark**; require `2` consecutive clean hourly cycles to re-arm. |
| **M2: Secondary Feed Missing, Core Fresh** | `GREEN` | Core price/CVD/depth feeds are fresh (`< 5 min`), **but a slow macro/on-chain feed (`e.g., H.4.1` or `Farside`) is delayed**. | Core execution tape is valid; slow background feed is pending publication. | Keep core state `AMBER` (do not freeze exits), apply `MOD 31 M7` 50% caution penalty to the missing macro/on-chain sub-metric. |
| **M3: Stablecoin De-Peg Quorum Split** | `GREEN` (3-Venue Quorum) | Coinbase USD and Kraken USD agree within `8 bps`, **but Binance USDT trades `+45 bps` higher** due to USDT de-peg pressure. | Cross-venue dispersion caused by quote-currency (`USDT` vs `USD`) divergence, not API failure. | Exclude USDT venue from USD reference price; anchor execution exclusively to **Domestic USD quorum (`MOD 07`)**. |
| **M4: Post-Outage Re-Arm Verification** | `UNKNOWN` (Frozen) | Outage resolves and fresh telemetry arrives on Cycle 1. | Single packet could still contain catch-up backlog spikes. | **Hold Freeze Through Cycle 1;** lift `UNKNOWN` lock only after **Cycle 2** passes all SLA & quorum checks. |
| **M5: Manual Operator Override Logged** | Any Active State | Operator manually overrides a `MOD 33` or `MOD 18` rule during live trading. | Discretionary intervention bypassed deterministic ruleset. | **Force `override_audit_flag = TRUE`** in JSON log; mandate `MOD 28` post-trade autopsy regardless of P&L outcome. |
| **M6: Local VPS / Mobile Clock Drift** | `GREEN` | System clock drifts `> 2000 ms` from UTC NTP reference. | Candle-close timestamps (`1H / 4H` bar-count rules in `00C`) could misalign across exchanges. | Trigger `AMBER` clock-sync warning; block bar-close entries until NTP sync restores `< 500 ms`. |
| **M7: Schema Adapter Unmapped Key Spike** | `GREEN` | `cortex_schema_adapter.py` reports `> 5` newly unmapped critical keys after an upstream API schema change. | Upstream vendor changed JSON field names silently. | **Flip to `UNKNOWN` (`Schema Drift Halt`)** until `KEY_ALIAS_MAP` is updated and unit-tested. |
| **M8: Clean Audit Trail Attestation** | Routine Cycle | Every cycle writes immutable `(input_hash, ruleset_hash, verdict_hash)` to Git history. | Guarantees 100% walk-forward backtest fidelity without look-ahead bias. | Archive `as_of_timestamp_utc` alongside `publication_timestamp_utc` for all delayed macro/ETF prints. |
