# PROJECT CORTEX-BTC — MODULE 31: INSTITUTIONAL CAPITAL DEFENSE MATRIX (ICDM 100-POINT FRAGILITY SCALE)
**Waterfall Tier:** Cross-Pillar Quantitative Crash-Risk Scoring Rubric (0–100 Point Deterministic Fragility Gauge) governing Pillar 4 Capital Allocation.
**Provenance & Empirical Benchmark Anchor:** Upgraded from Master Log **Entry #37** (`03_Entry #37: Institutional Capital Defense Matrix`) — Quantifying structural market fragility across four weighted 25-point pillars (`Max = 100 Points`), where an aggregate score **`>= 60`** automatically enforces a system-wide **`100% CASH LOCK`**.

---

## 1. Machine-Readable State & Routing Block (Python / Hermes / NotebookLM Index)

```yaml
module_id: "MOD_31"
entry_type: "QUANTITATIVE_FRAGILITY_SCORECARD"
waterfall_pillar: "PILLAR_1_TO_5_ICDM_100PT_SCALE"
title: "Institutional Capital Defense Matrix (ICDM 100-Point Fragility Scale)"

# MASTER SCORING THRESHOLDS (0 TO 100 POINTS)
icdm_score_thresholds:
  LOW_FRAGILITY_GREEN: "0 to 35 points -> Standard 1.0x Spot Swing Allocation (Full 0.75% Portfolio Risk Ceiling)"
  ELEVATED_VULNERABILITY_AMBER: "36 to 59 points -> Reduced 0.25x to 0.50x Spot Size (Max 0.375% Risk; Staged Limit Orders Only; Zero Breakout Buying)"
  SYSTEMIC_CRASH_THREAT_RED: ">= 60 points -> MANDATORY 100% CASH LOCK (0.00% Risk; Zero Market Buy Orders)"

# FOUR 25-POINT SCORING VECTORS (TOTAL = 100 PTS)
scoring_vectors:
  vector_1_macro_cost_of_capital_max_25:
    us_10y_real_nominal_yield: "10 pts if US 10Y > 4.85% (or TIPS > 2.2%); 5 pts if 4.50%-4.85%; 0 pts if < 4.50%"
    dxy_momentum: "8 pts if DXY > 104.5 & rising above 50D EMA (ADX > 25); 4 pts if 102.5-104.5; 0 pts if < 102.5"
    credit_equity_derisking: "7 pts if HYG/LQD breaks support or NDX drops > 5% in 10d; 0 pts if tight"
  vector_2_structural_liquidity_vacuum_max_25:
    etf_net_flows: "10 pts if 5D US Spot ETF flows < -$250M AND YTD flows invert negative; 5 pts if 0 to +$250M; 0 pts if sustained inflows"
    coinbase_premium_inversion: "8 pts if Coinbase Premium < -0.05% for > 48h; 0 pts if positive"
    orderbook_bbo_skew: "7 pts if +/-2% Best Bid vs Best Ask depth ratio < 0.70 (asks outweigh bids > 1.4x); 0 pts if balanced"
  vector_3_derivatives_asymmetry_max_25:
    liquidation_density_ratio: "10 pts if downside long liq notional (-5%) exceeds upside short liq (+5%) by > 2.5:1; 5 pts if 1.5-2.5; 0 pts if short-heavy"
    funding_neutrality_breakdown: "8 pts if funding stays >= 0.00% during support breakdown; 0 pts if deeply negative (< -0.02%)"
    whale_positioning_ratio: "7 pts if top trader/whale net short notional exceeds long notional by > 1.8:1; 0 pts if balanced"
  vector_4_onchain_cohort_friction_max_25:
    sth_cost_basis_breach: "10 pts if Spot < STH Realized Price (STH-MVRV < 1.00); 0 pts if above"
    sth_sopr_inversion: "8 pts if STH-SOPR < 0.98 for 3 consecutive days; 0 pts if > 1.00"
    ma_200d_failure_proximity: "7 pts if Spot is below or within 2.5% of 200D SMA after losing 200D EMA; 0 pts if > 6% above"

# RISK & SIZING CONSTANTS (PILLAR 4)
risk_parameters:
  max_portfolio_risk_pct: 0.75
  amber_reduced_risk_pct: 0.375
  red_lock_risk_pct: 0.00
  leverage_permitted: 1.0 # Strict Unleveraged Spot Only
```

