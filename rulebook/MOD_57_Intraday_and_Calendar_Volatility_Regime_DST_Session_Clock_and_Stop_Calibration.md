# PROJECT CORTEX-BTC BRAIN — MODULE 57: INTRADAY & CALENDAR VOLATILITY REGIME, DST SESSION CLOCK & EMPIRICAL STOP-CALIBRATION ENGINE

**Waterfall Tier:** Pillar 2 & Pillar 4 Bridge (Temporal Microstructure, Volatility Clustering & Stop-Distance Calibration) — operates alongside MOD 12 (Garman-Klass Volatility), MOD 17 (200D MA & Session Handoffs), MOD 18 (0.75% Spot-Only Risk Sizing), MOD 37 (Net-3.0R Slippage Governor), MOD 50 (Weekend Thin-Liquidity Protocol), and MOD 54 (500/600/500 Kline Lookback Contract).
**Empirical Benchmark Anchor:** Re-verified merged study across 16,406 hourly candles (683 full UTC days, 01 Jan 2025 00:00 UTC to 15 Nov 2026 13:00 UTC; zero gaps/duplicates) reconciling five independent quantitative audits (Antigravity, Opencode, Gemini, Minimax, Meta AI v3), cross-validated out-of-sample across 2,694 full UTC daily bars from `btc_daily_2017_to_now.csv` (17 Aug 2017 to 31 Dec 2024; 3,377 full UTC days combined).
**Governance Posture:** Statistical volatility & stop-sizing calibrator (`ZERO_DIRECTIONAL_ENTRY_SIGNALS`). Governs stop width, session risk windows, and anti-overfitting quarantines — never issues standalone directional buy/sell triggers.

---

#### 1. Machine-Readable State & Routing Block (Python / Hermes / NotebookLM Index)

