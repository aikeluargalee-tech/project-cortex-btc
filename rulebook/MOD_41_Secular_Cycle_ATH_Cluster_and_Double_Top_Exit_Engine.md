# [45/45] MOD 41 — Secular Cycle ATH Cluster & Double-Top Exit Engine (Pillar 1 & 4)

*Source File: `MOD_41_Secular_Cycle_ATH_Cluster_and_Double_Top_Exit_Engine.md` (Extracted from `1. ATH Crash 1.pdf` — 3,341 Daily Candles, 107 New ATHs, 5 Clusters, 39 Order-25 Pivots)*

---

# PROJECT CORTEX-BTC — MODULE 41: SECULAR CYCLE ATH CLUSTER & DOUBLE-TOP EXIT ENGINE
**Waterfall Tier:** Pillar 1 (Secular Cycle Positioning) & Pillar 4 (Two-Stage Distribution / Profit-Exit Architecture).
**Empirical Benchmark Anchor:** Full Binance BTCUSDT 1D dataset (`2017-08-17` to `2026-10-09`; `3,341` daily candles, `107` new ATHs, `5` ATH clusters, `39` major order-25 pivots, `58` double-tops with `gap <= 330d` and `trough >= 12%`), spanning the 2017 single blow-off (`$19,798`), 2021 double-top (`$64,854` -> `-55.6%` -> `$69,000`), and 2024–2025 extended double-top (`$73,777` -> `-33.6%` -> `$126,199` Oct 6, 2025 -> `-19.2%` Oct 10 flush -> `-54.2%` drawdown).

---

## 1. Machine-Readable State & Routing Block (Python / Hermes / NotebookLM Index)

```yaml
module_id: "MOD_41"
entry_type: "SECULAR_ATH_CLUSTER_AND_DOUBLE_TOP_EXIT_ENGINE"
waterfall_pillar: "PILLAR_1_AND_PILLAR_4_CYCLE_EXIT"
title: "Secular Cycle ATH Cluster & Double-Top Exit Engine"

# GOVERNANCE & EPISTEMIC GUARDRAILS
sample_size_disclosure: "Rule 1 proven 4/4 major ATHs; Rules 2-4 rest on n=2-4 cycle tops & 7 ~+4% double-tops — treat as risk filter & tranche framework, NEVER as standalone price prediction."
daily_timeframe_primacy: "Daily closes govern Rule 1 (-10% close in 3-8d); intraday/hourly noise is subordinate."

# PRIMARY TELEMETRY INPUTS
ath_exit_telemetry:
  ath_high_usd: "Current or latest all-time high print (Day 0 anchor)"
  ath_close_usd: "Day 0 daily UTC close"
  days_since_ath: "Calendar days elapsed since Day 0 ATH (10-day Rule 1 timer)"
  drawdown_from_ath_close_pct: "(Daily_Close - ATH_High) / ATH_High * 100"
  drawdown_from_ath_wick_pct: "(Intraday_Low - ATH_High) / ATH_High * 100"
  prior_cluster_peak_usd: "Preceding major pivot high (order 25) prior to >= 12% / 30-55% shakeout"
  prior_trough_drawdown_pct: "Max correction depth between Peak 1 and Peak 2"
  second_peak_overshoot_pct: "(New_ATH - Prior_Cluster_Peak) / Prior_Cluster_Peak * 100"
  second_peak_ratio: "New_ATH / Prior_Cluster_Peak (1.01x-1.06x = flat exhaustion zone)"
  oi_at_record_high: "Boolean: derivatives open interest at cycle/all-time highs (MOD 01/02)"
  funding_positive: "Boolean: perp funding rate > 0% at ATH print"

# DETERMINISTIC THRESHOLDS (CALIBRATED FROM 3,341 DAILY CANDLES)
ath_exit_thresholds:
  rule1_timer_window_days: [1, 10]
  rule1_close_trigger_days: [3, 8]
  rule1_close_drop_pct: -10.0         # Daily close <= -10.0% in 3-8d (4/4 hit rate)
  rule1_wick_range_days: [4, 9]
  rule1_wick_drop_pct_band: [-44.0, -17.0] # Week-1 liquidation wick (-17% to -44%)
  rule2_shakeout_band_pct: [-55.0, -30.0]  # Mid-cycle Cluster A -> Cluster B shakeout
  rule3_min_trough_pct: -12.0         # Minimum trough separating two peaks (gap <= 330d)
  rule3_fatal_flat_overshoot_pct: [1.0, 6.0]   # +1% to +6% (1.01x-1.06x, avg +3%)
  rule3_healthy_wide_overshoot_min_pct: 13.0   # +13% to +50%+ continuation band
  rule4_cycle_top_multiples: [3.49, 1.83]      # 2017->2021 (+248%), 2021->2025 (+83%)

# RISK & EXIT PARAMETERS (PILLAR 4)
exit_parameters:
  laddered_tranche_example: "4 x 5% partial profit tranches across marginal highs (vs single all-or-nothing price)"
  stage1_flat_double_top_trim: "Partial profit-take ('sell some') when 2nd peak hits +1% to +6% (~+4%)"
  stage2_rule1_confirm_exit: "Accelerated de-risk ('sell more') if Rule 1 (-10% daily close in 3-8d) fires"
  max_leverage_permitted: 1.0 # Strict Unleveraged Spot Only
```