---

## 2. Live Empirical Calibration Proof (November 13, 2026 ICDM Audit)

Applying the **ICDM 100-Point Fragility Scale** to today's live market demonstrates its exact precision:
* **Vector 1 (Macro Drain):** US 10Y at `5.129%` (**10 pts**) + DXY at `103.2` (**4 pts**) + Credit/Rate volatility (**5 pts**) = **19 / 25 pts**.
* **Vector 2 (Liquidity Vacuum):** 5D ETF outflows at `-$1.44B` (**10 pts**) + Coinbase Premium at `-0.13%` for 49 days (**8 pts**) + Thin `$72M` skewed book (**7 pts**) = **25 / 25 pts**.
* **Vector 3 (Derivatives Asymmetry):** Heavy long liquidation cascade (**5 pts**) + Funding only flipping negative *after* the break (**4 pts**) + Whale short skew (**5 pts**) = **14 / 25 pts**.
* **Vector 4 (On-Chain Cohort Friction):** Spot (`~$68.7K`) below STH Realized Price (`$75.6K`) (**10 pts**) + STH-SOPR `< 0.98` (**8 pts**) + Below 200D MA (**7 pts**) = **25 / 25 pts**.
* **Total Live ICDM Score:** **`83 / 100 Points` (`>= 60` Threshold) $\rightarrow$ AUTOMATIC `100% CASH LOCK`**.

---

## 3. Core Conditional Signal Units (`Condition A -> Outcome B -> Rule C`)

### CSU-31A: Low Fragility / Robust Bids (`ICDM Score = 0 to 35 Points`)
* **Trigger Condition A (The Telemetry Scan):**
  1. Aggregate ICDM score across all four 25-point vectors computes between **`0` and `35` points** (`yields < 4.50%`, `positive ETF inflows & Coinbase Premium`, `balanced/short-heavy liquidation map`, and `Spot > STH Realized Price & 200D SMA`).
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Deep structural bid cushions across macro, institutional ETFs, order books, and on-chain cost basis.
  * **Probable Trajectory:** High-resilience bull trend where minor pullbacks are rapidly absorbed.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **AUTHORIZE STANDARD `1.0x` SPOT SWING ALLOCATION (`Full 0.75% Portfolio Risk Ceiling`).** Buy structural dips (`MOD 10B / 11A / 13A`) and trail Stage 2 runners.

### CSU-31B: Elevated Vulnerability (`ICDM Score = 36 to 59 Points`)
* **Trigger Condition A (The Telemetry Scan):**
  1. Aggregate ICDM score computes between **`36` and `59` points** (e.g., macro yields elevated at `4.65%` or STH cost basis under pressure, while ETF flows or order-book depth remain mixed).
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Asymmetric air-pocket risk is building beneath the surface; chasing market breakouts carries negative expectancy.
  * **Probable Trajectory:** Choppy two-way volatility with sharp stop-hunt sweeps below support before recoveries.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **CAP EXPOSURE AT `0.25x` TO `0.50x` SPOT SIZE (`Max 0.375% Portfolio Risk`).** Strictly ban market breakout buying; use staged limit orders *only* at confirmed HTF VAL liquidity shelves (`MOD 11A`).

