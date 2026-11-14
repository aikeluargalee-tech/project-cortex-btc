# PROJECT CORTEX-BTC — MODULE 37: EXECUTABLE LIQUIDITY, NET-3.0R SLIPPAGE & EQUITY-CURVE GOVERNOR
**Waterfall Tier:** Pillar 4 & Tier D Control-Plane Execution & Portfolio-Heat Governor (Verifies L2 executable depth, post-cost `Net R >= 3.0`, stressed stop slippage, and temporal drawdown caps).
**Provenance & Empirical Benchmark Anchor:** Synthesized from the November 13, 2026 Cross-Model Architecture Audit (ChatGPT `MOD 40` + Qwen `MOD 40` + Perplexity `MOD 38`) — ensuring theoretical chart setups survive real-world order-book impact, trading fees, stressed stop-loss slippage, and multi-trade temporal loss limits without ever exceeding the **0.75% Sovereign Risk Shield**.

---

## 1. Machine-Readable State & Routing Block (Python / Hermes / NotebookLM Index)

```yaml
module_id: "MOD_37"
entry_type: "EXECUTABLE_LIQUIDITY_AND_EQUITY_GOVERNOR"
waterfall_pillar: "PILLAR_4_TIER_D_EXECUTION_AND_HEAT_GOVERNOR"
title: "Executable Liquidity, Net-3.0R Slippage & Equity-Curve Governor"

# SUPREME GOVERNANCE PRIORITY
governance_priority: 2 # Sits directly beneath MOD 36 Trust Gate and above MOD 18 Order Entry
advisory_invariant: "Advisory & hard-veto decision governor only; never initiates autonomous orders or raises risk above 0.75%."

# EXECUTABLE LIQUIDITY & POST-COST 3.0R FORMULAS
execution_cost_equations:
  r_planned_usd: "(Position_Size_BTC * Stop_Distance_USD) + Estimated_Roundtrip_Fees_and_Entry_Slippage_USD"
  r_stressed_usd: "(Position_Size_BTC * Stop_Distance_USD) + Stressed_Exit_Slippage_USD + Roundtrip_Fees_USD"
  net_reward_to_risk: "(Target_T2_USD - Expected_Avg_Fill_USD - Roundtrip_Costs_Per_BTC) / (Expected_Avg_Fill_USD - Hard_Stop_USD + Stressed_Slippage_Per_BTC)"

# L2 ORDER BOOK & VENUE HEALTH THRESHOLDS
venue_liquidity_thresholds:
  max_top_of_book_spread_bps: 15.0 # Sustained > 15 bps for 30 min -> DEGRADED / BLOCK
  min_depth_vs_30d_median_pct: 60.0 # Depth down > 40% vs 30D median -> DEGRADED
  max_order_impact_of_10bps_depth_pct: 25.0 # Intended spot order must not consume > 25% of +/-10 bps L2 book depth
  min_net_r_multiple: 3.0 # Hard post-cost asymmetry floor (00C + MOD 18)

# TEMPORAL EQUITY-CURVE & PORTFOLIO HEAT INVARIANTS
equity_governor_limits:
  max_portfolio_heat_pct: 0.75 # Sum of open risk + pending entry risk across ALL positions <= 0.75%
  daily_loss_budget_pct: -1.50 # Day realized + open P&L <= -1.50% (2 full stops) -> 24H FLAT-LOCK
  weekly_loss_budget_pct: -3.00 # Rolling 7D P&L <= -3.00% -> 7-DAY COOLDOWN + MOD 28 Autopsy
  trailing_20_trade_min_avg_winner_r: 2.50 # Below 2.50R over 20 trades -> Strategy Drift Half-Risk (0.375%)

# RISK & SIZING CONSTANTS (PILLAR 4)
risk_parameters:
  max_portfolio_risk_pct: 0.75
  amber_reduced_risk_pct: 0.375
  red_lock_risk_pct: 0.00
  leverage_permitted: 1.0 # Strict Unleveraged Spot Only
```

---

## 2. Protective Circuit Breakers (Execution & Drawdown Invariants)

