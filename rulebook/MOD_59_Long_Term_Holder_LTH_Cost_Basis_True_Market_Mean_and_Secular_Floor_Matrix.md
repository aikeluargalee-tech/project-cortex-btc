# PROJECT CORETEX-BTC BRAIN — MODULE 59: LONG-TERM HOLDER (LTH) COST BASIS, TRUE MARKET MEAN & SECULAR FLOOR MATRIX

**Waterfall Tier:** Pillar 5 (On-Chain Valuation, Cohort Cost-Basis Stack & Sovereign Barbell Reserve Governance) — operates directly alongside `MOD 13` (STH Realized Price & MVRV), `MOD 14` (SOPR Reset Cycles), `MOD 15` (Realized Cap Impulse & LTH-to-STH Wealth Transfer), `MOD 18` (`CSU-18D` Sovereign Cold-Storage Tranches), `MOD 32` (`2-of-3` Dual-Jurisdiction Multi-Sig Custody), `MOD 41` (Secular Cycle ATH Exit Engine), `MOD 46` (Block `1,050,000` April 2028 Secular Horizon), and `MOD 56` (Secular Cycle Anatomy & Diminishing Returns).
**Empirical Benchmark Anchor:** Q4 2026 Multi-Cohort Cost-Basis Stack — Bitcoin breaking below Short-Term Holder Realized Price (`$75,600–$75,771`), US Spot ETF Cost Basis (`~$81,500`), and the Cointime-Weighted **True Market Mean / Active Investor Realized Price (`~$77,500–$78,000`)** down toward the `$64,000` Epoch 4 Halving baseline, while Aggregate Realized Price (`~$53,000–$55,000`) and Long-Term Holder (`LTH`, UTXOs >= 155 days) Realized Price (`LTH-MVRV ~1.45–1.55`, MVRV Z-Score `~0.59`) define the deeper secular accumulation tiers below.
**Governance Posture:** Multi-horizon on-chain valuation & barbell reserve governor (`ZERO_INTRADAY_SCALP_SIGNALS`). Governs Sleeve B (`2-of-3` multi-sig cold storage) accumulation tranches and macro overhead cost-basis resistance walls while deferring tactical Sleeve A (`<= 0.75%` risk) execution timing to Pillars 1–4.

---

#### 1. Machine-Readable State & Routing Block (Python / Hermes / NotebookLM Index)

