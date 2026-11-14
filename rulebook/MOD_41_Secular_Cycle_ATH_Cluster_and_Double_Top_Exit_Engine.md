# MOD 41 — Secular Cycle ATH Cluster, First-Week Flush (Rule 1) & Flat Double-Top (+4% Rule 3) Exit Engine (Pillar 1 & 5)

*Source File: `MOD_41_Secular_Cycle_ATH_Cluster_and_Double_Top_Exit_Engine.md`*

---

# PROJECT CORTEX-BTC — MODULE 41: SECULAR CYCLE ATH CLUSTER, FIRST-WEEK FLUSH (RULE 1) & FLAT DOUBLE-TOP (+4% RULE 3) EXIT ENGINE
**Waterfall Tier:** Pillar 1 & Pillar 5 Secular Cycle Top & Sovereign Distribution Architecture (Governs multi-year bull-cycle harvest, post-ATH leverage flush survival, and bear-market drawdown defense).
**Empirical Benchmark Anchor:** Validated across **3,341 daily candles** (Binance BTCUSDT 2017–2026), **107 new All-Time Highs**, and **39 major Order-25 pivots**—codifying the **2017 single parabolic blow-off** (`$19,798` -> `-84.1%` to `$3,156`), **2021 double-top cluster** (`$64,854` Apr 14 -> `-55.6%` `$28,805` -> `$69,000` Nov 10 [`+6.4%` flat double top] -> `-77.6%` to `$15,476`), and **2024–2025 extended double-top cluster** (`$73,777` Mar 14 2024 -> `-33.6%` `$49,000` -> `$123,218` Jul 14 / `$124,474` Aug 14 -> `$126,199–$126,200` Oct 6 2025 [`+1.4%` to `+2.4%` flat double top] -> Oct 10 `$102,000` `-19.2%` 4-day flush / `$19B` liquidation -> `-54.2%` to `$57,800–$58,115` Jun/Jul 2026).

---

## 1. Machine-Readable State & Routing Block (Python / Hermes / NotebookLM Index)

```yaml
module_id: "MOD_41"
entry_type: "SECULAR_CYCLE_HARVEST_AND_CRASH_PROTOCOL"
waterfall_pillar: "PILLAR_1_AND_5_SECULAR_CYCLE_ARCHITECTURE"
title: "Secular Cycle ATH Cluster, First-Week Flush (Rule 1) & Flat Double-Top (+4% Rule 3) Exit Engine"

# EMPIRICAL CONSTANTS (3,341 DAILY CANDLES | 107 ATHs | 39 ORDER-25 PIVOTS)
empirical_constants:
  rule_1_first_week_flush:
    trigger: "New All-Time High printed alongside record Open Interest and positive funding"
    timer_days: 10
    daily_close_flush_threshold_pct: -10.0
    daily_close_window_days: [3, 8]
    wick_low_flush_threshold_pct: [-17.0, -44.0]
    wick_low_window_days: [4, 9]
    historical_hit_rate: "4/4 major cycle ATHs (2017: 3d/-44.6% 5d; 2021: 8d/-19.4% 9d; 2024: 5d/-17.6% 6d; 2025: 5d/-19.2% 4d)"
  rule_2_double_top_cluster_architecture:
    cluster_window_days: 180
    mid_cycle_shakeout_range_pct: [-30.0, -55.0]
    final_bear_drawdown_range_pct: [-50.0, -85.0]
  rule_3_overshoot_flat_vs_wide:
    minimum_prior_trough_pct: -12.0
    fatal_flat_overshoot_pct: [1.0, 6.0] # Avg +3% to +4% -> 71% drop > -20% in 90d (median -36.1%), 57% crash > -50% in 500d (median -54.2%)
    healthy_wide_overshoot_pct: [13.0, 50.0] # Bull continuation (32 of 33 ATHs in 2024-2025)
  cycle_diminishing_multiples:
    cycle_2017_to_2021_multiple: 3.49 # +248% ($19,798 -> $69,000)
    cycle_2021_to_2025_multiple: 1.83 # +83% ($69,000 -> $126,199)
    next_cycle_projections_from_126200:
      conservative_meta_ai_model:
        peak_1_sell_1_zone_usd: [172000, 180000] # 1.36x - 1.43x
        shakeout_dip_buyback_zone_usd: [115000, 125000] # -30% to -35%
        peak_2_plus_4pct_sell_2_zone_usd: [179000, 187000] # Avg $184k
        final_bear_bottom_zone_usd: [50000, 85000] # -54% to -77%
      bull_stretch_opencode_model:
        peak_1_sell_1_zone_usd: [230000, 250000] # ~1.83x
        shakeout_dip_buyback_zone_usd: [138000, 172000] # -25% to -40%
        peak_2_plus_4pct_sell_2_zone_usd: [232000, 265000] # Avg $240k
        final_bear_bottom_zone_usd: [98000, 106000] # -54% to -63%

# ANTI-TRAP CIRCUIT BREAKERS
circuit_breakers:
  CB_01_DAILY_CLOSE_OVER_HOURLY_NOISE: "Evaluate Rule 1 (-10% flush) strictly on Daily UTC closes rather than intraday hourly wicks."
  CB_02_NEVER_ALL_OUT_AT_PLUS_4PCT: "At a +4% second peak, sell partial tranches (laddered, e.g., 4x5% tranches) rather than 100% all-out, so continuation (+13%+) still leaves upside runner exposure."
  CB_03_RULE_1_CONFIRMATION_GATE: "Use Rule 2 & Rule 3 (+1% to +6% flat overshoot) as the structural filter, and Rule 1 (-10% daily close in 3-8 days) as the hard confirmation trigger to exit remaining cycle exposure."
  CB_04_NO_SINGLE_MAGIC_NUMBER: "Treat projected cycle zones ($175k-$184k or $230k-$250k) as broad distribution bands rather than a single exact price target."

# RISK & SIZING CONSTANTS (PILLAR 4)
risk_parameters:
  swing_risk_cap_pct: 0.75
  leverage_permitted: 1.0 # Strict 1.0x Spot Only
  distribution_execution: "LADDERED_TRANCHES_PLUS_RULE_1_CONFIRMATION"
```

