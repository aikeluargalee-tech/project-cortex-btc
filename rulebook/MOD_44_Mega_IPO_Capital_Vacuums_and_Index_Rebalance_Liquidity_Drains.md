# PROJECT CORTEX-BTC — MODULE 44: MEGA-IPO CAPITAL VACUUMS & INDEX REBALANCE LIQUIDITY DRAINS
**Waterfall Tier:** Pillar 1 (Macro Liquidity Plumbing) & Pillar 5 (Institutional Flows & Calendar Calendar-Event Risk) — operates alongside `MOD 07` (Spot ETF Flows), `MOD 17` (Index Rebalancings), `MOD 22` (Net Fed Liquidity), and `MOD 38` (ETF Primary-Market Settlement).
**Empirical Benchmark Anchor:**
1. **SpaceX (`SPCX`) Mega-IPO Vacuum (May–July 2026):** Filed May 20, priced June 11, debuted June 12, 2026 (`~$75B` raise at `~$1.77T` valuation). BTC declined `-19%` to `-28%` across the subscription window alongside `~$4.0B` in June US Spot ETF outflows, and continued bleeding for **18 days post-listing** to `~$57,700–$58,500` in late June/early July before rebounding `+26%+` once capital lockups cleared.
2. **Anthropic (`ANT`) Mega-IPO Vacuum & MSCI `MSTR` Exclusion (November 2026):** Anthropic offering up to `$64.4B` (`825M` shares at `$70–$78`, `~6x` oversubscribed, pricing Nov 18, Nasdaq debut Nov 19, 2026) plus `$26B` strategic placement, overlapping with **MSCI's November 30, 2026 close** removal of Strategy (`MSTR`, `850,364 BTC` treasury; `~13M` index-linked shares), Metaplanet, Upexi, and IREN. US Spot BTC ETFs shed `~$2.35B` across two weeks (7-day withdrawal streak through Nov 13–14), driving BTC from `> $81,000` down to `$65,000–$68,000` (`-18%` to `-23%`).

---

## 1. Machine-Readable State & Routing Block (Python / Hermes / NotebookLM Index)

```yaml
module_id: "MOD_44"
entry_type: "MASTER_EVENT_LIQUIDITY_FILTER"
waterfall_pillar: "PILLAR_1_AND_5_CAPITAL_VACUUM_CALENDAR"
title: "Mega-IPO Capital Vacuums & Index Rebalance Liquidity Drains"

# CALENDAR & LIQUIDITY VACUUM THRESHOLDS
event_parameters:
  mega_ipo_threshold_usd: 25000000000 # >= $25B public offering size (capital siphon threshold)
  mega_ipo_lead_window_days: 30 # Pre-pricing capital commitment & subscription drain window (T-30d to T-0)
  post_ipo_settlement_lag_days: [10, 21] # Empirical lag after listing before IPO escrow/lockup refunds clear (e.g., SpaceX +18d)
  index_rebalance_threshold_usd: 5000000000 # >= $5B passive float-adjusted forced turnover (e.g., MSCI Nov 30, 2026 MSTR/Metaplanet/Upexi)
  index_rebalance_window_days: 14 # T-14d to T+1d around effective close date
  etf_redemption_confirmation:
    streak_days_min: 3 # >= 3 consecutive trading days of net US Spot BTC ETF outflows
    cumulative_outflow_trigger_usd: -750000000 # <= -$750M rolling 10-day US Spot ETF net flow

# ANTI-TRAP CIRCUIT BREAKERS
circuit_breakers:
  CB_01_NO_IPO_DAY_BOTTOM_CALLING: "NEVER buy BTC solely because a Mega-IPO begins trading (T+0). Capital lockups, oversubscription escrow refunds, and passive index rebalances routinely extend selling 10-21 days post-listing (SpaceX June 12 -> July 1 trough)."
  CB_02_ETF_FLOW_VERIFICATION_GATE: "Narrative headlines about 'IPO rotation' are insufficient alone; require physical confirmation via >= 3 consecutive days of US Spot ETF net outflows (MOD 07) and negative Coinbase Premium (MOD 19)."
  CB_03_COMPOUND_DEADLINE_STACKING: "When a Mega-IPO listing window overlaps with a major passive equity index rebalance (e.g., Nov 19 ANT IPO + Nov 30 MSCI MSTR deletion), extend defensive cash lock through the later settlement deadline (T+1 post-rebalance)."
  CB_04_NO_SHORTING_ON_CALENDAR_ALONE: "Strictly enforce 1.0x Spot Only; never short BTC purely on an upcoming IPO date without Pillar 2 order-flow breakdown."

# RISK & SIZING CONSTANTS (PILLAR 4)
risk_parameters:
  active_vacuum_max_risk_pct: 0.00 # Enforce 100% Cash Lock during unabsorbed ETF outflow streaks
  post_settlement_reclaim_risk_pct: 0.75 # Full 0.75% spot risk unlocked only after ETF flows flatten + 4H VAH reclaim
  leverage_permitted: 1.0 # Strict Unleveraged Spot Only
```

