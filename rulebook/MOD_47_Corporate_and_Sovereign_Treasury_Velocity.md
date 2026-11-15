# PROJECT CORETEX BTC BRAIN — MODULE 47: CORPORATE & SOVEREIGN TREASURY VELOCITY (mNAV & PROXY FLYWHEEL)
**Waterfall Tier:** Pillar 1 (Macro & Institutional Capital Allocation) & Pillar 5 (Corporate/Sovereign Balance-Sheet Flows & Supply Absorption) — operates alongside `MOD 07` (Spot ETF Flows), `MOD 17` (Index Rebalancings), `MOD 38` (Corporate Treasury ATM / TWAP Supply), `MOD 39` (Exchange Supply & Cold Sweeps), and `MOD 44` (Index Rebalance Liquidity Drains).
**Empirical Benchmark Anchor:**
1. **2024–2025 Accretive `mNAV` Flywheel:** Listed Digital Asset Treasury (DAT) companies traded at `1.8x–2.5x+` `mNAV`, enabling continuous At-The-Market (ATM) equity and zero-coupon convertible issuance to buy spot BTC accretively—acting as a persistent structural bid alongside US Spot ETFs.
2. **2026 `mNAV` Compression & Buyback Pivot (November 2026 Benchmark):** Across 2026, corporate treasury premiums compressed sharply: **Strategy (`MSTR`, `850,364 BTC` / `~4.05%` of total BTC supply; `~$19.7B` senior debt/preferred stack)** saw `mNAV` compress from `> 2.0x` down to `~0.93x–1.21x` (and authorized `$1.0B` in share buybacks on June 29, 2026), while **Metaplanet (`TSE: 3350`, `44,000 BTC`)** compressed to **`~0.49x mNAV`** and deployed `¥28.27B` (`108.7M` shares) into share repurchases rather than new BTC accumulation ahead of **MSCI's November 30, 2026** index deletion.

---

## 1. Machine-Readable State & Routing Block (Python / Hermes / GitHub Index)

```yaml
module_id: "MOD_47"
entry_type: "INSTITUTIONAL_SUPPLY_AND_FLYWHEEL_ENGINE"
waterfall_pillar: "PILLAR_1_AND_5_TREASURY_VELOCITY"
title: "Corporate & Sovereign Treasury Velocity (mNAV & Proxy Flywheel)"

# mNAV & CORPORATE TREASURY FLYWHEEL THRESHOLDS
mnav_parameters:
  flywheel_expansion_zone: 1.35 # mNAV >= 1.35x -> Accretive ATM equity issuance active (structural BTC spot bid)
  neutral_stall_zone: [1.00, 1.34] # mNAV 1.00x - 1.34x -> ATM issuance slows; companies pivot to preferreds/buybacks
  discount_freeze_zone: 0.99 # mNAV < 1.00x -> Equity issuance is dilutive to BTC-per-share; ATM spot bid freezes
  distress_liquidation_watch: 0.65 # mNAV <= 0.65x + senior debt maturity wall -> Monitor treasury restructuring risk
  corporate_accumulation_velocity_30d:
    strong_bid_btc: 15000 # >= +15,000 BTC net 30D corporate/sovereign treasury additions
    frozen_bid_btc: 2500 # <= +2,500 BTC net 30D additions (structural corporate bid offline)

# SOVEREIGN RESERVE & CEBE (COMMON EQUITY BITCOIN EXPOSURE) METRICS
structural_checks:
  cebe_senior_claim_ratio_warning: 0.35 # Senior debt + preferred notional >= 35% of gross BTC treasury value
  sovereign_strategic_reserve_trigger: "Confirmed G20 / Central Bank / Sovereign Wealth Fund treasury allocation or legislative reserve bill enactment"

# ANTI-TRAP CIRCUIT BREAKERS
circuit_breakers:
  CB_01_NO_MNAV_DISCOUNT_SELL_PANIC: "NEVER assume an mNAV < 1.0x discount (e.g., Metaplanet 0.49x or MSTR 0.93x-1.08x) automatically forces a treasury company to dump its BTC on the open market; check debt maturity walls and cash reserves first."
  CB_02_ATM_EXECUTION_TIMING: "Corporate ATM announcements do NOT equal instant market-buy breakout triggers; treasuries typically execute via multi-day OTC/TWAP desks (MOD 21 / MOD 38 M5). Require live Domestic USD Spot CVD confirmation."
  CB_03_FROZEN_BID_ADJUSTMENT: "When aggregate DAT mNAV < 1.15x, remove 'corporate treasury ATM buying' from bullish confluence models—rely strictly on US Spot ETFs (MOD 07) and Domestic USD Spot CVD (MOD 05)."
  CB_04_NO_PROXY_STOCK_SUBSTITUTION: "Project CoreTex BTC Brain executes strictly 1.0x Spot BTC (and USDT)—never substitute leveraged proxy equities (MSTR/Metaplanet) for spot BTC exposure."

# RISK & SIZING CONSTANTS (PILLAR 4)
risk_parameters:
  max_portfolio_risk_pct: 0.75
  frozen_flywheel_risk_cap_pct: 0.375 # Cap tactical breakout sizing at 0.375% if corporate bid is frozen unless ETFs > +$400M/day
  leverage_permitted: 1.0 # Strict Unleveraged Spot Only
```

