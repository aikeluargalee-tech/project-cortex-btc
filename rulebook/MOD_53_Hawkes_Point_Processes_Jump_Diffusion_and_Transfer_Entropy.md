# PROJECT CORTEX-BTC — MODULE 53: HAWKES POINT PROCESSES, JUMP-DIFFUSION DE-NOISING & TRANSFER ENTROPY CAPITAL ROTATION ENGINE
**Waterfall Tier:** Pillar 1 (Macro Liquidity & Cross-Asset Rotation) and Pillar 2 (Microstructure, Path Geometry & Order Flow).  
**Empirical Benchmark Anchor:** Codifies the mathematical separation of endogenous derivatives leverage cascades from exogenous spot accumulation. Solves standard chart blindness during high-volatility liquidity shocks (e.g., flash deleveraging flushes) and external capital suction events (e.g., mega-equity IPOs and index rebalances). Replaces discretionary chart interpretation with Hawkes self-exciting point processes, jump-diffusion drift separation, and cross-asset transfer entropy.

---

## 1. Machine-Readable State & Routing Block (Python / Hermes / NotebookLM Index)

```yaml
module_id: "MOD_53"
entry_type: "CONDITIONAL_SIGNAL_UNIT"
waterfall_pillar: "PILLAR_1_MACRO_AND_PILLAR_2_MICROSTRUCTURE"
title: "Hawkes Point Processes, Jump-Diffusion De-Noising & Transfer Entropy Capital Rotation Engine"

# COMPUTATIONAL & TELEMETRY PARAMETERS
computational_parameters:
  hawkes_microstructure_filter_a:
    shock_detection_atr_multiplier: 2.0 # 4H candle range > 2.0x 14-period ATR
    shock_detection_absolute_move_pct: 2.5 # 4H absolute price change > 2.5%
    mandatory_cooling_window_candles: 2 # 8 hours (2x 4H candles) freeze on breakout chasing
    whipsaw_retrace_threshold_pct: 60.0 # Price retraces > 60% of shock candle within 8h on declining volume
    rejection_wick_ratio_threshold: 0.55 # Wick > 55% of candle range = stop harvest
    oi_flush_drop_threshold_pct: -3.0 # Aggregate OI drops > 3.0% during move
    sustainable_trend_funding_range_pct: [-0.010, 0.025] # 8h perp funding band
    sustainable_trend_cvd_confirmation_candles: 2 # Consecutive 4H spot CVD closes

  transfer_entropy_rotation_filter_b:
    etf_net_inflow_inflection_consecutive_days: 2
    etf_net_inflow_minimum_daily_usd: 100000000 # >= +\$100M/day (IBIT/FBTC composite)
    stablecoin_7d_net_supply_expansion_pct: 0.5 # Combined USDT + USDC
    exchange_stablecoin_reserve_direction: "EXPANDING" # Staging on-exchange
    cross_asset_relative_strength:
      pair: "BTC/QQQ"
      condition: "Daily higher low AND daily close > 10-day EMA"
    rotation_confirmation_threshold: 2 # Minimum 2 of 3 sub-triggers met

# ANTI-TRAP CIRCUIT BREAKERS
circuit_breakers:
  CB_01_HAWKES_AFTERSHOCK_FREEZE: "Never execute market breakout orders during an active Hawkes shock (4H range > 2.0x ATR or > 2.5% move). Enforce a mandatory 8-hour cooling timer."
  CB_02_SPOT_CVD_CONFIRMATION_MANDATE: "A price thrust accompanied by contracting Open Interest (OI delta < -3%) and flat/divergent Spot CVD is classified as a synthetic liquidation flush. Breakout buying is strictly banned."
  CB_03_TWO_SESSION_ETF_ROTATION_GATE: "Following an external macro/IPO capital drain, never front-run capital return until US Spot ETFs register 2 consecutive sessions of net inflows exceeding +\$100M/day."
  CB_04_STRICT_UNLEVERAGED_SPOT_BARBELL: "Enforce 1.0x unleveraged spot allocation only. When Filter B indicates Suction Active, risk is capped at 0.00% (Cash) or 0.375% (Half-Size Defensive Wicks)."

# RISK & SIZING CONSTANTS (PILLAR 4)
risk_parameters:
  max_portfolio_risk_pct: 0.75
  half_size_swing_risk_pct: 0.375
  leverage_permitted: 1.0 # Strict Spot Only
  stop_loss_placement: "1.0 ATR below the Hawkes shock origin or structural swing low"


```

--------------------------------------------------------------------------------