```yaml
module_id: "MOD_59"
entry_type: "SECULAR_ONCHAIN_VALUATION_AND_RESERVE_MATRIX"
waterfall_pillar: "PILLAR_5_COHORT_COST_BASIS_AND_SECULAR_FLOOR"
title: "Long-Term Holder (LTH) Cost Basis, True Market Mean & Secular Floor Matrix"

# MASTER WATERFALL AUTHORITY & BARBELL ROUTING
waterfall_authority: "PILLAR_5_SECULAR_VALUATION_GOVERNOR"
barbell_routing:
  sleeve_a_tactical_swing: "Cannot override Pillar 1 GATE_RED or MOD 44/58 locks; uses MOD 59 levels strictly as macro support/resistance context."
  sleeve_b_sovereign_vault: "Primary quantitative trigger matrix for CSU-18D & CSU-46A generational cold-storage tranches (2-of-3 multi-sig)."

# ON-CHAIN COST-BASIS & VALUATION STACK DEFINITIONS
cost_basis_stack:
  tier_1_sth_realized_price: "UTXOs aged < 155 days (governed by MOD 13; ~$75,600-$75,771 Q4 2026 benchmark)"
  tier_2_true_market_mean: "Active Investor Realized Price (Cointime-weighted Realized Cap / Active Supply; ~$77,500-$78,000 Q4 2026 benchmark)"
  tier_3_aggregate_realized_price: "Total Realized Cap / Circulating Supply (all-coin on-chain cost basis; ~$53,000-$55,000 Q4 2026 benchmark)"
  tier_4_lth_realized_price: "UTXOs aged >= 155 days held outside exchange reserves (LTH_MVRV = Spot_Price / LTH_Realized_Price)"
  tier_5_secular_200w_sma: "200-Week Simple Moving Average (cross-referenced with MOD 17 M7 & MOD 18 CSU-18D)"

# SECULAR VALUATION BANDS (DIMINISHING-VOLATILITY ADJUSTED PER MOD 56)
valuation_thresholds:
  lth_mvrv_bands:
    GENERATIONAL_CAPITULATION: "<= 1.00 (LTH cohort underwater in aggregate; historical bear-market bottom zone)"
    DEEP_VALUE_ACCUMULATION: "1.01 to 1.35 (Post-flush accumulation & True Market Mean discount)"
    NEUTRAL_MID_CYCLE: "1.36 to 2.40"
    DISTRIBUTION_WARNING: ">= 2.80 to 3.50 (Veteran LTH profit-taking acceleration; arm MOD 41)"
  mvrv_z_score_bands:
    SECULAR_FLOOR_ZONE: "<= 0.00 (Market Cap <= Realized Cap; historically < -0.50 to 0.00 marks generational troughs)"
    DEEP_VALUE_ZONE: "0.01 to 0.75 (Q4 2026 benchmark ~0.59)"
    CYCLE_OVERHEATED_ZONE: ">= 3.00 to 4.50 (Adjusted downward from 2013-2017 7.0+ peaks per MOD 56 diminishing-return law)"
  entity_adjusted_nupl_bands:
    CAPITULATION_RED: "< 0.00 (Net market unrealized loss)"
    HOPE_FEAR_ORANGE: "0.00 to 0.25"
    OPTIMISM_YELLOW: "0.25 to 0.50"
    BELIEF_GREEN: "0.50 to 0.70"
    EUPHORIA_BLUE: ">= 0.70 (Cross-trigger MOD 13C & MOD 41 cycle harvest)"

# ANTI-TRAP CIRCUIT BREAKERS
circuit_breakers:
  CB_01_COHORT_AGING_ILLUSION: "NEVER interpret a rising LTH Realized Price during a bear market as fresh institutional buying; coins bought near cycle highs automatically age past 155 days and mechanically pull LTH Realized Price upward."
  CB_02_SLEEVE_A_CASH_LOCK_SUPREMACY: "Deep on-chain value (e.g., Spot < True Market Mean) NEVER authorizes Sleeve A tactical swing entries while Pillar 1 == GATE_RED, MOD 44 IPO/MSCI vacuum is active, or MOD 58 Trinity Lock is engaged."
  CB_03_ETF_STABILIZATION_PREREQUISITE: "Before deploying Sleeve B Sovereign Cold-Storage tranches into a deep value zone, require US Spot ETF 3-day net outflows to halt (>= $0M) per MOD 38 & MOD 46 CSU-46A."
  CB_04_OVERHEAD_BREAKEVEN_SUPPLY_WALL: "When 6m-2y coin cohorts sit underwater above spot price (e.g., $88k-$100k shelves), treat initial rallies into those bands as heavy breakeven supply walls requiring Domestic USD Spot CVD absorption before chasing."
  CB_05_OPSEC_72H_CUSTODY_WALL: "All Sleeve B tranches acquired on regulated domestic USD spot gateways must obey MOD 32 M6 (no mobile-only multi-sig signing while traveling) and the 72-Hour Operational Wall into 2-of-3 Malaysia/Indonesia cold storage."

# RISK & SIZING CONSTANTS
risk_parameters:
  sleeve_a_swing_max_risk_pct: 0.75 # 0.375% Amber / 0.00% Red
  sleeve_b_tranche_schedule: "3 to 4 pre-allocated reserve tranches across Tier 2 -> Tier 5 floor bands"
  leverage_permitted: 1.0 # Strict Unleveraged Spot Only
```

---

#### 2. Protective Circuit Breakers (Mandatory On-Chain & Barbell Guardrails)