```yaml
module_id: "MOD_57"
entry_type: "VOLATILITY_REGIME_AND_STOP_CALIBRATOR"
waterfall_pillar: "PILLAR_2_AND_4_TEMPORAL_VOLATILITY"
title: "Intraday & Calendar Volatility Regime, DST Session Clock & Empirical Stop-Calibration Engine"

# EMPIRICAL BENCHMARK METADATA (IN-SAMPLE 2025-2026 + OUT-OF-SAMPLE 2017-2024)
empirical_sample:
  venue_reference: "Binance Spot BTCUSDT (cross-checked against 3-venue quorum per MOD 36)"
  in_sample_hourly_window_utc: "2025-01-01T00:00:00Z to 2026-11-15T13:00:00Z"
  in_sample_full_utc_days: 683
  in_sample_hourly_bars: 16406
  out_of_sample_daily_window_utc: "2017-08-17 to 2024-12-31"
  out_of_sample_full_utc_days: 2694
  combined_full_utc_days: 3377
  timezone_standard: "UTC primary; MYT/SGT (UTC+8) operator HUD display"

# CALENDAR VOLATILITY & COVARIANCE PARAMETERS (UTC DAY)
calendar_volatility:
  daily_range_mean_pct_2025_2026:
    Monday: 3.87
    Tuesday: 3.69
    Wednesday: 3.62
    Thursday: 3.67
    Friday: 3.94
    Saturday: 1.83
    Sunday: 2.75
  daily_range_mean_pct_oos_2017_2024:
    Monday: 5.94 # #1 OOS daily range (49.6% > 5% tail)
    Tuesday: 5.42
    Wednesday: 5.84
    Thursday: 5.79
    Friday: 5.68
    Saturday: 3.97 # #7 quietest in both OOS (3.97%) and IS (1.83%)
    Sunday: 4.51
  hourly_range_mean_pct:
    Monday: 0.73
    Tuesday: 0.68
    Wednesday: 0.67
    Thursday: 0.68
    Friday: 0.71
    Saturday: 0.37
    Sunday: 0.48
  tail_risk_prob_daily_range_gt_5pct:
    Friday: 24.5
    Monday: 20.6
    Thursday: 19.4
    Saturday: 4.1
  intraday_covariance_effect:
    Monday_hourly_cancelling_pct: -35.6 # Highest per-hour range (0.73%), lower close-to-close vol (43.9%)
    Thursday_hourly_reinforcing_pct: 17.4 # Highest close-to-close annualized vol (51.2%); drift -56 bps IS vs -19 bps OOS (p=0.414)
  weekend_regime_override:
    weekday_vs_weekend_hourly_ratio: 1.63 # 0.69% vs 0.42%
    calm_saturday_bp: 14.2
    high_vol_saturday_bp: 40.0 # Weekend quietness disappears during active market storms (e.g., 31 Jan 2026 10.15% range)

# DST-TRACKED US EQUITY OPEN SESSION CLOCK (UTC / MYT)
session_clock:
  us_daylight_saving_mar_nov:
    us_equity_open_utc: "13:30"
    peak_4h_window_utc: "13:00-17:00" # 21:00-01:00 MYT/SGT
    single_peak_hour_utc: "14:00" # 0.91% mean range
  us_standard_time_nov_mar:
    us_equity_open_utc: "14:30"
    peak_4h_window_utc: "14:00-18:00" # 22:00-02:00 MYT/SGT (Active post-Nov 1, 2026)
    single_peak_hour_utc: "15:00" # 1.31% mean range (14:00 UTC = 1.23%)
  quietest_trough_hour_utc: "10:00" # 18:00 MYT/SGT (0.46% mean range; 2.2x narrower than 14:00 UTC)
  us_session_share_of_daily_range_pct: 41.3 # 13:00-20:00 UTC (33% of hours) holds 41.3% of daily range sum
  same_day_width_predictor_hours_utc: ["14:00", "15:00", "16:00", "17:00"] # Corr 0.61-0.66 with full-day range
  opening_range_anchor_hour_utc: "00:00" # 08:00 MYT: sets daily High 12.3% & Low 14.5% of days (3.0x-3.5x random 4.2%); >75% of initial breaks snap back inside OR
  sunday_mini_open_hour_utc: "22:00" # 06:00 MYT Monday: 0.94% mean range (~2.0x Sunday 0.48% average)

# VOLATILITY CLUSTERING, VOLUME-WIDTH & 200D REGIME CALIBRATORS
clustering_and_regime:
  hourly_range_autocorr_lag1: 0.57
  hourly_range_autocorr_lag24: 0.33
  daily_range_autocorr_lag1_is: 0.39
  daily_range_autocorr_lag1_oos: 0.53
  post_2pct_hour_next_hour_range_pct: 1.69 # vs 0.62% baseline (n=353)
  post_6pct_day_next_day_range_pct_is: 5.41 # n=59
  post_6pct_day_next_day_range_pct_oos: 7.66 # n=787
  post_compression_lt_1_5pct_next_day_range_pct_is: 2.32 # n=83
  post_compression_lt_1_5pct_next_day_range_pct_oos: 2.37 # n=146
  volume_to_daily_range_corr: 0.85
  volume_surge_2x_20d_ma:
    etf_era_2025_2026_same_day_range_pct: 8.33
    etf_era_2025_2026_next_day_return_pct: -0.29 # 39.3% win (multi-day institutional/liquidation cascades)
    pre_etf_oos_2017_2024_next_day_return_pct: 0.74 # 57.5% win (n=127; retail V-bottom regime retired post-ETF)
  sma_200d_regime_split:
    is_2025_2026_below_200d: {range_pct: 3.60, drift_pct: -0.22, win_pct: 45.9}
    is_2025_2026_above_200d: {range_pct: 3.10, drift_pct: 0.15, win_pct: 52.3}
    oos_2018_2024_below_200d: {range_pct: 4.96, drift_pct: -0.15, win_pct: 48.2}
    oos_2018_2024_above_200d: {range_pct: 4.86, drift_pct: 0.41, win_pct: 53.8} # Welch p=0.0001 on drift split

# RISK & SIZING CONSTANTS (PILLAR 4 INVARIANTS)
risk_parameters:
  max_portfolio_risk_pct: 0.75 # Never exceeded regardless of calendar multiplier
  stop_widening_notional_scaling: "Wider calendar/cluster stops MUST shrink BTC notional size proportionally so dollar risk stays <= 0.75% (MOD 18 M4)."
  leverage_permitted: 1.0 # Strict Unleveraged Spot Only
```

---

#### 2. Protective Circuit Breakers (Anti-Overfitting & Tail-Risk Guardrails)

