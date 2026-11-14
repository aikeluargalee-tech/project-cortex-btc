# PROJECT CORTEX-BTC — MODULE 39: EXCHANGE SUPPLY ACTIVATION & AGED-UTXO DORMANCY ENGINE
**Waterfall Tier:** Pillar 5 On-Chain Supply-Activation Engine (Tracks dormant/aged UTXO spending and entity-adjusted BTC migration onto exchange-controlled infrastructure *before* realized spot selling prints).
**Provenance & Empirical Benchmark Anchor:** Synthesized from the November 13, 2026 Cross-Model Architecture Audit (ChatGPT `MOD 37` + Qwen `MOD 38` + Meta `MOD 39`) — separating *cohort valuation* (`MOD 13–15`) from *exchange-accessible supply activation* (`Supply-Adjusted CDD`, `Dormancy`, and `Point-in-Time Entity-Adjusted Exchange Net Position Change`) with a strict anti-double-counting cap against `MOD 15`.

---

## 1. Machine-Readable State & Routing Block (Python / Hermes / NotebookLM Index)

```yaml
module_id: "MOD_39"
entry_type: "ONCHAIN_SUPPLY_ACTIVATION_ENGINE"
waterfall_pillar: "PILLAR_5_EXCHANGE_SUPPLY_ACTIVATION"
title: "Exchange Supply Activation & Aged-UTXO Dormancy Engine"

# PILLAR 1 & ANTI-DOUBLE-COUNTING GOVERNANCE
pillar_1_permission_required: true
anti_double_count_rule: "ICDM Vector 4 applies max(MOD_15_LTH_Delta, MOD_39_Supply_Delta) — NEVER sum both deltas."
point_in_time_integrity: "Historical backtests MUST use point-in-time entity-adjusted exchange labels (never retroactively relabeled clusters)."

# PRIMARY TELEMETRY INPUTS (SUPPLY ACTIVATION & VENUE MIGRATION)
supply_activation_telemetry:
  supply_adjusted_cdd_zscore: "Z-score of (Value_BTC * Coin_Lifespan_Days) normalized by circulating supply"
  dormancy_7d_trend: "CDD / Transfer_Volume_BTC (average age of spent coins)"
  entity_adjusted_exchange_netflow_72h_btc: "Confirmed external inflows minus outflows across entity-labelled exchanges (excludes internal wallet reshuffles)"
  exchange_reserve_30d_change_pct: "30-day percentage change in total BTC held on identified exchanges"
  illiquid_supply_30d_change_btc: "30-day net change in entities with < 25% historical spending ratio"
  exchange_label_confidence: "Attribution confidence score (HIGH / MEDIUM / LOW)"

# DETERMINISTIC THRESHOLDS (INITIAL CALIBRATION PARAMETERS)
supply_thresholds:
  cdd_spike_zscore_min: 3.0 # Supply-adjusted CDD >= +3.0 sigma -> Aged UTXO awakening
  net_inflow_72h_overhang_btc: 12000.0 # Sustained 72h entity-adjusted net exchange inflow
  supply_shock_outflow_30d_pct: -2.0 # Exchange balances down > -2.0% over 30D -> Structural supply sink

# RISK & SIZING CONSTANTS (PILLAR 4)
risk_parameters:
  max_portfolio_risk_pct: 0.75
  supply_overhang_max_risk_pct: 0.375
  leverage_permitted: 1.0 # Strict Unleveraged Spot Only
```

---

## 2. Protective Circuit Breakers (On-Chain Supply Anti-Noise Rules)

