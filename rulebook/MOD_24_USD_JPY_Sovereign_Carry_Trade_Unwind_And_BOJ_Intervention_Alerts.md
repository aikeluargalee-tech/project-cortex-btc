# PROJECT CORTEX-BTC — MODULE 24: USD/JPY SOVEREIGN CARRY-TRADE UNWIND & BOJ INTERVENTION ALERTS
**Waterfall Tier:** Pillar 1 (Global FX Liquidity & Cross-Asset Leverage Carry-Trade Breaker) cross-verified with Pillar 4 (Portfolio Engineering).
**Empirical Benchmark Anchor:** November 13, 2026 Live FX Telemetry — **USD/JPY** trading directly on the psychological **160.00 Bank of Japan (BOJ) intervention threshold** (**159.88–160.13 JPY/USD**, spiking to **160.1255** at 06:15 UTC before snapping sharply downward to **159.7130** at 06:40 UTC) alongside US 10Y yields at **5.129%**, creating acute bilateral FX intervention and carry-trade unwind tail risk.

---

## 1. Machine-Readable State & Routing Block (Python / Hermes / NotebookLM Index)

```yaml
module_id: "MOD_24"
entry_type: "MASTER_PERMISSION_GATE"
waterfall_pillar: "PILLAR_1_SOVEREIGN_FX_CARRY_BREAKER"
title: "USD/JPY Sovereign Carry-Trade Unwind & BOJ Intervention Alerts"

# MASTER WATERFALL AUTHORITY (GLOBAL CARRY-TRADE LIQUIDITY GATE)
waterfall_authority: "CROSS_ASSET_CARRY_CIRCUIT_BREAKER"

# PRIMARY TELEMETRY TRIGGERS (YEN CARRY & RATE DIFFERENTIAL)
base_regime_triggers:
  usdjpy_level_and_velocity:
    INTERVENTION_DANGER_ZONE: "USD/JPY >= 158.00 - 160.00+ (heightened Ministry of Finance / BOJ physical FX intervention risk)"
    CARRY_UNWIND_SHOCK: "USD/JPY drops >= -1.5% in 24H OR >= -3.0% in 5 trading days (violent Yen appreciation margin call)"
    GRADUAL_CARRY_TAILWIND: "USD/JPY stable or drifting moderately higher (+0.2% to +1.0%/wk) while US-JP 10Y spread is calm and MOVE < 85"
  us_jp_10y_spread: "US 10Y Treasury Yield minus JGB 10Y Yield 10-day rate of change (bps)"

# ANTI-TRAP CIRCUIT BREAKERS
circuit_breakers:
  CB_01_PREMATURE_CLOSE: "NEVER buy a Bitcoin dip during an active Yen carry-trade unwind (USD/JPY plunging >= -1.5%/24h); cross-asset macro funds liquidate BTC 24/7 to cover Yen-funded margin calls."
  CB_02_VENUE_CONTAMINATION: "Monitor spot USD/JPY and 1-month USD/JPY implied volatility across Tokyo (00:00-06:00 UTC) and London/NY sessions."
  CB_03_FORCED_FLOW_STANDDOWN: "Enforce automatic 24H-48H Cash Stand-Down during Bank of Japan (BOJ) policy meetings and suspected MOF FX intervention spikes."
  CB_04_SIGNAL_HALF_LIFE: "Carry-trade unwind shocks trigger violent 2-10 day cross-asset liquidation waves; wait for USD/JPY 4H volatility to compress before re-entering BTC."

# RISK & SIZING CONSTANTS (PILLAR 4)
risk_parameters:
  calm_carry_max_risk_pct: 0.75
  intervention_zone_max_risk_pct: 0.375
  active_unwind_max_risk_pct: 0.00 # Emergency 100% Cash Lock
  leverage_permitted: 1.0 # Strict Unleveraged Spot Only
```

---

## 2. Protective Circuit Breakers (Mandatory Pre-Execution Filters)