*   **Circuit Breaker 1 — The Cohort Aging-Up Illusion (`CB-01`):** Every day, coins that have not moved for `155 days` graduate from STH (`MOD 13`) into LTH (`MOD 59`). Following a cycle peak, top-buyers who refuse to sell automatically cross the 155-day threshold, causing **LTH Realized Price to climb mechanically** and **LTH-MVRV to fall** even while price is flat or falling. Never mistake aging-induced LTH cost-basis drift for fresh institutional inflows; always cross-check `MOD 15` 30-Day Realized Cap Impulse and `MOD 07` Domestic USD Spot CVD.
*   **Circuit Breaker 2 — Sleeve A Tactical Cash-Lock Supremacy (`CB-02`):** On-chain valuation models operate on multi-month horizons and cannot prevent `-15%` to `-30%` macro liquidation cascades (`MOD 03` / `MOD 23` / `MOD 44`). Even when Spot trades below the True Market Mean (`~$77.5k–$78k`), **Sleeve A** (`<= 0.75%` risk tactical swing book) remains strictly locked in `100% CASH` whenever Pillar 1 is `GATE_RED` or `MOD 44`/`MOD 58` locks are active.
*   **Circuit Breaker 3 — ETF Primary-Flow Stabilization Gate (`CB-03`):** In the institutional ETF era, catching a falling knife into a secular cost-basis band while Authorized Participants are still executing daily primary redemptions (`MOD 38`) exposes Sleeve B capital to unnecessary drawdown. Require `>= 3` consecutive sessions of halted US Spot ETF net outflows (`>= $0M`) before releasing a Sleeve B reserve tranche.
*   **Circuit Breaker 4 — Trapped Veteran Breakeven Supply Walls (`CB-04`):** Coins acquired `6` to `24` months prior to a drawdown (e.g., the `$88,000` `6–12m` cohort and `$100,000` `1–2y` cohort cost bases) act as structural overhead supply ceilings. Require confirmed `MOD 54` `4H/1D` Break of Structure + positive Coinbase Premium (`MOD 19`) to clear each vintage shelf.
*   **Circuit Breaker 5 — Dual-Jurisdiction Multi-Sig OpSec (`CB-05`):** Every Sleeve B tranche is strictly air-gapped from Sleeve A (`MOD 46 CB-04`). Execute spot purchases exclusively via regulated domestic fiat gateways, settle UTXOs cleanly, and sweep into `2-of-3` Malaysia/Indonesia hardware multi-sig cold storage only from a verified desktop quorum (`MOD 32`).

---

#### 3. Core Conditional Signal Units (Condition A -> Outcome B -> Rule C)

##### CSU-59A: True Market Mean Loss & Mid-Cycle Value Compression (`Realized Price < Spot < True Market Mean`)
*   **Trigger Condition A (The Telemetry Scan):**
    1. Spot price breaks below both **STH Realized Price (`MOD 13`)** and the **True Market Mean / Active Investor Realized Price (`~$77,500–$78,000`)**, while remaining above **Aggregate Realized Price (`~$53,000–$55,000`)**.
    2. `MVRV Z-Score` compresses into `0.00 to 0.75`, `LTH-MVRV` sits between `1.10 and 1.60`, and `Entity-Adjusted NUPL` compresses into the `0.00–0.25` Hope/Fear band.
*   **Observed Outcome B (The Mechanical Trajectory):**
    *   **Sovereign Macro Lens:** Active cycle capital is underwater on average, stripping out speculative froth and compressing market value toward long-term network cost basis—mirroring Q4 2026's drawdown into the `$64,000` Epoch 4 halving anchor (`MOD 46`).
    *   **Probable Trajectory:** Multi-week range compression and liquidity testing between the `$64k` halving anchor / True Market Mean ceiling and Aggregate Realized Price / `200W SMA` support until macro/calendar drains clear.
*   **Execution Rule C (The Non-Negotiable Action):**
    *   **Sleeve A (Tactical Swing):** **ENFORCE `100% CASH LOCK` (`0.00%` Risk)** while `Pillar 1 == GATE_RED` or `MOD 44` calendar drains remain active (`CB-02`).
    *   **Sleeve B (Sovereign Vault):** Arm **Tranche 1 Reserve Watch** at the `$64,000` Block `840,000` anchor (`CSU-46A`), holding execution until `CB-03` (ETF outflows halt) and `MOD 33 REGIME_5` confirm.

