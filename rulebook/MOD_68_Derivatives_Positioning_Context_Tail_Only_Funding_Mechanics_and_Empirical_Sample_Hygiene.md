##### PROJECT CORTEX-BTC — MODULE 68: DERIVATIVES POSITIONING CONTEXT, TAIL-ONLY FUNDING MECHANICS & EMPIRICAL SAMPLE HYGIENE
**Waterfall Tier:** Pillar 3 & Tier D Bridge (Context-Only Leverage Crowding Taxonomy, Exchange Formula Clamp Hygiene & 4-Rule Statistical Validation Governor) — harmonized with **MOD 01** (Rising OI + Extreme Negative Basis), **MOD 02** (Crowded Positive Basis), **MOD 03** (Deleveraging Flushes & OI Resets), **MOD 04** (Funding Velocity & Venue Spreads), **MOD 05** (Spot vs. Perp CVD), **MOD 31** (ICDM Fragility Scale), **MOD 42.1** (BTC-Denominated OI Rulebook 3.2), **MOD 52** (Rolling 30-Trade Expectancy Audit), **MOD 60** (7-Rank Veto Precedence Ladder), **MOD 62** (DIBSE v2.0), and **MOD 65** (Media De-Noising & Signal Hygiene).
**Document Provenance:** Codified from `funding-rates-and-open-interest.md` (*Funding Rates and Open Interest: Reading the Leverage Crowd*, Nov 2026 empirical audit) and corrected against official Binance/OKX perpetual funding-rate specifications (including the fixed `+0.01%/8h` interest-rate clamp and May 2025 / Jan 2026 dynamic settlement-interval updates).
**Governance Posture:** Context-Only Derivatives Crowding & Empirical Validation Governor. **Zero standalone trade authorization.** Enforces strict separation between linear sentiment folklore and true tail-only leverage mechanics, prevents small-sample or overlapping-window overfitting, and corrects exchange formula distortions before any positioning metric enters Pillar 3 or `ctc_backtest_lab` research.

--------------------------------------------------------------------------------