---

## 2. Protective Circuit Breakers (Mandatory Secular Cycle Filters)

* **Circuit Breaker 1 — The Week-1 Leverage Killer Timer (`CB-01`):** Whenever Bitcoin sets a new All-Time High with record Open Interest and positive funding, the first violent flush is **days** away, not months away. Start a **10-day countdown timer** on Day 0 (`ATH high + ATH close`). Watch daily closes (`-10%` in `3–8` days) rather than intraday hourly noise.
* **Circuit Breaker 2 — Partial Laddering Over All-In/All-Out Guesses (`CB-02`):** Tops are rounded multi-week processes, not single prints. Never dump 100% of sovereign holdings on a single target price; scale out in **laddered tranches** (e.g., `4 x 5%` tranches) when marginal highs stall, and let `Rule 1` (`-10%` daily close) confirm whether the distribution is fatal.
* **Circuit Breaker 3 — Descriptive Filter vs. Tradable Trigger (`CB-03`):** In 2024–2025, Bitcoin printed `33` new ATHs—`32` resolved higher because the overshoot above prior peaks was wide (`+13%` to `+50%+`), and only the `33rd` crashed because the overshoot was flat (`+1.4%` to `+2.4%`). Never short or exit a secular bull market prematurely during wide `+13%+` continuations.
* **Circuit Breaker 4 — Diminishing Cycle Multiples Discipline (`CB-04`):** Cycle multiples compressed from `3.49x` (2017 -> 2021) to `1.83x` (2021 -> 2025). Calibrate future cycle harvest bands conservatively (`$172k–$187k` base / `$230k–$265k` bull stretch) rather than extrapolating parabolic 2017 multiples.

---

## 3. Core Conditional Signal Units (`Condition A -> Outcome B -> Rule C`)

### CSU-41A: Rule 1 — First-Week Post-ATH Leverage Flush ("The 10-Day Countdown")
* **Trigger Condition A (The Telemetry Scan):**
  1. **Day 0 Ignition:** BTC prints a new All-Time High while aggregate Open Interest sits at record highs (`>= 90th percentile`) and perpetual funding is positive (`MOD 02`).
  2. **Days 1–10 Countdown:** Monitor daily UTC closes against the Day 0 ATH high.
  3. **Flush Trigger:** Daily close drops **`<= -10.0%` below ATH within Days 3–8** (and/or intraday liquidation wick reaches **`-17%` to `-44%` within Days 4–9**).
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Record post-ATH leverage triggers an immediate mechanical margin-wipeout wave (`4/4` historical cycle hit rate: 2017 `-44.6%`, 2021 `-19.4%`, 2024 `-17.6%`, 2025 `-19.2%` / `$19B` liquidation).
  * **Probable Trajectory:** Sharp Week-1 liquidation flush clearing over-leveraged breakout chasers; true cycle bottom takes `100+` days if it is a final top, or forms a mid-cycle shakeout base if overshoot was wide.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Days 0–3 (Pre-Flush):** Tighten trailing stops on tactical swing positions (`MOD 18`) and take Stage 1 profits (`50%`) into record funding (`MOD 02B`) before the flush strikes.
  * **Days 3–9 (Active Flush):** Enforce **100% Cash Lock** on tactical swing capital (`MOD 03B`). Do not catch the falling knife until daily close stabilizes and `MOD 03A` + `MOD 05A` Domestic USD Spot CVD confirm absorption.