### CSU-31C: Systemic Crash Threat (`ICDM Score >= 60 Points`)
* **Trigger Condition A (The Telemetry Scan):**
  1. Aggregate ICDM score reaches or exceeds **`60 / 100 Points`** (multi-pillar convergence of sovereign yield/DXY drain, ETF/Coinbase buyer strike, long-heavy liquidation asymmetry, and underwater STH cohorts).
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Structural buyer strike combined with forced cross-asset and derivatives deleveraging.
  * **Probable Trajectory:** High-velocity cascading drawdowns (`-15% to -35%+`) and failed dead-cat bounces.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **MANDATORY SYSTEM-WIDE `100% CASH LOCK` (`0.00% Risk Deployed`).** Zero market buy orders. Exception: small exploratory resting bids *only* at multi-year historical volume shelves (`200W MA`), cut immediately to cash if a daily candle closes below invalidation.

---

## 4. Dynamic Regime Mutation Lookup Matrix (`M1` through `M8`)

| Mutation ID | Initial State | Telemetry Mutation Observed (`Condition A'`) | Mechanical Meaning (`Outcome B'`) | Mandatory Execution Override (`Rule C'`) |
| :--- | :--- | :--- | :--- | :--- |
| **M1: Score Crosses 60 Tripwire** | `CSU-31B` (`Score 52`) | ETF outflows accelerate (`-$300M`) and Spot loses STH Realized Price, pushing **ICDM Score from `52` to `68`**. | Fragility crossed the critical systemic threshold mid-week. | **Immediate Kill-Switch:** Exit any open `0.375%` tactical swing at market and enforce **100% Cash Lock**. |
| **M2: Score Drops Below 55 De-Escalation** | `CSU-31C` (`Score 83`) | 10Y yields cool (`< 4.80%`), ETF outflows halt, and Coinbase Premium turns positive—dropping **ICDM Score from `83` to `48`**. | Structural buyer strike and macro drain have subsided below crash threshold. | Lift `100% Cash Lock`; transition to `CSU-31B` (`0.375% Risk` staged limit reclaims). |
| **M3: Single-Pillar 25/25 Max-Out** | `CSU-31B` (`Score 45`) | Total score is `45`, **but Vector 2 (Liquidity Vacuum) hits `25 / 25` max points** (`massive ETF outflows + thin book`). | Acute spot liquidity vacuum can trigger a flash drop even before macro/on-chain lag catches up. | **Treat as Effective `Score >= 60` (`100% Cash Lock`)** until Vector 2 drops below `15/25`. |
| **M4: Post-Flush Vector 3 Reset** | `CSU-31C` (`Score 75`) | After a `$1.4B` liquidation cascade, Vector 3 drops from `22/25` down to `4/25` (`shorts now crowded, longs wiped out`), lowering score to `56`. | Derivatives asymmetry flipped from downside fuel to upside squeeze fuel. | Authorize tactical `CSU-31B` (`0.375%`) VAL reclaim entry with strict `R >= 3.0` filter. |
| **M5: Return to Low-Fragility Bull** | `CSU-31B` (`Score 42`) | Spot reclaims `200D SMA` and `STH Realized Price` (`Vector 4 -> 0/25`), dropping total **ICDM Score below `35`**. | Full multi-pillar structural health restored. | **Promote to `CSU-31A` (`Full 0.75% Risk Ceiling`)**. |
| **M6: Stealth Score Creep** | `CSU-31A` (`Score 24`) | Price is still making marginal highs, **but ICDM Score creeps from `24` up to `44`** (Coinbase Premium inverting + BBO bid skew dropping). | Hidden deterioration beneath calm surface price (`divergent fragility`). | **Bank Stage 1 (50%) Profit** and tighten stops ahead of visible price breakdown. |
| **M7: Data-Absence Conservative Penalty** | Daily Telemetry Scan | One or more ICDM sub-metrics are temporarily unavailable in the live feed. | Under zero-hallucination rules, missing telemetry cannot be assumed bullish (`0 pts`). | Assign **50% neutral-caution points** to any missing sub-metric until verified data arrives. |
| **M8: Daily ICDM Audit Logging** | Routine Daily Ops | Compute exact `0–100` ICDM score alongside `MOD 18` Waterfall every session. | Tracks directional fragility velocity (`Delta_ICDM` 24H/7D) in addition to static score. | If `ICDM` rises by **`+15 points` in 48 hours**, automatically reduce risk tier by one level. |
