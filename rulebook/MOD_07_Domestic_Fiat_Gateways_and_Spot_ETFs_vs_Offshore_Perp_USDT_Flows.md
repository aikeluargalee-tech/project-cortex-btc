# PROJECT CORTEX-BTC — MODULE 07: DOMESTIC FIAT GATEWAYS (USD) & SPOT ETFS VS. OFFSHORE PERP/USDT FLOWS
**Waterfall Tier:** Pillar 2 (Microstructure & Order Flow) integrated with Pillar 5 (Institutional & On-Chain Flows).
**Empirical Benchmark Anchor:** November 2026 Venue Divergence — US Spot BTC ETFs recording **-$1.177B** in 3-week outflows (including **-$299.8M** single-day outflow on Nov 12) and CME Open Interest dropping **~15%**, while offshore perpetual venues (OKX/Hyperliquid/Binance) expanded leveraged OI by **+22,000 BTC** before breaking down.

---

## 1. Machine-Readable State & Routing Block (Python / Hermes / NotebookLM Index)

```yaml
module_id: "MOD_07"
entry_type: "CONDITIONAL_SIGNAL_UNIT"
waterfall_pillar: "PILLAR_2_AND_5_INSTITUTIONAL_VENUE_FLOWS"
title: "Domestic Fiat Gateways (USD) & Spot ETFs vs. Offshore Perp/USDT Flows"

# PILLAR 1 MASTER PERMISSION PRE-CHECK
pillar_1_permission_required: true
cash_lock_override: "If Pillar 1 Macro Regime == RISK_OFF_100_CASH, block all Long executions."

# PRIMARY TELEMETRY TRIGGERS (VENUE HIERARCHY METRICS)
base_regime_triggers:
  coinbase_premium_index_pct: "Percentage spread between Coinbase BTC-USD and Binance BTC-USDT"
  us_spot_etf_netflow_usd: "Daily and 5D rolling net creation/redemption across US Spot BTC ETFs (IBIT, FBTC, etc.)"
  cme_oi_vs_offshore_oi: "7D % change in CME Regulated Futures OI vs. Offshore Perpetual OI (Binance/OKX/Bybit/Hyperliquid)"
  usd_vs_usdt_spot_cvd: "Net Spot CVD on Fiat USD pairs vs. Stablecoin USDT pairs"

# ANTI-TRAP CIRCUIT BREAKERS
circuit_breakers:
  CB_01_OFFSHORE_SOLO_BAN: "NEVER execute a Spot Long when Coinbase Premium is negative (< -0.03%) and US Spot ETF 3D netflow is negative, regardless of how bullish offshore USDT charts look."
  CB_02_CASH_AND_CARRY_FILTER: "Discount positive Spot ETF inflows by 50%–80% if CME Short Open Interest expands by the exact same notional dollar amount (delta-neutral basis trade, not directional buying)."
  CB_03_NY_OPEN_SETTLEMENT_WAIT: "Wait for the first 30–60 minutes of the NY Equity Cash Open (09:30–10:30 EST) to verify whether IBIT/ETF order flow absorbs or rejects overnight offshore moves."

# RISK & SIZING CONSTANTS (PILLAR 4)
risk_parameters:
  max_portfolio_risk_pct: 0.75
  leverage_permitted: 1.0
  exit_protocol: "TWO_STAGE_STRUCTURAL"
```

---

## 2. Protective Circuit Breakers (Mandatory Pre-Execution Filters)

* **Circuit Breaker 1 — The Sovereign Venue Hierarchy Law:** Not all exchanges are equal. **Domestic Fiat Gateways (Coinbase/Kraken BTC-USD + US Spot ETFs IBIT/FBTC)** represent regulated fiat capital entering or exiting the Bitcoin ecosystem. **Offshore Venues (Binance/OKX/Bybit USDT + Perps)** represent internal crypto-collateralized rotation and high-turnover leverage. Whenever Domestic USD flows conflict with Offshore USDT flows, **Domestic USD is treated as ground truth.**
* **Circuit Breaker 2 — The Wall Street Cash-and-Carry Filter:** When US Spot ETFs print a `+$300M` daily inflow, do not automatically assume `+$300M` of directional bullish buying. Cross-check **CME Open Interest** and **Annualized CME Basis**: if CME OI expands simultaneously while price stays flat, hedge funds are buying the ETF and shorting CME futures (delta-neutral arbitrage).
* **Circuit Breaker 3 — T+1 ETF Flow Lag Protection:** Daily ETF netflow summary tables are published *after* the US market close. During live market hours, use **intraday IBIT volume + Coinbase BTC-USD Spot CVD + Coinbase Premium Index** as the real-time proxy for institutional ETF creation/redemption.

