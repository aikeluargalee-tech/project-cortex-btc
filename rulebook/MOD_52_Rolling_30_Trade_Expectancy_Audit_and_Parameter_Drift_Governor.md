# PROJECT CORETEX BTC BRAIN — MODULE 52: ROLLING 30-TRADE EXPECTANCY AUDIT & PARAMETER DRIFT GOVERNOR
**Waterfall Tier:** Tier D (Continuous Governance, Statistical Calibration & Anti-Curve-Fitting Control-Plane) — operates directly alongside `MOD 18` (`0.75%` Risk & Two-Stage Exit), `MOD 28` (Live Autopsy & Black Swan Engine), `MOD 30` (`PCF3` Configs `A–J`), `MOD 36` (Determinism Attestation), and `MOD 37` (`Net R >= 3.0` & Equity-Curve Governor).
**Empirical Benchmark Anchor:**
1. **Live Operations Launch Baseline (November 2026):** Ahead of deploying Project CoreTex BTC Brain onto a 24/7 Ubuntu VPS + Hermes Agent + GitHub Actions stack, `MOD 52` establishes the deterministic statistical audit ledger (`trade_audit_ledger.json`) required to verify that live execution matches theoretical **`Net R >= 3.0`** expectancy without silent slippage erosion, regime drift, or emotional parameter tampering.
2. **Expectancy Law (`E[R]`):** Across a rolling window of `N = 30` closed spot trades, true system edge is governed by:
   $$E[R] = (\text{WinRate} \times \text{AvgWin}_R) - (\text{LossRate} \times \text{AvgLoss}_R)$$
   With strict `1.0x` spot-only `0.75%` risk capping every losing trade at `-1.0R` (`-0.75%` equity) and `MOD 37` requiring `>= +3.0R` projected reward, even a `35%` win rate yields `+0.40R` positive expectancy per trade (`+12.0R` / `+9.0%` compounded equity per 30 trades).

---

## 1. Machine-Readable State & Routing Block (Python / Hermes / GitHub Index)

```yaml
module_id: "MOD_52"
entry_type: "EXPECTANCY_AND_DRIFT_GOVERNOR"
waterfall_pillar: "TIER_D_STATISTICAL_GOVERNANCE"
title: "Rolling 30-Trade Expectancy Audit & Parameter Drift Governor"

# STATISTICAL AUDIT & EXPECTANCY THRESHOLDS
audit_parameters:
  rolling_window_trades: 30
  minimum_sample_for_param_change: 30 # BANNED from tuning thresholds on < 30 trades (anti-overfitting law)
  target_realized_expectancy_r: 0.35 # Healthy E[R] >= +0.35R per trade
  warning_expectancy_r: 0.10 # E[R] between 0.00R and +0.10R -> Trigger Amber Audit
  negative_expectancy_halt_r: 0.00 # Rolling 30-trade E[R] < 0.00R -> Mandatory System Audit & 0.375% Risk Throttle
  slippage_drift_tolerance_r: 0.25 # Max allowed gap between Modeled Net R (MOD 37) and Realized Net R
  config_quarantine_losses: 4 # Any MOD 30 Config (A-J) suffering 4 consecutive -1.0R losses enters quarantine

# ANTI-TRAP CIRCUIT BREAKERS
circuit_breakers:
  CB_01_ZERO_SMALL_SAMPLE_CURVE_FITTING: "NEVER modify module thresholds (Z-scores, VAH bar counts, or stop multipliers) based on 1 to 10 trades; require N >= 30 closed trades OR a verified structural Black Swan autopsy (MOD 28)."
  CB_02_SLIPPAGE_EROSION_THROTTLE: "If realized execution slippage/fees erode >= 0.25R vs MOD 37 pre-trade estimates across 10+ trades, force passive-only limit routing and halve risk to 0.375% until execution fills normalize."
  CB_03_CONFIG_ATTRIBUTION_QUARANTINE: "Track win rate and E[R] separately for each MOD 30 Config (A-J) and MOD 33 Regime (1-5); if any single Config prints 4 consecutive stop-outs, quarantine that Config without disabling healthy Configs."
  CB_04_IMMUTABLE_RISK_CEILING: "No statistical audit or winning streak may EVER raise max risk above 0.75% per trade or authorize > 1.0x leverage."

# RISK & SIZING CONSTANTS (PILLAR 4)
risk_parameters:
  healthy_expectancy_max_risk_pct: 0.75 # E[R] >= +0.10R
  degraded_expectancy_cap_pct: 0.375 # Rolling 30-trade E[R] < 0.00R or Slippage Drift >= 0.25R
  leverage_permitted: 1.0 # Strict Unleveraged Spot Only
```

