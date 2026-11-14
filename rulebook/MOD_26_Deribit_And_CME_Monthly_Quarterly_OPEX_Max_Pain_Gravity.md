# PROJECT CORTEX-BTC — MODULE 26: DERIBIT & CME MONTHLY/QUARTERLY OPEX MAX PAIN GRAVITY
**Waterfall Tier:** Pillar 3 (Derivatives Expiration Calendar, Strike Pinning & Post-Expiry Volatility Release) cross-verified with Pillar 1 (Macro) and Pillar 4 (Portfolio Engineering).
**Empirical Benchmark Anchor:** November 10–13, 2026 Deribit & CME Expiration Telemetry — Front weekly expiry (`13NOV26`, **27.2K BTC** OI) carrying Max Pain at **$77,000** (`+/- 3.0%` implied 1-SD move) and major quarterly expiry (`25DEC26`, **95.3K BTC** OI) carrying Max Pain at **$75,000**, demonstrating how macro/ETF shocks (`10Y Yield 5.129%`, `-$1.44B ETF outflows`) override Max Pain gravity prior to expiry while setting up post-settlement volatility releases.

---

## 1. Machine-Readable State & Routing Block (Python / Hermes / NotebookLM Index)

```yaml
module_id: "MOD_26"
entry_type: "CONDITIONAL_SIGNAL_UNIT"
waterfall_pillar: "PILLAR_3_OPEX_EXPIRATION_DYNAMICS"
title: "Deribit & CME Monthly/Quarterly OpEx Max Pain Gravity & Post-Expiry Release"

# PILLAR 1 MASTER PERMISSION PRE-CHECK
pillar_1_permission_required: true
cash_lock_override: "If Pillar 1 Macro Regime == RISK_OFF_100_CASH, Max Pain gravity will NOT rescue price during an active macro liquidity drain—enforce 100% Cash Lock."

# PRIMARY TELEMETRY TRIGGERS (EXPIRATION CALENDAR & NOTIONAL CONCENTRATION)
base_regime_triggers:
  deribit_settlement_time: "Every Friday at 08:00 UTC (Major monthly/quarterly expiries on last Friday of month/quarter)"
  cme_options_settlement_time: "Last Friday of contract month at 16:00 UTC (London BRR fixing)"
  notional_gravity_threshold: "Expiry Open Interest >= 25,000 BTC (Weekly) or >= 80,000 - 150,000+ BTC (Monthly/Quarterly)"
  opex_pin_window: "T-48 hours to T-0 hours prior to Friday 08:00 UTC settlement when Spot is within +/- 4% of Max Pain and Pillar 1 is calm"
  post_opex_release_window: "T+1 hour to T+36 hours following Friday 08:00 UTC settlement (Gamma Unclench Window)"

# ANTI-TRAP CIRCUIT BREAKERS
circuit_breakers:
  CB_01_PREMATURE_CLOSE: "NEVER buy a dip solely because price is below Max Pain; Max Pain is a statistical gravity metric, NOT a guaranteed support floor during macro or ETF outflows."
  CB_02_VENUE_CONTAMINATION: "Weight Max Pain toward Deribit (~79% options OI) and CME institutional options rather than low-volume retail option venues."
  CB_03_FORCED_FLOW_STANDDOWN: "During the final 12 hours before a major monthly/quarterly expiry (> 80K BTC OI), stand down from new breakout entries to avoid dealer pinning chop."
  CB_04_SIGNAL_HALF_LIFE: "Max Pain gravity expires instantly at 08:00 UTC Friday; immediately transition to Post-OpEx Breakout/Reclaim rules after settlement."

# RISK & SIZING CONSTANTS (PILLAR 4)
risk_parameters:
  max_portfolio_risk_pct: 0.75
  leverage_permitted: 1.0 # Strict Unleveraged Spot Only
  exit_protocol: "TWO_STAGE_STRUCTURAL"
```

---

## 2. Protective Circuit Breakers (Mandatory Pre-Execution Filters)

