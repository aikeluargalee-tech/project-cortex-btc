# PROJECT CORTEX-BTC — MODULE 20: CME FUTURES BASIS & WEEKEND GAP FILL TOPOLOGY
**Waterfall Tier:** Pillar 2 & Pillar 3 Bridge (Regulated Institutional Term Structure & Friday-to-Sunday Settlement Gaps) cross-verified with Pillar 4 (Portfolio Engineering).
**Empirical Benchmark Anchor:** November 2026 Regulated Derivatives Telemetry — CME Bitcoin Futures trading at a regulated institutional contango basis of **+5.3% to +5.7% annualized** even while offshore perpetuals dipped into negative basis (`-0.047%`), alongside CME Open Interest contracting **~15%** during the November 10–13 institutional de-risking from **$75,771** down to **$68,450** prior to the Friday `21:00 UTC` CME weekly close.

---

## 1. Machine-Readable State & Routing Block (Python / Hermes / NotebookLM Index)

```yaml
module_id: "MOD_20"
entry_type: "CONDITIONAL_SIGNAL_UNIT"
waterfall_pillar: "PILLAR_2_3_CME_INSTITUTIONAL_STRUCTURE"
title: "CME Futures Basis & Weekend Gap Fill Topology"

# PILLAR 1 MASTER PERMISSION PRE-CHECK
pillar_1_permission_required: true
cash_lock_override: "If Pillar 1 Macro Regime == RISK_OFF_100_CASH, use CME gaps strictly as resistance exit targets—never chase upward weekend gaps."

# PRIMARY TELEMETRY TRIGGERS (CME SETTLEMENT & BASIS)
base_regime_triggers:
  cme_schedule_utc: "Closes Friday 21:00 UTC (16:00 CT); Reopens Sunday 22:00 UTC (17:00 CT)"
  cme_annualized_basis: "((CME_Front_Month - Spot_BRTI) / Spot_BRTI) * (365 / Days_To_Expiry) * 100"
  institutional_demand_basis: "CME Annualized Basis >= +10.0% to +18.0% with rising CME OI"
  institutional_unwinding_basis: "CME Annualized Basis <= +4.0% with falling CME OI (benchmark -15% CME OI contraction)"
  cme_weekend_gap_pct: "abs(Sunday_2200_Open - Friday_2100_Close) / Friday_2100_Close >= 1.0%"

# ANTI-TRAP CIRCUIT BREAKERS
circuit_breakers:
  CB_01_PREMATURE_CLOSE: "NEVER buy a weekend (Sat-Sun) breakout above Friday's CME close on thin offshore volume without Sunday 22:00 UTC + Monday NY confirmation."
  CB_02_VENUE_CONTAMINATION: "Separate CME institutional basis from offshore perpetual basis; when CME basis compresses while offshore funding spikes, offshore retail is trapped."
  CB_03_FORCED_FLOW_STANDDOWN: "Stand down during CME last-Friday monthly contract roll windows (final 24h before settlement) due to mechanical calendar-spread distortion."
  CB_04_SIGNAL_HALF_LIFE: "CME weekend gaps carry a 70%+ statistical fill probability within 48 hours of Sunday reopen—treat un-filled gaps as high-gravity magnets."

# RISK & SIZING CONSTANTS (PILLAR 4)
risk_parameters:
  max_portfolio_risk_pct: 0.75
  leverage_permitted: 1.0 # Strict Unleveraged Spot Only
  exit_protocol: "TWO_STAGE_STRUCTURAL"
```

---

## 2. Protective Circuit Breakers (Mandatory Pre-Execution Filters)

* **Circuit Breaker 1 — The Weekend Thin-Liquidity Trap (`CB-01`):** Because CME Group closes Friday at `21:00 UTC` and reopens Sunday at `22:00 UTC`, weekend price moves occur on thin offshore order books without institutional arbitrageurs. Weekend breakouts fail over **70% of the time** once CME reopens.
* **Circuit Breaker 2 — CME Basis vs. Offshore Perp Divergence (`CB-02`):** CME futures are dominated by regulated US hedge funds, asset managers, and ETF market makers. When CME annualized basis compresses toward money-market T-bill rates (`~4%–5%`) while CME OI falls (`-15%`), institutions are unwinding long exposure regardless of offshore retail excitement.
* **Circuit Breaker 3 — Monthly Contract Roll Distortion (`CB-03`):** During the final 48 hours before CME monthly expiry (last Friday of each month at `16:00 UTC`), OI shifts between front-month and next-month contracts; do not mistake roll volume for directional positioning.
* **Circuit Breaker 4 — Gap-Fill Confirmation Rule (`CB-04`):** Never blindly fade a weekend gap without Pillar 2 confirmation (`15m/1H VAH/VAL rejection or reclaim + Domestic USD Spot CVD`).

