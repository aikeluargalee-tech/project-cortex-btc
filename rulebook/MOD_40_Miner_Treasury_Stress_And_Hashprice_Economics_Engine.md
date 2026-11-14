# PROJECT CORTEX-BTC — MODULE 40: MINER TREASURY STRESS & HASHPRICE ECONOMICS ENGINE
**Waterfall Tier:** Pillar 5 Structural Supply-Side Economics Engine (Detects deteriorating miner unit revenue via `Hashprice`, network difficulty retarget pressure, fee-share compression, and corroborated miner-to-exchange transfers).
**Provenance & Empirical Benchmark Anchor:** Synthesized from the November 13, 2026 Cross-Model Architecture Audit (ChatGPT `MOD 38` + Qwen `MOD 37` + Meta `MOD 36` + Perplexity `MOD 37`) — isolating obligated miner supply economics from investor cohorts (`MOD 13–15`) while strictly distinguishing *gross hashprice compression* from *confirmed miner-to-exchange selling*.

---

## 1. Machine-Readable State & Routing Block (Python / Hermes / NotebookLM Index)

```yaml
module_id: "MOD_40"
entry_type: "MINER_ECONOMICS_AND_SUPPLY_STRESS_ENGINE"
waterfall_pillar: "PILLAR_5_MINER_TREASURY_STRESS"
title: "Miner Treasury Stress & Hashprice Economics Engine"

# PILLAR 1 & ANTI-DOUBLE-COUNTING GOVERNANCE
pillar_1_permission_required: true
anti_double_count_rule: "Miner-to-exchange transfers scored here are excluded from MOD 39 non-miner exchange inflows."
epistemic_disclosure: "Hashprice measures gross expected revenue per PH/day — NEVER assume an unverified electricity breakeven cost."

# PRIMARY TELEMETRY INPUTS (HASHRATE INDEX / MEMPOOL.SPACE / ON-CHAIN)
miner_economics_telemetry:
  btc_hashprice_per_ph_day: "Expected daily BTC revenue per PH/s (subsidy + fees / network difficulty)"
  usd_hashprice_per_ph_day: "Expected daily USD revenue per PH/s (BTC_Hashprice * Spot_USD)"
  hashprice_365d_percentile: "Rolling 365-day percentile rank of USD & BTC hashprice"
  next_difficulty_retarget_pct: "Projected difficulty adjustment % from mempool.space block-pace telemetry"
  fee_share_of_block_reward_pct: "Transaction fees / (Block subsidy + Transaction fees) * 100"
  network_hashrate_7d_vs_30d_pct: "7-day vs 30-day estimated network hashrate divergence (capitulation proxy)"
  miner_to_exchange_flow_zscore: "Z-score of BTC moving from identified mining pools to exchange wallets"

# DETERMINISTIC THRESHOLDS (INITIAL CALIBRATION PARAMETERS)
miner_stress_thresholds:
  hashprice_stress_percentile_max: 15.0 # Rolling 365D <= 15th percentile -> Revenue compression
  difficulty_squeeze_retarget_min_pct: 4.0 # Difficulty rising >= +4.0% while hashprice depressed
  hashrate_capitulation_drop_pct: -5.0 # 7D hashrate >= 5% below 30D average -> Unprofitable rigs shutting off
  miner_exchange_inflow_zscore_min: 2.0 # Corroborated miner-to-exchange transfer burst

# RISK & SIZING CONSTANTS (PILLAR 4)
risk_parameters:
  max_portfolio_risk_pct: 0.75
  miner_distribution_max_risk_pct: 0.375
  leverage_permitted: 1.0 # Strict Unleveraged Spot Only
```

---

## 2. Protective Circuit Breakers (Miner Telemetry Anti-Fallacy Rules)