---

## 2. Protective Circuit Breakers (Mandatory Treasury-Flywheel Invariants)

* **Circuit Breaker 1 — Discount `mNAV` Is Not Forced BTC Liquidation (`CB-01`):** When a treasury stock trades below `1.0x mNAV` (such as Metaplanet at `~0.49x` or Strategy near `0.93x–1.08x`), issuing equity becomes dilutive to BTC-per-share, **freezing new corporate BTC purchases** and shifting management toward stock buybacks. However, unless unsecured debt maturities or preferred dividend shortfalls force asset sales, discounted `mNAV` removes a *buyer* rather than creating a *forced BTC seller*.
* **Circuit Breaker 2 — OTC/TWAP Execution Reality (`CB-02`):** Corporate treasury purchases rarely chase spot order books at market; they execute via institutional OTC desks and algorithmic TWAP slices (`MOD 21`). Never buy a headline treasury purchase announcement (`Form 8-K`) unless price simultaneously holds above `4H VAH` with positive `Domestic USD Spot CVD`.
* **Circuit Breaker 3 — Remove Phantom Corporate Bid During Compression (`CB-03`):** Whenever leading treasury `mNAV` averages `< 1.15x`, treat the corporate ATM flywheel as **OFFLINE (`0 BTC` marginal demand)**. Require US Spot ETF inflows (`MOD 07`) and `Coinbase USD Spot CVD` to carry 100% of the bullish burden.
* **Circuit Breaker 4 — Pure `1.0x` Spot BTC Execution (`CB-04`):** Proxy equities carry double-beta risk (`BTC` price beta $\times$ `mNAV` multiple compression + index deletion risk). Execute exclusively in `1.0x` Spot BTC and USDT.

---

## 3. Core Conditional Signal Units (`Condition A -> Outcome B -> Rule C`)

### CSU-47A: Accretive `mNAV` Flywheel Expansion (`mNAV >= 1.35x` + Rising Velocity)
* **Trigger Condition A (The Telemetry Scan):**
  1. Benchmark treasury `mNAV` (`Strategy` and top-5 corporate holders) holds `>= 1.35x` with positive 14-day slope.
  2. Net 30-day corporate + sovereign BTC treasury additions exceed **`+15,000 BTC`** (`>= ~1.1x` monthly new miner issuance of `13,500 BTC`).
  3. `Pillar 1` is `GATE_GREEN` and `Domestic USD Spot CVD` confirms upward absorption (`MOD 05A`).
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Treasury companies can issue equity/convertibles at a premium to NAV and convert proceeds into spot BTC, absorbing more than 100% of daily post-halving miner supply (`~450 BTC/day`).
  * **Probable Trajectory:** Persistent structural floor beneath `4H/1D POC` and shallow pullbacks (`-8%` to `-15%`) during bull expansions.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **AUTHORIZE FULL `0.75%` SPOT RISK** on verified `MOD 11` / `MOD 30` pullback reclaims; prioritize Stage 2 trailing runners (`MOD 18`).

### CSU-47B: `mNAV` Compression & Buyback Pivot (`mNAV <= 1.10x` — Corporate Bid Frozen)
* **Trigger Condition A (The Telemetry Scan):**
  1. Benchmark corporate treasury `mNAV` compresses to `<= 1.10x` (or `< 1.00x` discount) and 30-day corporate net BTC additions drop below **`+2,500 BTC`**.
  2. Treasury managements pivot capital allocation from buying spot BTC to **repurchasing their own discounted shares** (e.g., Strategy `$1.0B` buyback authorization; Metaplanet `¥60B` buyback program).
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** A major pillar of 2024–2025 marginal spot demand has stepped off the bid; BTC becomes more sensitive to US Spot ETF flows (`MOD 07`) and macro liquidity (`MOD 22`).
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **STRIP CORPORATE BID ASSUMPTION FROM MODELS (`CB-03`).** Cap tactical breakout risk at **`0.375%` (`GATE_AMBER`)** unless US Spot ETFs print `>= +$400M/day` net inflows and `Coinbase USD Spot CVD` leads independently.

### CSU-47C: Corporate Treasury Balance-Sheet Stress / Restructuring Alert (`mNAV <= 0.65x` + Debt Wall)
* **Trigger Condition A (The Telemetry Scan):**
  1. A top-5 corporate BTC holder (`>= 25,000 BTC`) trades below **`0.65x mNAV`** while facing an imminent convertible put date, covenant breach, or unhedged cash-interest shortfall, **AND** on-chain attribution (`MOD 39`) detects corporate custody outflows toward exchange/OTC desks.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Risk of forced balance-sheet deleveraging (partial BTC liquidation to retire senior claims or fund buybacks/debt service), triggering acute headline contagion.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **ENFORCE IMMEDIATE `100% CASH LOCK` (`0.00%` risk).** Wait for the liquidation block to clear on-chain (`MOD 39`) and `1H/4H VAH` to reclaim before re-entering.