##### CSU-59B: Generational Secular Floor & LTH Underwater Capitulation (`LTH-MVRV <= 1.00` / `MVRV Z-Score <= 0.00`)
*   **Trigger Condition A (The Telemetry Scan):**
    1. Spot price touches or sweeps **Aggregate Realized Price (`~$53,000–$55,000`)**, **LTH Realized Price (`LTH-MVRV <= 1.00`)**, or the **200-Week SMA (`MOD 17 M7`)**.
    2. `MVRV Z-Score <= 0.00` and `Entity-Adjusted NUPL < 0.00` (Capitulation Red zone), while LTH Realized Loss spikes and subsequently decelerates (`> 70%` drop from peak loss velocity).
    3. **Authentication (`CB-03`):** US Spot ETF 3-day net outflows halt (`>= $0M`) and `100–10,000 BTC` shark/whale cohorts resume net accumulation (`MOD 15C`).
*   **Observed Outcome B (The Mechanical Trajectory):**
    *   **Sovereign Macro Lens:** Even veteran holders (`>= 155 days`) are underwater in aggregate, marking maximum historical cyclical undervaluation ahead of **Block `1,050,000` (April 2028)** (`MOD 46`).
    *   **Probable Trajectory:** Generational multi-year asymmetric bottoming zone (`77.6%–84.2%` cyclical drawdown trough equivalence per `MOD 56`).
*   **Execution Rule C (The Non-Negotiable Action):**
    *   **Sleeve B (Sovereign Vault):** **DEPLOY TIER-2 & TIER-3 SOVEREIGN COLD-STORAGE TRANCHES (`MOD 18 CSU-18D`)** via Domestic USD Spot gateways and sweep into `2-of-3` multi-sig cold storage (`CB-05`).
    *   **Sleeve A (Tactical Swing):** Authorize `0.375%` Amber (or `0.75%` Green) spot swing entries upon verified `MOD 11` / `MOD 54` `4H/1D` VAH reclaim (`MOD 37 Net R >= 3.0`).

##### CSU-59C: Veteran LTH Distribution & Overhead Cohort Supply Wall (`LTH-MVRV >= 2.80` / `NUPL >= 0.70`)
*   **Trigger Condition A (The Telemetry Scan):**
    1. `LTH-MVRV` expands above **`2.80–3.50`**, `MVRV Z-Score` reaches **`>= 3.00–4.50`**, and `Entity-Adjusted NUPL` enters **`>= 0.70` (Euphoria/Greed)**—OR Spot rallies directly into an underwater `6m–2y` cohort cost-basis shelf (`CB-04`).
    2. Veteran LTH supply drops at `>= 90th` percentile velocity (`MOD 15B`) while Domestic USD Spot CVD diverges negatively (`MOD 05C`).
*   **Observed Outcome B (The Mechanical Trajectory):**
    *   **Sovereign Macro Lens:** Veteran holders are systematically transferring coins into late-cycle retail FOMO, saturating marginal fiat demand.
    *   **Probable Trajectory:** Multi-week distribution top or sharp `-20%` to `-40%` cyclical mean reversion.
*   **Execution Rule C (The Non-Negotiable Action):**
    *   **Action:** **BLOCK NEW SWING BREAKOUT ENTRIES; TRIGGER `MOD 41` LADDERED HARVEST (`4 x 5%`)** on designated cycle-peak tranches and tighten Sleeve A trailing stops to `1D VAL`.

##### CSU-59D: Post-Capitulation Cost-Basis Convergence & True Market Mean Reclaim
*   **Trigger Condition A (The Telemetry Scan):**
    1. Following a `CSU-59A` or `CSU-59B` bear base, STH Realized Price, LTH Realized Price, and Aggregate Realized Price converge tightly, and Spot reclaims both **STH Realized Price** and the **True Market Mean** across `>= 3` consecutive daily closes.
    2. Supported by `Pillar 1 == GATE_GREEN` (`MOD 16A` / `MOD 22`) and positive US Spot ETF net inflows (`MOD 38`).