---

## 2. Protective Circuit Breakers (Mandatory Event-Liquidity Filters)

* **Circuit Breaker 1 — The Listing-Day Bottom Fallacy (`CB-01`):** Retail traders assume Bitcoin bottoms the moment a Mega-IPO rings the opening bell (`T+0`). Empirically, institutional allocation settlements, oversubscription escrow cycles, and secondary tech rotations keep pressure on liquid crypto proxies for **10 to 21 days after listing** (`SpaceX` debuted June 12, 2026, yet BTC did not bottom until late June / July 1). Never catch falling knives on listing day.
* **Circuit Breaker 2 — Physical Flow Over Headlines (`CB-02`):** Do not freeze trading over routine `$1B–$5B` IPOs. `MOD 44` activates **only** when a single equity offering (or stacked cluster) exceeds **`$25B+`** (or an index deletion forces **`$5B+`** in passive crypto-proxy turnover) **AND** `MOD 07` confirms `>= 3` consecutive days of US Spot BTC ETF net redemptions (`<= -$750M` 10-day cumulative).
* **Circuit Breaker 3 — Stacked Calendar Deadlines (`CB-03`):** When a Mega-IPO (`Nov 19, 2026 ANT`) sits directly ahead of a mandatory passive benchmark deletion (`Nov 30, 2026 MSCI close removing Strategy MSTR, Metaplanet, Upexi`), passive funds execute forced closing-cross sales on the effective date. Keep tactical swing capital in **100% Cash Lock** until the final calendar deadline clears.
* **Circuit Breaker 4 — Re-Entry Authentication (`CB-04`):** Transitioning from post-vacuum defense to generational accumulation requires **both** calendar clearance (`T+1` past final deadline) **and** `MOD 07 / MOD 03 / MOD 11` confirmation (ETF outflows halting + `Domestic USD Spot CVD` higher low + `1H/4H VAH` reclaim).

---

## 3. Core Conditional Signal Units (`Condition A -> Outcome B -> Rule C`)

### CSU-44A: Pre-IPO Capital Siphon & Subscription Drain (`T-30d` to `T-0`)
* **Trigger Condition A (The Telemetry Scan):**
  1. Hermes Calendar / Macro Scanner flags an upcoming Mega-IPO (`>= $25B` offering size, e.g., `SpaceX $75B`, `Anthropic $64.4B`) entering institutional book-building and retail subscription windows (`T-30d` to `T-0`).
  2. **Physical Confirmation:** US Spot BTC ETFs print `>= 3` consecutive daily net outflows (`cumulative 10D <= -$750M`) with `IBIT` leading redemptions (`MOD 07`), while `Coinbase Premium Z-score` turns negative (`MOD 19`).
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Multi-asset funds, family offices, and high-beta retail accounts liquidate their most liquid 24/7 risk asset (BTC / Spot ETFs) to post cash collateral for oversubscribed mega-cap equity allocations.
  * **Probable Trajectory:** Persistent `-15%` to `-28%` liquidity-vacuum drift punctuated by `15:00 ET / 20:00 UTC` BRRNY fix-window Authorized Participant basket sales (`MOD 38 M2`).
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **ENFORCE 100% CASH LOCK (`0.00%` tactical risk).** Tighten trailing stops on any open swing positions (`MOD 18`) and reject all intraday relief-bounce long entries until the subscription drain subsides.

