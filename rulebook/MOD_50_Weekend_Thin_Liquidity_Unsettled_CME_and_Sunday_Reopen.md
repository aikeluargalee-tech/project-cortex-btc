# PROJECT CORETEX BTC BRAIN — MODULE 50: WEEKEND THIN-LIQUIDITY, UNSETTLED CME CLEARING & SUNDAY 22:00 UTC RE-OPEN PROTOCOL
**Waterfall Tier:** Pillar 2 (Microstructure & Session Liquidity) & Pillar 4 (Execution Timing & Sizing Governor) — operates directly alongside `MOD 05` (Spot vs. Perp CVD), `MOD 07` (Domestic USD Gateways vs. Offshore), `MOD 17` (Session Handoffs), `MOD 20` (CME Basis & Gap Topology), and `MOD 37` (Executable L2 Depth & Slippage).
**Empirical Benchmark Anchor:**
1. **November 15, 2026 Live Weekend Sweep & Bounce:** On Sunday, November 15, 2026 (`01:44 UTC` / `09:44 AM MYT`), Bitcoin swept down to **`$62,199`** (`RM 253,910`) during thin weekend liquidity before rebounding `+4.2%` to **`~$64,800`** (`RM 264,961`) by `04:50 UTC` (`12:50 PM MYT`), while US Spot BTC ETFs (`-$1.07B` across Nov 9–13) remained closed until Monday's US cash session.
2. **2026 CME Weekend Trading vs. Next-Business-Day Settlement Constraint:** Following CME's May 2026 Globex expansion, covered crypto futures trade over weekends (with a 2-hour weekly maintenance window), **but** clearing, margin settlement, and Fedwire bank transfers still do not settle until the next business day (facing `$3.73B` median / `$24.31B` stress pre-funding hurdles), leaving institutional ETF Authorized Participants and prime clearing desks largely sidelined until **Sunday `22:00–23:00 UTC` (`06:00–07:00 AM MYT` Monday)** and **Monday `13:30–14:30 UTC` (`21:30–22:30 MYT`)**.

---

## 1. Machine-Readable State & Routing Block (Python / Hermes / GitHub Index)

```yaml
module_id: "MOD_50"
entry_type: "WEEKEND_LIQUIDITY_AND_SETTLEMENT_GOVERNOR"
waterfall_pillar: "PILLAR_2_AND_4_WEEKEND_EXECUTION"
title: "Weekend Thin-Liquidity, Unsettled CME Clearing & Sunday 22:00 UTC Re-Open Protocol"

# WEEKEND & INSTITUTIONAL SETTLEMENT WINDOWS (UTC / MYT)
session_windows:
  weekend_thin_window_utc: "Friday 21:00 UTC to Sunday 22:00 UTC" # Saturday 05:00 MYT to Monday 06:00 MYT
  cme_maintenance_blackout_utc: "Friday 21:00 UTC to Friday 23:00 UTC"
  sunday_weekly_reopen_utc: "Sunday 22:00 UTC to Monday 01:00 UTC" # Monday 06:00 - 09:00 MYT
  monday_us_etf_cash_open_utc: "Monday 13:30 UTC to Monday 15:30 UTC" # Monday 21:30 - 23:30 MYT
  l2_depth_haircut_threshold_pct: -35.0 # Weekend top-of-book L2 depth typically drops 35%-55% vs weekday median

# ANTI-TRAP CIRCUIT BREAKERS
circuit_breakers:
  CB_01_NO_WEEKEND_BREAKOUT_CHASING: "NEVER chase a Saturday or Sunday breakout above 4H VAH with full 0.75% risk while US Spot ETFs and Fedwire clearing are closed; require Monday 00:00 UTC weekly close + NY ETF Cash Open (13:30 UTC) confirmation."
  CB_02_UNSETTLED_CME_VOLUME_FILTER: "Treat Saturday/Sunday CME futures prints as pre-settled weekend positioning; wait until Sunday 22:00-23:00 UTC clearing handoff before trusting CME basis shifts (MOD 20)."
  CB_03_SPREAD_AND_SLIPPAGE_GATE: "During Friday 21:00 UTC - Sunday 22:00 UTC, enforce MOD 37 strict passive limit-order execution only; reject market orders if 1% L2 book depth drops > -40% below 30D weekday median."
  CB_04_BEAR_VACUUM_WEEKEND_LOCK: "When Pillar 1 == GATE_RED or MOD 44 Mega-IPO/Index drain is active, enforce strict 100% Cash Lock across the entire weekend regardless of +3% to +5% Sunday relief bounces."

# RISK & SIZING CONSTANTS (PILLAR 4)
risk_parameters:
  weekend_counter_trend_max_risk_pct: 0.00 # 0.00% during GATE_RED / MOD 44 locks
  weekend_authenticated_spring_risk_pct: 0.375 # Half-size (0.375% max) ONLY if Pillar 1 == GATE_GREEN + USD Spot CVD confirms
  post_monday_ny_open_max_risk_pct: 0.75 # Full 0.75% unlocked only after Monday NY ETF Cash Open confirmation
  leverage_permitted: 1.0 # Strict Unleveraged Spot Only
```