###### 1. Machine-Readable State & Routing Block (Python / Hermes / NotebookLM Index)
```yaml
module_id: "MOD_68"
entry_type: "DERIVATIVES_CONTEXT_AND_SAMPLE_HYGIENE_GOVERNOR"
waterfall_pillar: "PILLAR_3_AND_TIER_D_POSITIONING_HYGIENE"
title: "Derivatives Positioning Context, Tail-Only Funding Mechanics & Empirical Sample Hygiene"

# MOD 60 PRECEDENCE & EXECUTION BOUNDARY
governance_registration:
  mod_60_precedence_rank: "PILLAR_3_CONTEXT_AND_TIER_D_VALIDATION_FILTER"
  standalone_trade_authorization: false # Positioning is CONTEXT ONLY; never a standalone buy/sell trigger
  upstream_veto_subordination: "NEVER overrides MOD 60 Ranks 0-3 (MOD 36 DATA HALT, MOD 16 GATE_RED, ICDM >= 60, MOD 44/58 Event Lock, or MOD 34/51 Active Cascade)."

# SINGLE-SAMPLE EMPIRICAL REFERENCE BENCHMARKS (NOT UNIVERSAL LAWS)
single_sample_benchmarks:
  daily_btcusdt_sample:
    window: "2019-09 to 2026-10"
    total_observations_n: 2587
    rank_ic_funding_vs_7d_return: -0.047 # Tail signal, not a linear scale
    extreme_negative_daily_band_lt_neg0_01pct: {n: 146, mean_7d_pct: 4.68, median_7d_pct: 2.95, hit_rate_pct: 66.4, distinct_crash_episodes: 4}
    mid_and_positive_bands: "Indistinguishable from base-rate coin flip (49.5%-55.1% hit rates); >+0.03%/day bucket (n=1041, 40.3%) is distorted by Binance +0.01%/8h clamp"
  non_overlapping_weekly_sample:
    window: "2021-01 to 2026-09"
    total_observations_n: 299
    crowded_shorts_neg_funding_rising_oi: {n: 18, mean_7d_pct: 3.05, median_7d_pct: 3.55, hit_rate_pct: 72.0, ci_95_pct: [50, 87], mean_14d_pct: 3.03}
    positions_leaving_neg_funding_falling_oi: {n: 18, mean_7d_pct: 1.80, median_7d_pct: -0.06, hit_rate_pct: 50.0, mean_14d_pct: 3.35}
    crowded_longs_pos_funding_rising_oi: {n: 156, mean_7d_pct: 0.33, median_7d_pct: 0.02, hit_rate_pct: 50.0, mean_14d_pct: 1.37}
    quiet_deleveraging_pos_funding_falling_oi: {n: 107, mean_7d_pct: 0.25, median_7d_pct: 0.03, hit_rate_pct: 50.0, mean_14d_pct: 0.12}

# EXCHANGE FORMULA & NORMALIZATION CONSTANTS
exchange_mechanics_guards:
  binance_okx_interest_rate_8h_pct: 0.01 # Fixed 0.03%/day (10.95% simple APR); NOT zero-centered
  binance_clamp_band_pct: [-0.05, 0.05] # Average premium in [-0.04%, +0.06%] prints flat +0.01%/8h
  dynamic_settlement_clock_break: "2025-05 hourly escalation & 2026-01 reversion rules (do not mix raw per-period prints across regimes without realized daily summation)"
  oi_denomination_mandatory: "BTC_CONTRACTS_ONLY" # Prevents USD price-inflation distortion (MOD 42.1 Rulebook 3.2)
  symmetric_tail_quantiles: [0.05, 0.95] # Required for valid upper-vs-lower tail testing

# 4-RULE EMPIRICAL SAMPLE HYGIENE CONSTANTS (HARMONIZED WITH MOD 52 CB-05 & MOD 65 CB-06)
sample_hygiene_rules:
  r1_denominator_and_ci: "Mandatory n/N + 95% confidence interval reporting"
  r2_overlap_correction: "Use non-overlapping intervals OR divide effective sample size by overlap horizon k (uncertainty inflated ~sqrt(k))"
  r3_episode_clustering: "Count distinct independent market episodes rather than raw consecutive crash days"
  r4_ev_and_regime_split: "EV_unit_risk = (up_fraction * gain_drop_ratio) - (1 - up_fraction), conditioned on >200D vs <200D SMA"

# RISK & SIZING CONSTANTS (PILLAR 4)
risk_parameters:
  sizing_from_funding_alone_pct: 0.00 # Strictly prohibited; use for confidence/patience calibration only
  leverage_permitted: 1.0 # Strict Unleveraged Spot Only
```

--------------------------------------------------------------------------------

###### 2. Protective Circuit Breakers (Mandatory Positioning & Empirical Invariants)
*   **Circuit Breaker 1 — Tail-Not-Scale & Context-Only Law (CB-01):** Perpetual funding has near-zero linear rank correlation with forward returns (`IC ≈ -0.047` across 2,587 daily BTCUSDT bars). Mid-range funding prints (including mild negative rates such as `-0.002%` to `-0.007%/8h`) sit inside a coin-flip noise band. Funding is strictly a **tail-only context condition**—never a sentiment slider and never a standalone spot entry or position-sizing trigger.
*   **Circuit Breaker 2 — Mandatory 2×2 Funding × BTC-Denominated OI Split (CB-02):** Never quote funding as a single scalar without pairing it with **Open Interest direction measured in BTC contracts** (never USD notional, which mechanically inflates with rising price per `MOD 42.1` Rulebook 3.2). Negative funding + rising BTC OI (*Crowded Shorts*: trapped bears paying to stay short) and negative funding + falling BTC OI (*Positions Leaving*: an empty room with no forced buyers) have opposite mechanical trajectories.
*   **Circuit Breaker 3 — Exchange Formula Clamp & Clock-Shift Guard (CB-03):** Standard perpetual formulas on Binance and OKX embed a fixed `+0.01%/8h` (`+0.03%/day`, `10.95%` simple APR) interest-rate component with a `±0.05%` clamp, flattening any average premium between `-0.04%` and `+0.06%` to exactly `+0.01%/8h`. Consequently:
    1. A daily bucket labeled `> +0.03%/day` captures **~40%+** of all days and is **NOT** an extreme upper tail; valid upper-tail testing requires symmetric empirical quantiles (e.g., rolling `>= 90th–95th` percentile or `> +0.035%/8h` per `MOD 04`).
    2. Because venues introduced dynamic hourly settlement escalation (Binance May 2025 / Jan 2026 reversion rules), aggregate historical funding by **realized daily sum** rather than multiplying raw per-period prints by `1,095`.
