# PROJECT CORTEX-BTC — MODULE 38: ETF PRIMARY-MARKET SETTLEMENT & BRRNY FIX-WINDOW ENGINE
**Waterfall Tier:** Pillar 2 & Pillar 5 Institutional Settlement Mechanics Engine (Extends `MOD 07` by separating intraday creation/redemption arbitrage during the `15:00–16:00 NY` BRRNY fix window from `T+1` lagged flow tables and in-kind vs. cash AP delivery).
**Provenance & Empirical Benchmark Anchor:** Synthesized from the November 13, 2026 Cross-Model Architecture Audit (ChatGPT `MOD 39` + Qwen `MOD 36` + Meta `MOD 38`) — incorporating the SEC's **July 29, 2025 in-kind ETP creation/redemption approval**, **T+1 settlement mechanics**, and the **CME CF BRRNY (`15:00–16:00 ET`)** daily NAV benchmark window.

---

## 1. Machine-Readable State & Routing Block (Python / Hermes / NotebookLM Index)

```yaml
module_id: "MOD_38"
entry_type: "INSTITUTIONAL_ETF_SETTLEMENT_ENGINE"
waterfall_pillar: "PILLAR_2_5_ETF_PRIMARY_MARKET_SETTLEMENT"
title: "ETF Primary-Market Settlement & BRRNY Fix-Window Engine"

# PILLAR 1 MASTER PERMISSION PRE-CHECK
pillar_1_permission_required: true
icdm_integration: "Adjusts MOD 31 Vector 2 Institutional Flow quality (capped +/- 8 pts; never double-counts Farside prints)."

# PRIMARY TELEMETRY INPUTS (INTRADAY NOWCAST VS T+1 SETTLEMENT)
etf_settlement_telemetry:
  tracked_spot_etfs: ["IBIT", "FBTC", "BITB", "ARKB", "GBTC", "BTC"]
  nav_fix_benchmark: "CME CF BRRNY (15:00-16:00 ET / 20:00-21:00 UTC calculation window)"
  intraday_inav_premium_bps: "((ETF_Market_Price / (BTC_Per_Share * Live_BRRNY_Composite_BTC)) - 1.0) * 10000"
  creation_redemption_route: ["CASH_SETTLEMENT", "IN_KIND_DELIVERY", "UNKNOWN"]
  settlement_lag_convention: "T+1 (Trade date order recorded T+0; BTC/cash settled T+1)"

# DETERMINISTIC THRESHOLDS (INITIAL CALIBRATION PARAMETERS)
settlement_thresholds:
  fix_window_premium_bull_bps: 15.0 # >= +15 bps across >= 4 of 6 ETFs during 15:00-16:00 ET
  fix_window_discount_bear_bps: -15.0 # <= -15 bps across >= 4 of 6 ETFs during 15:00-16:00 ET
  session_discount_persistence_pct: 60.0 # >= 60% of US session trading at discount -> AP redemption pressure

# RISK & SIZING CONSTANTS (PILLAR 4)
risk_parameters:
  max_portfolio_risk_pct: 0.75
  redemption_headwind_max_risk_pct: 0.375
  leverage_permitted: 1.0 # Strict Unleveraged Spot Only
```

---

## 2. Protective Circuit Breakers (ETF Primary-Market Anti-Trap Filters)

* **Circuit Breaker 1 — In-Kind vs. Cash Creation Distinction (`CB-01`):** Following the SEC's **July 29, 2025 approval of in-kind creations and redemptions** for spot Bitcoin ETPs, Authorized Participants (APs) can deliver or receive existing BTC inventory directly without executing a public spot-market buy/sell order. Never assume an in-kind share creation equals fresh public-market USD buying unless confirmed by **Domestic USD Spot CVD (`MOD 05 / MOD 19`)**.
* **Circuit Breaker 2 — `T+1` Flow Lag Awareness (`CB-02`):** Public ETF flow tables (e.g., Farside Investors) publish after evening share-count updates and reflect **prior-session (`T+0`) orders settling `T+1`**. Never treat an evening Farside print as a live intraday momentum trigger; use **intraday iNAV premium/discount breadth** as the contemporaneous nowcast and Farside prints strictly as `T+1` settlement confirmation.
* **Circuit Breaker 3 — The `15:00–16:00 ET` (`20:00–21:00 UTC`) BRRNY Fix-Window Guard (`CB-03`):** Major US spot ETFs (including IBIT) strike daily NAV against the **CME CF BRRNY** window (`15:00–16:00 ET`). Persistent `<= -15 bps` ETF discounts entering `15:00 ET` signal AP redemption arbitrage (selling spot into the fix)—block new spot entries until the `16:00 ET` (`21:00 UTC`) fix completes.
* **Circuit Breaker 4 — Never Infer Flow From Share Price Alone (`CB-04`):** High ETF share volume with zero iNAV premium/discount represents secondary-market share rotation between equity traders, **not** primary-market BTC creation or redemption.