---

## 2. Protective Circuit Breakers (Mandatory Weekend Invariants)

* **Circuit Breaker 1 — No Weekend Breakout Chasing (`CB-01`):** Thin weekend order books (`-35%` to `-55%` L2 depth) allow offshore perp desks to engineer `+3%` to `+6%` squeezes above `4H VAH` that mean-revert once institutional ETF and macro desks return on Monday. Cap weekend exposure at **`0.375%` (`GATE_AMBER`)** even in `GATE_GREEN` regimes, unlocking full **`0.75%`** only after Monday `13:30–15:30 UTC` NY confirmation.
* **Circuit Breaker 2 — Unsettled Weekend CME Distortion (`CB-02`):** Weekend CME crypto trades remain unsettled on clearing members' books until Monday banking hours; never treat Saturday/Sunday CME volume spikes as settled institutional accumulation (`MOD 20`).
* **Circuit Breaker 3 — Passive Limit-Only Execution (`CB-03`):** Thin weekend depth widens effective slippage (`MOD 37`). All weekend entries or exits must use passive limit orders placed inside `MOD 11` Volume Profile nodes.
* **Circuit Breaker 4 — Bear-Vacuum Weekend Lock (`CB-04`):** During `GATE_RED` or `MOD 44` calendar drains (e.g., November 15, 2026 `$62,199 -> $64,800` Sunday bounce inside the Nov 19 ANT IPO / Nov 30 MSCI window), maintain **`100% Cash Lock` (`0.00%` risk)** through the weekend.

---

## 3. Core Conditional Signal Units (`Condition A -> Outcome B -> Rule C`)

### CSU-50A: Weekend Thin-Book Stop-Hunt & Sunday Liquidity Sweep
* **Trigger Condition A:** Between Friday `21:00 UTC` and Sunday `20:00 UTC`, BTC sweeps below a prior week's low or `4H VAL` (`-3%` to `-8%`), triggers offshore perp liquidations (`MOD 03`), and rapidly reclaims `4H VAL` while `Coinbase USD Spot CVD` (`MOD 05`) absorbs the dip.
* **Observed Outcome B:** Thin weekend liquidity exaggerated a stop-run into resting spot bids without settled institutional ETF selling.
* **Execution Rule C:** If `Pillar 1 == GATE_GREEN` (and `MOD 44` is inactive), allow a **half-size `0.375%` spot limit entry** with stop below the sweep low; if `Pillar 1 == GATE_RED` or `MOD 44` is active, **hold `100% Cash Lock` (`0.00%`)** until Monday NY ETF open.

### CSU-50B: Weekend Fakeout Breakout Above `4H VAH`
* **Trigger Condition A:** BTC breaks above `4H VAH` on Saturday or Sunday driven by rising offshore `Perp OI` and positive `Funding`, while `Coinbase USD Spot CVD` is flat/negative (`MOD 05C` Quad 3).
* **Observed Outcome B:** Leverage-driven weekend markup lacking US institutional spot backing; high probability of a Sunday `22:00 UTC` / Monday `13:30 UTC` fade back into the prior range.
* **Execution Rule C:** **REJECT WEEKEND BREAKOUT ENTRY (`CB-01`).** Wait for Monday `14:30 UTC` US Spot ETF open to prove real cash demand.

