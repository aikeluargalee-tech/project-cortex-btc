# PROJECT CORTEX-BTC — MODULE 29: EQUITY MULTIPLE COMPRESSION, ENERGY SHOCKS & HIGH-BETA CONTAGION
**Waterfall Tier:** Pillar 1 (Cross-Asset Valuation Denominator, Energy Cost-Push Inflation & Tech/AI Credit Contagion) cross-verified with Pillar 4 (Portfolio Engineering).
**Provenance & Empirical Benchmark Anchor:** Upgraded from Master Log **Entries #1 & #36** — Reconciling **+30% YoY S&P 500 earnings growth** against **~20% equity P/E multiple contraction** driven by elevated discount rates, alongside Q4 2026 shocks (**Brent crude > $108–$111/bbl**, **WTI > $100/bbl**, **KOSPI -40% crash**, **SOX semiconductor -16% 8-session plunge**, **CoreWeave 15% bond yields**, and **MSCI MSTR index removal risk**).

---

## 1. Machine-Readable State & Routing Block (Python / Hermes / NotebookLM Index)

```yaml
module_id: "MOD_29"
entry_type: "MASTER_PERMISSION_GATE"
waterfall_pillar: "PILLAR_1_CROSS_ASSET_BETA_AND_MULTIPLE_COMPRESSION"
title: "Equity Multiple Compression, Energy Shocks & High-Beta Contagion (Entries #1 & #36)"

# PILLAR 1 MASTER PERMISSION PRE-CHECK
waterfall_authority: "CROSS_ASSET_CONTAGION_FILTER"

# PRIMARY TELEMETRY TRIGGERS (CROSS-ASSET VALUATION & COMMODITY SHOCKS)
base_regime_triggers:
  multiple_compression_regime: "Strong YoY corporate earnings (+20% to +30%) paired with contracting equity P/E multiples (-15% to -20%) due to restrictive real discount rates"
  energy_inflation_shock: "Brent Crude >= $100-$110/bbl OR WTI Crude >= $95-$100/bbl (+15% surge in 30 days) driving headline CPI/PPI acceleration"
  tech_credit_contagion: "US Semiconductor Index (SOX) or Nasdaq-100 drawdown >= -8% to -15% OR AI/hyperscaler high-yield bond spreads blowing out"
  treasury_proxy_index_risk: "MSCI/S&P passive index removal announcements targeting Bitcoin treasury equities (e.g., MSTR)"

# ANTI-TRAP CIRCUIT BREAKERS
circuit_breakers:
  CB_01_PREMATURE_CLOSE: "NEVER buy a Bitcoin breakout based on strong tech earnings or positive crypto headlines while elevated real discount rates are compressing equity P/E multiples."
  CB_02_VENUE_CONTAMINATION: "Monitor cross-asset equity/credit stress during US cash equity hours (13:30-20:00 UTC) when institutional multi-asset portfolio de-risking executes."
  CB_03_FORCED_FLOW_STANDDOWN: "When WTI/Brent oil spikes above $100/bbl alongside hot CPI/PPI prints, enforce 100% Cash Lock until energy prices peak and roll over."
  CB_04_SIGNAL_HALF_LIFE: "Cross-asset multiple compression and energy-inflation shocks impose 3-week to 3-month macro ceilings on high-beta assets."

# RISK & SIZING CONSTANTS (PILLAR 4)
risk_parameters:
  multiple_compression_max_risk_pct: 0.375 # 30%-50% range-bound risk cap per Entry #36
  contagion_shock_max_risk_pct: 0.00 # 100% Cash Lock
  leverage_permitted: 1.0 # Strict Unleveraged Spot Only
```

---

## 2. Protective Circuit Breakers (Mandatory Pre-Execution Filters)