### CSU-41B: Rule 2 & Rule 3 — Flat Double-Top Exhaustion ("+1% to +6% Second-Peak Harvest")
* **Trigger Condition A (The Telemetry Scan):**
  1. Following an initial ATH cluster (`Peak 1`) and a `>= 12%` correction trough (typically `-13%` to `-55%` over `32` to `210` days), Bitcoin rallies back to print a second ATH cluster (`Peak 2`).
  2. **Flat Overshoot Measurement:** `Peak 2` exceeds `Peak 1` by only **`+1.0%` to `+6.0%`** (`1.01x` to `1.06x`, average `+3%` to `+4%`) and begins rounding over with flattening/negative Domestic USD Spot CVD (`MOD 05C` / `MOD 19C`).
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Marginal demand is exhausted (`Flat = Fatal`): institutional holders are distributing into a rounded double-top ceiling (`71%` historical probability of `> -20%` drop in 90 days, median `-36.1%`; `57%` probability of `-50%` to `-85%` bear market within 500 days).
* **Execution Rule C (The Non-Negotiable Action):**
  * **Step 1 (`+4%` Peak 2 Partial Harvest):** Execute **Tranche 2 Laddered Profit-Taking** (sell partial sovereign/swing tranches into the `+1%` to `+6%` overshoot zone) and immediately arm the `Rule 1` 10-Day Timer.
  * **Step 2 (`Rule 1` Confirmation Exit):** If `-10%` daily close triggers within `3–8` days of `Peak 2`, confirm Fatal Flat Double-Top—exit remaining tactical swing exposure into **100% Cash Lock** and transition to `CSU-41D` Bear Drawdown Defense.

### CSU-41C: Healthy Wide Continuation ("+13% to +50%+ Breakout Expansion")
* **Trigger Condition A (The Telemetry Scan):**
  1. Following a `>= 12%` correction trough, `Peak 2` breaks decisively **`+13%` to `+50%+` above `Peak 1`** backed by expanding Domestic USD Spot CVD, US Spot ETF inflows (`MOD 07A`), and Pillar 1 `GATE_GREEN` (`MOD 16A`).
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Wide structural expansion (`Wide = Healthy`, matching the 32 mid-bull ATHs of 2024–2025). New capital is repricing Bitcoin into a higher valuation tier.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** Retain core long exposure and trail stops behind `4H/1D` Volume Profile VALs (`MOD 11/18`), applying only tactical `Rule 1` stop-tightening during Week-1 post-ATH leverage flushes.

### CSU-41D: Two-Swing Cycle Harvest & Post-Top Bear Drawdown Protocol ("Active Cycle Map")
* **Trigger Condition A (The Telemetry Scan):**
  1. **Phase A (Post-Top Bear Drawdown — Current Nov 2026 Regime):** Final cycle top confirmed (Oct 6, 2025 `$126,199` flat `+1.4%` double-top + Oct 10 `$102,000` Rule 1 flush -> Jun/Jul 2026 `$57,800–$58,115` `-54.2%` drawdown). Price remains below STH Realized Price (`$75,600`) and 200D MA (`MOD 13B` / `MOD 17`).
  2. **Phase B (Next Post-2028 Halving Bull Cycle Roadmap):** Once secular bull trend reclaims `$126,200`, track the Two-Swing Harvest Roadmap:
     * **Swing 1 (First Run):** Scale out Sell Tranche 1 in the `$172k–$180k` conservative zone (or `$230k–$250k` bull stretch zone); re-accumulate on the `-25%` to `-40%` shakeout dip (`$115k–$125k` conservative / `$138k–$172k` bull).
     * **Swing 2 (Second Run `+4%`):** Scale out Sell Tranche 2 at `+4%` above `Peak 1` (`$179k–$187k` conservative / `$232k–$265k` bull) and enforce `Rule 1` (`-10%` close in `3–8d`) before the `-54%` to `-77%` bear cycle.
* **Execution Rule C (The Non-Negotiable Action):**
  * **During Phase A (Bear Drawdown):** Enforce **100% Cash Lock (`0.00%` risk)** whenever Pillar 1 is `GATE_RED` or `ICDM >= 60` (`MOD 31`), deploying capital only on verified `MOD 03A / 13D / 18B` deep-discount capitulation reclaims or generational cold-storage tranches (`MOD 18D`).

