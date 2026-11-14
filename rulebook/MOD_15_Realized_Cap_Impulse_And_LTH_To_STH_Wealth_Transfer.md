# PROJECT CORTEX-BTC — MODULE 15: REALIZED CAP IMPULSE & LTH-TO-STH WEALTH TRANSFER
**Waterfall Tier:** Pillar 5 (On-Chain Cohorts, Capital Flows & Sovereign Defense) cross-verified with Pillar 1 (Macro Permissions) and Pillar 4 (Portfolio Engineering).
**Empirical Benchmark Anchor:** November 2026 Cohort & Supply Telemetry — Following Bitcoin's **41% drawdown** from its October 2025 ATH (**$126,080**) down to the **$68,000–$75,000** range amid **$1.44B** in 5-day US Spot ETF outflows and **$14.2B** in 30-day stablecoin contraction, wallets holding **100 to 10,000 BTC** shifted to net accumulation while mega-whales (`> 10,000 BTC`) and retail (`< 100 BTC`) reduced exposure.

---

## 1. Machine-Readable State & Routing Block (Python / Hermes / NotebookLM Index)

```yaml
module_id: "MOD_15"
entry_type: "CONDITIONAL_SIGNAL_UNIT"
waterfall_pillar: "PILLAR_5_ONCHAIN_CAPITAL_FLOWS"
title: "Realized Cap Impulse & LTH-to-STH Wealth Transfer (Distribution vs. Re-Accumulation)"

# PILLAR 1 MASTER PERMISSION PRE-CHECK
pillar_1_permission_required: true
cash_lock_override: "If Pillar 1 Macro Regime == RISK_OFF_100_CASH and 30D Realized Cap Impulse < 0, enforce 100% Cash Shield."

# PRIMARY TELEMETRY TRIGGERS (MACRO ON-CHAIN CAPITAL FLOWS)
base_regime_triggers:
  realized_cap_30d_impulse: "30-day net change in Bitcoin Realized Capitalization (USD) >= +2.0% (Inflow) or <= -0.5% (Capital Outflow)"
  lth_supply_30d_delta: "30-day net change in Long-Term Holder (> 155d) supply (BTC)"
  whale_shark_cohort_delta: "Net 7D/30D balance change of 100 - 10,000 BTC non-exchange entities"
  exchange_reserve_trend: "30-day net spot exchange BTC reserve change (Inflow = Sell Pressure vs. Outflow = Cold Custody)"

# ANTI-TRAP CIRCUIT BREAKERS
circuit_breakers:
  CB_01_PREMATURE_CLOSE: "NEVER buy a macro dip while 30D Realized Cap Impulse is negative AND 100-10,000 BTC cohorts are distributing."
  CB_02_VENUE_CONTAMINATION: "Exclude internal exchange address reshuffles and ETF custodian wallet migrations when measuring exchange reserve outflows."
  CB_03_FORCED_FLOW_STANDDOWN: "When LTH distribution velocity exceeds combined Spot ETF + 100-10K BTC absorption for >= 14 days, restrict entries to defensive cash preservation."
  CB_04_SIGNAL_HALF_LIFE: "Realized Cap & LTH/STH wealth transfer govern 2-week to 6-month cycle positioning; use Pillar 2 for exact swing execution."

# RISK & SIZING CONSTANTS (PILLAR 4)
risk_parameters:
  max_portfolio_risk_pct: 0.75
  leverage_permitted: 1.0 # Strict Unleveraged Spot Only
  exit_protocol: "TWO_STAGE_STRUCTURAL"
```

---

## 2. Protective Circuit Breakers (Mandatory Pre-Execution Filters)

Realized Capitalization values every Bitcoin UTXO at the price it last moved on-chain, making **30-Day Realized Cap Impulse** the purest measure of **net new fiat dollars entering or exiting the Bitcoin network**. Before acting on Module 15, four circuit breakers apply:
* **Circuit Breaker 1 — Net Capital Outflow Guard (`CB-01`):** When 30-day Realized Cap contracts (`net capital leaving the network at a realized loss`), Bitcoin is in a macro capital-drain regime. Tactical swing entries must be blocked or strictly gated until Realized Cap flattens and institutional cohorts (`100–10,000 BTC`) resume accumulation.
* **Circuit Breaker 2 — Custodian & ETF Wallet Separation (`CB-02`):** Modern exchange reserve tracking must filter out Coinbase Custody ETF creations/redemptions and internal exchange wallet migrations so synthetic balance shifts are not mistaken for organic spot withdrawals.
* **Circuit Breaker 3 — Absorption Deficit Check (`CB-03`):** Long-Term Holders always distribute into bull markets; LTH selling is only bearish when **LTH distribution exceeds fresh Realized Cap / Spot ETF inflows**, causing price to stall and roll over.
* **Circuit Breaker 4 — Sovereign Cold-Storage Alignment:** Aligns tactical swing risk (`0.75%` ceiling) with long-term sovereign custody allocation (`multi-vendor hardware multi-sig`).