*   **Circuit Breaker 4 — Spot-Blindness, Passive Long-Trap & Basis-Arb Filter (CB-04):** Perpetual funding cannot see unleveraged spot flows. Before treating `Negative Funding + Rising OI` as bullish squeeze fuel, verify **Domestic USD Spot CVD (`MOD 05` / `MOD 07` / `MOD 19`)** to rule out a **`MOD 01 CSU-01B` Passive Long-Trap Cascade** or **`M5` Short-Pile-On Breakdown**. Likewise, distinguish directional crowded longs from institutional delta-neutral Spot ETF / short-perp basis arbitrage (`MOD 04 M7`).
*   **Circuit Breaker 5 — 4-Rule Empirical Sample Hygiene Gate (CB-05):** Any positioning research, backtest, or media claim must report: (1) exact denominator $n/N$ and 95% CI width (`n = 18` at `72%` spans `50%–87%`, too wide for sizing); (2) non-overlapping horizons or `~sqrt(k)` overlap discounting; (3) distinct cluster episodes (`146` tail days = `~4` crashes); and (4) payoff-adjusted $\text{EV}_{\text{unit risk}}$ split by trend regime (`>200D` vs. `<200D` SMA). Cross-locked with **`MOD 52 CB-05`** and **`MOD 65 CB-06`**.
*   **Circuit Breaker 6 — Upstream Veto Subordination (CB-06):** Even a genuine extreme `Crowded Shorts` tail state has **0.00% execution authority** while `MOD 60` Ranks 0–3 (`MOD 36 DATA HALT`, `MOD 16 GATE_RED`, `MOD 31 ICDM >= 60`, `MOD 44` calendar lock, or `MOD 64` shadow-credit stress) remain active.

--------------------------------------------------------------------------------

###### 3. Core Conditional Signal Units (Condition A -> Outcome B -> Rule C)
###### CSU-68A: Qualified Crowded-Shorts Context ("Tail Squeeze Fuel — Context Only")
*   **Trigger Condition A (The Telemetry Scan):**
    1. Realized daily OI-weighted funding falls into the **bottom 5th percentile** (`< -0.01%/day` or `<= -0.015%/8h` across multi-venue composite, `MOD 04 CB-02`).
    2. **BTC-denominated Open Interest** is **rising** (confirming new shorts opening and paying to stay short, not old positions closing).
    3. **Spot & Macro Gate Verification:** `MOD 60` Ranks 0–3 are clear (`ICDM < 55`, non-`GATE_RED`) **AND** Domestic USD Spot CVD (`MOD 05`) prints absorption/higher lows at HTF structural support (`MOD 11` / `MOD 54`).
*   **Observed Outcome B (The Mechanical Trajectory):**
    *   **Microstructure Lens:** Short positioning is genuinely crowded at an extreme tail (`72%` hit rate in the 2021–2026 weekly reference sample, `n = 18`, 95% CI `50%–87%`), creating asymmetric forced-cover fuel if price reclaims structure.
*   **Execution Rule C (The Non-Negotiable Action):**
    *   **Action:** **ELEVATE WATCH PRIORITY — DO NOT SIZE FROM FUNDING ALONE.** Pass qualified context to **`MOD 01` (`CSU-01A`)**, **`MOD 18`**, and **`MOD 62`** (Loop A) to await a closed-bar 1H/4H VAL/POC reclaim with **Net R >= 3.0** and standard risk caps (`<= 0.375%` Amber / `<= 0.75%` Green).

###### CSU-68B: Empty-Room Trap Quarantine ("Negative Funding + Falling OI")
*   **Trigger Condition A (The Telemetry Scan):**
    1. Perpetual funding turns negative (`< 0.00%`), **AND**
    2. **BTC-denominated Open Interest is falling** across 24h–7d windows (old leveraged positions closing/draining out).
*   **Observed Outcome B (The Mechanical Trajectory):**
    *   **Microstructure Lens:** Market is in the **Positions Leaving** state (`50%` hit rate / `-0.06%` median 7d return in the weekly reference sample)—there are no trapped shorts left to fuel a mechanical short squeeze.