* **Circuit Breaker 1 — The Discount-Rate Denominator Law (`CB-01`):** Retail traders assume strong corporate earnings (`+30% YoY`) guarantee a bull market. In reality, when central banks hold real interest rates restrictive, the mathematical discount-rate denominator expands—crushing P/E multiples (`-20%`). Because Bitcoin trades as a high-beta liquidity/duration proxy during macro tightening, equity multiple compression creates an invisible ceiling over BTC rallies.
* **Circuit Breaker 2 — Energy Cost-Push Stagflation Trap (`CB-03`):** Surging crude oil (`Brent > $108`, `WTI > $100`) leaks directly into headline CPI and PPI (`e.g., PPI 6.3%–6.6% YoY`), tying the Federal Reserve's hands and preventing rate cuts even if equities fall.
* **Circuit Breaker 3 — AI Capex & Tech Credit Contagion (`CB-02`):** When AI hyperscaler credit spreads widen (`e.g., 15% neocloud bond yields`) or semiconductor indices (`SOX`) suffer multi-day liquidation streaks, institutional multi-asset funds sell liquid Bitcoin holdings to cover tech/equity drawdowns.

---

## 3. Core Conditional Signal Units (`Condition A -> Outcome B -> Rule C`)

### CSU-29A: Restrictive Multiple Compression Chop ("Earnings Up, Multiples Down Ceiling")
* **Trigger Condition A (The Telemetry Scan):**
  1. Corporate earnings growth remains positive, **but restrictive real yields (`10Y TIPS > 2.0%`) force equity P/E multiples to contract (`-10% to -20%`)**.
  2. Bitcoin oscillates inside a wide macro consolidation range without a central-bank liquidity pivot (`MOD 16 / MOD 22`).
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Valuation compression caps upside momentum; institutional allocators sell high-beta strength rather than chasing breakouts.
  * **Probable Trajectory:** Range stagnation where upside breakout attempts fail at overhead resistance until discount rates ease.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Gate Output:** **`CAP PILLAR 1 AT GATE_AMBER (0.375% Risk / 30%–50% Range-Bound Sizing Cap per Entry #36)`.**
  * **Action:** Strictly ban breakout chasing; execute only verified range-low sweeps (`MOD 11A`) with mandatory profit exits at range POC/VAH.

### CSU-29B: Energy Inflation & Tech/Credit Contagion Shock ("Cross-Asset De-Risking Cascade")
* **Trigger Condition A (The Telemetry Scan):**
  1. **Oil Shock:** WTI/Brent crude spikes above **`$100–$110/bbl`**, driving hot CPI/PPI surprises (`> 6% YoY PPI`).
  2. **Equity/Credit Stress:** `SOX` or `Nasdaq-100` plunges `>= -8%` alongside widening AI/corporate credit spreads or global index circuit breakers (e.g., KOSPI drawdown).
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Stagflationary macro shock—rising energy costs prevent Fed easing while falling tech/credit portfolios trigger forced cross-asset margin liquidations.
  * **Probable Trajectory:** High-beta liquidation contagion dragging Bitcoin toward deep on-chain support shelves.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Gate Output:** **`ENFORCE PILLAR 1 = GATE_RED_100_CASH_LOCK`.** Close tactical longs immediately and preserve 100% dry powder.

### CSU-29C: Passive Treasury-Proxy Index Exclusion ("Forced Mechanical Selling Window")
* **Trigger Condition A (The Telemetry Scan):**
  1. Major index provider (MSCI, S&P, Nasdaq) announces removal or re-weighting of a major Bitcoin corporate treasury equity (`e.g., MSTR`), creating a known passive-fund forced rebalancing deadline.
* **Observed Outcome B (The Mechanical Trajectory):**
  Passive index funds must sell shares mechanically regardless of price, depressing equity-crypto sentiment and triggering sympathetic futures shorting in BTC.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **ENFORCE `MOD 17D` 48H CASH STAND-DOWN** across the rebalancing effective date; evaluate post-rebalance relief only after forced selling completes.

### CSU-29D: Discount-Rate Pivot & Multiple Expansion Ignition ("Liquidity Re-Rating")
* **Trigger Condition A (The Telemetry Scan):**
  1. Oil retreats below `$85/bbl`, inflation prints cool below consensus, `10Y` real yields drop sharply, and equity P/E multiples begin expanding alongside positive **US Spot ETF inflows**.