* **Circuit Breaker 1 — Post-Cost `Net R >= 3.0` Law (`CB-01`):** A setup showing `3.3R` on a clean chart that degrades to `2.6R` after bid-ask spread, L2 book walk, maker/taker fees, and stressed stop slippage is **mathematically negative-expectancy** under your system. `MOD 37` blocks any entry where `Net_R < 3.0`.
* **Circuit Breaker 2 — Portfolio-Wide Heat Ceiling (`CB-02`):** Multiple staggered or re-entered tranches (`e.g., T1 + T2`) can never sum to more than **`0.75%` total portfolio equity at risk** (`0.375%` in Amber regimes). If an existing tranche still carries `0.40%` open risk, a secondary add is capped at `0.35%`.
* **Circuit Breaker 3 — Temporal Loss Budgets (`CB-03`):** Per-trade caps do not stop clustering losses during hostile regime transitions. Hitting **`-1.50%` daily P&L** triggers a mandatory **24-hour `FLAT-LOCK`**, and hitting **`-3.00%` rolling 7-day P&L** enforces a **7-day cooldown + `MOD 28` Autopsy**.
* **Circuit Breaker 4 — Cold Reserve vs. Execution Float Isolation (`CB-04`):** Operational trading capital is strictly bounded to a prefunded spot execution float; `MOD 37` never assumes instant access to 2-of-3 multi-sig cold reserves (`72-hour operational wall`, `MOD 32`).

---

## 3. Core Conditional Signal Units (`Condition A -> Outcome B -> Rule C`)

### CSU-37A: Executable Depth Degradation or Net-R Collapse (`NEW_ENTRY = BLOCKED`)
* **Trigger Condition A (The Telemetry Scan):**
  1. Top-of-book spread widens above **`15 bps`** for `30+ minutes`, **OR** `1%` L2 book depth drops **`> 40%` below its 30-day median**, **OR** intended spot order size exceeds **`25%` of `+/-10 bps` L2 depth**.
  2. Recomputing entry/stop/target with realistic L2 book walk and fees yields **`Net_R < 3.0`** or **`R_stressed > 0.75%` (`0.375%` Amber)**.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Execution Lens:** Thin book and adverse selection will eat the theoretical chart edge via entry/exit slippage.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **BLOCK NEW ENTRY (`MOD_37_STATE = RED`)** or scale down order size / switch strictly to passive post-only limit ladder (`MOD 21`) until `Net_R >= 3.0` and `R_stressed <= approved_risk_budget`.

### CSU-37B: Daily or Weekly Loss Budget Exhausted ("Temporal Drawdown Lock")
* **Trigger Condition A (The Telemetry Scan):**
  1. Intraday realized + unrealized P&L reaches **`<= -1.50%`** of portfolio equity (`two full 0.75% stops`), **OR** rolling 7-day P&L reaches **`<= -3.00%`**.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Governance Lens:** Strategy is out of phase with market microstructure or experiencing a regime transition; continuing to trade risks compounding tilt/whipsaw losses.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **ENFORCE `FLAT-LOCK` (Overrides all `MOD 33` entry permissions):**
    * If Daily `-1.50%` breached: **24-hour hard lock** (`0.00%` new risk).
    * If Weekly `-3.00%` breached: **7-day hard cooldown** + mandatory `MOD 28` Live Autopsy before re-arming.

### CSU-37C: Portfolio Heat Invariant Breach ("Stacked Tranche Cap")
* **Trigger Condition A (The Telemetry Scan):**
  1. Proposed new order risk plus existing open-position risk (`measured to hard stops`) exceeds **`0.75%` of total equity** (`or 0.375%` under Amber regimes).
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Governance Lens:** Stacked re-entries would breach the single-event Sovereign Risk Shield if a sudden gap hits all stops simultaneously.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **REJECT OR TRIM INCREMENTAL ORDER** so `Total_Open_Portfolio_Heat <= Max_Approved_Risk_Pct` (`0.75%` or `0.375%`).

