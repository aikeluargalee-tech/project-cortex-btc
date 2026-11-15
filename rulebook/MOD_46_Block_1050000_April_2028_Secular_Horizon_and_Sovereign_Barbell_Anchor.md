# PROJECT CORTEX-BTC — MODULE 46: BLOCK 1,050,000 (APRIL 2028) SECULAR HORIZON & SOVEREIGN BARBELL ANCHOR
**Waterfall Tier:** Pillar 1 (Secular Supply Schedule), Pillar 4 (Barbell Capital Allocation), & Pillar 5 (On-Chain Cohorts & Sovereign Multi-Sig Custody) — operates directly alongside `MOD 13` (STH Realized Price & MVRV), `MOD 14` (SOPR Reset Cycles), `MOD 18` (`CSU-18D` Sovereign Cold-Storage Tranches), `MOD 32` (`2-of-3` Dual-Jurisdiction Cold Storage), and `MOD 41` (Secular Cycle ATH Cluster & Harvest Roadmaps).
**Empirical Benchmark Anchor:**
1. **Epoch 1 — Block `210,000` (28 Nov 2012):** Block subsidy cut `50 -> 25 BTC`. Halving price `~$12` -> cycle peak `~$1,163` (`~12 months` post-halving).
2. **Epoch 2 — Block `420,000` (9 Jul 2016):** Block subsidy cut `25 -> 12.5 BTC`. Halving price `~$650` -> cycle peak `~$19,700` (`~17 months` post-halving).
3. **Epoch 3 — Block `630,000` (11 May 2020):** Block subsidy cut `12.5 -> 6.25 BTC`. Halving price `~$8,800` -> cycle peak `~$69,000` (`~18 months` post-halving; `+684%` halving-to-peak expansion).
4. **Epoch 4 — Block `840,000` (20 Apr 2024):** Block subsidy cut `6.25 -> 3.125 BTC`. Halving price `~$64,000` -> cycle peak `~$126,199` on Oct 6, 2025 (`~17.5–18 months` post-halving; `+97%` halving-to-peak expansion), followed by the `2026` bear drawdown back to the `~$62,000–$64,300` prior-halving valuation floor.
5. **Epoch 5 — Block `1,050,000` (~April 8–13, 2028):** Scheduled block subsidy cut from `3.125 BTC` (`~450 BTC/day`) to `1.5625 BTC` (`~225 BTC/day`). Historical `12–18 month` post-halving peak lag maps the primary Epoch 5 distribution window to **April 2029 – October 2029** under diminishing structural multiples (`MOD 41`).

---

## 1. Machine-Readable State & Routing Block (Python / Hermes / NotebookLM Index)