---

## 2. Protective Circuit Breakers (Mandatory Governance Invariants)

* **Circuit Breaker 1 — Anti-Curve-Fitting Law (`CB-01`):** Changing Z-score thresholds or lookback windows after two or three frustrating losses destroys out-of-sample robustness. Parameter adjustments require **`N >= 30` closed trades** in the audit ledger (`CB-01`), except when a structural Black Swan (`MOD 28`) exposes a verified market-plumbing blind spot.
* **Circuit Breaker 2 — Execution Slippage & Fee Drift Guard (`CB-02`):** If real-world fills on USD spot venues slip `>= 0.25R` worse than `MOD 37` pre-trade L2 projections over 10 consecutive trades, `MOD 52` automatically throttles sizing to **`0.375%` (`GATE_AMBER`)** and enforces passive maker limit execution.
* **Circuit Breaker 3 — Granular Config Quarantine (`CB-03`):** Rather than shutting down the entire brain when one setup struggles, `MOD 52` isolates performance by `MOD 30` Config (`A–J`) and `MOD 33` Regime (`1–5`), quarantining any specific Config that hits **4 consecutive `-1.0R` stop-outs** for a `MOD 28` post-mortem.
* **Circuit Breaker 4 — Immutable Sovereign Risk Ceiling (`CB-04`):** Even if rolling 30-trade expectancy exceeds `+0.80R`, maximum equity risk per trade stays permanently locked at **`0.75%`** (`1.0x` spot only).

---

## 3. Core Conditional Signal Units (`Condition A -> Outcome B -> Rule C`)

### CSU-52A: Healthy Positive Expectancy Regime (`Rolling 30-Trade E[R] >= +0.35R`)
* **Trigger Condition A:** Across the last `30` closed spot trades, realized `E[R] >= +0.35R`, average losing trade stays `<= 1.05R` (confirming disciplined stop adherence), and slippage drift vs. `MOD 37` is `< 0.25R`.
* **Observed Outcome B:** The 5-Pillar Waterfall and `MOD 30` configurations are aligned with live market microstructure.
* **Execution Rule C:** **MAINTAIN FULL `0.75%` SPOT RISK AUTHORIZATION** (when `Pillar 1 == GATE_GREEN`) and prohibit discretionary parameter edits (`CB-01`).

### CSU-52B: Slippage / Execution Friction Drift Alert (`Realized R - Modeled R <= -0.25R`)
* **Trigger Condition A:** Over the last `10+` executed spot trades, actual entry/exit slippage + taker fees reduce realized reward by `>= 0.25R` compared to `MOD 37` pre-trade calculations.
* **Observed Outcome B:** Exchange L2 depth or order routing is experiencing higher friction than modeled (e.g., chasing market orders during volatile `1H` candles).
* **Execution Rule C:** **THROTTLE MAX RISK TO `0.375%` (`GATE_AMBER`)** and enforce **100% passive limit-order entry (`MOD 51 CB-03`)** until 10-trade slippage drift drops back below `0.15R`.