---

## 2. Empirical Baseline & Historical Proof Table (3,341 Daily Candles)

### A. Rule 1 — First-Week Leverage Flush (`4/4` Major ATH Hit Rate)
When Bitcoin prints a new cycle ATH with record Open Interest and positive funding, the first leverage wipeout occurs within **days**, not months:
* **`-10%` daily close:** **`3 to 8 days`** after ATH.
* **`-17%` to `-44%` intraday wick low:** **`4 to 9 days`** after ATH.

| Cycle ATH | Days to `-10%` Daily Close | Days to Liquidation Wick Low | Wick Depth | Empirical Note |
| :--- | :--- | :--- | :--- | :--- |
| **2017** (`$19,798` Dec 17) | `3 days` | `5 days` | `-44.6%` | Single parabolic blow-off; `-84.1%` bear to `$3,156` in `363d`. |
| **2021** (`$69,000` Nov 10) | `8 days` | `9 days` | `-19.4%` | Followed Cluster A (`$64,854`) + `-55.6%` shakeout (`$28,805`, `69d`). |
| **2024** (`$73,777` Mar 14) | `5 days` | `6 days` | `-17.6%` | Cluster A peak; followed by `-33.6%` shakeout to `$49,000` (`144d`). |
| **2025** (`$126,199` Oct 6) | `5 days` | `4 days` (`Oct 10`) | `-19.2%` (`$102,000`) | Triggered `$19B` / `1.6M` traders liquidation flush; `-54.2%` drawdown to `$57,800–$58,115` (`268d`). |

### B. Rule 3 — Second-Peak Overshoot Registry ("FLAT = FATAL, WIDE = HEALTHY")
Across `58` double-tops (`gap <= 330d`, `trough >= 12%`, `2nd >= 1st`): overall median overshoot `+24.5%` (crash tops `28`: median `+14.3%`; continuation `30`: median `+47.5%`). Across `7` historical `~+4%` (`+2%` to `+6%`) second peaks: **`71%`** dropped `> -20%` in `90d` (median `-36.1%` in `90d`, `-54.2%` in `500d`) and **`57%`** crashed `> -50%` within `500d`.

