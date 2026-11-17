### PROJECT CORTEX-BTC — MODULE 63: CORTEX-RHYME EMPIRICAL DERIVATIVES STATE-SPACE ANALOGUE & EXPECTANCY ENGINE
**Waterfall Tier:** Pillar 1 & Pillar 4 Quantitative Prior Bridge (Base-Rate Conditioning, Tail-Asymmetry Auditing & Sizing Conviction Modulator) — harmonized with MOD 12 (Garman-Klass Volatility), MOD 18 (Master 5-Pillar Compiler & 0.75% Risk Sizing), MOD 33 (Unified 5-Regime Master Radar), MOD 36 (Telemetry Trust & Staleness SLA), MOD 37 (Executable Liquidity & Net-3.0R Slippage Governor), MOD 60 (7-Rank Veto Precedence Ladder), and MOD 62 (Dual-Inventory Bidirectional Swing Engine — DIBSE v2.0).
**Document Provenance:** Codified from `CORTEX-RHYME v1.1.0` (`aikeluargalee-tech/cortex-rhyme` open-source static edge telemetry engine).
**Governance Posture:** Non-Parametric Base-Rate Prior & Expectancy Auditor (Subordinate to MOD 60 Ranks 0–3 upstream vetoes; advisory input to Rank 4/5 MOD 18 & MOD 62 Portfolio Allocation Controller). Never acts as an autonomous buy/sell trigger.

--------------------------------------------------------------------------------

#### 0. CORTEX-BTC v7.1 HARMONIZATION & PRECEDENCE BRIDGE
```yaml
module_id: "MOD_63"
entry_type: "EMPIRICAL_STATE_SPACE_ANALOGUE_ENGINE"
waterfall_pillar: "PILLAR_1_TO_PILLAR_4_EXPECTANCY_PRIOR_BRIDGE"
title: "CORTEX-RHYME: Empirical Derivatives State-Space Analogue & Expectancy Engine"

# MOD 60 VETO PRECEDENCE REGISTRATION
governance_registration:
  mod_60_precedence_rank: "ADVISORY_PRIOR_TO_RANK_4_AND_RANK_5"
  upstream_veto_subordination: "Any MOD 60 Rank 0-3 veto (MOD 36 DATA HALT, MOD 16 GATE_RED, ICDM >= 60, MOD 44/58 Event Lock, or MOD 34/51 Active Cascade) immediately overrides MOD 63 -> NO TRADE / REMAIN CURRENT INVENTORY."
  standalone_trade_authorization: false # Strictly prohibited; feeds sizing & expectancy only

# STATE-SPACE VECTOR SPECIFICATION (5 ORTHOGONAL DIMENSIONS)
state_vector_schema:
  frequency: "1H_UTC_CLOSED_BARS"
  normalization: "CAUSAL_TRAILING_168H_Z_SCORE" # Zero future leakage [t-168, t]
  distance_metric: "REGULARIZED_MAHALANOBIS_5D" # Tikhonov ridge = 0.05; de-correlates funding & basis
  dimensions:
    - id: "z_funding"
      metric: "8H Perpetual Funding Rate"
      prior_scale: 1.15
    - id: "z_basis"
      metric: "Perp Mark vs. Spot Index Basis (bps)"
      prior_scale: 1.00
    - id: "z_oi_delta"
      metric: "24H Open Interest % Change"
      prior_scale: 1.15
    - id: "z_gk_vol"
      metric: "24H Annualized Garman-Klass Realized Volatility (MOD 12)"
      prior_scale: 1.00
    - id: "z_book_flow"
      metric: "Hourly Taker Buy/Sell Ratio + Live Top-20 L2 Skew"
      prior_scale: 1.10

# ANTI-PATHOLOGY SAFEGUARDS
statistical_guardrails:
  forward_embargo_hours: 72 # Excludes trailing 72h so all analogues have finalized outcomes
  declustering_min_gap_hours: 24 # Prevents adjacent hourly bars of one event from inflating N
  target_analogues_k: 20
  max_mahalanobis_radius: 2.65
  staleness_sla_hours: 2.5 # Aligned with MOD 36 freshness requirements

# SAMPLE QUALITY GRADING TIERS
quality_tiers:
  SOLID: "analogues_found >= 18 AND avg_vector_distance <= 1.65 AND history_days >= 90.0"
  MODERATE: "10 <= analogues_found < 18 OR 1.65 < avg_vector_distance <= 2.35 OR history_days < 90.0"
  THIN: "analogues_found < 10 OR avg_vector_distance > 2.35 -> ASSIGN ZERO ANALOGUE WEIGHT"
```

--------------------------------------------------------------------------------

### PART I — EPISTEMOLOGY & SYSTEM PURPOSE
#### Rule 1. Core Mandate
Spot price levels are non-stationary across macro cycles, whereas derivatives leverage mechanics, carry stress, volatility clustering, and order-book liquidity exhibit recurring structural behavior.
**MOD 63 (CORTEX-RHYME)** answers one empirical question before tactical capital is deployed:
> *"When Bitcoin's derivatives positioning, carry cost, volatility, and order-book flow looked statistically identical to the present hour, how did forward return distributions over +4h, +24h, and +72h deviate from unconditional background noise (`baseline_all_hours`)?"*