```yaml
module_id: "MOD_46"
entry_type: "SECULAR_HORIZON_AND_BARBELL_ANCHOR"
waterfall_pillar: "PILLAR_1_4_5_SECULAR_SUPPLY_EPOCH"
title: "Block 1,050,000 (April 2028) Secular Horizon & Sovereign Barbell Anchor"

# EPOCH 5 SUPPLY SCHEDULE & HORIZON CONSTANTS
epoch_parameters:
  target_halving_block: 1050000
  projected_halving_window: "2028-04-08 to 2028-04-13"
  current_subsidy_btc: 3.125 # ~450 BTC/day new issuance
  post_halving_subsidy_btc: 1.5625 # ~225 BTC/day new issuance (50% supply cut)
  epoch_4_halving_price_anchor_usd: 64000 # Block 840,000 (Apr 20, 2024) valuation baseline
  historical_peak_lag_months: [12, 18] # Empirical lag after halving block (2012: 12m, 2016: 17m, 2020: 18m, 2024: 18m)
  projected_epoch_5_peak_window: "2029-04 to 2029-10"
  diminishing_return_law: "Structure repeats (12-18m post-halving peak), magnitude compresses (3.49x in 2021 -> 1.83x ATH-to-ATH / +97% halving-to-peak in 2025)"

# BARBELL ARCHITECTURE SEPARATION (TACTICAL SWING VS. SOVEREIGN COLD STORAGE)
barbell_sleeves:
  sleeve_a_tactical_swing:
    purpose: "Harvest 2-way spot swings & enforce 100% Cash Lock during liquidity vacuums (MOD 44/45)"
    max_risk_per_trade_pct: 0.75
    leverage_permitted: 1.0 # Strict 1.0x Spot Only
    horizon_days: [1, 30]
  sleeve_b_sovereign_vault:
    purpose: "Accumulate discounted UTXOs ahead of Block 1,050,000 (Apr 2028) & Apr-Oct 2029 peak window"
    custody_standard: "2-of-3 Dual-Jurisdiction Multi-Sig Cold Storage (MOD 32 CSU-32C)"
    horizon_months: [18, 36]
    never_used_for: "Intraday/weekly swing stop-losses or exchange margin collateral"

# ANTI-TRAP CIRCUIT BREAKERS
circuit_breakers:
  CB_01_HORIZON_NOT_PREDICTION: "Use April 2028 (Block 1,050,000) as a multi-year valuation anchor, NEVER as an excuse to ignore short-term cash locks during active liquidation cascades (MOD 03) or Mega-IPO drains (MOD 44)."
  CB_02_HALVING_IS_SUPPLY_CUT_NOT_PEAK: "Block 1,050,000 (April 2028) is the supply shock; historical cycle tops arrive 12-18 months AFTER the halving (April-October 2029)."
  CB_03_DIMINISHING_MAGNITUDE_DISCIPLINE: "Calibrate Epoch 5 harvest expectations strictly to MOD 41 diminishing-return bands ($172k-$180k Conservative / $230k-$250k Bull Stretch), never early-cycle 10x+ extrapolations."
  CB_04_BARBELL_FIREWALL: "Never raid Sovereign Multi-Sig Cold Storage for tactical swing trades, and never deploy Sovereign Reserve tranches until on-chain capitulation & ETF flow stabilization gates pass."

# RISK & SIZING CONSTANTS
risk_parameters:
  tactical_swing_max_risk_pct: 0.75
  leverage_permitted: 1.0 # Strict Unleveraged Spot Only
```

---

## 2. Protective Circuit Breakers (Mandatory Horizon & Barbell Invariants)

* **Circuit Breaker 1 — Time Horizon Is Not a License to Catch Falling Knives (`CB-01`):** Anchoring to April 2028 (`Block 1,050,000`) eliminates short-term emotional panic, **but** Tactical Swing capital (`Sleeve A`) must still obey `MOD 44` and `MOD 45` (`100% Cash Lock` during active ETF outflow streaks and forced deleveraging). Long-term conviction never overrides short-term risk gates.
* **Circuit Breaker 2 — Supply Cut vs. Peak Window Separation (`CB-02`):** Do not expect a secular cycle top in April 2028 itself. Block `1,050,000` cuts daily new supply from `~450 BTC` to `~225 BTC`; the structural supply deficit compounds over the following **12 to 18 months**, placing the primary `MOD 41` harvest window in **April 2029 – October 2029**.
* **Circuit Breaker 3 — Diminishing Return Realism (`CB-03`):** As Bitcoin's market capitalization scales past `$1.3T–$2.5T+`, percentage gains per halving epoch compress (`+684%` in `2020–2021` $\rightarrow$ `+97%` in `2024–2025`). Enforce `MOD 41` laddered profit-taking (`4 x 5%` tranches) inside realistic diminishing-return bands rather than holding through a `-54%` to `-77%` post-peak bear market.
* **Circuit Breaker 4 — Strict Barbell Firewall (`CB-04`):** Keep **Sleeve A (Active Exchange USDT/BTC Swing)** and **Sleeve B (`2-of-3` Dual-Jurisdiction Multi-Sig Cold Storage per `MOD 32`)** completely air-gapped. Sovereign UTXOs acquired at or below the prior-halving price floor (`~$64,000`) remain untouched until `MOD 41` Swing 1 / Swing 2 distribution zones in `2029`.