---

## 3. Core Conditional Signal Units (`Condition A -> Outcome B -> Rule C`)

### CSU-20A: Downward Weekend Gap Fill Reversal ("Sunday Sweep & Reclaim Magnet")
* **Trigger Condition A (The Telemetry Scan):**
  1. Over Saturday–Sunday, Bitcoin drops **`>= 1.5% to 4.0%` below Friday's `21:00 UTC` CME Close** on thin offshore volume, leaving an open downside CME gap above spot.
  2. **Sunday Open / Monday NY Absorption:** Following Sunday `22:00 UTC` CME reopen (or Monday `13:30 UTC` NY open), price sweeps an intraday liquidity low, **reclaims the 15m/1H Volume Profile VAL**, and **Domestic USD Spot CVD** + Coinbase Premium (`MOD 19`) turn positive.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Offshore weekend sellers pushed price away from institutional fair value while CME desks were offline; upon reopen, institutional arbitrageurs and spot buyers step in to close the gap.
  * **Probable Trajectory:** High-probability upward rotation back to **100% fill of Friday's `21:00 UTC` CME Close price**.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Entry Trigger:** Execute **Unleveraged Spot Long** upon confirmed **15m/1H VAL reclaim** after Sunday `22:00 UTC` with positive Domestic USD Spot CVD.
  * **Position Sizing Formula (0.75% Risk Ceiling):**
    `Spot Position (BTC) = (0.0075 * Total Portfolio Equity) / (Entry Price - Invalidation Stop Price)`
  * **Hard Structural Invalidation Stop:** Place hard stop beneath the weekend / Sunday-open sweep wick low.
  * **Two-Stage Profit Exit Protocol:**
    * **Stage 1 Exit (70% of Position):** Close 70% directly at the **exact Friday `21:00 UTC` CME Gap Fill level**; move stop to breakeven.
    * **Stage 2 Exit (Remaining 30%):** Trail behind 1H VAL if Domestic USD Spot CVD continues expanding through the gap.

### CSU-20B: Upward Weekend Gap Bull Trap ("Illiquid Sunday Pump Fade")
* **Trigger Condition A (The Telemetry Scan):**
  1. Over Saturday–Sunday, Bitcoin rallies **`>= 1.5% to 4.0%` above Friday's `21:00 UTC` CME Close** on rising offshore perp OI (`Binance/Bybit`) and thin weekend spot volume (`< 30th percentile`).
  2. At Sunday `22:00 UTC` CME reopen or Monday `13:30 UTC` NY open, **Coinbase Premium (`MOD 19`) is negative (`<= -0.08%`)** and price loses the Sunday-open 1H POC/VAL.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Offshore retail traders chased an illiquid weekend pump, creating a high-gravity CME gap below spot that US institutional sellers immediately target at the open.
  * **Probable Trajectory:** Downward mean-reversion flush filling 100% of the upward weekend gap back to Friday's CME close.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **BLOCK ALL SUNDAY/MONDAY MORNING LONG ENTRIES. LOCK 100% CASH.** If holding an existing Spot Long from Friday, bank 50%–100% profit into the upward weekend gap ahead of the Monday NY open.

### CSU-20C: CME Institutional Basis Expansion ("Regulated Leverage Tailwind")
* **Trigger Condition A (The Telemetry Scan):**
  1. CME front-month annualized basis expands from `5%` above **`+10.0% to +16.0%` APR** alongside **rising CME Open Interest** and **positive US Spot ETF net inflows**.
  2. Perpetual basis (`MOD 02`) remains disciplined (`< +0.025%`), showing regulated institutions—not reckless retail—are driving the futures premium.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Regulated hedge funds and institutional allocators are adding directional long exposure via CME futures while ETF demand absorbs underlying spot supply.
  * **Probable Trajectory:** Sustained multi-week institutional bull trend.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **AUTHORIZE FULL `0.75% RISK` SPOT SWING ENTRIES** on Pillar 2 pullbacks (`MOD 10B / 11A`).