* **Circuit Breaker 1 — Exchange Deposit $\neq$ Immediate Market Sell (`CB-01`):** Coins moving into exchange wallets may be intended for OTC settlement, derivatives collateral, or institutional custody rather than immediate spot liquidation. An exchange inflow spike **never** triggers a standalone market exit unless corroborated by deteriorating spot structure (`Spot < STH Realized Price`, `USD Spot CVD < 0`, or `4H POC/VAL rejection`).
* **Circuit Breaker 2 — Entity-Adjustment Mandatory (`CB-02`):** Raw on-chain transfer volume and unadjusted Coin Days Destroyed (`CDD`) are heavily distorted by internal exchange cold-to-hot wallet consolidations. Only **entity-adjusted** exchange flows and **supply-adjusted CDD** may enter `MOD 39`.
* **Circuit Breaker 3 — Anti-Double-Counting Cap vs. `MOD 15` (`CB-03`):** Because `MOD 15` already tracks LTH-to-STH wealth transfer, `MOD 31` ICDM takes **`max(MOD_15_points, MOD_39_points)`**—preventing the same old-coin distribution wave from being penalized twice.
* **Circuit Breaker 4 — Low Label Confidence Quarantine (`CB-04`):** If an on-chain provider flags `exchange_label_confidence == LOW` (unidentified cluster migration), tag `MOD_39_STATE = UNKNOWN` (`MOD 36`) rather than triggering a false distribution alert.

---

## 3. Core Conditional Signal Units (`Condition A -> Outcome B -> Rule C`)

### CSU-39A: Aged-UTXO Awakening & Exchange Supply Overhang ("Pre-Distribution Warning")
* **Trigger Condition A (The Telemetry Scan):**
  1. **Supply-Adjusted CDD `>= +3.0 sigma`** (dormant `1Y+` UTXOs awakening) **AND** **72-hour entity-adjusted net exchange inflow `> +12,000 BTC`** (`HIGH` label confidence).
  2. **Structural Confirmation:** Price trades below `STH Realized Price` (`MOD 13`, `STH-MVRV < 1.00`) OR fails to hold above `4H POC / VAH` with weakening `USD Spot CVD` (`MOD 05`).
* **Observed Outcome B (The Mechanical Trajectory):**
  * **On-Chain Supply Lens:** Dormant holders have moved physical inventory onto exchange order books into weak spot demand—creating overhead supply overhang.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **BLOCK NEW SPOT LONGS (`+7 pts` ICDM fragility, subject to `max(MOD 15, MOD 39)` cap)**; if holding an active swing long, **accelerate `Stage 1 (50%)` profit exit** on the first 4H close below POC.

### CSU-39B: Structural Supply Sink & Re-Dormancy ("Illiquid Squeeze Tailwind")
* **Trigger Condition A (The Telemetry Scan):**
  1. **30-day exchange reserves drop `<= -2.0%`** (persistent entity-adjusted net exchange outflows for `>= 7 consecutive days`) **AND** **illiquid supply increases** over 30 days.
  2. **Supply-Adjusted CDD & Dormancy** remain at or below baseline (`Z < +1.0`), proving long-term holders are locking coins away rather than spending.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **On-Chain Supply Lens:** Available exchange float is contracting; shallow pullbacks get absorbed quickly once `MOD 33` permits trend entries.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **AWARD CONFLUENCE CREDIT TO `MOD 18` (`-6 pts` ICDM fragility)**; allow `Stage 2` trailing runners extra room (`hold through first pullback above 4H POC`) when `MOD 33` is in `REGIME_1` or `REGIME_2`.

### CSU-39C: Internal Custodian / Exchange Consolidation ("False Inflow Filter")
* **Trigger Condition A (The Telemetry Scan):**
  1. Raw CDD or gross transfer volume spikes, **but entity-adjusted net exchange inflow stays `~0 BTC`** (coins moved within the same custodian or exchange entity).
* **Observed Outcome B (The Mechanical Trajectory):**
  * **On-Chain Supply Lens:** Routine operational wallet maintenance—zero net increase in sellable exchange inventory.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **SUPPRESS SUPPLY ALERT (`MOD_39_STATE = GREEN / NEUTRAL`).** Zero change to active risk or exit posture.