---

## 3. Core Conditional Signal Units (`Condition A -> Outcome B -> Rule C`)

### CSU-46A: Pre-Halving Prior-Epoch Valuation Reset (`T-24m` to `T-12m` Before Block `1,050,000`)
* **Trigger Condition A (The Telemetry Scan):**
  1. Bitcoin is `12 to 24 months` ahead of `Block 1,050,000` (e.g., late `2026` through `Q1 2027`) and retraces back to or below the **prior halving's price anchor (`~$64,000` Block `840,000` baseline)**.
  2. **Authentication:** Active calendar liquidity drains (`MOD 44` IPO/index deadlines) have cleared, US Spot BTC ETF 3-day flows flatten (`>= $0M`), and on-chain stress reaches generational discount zones (`STH-MVRV <= 0.85` per `MOD 13D`, `STH-SOPR` curling above `0.975` per `MOD 14 M8`, or `200W MA` proximity).
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Multi-year bear drawdown has erased post-halving speculative excess, pricing Bitcoin at or below its `2024` supply-cut baseline `~17 months` before the `2028` halving cuts new issuance in half again.
  * **Probable Trajectory:** Multi-month base-building (`2027`) transitioning into pre-halving markup (`late 2027 – Q1 2028`).
* **Execution Rule C (The Non-Negotiable Action):**
  * **Sleeve A (Tactical Swing):** Unlock `0.75%` spot risk on verified `4H VAH` reclaims (`MOD 37 Net R >= 3.0`).
  * **Sleeve B (Sovereign Vault):** Deploy pre-allocated **Sovereign Cold-Storage Tranches (`CSU-18D`)** via Domestic USD Spot gateways and sweep settled UTXOs into `2-of-3` multi-sig cold storage (`MOD 32 CSU-32C`, respecting the `72-Hour Operational Wall`).

### CSU-46B: Pre-Halving Countdown & Supply-Cut Transition (`T-6m` to `Block 1,050,000`)
* **Trigger Condition A (The Telemetry Scan):**
  1. Chain height crosses `Block 1,023,750` (`~6 months` / `~26,250 blocks` prior to `Block 1,050,000`, `Q4 2027 – April 2028`).
  2. `200D MA` slopes upward (`MOD 17A`), `Net Fed Liquidity` / `Global M2` is neutral-to-expanding (`MOD 22`), and `Hashprice` approaches pre-halving compression (`MOD 40`).
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Market front-runs the impending `50%` reduction in miner daily issuance (`450 -> 225 BTC/day`), often accompanied by a short-term "sell-the-news" shakeout around the exact halving block (`Block 1,050,000`).
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** Hold **Sleeve B (Sovereign Vault)** intact through any `Block 1,050,000` halving-week volatility; use `Sleeve A` (`0.75%` risk) to buy post-halving `15m/1H VAL` liquidity sweeps (`MOD 11A`) once funding resets.

### CSU-46C: Post-Halving Markup & Epoch 5 Harvest Window (`T+12m` to `T+18m` / `April–October 2029`)
* **Trigger Condition A (The Telemetry Scan):**
  1. Time elapsed since `Block 1,050,000` enters the **`12 to 18 month` historical peak window (`April 2029 – October 2029`)** AND price reclaims/exceeds the prior cycle ATH (`$126,200`, `MOD 41 M8`).
  2. Price enters `MOD 41` **Swing 1 (`$172k–$180k` Conservative / `$230k–$250k` Bull Stretch)** or **Swing 2 (`+1%` to `+6%` Flat Peak 2 band)**.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Cumulative daily supply deficit from the `1.5625 BTC` block subsidy collides with peak institutional/retail momentum, creating the terminal distribution cluster of Epoch 5.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** Hand off control directly to **`MOD 41` & `MOD 41.1`**—execute `4 x 5%` laddered profit-taking tranches into euphoria and enforce the **10-Day `Rule 1` (`-10.0%` daily UTC close)** hard exit before the next secular bear market.