---

## 3. Core Conditional Signal Units (`Condition A -> Outcome B -> Rule C`)

### CSU-38A: BRRNY Fix-Window Creation Arbitrage ("Mechanically-Backed Spot Bid")
* **Trigger Condition A (The Telemetry Scan):**
  1. During **`15:00–16:00 ET` (`20:00–21:00 UTC`)**, at least **`4 of 6` major spot ETFs** (`IBIT, FBTC, BITB, ARKB, GBTC, BTC`) trade at a persistent intraday premium **`>= +15 bps`** above indicative NAV (`BTC_per_share * BRRNY_composite`).
  2. Confirmed by **positive Domestic USD Spot CVD (`MOD 05`)** and **Coinbase Premium `>= +0.03%` (`MOD 19`)**.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Settlement Lens:** APs are capturing the ETF premium by buying spot BTC across BRRNY constituent venues (Coinbase, Kraken, Bitstamp, Gemini, LMAX) to hedge cash creations into the `16:00 ET` fix.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **AWARD CONFLUENCE CREDIT TO `MOD 18` (`-6 pts` ICDM fragility)**; defer `Stage 1` profit-taking until after the `16:00 ET` (`21:00 UTC`) fix completes, and authorize `0.75%` full-risk long setups if `MOD 33` permits.

### CSU-38B: Persistent Intraday Discount & AP Redemption Nowcast ("Pre-Print Distribution")
* **Trigger Condition A (The Telemetry Scan):**
  1. At least **`4 of 6` spot ETFs** trade at an intraday discount **`<= -15 bps`** for **`>= 60%` of the US session** (or into the `15:00–16:00 ET` fix window), **AND** prior `3-day` settled flows are net negative (`< -$250M`).
  2. Confirmed by negative Coinbase Premium (`< -0.05%`).
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Settlement Lens:** APs are redeeming ETF shares and unloading spot BTC across constituent venues ahead of tonight's `T+1` outflow report (`MOD 17 M8` NY-close dump).
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **BLOCK ALL NEW SPOT LONGS (`+8 pts` ICDM fragility)**; if holding an active swing long, tighten trailing stop before `20:00 UTC` (`15:00 ET`) and accelerate `Stage 1` exit to VAL loss.

### CSU-38C: In-Kind Creation / Redemption Re-Classification ("Zero Public-Book Impact")
* **Trigger Condition A (The Telemetry Scan):**
  1. Issuer daily holdings file reports a large share creation or redemption (`>= $200M`), **but intraday iNAV premium/discount stayed flat (`-5 bps to +5 bps`) AND Domestic USD Spot CVD showed zero corresponding impulse**.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Settlement Lens:** Institutional holder executed an **in-kind basket transfer** (`SEC July 2025 rule`), moving existing BTC into/out of the trust wrapper without hitting public spot order books.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **DO NOT CHASE OR PANIC-SELL ON HEADLINE FLOW NUMBER.** Tag flow event as `IN_KIND_NEUTRAL` and keep execution anchored to live `MOD 05 / MOD 30` spot order flow.

### CSU-38D: Post-Redemption Settlement Exhaustion ("T+1 Overhang Cleared")
* **Trigger Condition A (The Telemetry Scan):**
  1. Following `3+` days of heavy redemptions, intraday ETF discounts compress from `-25 bps` back to **`>= 0 bps`**, Domestic USD Spot CVD turns positive, and price reclaims 4H VAL (`MOD 11A`).
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Settlement Lens:** AP redemption selling pressure has subsided; secondary demand is absorbing remaining supply.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **LIFT REDEMPTION VETO;** permit `0.375%–0.75%` spot reclaim entry subject to `MOD 33` Master Regime and `R >= 3.0`.