### CSU-52C: Single-Config Regime Mismatch (`4 Consecutive -1.0R Losses in One Config`)
* **Trigger Condition A:** A specific `MOD 30` configuration (e.g., `CONFIG_G` breakout or `CONFIG_F` range fade) records **4 consecutive stop-outs** inside the current `MOD 33` regime, while total portfolio drawdown remains within `MOD 37` bounds.
* **Observed Outcome B:** That specific tactical pattern is temporarily mismatched with current order-book behavior.
* **Execution Rule C:** **QUARANTINE ONLY THAT CONFIG (`STATUS = QUARANTINED`)** and generate a `MOD 28` diagnostic entry; keep unaffected `MOD 30` Configs active at normal sizing.

### CSU-52D: Rolling 30-Trade Negative Expectancy Governor (`Rolling 30-Trade E[R] < 0.00R`)
* **Trigger Condition A:** Rolling `30`-trade realized expectancy drops below **`0.00R`** (or cumulative drawdown hits `MOD 37` `-3.00%` weekly lock).
* **Observed Outcome B:** Structural regime shift has degraded edge across multiple waterfall modules.
* **Execution Rule C:** **ENFORCE `0.375%` HALF-SIZE RISK CAP (`GATE_AMBER`)** across all signals, run a full `MOD 28` 30-trade attribution autopsy via Hermes + Gemini, and require `10` consecutive trades at `E[R] >= +0.20R` before restoring `0.75%` sizing.

---

## 4. Dynamic Regime Mutation Lookup Matrix (`M1` through `M8`)

| Mutation ID | Initial State | Telemetry Mutation Observed | Mandatory Execution Override |
| :--- | :--- | :--- | :--- |
| **M1: Premature Stage-2 Runner Cutting** | `CSU-52A` / `52D` | Audit reveals `AvgWin_R` dropped from `3.2R` to `< 1.8R` because operator manually closed Stage 2 (`50%`) runners early before `1D` targets. | **Lock Automated Trailing Stop (`MOD 18`);** ban manual early runner exits unless `Rule 1` / `MOD 34` fires. |
| **M2: Stop-Loss Slippage Breach (`AvgLoss > 1.15R`)** | Any Active State | Gapping weekend or cascade stops cause average loss to exceed `1.15R` (`> 0.86%` equity per trade). | **Activate `MOD 50` Weekend & `MOD 51` Limit-Ladder Filters** immediately. |
| **M3: Post-Quarantine Paper-Validation Re-Entry** | `CSU-52C` (Quarantined) | A quarantined `MOD 30` Config logs `5` consecutive simulated shadow signals with `E[R] >= +0.40R` after a `MOD 33` regime shift. | **Lift Quarantine at `0.375%` Probe Sizing** for the next 5 live trades. |
| **M4: Zero-Trade Patience Streak (`> 21 Days` Cash Lock)** | `GATE_RED` / `MOD 44` | System executes `0` trades for `21+` days during an extended bear/IPO drain (`Nov 2026` regime). | **Log `0.00R` Capital Preservation Win;** do NOT lower `Net R >= 3.0` standards just to force activity. |
| **M5: `MOD 36` Telemetry Corruption Invalidation** | Audit Review | A logged loss occurred while an upstream feed was stale (`MOD 36` breach). | **Tag Trade `INFRASTRUCTURE_FAULT`**, exclude from strategy `E[R]`, and tighten `MOD 36` SLA check. |
| **M6: Sovereign Vault (`Sleeve B`) Firewall Audit** | Monthly Review | Monthly check confirms `0` tactical swing stop-outs touched `Sleeve B` `2-of-3` cold storage (`MOD 46 CB-04`). | **Certify `BARBELL_INTEGRITY = PASS`** on monthly `MOD 45` HUD report. |
| **M7: Rulebook Commit & Checksum Verification (`MOD 36`)** | Every Git Sync | New module (`MOD 47–52`) is pushed to `origin/main` via Google Antigravity. | **Record SHA-256 Commit Hash in `trade_audit_ledger.json`** to link every trade to its exact rulebook version. |
| **M8: Audit Ledger Missing / Corrupted (`MOD 36`)** | Pre-Trade Check | `trade_audit_ledger.json` fails JSON schema validation on VPS. | **Fail-Closed to `0.375%` (`GATE_AMBER`)** until ledger is restored from GitHub backup. |
