# PROJECT CORTEX-BTC — MODULE 41.2: TWO-SWING HARVEST ROADMAP, DIMINISHING MULTIPLES & SECULAR SHAKEOUT ENGINE

**Waterfall Tier:** Pillar 4 (Macro Trend & Cycle Topology) & Pillar 5 (On-Chain Cohorts & Capital Preservation).
**Parent Engines:** Subordinate extension to MOD 41 (ATH Cluster & Flat Double-Top Engine) and MOD 41.1 (Countdown Field Runbook); harmonized with MOD 13 (STH-MVRV), MOD 17 (200D MA Secular Gate), MOD 46 (Block 1,050,000 April 2028 Horizon), and MOD 62 (DIBSE Barbell Allocation).
**Governance Posture:** Strategic Macro Harvest & Capital Allocation Engine. Enforces deterministic multi-tranche scaling at secular peaks and hard-stop protection against post-ATH bear cascades.

---

## 0. Machine-Readable State & Routing Block

```yaml
module_id: "MOD_41.2"
entry_type: "SECULAR_HARVEST_ROADMAP"
waterfall_pillar: "PILLAR_4_AND_PILLAR_5"
title: "Two-Swing Harvest Roadmap, Diminishing Multiples & Secular Shakeout Engine"
parent_modules: ["MOD_41", "MOD_41.1"]

ignition_trigger:
  price_level: 126200.00
  condition: "DAILY_UTC_CLOSE_ABOVE_PRIOR_ATH_WITH_GATE_GREEN"

models:
  conservative:
    multiple_range: [1.36, 1.43]
    swing_1_target: [172000, 180000]
    trough_retrace_pct: [-0.30, -0.35]
    trough_target: [115000, 125000]
    swing_2_target: [179000, 187000]
    secular_bear_floor: [50000, 85000]
  bull_stretch:
    multiple: 1.83
    swing_1_target: [230000, 250000]
    trough_retrace_pct: [-0.25, -0.40]
    trough_target: [138000, 172000]
    swing_2_target: [232000, 265000]
    secular_bear_floor: [98000, 106000]

execution_invariants:
  max_portfolio_risk_per_trade: 0.0075
  leverage_multiplier: 1.0
  tranche_size_peak_2: 0.05
  tranche_count_peak_2: 4
  rule_1_confirmation_retrace: -0.10
```

---

### PART I — ARCHITECTURAL PREMISE & IGNITION TRIGGER

#### Rule 1. Diminishing Cycle Multiples
As Bitcoin's asset scale expands, percentage returns from prior cycle All-Time Highs compress predictably:
* **2017 → 2021:** Multiple of **3.49x** (+248% from $19,798 to $69,000).
* **2021 → 2025:** Multiple compressed to **1.83x** (+83% from $69,000 to $126,199).

#### Rule 2. Ignition Trigger (Cycle Reclaim)
The entire Two-Swing Roadmap formally arms when Bitcoin definitively breaks and holds above the prior cycle peak at **$126,200** with **Pillar 1 GATE_GREEN** and positive US Spot ETF net inflows (MOD 41 Mutation M8).

---

### PART II — THE TWO MASTER CYCLE HARVEST MODELS

| Cycle Phase | Conservative Model (1.36x–1.43x) | Bull Stretch Model (~1.83x) | Structural Telemetry & Action |
| :--- | :--- | :--- | :--- |
| **Swing 1 (Peak 1)** | **$172,000 – $180,000** | **$230,000 – $250,000** | Initial secular ATH cluster; trim tactical swing exposure (50% Stage 1) into euphoric funding. |
| **Mid-Cycle Shakeout Trough** | **$115,000 – $125,000**<br>*(−30% to −35% dip)* | **$138,000 – $172,000**<br>*(−25% to −40% dip)* | Multi-month deleveraging wash; re-accumulate buyback tranches upon 200D MA reclaim. |
| **Swing 2 (Peak 2 / +4% Band)** | **$179,000 – $187,000**<br>*(avg. $184,000)* | **$232,000 – $265,000**<br>*(avg. $240,000)* | Flat overshoot zone (+1.0% to +6.0%); execute laddered tranche distribution (4 × 5%). |
| **Secular Bear Market Floor** | **$50,000 – $85,000**<br>*(−54% to −77% crash)* | **$98,000 – $106,000**<br>*(−54% to −63% crash)* | Generational cycle floor (16%–22% below old $126.2k ATH); deploy Sovereign Multi-Sig Vault tranches. |

---

### PART III — EXECUTION WALKTHROUGH: PHASE BY PHASE

```
  [Break $126.2k] ────────► SWING 1 (Peak 1)
                                │
                                ▼
                       MID-CYCLE SHAKEOUT
                    (-25% to -40% Trough)
                                │
                                ▼ (Re-Accumulate)
                            SWING 2 (Peak 2)
                         (+1% to +6% Flat ATH)
                                │
                                ▼ (Arm Rule 1 Countdown)
                       RULE 1 TRIPWIRE (-10%)
                                │
                                ▼
                       100% CASH LOCK EXPOSURE
```

