##### PROJECT CORTEX-BTC — MODULE 65: MEDIA DE-NOISING, NARRATIVE TRIAGE & SIGNAL HYGIENE PROTOCOL
**Waterfall Tier:** Tier D Meta-Governance, Media Audit & Signal Hygiene Gate (Filtering External Market Updates, Model Category Errors, Single-Candle Traps, Statistical Claim Flaws & Narrative Overreach Before Pillar 1–5 Ingestion) — harmonized with MOD 35 (Heatmap Distance Rule), MOD 36 (Telemetry Trust & Staleness SLA), MOD 41 (Candle-Close Confirmation), MOD 52 (Rolling 30-Trade Expectancy & Empirical Sample Hygiene), MOD 54 (Multi-Timeframe Kline Lock), MOD 56 (Anti-Narrative Discipline), MOD 60 (7-Rank Veto Precedence Ladder), MOD 61 (Data Hub Ingestion & Hygiene Gate), and MOD 68 (Derivatives Positioning Context & Tail-Only Funding Mechanics).
**Document Provenance:** Codified from `Bitcoin-Educational-Article.md` (*Bitcoin in a Downtrend: How to Read Liquidity, ETF Flows, and Sentiment Without Getting Fooled*, Nov 2026 empirical case study) and upgraded via `funding-rates-and-open-interest.md` (Nov 2026 empirical funding/OI hygiene audit).
**Governance Posture:** Mandatory Pre-Ingestion Media & Commentary Firewall. Prevents viral YouTube/X/blog narratives, stale multi-year heatmap projections, unconfirmed single-candle CHoCH calls, backward-looking sentiment readings, and statistically flawed backtest/funding claims from bypassing MOD 60 upstream vetoes or triggering premature Sleeve A USDT deployment.

--------------------------------------------------------------------------------

###### 1. Machine-Readable State & Routing Block (Python / Hermes / NotebookLM Index)
```yaml
module_id: "MOD_65"
entry_type: "MEDIA_DENOISING_AND_SIGNAL_HYGIENE_GOVERNOR"
waterfall_pillar: "TIER_D_MEDIA_TRIAGE_AND_SIGNAL_HYGIENE"
title: "Media De-Noising, Narrative Triage & Signal Hygiene Protocol"

# MOD 60 PRECEDENCE & HYGIENE REGISTRATION
governance_registration:
  mod_60_precedence_rank: "PRE_INGESTION_HYGIENE_GATE_TO_MOD_61"
  upstream_veto_subordination: "External commentary, sentiment troughs, or single-indicator divergences NEVER override MOD 60 Ranks 0-3 (MOD 36 DATA HALT, MOD 16 GATE_RED, ICDM >= 60, MOD 44/58 Event Lock, or MOD 34/51 Active Cascade)."
  standalone_trade_authorization: false # Strictly prohibited; acts as a narrative & model-hygiene firewall

# 6-QUESTION MEDIA & EMPIRICAL AUDIT GATE (MANDATORY BEFORE LOGGING EXTERNAL CLAIMS)
media_audit_checklist:
  q1_timeframe_separation: "Are Higher-Timeframe (1D/1W), Tactical Swing (4H/1H), and Long-Term Accumulation horizons explicitly separated without goalpost shifting?"
  q2_deterministic_trigger: "Does the claim define an exact candle-close confirmation and hard invalidation level (wicks excluded per MOD 41 CB-01 / MOD 54)?"
  q3_primary_source_verification: "Are ETF flows (Farside/SoSoValue), derivatives (CoinGlass/exchange specs), and sentiment (Alternative.me) traced to primary feeds rather than unverified commentary?"
  q4_falsifiability_condition: "Does the thesis state an explicit 'I am wrong if...' invalidation line alongside the alternative scenario?"
  q5_risk_and_horizon_completeness: "Does the analysis account for position sizing (<= 0.75% cap), liquidity friction, and time horizon—or is it entertainment?"
  q6_empirical_sample_and_formula_hygiene: "If quoting win rates or historical studies, does it report denominator/CI, discount overlapping windows, count distinct episodes, compute payoff-adjusted EV, and respect venue formula mechanics (e.g., Binance +0.01%/8h funding clamp)?"

# MODEL vs. FACT SEPARATION THRESHOLDS
hygiene_constants:
  heatmap_lookback_skepticism_days: 30 # Heatmaps > 30d (especially 1Y-2Y) carry stale closed-OI ghost bands (MOD 35 CB-01)
  choch_sequence_steps_required: 2 # Step 1: Pivot break close (CHoCH) -> Step 2: Higher Low + Higher High (never 1-step)
  sentiment_extreme_fear_ceiling: 20 # Backward-looking stretch indicator only; zero standalone entry authority
  etf_flow_lag_and_reflexivity: "T+1 settlement & price-flow feedback loop; single-day flips (e.g., +$8M) do not break multi-day trends"
  funding_formula_clamp_8h_pct: 0.01 # Binance/OKX default 8h interest rate (+0.03%/day); >+0.03%/day is NOT an extreme upper tail (MOD 68 CB-03)

# RISK & SIZING CONSTANTS (PILLAR 4)
risk_parameters:
  narrative_only_max_risk_pct: 0.00 # Strict 100% Cash Lock if thesis fails the Media Audit
  leverage_permitted: 1.0 # Strict Unleveraged Spot Only
```