| Class | 1st Peak -> 2nd Peak Dates | Price Trajectory & Overshoot | Intervening Trough / Gap | Subsequent Outcome |
| :--- | :--- | :--- | :--- | :--- |
| **Fatal Flat** | `2018-09-04 -> 2018-10-15` | `$7,410 -> $7,680` (**`+3.6%`**) | `-17.5%` / `41d` | `-58.9%` in `90d` |
| **Fatal Flat** | `2019-10-26 -> 2020-02-13` | `$10,370 -> $10,500` (**`+1.3%`**) | `-37.9%` / `110d` | Bear / COVID crash (`-50%+`) |
| **Fatal Flat** | `2021-03-13 -> 2021-04-14` | `$61,844 -> $64,854` (**`+4.9%`**) | `-18.5%` / `32d` | `-55.6%` in `90d` (`-72.8%` `500d`) |
| **Fatal Flat** | `2021-04-14 -> 2021-11-10` | `$64,854 -> $69,000` (**`+6.4%`**) | `-55.6%` / `210d` | `-77.6%` bear to `$15,476` |
| **Fatal Flat** | `2022-02-10 -> 2022-03-28` | `$45,821 -> $48,190` (**`+5.2%`**) | Bear rally | `-63.4%` in `90d` (`-67.9%` `500d`) |
| **Fatal Flat** | `2025-07-14 -> 2025-10-06` | `$123,218 -> $126,200` (**`+2.4%`**) | `-13.0%` / `84d` | `-36.1%` in `90d`, `-54.2%` `500d` |
| **Fatal Flat** | `2025-08-14 -> 2025-10-06` | `$124,474 -> $126,200` (**`+1.4%`**) | `-13.8%` / `53d` | `-54.2%` bear (`$57,800` Jul 2026) |
| **Healthy Wide** | `2020-06-01 -> 2020-08-17` | `$10,380 -> $12,468` (**`+20.1%`**) | `-14.9%` / `77d` | Bull continuation |
| **Healthy Wide** | `2024-01-11 -> 2024-03-14` | `$48,969 -> $73,777` (**`+50.7%`**) | `-21.3%` / `63d` | Bull continuation |
| **Healthy Wide** | `2024-07-29 -> 2024-12-17` | `$70,080 -> $108,353` (**`+54.6%`**) | `-30.1%` / `141d` | Bull continuation |
| **Healthy Wide** | `2024-12-17 -> 2025-07-14` | `$108,353 -> $123,218` (**`+13.7%`**) | `-31.2%` / `209d` | Bull continuation |

### C. Rule 4 — Diminishing Cycle-Top Multiples (Planning Context Only)
* `2017 -> 2021`: `3.49x` (`+248%`)
* `2021 -> 2025`: `1.83x` (`+83%`)
* Extrapolating from `$126,199` yields a wide planning zone of **`$230k–$439k`** (`1.83x = ~$231k`, `2.5x = ~$315k`, `3.49x = ~$440k`). Note that `$230k` is merely `$126,199 x 1.83`, not a true psychological anchor; round-number psychological zones sit at **`$200k`**, **`$250k`**, and **`$300k`**.

---

## 3. Protective Circuit Breakers (Cycle-Top Anti-Fallacy Rules)

* **Circuit Breaker 1 — Double-Tops Are Descriptive, Not Standalone Short/Sell Signals (`CB-01`):** `2024–2025` printed `33` new ATHs; `32` broke down mildly and resolved higher—only the 33rd ended the cycle. Never exit 100% spot solely because price looks "rounded"; use `Rule 3` (`+1%–+6%` overshoot) as a **filter** and `Rule 1` (`-10%` daily close in `3–8d`) as the **confirmation trigger**.
* **Circuit Breaker 2 — Mechanical Extrapolation Fallacy (`CB-02`):** With `n = 2` completed cycle multiples (`3.49x`, `1.83x`), never anchor all exits to one magic target (e.g., `$230k`). Scale out in **laddered tranches** (`e.g., 4 x 5%`) across marginal highs.
* **Circuit Breaker 3 — Week-1 Wick vs. Secular Bottom Separation (`CB-03`):** Do not mistake the Day 4–9 liquidation wick (`-17%` to `-44%`) for the final bear-market bottom; true bear lows take `100–376` days while dipping `~16%–22%` below the prior cycle's ATH (`$15,476` vs `$19,798`; `$57,800` vs `$69,000`).
* **Circuit Breaker 4 — Daily Close Over Hourly Noise (`CB-04`):** Intraday wicks during ATH discovery routinely whipsaw hourly candles; only a **completed UTC daily close `<= -10.0%` from ATH** triggers Rule 1 Stage-2 confirmation.