### CSU-50C: Sunday `22:00 UTC` Clearing Handoff & Weekly Close Authentication
* **Trigger Condition A:** At Sunday `22:00 UTC` (`06:00 AM MYT` Monday) through Monday `00:00 UTC` weekly close, CME clearing re-opens without a gap-down breakdown, `BTC` holds above `4H VAH` (`4+` consecutive `1H` bars), and `Asian/European` spot sessions hold Friday's settlement value.
* **Observed Outcome B:** Weekend structure survived the weekly clearing handoff intact.
* **Execution Rule C:** Prepare **`0.375%` initial spot tranche** at `4H POC/VAH` retest, scaling to **`0.75%`** upon Monday `13:30–15:30 UTC` NY ETF flow confirmation (`MOD 07`).

### CSU-50D: Monday `13:30 UTC` NY Cash Open Gap-Fill & Trend Resolution
* **Trigger Condition A:** Monday NY cash equity & Spot ETF session opens (`13:30–15:30 UTC`); if a weekend price gap (`>= 1.5%` from Friday `21:00 UTC` CME settlement) exists, price tests the gap zone and prints either a `Domestic USD Spot CVD` higher-low reclaim or an ETF outflow breakdown (`MOD 38 M2`).
* **Observed Outcome B:** Settled institutional flow resolves the weekend divergence into the true weekly directional impulse.
* **Execution Rule C:** **DEPLOY FULL `0.75%` SPOT RISK** (`MOD 37 Net R >= 3.0`) only if gap retest holds with positive `USD Spot CVD` and `ETF inflows >= $0M`; otherwise enforce `100% Cash Lock`.

---

## 4. Dynamic Regime Mutation Lookup Matrix (`M1` through `M8`)

| Mutation ID | Initial State | Telemetry Mutation Observed | Mandatory Execution Override |
| :--- | :--- | :--- | :--- |
| **M1: Sunday `22:00 UTC` Gap-Down Flush** | `CSU-50C` | CME weekly open at `22:00 UTC` triggers an immediate `-2%` to `-4%` gap-fill flush back to Friday's `21:00 UTC` close. | **Do Not Market-Buy the Open;** wait `2–4 hours` for `1H VAL` stabilization (`MOD 11`). |
| **M2: Monday NY Open ETF Outflow Ambush** | Weekend Bounce | BTC rallies `+4%` on Sunday, then Monday `14:30–16:00 UTC` prints heavy `IBIT/FBTC` primary redemptions (`MOD 38`). | **Confirm `CB-01` Veto Validated;** stay in `100% Cash Lock`. |
| **M3: Unfilled Runaway Weekend Gap (`GATE_GREEN`)** | `CSU-50C` | In `REGIME_1` (`GATE_GREEN`), a `+3%+` weekend gap fails to fill by Monday `16:00 UTC` and `IBIT` opens with `+$300M+` volume surge. | **Enter on First `1H VAH` Pullback (`0.75%` risk)** rather than waiting indefinitely for a full gap fill (`MOD 20 M1`). |
| **M4: Holiday Extended 3-Day US Market Closure** | US Bank Holiday | Fedwire, CME clearing, and US Spot ETFs remain closed through Monday (e.g., Memorial Day, Labor Day, MLK Day). | **Extend Weekend Protocol Through Tuesday `13:30 UTC`** (`CB-01`). |
| **M5: Weekend Exchange Maintenance / Outage** | Sat–Sun Session | Major USD spot venue (`Coinbase`/`Kraken`) enters scheduled weekend maintenance, dropping `MOD 36` quorum below 3 venues. | **Tag `TRUST = UNKNOWN` (`MOD 36`) & Lock `100% Cash`** until all 3 venues resume. |
| **M6: High-Correlation `NDX` Futures Open (`MOD 49`)** | Sun `22:00 UTC` | `Corr(BTC, NDX)_30D >= +0.65` and `NQ` futures gap down `> -1.5%` at Sunday `22:00 UTC` open. | **Enforce `MOD 49 CB-02` Contagion Lock** immediately. |
| **M7: Weekend Whale Cold-Storage Sweep (`MOD 39`)** | Sat–Sun Session | Large spot buyers withdraw `> 5,000 BTC` off Coinbase/Kraken into cold storage over the weekend despite thin volume. | **Flag Bullish Accumulation Watch;** execute upon Monday NY Open confirmation. |
| **M8: Weekend Stablecoin De-Peg Scare (`MOD 48`)** | Sat–Sun Session | Thin weekend liquidity causes brief `USDT/USDC` wick to `$0.993` that recovers within `< 30 mins`. | **Pause `60 mins` to verify peg stability** before resuming normal radar monitoring. |