---

## 3. Core Conditional Signal Units (`Condition A -> Outcome B -> Rule C`)

### CSU-07A: Pure Directional Institutional Accumulation (Fiat Gateway Lead)
* **Trigger Condition A (The Telemetry Scan):**
  1. **Coinbase Premium Index** holds consistently positive (`>= +0.05% to +0.20%`) during US trading hours, and **Coinbase/Kraken USD Spot CVD** slopes steeply upward.
  2. **US Spot BTC ETFs** record sustained net inflows (`>= +$150M to +$500M+/day` on a 3D rolling basis), led by BlackRock (`IBIT`) and Fidelity (`FBTC`).
  3. **CME Open Interest** either grows *less* than ETF inflows (confirming unhedged directional spot buying) or rises alongside expanding positive CME basis as institutions take outright long exposure.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Genuine fiat liquidity from sovereign, RIA, and corporate allocators is permanently absorbing circulating BTC into cold-storage ETF custodians.
  * **Probable Trajectory:** Structural multi-week uptrend where every offshore perpetual flush is rapidly bought up during the New York cash session.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Entry Trigger:** Execute **Full-Allocation Unleveraged Spot Swing** under the **0.75% Risk Ceiling** upon a 1H Volume Profile VAH reclaim during or immediately following the NY cash open:
    `Spot Position (BTC) = (0.0075 * Total Portfolio Equity) / (Entry Price - 1H/4H VAL Stop)`
  * **Two-Stage Profit Exit:** Hold core position across multi-day swings; take Stage 1 (50%) at HTF valuation targets (`STH-MVRV >= 1.30` or 1D VAH) and trail Stage 2 behind the 4H/1D VAL.

### CSU-07B: Offshore Leverage Bull Trap Against Domestic Fiat Distribution
* **Trigger Condition A (The Telemetry Scan):**
  1. Offshore perpetual Open Interest (Binance, OKX, Bybit, Hyperliquid) expands rapidly (`+10,000 to +25,000+ BTC`) and offshore USDT Spot CVD appears flat or slightly positive.
  2. Simultaneously, **Coinbase Premium Index** is persistently negative (`<= -0.05%`), **Coinbase USD Spot CVD** slopes downward, **CME Open Interest drops (`-10% to -15%`)**, and **US Spot ETFs print multi-day net outflows** (e.g., `-$299.8M/day`, `-$1.177B` over 3 weeks).
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** US institutions and fiat holders are actively redeeming ETFs and selling physical BTC on Coinbase, while offshore retail traders are trying to prop up the market with leveraged perpetual contracts and USDT churn.
  * **Probable Trajectory:** Fiat supply eventually overwhelms offshore paper leverage, triggering a violent multi-leg breakdown that liquidates the offshore dip-buyers (`November 2026 Empirical Precedent`).
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **LOCK 100% CASH (CB-01 Tripped).** Completely ignore bullish offshore perpetual or USDT signals until Coinbase Premium and 3-day rolling US Spot ETF netflows flip back to positive.

### CSU-07C: Delta-Neutral Wall Street Basis Absorption (High Inflow / Flat Price)
* **Trigger Condition A (The Telemetry Scan):**
  1. US Spot BTC ETFs print large positive inflows (`+$250M to +$600M/day`), yet BTC spot price remains range-bound (`< 1.5%` net progress).
  2. **CME Futures Open Interest** increases by nearly the exact same dollar notional as the cumulative ETF inflows, while CME annualized basis sits at an attractive `+10% to +16%`.
  3. Directional Coinbase USD Spot Premium outside the TWAP settlement windows remains flat (`~0.00%`).
* **Observed Outcome B (The Mechanical Trajectory):**
  Arbitrage hedge funds are capturing the CME basis spread by buying ETF shares and shorting CME futures 1:1. Net market delta is zero—neither bullish nor bearish until the basis compresses or directional spot buyers arrive.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **STANDBY / DO NOT CHASE HEADLINE ETF INFLOWS.** Treat the market as range-bound (`Module 11` Value Area rotation) until directional Coinbase USD Spot CVD breaks price above 4H VAH.

### CSU-07D: Exhaustion of ETF Outflow Capitulation (Contrarian Institutional Floor)
* **Trigger Condition A (The Telemetry Scan):**
  1. After 2 to 4 weeks of heavy US Spot ETF outflows (`>= -$1.0B` cumulative) and a `-15% to -30%` BTC price correction, a single day prints peak ETF outflow headlines.
  2. Despite the ugly T+1 outflow headline, **intraday Coinbase BTC-USD Spot CVD and the Coinbase Premium Index flip sharply positive** (`>= +0.08%`) and price reclaims the 1H/4H VAL.