*   **Circuit Breaker 1 — Appendix B & OOS False-Edge Quarantine (CB-01):** Never execute trades based on unadjusted day-hour directional claims, raw taker-buy ratios (`lag-1` corr `0.04`), yesterday's return (`lag-1` autocorr `-0.05` daily / `-0.01` hourly), turn-of-month Day-1 drift, Thursday drift (`-19 bps` OOS, `p=0.414`), or unauthenticated 2–5 bps absorption candles (below taker fees). Green-Monday -> red-Tuesday (`32.7%` win in 2025–2026 vs `47.1%` win / `+0.05%` in 2017–2024 OOS) failed out-of-sample replication and is downgraded to non-binding background trivia.
*   **Circuit Breaker 2 — Tail-Sized Stop Discipline & Notional Compression (CB-02):** Because `1%` of hours carry `28%` of total return variance (`99th` percentile hourly move = `176 bps`, `9x` the `19.5 bps` median), stops sized to median hours are systematically stopped out on Fridays, Mondays, and during the US equity open window (`13:00–18:00 UTC`). Widen structural stops during high-vol windows (`-21.3%` noise stop-out reduction verified across `16,300` bars) and compress BTC notional size proportionally (`MOD 18 M4`) so max risk never exceeds `0.75%` (`0.375%` Amber).
*   **Circuit Breaker 3 — ETF-Era Volume-Surge Day-1 Bounce Ban (CB-03):** While pre-ETF retail cycles (`2017–2024`, `n=127`) averaged `+0.74%` (`57.5%` win) the day after a `> 2.0x` 20D volume surge, the institutional ETF era (`2025–2026`) inverted to `-0.29%` (`39.3%` win; `8.33%` range) due to multi-day AP redemption and liquidation cascades. Classify any `> 2.0x` volume surge as a multi-day shock rather than a Day-1 V-bottom and enforce `MOD 03` / `MOD 34` stand-down.
*   **Circuit Breaker 4 — 00:00 UTC Opening Range Protection (CB-04):** Because `00:00 UTC` (`08:00 MYT`) prints the daily high (`12.3%`) or daily low (`14.5%`) roughly `3x` more often than random (`4.2%`), and **`77.5%` of upward breaks and `75.1%` of downward breaks snap back inside the `00:00 UTC` range before UTC close**, never chase a raw `00:00 UTC` break or fade it without `MOD 11` / `MOD 05` Domestic USD Spot CVD confirmation.
*   **Circuit Breaker 5 — Timezone & Sample-Window Honesty (CB-05):** All daily and monthly aggregations must strictly use **UTC** boundaries (converting to **MYT/SGT** only for display) to prevent cross-month distortion (e.g., Feb 2026 `-14.94%` UTC vs. `-20.25%` SGT).

---

#### 3. Core Conditional Signal Units (Condition A -> Outcome B -> Rule C)

##### CSU-57A: US Equity Open DST Peak Window & Same-Day Range Expansion
*   **Trigger Condition A (The Telemetry Scan):**
    1. Clock enters the active US cash-equity open block: **`13:00–17:00 UTC` (`21:00–01:00 MYT`)** during US Daylight Time (Mar–Nov) or **`14:00–18:00 UTC` (`22:00–02:00 MYT`)** during US Standard Time (Nov–Mar).
    2. **Same-Day Regime Confirmation:** The `14:00–17:00 UTC` block prints wide hourly ranges (`> 1.0%`/hr; `0.61–0.66` correlation with full-day range).
*   **Observed Outcome B (The Mechanical Trajectory):**
    *   **Microstructure Lens:** Institutional USD spot, ETF Authorized Participant flow, and macro desks dominate order flow (`41.3%` of total daily range occurs inside `13:00–20:00 UTC`), creating fat-tailed price discovery.
*   **Execution Rule C (The Non-Negotiable Action):**
    *   **Action:** Apply `1.25x–1.50x` volatility stop buffer on any `MOD 18` authorized spot entry, scale BTC notional size down proportionally to keep equity risk `<= 0.75%`, and prohibit tight scalp stops inside the peak window.

##### CSU-57B: High-Volatility Clustering Carryover (Post-2% Hour / Post-6% Day)
*   **Trigger Condition A (The Telemetry Scan):**
    1. Prior `1H` candle range exceeds **`2.0%`** (`lag-1` autocorr `0.57`), **OR** prior full UTC day range exceeds **`6.0%`** (`lag-1` autocorr `0.39` IS / `0.53` OOS).