*   **Execution Rule C (The Non-Negotiable Action):**
    *   **Action:** **QUARANTINE SQUEEZE NARRATIVE; STAND DOWN.** Do not deploy Sleeve A USDT on "negative funding = bounce" slogans; evaluate price strictly via **`MOD 03` (`CSU-03D`)** voluntary unwind + **`MOD 11`** Volume Profile + **`MOD 05`** Spot CVD.

###### CSU-68C: Symmetric Upper-Tail Crowded-Long Fragility Filter ("True Blow-Off Overhang")
*   **Trigger Condition A (The Telemetry Scan):**
    1. OI-weighted funding breaks cleanly **above** the Binance/OKX `+0.01%/8h` (`+0.03%/day`) clamped plateau into the **top 5th–10th rolling percentile** (`>= +0.030% to +0.035%/8h` / `>= +0.09% to +0.105%/day`).
    2. **BTC-denominated Open Interest** is expanding rapidly (`>= +5%` over 48h–7d) while **Domestic USD Spot CVD flattens or diverges negatively** (`MOD 42.1` Rulebook 3.1/3.2).
*   **Observed Outcome B (The Mechanical Trajectory):**
    *   **Microstructure Lens:** Eliminates the `+0.03%/day` clamp dilution error and isolates genuine directional long crowding where upside rallies are fragile and downside liquidation cascades accelerate rapidly.
*   **Execution Rule C (The Non-Negotiable Action):**
    *   **Action:** **BLOCK NEW SLEEVE A LONG ADDITIONS (`MOD 02` / `MOD 04 CSU-04C`).** Tighten trailing stops on open Loop A longs and authorize **Loop B (`BTC -> USDT`)** defensive profit-taking (`MOD 18` Stage 1 / `MOD 62` Rule 18) upon closed-bar rejection at HTF resistance.

###### CSU-68D: Statistical Claim & Backtest Rejection ("Thin-Sample / Formula-Flawed Study")
*   **Trigger Condition A (The Telemetry Scan):**
    1. An external article, indicator pitch, or internal `ctc_backtest_lab` candidate cites a derivatives/positioning edge while failing any item of the **4-Rule Empirical Sample Hygiene Gate** (missing denominator/CI, uncorrected overlapping forward returns, clustered episodes treated as independent $N$, hit rate without EV/regime split, or unadjusted `+0.01%/8h` clamp / USD OI).
*   **Observed Outcome B (The Mechanical Trajectory):**
    *   **Governance Risk:** False statistical precision leads to curve-fitted parameters and oversized bets on thin tail samples (`n < 20`).
*   **Execution Rule C (The Non-Negotiable Action):**
    *   **Action:** **REJECT FOR PRODUCTION DEPLOYMENT (`0.00%` Weight).** Log the flaw in **`00H` Section 4** (`MOD 65 CB-06`) and require a strictly causal, non-overlapping, symmetric-quantile re-test under **`MOD 52 CB-05`** before re-evaluation.

--------------------------------------------------------------------------------