* **Circuit Breaker 1 — The "Max Pain Is Not Support" Law (`CB-01`):** A common retail trap is buying Bitcoin blindly because *"Max Pain is $77,000 and BTC is at $71,000, so dealers will push it back up by Friday."* As November 10–13, 2026 proved, when macro tightening (`10Y Yield 5.13%`) and Spot ETF outflows (`-$1.44B`) hit simultaneously, spot breaks right through put walls and leaves Max Pain far above. **Never trade Max Pain without Pillar 1 permission and Pillar 2 USD Spot CVD confirmation.**
* **Circuit Breaker 2 — Pre-Expiry Pinning Chop Filter (`CB-03`):** When macro conditions *are* calm (`MOVE < 85`, `Positive GEX`), massive monthly/quarterly expiries (`> 80K BTC` OI) create strong dealer hedging gravity within `+/- 3%` of Max Pain during the final 36–48 hours—chopping up breakout traders until `08:00 UTC` Friday passes.
* **Circuit Breaker 3 — Post-Expiry Volatility Release (`CB-04`):** Once the `08:00 UTC` Friday settlement bell rings, billions of dollars in option gamma expire simultaneously. Dealers unwind their delta hedges, frequently unleashing a clean directional trend move over the following Friday NY and Monday sessions.

---

## 3. Core Conditional Signal Units (`Condition A -> Outcome B -> Rule C`)

### CSU-26A: Post-OpEx Volatility Release Breakout ("Gamma Unclench Impulse")
* **Trigger Condition A (The Telemetry Scan):**
  1. A major monthly or quarterly Deribit/CME OpEx (`>= 60,000 BTC` expiring OI) has just settled (`after Friday 08:00 UTC` / `16:00 UTC`).
  2. During the week leading into OpEx, price was pinned in a tight range (`Garman-Klass volatility <= 25th percentile`, `MOD 12`).
  3. **Post-Settlement Ignition:** Within `1 to 36 hours` post-expiry, price breaks decisively above the pre-expiry **Volume Profile VAH** (`MOD 11B`) backed by surging **Domestic Fiat (USD) Spot CVD** and Coinbase Premium (`> +0.04%`).
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Expiring options removed the dealer gamma ceiling that was suppressing price; institutional spot buyers step into a freshly cleared derivatives slate.
  * **Probable Trajectory:** Clean multi-day directional trend expansion (`+6% to +15%`) as new monthly option positioning builds at higher strikes.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Entry Trigger:** Execute **Unleveraged Spot Long** on the first 15m/1H pullback retest of the **reclaimed pre-expiry VAH** after Friday `08:00 UTC` settlement, sized strictly to the **0.75% Risk Ceiling**.
  * **Two-Stage Profit Exit Protocol:**
    * **Stage 1 Exit (50% of Position):** Close 50% at `+2.5R` or next major new-month Call Wall; move stop to breakeven.
    * **Stage 2 Exit (Remaining 50%):** Trail behind 4H Volume Profile VAL.

### CSU-26B: Calm-Regime Pre-OpEx Max Pain Gravitation ("Controlled Mean-Reversion Drift")
* **Trigger Condition A (The Telemetry Scan):**
  1. Time-to-expiry is **`T-48h to T-6h`** before a major Friday `08:00 UTC` expiry (`>= 40,000 BTC` OI).
  2. Pillar 1 is calm (`GATE_GREEN` or `GATE_AMBER`, `MOVE < 85`, no major CPI/FOMC shock), and spot trades `2.0% to 4.5%` below **Max Pain** while sitting cleanly above a major **Put Wall / 4H VAL**.
  3. **Domestic USD Spot CVD** turns positive at 4H VAL support (`confirming real buyers alongside dealer delta-hedging`).
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** As short-dated puts decay (`Theta burn`), market makers buy back short futures hedges, pulling spot price back toward the Max Pain strike into Friday `08:00 UTC`.
  * **Probable Trajectory:** Controlled mean-reversion drift toward Max Pain, stalling right at the Max Pain strike before settlement.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Entry Trigger:** Execute **Reduced-Size Unleveraged Spot Long (`0.375% Risk`)** upon 15m/1H VAL reclaim, with **mandatory Stage 2 Full Profit Exit at Max Pain (or by Friday `07:30 UTC` ahead of settlement)**.

### CSU-26C: Pre-OpEx Pinning Chop ("T-24H Dealer Equilibrium Lock")
* **Trigger Condition A (The Telemetry Scan):**
  1. Time-to-expiry is **`< 24 hours`** before a major monthly/quarterly OpEx (`>= 80,000 BTC` OI), and spot is already trading within **`+/- 1.2%` of Max Pain**.
* **Observed Outcome B (The Mechanical Trajectory):**
  Dealer gamma pinning is at peak intensity; every `0.8%` move up or down is immediately faded by automated market-maker hedging.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **STANDBY IN 100% CASH (`CB-03`).** Zero new entries allowed until after `08:00 UTC` Friday settlement clears the pin.

