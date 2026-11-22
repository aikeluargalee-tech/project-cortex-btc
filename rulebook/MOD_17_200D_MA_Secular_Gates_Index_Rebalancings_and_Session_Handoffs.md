### PROJECT CORTEX-BTC — MODULE 17: 200D MA SECULAR GATES, INDEX REBALANCINGS & SESSION HANDOFFS
**Waterfall Tier:** Pillar 1 & Pillar 2 Bridge (Secular Trend Regime, Forced Institutional Calendar Flows & Intraday Session Microstructure) cross-verified with Pillar 4. **Empirical Benchmark Anchor:** November 2026 Secular & Session Telemetry — Bitcoin trading below its **200-Day Simple/Exponential Moving Average** during the Q4 2026 drawdown from **$126,080** to **$68,000–$75,000**, exhibiting recurring **Asia/Europe session relief bounces** that are consistently sold during the **New York ETF Cash-Open window (13:30–16:00 UTC)** amid **-$1.44B** in 5-day US Spot ETF redemptions.

--------------------------------------------------------------------------------

#### 1. Machine-Readable State & Routing Block (Python / Hermes / NotebookLM Index)
```yaml
module_id: "MOD_17"
entry_type: "CONDITIONAL_SIGNAL_UNIT"
waterfall_pillar: "PILLAR_1_2_SECULAR_AND_SESSION_TIMING"
title: "200D MA Secular Gates, Index Rebalancings & Session Handoffs (Asia / London / NY)"

# PILLAR 1 MASTER PERMISSION PRE-CHECK
pillar_1_permission_required: true
cash_lock_override: "If Spot < 200D MA AND 200D MA slope < 0, secular regime is BEAR_DEFENSIVE—restrict all Longs to reduced-size (0.375%) capitulation reclaims."

# PRIMARY TELEMETRY TRIGGERS (SECULAR & TEMPORAL STRUCTURE)
base_regime_triggers:
  secular_ma_gate: "Spot Price vs. 200-Day SMA/EMA + 200-Week SMA structural floor"
  forced_flow_calendar: "Quarterly MSCI/S&P/Strategy index rebalancings, Monthly/Quarterly CME & Deribit OpEx (final 48h), Tax/Quarter-End window dressing"
  session_windows_utc:
    ASIA_SESSION: "00:00 - 08:00 UTC (Offshore Perp / Retail & Asian Spot Dominance)"
    LONDON_SESSION: "08:00 - 13:30 UTC (European Institutional & Liquidity Sweep Window)"
    NEW_YORK_SESSION: "13:30 - 21:00 UTC (US Spot ETF Cash Open, CME Futures & Domestic USD Institutional Flow)"

# ANTI-TRAP CIRCUIT BREAKERS
circuit_breakers:
  CB_01_PREMATURE_CLOSE: "NEVER buy a single daily close above the 200D MA without a 3-day acceptance hold or successful pullback retest with positive USD Spot CVD."
  CB_02_VENUE_CONTAMINATION: "Never trust an Asia-session perp pump (00:00-08:00 UTC) until it survives the NY ETF Cash Open (13:30-15:30 UTC) without USD Spot CVD selling."
  CB_03_FORCED_FLOW_STANDDOWN: "Enforce mandatory 24H-48H Stand-Down during passive index rebalancing windows (e.g., MSCI/equity proxy removals) and quarterly OpEx pin hours."
  CB_04_SIGNAL_HALF_LIFE: "Session handoffs govern 4H-24H execution timing; the 200D MA governs multi-month secular risk posture."

# RISK & SIZING CONSTANTS (PILLAR 4)
risk_parameters:
  max_portfolio_risk_pct: 0.75
  below_200d_ma_risk_cap_pct: 0.375
  leverage_permitted: 1.0 # Strict Unleveraged Spot Only
  exit_protocol: "TWO_STAGE_STRUCTURAL"
```

--------------------------------------------------------------------------------

#### 2. Protective Circuit Breakers (Mandatory Pre-Execution Filters)
Before any Scenario in Module 17 can authorize capital deployment, all four circuit breakers must pass:
*   **Circuit Breaker 1 — The 200-Day Moving Average Secular Divider (CB-01):** Across Bitcoin's entire market history, trading above a rising 200D MA defines secular expansion (full 0.75% risk permitted), whereas trading below a declining 200D MA defines capital-preservation defense (maximum 0.375% risk only on extreme capitulation resets, otherwise 100% Cash). *(Cross-reference **`MOD 57 M4`** & **`MOD 68.1`**: Above the 200D SMA, every populated weekly Funding × OI leverage cell collapses to a `49%–51%` coin flip with `0 / 299` weekly crowded-short occurrences; directional crowded-short separation appears exclusively below the 200D SMA.)*
*   **Circuit Breaker 2 — The New York Session Truth Test (CB-02):** In the Spot ETF era, **New York hours (13:30–21:00 UTC)** dictate structural direction. Rallies built on offshore leverage during Asia hours routinely get faded by NY ETF/institutional desks if US flows are negative. Always wait for the NY cash open to validate overnight moves.
*   **Circuit Breaker 3 — Passive Index & Forced Corporate Flow Stand-Down (CB-03):** When major equity/index providers (such as MSCI removals of Bitcoin treasury proxies) or quarter-end institutional rebalancings execute forced mechanical selling, order flow is price-insensitive. Stand down in **100% Cash** until the mechanical rebalancing window closes.
*   **Circuit Breaker 4 — Weekend / CME Gap Discipline:** Avoid initiating swing positions during thin Saturday–Sunday offshore chop; wait for Sunday 22:00 UTC CME futures open and Monday NY liquidity.