* **Circuit Breaker 1 — Gross Revenue $\neq$ Net Profit (`CB-01`):** `Hashprice` (`USD` or `BTC` per `PH/day`) measures gross expected mining revenue—it does **not** know private fleet energy contracts (`$/kWh`), ASIC efficiency (`J/TH`), or debt service. Never invent a hardcoded "miner breakeven price"; rely strictly on rolling `365D` hashprice percentiles and observable on-chain behavior.
* **Circuit Breaker 2 — Revenue Stress Alone Is Not a Sell Signal (`CB-02`):** Low hashprice alone indicates tight margins, not automatic selling (well-capitalized miners often hold BTC or fund opex via equity/credit). `MOD 40` only restricts long risk when **Hashprice Stress** is corroborated by **elevated Miner-to-Exchange transfers (`Z >= 2.0`)**.
* **Circuit Breaker 3 — Pool Attribution Caveat (`CB-03`):** Public mining-pool payout addresses aggregate hashpower from thousands of independent sub-miners; treat `miner_to_exchange_flow_zscore` as a directional supply proxy requiring `MOD 05` Spot CVD confirmation, never a standalone trigger.
* **Circuit Breaker 4 — Weekly Pool Share Cadence (`CB-04`):** Mining pool distribution averages (`e.g., mempool.space` 1W pool stats) update on multi-day windows—never treat weekly pool shares as intraday signals.

---

## 3. Core Conditional Signal Units (`Condition A -> Outcome B -> Rule C`)

### CSU-40A: Corroborated Miner Treasury Distribution ("Obligated Supply Overhang")
* **Trigger Condition A (The Telemetry Scan):**
  1. **Hashprice Compression:** Rolling 365D `USD Hashprice` falls **`<= 15th percentile`** while transaction fees contribute **`< 3%` of block rewards** (or next difficulty retarget projects **`>= +4.0%`**, squeezing margins further).
  2. **Corroborated Supply Movement:** `miner_to_exchange_flow_zscore >= +2.0` over a 72H window while `USD Spot CVD` weakens below resistance.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Supply-Side Lens:** Margin-compressed miners are actively transferring treasury BTC to exchanges to cover operating/power obligations—creating persistent overhead sell pressure on rallies.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **CAP RISK AT `0.375%` (`AMBER` | `+8 pts` ICDM fragility)**; block breakout chasing (`MOD 30 CONFIG_A`) and take `Stage 1 (50%)` profits at the first structural resistance (`POC / VAH`).

### CSU-40B: Hashrate Capitulation & Post-Flush Miner Reset ("Generational Bottoming Signal")
* **Trigger Condition A (The Telemetry Scan):**
  1. **Rig Shut-Off & Difficulty Relief:** 7D network hashrate drops **`>= -5.0%` below 30D average** (triggering a negative difficulty adjustment projection `<= -3.0%`), **AND** `miner_to_exchange_flow_zscore` spikes `>= +3.0` and then **decays back `< +1.0` within 48–72 hours**.
  2. **Structural Reclaim:** Price reclaims swept 4H VAL (`MOD 11A`) with positive `USD Spot CVD` and `Hashprice` 5D slope turning upward.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Supply-Side Lens:** High-cost rigs have unplugged, forced miner treasury liquidation has exhausted itself, and upcoming downward difficulty retarget restores margins for surviving miners.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **RE-ARM FULL ENTRY PERMISSION (`-5 pts` ICDM fragility)**; authorize `0.375%–0.75%` spot reversal entry (`MOD 30 CONFIG_F / CONFIG_J`, `R >= 3.0`).

### CSU-40C: Uncorroborated Margin Squeeze ("Watch-Only Caution")
* **Trigger Condition A (The Telemetry Scan):**
  1. `USD Hashprice` drops `<= 15th percentile`, **but `miner_to_exchange_flow_zscore` remains `< +1.0`** (miners are holding reserves or funding opex off-chain).
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Supply-Side Lens:** Economic stress exists, but zero incremental BTC is hitting exchange order books.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **EMIT `MOD_40_STATE = AMBER` (Advisory Warning Only).** Do not restrict `MOD 33` entries unless `miner_to_exchange_flow_zscore` crosses `>= +2.0`.

