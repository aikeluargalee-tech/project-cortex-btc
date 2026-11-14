# PROJECT CORTEX-BTC — MODULE 22: NET FED LIQUIDITY IMPULSE (FED BALANCE SHEET − TGA − RRP)
**Waterfall Tier:** Pillar 1 (Master Macro Liquidity Plumbing — Leading Dollar Reserve Impulse) cross-verified with Pillar 4 (Portfolio Engineering) and Pillar 5 (Sovereign Defense).
**Empirical Benchmark Anchor:** November 2026 Federal Reserve & US Treasury Plumbing Telemetry — US Treasury General Account (**TGA**) elevated at **$912.13B** (draining private bank reserves), Overnight Reverse Repo (**RRP**) facility near exhaustion, US 10-Year Yield at **5.129%**, and crypto stablecoins contracting **-$14.2B in 30 days**—confirming an active **Net Dollar Liquidity Drain (`GATE_RED`)**.

---

## 1. Machine-Readable State & Routing Block (Python / Hermes / NotebookLM Index)

```yaml
module_id: "MOD_22"
entry_type: "MASTER_PERMISSION_GATE"
waterfall_pillar: "PILLAR_1_MACRO_LIQUIDITY_PLUMBING"
title: "Net Fed Liquidity Impulse (Fed Balance Sheet - TGA - RRP)"

# MASTER WATERFALL AUTHORITY (FEEDS DIRECTLY INTO MOD 16 PILLAR 1 GATE)
waterfall_authority: "LEADING_MACRO_PLUMBING"
net_liquidity_formula: "Net_Fed_Liquidity = Fed_Total_Assets (WALCL) - Treasury_General_Account (WTREGEN) - Reverse_Repo (RRPONTSYD)"

# PRIMARY TELEMETRY TRIGGERS (4-WEEK & 13-WEEK RATE OF CHANGE)
base_regime_triggers:
  impulse_4w_delta_usd: "4-week net change in Net_Fed_Liquidity (USD Billions)"
  impulse_13w_delta_usd: "13-week (quarterly) net change in Net_Fed_Liquidity (USD Billions)"
  liquidity_injection_regime: "4W Net Liquidity >= +$75B AND 13W >= +$150B (TGA draining into economy / Fed expanding)"
  liquidity_drain_regime: "4W Net Liquidity <= -$75B OR TGA surging above $850B-$900B+ while RRP is depleted (< $100B)"
  rrp_buffer_status: "When RRP < $100B, TGA refills drain bank reserves 1-for-1 (high risk-asset sensitivity)"

# ANTI-TRAP CIRCUIT BREAKERS
circuit_breakers:
  CB_01_PREMATURE_CLOSE: "NEVER ignore a multi-week Net Fed Liquidity drain >= -$100B when evaluating multi-week swing holds; liquidity drains create delayed 2-6 week gravity on BTC."
  CB_02_VENUE_CONTAMINATION: "Use official Federal Reserve H.4.1 weekly releases (released Thursdays 20:30 UTC) and daily US Treasury DTS TGA updates."
  CB_03_FORCED_FLOW_STANDDOWN: "During quarterly US corporate/individual tax deadlines (Apr 15, Jun 15, Sep 15, Jan 15) when TGA spikes rapidly, tighten swing stops or hold Cash."
  CB_04_SIGNAL_HALF_LIFE: "Net Fed Liquidity leads Bitcoin macro inflection points by 2 to 6 weeks; use Pillar 2 for exact entry/exit execution."

# RISK & SIZING CONSTANTS (PILLAR 4)
risk_parameters:
  liquidity_expansion_max_risk_pct: 0.75
  liquidity_drain_max_risk_pct: 0.00 # Downgrades Pillar 1 toward GATE_RED 100% Cash Lock
  leverage_permitted: 1.0 # Strict Unleveraged Spot Only
```

---

## 2. Protective Circuit Breakers (Mandatory Pre-Execution Filters)