---

## 4. Dynamic Regime Mutation Lookup Matrix (`M1` through `M6`)

| Mutation ID | Initial State | Telemetry Mutation Observed (`Condition A'`) | Mechanical Meaning (`Outcome B'`) | Mandatory Execution Override (`Rule C'`) |
| :--- | :--- | :--- | :--- | :--- |
| **M1: ETF-Accelerated Early Cycle Top** | Post-`Block 1,050,000` (`T+6m` to `T+11m`) | Massive US Spot ETF inflows (`> +$500M/day`) push BTC into `MOD 41` harvest targets (`$172k+`) *before* month 12, followed by a `+1%` to `+6%` flat double-top and `Rule 1` (`-10%` close). | Institutional front-running compressed the `12–18m` post-halving lag (similar to ETF-driven early highs). | **Do Not Wait for April 2029 Calendar Date:** Trigger `MOD 41` laddered distribution immediately when price + `Rule 1` signals fire. |
| **M2: Macro Liquidity Delay (`T+19m` to `T+24m`)** | `T+18m` (Oct 2029) | Global liquidity tightening (`MOD 22` / `MOD 24`) delays breakout past month 18, while `STH-MVRV` remains healthy (`1.0–1.25`) without a flat double-top breakdown. | Liquidity cycle lagged the halving schedule by 1–2 quarters (lengthening cycle variant). | **Trail Stops Behind `1D VAL` (`MOD 41 M1`);** let price structure—not calendar date alone—force final exit. |
| **M3: Post-Halving Miner Capitulation Dip** | `Block 1,050,000` + `1–60 Days` | Immediately after the subsidy drops to `1.5625 BTC`, inefficient miners capitulate (`MOD 40 CSU-40B`), causing a `-15%` to `-25%` shakeout before difficulty adjusts down. | Temporary post-halving supply indigestion before lower issuance tightens float. | **Deploy Tactical `0.75%` Spot Long (`MOD 40 M3`)** upon difficulty downward retarget + `USD Spot CVD` reclaim. |
| **M4: Deep Sub-Halving-Price Capitulation** | `CSU-46A` (`2026–2027` Bear) | Macro contagion (`MOD 29` / `MOD 44`) drives BTC `15%–25%` *below* the `$64,000` 2024 halving price (`~$48,000–$55,000`) alongside `LTH-SOPR < 1.0`. | Extreme generational discount below the previous halving's cost/valuation floor. | **Accelerate `Sleeve B` Sovereign Cold-Storage Tranches (`CSU-18D`)** once ETF outflows stop. |
| **M5: Short-Term Anchor Drift Warning** | Any Bear/Chop Week | Operator or external commentary anchors decisions to "last week's candle" or "last month's high" instead of `Block 1,050,000` vs. current discount. | Recency bias threatening premature capitulation at multi-year value floors. | **Print Horizon Reminder in `MOD 45` HUD:** *"Anchor = Block 1,050,000 (Apr 2028) vs. Today; Sleeve A Cash Lock protects timing, Sleeve B accumulates value."* |
| **M6: Sovereign Custody OpSec Gate** | Executing `CSU-46A` Tranche | Operator is traveling without laptop access (`Galaxy A55` only) when a Sovereign Cold-Storage tranche triggers. | Elevated mobile/network OpSec risk during multi-sig UTXO settlement (`MOD 32 M6`). | Accumulate on regulated USD Spot exchange first; **enforce `72-Hour Operational Wall`** until back at secure desktop quorum. |