--------------------------------------------------------------------------------

###### 2. Protective Circuit Breakers (External Commentary & Indicator Anti-Trap Rules)
*   **Circuit Breaker 1 — Model-vs.-Order-Book Translation Filter (CB-01):** Never treat liquidation heatmaps, cycle curves, or oscillator bands as resting order-book liquidity or deterministic timetables. Translate any headline claiming *"$X billion of liquidity sits at Price Y"* into: *"The provider's leverage model estimates $X billion would liquidate if price traded at Price Y, using entry/OI assumptions that may be stale—especially on multi-year (1Y–2Y) lookbacks."* (Cross-locked with **MOD 35 CB-01**).
*   **Circuit Breaker 2 — Single-Candle CHoCH & Moving-Goalpost Ban (CB-02):** A single candle close above a lower high (**CHoCH**) or a single higher low is an early structural clue—**not** confirmation of a new bull market. Require a two-step structural sequence (**CHoCH close → Higher Low → Higher High**) on the governing timeframe (MOD 54), and lock invalidation triggers upfront so analysts cannot shift bull-confirmation goalposts downward mid-downtrend (e.g., shifting from $87k daily close to a $66k bounce).
*   **Circuit Breaker 3 — Oversold RSI Extension vs. Timing Filter (CB-03):** Daily RSI < 30 measures downside velocity and extension, **not** a calendar reversal date. In active downtrends (MOD 17 below 200D SMA), oversold bounces routinely form lower highs before rolling over. Use RSI strictly to avoid chasing late breakdown shorts—never as a standalone spot buy trigger.
*   **Circuit Breaker 4 — Backward-Looking Sentiment & Reflexive ETF Flow Filter (CB-04):** Extreme Fear readings (e.g., Crypto Fear & Greed <= 11) and single-day ETF flow pauses (e.g., +$7.9M after -$1.91B in outflows) reflect *past* price pain and T+1 reflexive redemptions, not forward capital commitments. Use sentiment exclusively as a **personal-bias audit** (*"Am I reacting to structure or to red candles?"*), never as an entry timer (MOD 56 CB-02).
*   **Circuit Breaker 5 — Multi-Horizon Frame Separation Lock (CB-05):** Strictly decouple **Long-Term Sovereign Accumulation (Sleeve B)**, **Daily Structural Regime (Pillar 1/2)**, and **Intraday Tactical Execution (Sleeve A)**. Never allow a long-term *"generational discount"* narrative to justify premature tactical buying while daily structure and macro gates (MOD 16 / MOD 31 / MOD 64) remain GATE_RED.
*   **Circuit Breaker 6 — Statistical Claim & Exchange-Formula Hygiene Filter (CB-06):** Reject or flag any quantitative claim, X thread, or educational study that: (a) quotes a hit rate without sample denominator $n/N$, 95% confidence interval, or payoff-adjusted EV (`MOD 52 CB-05`); (b) samples overlapping multi-day forward returns daily without overlap correction or cluster-episode deduplication; or (c) misinterprets exchange-formula artifacts—such as treating Binance's `+0.01%/8h` (`+0.03%/day`) clamped interest-rate baseline as a "zero-centered" scale or using `> +0.03%/day` to claim positive funding does not signal upper-tail fragility (`MOD 68 CB-03`).