### CSU-40D: Fee-Market Surge & Hashprice Expansion ("Healthy Network Tailwind")
* **Trigger Condition A (The Telemetry Scan):**
  1. `USD Hashprice` trends above its 50th percentile with rising on-chain fee share (`> 8%` of block rewards) and `miner_to_exchange_flow_zscore <= 0.0` (miners accumulating).
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Supply-Side Lens:** Strong network block-space demand and healthy miner margins eliminate forced treasury selling.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **SET `MOD_40_STATE = GREEN`.** Full `0.75%` risk ceiling permitted when `MOD 33` is in `REGIME_1` or `REGIME_2`.

---

## 4. Dynamic Regime Mutation Lookup Matrix (`M1` through `M8`)

| Mutation ID | Initial State | Telemetry Mutation Observed (`Condition A'`) | Mechanical Meaning (`Outcome B'`) | Mandatory Execution Override (`Rule C'`) |
| :--- | :--- | :--- | :--- | :--- |
| **M1: Post-Halving / Price Drop Hashprice Cliff** | `GREEN` | Spot BTC drops `-15%` into a difficulty retarget that still adjusts **upward `+5%`**, crushing `USD Hashprice` to a multi-year low. | Double revenue squeeze (lower BTC price + higher difficulty) forces weaker miners to liquidate reserves. | Escalate to `CSU-40A` watch; monitor `miner_to_exchange_flow_zscore` every 4H. |
| **M2: Miner Outflow Spike Absorbed by ETFs** | `CSU-40A` (Miner Inflows) | `miner_to_exchange_flow_zscore` hits `+2.5`, **but US Spot ETFs (`MOD 38`) + Coinbase USD Spot CVD absorb all supply above 4H POC**. | Institutional demand is effortlessly soaking up miner treasury sales. | **Override Bearish Cap;** keep `Stage 2` runner open while price holds above 4H POC. |
| **M3: Difficulty Downward Retarget Relief** | `CSU-40B` (Capitulation) | Negative difficulty adjustment (`-4% to -8%`) executes on-chain, immediately lifting `BTC Hashprice` for active rigs. | Structural cost-per-BTC drops overnight for surviving miners, removing sell urgency. | Confirm bottoming transition (`REGIME_5 -> REGIME_2` in `MOD 33`). |
| **M4: Regional Grid / Weather Hashrate Shock** | `GREEN` | Estimated 24H hashrate drops `-12%` abruptly due to a seasonal grid curtailment (e.g., Texas/winter storm) while `USD Hashprice` is healthy (`> 40th pct`). | Temporary exogenous power curtailment—not financial miner insolvency. | **Do Not Trigger `CSU-40B` Capitulation Signal;** wait for hashrate recovery within 72h. |
| **M5: Miner OTC vs. Public Exchange Routing** | `CSU-40A` | Miner pool balances decline, **but coins move to known OTC/custody desks with zero public exchange order-book impact**. | Miner monetized treasury via private OTC desk without hitting spot order books. | Keep `MOD_40_STATE = AMBER` (caution) rather than `RED` hard restriction. |
| **M6: Ordinal / Inscription / Settlement Fee Spike** | `CSU-40C` (Low Price) | On-chain congestion pushes transaction fees to `> 25%` of block rewards, lifting `Hashprice` out of the bottom decile. | Fee revenue windfall temporarily rescues miner cash flows without needing BTC price appreciation. | Downgrade stress from `CSU-40A` back to `GREEN / NEUTRAL`. |
| **M7: Pre-Retarget Block-Pace Acceleration** | Routine Scan | `mempool.space` shows block intervals averaging `< 8.5 min`, projecting a `+7%+` upward difficulty jump in `< 48 hours`. | Upcoming difficulty spike will compress `BTC Hashprice` by `~7%` upon retarget. | Flag upcoming margin compression in daily HUD if `USD Hashprice` is already `< 25th pct`. |
| **M8: Hashprice / Mempool Feed Outage** | Routine Scan | `mempool.space` or Hashrate Index API fails SLA (`MOD 36`). | Missing secondary supply-side telemetry. | Tag `MOD_40_STATE = UNKNOWN` (advisory only—never freeze core execution solely on miner API lag). |