### CSU-37D: Realized Expectancy / CUSUM Drift Warning ("Exit-Engine Recalibration")
* **Trigger Condition A (The Telemetry Scan):**
  1. Over a trailing window of `20` completed trades, realized average winner drops below **`2.50R`** (design target `>= 3.0R`) or cumulative sum (`CUSUM`) of `(R_i - E[R])` breaches control limit `h`.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Governance Lens:** Either stops are too tight for current Garman-Klass volatility (`MOD 12`) or Stage 1/Stage 2 exits are cutting winners prematurely.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **THROTTLE MAX RISK TO `0.375%` (`AMBER`)** and trigger `MOD 18` exit-parameter calibration review until `20` validated trades restore expectancy.

---

## 4. Dynamic Regime Mutation Lookup Matrix (`M1` through `M8`)

| Mutation ID | Initial State | Telemetry Mutation Observed (`Condition A'`) | Mechanical Meaning (`Outcome B'`) | Mandatory Execution Override (`Rule C'`) |
| :--- | :--- | :--- | :--- | :--- |
| **M1: Pre-Event Depth Evaporation** | `GREEN` (Valid Setup) | 15 minutes before a macro print, L2 `1%` bid depth drops `-45%` (`like Nov 13's thin $72M book`), pushing `R_stressed` to `1.15%`. | Stop-loss slippage risk jumped 50% above the `0.75%` ceiling. | **Automatically Scale Down BTC Size by 35%** (or abort) so `R_stressed <= 0.75%`. |
| **M2: Passive Limit Slice Rescue** | `AMBER` (Size > 25% of 10bps book) | Single market/aggressive limit order would walk 18 bps of book, dropping `Net_R` from `3.2R` to `2.7R`. | Market impact destroys `3.0R` asymmetry if executed in one clip. | **Route to `MOD 21` TWAP / Post-Only Ladder** (`3` child slices); approve only if blended `Net_R >= 3.0`. |
| **M3: Breakeven Stop Frees Portfolio Heat** | `CSU-37C` (Heat at `0.75%`) | Open Trade 1 hits Stage 1 (`50%` banked) and its trailing stop moves strictly **above entry price (`risk-free / locked profit`)**. | Open downside risk on Trade 1 is now `0.00%` of equity. | **Reset Trade 1 Open Heat to `0.00%`**, unlocking fresh `0.75%` risk budget for a new setup. |
| **M4: Daily Lock Override Attempt** | `CSU-37B` (`-1.50%` Daily Lock) | A textbook `CONFIG_J` Bear Trap prints 4 hours after hitting `-1.50%` daily loss limit. | High-conviction setup appears during mandatory cooling-off period. | **Hard Veto Preserved:** Never bypass the `24h` daily lock; log missed setup for `MOD 28` review. |
| **M5: Exchange API Rate-Limit / Reject Spike** | `GREEN` | Primary execution venue returns HTTP `429/5xx` errors or order-ack latency exceeds `1500 ms`. | Venue execution reliability degraded; stop/exit updates could fail. | **Set `MOD_37_STATE = RED` (`Venue Degraded`)**; halt new entries until venue API latency normalizes `< 300 ms`. |
| **M6: Stressed Stop Gap Adjustment** | Active Open Swing | Weekend or macro volatility doubles Garman-Klass APR (`MOD 12 M5`), increasing expected stop-out slippage. | Historical 20 bps stop-slippage buffer is now too narrow for live volatility. | **Recompute `R_stressed` with `2.0x` slippage buffer**; trim partial exposure if `R_stressed` exceeds `0.90%`. |
| **M7: Fee-Tier / Zero-Fee Pair Shift** | Routine Audit | Execution venue changes maker/taker fee schedule on `BTC/USD` or `BTC/USDT`. | Roundtrip transaction cost changes `Net_R` threshold calculations. | Update `roundtrip_fee_bps` constant in `btc_config.json` before next live entry evaluation. |
| **M8: Post-Cooldown Half-Risk Ramp** | Exiting `7-Day` Weekly Lock | 7-day cooldown and `MOD 28` autopsy complete cleanly. | Re-entering live markets after a `-3.0%` drawdown requires controlled re-acclimation. | **Cap First 5 Post-Cooldown Trades at `0.375%` Risk** (`Half-Risk`) before restoring full `0.75%` ceiling. |