--------------------------------------------------------------------------------

#### 3. Core Conditional Signal Units (Condition A -> Outcome B -> Rule C)
##### CSU-17A: Secular 200D MA Reclaim & Retest ("Macro Bull Regime Ignition")
*   **Trigger Condition A (The Telemetry Scan):**
    1. Bitcoin reclaims its **200-Day Moving Average** from below with a strong volume-backed impulse (MOD 08A) and holds above the 200D MA for >= 3 consecutive daily closes.
    2. **Retest Confirmation:** Price pulls back to kiss the **200D MA from above**, where **Domestic Fiat (USD) Spot CVD** and US Spot ETF netflows surge positive (absorbing all sellers) and 1H/4H Volume Profile VAL holds.
*   **Observed Outcome B (The Mechanical Trajectory):**
    *   **Sovereign Macro Lens:** Secular trend-following funds, CTA algorithms, and institutional asset allocators flip from net-short/neutral back to systematic long allocation.
    *   **Probable Trajectory:** Multi-month structural uptrend with high-probability higher lows along the rising 200D MA.
*   **Execution Rule C (The Non-Negotiable Action):**
    *   **Entry Trigger:** Execute **Unleveraged Spot Long** upon the confirmed **15m/1H VAH reclaim off the 200D MA retest**, sized to the full **0.75% Risk Ceiling** with hard structural stop 3%–4% below the 200D MA swing low.
    *   **Two-Stage Profit Exit Protocol:**
        *   **Stage 1 Exit (50% of Position):** Close 50% at +3.0R or STH-MVRV = 1.25; move stop to breakeven.
        *   **Stage 2 Exit (Remaining 50%):** Trail behind 4H/1D Volume Profile VALs while price holds above the 200D MA.

##### CSU-17B: Asia/London Stop Sweep -> New York Institutional Reversal ("NY Absorption Session")
*   **Trigger Condition A (The Telemetry Scan):**
    1. During **Asia (00:00–08:00 UTC)** or **London (08:00–13:30 UTC)** hours, price sweeps downward below the prior day's low / 4H VAL, triggering offshore long liquidations (MOD 03).
    2. **New York Session Reversal (13:30–16:30 UTC):** Immediately upon the US equity/ETF cash open, **Coinbase USD Spot CVD surges vertically positive**, price reclaims the London/Asia range VAL, and A_CVD,OI flips positive.
*   **Observed Outcome B (The Mechanical Trajectory):**
    *   **Sovereign Macro Lens:** US institutional desks used overnight offshore liquidity sweeps to accumulate discounted spot inventory at the NY open.
    *   **Probable Trajectory:** Strong NY-session trend reversal reclaiming the entire overnight drop and squeezing late European/Asian breakdown shorts.
*   **Execution Rule C (The Non-Negotiable Action):**
    *   **Entry Trigger:** Execute **Unleveraged Spot Long** upon the **15m/1H close back above the overnight VAL** between 13:30 and 16:30 UTC, sized strictly to the **0.75% Risk Ceiling** (0.375% if below 200D MA) with stop beneath the overnight sweep low.

##### CSU-17C: Asia Leveraged Perp Pump -> New York Spot Fade ("The Offshore Pump Trap")
*   **Trigger Condition A (The Telemetry Scan):**
    1. During **Asia hours (00:00–08:00 UTC)**, Bitcoin rallies +2% to +5% driven by rising offshore Open Interest (Binance/OKX/Bybit) and positive funding, while **Domestic USD Spot CVD is flat**.
    2. **NY Cash Open Rejection (13:30–15:30 UTC):** At the US market open, **Coinbase USD Spot CVD turns steeply negative**, price loses the Asia session POC/VAL, and A_P,V rolls over negative.
*   **Observed Outcome B (The Mechanical Trajectory):**
    *   **Sovereign Macro Lens:** Offshore retail leverage chased an illiquid overnight bounce directly into waiting US institutional spot/ETF sell programs.
    *   **Probable Trajectory:** Complete retracement of the Asia pump plus a downward stop-hunt through the prior day's low.