#### Phase 1: Swing 1 Distribution (Peak 1)
* **Price Behavior:** Bitcoin traverses price discovery toward either **$172k–$180k** (Conservative) or **$230k–$250k** (Bull Stretch).
* **Execution Directives:**
  * **Days 0–2:** Track Coinbase Premium Z-scores and US Spot ETF flows. Harvest Stage 1 tactical profits (**50% off the table**) directly into overheated positive funding (≥ +0.025%) and retail FOMO breakouts.
  * **Days 3–8 (Rule 1 Timer):** Monitor daily 23:59:59 UTC closes. A daily close ≤ -10.0% below the Day 0 ATH high triggers the **Rule 1 First-Week Flush**.
  * **Days 4–9 (Liquidation Wick Zone):** Stand down in cash while cascading liquidation wicks clear leverage by **−17% to −44%**. Core Sleeve B sovereign multi-sig cold storage remains completely untouched.

#### Phase 2: The Mid-Cycle Shakeout & Buyback Zone
* **Structural Context:** Following Peak 1, the market enters a **−25% to −40% correction trough** spanning 32 to 210 days.
* **Trough Targets:**
  * **Conservative:** $115,000 to $125,000.
  * **Bull Stretch:** $138,000 to $172,000.
* **Buyback Authentication (Mutation M4):** Tactical re-accumulation tranches are authorized **only** when all of the following conditions verify:
  1. **On-Chain Reset:** Short-Term Holder MVRV compresses into deep value (STH-MVRV ≤ 0.85 per MOD 13D).
  2. **Cohort Flow:** 100–10,000 BTC shark/whale wallets transition from distribution to net accumulation (MOD 15C).
  3. **Order-Flow Reclaim:** Spot price and Domestic USD Spot CVD decisively reclaim the **200-Day Moving Average** (MOD 17A) and 4H Volume Profile VAH.

#### Phase 3: Swing 2 Distribution (Peak 2 / The Flat +4% Trap)
* **Price Behavior:** The market rallies out of the shakeout trough back up to test or marginally exceed Peak 1.
* **Rule 3 Diagnostic (Flat vs. Wide Overshoot):**
  * **Flat Overshoot (+1.0% to +6.0%, Average +3% to +4%):** Peak 2 clears Peak 1 by only a sliver ($179k–$187k Conservative or $232k–$265k Bull Stretch) with flat or negative Domestic USD Spot CVD.
  * **The Empirical Law:** Historically, a flat overshoot carries a **71% probability of dropping > −20% within 90 days** (median −36.1%) and a **57% probability of crashing −50% to −85% within 500 days**.
* **Execution Directive:**
  * **Laddered Tranches:** Execute partial sales across **four equal tranches of 5% each** (20% total harvest) throughout the +1% to +6% zone. **Never dump 100% on a price target alone** (CB-02), ensuring upside participation remains if it mutates into a wide continuation (+13%+).
  * **Arm Rule 1 Countdown:** Arm the 10-day daily close countdown timer immediately on Day 0 of Peak 2.

#### Phase 4: Final Bear Cycle Confirmation & Defense
* **Execution Trigger (Rule 1 Confirmation):** Within Days 3 to 8 of the Peak 2 high, if a daily UTC close finishes **≤ -10.0% below the ATH**, the fatal flat double top is confirmed (Mutation M2).
* **Mandatory Action:**
  * Immediately lock **100% Cash** on all remaining tactical swing capital (Sleeve A).
  * Stand down on all dip-buying during the subsequent multi-year bear decline toward the secular floor targets ($50k–$85k Conservative or $98k–$106k Bull Stretch).
  * Deploy deep-value sovereign vault tranches into 2-of-3 multi-sig cold storage (Sleeve B) only when price touches the **200-Week SMA / Realized Price** or drops **16% to 22% below the prior cycle's $126,200 ATH**.

---

### PART IV — KEY OPERATIONAL CIRCUIT BREAKERS

1. **Daily Closes Over Hourly Noise (CB-01):** Rule 1 execution is evaluated strictly at **23:59:59 UTC daily close**—never panic-exit or lock cash based on an intraday hourly liquidation wick.
2. **Never 100% All-Out on Price Alone (CB-02):** Always sell in laddered 5% tranches at Peak 2; only the confirmed **Rule 1 daily close (≤ -10%)** authorizes a 100% tactical cash lock.
3. **Temporal Alignment to Block 1,050,000 (MOD 46):** Secular cycle tops historically lag the quadrennial halving by **12 to 18 months**. For the Epoch 5 cycle following the April 2028 halving, this roadmap targets the primary distribution harvest window between **April 2029 and October 2029**.