###### 4. Dynamic Regime Mutation Lookup Matrix (M1 through M6)
| Mutation ID | Initial State | Telemetry Mutation Observed (Condition A') | Mechanical Meaning (Outcome B') | Mandatory Execution Override (Rule C') |
| ------ | ------ | ------ | ------ | ------ |
| **M1: Mild-Negative Noise Mirage** | Watchlist Alert | Funding dips to `-0.002%` to `-0.008%/8h` on offshore venues while Binance/Coinbase hover near `0.000%` to `+0.003%`. | Inside the coin-flip noise band (`IC ≈ -0.047`), not an extreme crowded-short tail. | **Ignore Squeeze Narrative;** assign `0.00%` bullish weight (CB-01). |
| **M2: Crowded Shorts -> Passive Long Trap** | CSU-68A (Neg Funding + Rising OI) | Price breaks 4H VAL while **Domestic USD Spot CVD turns steeply negative** and ETFs print outflows. | Rising OI reflects offshore passive knife-catchers or aggressive momentum shorts overwhelming absent spot bids (`MOD 01 CSU-01B` / `M5`). | **Abort Squeeze Watch; Enforce 100% Cash Lock** until `MOD 03` full OI flush completes. |
| **M3: Clamp-Plateau False Calm** | Routine Scan | Binance BTCUSDT prints flat `+0.0100%/8h` for days while intraday perp premium swings between `-0.035%` and `+0.055%`. | Formula clamp (`±0.05%`) is censoring real basis shifts inside the plateau (CB-03). | **Read Raw Perp-vs-Spot Basis & Spot/Perp CVD (`MOD 05`) directly** instead of clamped funding prints. |
| **M4: Settlement-Clock Regime Break** | Historical Backtest | Backtest pools pre-May 2025 8h funding prints with post-May 2025 hourly-escalated cap prints using a fixed `×1,095` annualizer. | Mixed clock mechanics distort historical tail percentiles and APR comparisons (CB-03). | **Re-aggregate via Realized Daily Funding Sum** (`sum(period_rates_in_utc_day)`) across all backtests. |
| **M5: Cash-and-Carry Basis Arb Mirage** | Elevated OI + Positive Funding | BTC OI and positive funding rise steadily while **US Spot ETF inflows surge** and CME/dated basis stays orderly (`+8%–12%` APR). | Institutional delta-neutral basis carry (long Spot ETF / short Perp), not fragile retail leverage (`MOD 04 M7`). | **Do Not Treat as Crowded-Long Top;** require Spot CVD breakdown + `>95th` pct funding before Loop B exit. |
| **M6: Upstream Veto Override During Tail** | CSU-68A (Extreme Neg Tail) | Genuine crowded-short tail prints while `MOD 31 ICDM >= 60`, `MOD 64` credit stress, or `MOD 29` equity contagion is active (`GATE_RED`). | Macro liquidity drain overrides local derivatives positioning. | **Enforce `GATE_RED_100_CASH_LOCK` (CB-06);** log context in `00H` without deploying Sleeve A USDT. |

--------------------------------------------------------------------------------

###### 5. Operational Reference Tables (2×2 State Matrix & 4-Rule Audit Gate)
**Table A — The 2×2 Funding × BTC-Denominated OI Context Matrix (Context Only)**
| Market State | Realized Funding | BTC-Denominated OI | Mechanical Meaning | CoreTex Action Posture |
| ------ | ------ | ------ | ------ | ------ |
| **Crowded Shorts** | Extreme Negative (`< 5th` pct) | **Rising** | New shorts opening and paying to stay short | **Watchlist Priority** — Pass to `MOD 01` / `MOD 05` Spot CVD & `MOD 60` gates (`CSU-68A`). |
| **Positions Leaving** | Negative | **Falling** | Old leveraged positions closing ("empty room") | **Stand Down** — Zero squeeze fuel (`CSU-68B`); wait for `MOD 03D` / `MOD 11` base. |
| **Crowded Longs (True Upper Tail)** | Extreme Positive (`> 95th` pct, above `+0.01%/8h` clamp) | **Rising** | Fragile leveraged bulls paying high carry | **Block New Longs** — Tighten stops / screen Loop B distribution (`CSU-68C`). |
| **Quiet Deleveraging** | Positive / Neutral | **Falling** | Voluntary leverage drain, no directional conviction | **Baseline Noise** — Defer to `MOD 03D` time-bleed + `MOD 11` Volume Profile. |

**Table B — Mandatory 4-Rule Empirical Sample Hygiene Audit (`MOD 52` / `MOD 65` / `MOD 68`)**
| Audit Rule | Diagnostic Formula / Check | Minimum CoreTex Standard |
| ------ | ------ | ------ |
| **1. Denominator & CI** | Report `n / N` and 95% confidence interval width | Never size positions off small-sample tails (e.g., `n = 18` → `50%–87%` CI). |
| **2. Overlap Correction** | Sample non-overlapping bars or discount effective $N$ by overlap $k$ (`~sqrt(k)`) | Prohibit raw daily overlapping 7d return counts as independent proofs. |
| **3. Cluster-Episode Count** | Collapse consecutive tail days into distinct market episodes | Distinguish `146` daily tail rows from `4` independent crash episodes. |
| **4. Payoff EV & Regime Split** | $\text{EV}_{\text{unit risk}} = (\text{up\_fraction} \times \text{gain\_drop\_ratio}) - (1 - \text{up\_fraction})$ | Require positive post-slippage `E[R]` stratified across `>200D` vs. `<200D` SMA. |

--------------------------------------------------------------------------------

###### FINAL DIRECTIVE
**MOD 68 keeps leverage telemetry honest: perpetual funding is a censored, tail-only context signal—never a linear sentiment score, never a standalone trigger, and never stronger than its denominator, its exchange clamp formula, or the underlying Domestic USD Spot CVD.**