---

## 4. Dynamic Regime Mutation Lookup Matrix (`M1` through `M8`)

| Mutation ID | Initial State | Telemetry Mutation Observed (`Condition A'`) | Mechanical Meaning (`Outcome B'`) | Mandatory Execution Override (`Rule C'`) |
| :--- | :--- | :--- | :--- | :--- |
| **M1: +4% Flat Peak Mutates Into Wide Breakout** | `CSU-41B` (`+4%` Peak 2) | After selling partial tranches at `+4%`, price refuses to trigger Rule 1 (no `-10%` close in 8 days) and surges `> +13%` above Peak 1 on strong USD Spot CVD + ETF inflows. | Double-top exhaustion invalidated (like May -> Jul 2025); bull trend resumed. | **Promote to `CSU-41C`:** Hold remaining BTC runner and trail stops behind `4H/1D` VAL. |
| **M2: Rule 1 Flush Triggered Within 3–8 Days** | `CSU-41A / 41B` (New ATH) | Within `3–8` daily candles of a new ATH (especially a `+1%` to `+6%` Peak 2), daily UTC close finishes `<= -10.0%` below ATH and OI collapses. | Textbook Week-1 leverage flush / fatal double-top breakdown confirmed. | **Execute Full Tactical Exit (100% Cash Lock).** Ban dip-buying until `MOD 03A` reset completes. |
| **M3: Parabolic Single-Spike Blow-Off (`2017` Exception)** | Rapid Vertical Surge | Price doubles (`+100%+`) in `< 30` days with extreme funding (`> +0.05%/8h`), `STH-MVRV >= 1.40`, and `Skew_25D <= -5%`—without waiting for a second peak. | Rare parabolic blow-off top (2017 exception where no second higher ATH prints). | **Ladder Out Heavy Tranches Immediately** and enforce Rule 1 (`-10%` 3-day close) as hard exit trigger. |
| **M4: Mid-Cycle -30% to -55% Shakeout Bottom** | Post-Peak 1 Correction | After Peak 1 (`$175k` or `$230k` zone), price drops `-30%` to `-40%` (`$115k–$125k` or `$138k–$172k`), `STH-MVRV <= 0.85` (`MOD 13D`), and `100–10K` BTC sharks accumulate (`MOD 15C`). | Mid-cycle shakeout trough complete; setup for Swing 2 run to Peak 2 (`+4%`). | **Authorize Buy-Back Tranches** once `MOD 17A` (200D MA) and Domestic USD Spot CVD reclaim positive trend. |
| **M5: Bear Drawdown Old-ATH Support Test** | `CSU-41D` (Bear Market) | During the post-Peak 2 bear crash, price drops `16%–22%` below the previous cycle's ATH (Rule 5 historical floor band) with `LTH-SOPR < 1.0` (`MOD 14 M6`). | Secular bear market approaching historical exhaustion floor. | **Initiate sovereign multi-sig cold-storage accumulation tranches (`MOD 18D`).** |
| **M6: Mini Intra-Cluster Double Top (`< 45d`)** | Inside Active ATH Cluster | Two peaks separated by `14–45` days with `+2%` to `+5%` overshoot followed by a `-10%` close (e.g., Dec 2017 `$16.65k -> $17.99k`). | Tactical intra-cluster distribution wave (`-20%` to `-35%` pullback risk). | **Exit tactical swing position (`MOD 18`) into 100% Cash;** preserve core long-term holdings unless macro cycle Peak 2 triggers. |
| **M7: Record OI Without Spot Follow-Through at ATH** | Day 0 New ATH | Price pokes `+1%` to `+2%` above prior ATH on surging offshore Perp OI (`MOD 02B`) while Coinbase Premium (`MOD 19C`) is negative and US ETFs show outflows. | Classic synthetic/retail ATH trap—highest probability of an immediate Day 3–5 Rule 1 crash. | **Front-Run Rule 1:** Take profits immediately at the marginal new high before the `-10%` close hits. |
| **M8: Post-Bear Secular Reclaim (`> $126,200`)** | `CSU-41D` -> New Cycle | Following the 2026 bear bottom and April 2028 Halving cycle, Bitcoin breaks decisively above `$126,200` on Pillar 1 `GATE_GREEN` and positive US ETF inflows. | New secular bull discovery cycle initiated; activates Swing 1 harvest targets (`$172k–$180k` / `$230k–$250k`). | **Arm `MOD 41` Swing 1 laddered sell zones** and reset ATH cluster tracker to Cluster A. |