### CSU-39D: Post-Distribution Inflow Exhaustion ("Overhang Absorbed")
* **Trigger Condition A (The Telemetry Scan):**
  1. Following a `CSU-39A` inflow spike, 72H entity-adjusted net exchange flows flip back negative (`net outflows`), `Supply-Adjusted CDD` drops `< +1.0 sigma`, and price reclaims 4H VAL/POC with positive `USD Spot CVD`.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **On-Chain Supply Lens:** Deposited supply has been absorbed by buyers without breaking structural support.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **LIFT SUPPLY OVERHANG VETO;** re-enable standard `MOD 18 / MOD 33` entry evaluation (`R >= 3.0`).

---

## 4. Dynamic Regime Mutation Lookup Matrix (`M1` through `M8`)

| Mutation ID | Initial State | Telemetry Mutation Observed (`Condition A'`) | Mechanical Meaning (`Outcome B'`) | Mandatory Execution Override (`Rule C'`) |
| :--- | :--- | :--- | :--- | :--- |
| **M1: Whale Deposit + Perp Pump Divergence** | `REGIME_1 / 2` (Rally) | Price makes a marginal new high on perp CVD, **while `Supply-Adjusted CDD >= +3.5 Z` and `> 5,000 BTC` hits exchanges** (`MOD 30 CONFIG_H`). | Old coins are moving onto exchanges specifically to sell into retail breakout FOMO. | **Immediate `Stage 1 (50%–70%)` Profit Exit** ahead of visible price breakdown. |
| **M2: Capitulation Inflow Into Passive Bid Wall** | `REGIME_4 / 5` (Selloff) | Heavy `STH` exchange inflows print during a flush, **but `1Y+` LTH CDD stays dormant and `USD Spot CVD` turns sharply positive at HTF VAL**. | Weak hands are panic-depositing into strong institutional absorption (`MOD 06A`). | **Do Not Panic-Sell;** prepare `MOD 30 CONFIG_J` reclaim watch once inflows peak. |
| **M3: Post-Halving / ETF Custody Cold Sweep** | `REGIME_2` (Range) | `> 15,000 BTC` leaves Coinbase/BitGo in a single 48H window while `Dormancy` stays low. | Institutional ETF or corporate treasury cold-storage withdrawal—removing liquid float. | **Bullish Structural Bias (`CSU-39B`)**; prioritize long setups upon 4H VAH acceptance. |
| **M4: Retroactive Cluster Relabeling Guard** | Backtest / Audit | On-chain vendor updates wallet labels retroactively for a past month. | Using retroactively updated labels introduces look-ahead bias into historical calibration. | **Enforce Point-in-Time Snapshot Hash (`MOD 36`)**; never re-score live rules on revised history. |
| **M5: Miner vs. Non-Miner Inflow Attribution** | `CSU-39A` (Inflow Spike) | Entity attribution reveals `> 60%` of the exchange inflow originated from known mining pools rather than dormant investors. | Supply pressure is miner-treasury driven rather than LTH distribution. | **Route Signal to `MOD 40` (Miner Economics)** to avoid double-counting the same BTC transfer. |
| **M6: Multi-Week Exchange Balance Trend Flip** | `CSU-39B` (Supply Sink) | After 60 days of declining exchange balances, 30D exchange reserve change flips from **`-2.5%` to `+1.5%`** while price stalls below 200D MA. | Multi-month accumulation regime has transitioned into net exchange distribution. | **Downgrade `MOD_39_STATE` from `GREEN` to `AMBER`**; tighten trailing stops on open swings. |
| **M7: Stablecoin + BTC Simultaneous Inflow** | `REGIME_2 / 5` | Both `BTC` and `> $500M` in fresh `USDC/USDT` enter spot exchanges simultaneously while `USD Spot CVD` rises. | Fresh stablecoin buying power matches incoming BTC supply (`balanced liquidity expansion`). | **Neutralize Supply Veto;** allow `MOD 30` order flow to arbitrate direction. |
| **M8: On-Chain Indexer Lag (`> 6 Blocks`)** | Routine Scan | Primary on-chain API lags Bitcoin chain tip by `> 6 blocks` (`~60+ min`). | Recent exchange deposit bursts may not yet appear in the JSON feed. | Tag `MOD_39_STATE = UNKNOWN` (`MOD 36`) during high-volatility cascades until indexer catches tip. |