### CSU-26D: Macro Override Breakdown Through OpEx ("Unpinned Waterfall")
* **Trigger Condition A (The Telemetry Scan):**
  1. Ahead of Friday OpEx, Pillar 1 trips `GATE_RED` (`10Y yield / DXY / ETF outflow shock`) and spot breaks below both Max Pain and the primary **Put Wall** (`MOD 25C`).
* **Observed Outcome B (The Mechanical Trajectory):**
  Macro forced selling overwhelms options pinning; underwater put dealers accelerate the drop rather than pulling price back to Max Pain.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **ENFORCE 100% CASH LOCK (`CB-01`).** Completely ignore the higher Max Pain figure until post-expiry `MOD 03A` capitulation absorption confirms.

---

## 4. Dynamic Regime Mutation Lookup Matrix (`M1` through `M8`)

| Mutation ID | Initial State | Telemetry Mutation Observed (`Condition A'`) | Mechanical Meaning (`Outcome B'`) | Mandatory Execution Override (`Rule C'`) |
| :--- | :--- | :--- | :--- | :--- |
| **M1: Post-Expiry False Breakout Sweep** | Friday `08:30–14:00 UTC` | Immediately after `08:00 UTC` OpEx, price sweeps *down* below range VAL for 1–2 hours, then snaps back above VAH at NY open (`13:30 UTC`) with USD Spot CVD. | Dealers unwound residual hedges downward first before institutional spot buyers launched the real post-OpEx trend. | **Enter `0.75% Risk` Spot Long on VAH reclaim** (`CSU-26A` + `MOD 11B`). |
| **M2: Quarterly Triple-Witching Mega-Expiry** | Last Friday of Mar/Jun/Sep/Dec | Deribit quarterly OpEx (`08:00 UTC`) + CME quarterly futures/options expiry (`16:00 UTC`) occur on the same day (`> 120K BTC` combined OI). | Maximum structural positioning reset of the quarter; massive new-quarter allocation flows follow Monday. | **Stand Down Friday (`100% Cash`)**; prepare full Pillar 1–5 scan for Monday NY open. |
| **M3: Max Pain Roll-Down Capitulation** | `CSU-26D` (Breakdown) | As spot drops `> 8%` below original Max Pain, traders aggressively buy lower puts, dragging **Max Pain down by `$3K–$5K`** mid-week. | Options market repriced lower equilibrium; original Max Pain is obsolete. | Recalculate new Max Pain and Put Wall; do not target old strike levels. |
| **M4: Pre-OpEx Short Squeeze Into Call Wall** | `CSU-26B` (Drift Up) | Spot reaches Max Pain on Thursday, **Domestic USD Spot CVD surges**, and perp shorts (`MOD 01`) get squeezed through Max Pain into the Call Wall. | Organic spot demand overwhelmed dealer pinning and forced upside delta-hedging. | **Bank 50% at Max Pain**; trail remaining 50% up to the Call Wall, then close before `07:30 UTC` Friday. |
| **M5: CME `16:00 UTC` Friday Fixing Twist** | Last Friday of Month (`15:00–16:00 UTC`) | Sharp 60-minute volume/price distortion between `15:00 and 16:00 UTC` as CME settles monthly options against the London BRR index. | Institutional fixing execution noise. | **Avoid New Entries `15:00–16:15 UTC`** on CME expiry Fridays. |
| **M6: Post-OpEx DVOL Collapse** | Friday `08:00 UTC` Settlement | Implied volatility (`DVOL`) drops sharply post-expiry while spot sits dead flat inside a tiny `0.8%` weekend range. | Post-expiry volatility crush (`vol sellers dominating`); next big move waits for Monday NY. | **Hold 100% Cash Over Weekend**; arm `MOD 12A` volatility squeeze breakout alerts for Monday. |
| **M7: Overhang Relief Rally** | `CSU-26D` -> Post-OpEx | Price bled into Friday OpEx due to heavy put hedging; the moment `08:00 UTC` passes, put hedges expire, dealers buy back short futures, and **USD Spot CVD steps in**. | Removal of put-hedging overhang triggers an immediate mechanical relief bounce. | Evaluate `0.375%–0.75% Risk` Spot Long upon 15m/1H VAL reclaim post-`08:00 UTC`. |
| **M8: New-Month Call Wall Magnet Shift** | Post-OpEx Monday | Newly dominant monthly expiry shows massive Call OI building `$10K–$15K` above spot with positive Coinbase Premium. | Institutional positioning for next upside leg is actively establishing. | Align `Stage 2` swing profit targets with the new dominant Call Wall strike. |