---

## 4. Dynamic Regime Mutation Lookup Matrix (`M1` through `M8`)

| Mutation ID | Initial State | Telemetry Mutation Observed (`Condition A'`) | Mechanical Meaning (`Outcome B'`) | Mandatory Execution Override (`Rule C'`) |
| :--- | :--- | :--- | :--- | :--- |
| **M1: `15:00 ET` Fix Squeeze Ignition** | Neutral US Session | At `15:05 ET (20:05 UTC)`, IBIT + FBTC premiums jump from `+4 bps` to **`+22 bps`** while Coinbase USD Spot CVD spikes vertical. | Heavy late-day institutional cash creation orders hitting the BRRNY fix window. | **Authorize `0.75% Risk` Breakout/Retest Entry** (`MOD 30 CONFIG_A`) if `MOD 33` permits. |
| **M2: `15:00 ET` Redemption Waterfall** | Fragile / `REGIME_3/4` | Entering `15:00 ET (20:00 UTC)`, ETF discounts widen to **`-25 bps`** and spot breaks 1H VAL on expanding sell delta. | APs executing end-of-day redemption basket sales into a thin book (`MOD 17 M8`). | **Enforce Immediate `100% Cash Lock`**; exit any tactical long before `20:15 UTC`. |
| **M3: High ETF Volume, Zero iNAV Spread** | Any Active State | ETF share volume hits `2.0x` 30D average, **but iNAV spread stays `+/- 3 bps` all day**. | Pure secondary-market rotation between equity traders—zero primary-market BTC creation/redemption. | **Ignore Volume Headline;** maintain baseline `MOD 33` regime posture. |
| **M4: T+1 Outflow Print After Green Intraday** | `CSU-38D` (Reclaim) | Evening Farside report prints `-$250M` outflow (from yesterday's `T+0` redemptions), **even though today's intraday iNAV closed at `+12 bps`**. | Lagged `T+1` accounting print reflecting yesterday's already-absorbed selling. | **Do Not Panic-Exit Today's Reclaim;** trust today's live iNAV + USD Spot CVD over `T+1` prints. |
| **M5: Corporate Treasury ATM / Convertible Supply** | `REGIME_2 / 3` | Major corporate BTC proxy (`e.g., MSTR`) announces an active at-the-market (`ATM`) equity/convertible raise alongside ETF inflows. | Corporate treasury purchases frequently execute via OTC/TWAP rather than aggressive market lifting. | Require `MOD 21` TWAP absorption confirmation before assuming immediate breakout follow-through. |
| **M6: Post-In-Kind Regime Coefficient Drift** | Quarterly Calibration | Rolling 60-day regression of `Farside_Flow` vs. `Same_Day_Spot_Return` drops `> 2 sigma` below 2024 cash-only baseline. | In-kind ETP arbitrage permanently dampened spot-impact-per-dollar of reported ETF flows. | **Down-weight Raw Flow Magnitude by 50%** in `MOD 07`; rely primarily on `Coinbase Premium + USD Spot CVD`. |
| **M7: Pre-Market Gap Arbitrage Trap** | `13:30 UTC` NY Open | BTC rallies `+3%` overnight in Asia, causing ETFs to gap up at `09:30 ET` with a `-18 bps` discount to live spot. | US equity open is pricing ETF shares *below* overnight spot—APs will sell spot to arbitrage the gap. | **Block NY Open Chasing (`09:30–10:15 ET`)**; wait for spot and ETF iNAV to converge first. |
| **M8: Issuer Holdings File Delay (`UNKNOWN`)** | Overnight Audit | Custodian/issuer fails to publish updated `BTC_per_share` or shares-outstanding file by `08:00 MYT`. | `iNAV` denominator cannot be verified cleanly (`MOD 36`). | Tag `MOD_38_STATE = UNKNOWN` until issuer basket file updates; do not extrapolate prior-day shares. |