Why **Net Fed Liquidity (`WALCL − TGA − RRP`)** is the master plumbing gauge of global risk assets:
* When the US Treasury refills its checking account at the Fed (**TGA rises**), it pulls cash directly out of commercial bank reserves and money markets.
* Previously, rising TGA was cushioned by money-market funds draining the **Reverse Repo (RRP)** facility. **Once RRP approaches zero (`< $100B`), every dollar added to TGA drains commercial bank reserves 1-for-1**, starving risk assets of dollar liquidity.
* **Circuit Breaker 1 — The RRP Exhaustion Multiplier (`CB-01`):** Whenever `RRP < $100B` AND `TGA > $850B` (benchmark: **$912.13B** in Nov 2026), any further Treasury debt issuance drains bank liquidity immediately—forcing Pillar 1 into heightened defensive posture (`GATE_AMBER` or `GATE_RED`).
* **Circuit Breaker 2 — Tax-Date TGA Surge Protection (`CB-03`):** Around major US tax collection dates, TGA jumps sharply over 10–15 days, routinely triggering equity and Bitcoin pullbacks.
* **Circuit Breaker 3 — Lead-Lag Calibration (`CB-04`):** Liquidity plumbing shifts lead Bitcoin spot price by **2 to 6 weeks**; combine `MOD 22` with `MOD 16` (10Y Yield, DXY, Stablecoins) to set the active Pillar 1 Gate.

---

## 3. Core Conditional Signal Units (`Condition A -> Outcome B -> Rule C`)

### CSU-22A: Treasury TGA Drain & Reserve Injection ("Stealth QE Liquidity Tailwind")
* **Trigger Condition A (The Telemetry Scan):**
  1. **Net Fed Liquidity (`WALCL − TGA − RRP`)** expands by **`>= +$75B` over 4 weeks** and **`>= +$150B` over 13 weeks** (driven by Treasury spending down the TGA below `$700B`, Fed balance-sheet expansion, or RRP outflows).
  2. Confirmed by `MOD 16` (`DXY falling`, `30D Stablecoin supply expanding >= +1.5%`).
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Dollars are flowing out of the Treasury's Fed account directly into private commercial bank reserves and institutional balance sheets, lowering funding stress and fueling asset inflation.
  * **Probable Trajectory:** Strong structural macro tailwind supporting multi-week Bitcoin trend expansion and rapid absorption of derivatives dips.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Gate Output:** **`REINFORCE PILLAR 1 = GATE_GREEN_FULL_RISK` (`0.75% Risk Ceiling`).**
  * **Action:** Authorize full-size unleveraged spot swing entries on all validated Pillar 2/3 setups and maximize `Stage 2` trailing runners.

### CSU-22B: TGA Refill Drain With Depleted RRP ("Bank Reserve Vacuum")
* **Trigger Condition A (The Telemetry Scan):**
  1. **TGA surges above `$850B–$900B+`** (benchmark: **$912.13B** in Nov 2026) due to heavy net Treasury bill/bond issuance or tax receipts, while **RRP sits below `$100B`** (zero buffer left).
  2. **4-Week Net Fed Liquidity contracts by `<= -$75B to -$150B`**, accompanied by rising SOFR/repo rates, rising 10Y yields (`> 5.0%`), and contracting crypto stablecoins (`MOD 16C`).
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** The US Treasury is vacuuming dollar liquidity out of private markets to fund fiscal deficits without an RRP cushion, tightening dollar availability globally.
  * **Probable Trajectory:** High risk of liquidity air pockets, thin crypto order books (`$72M depth`), and failed breakout rallies until TGA peaks and begins spending down.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Gate Output:** **`DOWNGRADE PILLAR 1 TO GATE_RED_100_CASH_LOCK` (or strict `GATE_AMBER` if 200D MA holds).**
  * **Action:** Lock **100% Cash** on tactical swing capital; preserve dry powder until `Mutation M1` signals TGA spend-down inflection.

### CSU-22C: Neutral Plumbing / Offset Flows ("Balanced Reserve Regime")
* **Trigger Condition A (The Telemetry Scan):**
  1. `4-Week Net Fed Liquidity` remains within **`-$40B to +$40B`** (e.g., modest Fed QT offset by steady TGA spending).
* **Observed Outcome B (The Mechanical Trajectory):**
  Macro plumbing is neutral; Bitcoin price action will be governed by crypto-native flows (`Spot ETFs`, `Stablecoins`, `Perp OI/CVD`).
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** Defer gate authority to `MOD 16` (Stablecoins/DXY/Yields) and `MOD 17` (200D MA).