Why **USD/JPY** is one of the most dangerous hidden liquidation triggers for Bitcoin:
* Global macro funds borrow cheap Japanese Yen (`JPY`) to fund leveraged long positions in US tech equities and Bitcoin (`the Yen Carry Trade`).
* When the Bank of Japan hikes rates, yields surge, or Japan's Ministry of Finance intervenes to defend the Yen near **160.00**, **USD/JPY plunges violently** (Yen strengthens rapidly). Every 1% jump in the Yen instantly inflates the debt burden of Yen-funded carry books—forcing macro funds to dump liquid 24/7 Bitcoin holdings to meet margin calls.
* **Circuit Breaker 1 — The Violent Yen-Spike Veto (`CB-01`):** Whenever `USD/JPY` drops `>= -1.5%` in 24 hours (or `>= -3.0%` in 5 days), **lock 100% Cash immediately**. Do not try to catch Bitcoin support until `USD/JPY` stabilizes.
* **Circuit Breaker 2 — The 160.00 Intervention Ceiling (`CB-03`):** When `USD/JPY` trades above **158.00–160.00+** (benchmark: **159.88–160.13** on Nov 13, 2026), bilateral FX intervention can strike without warning during Tokyo or NY hours, causing a 300–500 pip flash crash in `USD/JPY` and an immediate sympathy flush in BTC.
* **Circuit Breaker 3 — BOJ Policy Meeting Freeze (`CB-03`):** Stand down from new swing entries within `+/- 12 hours` of Bank of Japan rate decisions.

---

## 3. Core Conditional Signal Units (`Condition A -> Outcome B -> Rule C`)

### CSU-24A: Benign Carry Equilibrium ("Stable FX Liquidity Environment")
* **Trigger Condition A (The Telemetry Scan):**
  1. `USD/JPY` trades smoothly below intervention danger thresholds (`< 155.00`) with 5-day realized FX range `< 1.5%`.
  2. US-Japan yield differentials are stable and `MOVE Index < 85` (`MOD 23A`).
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Cross-border carry funding is stable; global macro funds face zero forced FX margin calls, leaving Bitcoin free to respond to spot ETF and on-chain inflows.
  * **Probable Trajectory:** Normal cross-asset risk regime permitting full Pillar 2/3 swing execution.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Gate Output:** **`PERMIT FULL 0.75% RISK CEILING`** when confirmed by `MOD 16` (`GATE_GREEN`).

### CSU-24B: The 158–160+ Intervention Danger Zone ("Asymmetric FX Tail-Risk Ceiling")
* **Trigger Condition A (The Telemetry Scan):**
  1. `USD/JPY` climbs into or above **`158.00–160.00+`** (benchmark: **159.88–160.13** on Nov 13, 2026) driven by wide US-Japan yield spreads (`10Y > 5.0%`), triggering verbal warnings from Japanese Ministry of Finance officials.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Market is coiled on a hair-trigger: either hot US yields push `USD/JPY` higher (draining global liquidity via strong USD) OR Japanese authorities intervene to smash `USD/JPY` lower (triggering an abrupt carry-trade margin unwind). Both outcomes create sharp asymmetric downside risk for Bitcoin.
  * **Probable Trajectory:** High risk of sudden `200–500 pip` `USD/JPY` air pockets that trigger simultaneous crypto liquidation cascades.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Gate Output:** **`CAP PILLAR 1 AT GATE_AMBER (Max 0.375% Risk)`** (or `GATE_RED` if `MOD 16` stablecoins are draining). Tighten stops on any open swing positions ahead of Tokyo (`00:00–06:00 UTC`) and NY (`13:30–16:00 UTC`) intervention windows.

### CSU-24C: Active Yen Carry-Trade Unwind ("Cross-Asset Margin Liquidation Cascade")
* **Trigger Condition A (The Telemetry Scan):**
  1. `USD/JPY` plunges **`>= -1.5%` within 24 hours** (or `>= -3.0%` over 5 trading days) on surging volume, accompanied by falling Nasdaq/Nikkei futures and rising `MOVE` volatility.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Forced cross-asset deleveraging—macro funds are liquidating Bitcoin, gold, and tech equities simultaneously to pay back appreciating Yen loans.
  * **Probable Trajectory:** Multi-day liquidation cascade that ignores local crypto support levels until `USD/JPY` stops falling.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Gate Output:** **`EMERGENCY PILLAR 1 = GATE_RED_100_CASH_LOCK`.**
  * **Action:** Exit any open tactical BTC exposure immediately; hold 100% Cash until `Mutation M1` confirms `USD/JPY` stabilization.

### CSU-24D: Post-Unwind FX Stabilization & Sovereign Rotation ("Carry Reset Rebound")
* **Trigger Condition A (The Telemetry Scan):**
  1. Following a `-3%+` Yen carry unwind flush, `USD/JPY` forms a multi-day base (`24H range < 0.8%`), US 10Y yields stabilize/fall (`DXY < 102`), and Bitcoin reclaims 1H/4H Volume Profile **VAL** with positive **Domestic USD Spot CVD**.