#### Rule 2. Strict Non-Prediction Doctrine
1. MOD 63 is **not** a directional price oracle and **never** issues standalone `ACCUMULATE` or `REDUCE` commands.
2. MOD 63 functions exclusively as a **Layer 1 Base-Rate Prior** within the 3-Layer Decision Hierarchy:
   - **Layer 1 — Base Rate Prior (MOD 63):** Establishes conditional return expectancy, directional win-rate lift ($\Delta\text{Up-Share}$), and tail-risk asymmetry.
   - **Layer 2 — Live Mechanism (MOD 01–30 / PCF3 / AEGIS-3):** Confirms active forcing functions (Spot CVD absorption, passive limit walls, liquidation cascades).
   - **Layer 3 — Hard Structure & Sizing (MOD 11 / MOD 18 / MOD 37 / MOD 62):** Defines structural invalidation, Net $R \ge 3.0$ geometry, and Sleeve A inventory allocation.

--------------------------------------------------------------------------------

### PART II — MATHEMATICAL & STATISTICAL SAFEGUARDS
#### Rule 3. Elimination of the Five Analogue Pathologies
To prevent false statistical confidence, any telemetry ingested from `cortex-rhyme` must enforce five mandatory constraints:
1. **Causal Rolling Standardization (Zero Lookahead):** Feature Z-scores must be calculated strictly over trailing $[t-168, t]$ windows. Future data must never enter mean or standard deviation denominators.
2. **Mahalanobis Covariance Whitening:** Because perpetual funding and perp-to-spot basis are strongly collinear, distances must be computed using the regularized inverse covariance matrix $\Sigma_{\text{causal}}^{-1}$ estimated strictly prior to the 72h embargo window, preventing carry stress from being double-counted.
3. **24-Hour De-Clustering:** Candidate matches are ranked by ascending Mahalanobis distance $D_M$. A candidate at hour $i$ is admitted only if $|i - j| \ge 24\text{ hours}$ for every already-selected analogue $j$, ensuring $k$ independent historical regimes rather than autocorrelated clones of a single event.
4. **72-Hour Forward Embargo:** All observations within 72 hours of `as_of_utc` are excluded from the candidate pool so every analogue carries a complete, finalized +4h, +24h, and +72h forward return vector.
5. **Baseline-Relative Conditioning:** Every conditional statistic (`after_similar_setups`) must be evaluated directly against the unconditional full-archive distribution (`baseline_all_hours`). Raw win rates without baseline lift (`up_share_lift_pts`) are invalid for decision support.

--------------------------------------------------------------------------------

### PART III — INTEGRATION WITH MOD 18 SIZING & MOD 62 (DIBSE v2.0)
#### Rule 4. Sample Quality Gating
- **`THIN` Grade ($N < 10$ or $\bar{D}_M > 2.35$):** Indicates an unprecedented structural outlier or macro shock lacking historical precedent. MOD 63 assigns **0.0x sizing modifier** (neutral/no-opinion). Neither Loop A nor Loop B may cite a `THIN` readout to justify a trade.
- **`MODERATE` Grade:** May serve as supporting context only when aligned with Pillar 2/3 live order-flow confirmation.
- **`SOLID` Grade ($N \ge 18$, $\bar{D}_M \le 1.65$, $\text{history\_days} \ge 90$):** Eligible to modulate sizing conviction within MOD 18 and MOD 62 risk ceilings.

#### Rule 5. Tail-Asymmetry & Net-3.0R Veto Check
MOD 63 reports `median_up_pct` (median gain when $R > 0$) separately from `median_down_pct` (median loss when $R < 0$) and computes `tail_skew_ratio = |median_up_pct / median_down_pct|`.
- **Asymmetric Cliff Alert:** Even when `up_share` sits near 50%, if `tail_skew_ratio < 0.40` on the 24h or 72h horizon (indicating severe historical downside tail risk relative to modest upside), MOD 62's Portfolio Allocation Controller must tighten Loop A accumulation requirements and verify that hard structural stops (MOD 11/54) strictly preserve **Net $R \ge 3.0$** after MOD 37 slippage.
- **DIBSE Loop Alignment:**
  - **Loop A (`USDT → BTC → USDT`):** Favored when `sample_quality == SOLID`, 24h/72h `up_share_lift_pts >= +10.0 pts`, and `tail_skew_ratio >= 1.0` alongside confirmed spot absorption (MOD 05/06).
  - **Loop B (`BTC → USDT → BTC`):** Favored when `sample_quality == SOLID`, 24h/72h `up_share_lift_pts <= -10.0 pts` (or severe downside tail skew), and Pillar 2/3 distribution signals (MOD 02B/06B/13C) are active.

#### Rule 6. Data Integrity & Staleness SLA (MOD 36 Bridge)
- If `meta.status != "live"`, `as_of_utc` exceeds **2.5 hours** of staleness, or the endpoint is unreachable, MOD 63 transitions to **`UNAVAILABLE / STALE`** and contributes zero weight. Per MOD 36, stale advisory telemetry does not halt valid primary venue feeds unless primary hub quorum fails, but fabricated or estimated analogue numbers are strictly prohibited.

--------------------------------------------------------------------------------

### FINAL DIRECTIVE
**MOD 63 measures how loaded the historical spring is—never whether the trigger has been pulled. Base rates inform sizing and asymmetry; live order flow and hard structure govern execution.**