### CSU-22D: Emergency Fed Liquidity Facility / Balance Sheet Expansion ("Crisis-to-Bull Pivot")
* **Trigger Condition A (The Telemetry Scan):**
  1. Following a banking, bond-market (`MOVE > 130`), or sovereign funding stress event, the Federal Reserve halts QT, cuts rates, or launches an emergency lending facility—causing **`WALCL` (Fed Total Assets) to jump `>= +$100B` in 1–2 weeks**.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Explicit monetary debasement and central-bank liquidity backstop—the single most powerful multi-month catalyst in Bitcoin's history.
  * **Probable Trajectory:** Initial knee-jerk volatility followed by an explosive secular repricing higher in scarce monetary assets.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** Once initial 24H–48H bond volatility settles (`MOD 23 M1`), **LOCK `GATE_GREEN_FULL_RISK`** and deploy both `0.75% Risk` Spot Swings and Sovereign Cold-Storage tranches (`MOD 18D`).

---

## 4. Dynamic Regime Mutation Lookup Matrix (`M1` through `M8`)

| Mutation ID | Initial State | Telemetry Mutation Observed (`Condition A'`) | Mechanical Meaning (`Outcome B'`) | Mandatory Execution Override (`Rule C'`) |
| :--- | :--- | :--- | :--- | :--- |
| **M1: TGA Peak & Spend-Down Pivot** | `CSU-22B` (TGA Drain) | After peaking above `$900B+`, **TGA drops by `>= -$50B` over 2 weeks** as Treasury resumes net fiscal outlays into the economy. | The Treasury liquidity vacuum just reversed into a direct reserve injection. | **Upgrade Pillar 1 from `GATE_RED` to `GATE_AMBER`/`GREEN`**; watch `MOD 16` stablecoins for confirmation. |
| **M2: Quarterly Treasury Refunding (QRA) Shock** | Any State | US Treasury Quarterly Refunding Announcement projects higher-than-expected net borrowing (`TGA target raised sharply`) and 10Y yields jump `> +15 bps`. | Upcoming multi-month supply of Treasury debt will drain private liquidity. | **Downgrade Pillar 1 Gate by One Tier** (`GREEN -> AMBER` or `AMBER -> RED`). |
| **M3: Post-Tax-Date Liquidity Release** | `CB-03` (Tax Drain) | Following April 15 / June 15 / Sept 15 tax surges, TGA stabilizes and commercial bank reserves rebound. | Temporary seasonal tax liquidity drain is complete. | Lift `CB-03` tax stand-down; re-evaluate Pillar 2 order-flow triggers. |
| **M4: Fed QT Taper / Halt Announcement** | `CSU-22C` (Neutral) | FOMC announces tapering or ending Quantitative Tightening (`reducing monthly Treasury/MBS runoff`). | Removes a persistent `-$25B to -$60B/month` structural drag on `WALCL`. | **Bullish Macro Bias Upgrade:** Prioritize `Stage 2` trend-following holds. |
| **M5: Global Central Bank Liquidity Offset** | `CSU-22B` (US Drain) | Fed liquidity is flat/slightly negative, **but PBOC / ECB / BOJ inject `>= +$150B` equivalent** and DXY falls below 100. | Offshore sovereign liquidity expansion is offsetting US fiscal drain. | Keep Pillar 1 at **`GATE_AMBER` (`0.375% Risk`)**; confirm via offshore + domestic Spot CVD. |
| **M6: Repo / SOFR Funding Spike** | Any State | Overnight SOFR spikes `>= +15 bps` above the Fed Funds upper bound (dollar funding stress in repo markets). | Acute collateral/cash shortage in the banking system—institutions liquidate risk assets for cash. | **Immediate `GATE_RED_100_CASH_LOCK`** until repo rates normalize. |
| **M7: Stablecoin Lag Catch-Up** | `CSU-22A` (Fed Inj.) | Net Fed Liquidity turns positive (`+$100B`), and 2–3 weeks later **USDC + USDT 30D supply flips from negative to `+1.5%`**. | Dollar liquidity injection has officially transmitted into crypto-native settlement rails. | **Confirm `GATE_GREEN_FULL_RISK` (`0.75%`)**; maximum green light for spot swing deployment. |
| **M8: Thursday H.4.1 Surprise Revision** | Weekly Thursday `20:30 UTC` | Weekly Fed H.4.1 release shows unexpected `-$80B+` drop in bank reserves alongside breaking 4H VAL. | Confirms hidden liquidity tightening behind weak price action. | **Enforce 100% Cash Lock**; reject weekend relief bounces. |