* **Observed Outcome B (The Mechanical Trajectory):**
  Forced Yen-funded carry sellers have finished liquidating; discounted Bitcoin is absorbed by unleveraged spot buyers.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** Upgrade Pillar 1 to `GATE_AMBER` (`0.375% Risk`) and authorize Spot Long entry upon 15m/1H **VAH/VAL reclaim** (`MOD 11A`).

---

## 4. Dynamic Regime Mutation Lookup Matrix (`M1` through `M8`)

| Mutation ID | Initial State | Telemetry Mutation Observed (`Condition A'`) | Mechanical Meaning (`Outcome B'`) | Mandatory Execution Override (`Rule C'`) |
| :--- | :--- | :--- | :--- | :--- |
| **M1: USD/JPY Volatility Compression** | `CSU-24C` (Carry Unwind) | After a sharp plunge, `USD/JPY` holds a higher low for **48 consecutive hours** with intraday volatility dropping `> 50%`. | Forced Yen margin liquidation wave has exhausted its immediate selling pressure. | Lift emergency `CB-01` freeze; evaluate `CSU-24D` VAL reclaim on BTC. |
| **M2: Suspected MOF Stealth Intervention** | `CSU-24B` (`160.00+`) | `USD/JPY` drops `150–300 pips` in under 15 minutes during thin Tokyo/NY liquidity without a US economic release. | Official Ministry of Finance / BOJ physical Yen buying intervention. | **Immediate 24H Cash Stand-Down on BTC:** Wait to see if carry funds are forced to liquidate crypto over the next 2 sessions. |
| **M3: BOJ Hawkish Hike Shock** | Any State | Bank of Japan raises policy rate or cuts JGB purchases faster than consensus, sending JGB yields up and `USD/JPY` down `> -1.2%`. | Structural narrowing of US-Japan rate differential—multi-week carry headwind. | **Downgrade Pillar 1 to `GATE_RED_100_CASH_LOCK`** until cross-asset markets reprice. |
| **M4: Dovish Fed + Stable Yen Sweet Spot** | `CSU-24D` (Post-Unwind) | US 10Y yields drop sharply (`Fed dovish`), weakening DXY broadly (`EUR/USD ↑`), while `USD/JPY` drifts gently without panic. | Dollar weakens globally without acute Yen carry stress—ideal macro liquidity tailwind. | **Upgrade Pillar 1 to `GATE_GREEN_FULL_RISK` (`0.75%`)**. |
| **M5: Nikkei / Nasdaq Sympathy Circuit Breaker** | `CSU-24C` (Unwind) | Nikkei 225 or Nasdaq 100 drops `> -3%` intraday alongside plunging `USD/JPY`. | Full cross-asset risk-off contagion; BTC liquidity will be tapped by multi-asset funds. | **Enforce 100% Cash Lock**; zero knife-catching allowed. |
| **M6: 160.00 Clean Breakout Without Intervention** | `CSU-24B` (`160.00`) | `USD/JPY` breaks above `160.50` and holds for 5 days with zero intervention, **AND** `MOVE < 85` + US Spot ETFs have strong inflows. | Market absorbed the psychological level smoothly without liquidity stress. | Relax `CSU-24B` caution slightly, but keep stops disciplined against sudden intervention. |
| **M7: Weekend FX Gap Risk** | Friday `20:00 UTC` (`USD/JPY ~160`) | `USD/JPY` closes Friday right at `160.00` ahead of weekend G7/BOJ commentary. | High probability of a Sunday `22:00 UTC` FX gap spilling into crypto open. | **Bank Stage 1 (50%) Profit Before Friday Close**; avoid holding full size over weekend. |
| **M8: BTC Sovereign Hedge Divergence** | `CSU-24C` (FX Turmoil) | `USD/JPY` and fiat currencies experience severe volatility, **yet Coinbase Premium (`MOD 19`) surges `> +0.10%` and BTC breaks 4H VAH**. | Investors fleeing fiat currency instability into hard sovereign monetary assets (BTC/Gold). | **Authorize `0.375%–0.75%` Spot Long** *only* upon confirmed 4H VAH acceptance + positive USD Spot CVD. |