### CSU-44B: Post-Listing Settlement Lag & Escrow Refund Window (`T+0` to `T+21d`)
* **Trigger Condition A (The Telemetry Scan):**
  1. The Mega-IPO prices and begins public trading (`T+0`, e.g., `June 12 SPCX` or `Nov 19 ANT`), **but** US Spot BTC ETFs continue printing net outflows and BTC remains below its `4H VAH` and `STH Realized Price`.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Oversubscribed IPOs (`~6x` demand) lock up billions in brokerage/custodial escrow accounts until post-listing allocation refunds settle, while day-one equity volatility keeps cross-asset risk desks defensive.
  * **Probable Trajectory:** Secondary washout sweep (`10–21 days` post-listing) creating an asymmetric, non-fundamental dislocation trough.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **HOLD 100% CASH LOCK ON LISTING DAY (`T+0`).** Monitor `MOD 03 M8` (Silent Spot Divergence) and `MOD 07 M3` (`IBIT` volume climax at HTF support) for post-settlement absorption.

### CSU-44C: Passive Index Exclusion & Forced Rebalance Window (`T-14d` to `T+1d`)
* **Trigger Condition A (The Telemetry Scan):**
  1. A major index provider (`MSCI`, `S&P`, `Nasdaq-100`) announces the exclusion or weight cut of a major corporate Bitcoin treasury proxy (`>= $5B` passive turnover, e.g., **MSCI removing Strategy `MSTR` [850,364 BTC], Metaplanet, and Upexi effective Nov 30, 2026 close**).
  2. Proxy equity mNAV compresses (`< 1.0x`) and `BTC` breaks `1H/4H VAL` ahead of the effective rebalance close.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Passive index-tracking funds are legally mandated to sell proxy shares into the effective close date, creating mechanical equity-to-crypto contagion and halting corporate treasury ATM share issuance (`MOD 38 M5`).
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **EXTEND 100% CASH LOCK THROUGH REBALANCE CLOSE (`T+0` 21:00 UTC).** Evaluate tactical spot re-entry **only** on `T+1` or later once forced closing-cross volume clears (`MOD 17 M6`) and `Domestic USD Spot CVD` steps in.

### CSU-44D: Post-Vacuum Liquidity Re-Rotation & Reclaim ("The Harvest Setup")
* **Trigger Condition A (The Telemetry Scan):**
  1. Both the Mega-IPO listing (`>= T+5d` to `T+21d`) and any stacked index rebalance deadline (`>= T+1d`) have passed.
  2. **Flow Flip:** US Spot BTC ETFs stop bleeding (`3-day rolling net flow >= $0M`) and `Coinbase USD Spot CVD` prints a confirmed higher low (`MOD 03 M8`).
  3. **Structural Confirmation:** BTC reclaims and holds above its **1H / 4H Volume Profile VAH** (`4+` consecutive 1H bars) with post-cost **`Net R >= 3.0`** (`MOD 37`) and `Pillar 1` (`10Y` yield / `DXY`) stable.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Event-driven liquidity drain is exhausted; sidelined capital and IPO escrow refunds begin rotating back into discounted Bitcoin spot.
  * **Probable Trajectory:** Multi-week mean-reversion expansion (`+20%` to `+35%+` recovery leg, matching the post-SpaceX July–October 2026 rebound).
* **Execution Rule C (The Non-Negotiable Action):**
  * **Entry Trigger:** **UNLOCK FULL `0.75%` EQUITY RISK SPOT LONG** (1.0x unleveraged spot only) on the verified `4H VAH` / `POC` retest, targeting Stage 1 (`50%`) profit harvest at the pre-vacuum breakdown origin.

---

## 4. Dynamic Regime Mutation Lookup Matrix (`M1` through `M8`)