*   **Observed Outcome B (The Mechanical Trajectory):**
    *   **Sovereign Macro Lens:** All active and short-term cohorts are back in net unrealized profit, eliminating overhead breakeven supply and restoring bull-market reflexivity.
    *   **Probable Trajectory:** Transition into `MOD 33 REGIME_1` (Secular Liquidity Expansion) toward Block `1,050,000` (`MOD 46`).
*   **Execution Rule C (The Non-Negotiable Action):**
    *   **Action:** **UPGRADE SLEEVE A TO FULL `0.75%` RISK AUTHORIZATION (`MOD 18A`)** on `200D MA` / True Market Mean pullback retests; halt new Sleeve B deep-value reserve deployments and shift Sleeve B strictly to custody hold until the `April–October 2029` harvest window (`MOD 46`).

---

#### 4. Dynamic Regime Mutation Lookup Matrix (M1 through M6)

| Mutation ID | Initial State | Telemetry Mutation Observed (Condition A') | Mechanical Meaning (Outcome B') | Mandatory Execution Override (Rule C') |
| :--- | :--- | :--- | :--- | :--- |
| **M1: Cohort Aging-Up False Bottom** | `CSU-59A` (Bear Chop) | `LTH-MVRV` drops toward `1.10` solely because `6m`-old top-buyers aged past `155` days, **while `30D` Realized Cap (`MOD 15`) is still falling and ETFs bleed**. | Statistical aging artifact (`CB-01`), not true capitulation exhaustion. | **Hold Sleeve B Reserve Tranches in Cash;** wait for `30D` Realized Cap to flatten and ETF outflows to stop (`CB-03`). |
| **M2: True Market Mean Rejection Trap** | Bear Relief Rally | Spot rallies from `$64k` up to kiss the **True Market Mean (`~$77.5k–$78k`)** from below, prints heavy ask absorption (`MOD 06`), and USD Spot CVD turns negative. | Active investors who were trapped underwater exited at breakeven (`MOD 13 M2`). | **Enforce Sleeve A `100% CASH LOCK`:** Exit any tactical bounce immediately at the True Market Mean ceiling. |
| **M3: Sub-Realized-Price Flash Capitulation** | `CSU-59B` (Secular Floor) | Macro shock (`MOD 23` / `MOD 29`) drives Spot `10%–20%` *below* Aggregate Realized Price (`MVRV Z-Score < -0.50`) on extreme forced liquidations (`MOD 51`). | Rare generational dislocation where total market cap trades below aggregate on-chain cost basis. | **Accelerate Final Sleeve B Reserve Tranche (`MOD 46 M4`)** once `4H` liquidations decay `< 25%` of peak (`MOD 34D`). |
| **M4: US Spot ETF Cost-Basis Flip** | Bull / Mid-Cycle | Spot closes below the aggregate **US Spot ETF Cost Basis (`~$81,500`)** for `3+` days alongside accelerating primary redemptions (`MOD 38`). | Institutional ETF cohort flips underwater, removing the primary passive spot bid. | **Downgrade Pillar 5 Valuation Bias to Defensive;** block breakout longs until ETF Cost Basis is reclaimed. |
| **M5: Diminishing Z-Score Cycle Top** | `CSU-59C` (Bull Expansion) | `MVRV Z-Score` reaches `3.2–4.0` (below 2017's `7.0+`), **but `LTH` distribution (`MOD 15B`) and `MOD 41` `+4%` flat double-top fire simultaneously**. | Larger institutional market cap compressed peak Z-score amplitude (`MOD 56 CB-03`). | **Do Not Wait for `Z-Score = 7.0`:** Execute `MOD 41` laddered exits immediately upon `Rule 1` / `Rule 3` triggers. |
| **M6: Sovereign Reserve OpSec Quarantine** | `CSU-59B` Triggered | Operator is traveling with mobile-only access (`Samsung Galaxy A55`) when a generational floor signal triggers. | High operational risk for multi-sig UTXO hardware signing (`CB-05` / `MOD 32 M6`). | Execute spot purchase on regulated USD exchange only; **enforce `72-Hour Operational Wall`** before multi-sig cold-storage sweep.