---

## 3. Core Conditional Signal Units (`Condition A -> Outcome B -> Rule C`)

### CSU-15A: Fresh Capital Inflow & Healthy Wealth Transfer ("Cycle Expansion Engine")
* **Trigger Condition A (The Telemetry Scan):**
  1. **30-Day Realized Cap Impulse** expands strongly (`>= +2.0% to +5.0%+` per month), confirming massive net new USD capital entering Bitcoin.
  2. **LTH-to-STH Transfer:** Long-Term Holder supply declines gradually (`controlled distribution into strength`) while **US Spot ETF inflows**, **`100–10,000 BTC` entities**, and **Domestic USD Spot CVD** absorb every coin, driving price to higher highs.
  3. **Exchange Reserves:** Adjusted spot exchange BTC balances trend steadily downward into cold custody.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Textbook bull-market wealth transfer—veteran holders gradually realize gains into deep, persistent institutional and sovereign inflows without overwhelming order books.
  * **Probable Trajectory:** Sustained multi-week to multi-month bull trend where every derivative flush (`MOD 03`) is rapidly absorbed by fresh incoming capital.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Entry Trigger:** Authorize full **0.75% Risk Ceiling** Unleveraged Spot Long entries on every Pillar 2/3 pullback setup (`MOD 01`, `MOD 03`, `MOD 13A`).
  * **Two-Stage Profit Exit Protocol:**
    * **Stage 1 Exit (50% of Position):** Bank 50% at upper Garman-Klass volatility bands / local resistance; move stop to breakeven.
    * **Stage 2 Exit (Remaining 50%):** Trail generously beneath 4H/1D Volume Profile VALs until Realized Cap impulse decelerates (`Mutation M2`).

### CSU-15B: Unabsorbed LTH Distribution Top ("Cycle Exhaustion Ceiling")
* **Trigger Condition A (The Telemetry Scan):**
  1. **LTH Supply** drops sharply (`accelerated veteran distribution` at `>= 90th percentile` spending velocity) alongside `STH-MVRV >= 1.30` (`MOD 13C`).
  2. **30-Day Realized Cap Impulse** begins **flattening or decelerating** while **US Spot ETF inflows stall/flip negative**, and price prints a multi-week distribution range (failing to make new highs despite heavy volume).
  3. **`100–10,000 BTC` cohort balances** flip from net accumulation to net distribution.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Veteran supply has overwhelmed incoming institutional liquidity; late retail STH buyers are holding the bag at peak cost basis.
  * **Probable Trajectory:** High probability of a major macro distribution breakdown (`-20% to -40%` cycle drawdown) once marginal STH demand exhausts.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **EXECUTE FULL TACTICAL EXIT (100% CASH ON SWING BOOK).** Shift sovereign focus strictly to capital preservation and multi-sig custody security until Realized Cap and cohort accumulation reset.

### CSU-15C: LTH Re-Accumulation & Shark Absorption ("Silent Structural Bottoming")
* **Trigger Condition A (The Telemetry Scan):**
  1. Following a major `-30% to -45%` drawdown from cycle highs (benchmark: Nov 2026 `-41%` drawdown from `$126,080` into `$68K–$75K`), **30-Day Realized Cap stops falling** (`flattens near 0.0%`).
  2. **LTH Supply** climbs steadily (`coins aging past 155 days into strong hands`) and **`100–10,000 BTC` entities** show sustained net accumulation even while retail (`< 100 BTC`) and ETF headlines remain fearful (`Fear & Greed <= 25`).
  3. Price forms a multi-week base above a major HTF Volume Profile HVN with rising **Domestic USD Spot CVD**.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Supply is migrating from weak, price-sensitive retail hands into high-conviction institutional and sovereign cold storage, shrinking the liquid tradable float.
  * **Probable Trajectory:** Formation of a durable structural floor; once macro liquidity (`Pillar 1`) stabilizes, reduced float amplifies upside price elasticity.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Entry Trigger:** Execute **Unleveraged Spot Long** upon confirmed **4H/1D Volume Profile VAH reclaim** backed by Domestic USD Spot CVD, sized strictly to the **0.75% Risk Ceiling** with stop beneath the accumulation range VAL.