| Mutation ID | Initial State | Telemetry Mutation Observed (`Condition A'`) | Mechanical Meaning (`Outcome B'`) | Mandatory Execution Override (`Rule C'`) |
| :--- | :--- | :--- | :--- | :--- |
| **M1: Mega-IPO Siphon Absorbed Early** | `CSU-44A` (Pre-IPO Drain) | Despite an upcoming `$25B+` IPO, US Spot ETFs print `>= +$300M` net inflows over 3 days and `Coinbase Premium` stays positive above `4H VAH`. | Sovereign/ETF demand is strong enough to absorb equity IPO rotation without a drawdown. | **Downgrade `MOD 44` to Informational Watch;** allow normal `MOD 30` swing execution. |
| **M2: Post-IPO Day-1 Tech Crash Contagion** | `CSU-44B` (`T+0` Listing) | The Mega-IPO breaks below its IPO offer price on Day 1–3, triggering a `> -3%` Nasdaq tech sell-off and `VIX > 25` (`MOD 29`). | Capital vacuum mutated into broad cross-asset equity contagion (`MOD 29`). | **Maintain Strict `GATE_RED` 100% Cash Lock** until Nasdaq/NVDA stabilize and `ICDM < 60`. |
| **M3: Oversubscription Escrow Refund Surge** | `CSU-44B` (`T+3d` to `T+10d`) | Institutional/retail IPO refund cash hits brokerage accounts; `IBIT` volume spikes `>= 2.5x` average on an up-close (`MOD 07 M3`) with `USD Spot CVD` vertical. | Refunded IPO capital is rotating directly back into discounted Bitcoin spot. | **Accelerate Transition to `CSU-44D`:** Authorize `0.375%–0.75%` Spot Long upon `1H/4H VAH` reclaim. |
| **M4: Stacked IPO + Index Rebalance Double Drain** | `CSU-44A` + `CSU-44C` | A `$25B+` IPO listings window falls within 14 days of a major MSCI/S&P crypto-proxy deletion (e.g., `Nov 19 ANT` + `Nov 30 MSCI MSTR`). | Sequential dual liquidity drain prevents a clean V-bottom between the two dates. | **Lock 100% Cash Across Both Windows;** delay full `0.75%` deployment until `T+1` post-rebalance. |
| **M5: Proxy Treasury Forced-Sale Rumor Panic** | `CSU-44C` (Index Deletion) | Social media panics that an excluded treasury company (`MSTR`) must liquidate its BTC stack, causing a `-8%` single-day flush wick into `MOD 11A VAL` while `USD Spot CVD` absorbs. | Index deletion forces *passive equity funds* to sell shares—it does **not** force the company to sell underlying BTC. | **Prepare `CSU-42B` Wyckoff Spring Reclaim** once forced equity selling exhausts (`T+1` post-close). |
| **M6: Non-Crypto Mega-IPO Without ETF Outflows** | Calendar Alert (`>= $25B` IPO) | A major industrial/energy IPO launches (`>= $25B`), **but** US Spot BTC ETFs show zero outflow streak and `A_P,V` remains positive. | The IPO is drawing capital from value/industrial equities rather than crypto risk pools. | **Ignore Calendar Alert (`CB-02`);** execute baseline `MOD 33` radar signals. |
| **M7: Year-End Tax-Loss + Rebalance Compression** | Nov–Dec Rebalance Window | November 30 MSCI deletion is immediately followed by December institutional tax-loss harvesting on underwater ETF positions. | Year-end balance-sheet window dressing extends sideways accumulation before Q1 inflows. | **Size Entries at `0.375%` (`GATE_AMBER`)** until January ETF inflows confirm full `0.75%` risk. |
| **M8: Hermes Calendar Pre-Emptive Flag** | `T-35d` Before Event | Hermes Agent scans upcoming SEC S-1 filings / MSCI quarterly review announcements and detects an upcoming `>= $25B` IPO or `>= $5B` proxy deletion. | Early-warning visibility before mainstream retail traders notice the liquidity drain. | **Publish `MOD 44` Alert on Telegram HUD** and tighten Stage 1 profit-taking thresholds on open longs. |