####  **2. Protective Circuit Breakers (Mandatory Pre-Execution Filters)**
Before any trade signal can be authorized under this engine, all four circuit breakers must evaluate clean:
*   **Circuit Breaker 1 — The Hawkes Aftershock Cooling Lock (**   **CB-01**   **):**  In crypto derivatives markets, initial price breaks trigger chain-reaction forced liquidations (self-exciting aftershocks). When a single 4H candle exceeds  **2.0x 14-period ATR**  or prints an absolute move  **> 2.5%** , the market is in an endogenous shock state. All breakout market orders are frozen for  **2 candles (8 hours)** .
*   **Circuit Breaker 2 — Spot CVD Confirmation Mandate (**   **CB-02**   **):**  If price moves violently while aggregate Open Interest drops  **> 3.0%**  and Domestic USD Spot CVD diverges, the move is driven by leveraged stop-harvesting, not institutional accumulation. Chasing moves with a rejection wick  **> 55%**  of the total candle range is strictly prohibited.
*   **Circuit Breaker 3 — Two-Session ETF Inflow Rule (**   **CB-03**   **):**  During external capital drains (e.g., mega-IPOs or equity rebalancing windows), single-day green ETF prints are frequently noise. Re-entry requires  **2 consecutive trading days**  of US Spot ETF net inflows  **> +$100M/day** .
*   **Circuit Breaker 4 — Strict Spot-Only Execution Gate (**   **CB-04**   **):**  Leveraged positioning is barred. If capital suction is active and microstructure indicates whipsaw, portfolio posture must remain  **100% Cash / Invariant Patience** , with execution limited exclusively to passive deep-discount limit bids ("stink-bids").

--------------------------------------------------------------------------------

####  **3. Core Conditional Signal Units (Condition A -> Outcome B -> Rule C)**
#####  **CSU-53A: Hawkes Liquidation Shock & Whipsaw Invalidation (Filter A)**
*   **Trigger Condition A (The Telemetry Scan):**
    *   **Shock Detection:**  A 4H candle range exceeds  **2.0x 14-period ATR**  or executes an absolute price thrust  **> 2.5%** .
    *   **Whipsaw Invalidation Criteria (At least 2 of 3 met):**
    *  Aggregate Open Interest drops  **> 3.0%**  within the 4H window while Spot CVD fails to reach a new local extreme (MOD 05).
    *  The candle closes with an upper or lower rejection wick accounting for  **> 55%**  of the total candle range.
    *  Price retraces  **> 60%**  of the shock candle within the 8-hour cooling window on contracting volume.
*   **Observed Outcome B (The Mechanical Trajectory):**
    *   **Microstructure Lens:**  An endogenous liquidation cascade (Hawkes aftershock cluster) where market makers harvest thin stop liquidity. The move lacks organic spot backing and mean-reverts once liquidations exhaust.
*   **Execution Rule C (The Non-Negotiable Action):**
    *   **Classify as WHIPSAW (Fakeout).**  Block all directional breakout buying. Maintain core spot inventory untouched. Rest deep-value limit bids below support to capture liquidation wicks (MOD 51).
#####  **CSU-53B: Transfer Entropy Macro Capital Rotation Re-Entry (Filter B)**
*   **Trigger Condition A (The Telemetry Scan):**  Following an external capital vacuum event (e.g., mega-IPO window under MOD 44), monitor the 3 core plumbing gauges:
    *   **US Spot ETF Net Inflows:**  Record  **>= 2 consecutive US trading sessions**  of net inflows  **> +$100M/day**  (composite IBIT/FBTC/ARKB).
    *   **Stablecoin Supply Expansion:**  7-day net issuance of USDT + USDC expands by  **> +0.5%** , with exchange stablecoin reserves showing a net 72-hour increase (MOD 48).
    *   **Cross-Asset Relative Strength:**  The daily  **BTC/QQQ ratio**  prints a confirmed higher low and closes above its  **10-day EMA** .
*   **Observed Outcome B (The Mechanical Trajectory):**
    *   **Macro Plumbing Lens:**  Transfer entropy flips positive. External liquidity suction has peaked; institutional allocators and retail liquidity are rotating capital out of fiat/equities and back into Bitcoin spot rails.
*   **Execution Rule C (The Non-Negotiable Action):**
    *   **If 0 or 1 Trigger Met (Suction Active):**  Capital preservation protocol active. Treat upward price thrusts as low-liquidity relief rallies. Restrict deployment to defensive tranches on extreme wicks.
    *   **If >= 2 Triggers Met (Rotation Confirmed):**  Green-light transition to active spot accumulation. Authorize full 0.75% portfolio risk deployment when aligned with microstructure gates.
#####  **CSU-53C: Full Breakout Alignment (Dual-Gate Macro-Micro Confluence)**
*   **Trigger Condition A (The Telemetry Scan):**
    *   **Filter A Status = REAL SPOT TREND:**  Spot CVD trends positively across  **>= 2 consecutive 4H closes** , OI expands steadily without funding overheating (8h funding between  **-0.01% and +0.025%** ), and wick ratio remains  **< 45%** .
    *   **Filter B Status = ROTATION CONFIRMED:**  At least 2 of 3 transfer entropy liquidity conditions are verified positive.