* **Observed Outcome B (The Mechanical Trajectory):**
  Denominator drag reverses into multiple expansion—unleashing high-beta institutional capital back into Bitcoin.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **UPGRADE PILLAR 1 TO `GATE_GREEN_FULL_RISK` (`0.75% Risk Ceiling`)** across all Pillar 2/3 swing setups.

---

## 4. Dynamic Regime Mutation Lookup Matrix (`M1` through `M8`)

| Mutation ID | Initial State | Telemetry Mutation Observed (`Condition A'`) | Mechanical Meaning (`Outcome B'`) | Mandatory Execution Override (`Rule C'`) |
| :--- | :--- | :--- | :--- | :--- |
| **M1: Oil Peak & Disinflation Relief** | `CSU-29B` (Energy Shock) | Brent/WTI crude drops `> -12%` off peak below `$95/bbl` and 10Y yields pull back `>= -15 bps`. | Stagflationary inflation pressure is receding; Fed policy constraint eases. | Upgrade Pillar 1 from `GATE_RED` to `GATE_AMBER` (`0.375% Risk`). |
| **M2: Tech Liquidation Spillover** | `CSU-29A` (Range Chop) | `SOX` or `Nasdaq-100` breaks major 200D support with `> -3%` daily drop and surging VIX (`> 28`). | Multi-asset funds will tap 24/7 BTC liquidity for weekend/overnight margin needs. | **Immediate Downgrade to `GATE_RED_100_CASH_LOCK`.** |
| **M3: BTC Safe-Haven Decoupling** | `CSU-29B` (Equity Drop) | Nasdaq drops `-3%`, **yet Bitcoin rises `+3%` with `Coinbase Premium > +0.10%` and positive US ETF inflows**. | Institutional capital rotating *out* of overvalued tech multiples *into* scarce monetary BTC. | **Authorize `0.375%–0.75%` Spot Long** upon confirmed 4H VAH acceptance. |
| **M4: Post-MSCI Rebalance Absorption** | `CSU-29C` (Index Removal) | Rebalancing close passes, MSTR/proxy stabilizes, and **BTC Domestic USD Spot CVD surges positive** at HTF VAL. | Forced passive index overhang cleared; opportunistic buyers step in. | Lift stand-down; evaluate `MOD 11A` VAL reclaim entry. |
| **M5: Credit Spread Blowout Escalation** | `CSU-29B` (Tech Stress) | Corporate/AI high-yield bond spreads widen rapidly (`MOD 23C`) alongside bank stock drawdowns. | Credit contagion threatens systemic liquidity crunch. | **Strict 100% Cash Lock + Cold-Storage Custody Verification.** |
| **M6: Sovereign Fiscal Dominance Pivot** | `CSU-29A` (Multiple Comp.) | Central bank cuts rates or injects liquidity *despite* sticky 3%+ inflation to stabilize Treasury markets. | Real yields plunge (`negative real rate impulse`)—explosive monetary debasement tailwind. | **Lock `GATE_GREEN_FULL_RISK` (`0.75%`)**; maximize Stage 2 trend runners. |
| **M7: Earnings-Beat Bull Trap** | `CSU-29A` (Range Chop) | Mega-cap tech beats earnings, BTC spikes to range VAH on offshore perps, but **Coinbase Premium stays negative**. | Classic multiple-compression bull trap (`Entry #36`). | **Block Breakout Entry; Lock 100% Cash.** |
| **M8: Global Equity Circuit Breaker** | `CSU-29B` (Contagion) | Major Asian/European index (`KOSPI`, `Nikkei`) triggers emergency trading halts (`-7%+` crash). | Global margin call wave will hit US open (`13:30 UTC`). | **Hold 100% Cash Through NY Open (`13:30–16:00 UTC`)**; evaluate only after NY dust settles. |