### CSU-47D: Sovereign Strategic Reserve Adoption Catalyst (`G20` / Central Bank / SWF Allocation)
* **Trigger Condition A (The Telemetry Scan):**
  1. Official confirmation (central bank balance sheet, sovereign wealth fund filing, or enacted national treasury execution) of direct sovereign BTC spot accumulation (`>= 10,000 BTC` mandate), validated by multi-day `Coinbase USD Spot CVD` surge (`MOD 05A`) and `4H VAH` breakout.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Game-theoretic sovereign adoption shock permanently removes liquid float into multi-decade state custody (`MOD 39 CSU-39B`).
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **UPGRADE `Pillar 1` TO `GATE_GREEN` (`0.75%` max risk)** upon first `1H/4H VAH` retest with `Net R >= 3.0` (`MOD 37`); widen Stage 2 trailing stop behind `1D VAL`.

---

## 4. Dynamic Regime Mutation Lookup Matrix (`M1` through `M8`)

| Mutation ID | Initial State | Telemetry Mutation Observed (`Condition A'`) | Mechanical Meaning (`Outcome B'`) | Mandatory Execution Override (`Rule C'`) |
| :--- | :--- | :--- | :--- | :--- |
| **M1: `mNAV` Re-Expansion Above `1.35x`** | `CSU-47B` (Frozen Bid) | BTC rallies above `200D MA` + `STH Realized Price`, lifting leading treasury `mNAV` back above `1.35x` and restarting weekly ATM BTC buys. | The corporate equity-to-BTC flywheel just re-ignited. | **Upgrade Treasury Velocity to `GREEN`;** unlock full `0.75%` spot risk on `MOD 30` setups. |
| **M2: Buyback-Funded BTC Sale (`ETHZilla` / `MSTR` Clause)** | `CSU-47B` (`mNAV < 0.90x`) | A treasury company announces selling a tranche of spot BTC specifically to repurchase deeply discounted stock or preferred shares. | Net corporate treasury supply turns negative (`-BTC` flow) even without insolvency. | **Enforce `100% Cash Lock` for `48–72H`** until OTC/spot absorption completes (`MOD 06A`). |
| **M3: Post-Index-Exclusion `mNAV` Capitulation Bottom** | `CSU-47B` + `MOD 44` | After an MSCI/S&P index deletion close (`Nov 30, 2026`), proxy equity `mNAV` bottoms out while `BTC` holds `4H VAL` on positive `USD Spot CVD`. | Forced passive equity selling exhausted without triggering underlying BTC sales (`MOD 44 M5`). | **Evaluate `0.375%–0.75%` Spot Long** once `1H/4H VAH` reclaims (`MOD 37 Net R >= 3.0`). |
| **M4: Preferred-Stock "Phantom Growth" Divergence** | `CSU-47A` / `47B` | Treasury buys BTC via high-yield perpetual preferred stock (`STRK/STRF/STRC`), lifting gross BTC count while common `CEBE` per share stays flat. | Rising senior-claim drag increases long-term balance-sheet fragility during drawdowns. | **Do Not Treat Preferred-Funded Buys as Tier-1 Bull Fuel;** require independent Spot ETF confirmation. |
| **M5: Rumored Sovereign Reserve vs. Actual Execution** | Any State | Social media rumors a nation-state is buying BTC, **but** `Coinbase USD Spot CVD` is flat/negative and price rejects at `4H VAH`. | Unverified sovereign rumor used by offshore perp traders as exit liquidity (`MOD 05C`). | **Reject Breakout Entry (`CB-02`);** require hard on-chain/filing proof + `USD Spot CVD`. |
| **M6: Treasury-to-Treasury M&A Consolidation** | `CSU-47B` (`mNAV < 0.80x`) | A higher-`mNAV` treasury company acquires a distressed `< 0.75x mNAV` peer via stock swap. | Keeps BTC locked in corporate custody rather than hitting public spot order books. | **Neutralize Contagion Fear;** maintain baseline `MOD 33` radar posture. |
| **M7: ATM Announcement Fade Trap** | Intraday Rally | Treasury announces `$500M` BTC purchase on Monday morning, price spikes `+2%` into `4H VAH`, then `USD Spot CVD` turns negative as APs/arbs sell into the news. | Purchase already occurred via OTC the prior week; Monday's news is retail FOMO liquidity. | **Never Chase Monday 8-K Announcements;** wait for `4H VAL/POC` pullback retest. |
| **M8: `mNAV` Data Feed Lag (`MOD 36`)** | Routine Scan | Treasury dashboard API lags > 24H during a rapid `+/- 10%` BTC move. | Stale `mNAV` denominator distorts premium/discount reading. | Tag `MOD_47_STATE = UNKNOWN` (`MOD 36`); rely on live `MOD 07` ETF flows + `USD Spot CVD`. |