*   **Observed Outcome B (The Mechanical Trajectory):**
    *   **Confluence Lens:**  High-conviction structural expansion. Exogenous spot capital inflows absorb passive overhead resistance, while derivatives positioning provides healthy fuel without excessive leverage fragility.
*   **Execution Rule C (The Non-Negotiable Action):**
    *   **Execute Full Spot Swing Deployment:**  Authorize standard  **0.75% Portfolio Risk**  (MOD 18). Place initial hard stop-loss  **1.0 ATR**  below the breakout base. Trail stops behind 4H Volume Profile VAL/POC levels (MOD 11).

--------------------------------------------------------------------------------

####  **4. Combined 4-Quadrant Execution Matrix (Filter A × Filter B)**
| Filter A (Microstructure) | Filter B (Macro Liquidity) | Internal Market Regime | Mandatory Spot Execution Action |
| ------ | ------ | ------ | ------ |
| **WHIPSAW (Fakeout)** | **SUCTION ACTIVE** | **Trap & Chop Regime** | **100% Cash / Invariant Patience.**  Ban breakout chasing. Maintain resting stink-bids far below range lows. Core spot remains locked. |
| **WHIPSAW (Fakeout)** | **ROTATION CONFIRMED** | **Accumulation Shakeout** | **Buy the Flush.**  Use violent downward liquidation wicks to scale into spot inventory aggressively at heavy structural discounts. |
| **REAL SPOT TREND** | **SUCTION ACTIVE** | **Isolated Crypto Rally** | **Half-Size Tactical Swing.**  Authorize  **0.375% risk cap (50% sizing)** . Tighten trailing stops due to external equity/macro liquidity drag. |
| **REAL SPOT TREND** | **ROTATION CONFIRMED** | **Full Breakout Alignment** | **Full Sizing Deployment.**  High-conviction spot entry at standard  **0.75% risk cap** . Trail stops behind 4H ATR and Volume Profile nodes. |


--------------------------------------------------------------------------------

####  **5. Dynamic Regime Mutation Lookup Matrix (M1 through M5)**
| Mutation ID | Initial State | Telemetry Mutation Observed (Condition A') | Mechanical Meaning (Outcome B') | Mandatory Execution Override (Rule C') |
| ------ | ------ | ------ | ------ | ------ |
| **M1: Whipsaw Mutates into Organic Trend** | CSU-53A (Shock/Whipsaw) | Following an initial shock candle, price does not retrace > 60%; instead,  **Spot CVD surges across 2 consecutive 4H closes**  and funding remains neutral. | Short squeeze absorbed by genuine institutional spot buyers; transition to organic impulse. | **Promote to Real Spot Trend.**  Clear Filter A gate; check Filter B status to determine whether Half-Size or Full Sizing applies. |
| **M2: Suction Persists Despite Spot Price Push** | CSU-53C (Breakout Attempt) | Spot price pushes upward, but US ETFs print a 3rd day of net redemptions (< -$100M/day) while the BTC/QQQ ratio breaks below its 10-day EMA. | Offshore synthetic rally attempting to fight secular institutional fiat capital extraction. | **Demote to Half-Size Swing (**   **0.375% Risk**   **).**  Tighten stop-loss to breakeven or trailing 1.0 ATR; refuse full-size breakout orders. |
| **M3: False Rotation Flush** | CSU-53B (Rotation Confirmed) | 2 days of ETF inflows occur, but Day 3 reverses with extreme negative Coinbase Premium (MOD 19C) and stablecoin supply contracts. | Premature institutional rotation false-alarm; liquidity withdrawal resumes. | **Freeze New Spot Entries.**  Hold existing spot inventory; cancel pending resting bids above deep structural support. |
| **M4: Hawkes Parabolic Blow-Off** | CSU-53C (Active Trend) | 4H price candle exceeds  **3.5x ATR**  while 8h perp funding blows out  **> +0.05%**  and OI surges to 99th percentile extremes. | Terminal Hawkes branching explosion (self-exciting buying frenzy nearing leverage exhaustion). | **Initiate Stage 1 Profit Taking (50%).**  Tighten trailing stops to 1.0 ATR; arm MOD 41 Rule 1 ATH Countdown. |
| **M5: Macro Decoupling Divergence** | CSU-53A (Trap/Chop) | Equities (QQQ/SPY) crash on macro shocks, but BTC absorbs sell pressure with rising Coinbase Premium and flat Spot CVD. | Bitcoin demonstrating sovereign monetary decoupling and capital flight absorption (MOD 49). | **Override Suction Status.**  Authorize defensive spot scaling at major historical volume nodes (MOD 11). |