---

## 4. Core Conditional Signal Units (`Condition A -> Outcome B -> Rule C`)

### CSU-41A: First-Week Leverage Flush Timer ("Rule 1 — Day 1 to Day 10")
* **Trigger Condition A (The Telemetry Scan):**
  1. Bitcoin prints a **new cycle ATH** while **Open Interest is at record highs** (`MOD 01/02`) and **funding is positive**.
  2. Within **`3 to 8 days`** of the ATH print, a **completed UTC daily close prints `<= -10.0%` below ATH** (often accompanied by a **`-17% to -44%` intraday liquidation wick** between `Day 4` and `Day 9`).
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Cycle Microstructure Lens:** Crowded ATH breakout leverage has failed into an immediate Week-1 liquidation cascade (`4/4` historical cycles: 2017, 2021, 2024, 2025).
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **ARM 10-DAY ATH TIMER ON DAY 0;** prohibit fresh leveraged/chasing entries during `Day 1–10`. Upon `-10%` daily close confirmation, **execute Stage-2 distribution trim ("sell more")** and lock defensive cash (`MOD 30 CONFIG_F / CONFIG_H`).

### CSU-41B: Flat Exhaustion Double-Top Warning ("Rule 3 — +1% to +6% Overshoot")
* **Trigger Condition A (The Telemetry Scan):**
  1. Following a **`>= 12%` to `55%` shakeout** (`32–210+` days between peaks), Bitcoin prints a new ATH that sits only **`+1.0%` to `+6.0%` (`1.01x–1.06x`, average `+3%`)** above the prior cluster peak.
  2. Cross-pillar fragility creeps higher (`MOD 31 ICDM rising`, negative Coinbase Premium `MOD 19`, or slowing ETF inflows `MOD 38`).
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Cycle Exhaustion Lens:** `71%` historical rate of `> -20%` drop within `90d` (median `-36.1%` `90d`, `-54.2%` `500d`), with `57%` entering a full `-50%` to `-85%` bear market.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **EXECUTE STAGE-1 PARTIAL PROFIT TAKE ("sell some" / laddered tranches)** into `+4%` (`1.01x–1.06x`) marginal highs **AND arm `CSU-41A` 10-day timer**; retain core runner in case overshoot expands past `+13%`.

### CSU-41C: Healthy Wide Double-Top Continuation ("Rule 3 — +13% to +50%+ Expansion")
* **Trigger Condition A (The Telemetry Scan):**
  1. Following a `>= 12%` correction, the new ATH expands **`>= +13.0%`** (typically `+13%` to `+50%+`) above the prior peak while `MOD 05` USD Spot CVD and `MOD 16` macro remain constructive.
  2. `Rule 1` (`-10%` daily close in `3–8d`) does not break structural range support on a closing basis.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Cycle Expansion Lens:** Broad impulse discovery (`2020`, `Mar 2024`, `Dec 2024`, `Jul 2025`)—mid-bull continuation rather than flat distribution.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **HOLD CORE SPOT ALLOCATION (`MOD 18`)**; keep remaining tranches open with trailing structural stops below `4H POC / Daily VAL` while honoring the Day 1–10 flush watch.

### CSU-41D: Post-ATH Cluster Shakeout & Prior-ATH Floor ("Rule 2 — 30%–55% Shakeout vs. Bear Floor")
* **Trigger Condition A (The Telemetry Scan):**
  1. After Cluster A peaks, spot corrects **`-30%` to `-55%`** while macro liquidity (`MOD 16/22`) stabilizes (`e.g. 2021 -55.6%`, `2024 -33.6%`); **OR** after Cluster B final double-top breaks, spot approaches **`-16%` to `-22%` below the prior cycle's ATH** (`$15,476` vs `$19,798`; `$57,800` vs `$69,000`).
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Secular Cycle Lens:** Distinguishes mid-cycle Cluster A shakeouts from post-Cluster B secular bear drawdowns (`268–376` days, `-50%` to `-85%`).
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **REQUIRE FULL `MOD 33` + `MOD 17` (`200D MA`) + `MOD 37` (`Net R >= 3.0`) CONFLUENCE** before committing fresh spot capital; never catch falling knives purely on percentage drawdown alone.