* **Observed Outcome B (The Mechanical Trajectory):**
  ETF flow headlines report *yesterday's* panic redemptions, whereas intraday Coinbase USD Spot CVD reflects *today's* real-time institutional re-accumulation stepping in at the bottom.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** Prioritize **real-time intraday Coinbase USD Spot CVD + 1H VAH/VAL reclaim** over lagging T+1 ETF outflow headlines; authorize a **0.75% risk-capped Spot Long** with hard invalidation below the intraday absorption low.

---

## 4. Dynamic Regime Mutation Lookup Matrix (`M1` through `M8`)

| Mutation ID | Initial State | Telemetry Mutation Observed (`Condition A'`) | Mechanical Meaning (`Outcome B'`) | Mandatory Execution Override (`Rule C'`) |
| :--- | :--- | :--- | :--- | :--- |
| **M1: NY Open Rescue Flip** | `CSU-07B` (Offshore Weakness) | Price dumps during Asia/London hours on perp selling, then at 09:30 EST Coinbase Premium spikes `+0.10%` and USD Spot CVD absorbs the entire dip. | US institutional fiat buyers are using overnight offshore weakness to accumulate spot at a discount. | **Authorize Tactical Spot Long** under the **0.75% Risk Formula** once the first 1H NY candle reclaims VAL/POC. |
| **M2: NY Open Distribution Fade** | `CSU-05B` (Overnight Rally) | Asia/London pumps price `+3%` on Binance USDT/Perps, then at 09:30 EST Coinbase Premium plunges `-0.12%` and Coinbase USD Spot CVD dumps. | US institutions are selling into the overnight offshore mark-up every morning at the bell. | **Close Tactical Spot Longs Prior to/At NY Open Failure;** lock 100% Cash. |
| **M3: IBIT Volume Climax at Support** | `CSU-07D` (Correction) | `IBIT` prints `>= 2.5x` its 20-day average trading volume at a major HTF support level while closing near the high of the daily bar + positive Coinbase Premium. | Institutional block buyers have stepped in to absorb capitulating ETF sellers in size. | **High-Conviction Spot Swing Entry** (`0.75%` max equity risk) with hard stop below the climax bar low. |
| **M4: CME Basis Collapse Unwind** | `CSU-07C` (Basis Arb) | CME annualized basis drops from `+12%` down to `< +5%` (near T-bill yield) while ETF inflows flip to `-200M+/day` outflows. | Hedge funds are unwinding cash-and-carry positions by dumping Spot ETF shares on the open market. | **Enforce 100% Cash Lock (`CB-02`).** Wait for arbitrage unwind outflows to subside before buying. |
| **M5: Offshore Short-Squeeze Overrun** | `CSU-07A` (US Accumulation) | Sustained US Spot ETF buying drains spot float until offshore perp shorts (Binance/OKX) hit margin calls, causing offshore Perp CVD to spike above USD Spot CVD. | Fiat spot accumulation has successfully triggered an offshore short squeeze (`Module 01 / M1`). | **Execute Stage 1 Profit Exit (50% Spot)** into the offshore short-covering spike; trail remaining 50%. |
| **M6: USDT Minting Without USD Bid** | `CSU-07B` (Divergence) | Tether mints `$1B+` USDT offshore and Binance USDT Spot CVD ticks up, but Coinbase USD Spot CVD remains deeply negative. | Offshore market-maker inventory replenishment has not translated into US institutional demand. | **Maintain 100% Cash Lock** until Domestic USD gateways confirm. |
| **M7: Friday Afternoon ETF Taper** | `CSU-07A` (Uptrend) | After strong Mon–Thu ETF inflows, Friday after 14:00 EST sees Coinbase USD Spot CVD flatten while offshore Perp OI surges into the weekend. | Institutional desks have closed books for the week, leaving the weekend tape exposed to thin offshore leverage chop. | **Tighten Trailing Stops or Take Partial Stage 1 Profits** before Friday 16:00 EST close if Perp Basis is overheated. |
| **M8: Full Global Venue Alignment** | `CSU-07A` (Expansion) | Coinbase USD Spot CVD, US Spot ETFs (`+$400M+`), CME OI, and Offshore Spot/Perp CVD all turn strongly positive simultaneously above 1D VAH. | Rare global institutional + retail synchronized expansion regime. | **Hold Core Spot Swing Position** with wide structural trailing stop behind the 1D Volume Profile VAL. |