--------------------------------------------------------------------------------

###### 3. Core Conditional Signal Units (Condition A -> Outcome B -> Rule C)
###### CSU-65A: Media Narrative Failure ("Entertainment-Only / Unfalsifiable Update")
*   **Trigger Condition A (The Telemetry Scan):**
    1. An external video, post, or article fails >= 2 items on the **6-Question Media & Empirical Audit Gate** (e.g., mixes 15m bounce talk with 4-year cycle claims, cites 2-year heatmap clusters as guaranteed magnets, shifts invalidation goalposts, quotes unverified hit rates without denominator/EV, or omits risk sizing).
*   **Observed Outcome B (The Mechanical Trajectory):**
    *   **Cognitive & Execution Risk:** Ingesting uncalibrated commentary induces premature dip-buying into LVN air pockets or emotional capitulation at local sentiment troughs.
*   **Execution Rule C (The Non-Negotiable Action):**
    *   **Action:** **QUARANTINE & DISCARD NARRATIVE.** Assign **0.00% execution weight**; extract only verifiable primary-source data points (if any) into 00H after cross-checking against MOD 36 and MOD 61.

###### CSU-65B: Multi-Step Structural Reversal Sequence ("CHoCH-to-Trend Verification")
*   **Trigger Condition A (The Telemetry Scan):**
    1. Price prints a **Daily or 4H candle close** (wicks excluded) above the last Lower High (**Bullish CHoCH**), **AND**
    2. Subsequent pullback holds a verified **Higher Low** above prior swing support with positive Domestic USD Spot CVD (MOD 05/MOD 07), followed by a **Higher High** close.
*   **Observed Outcome B (The Mechanical Trajectory):**
    *   **Microstructure Lens:** Transitions market structure from an oversold downtrend bounce (lower-high rollover trap) into a validated two-step trend reversal.
*   **Execution Rule C (The Non-Negotiable Action):**
    *   **Action:** **PASS TO PILLAR 4 SIZING GATE (MOD 18 / MOD 62).** Authorize tactical Sleeve A spot deployment (0.375%–0.75% risk, Net R >= 3.0) *only* after verifying MOD 60 Ranks 0–3 (MOD 16, MOD 31 ICDM, MOD 44, MOD 64) are no longer GATE_RED.

###### CSU-65C: Extreme Fear Personal-Bias Audit ("Sentiment Stretch Protocol")
*   **Trigger Condition A (The Telemetry Scan):**
    1. Crypto Fear & Greed Index prints <= 15 (Extreme Fear) while 1D/4H structure remains below descending trendlines and 200D SMA (MOD 17), with net ETF flows negative (MOD 07).
*   **Observed Outcome B (The Mechanical Trajectory):**
    *   **Behavioral Lens:** Crowd pessimism is stretched, creating high probability of violent short-covering bounces that fail beneath HTF resistance (MOD 35 M3).
*   **Execution Rule C (The Non-Negotiable Action):**
    *   **Action:** **HOLD 100% CASH LOCK ON SLEEVE A (0.00% Risk); PROTECT SLEEVE B COLD STORAGE.** Do not panic-sell core cold storage into extreme fear, and do not deploy tactical USDT until CSU-65B structural sequence + MOD 03/MOD 14 exhaustion confirm.

--------------------------------------------------------------------------------