---

## 5. Dynamic Regime Mutation Lookup Matrix (`M1` through `M8`)

| Mutation ID | Initial State | Telemetry Mutation Observed (`Condition A'`) | Mechanical Meaning (`Outcome B'`) | Mandatory Execution Override (`Rule C'`) |
| :--- | :--- | :--- | :--- | :--- |
| **M1: Flat Double-Top -> Rule 1 Triggered** | `CSU-41B` (`+1% to +6%` Peak) | Within `3–8 days` of marginal new ATH, UTC daily close drops **`<= -10.0%` from ATH** (`e.g. Oct 10, 2025`). | Confirmed exhaustion double-top transitioning into Week-1 leverage flush and bear leg. | **Execute Stage-2 Exit ("sell more")**; shift to `MOD 30 CONFIG_H` / `100%` cash shield. |
| **M2: Flat +4% Reclaim -> Wide Expansion** | `CSU-41B` (Stage-1 Partial Trim) | After a mild `-12%` dip, spot reclaims and pushes **`>= +13%` above Peak 1** (`e.g. Dec 2024 -> Jul 2025`). | Market transitioned from mini double-top pause into healthy wide continuation (`CSU-41C`). | **Let remaining runner ride;** avoid re-chasing trimmed tranche unless `MOD 37 Net R >= 3.0`. |
| **M3: Blow-Off Parabolic Exception (`2017`)** | New ATH Cluster | Price doubles rapidly (`+100%+` in weeks) with vertical `funding >= +0.06%/8h` and zero `>= 12%` pullbacks. | Parabolic blow-off top (`2017` style) may crash `-84%` **without** forming a second Cluster B peak. | **Enforce `CSU-41A` Day 3–8 `-10%` close strictly** even without a double-top. |
| **M4: Two-Swing Plan Tranche Ladder** | Approaching Cluster A (`+36%–+80%`) | Spot enters psychological round-number zone (`$200k / $250k / $300k`) with `MOD 31 ICDM > 50`. | Distribution zones span wide bands (`$230k–$439k`), not a single print. | **Execute laddered `4 x 5%` partial trims** instead of waiting for one exact target. |
| **M5: Week-1 Wick Reclaimed Inside 24H** | `Day 4–9` (`-17%` Wick) | Intraday wick hits `-19%`, **but daily UTC close holds `> -10.0%` and Spot CVD surges positive**. | Leverage flushed cleanly without breaking daily closing structure (`2024` mid-bull reset). | **Hold core runner;** tighten trailing stop to wick mid-point rather than panic-selling bottom. |
| **M6: Mini Double-Top Inside Cluster** | Active Bull Cluster | Two peaks `2–6%` apart separated by `< 12%` dip (`12+` historical occurrences, e.g. Dec 2017). | Intra-cluster chop or localized shakeout rather than full cycle termination. | **Respect `-12%` minimum trough filter** before classifying as secular Cycle Cluster B. |
| **M7: Bear Drawdown Below Prior Cycle ATH** | Post-Cluster B Bear (`-50%+`) | Spot breaks prior cycle ATH and stabilizes **`-16%` to `-22%` below prior ATH** (`$57.8k` vs `$69k`). | Historical secular bear exhaustion zone (`268–376d`), where macro & on-chain bottoming starts. | **Transition from exit mode to `MOD 33 / MOD 18` accumulation watch** (`wait for Net R >= 3.0`). |
| **M8: Unverified Single-Cycle Extrapolation** | Long-Range Planning | User or model anchors exit exclusively to `1.83x` (`$230k`) as a "confirmed target". | `n = 2` cycle multiples cannot validate a single price point. | **Override to wide range (`$230k–$439k`) + round-number psych anchors (`$200k/$250k/$300k`).** |
