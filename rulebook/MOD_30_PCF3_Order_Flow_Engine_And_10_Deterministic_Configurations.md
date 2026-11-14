# PROJECT CORTEX-BTC — MODULE 30: PCF3 ORDER FLOW ENGINE & 10 DETERMINISTIC CONFIGURATIONS (A–J)
**Waterfall Tier:** Pillar 2 & Pillar 3 Rapid Synthesis Matrix (12-Variable Telemetry Classifier & Configurations `A` through `J`) cross-verified with Pillar 1 (Macro) and Pillar 4 (Portfolio Engineering).
**Provenance & Empirical Benchmark Anchor:** Upgraded from Master Log **Entry #35** (`02_Entry #35: PCF3 Order Flow Engine & 10 Execution Configurations`) — Synthesizing 12 core order-flow variables into 10 deterministic market configurations (`Config A` through `Config J`) and the 4-Regime Spot vs. Perpetual CVD Matrix.

---

## 1. Machine-Readable State & Routing Block (Python / Hermes / NotebookLM Index)

```yaml
module_id: "MOD_30"
entry_type: "MULTI_VARIABLE_STATE_CLASSIFIER"
waterfall_pillar: "PILLAR_2_3_PCF3_ORDER_FLOW_ENGINE"
title: "PCF3 Order Flow Engine & 10 Deterministic Execution Configurations (Configs A-J)"

# PILLAR 1 MASTER PERMISSION PRE-CHECK
pillar_1_permission_required: true
cash_lock_override: "If Pillar 1 Macro Regime == RISK_OFF_100_CASH, only Config C (Bullish Absorption) or Config F/J (Post-Cascade Reset/Bear Trap) can unlock a half-size 0.375% entry after confirmed VAL/VAH reclaim."

# THE 12 PCF3 EVIDENCE VARIABLES
pcf3_variables:
  - "1. Spot Volume (Expanding vs. Weak)"
  - "2. Domestic USD Spot CVD (Positive vs. Negative/Diverging)"
  - "3. Perpetual CVD (Subordinate to Spot vs. Dominant)"
  - "4. Open Interest (Rising Moderately vs. Exploding vs. Collapsing)"
  - "5. Funding Rate (Neutral vs. Increasingly Positive vs. Negative)"
  - "6. Liquidations (Balanced vs. Short Squeeze vs. Long Cascade)"
  - "7. US Spot ETF Flows (Strong Net Inflows vs. Outflows)"
  - "8. Whale Exchange Deposits (Stable vs. Rising Sell Deposits)"
  - "9. Futures Basis (Healthy vs. Extreme)"
  - "10. VWAP / Value Area Acceptance (Accepted Above vs. Repeated Rejection)"
  - "11. L2 Book Liquidity Depth (Thick vs. Thin)"
  - "12. Equity Correlation (Normal vs. Acute Contagion Spike)"

# RISK & SIZING CONSTANTS (PILLAR 4)
risk_parameters:
  max_portfolio_risk_pct: 0.75
  macro_headwind_absorption_risk_pct: 0.375
  leverage_permitted: 1.0 # Strict Unleveraged Spot Only
  exit_protocol: "TWO_STAGE_STRUCTURAL"
```

---

## 2. Protective Circuit Breakers (PCF3 Engine Governance)

* **Circuit Breaker 1 — Spot-Over-Perp Dominance Law:** Across all 10 PCF3 configurations, **Spot CVD + Spot Volume + ETF Flows** act as the primary truth filter. Whenever `Perp CVD` and `Open Interest` dominate while `Spot CVD` is weak or diverging (`Configs B, D, H`), the move is classified as **synthetic fragility**—never chase it.
* **Circuit Breaker 2 — Macro Headwind Override (`Config C` vs. `Config D`):** When macro headwinds are high (`Pillar 1` stressed), **Config C (`Bullish Absorption`)** proves Bitcoin is absorbing macro pressure via genuine spot/ETF buying, whereas **Config D (`Masked Fragility`)** warns that a thin-book perp rally is hiding imminent collapse.
* **Circuit Breaker 3 — Cascade Stand-Down (`Config E` vs. `Config F`):** Never buy during **Config E (`Long Liquidation Cascade`)**; wait strictly until telemetry transitions into **Config F (`Post-Cascade Reset`)** or **Config J (`Bear Trap / Absorption`)**.

---

## 3. Master Lookup Matrix: The 10 PCF3 Configurations (`Configs A – J`)