### CSU-20D: CME Institutional De-Risking Unwind ("Basis Compression & OI Drain")
* **Trigger Condition A (The Telemetry Scan):**
  1. CME Open Interest contracts sharply (`>= -10% to -15%` over 5–10 sessions) while CME annualized basis compresses toward or below the **US 3-Month T-Bill risk-free rate (`<= +4.5% APR`)** alongside US Spot ETF outflows.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Regulated institutions are closing long futures and unwinding basis trades—removing the primary institutional bid pillar from the market.
  * **Probable Trajectory:** Heavy overhead supply and downside vulnerability until CME OI stabilizes.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **ENFORCE 100% CASH LOCK** until CME OI stops contracting and Domestic USD Spot CVD turns positive.

---

## 4. Dynamic Regime Mutation Lookup Matrix (`M1` through `M8`)

| Mutation ID | Initial State | Telemetry Mutation Observed (`Condition A'`) | Mechanical Meaning (`Outcome B'`) | Mandatory Execution Override (`Rule C'`) |
| :--- | :--- | :--- | :--- | :--- |
| **M1: Breakaway Gap (Unfilled Impulse)** | `CSU-20B` (Upward Gap) | Monday NY session opens above Friday CME close, **Coinbase Premium surges `> +0.06%`**, US ETFs print big inflows, and price holds above Sunday VAH for 24h. | True institutional breakaway gap—will *not* fill in the short term. | Lift `CSU-20B` fade warning; enter `0.75% Risk` Spot Long on Monday NY VAH retest. |
| **M2: Gap-Fill Rejection Breakdown** | `CSU-20A` (Downward Gap) | Price rallies up to fill Friday's CME close, hits heavy ask absorption at the exact gap level, and **USD Spot CVD turns negative**. | Institutional sellers used the gap-fill magnet as a liquidity exit target. | **Stage 1 (70%) already banked at gap fill**; exit remaining 30% immediately at market. |
| **M3: CME Basis Inversion (Backwardation)** | `CSU-20D` (De-Risking) | CME front-month futures trade **below spot (`< 0.0%` annualized basis)** alongside falling CME OI. | Extreme institutional hedging panic or forced fund liquidation (`rare cycle bottom signal`). | Stand down during active drop (`CB-03`); prepare `MOD 03A` capitulation reversal once CME OI flattens. |
| **M4: Multi-Week Open Gap Magnet** | Active Trend | A weekend gap remains unfilled for `> 7 days`, then price loses 4H VAL and enters the LVN leading back to that old CME gap. | Untested CME settlement levels act as high-probability liquidity magnets during corrections. | **Use Unfilled CME Gap as Primary Downside Target**; keep 100% Cash until price reaches and reclaims the gap. |
| **M5: Friday Pre-Close Institutional Pin** | Friday `18:00–21:00 UTC` | Price oscillates tightly around a major strike/POC during the final 3 hours before CME's `21:00 UTC` weekly close. | Dealers and institutional desks squaring books into the weekly benchmark fixing. | **Zero New Entries Friday Afternoon**; wait for Sunday `22:00 UTC` reopen. |
| **M6: CME-Offshore Basis Arbitrage Squeeze** | `CSU-20C` (CME Strong) | CME basis jumps to `+14% APR` while offshore perp basis stays negative (`-0.03%`, `MOD 01`). | Regulated US institutions are bullish while offshore retail is heavily short—explosive arbitrage/squeeze setup. | **High-Conviction `0.75% Risk` Spot Long** upon 1H VAH reclaim with USD Spot CVD. |
| **M7: Quarter-End CME Roll Turbulence** | Final 48h of Mar/Jun/Sep/Dec | Massive volume spikes in CME calendar spreads with erratic intraday basis prints. | Mechanical quarterly contract roll—not organic directional flow. | **Circuit Breaker 3 Tripped:** Suspend CME basis signals until the new front-month contract becomes lead. |
| **M8: Post-Flush CME OI Bottom** | `CSU-20D` (Unwind) | After a `-15%+` CME OI drop, CME OI turns upward for `3 consecutive sessions` with rising basis and positive ETF flows. | Regulated institutional capital has finished de-risking and is re-entering long. | Upgrade institutional posture; authorize `0.75% Risk` Spot Swing deployment. |