*   **Execution Rule C (The Non-Negotiable Action):**
    *   **Action:** **BLOCK ALL MORNING LONG ENTRIES. LOCK 100% CASH.** If holding a tactical position from the prior day, exit immediately upon loss of the Asia POC at the NY open.

##### CSU-17D: Forced Index Rebalancing / Quarterly OpEx Stand-Down ("Mechanical Flow Freeze")
*   **Trigger Condition A (The Telemetry Scan):**
    1. Market is inside a known **forced mechanical flow window**: passive index rebalancing effective date (e.g., MSCI/S&P constituent adjustments), quarter-end institutional rebalancing (final 48 hours of Mar/Jun/Sep/Dec), or quarterly Deribit/CME Options Expiration (final 24 hours before 08:00 UTC Friday settlement).
    2. Order flow shows large, mechanical TWAP selling or extreme pin gravity around Max Pain strikes regardless of intraday sentiment.
*   **Observed Outcome B (The Mechanical Trajectory):** Price action is dominated by non-economic mechanical hedging and forced index flows rather than organic price discovery.
*   **Execution Rule C (The Non-Negotiable Action):**
    *   **Action:** **ENFORCE MANDATORY 24H–48H CASH STAND-DOWN (CB-03).** Wait until the rebalancing deadline or Friday 08:00 UTC OpEx settlement passes, then evaluate the post-settlement volatility release (MOD 12A).

--------------------------------------------------------------------------------

#### 4. Dynamic Regime Mutation Lookup Matrix (M1 through M8)
| Mutation ID | Initial State | Telemetry Mutation Observed (Condition A') | Mechanical Meaning (Outcome B') | Mandatory Execution Override (Rule C') |
| ------ | ------ | ------ | ------ | ------ |
| **M1: 200D MA Death-Cross Rejection** | Below 200D MA | Price rallies up to kiss the **declining 200D MA from below**, prints heavy ask absorption, and **USD Spot CVD turns negative**. | Secular bear ceiling defended by institutional sellers. | **Strict 100% Cash Lock.** Exit any counter-trend bounce immediately at the 200D MA touch. |
| **M2: Failed 200D MA Breakout** | CSU-17A (Reclaim) | Price closes above 200D MA for 1–2 days, then **closes back below 200D MA** on heavy ETF outflows and rising OI. | Secular false breakout ("bull trap above 200D MA"). | **Hard Stop Triggered / Enforce 100% Cash Lock.** |
| **M3: NY Open Confirmation Surge** | Asia/London Rally | Price rallies overnight, dips slightly into 13:30 UTC NY open, holds Asia VAH, and **US Spot ETFs + Coinbase CVD buy aggressively**. | US institutions validated and joined the overnight move ("All-Session Aligned Trend"). | **Authorize Spot Long Entry** on the 13:30–14:30 UTC VAH retest (0.75% Risk Ceiling). |
| **M4: London Stop-Hunt Reversal** | Asia Range Chop | At 08:00–10:00 UTC (London open), price sweeps Asia high/low by 0.5%–1.5% and immediately snaps back inside the Asia range. | Classic European liquidity sweep setting the intraday extreme. | Trade the MOD 11A VAL reclaim only if confirmed by positive USD Spot CVD. |
| **M5: Friday CME Close Pin & Sunday Gap** | Friday 20:00 UTC | Price drifts sharply away from Friday 21:00 UTC CME close over the weekend on thin offshore volume (< 30th pct). | Creates an un-traded CME futures gap prone to 70%+ fill probability within 48 hours of Sunday open. | **Do Not Chase Weekend Gaps**; wait for Sunday 22:00 UTC open and gap-fill absorption. |
| **M6: Post-Index-Rebalance Relief** | CSU-17D (Stand-Down) | Forced index selling deadline passes (e.g., market close on rebalancing day), selling volume vanishes, and **USD Spot CVD steps in**. | Artificial forced seller is completely removed from the order book. | Lift CB-03 stand-down; evaluate 0.375%–0.75% Spot Long on 15m/1H VAH reclaim. |
| **M7: 200-Week MA Sovereign Floor** | Deep Bear Drawdown | Price touches or sweeps the **200-Week Moving Average** (historically ultimate cycle floor) alongside STH-MVRV <= 0.82. | Multi-year generational valuation floor. | Initiate sovereign cold-storage accumulation tranches (MOD 18) once 1D/4H USD Spot CVD stabilizes. |
| **M8: NY Close Institutional Dump** | Intraday Uptrend | Price holds strong all day, then in the final hour (20:00–21:00 UTC NY close), massive spot selling hits to fulfill daily ETF redemptions. | Authorized Participants (APs) executing end-of-day ETF redemption basket sales. | **Tighten Stops Before 20:00 UTC** whenever preliminary ETF flow trackers signal heavy net outflows. |