###### 4. Dynamic Regime Mutation Lookup Matrix (M1 through M5)
| Mutation ID | Initial State | Telemetry Mutation Observed (Condition A') | Mechanical Meaning (Outcome B') | Mandatory Execution Override (Rule C') |
| ------ | ------ | ------ | ------ | ------ |
| **M1: Oversold Bounce Rollover Trap** | Daily RSI < 30 + Fear <= 15 | Price bounces +3% to +6% off support on a wick, **fails to close 1D/4H above prior Lower High**, and rolls over with negative Spot CVD. | Classic downtrend oversold relief bounce forming a new Lower High (not a reversal). | **Maintain 100% Cash Lock;** treat unclosed wicks above resistance as invalid rejections (CB-02). |
| **M2: False ETF Flow Dawn** | Multi-Day ETF Outflow Streak | Spot ETFs print a single barely positive session (e.g., +$8M after -$1.9B outflows), followed immediately by renewed redemptions (-$240M). | T+1 settlement noise / single-issuer rebalance rather than sustained institutional accumulation. | **Require >= 2 Consecutive Sessions of > +$100M Net Inflows + Coinbase Premium >= 0%** before lifting ETF outflow caution (MOD 31 M2). |
| **M3: Stale Multi-Year Heatmap Panic** | 2Y Heatmap Shows Distant Cluster | Viral updates highlight a multi-billion-dollar cluster 15%–20% below spot on a 1Y/2Y heatmap while nearer shelves sit 2%–5% away. | Model carry-forward artifact from historical OI (CB-01 / MOD 35 M7), not an immediate execution magnet. | **Filter Distant Band via MOD 35 Pull_Score;** anchor invalidation and watch levels strictly to active nearest shelves. |
| **M4: Goalpost Shift / Thesis Drift** | Bearish HTF Bias Active | Commentator keeps HTF bearish label while simultaneously pitching leveraged dip-buys without an explicit invalidation trigger. | Conflation of long-term DCA horizon with short-term tactical execution (CB-05). | **Reject Trade Signal;** enforce strict Sleeve A (tactical) vs. Sleeve B (sovereign cold storage) separation (MOD 62). |
| **M5: Validated Two-Step Reversal** | CSU-65C (Extreme Fear) | Price closes 1D above CHoCH level, prints a Higher Low on rising USD Spot CVD, ETF outflows flip to multi-day inflows, and ICDM < 55. | Sentiment trough + structural sequence + institutional flow alignment confirmed. | **Graduate from MOD 65 Quarantine to MOD 18 / MOD 62 Active Execution.** |

--------------------------------------------------------------------------------

###### 5. Operational 5-Minute Media & Empirical Triage Checklist (Quick-Reference Audit Table)
| Audit Gate | Diagnostic Question | Pass Requirement (Ingest to 00H / MOD) | Fail Action (Discard / Quarantine) |
| ------ | ------ | ------ | ------ |
| **1. Timeframe** | Is the governing chart horizon (1D, 4H, 15m, or multi-year cycle) explicitly isolated? | Explicit separation of tactical swing vs. multi-year DCA. | Reject mixed-horizon narratives (CB-05). |
| **2. Trigger** | Is there an exact **candle-close** confirmation and invalidation price? | Closed bar confirmation (1D/4H) with hard stop level. | Ignore wick pokes and open-ended ranges (CB-02). |
| **3. Source** | Are numbers traced to verifiable feeds (Farside, CoinGlass, Glassnode, FRED, exchange specs)? | Verifiable primary telemetry matching MOD 36 SLA. | Discard unverified screenshots or viral estimates. |
| **4. Alternative** | Is an explicit *"I am wrong if..."* invalidation scenario defined? | Two-sided conditional logic (If A -> B; if not A -> C). | Classify as entertainment; assign 0.00% weight. |
| **5. Risk & Sizing** | Are position sizing (<= 0.75%), Net R >= 3.0, and liquidity depth addressed? | Aligned with MOD 18 / MOD 37 unleveraged spot rules. | Block execution; never size off media conviction. |
| **6. Sample & Formula Hygiene** | Are denominator $n/N$, overlap discount, episode count, payoff EV, and venue formula clamps checked? | Passes MOD 52 CB-05 & MOD 68 CB-03/CB-05 audit. | Flag statistical/formula flaw in 00H; block sizing weight (CB-06). |

--------------------------------------------------------------------------------

###### FINAL DIRECTIVE
**MOD 65 separates market mechanics from market theater. Models estimate, oscillators measure extension, sentiment reflects the past, uncalibrated sample counts flatter noise, and only multi-step candle-close structure backed by verified spot flow authorizes capital.**