| Config Code | Configuration Name | Exact 12-Variable Telemetry Signature (`Condition A`) | Mechanical Interpretation (`Outcome B`) | Non-Negotiable Action (`Rule C`) |
| :--- | :--- | :--- | :--- | :--- |
| **`CONFIG_A`** | **HEALTHY BULL** | Price $\uparrow$ + Spot Vol expanding + **USD Spot CVD $\uparrow$** + ETF inflows $\uparrow$ + OI rising moderately + Funding neutral/controlled + Perp CVD subordinate + **VWAP accepted**. | Genuine institutional spot demand driving sustainable trend continuation. | **Authorize `0.75% Risk` Spot Long** on VWAP/VAH pullback retest (`MOD 11B`). |
| **`CONFIG_B`** | **LEVERAGED BULL** | Price $\uparrow$ + Spot Vol weak + **USD Spot CVD weak/flat** + **Perp CVD spiking** + OI exploding + Funding $\uparrow$ + Basis $\uparrow$. | Paper leverage dominating; high vulnerability to downside long-liquidation flush. | **BLOCK NEW ENTRIES.** Tighten stops on open swings (`MOD 02B`). |
| **`CONFIG_C`** | **BULLISH ABSORPTION** | **High macro headwinds** + Price $\uparrow$ + **USD Spot CVD $\uparrow$** + Spot Vol expanding + ETF inflows $\uparrow$ + OI controlled + Funding neutral. | Institutional spot demand is actively absorbing macro selling pressure—true relative strength. | **Authorize `0.375%–0.75% Risk` Spot Long** upon confirmed 4H VAH/VWAP acceptance. |
| **`CONFIG_D`** | **MASKED FRAGILITY** | **High macro headwinds** + Price $\uparrow$ + Spot Vol weak + **USD Spot CVD weak** + Perp CVD spiking + OI exploding + Funding spiking + **Book liquidity thinning**. | Bullish price optics masking severe underlying fragility—imminent rug-pull trap. | **ENFORCE 100% CASH LOCK.** Exit any tactical longs immediately. |
| **`CONFIG_E`** | **LONG LIQUIDATION CASCADE** | Price $\downarrow$ + **Long liquidations spiking** + **OI collapsing** + Funding collapsing + USD Spot CVD negative + Book liquidity deteriorating. | Active forced deleveraging waterfall in progress. | **MANDATORY 100% CASH FREEZE (`CB-03`).** Zero knife-catching until OI stops falling. |
| **`CONFIG_F`** | **POST-CASCADE RESET** | Large long liquidation completed $\rightarrow$ **OI falls substantially (`-8%+`)** $\rightarrow$ Funding normalizes $\rightarrow$ Price stabilizes $\rightarrow$ **USD Spot CVD turns $\uparrow$** + Spot Vol returns. | Leverage purged and organic spot demand stepping in; transition from cascade to re-accumulation. | **Authorize `0.375%–0.75% Risk` Spot Long** on 15m/1H VAL reclaim (`R >= 3.0`). |
| **`CONFIG_G`** | **SHORT SQUEEZE** | Price spiking $\uparrow$ + **Short liquidations spiking** + Funding initially neutral/negative + **OI falls initially**. | Trapped shorts forced to cover (`MOD 01A`). *Watch:* Promotes to `CONFIG_A` only if USD Spot CVD + Vol expand afterward. | Hold open squeeze long; execute **Stage 1 (50%) exit** into climax if USD Spot CVD fails to follow through. |
| **`CONFIG_H`** | **DISTRIBUTION / TOPPING RISK** | Price at highs **BUT** **USD Spot CVD $\downarrow$** + Spot Vol $\downarrow$ + ETF flows deteriorating + **OI exploding + Funding $\uparrow$ + Perp CVD $\uparrow$ + Whale exchange deposits $\uparrow$ + VWAP rejection**. | Maximum institutional distribution into retail leverage FOMO (`top warning`). | **EXECUTE 100% FULL PROFIT EXIT.** Lock Cash immediately. |
| **`CONFIG_I`** | **BEARISH CONTINUATION** | Price $\downarrow$ + **USD Spot CVD $\downarrow$** + Spot Vol expanding on selling + OI elevated + Funding positive + Long liquidations $\uparrow$ + **VWAP rejection**. | Structural downtrend confirmed by both spot selling and trapped dip-buyers (`MOD 04B`). | **STRICT 100% CASH LOCK.** |
| **`CONFIG_J`** | **BEAR TRAP / ABSORPTION** | Price $\downarrow$ on negative headlines + Spot CVD initially $\downarrow$, **BUT** sell volume declines + OI collapses + Long liquidations peak + Price stops falling + **USD Spot CVD turns $\uparrow$ + Reclaims VWAP**. | Bearish catalyst fully absorbed at liquidity pool (`Wyckoff Spring`); high-EV reversal setup. | **Authorize `0.375%–0.75% Risk` Spot Long** upon confirmed VWAP/VAL reclaim with stop below sweep wick. |

---

## 4. PCF3 Spot vs. Perpetual CVD 4-Regime Quick-Action Matrix

| Regime | Spot CVD Slope | Perp CVD Slope | Open Interest | Deterministic Playbook |
| :--- | :--- | :--- | :--- | :--- |
| **1. Organic Spot Accumulation** | **Steeply Positive** | Flat / Drifting | Flat / Moderate | **Sustainable Bull (`CONFIG_A`):** Buy dips to VWAP/VAL; trail Stage 2 swing runners. |
| **2. Synthetic Leverage Rally** | Flat / Falling | **Spiking Upward** | **Expanding Rapidly** | **Liquidity Trap (`CONFIG_B/D`):** Prone to violent long flushes back to VWAP. Do not chase. |
| **3. Spot Absorption / Capitulation Wick** | **Flattening / Curling Up** | **Dumping Hard** | **Plummeting (Liqs)** | **Highest-EV Reversal (`CONFIG_F/J`):** Enter spot long strictly *after* liquidation cascade halts and VWAP/VAL reclaims. |
| **4. Structural Spot Bleed** | **Drifting Downward** | Flat / Chopping | Compressed / Declining | **Cash Preservation (`CONFIG_I`):** Zero bounce sustainability until organic USD spot bids step in. |