### CSU-15D: Net Capital Outflow & Exchange Inflow Surge ("Macro Bear Drain")
* **Trigger Condition A (The Telemetry Scan):**
  1. **30-Day Realized Cap Impulse** is **negative (`<= -0.5% to -2.0%`)**, proving net USD capital is actively leaving the Bitcoin network at realized losses.
  2. Adjusted spot exchange BTC reserves rise (`coins moving onto exchanges to be sold`) alongside persistent **US Spot ETF net outflows** (`e.g., -$1.44B over 5 sessions`).
  3. Both `100–10,000 BTC` and `> 10,000 BTC` cohorts are net sellers.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Structural liquidity contraction—spot sellers are actively liquidating into thin order books with no institutional absorption wall beneath them.
  * **Probable Trajectory:** Continued lower lows and failed relief rallies until Realized Cap contraction halts and `100–10,000 BTC` accumulation reappears.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **ENFORCE STRICT 100% CASH LOCK.** Zero spot swing exposure permitted. Protect sovereign purchasing power until `CSU-15C` accumulation signals trigger.

---

## 4. Dynamic Regime Mutation Lookup Matrix (`M1` through `M8`)

| Mutation ID | Initial State | Telemetry Mutation Observed (`Condition A'`) | Mechanical Meaning (`Outcome B'`) | Mandatory Execution Override (`Rule C'`) |
| :--- | :--- | :--- | :--- | :--- |
| **M1: Shark Accumulation Divergence** | `CSU-15D` (Capital Drain) | Realized Cap is still slightly negative and ETFs show outflows, **but `100–10,000 BTC` wallets flip to strong net accumulation** at HTF support (`$68K`). | Mid-tier institutional sharks are front-running the bottom ahead of lagging ETF/retail flows. | Put `CSU-15C` on High Alert; authorize `0.375%–0.75% Risk` Spot Long *only* when 1H/4H VAH + USD Spot CVD confirm. |
| **M2: Realized Cap Inflection Flip** | `CSU-15C` (Bottoming) | **30-Day Realized Cap crosses from negative/flat back above `+0.5%`** alongside US Spot ETF outflows flipping to net inflows. | Macro capital drain has officially reversed into net capital inflow. | **Promote Regime to `CSU-15A`:** Authorize full `0.75% Risk` Spot Swing deployment. |
| **M3: LTH Distribution Cliff** | `CSU-15A` (Bull Expansion) | LTH 30D supply drops by `> 250,000 BTC` in 30 days while Realized Cap growth stalls and price fails at VAH. | Veteran holders dumped a massive supply wave that overwhelmed incoming buyers. | **Execute Immediate 100% Swing Profit Exit**; shift to defensive cash. |
| **M4: Exchange Inflow Whale Alert** | Any Bull/Range State | Sudden spike in adjusted spot exchange BTC inflows (`>= +2.5 Z-score`) driven by `> 1,000 BTC` deposits while USD Spot CVD turns negative. | Large holders just moved spot BTC onto exchanges for imminent market/limit distribution. | **Tighten Stops to 1H VAL Immediately** or lock 100% Cash until exchange inflows are absorbed. |
| **M5: Supply Shock Illiquidity Squeeze** | `CSU-15C` -> `15A` | LTH supply reaches an all-time high (`> 70%` of circulating supply) + exchange reserves hit multi-year lows + ETF inflows resume. | Historic liquid float compression; even modest spot inflows trigger explosive vertical repricing. | **Maximize Stage 2 Runner Hold** (trail behind 4H/1D VALs rather than capping upside early). |
| **M6: Retail FOMO Transfer Peak** | `CSU-15B` (Top Zone) | `< 10 BTC` retail cohort balances surge vertically while `100–10,000 BTC` and LTH cohorts dump aggressively. | Final stage of bull-cycle wealth transfer from smart money to late retail. | **Strict 100% Cash Lock on Swing Book**; block all FOMO entries. |
| **M7: Custodial Migration False Alarm** | `CSU-15A` (False Drop) | Raw exchange reserves appear to jump `+30,000 BTC`, but on-chain forensics show internal Coinbase/Binance cold-wallet reshuffle with zero USD Spot CVD selling. | Accounting/custody artifact rather than actual sell-side deposit flow. | **Ignore Raw Exchange Spike**; rely on Domestic USD Spot CVD (`MOD 05/07`) for truth. |
| **M8: Sovereign Multi-Sig Audit Trigger** | Any Major Regime Shift | Portfolio cash/BTC ratio shifts significantly (`> 25%` rebalance) or exchange counterparty stress emerges. | Operational custody hygiene check required under Pillar 5 sovereign defense. | Verify cold-storage multi-sig quorum and keep active exchange balance strictly limited to tactical swing margin. |