*   **Observed Outcome B (The Mechanical Trajectory):**
    *   **Microstructure Lens:** Volatility clusters strongly (`1.69%` expected next-hour range vs. `0.62%` baseline; `5.41%` IS / `7.66%` OOS expected next-day range). Aftershocks and liquidity sweeps persist across subsequent bars.
*   **Execution Rule C (The Non-Negotiable Action):**
    *   **Action:** Maintain elevated Garman-Klass (`MOD 12`) stop-distance floors for at least `4` subsequent `1H` bars (or `24H` after a `> 6.0%` day). Do not prematurely tighten trailing stops into noise.

##### CSU-57C: 00:00 UTC Opening Range Anchor & Sunday 22:00 UTC Mini-Open
*   **Trigger Condition A (The Telemetry Scan):**
    1. Price tests or breaks the **`00:00 UTC` (`08:00 MYT`)** first-hour high or low during intraday trading, **OR** clock reaches **Sunday `22:00 UTC` (`06:00 MYT` Monday)** where average hourly range jumps to `0.94%` (`~2x` Sunday's `0.48%` mean).
*   **Observed Outcome B (The Mechanical Trajectory):**
    *   **Microstructure Lens:** `00:00 UTC` sets the session's structural boundary `26.8%` of all days (`12.3%` high + `14.5%` low) with `>75%` mean-reversion on initial breaks, while Sunday `22:00 UTC` marks institutional pre-open positioning (`MOD 50`).
*   **Execution Rule C (The Non-Negotiable Action):**
    *   **Action:** Treat the `00:00 UTC` high/low as a hard horizontal structural reference (`MOD 11` / `MOD 54`). Require `4+` consecutive `1H` closes (`00C`) + `MOD 05/07` Domestic USD Spot CVD confirmation before treating a `00:00 UTC` breach as a structural breakout, and enforce `MOD 50` pre-settlement caution at Sunday `22:00 UTC`.

##### CSU-57D: Saturday Illiquidity vs. High-Vol Storm Override
*   **Trigger Condition A (The Telemetry Scan):**
    1. Calendar day is **Saturday UTC** (`1.83%` IS / `3.97%` OOS mean daily range — #7 quietest in both eras; `46%` weekday volume, `$540` higher avg institutional block size).
    2. **Regime Split:** Trailing 24H/7D volatility is either bottom-quartile calm (`14.2 bp`/hr baseline) OR top-quartile storm (`40.0 bp`/hr, matching Friday's `43.0 bp`).
*   **Observed Outcome B (The Mechanical Trajectory):**
    *   **Microstructure Lens:** Calm Saturdays mean-revert inside narrow ranges with wider effective spreads, whereas high-volatility Saturdays behave like full weekday cascades due to thin order-book depth (e.g., 31 Jan 2026 `-6.55%` / `10.15%` range).
*   **Execution Rule C (The Non-Negotiable Action):**
    *   **Action:** During calm Saturdays, avoid breakout chasing and enforce passive limit-only orders (`MOD 50 CB-03`). During high-vol regimes (`ICDM >= 60` or `MOD 33 R4`), cancel any Saturday volatility discount and enforce full `100% CASH LOCK`.

---

#### 4. Dynamic Regime Mutation Lookup Matrix (M1 through M4)

| Mutation ID | Initial State | Telemetry Mutation Observed (Condition A') | Mechanical Meaning (Outcome B') | Mandatory Execution Override (Rule C') |
| :--- | :--- | :--- | :--- | :--- |
| **M1: US DST Clock Shift (Mar / Nov)** | Standard Session Timer | Calendar crosses US DST transition (2nd Sunday in March or 1st Sunday in November). | Institutional peak volume & volatility window shifts by 1 UTC/MYT hour (`14:00` <-> `15:00 UTC`). | **Auto-Shift Peak Window:** `13:00–17:00 UTC` (`21:00–01:00 MYT`) in Summer; `14:00–18:00 UTC` (`22:00–02:00 MYT`) in Winter. |
| **M2: Monday Intraday Chop vs. Thursday Trend** | Weekday Execution | Monday prints wide hourly swings (`0.73%`/hr) with negative intraday covariance (`-35.6%`), vs. Thursday positive covariance (`+17.4%`). | Monday hourly moves tend to mean-revert intraday; Thursday moves reinforce into full-day directional swings (though Thursday drift `-19 bps` OOS is non-significant). | **On Mondays:** Take Stage 1 (50%) profits promptly at POC/VAH. **On Thursdays:** Respect intraday momentum once `MOD 05/07` CVD confirms. |
| **M3: Green-Monday -> Tuesday (OOS Retired)** | Monday Close > 0 | Monday UTC closes green (`32.7%` Tue win in 2025–2026, **but `47.1%` win / `+0.05%` in 2017–2024 OOS**, `n=189`). | Failed out-of-sample replication; 2025–2026 weakness was sample noise rather than a 9-year structural law. | **Downgraded to Non-Binding Trivia (`CB-01`):** Do not penalize or block Tuesday entries solely because Monday closed green. |
| **M4: Below-200D SMA Negative-Drift Regime** | Spot < 200D SMA | Price trades below 200D SMA (`-0.15%`/day OOS vs `+0.41%`/day above, `p=0.0001`; `-0.22%`/day IS vs `+0.15%`/day above, `p=0.0327`). | Proven 9-year secular regime divider: positive drift above 200D SMA, negative drift below 200D SMA. | **Enforce `MOD 17` Risk Cap (`<= 0.375%` Amber or `0.00%` Cash Lock)** below 200D SMA and widen structural stops in ETF-era drawdowns (`3.60%` daily range). |

---

#### 5. Nine-Year Out-of-Sample Audit Summary (`2017–2024` vs. `2025–2026`)

| Tested Rule / Phenomenon | Out-of-Sample (`2017–2024`, `n=2,694` Full Days) | In-Sample (`2025–2026`, `n=683` Full Days) | Verdict & `MOD 57` Action |
| :--- | :--- | :--- | :--- |
| **`200D SMA` Regime Drift Split** | Above: `+0.41%`/day (`53.8%` win) vs. Below: `-0.15%`/day (`48.2%` win) — **`p = 0.0001`** | Above: `+0.15%`/day (`52.6%` win) vs. Below: `-0.22%`/day (`45.9%` win) — **`p = 0.0327`** | **SURVIVES (`M4` Locked):** Core 9-year secular drift divider (`MOD 17` + `MOD 57`). |
| **Weekday Highs vs. Saturday Quiet** | Mon `5.94%` (#1), Fri `5.68%` vs. **Sat `3.97%` (#7 quietest)** | Fri `3.94%` (#1), Mon `3.87%` vs. **Sat `1.83%` (#7 quietest)** | **SURVIVES (`CB-02` / `CSU-57D`):** Permanent calendar volatility hierarchy. |
| **Daily Volatility Clustering** | `Lag-1` autocorr **`0.53`**; post-`>6%` day next range **`7.66%`** vs. post-`<1.5%` **`2.37%`** | `Lag-1` autocorr **`0.39`**; post-`>6%` day next range **`5.41%`** vs. post-`<1.5%` **`2.32%`** | **SURVIVES (`CSU-57B`):** Strongest universal volatility persistence law. |
| **3-Red-Day Streak Mild Bounce** | `n = 252` streaks: **`+0.33%`** next-day mean, **`56.0%`** win | `n = 89` streaks: **`+0.42%`** next-day mean, **`56.2%`** win | **SURVIVES (Soft Context Only):** Reproduces OOS, but remains below-threshold for standalone triggers. |
| **Green-Monday -> Red-Tuesday** | `n = 189`: Tuesday **`+0.05%`**, **`47.1%`** win (coin flip) | `n = 55`: Tuesday **`-0.38%`**, **`32.7%`** win | **FAILED OOS (`M3` Retired):** Sample noise in 2025–2026; removed as an active filter. |
| **Volume Surge (`>2.0x` 20D MA)** | `n = 127`: **`+0.74%`** next-day mean, **`57.5%`** win (pre-ETF V-bottoms) | `n = 35`: **`-0.37%`** next-day mean, **`40.0%`** win (ETF cascade regime) | **REGIME SHIFT (`CB-03`):** Post-ETF volume surges trigger multi-day unwinds, not Day-1 bounces. |
