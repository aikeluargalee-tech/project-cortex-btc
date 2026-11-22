##### PROJECT CORTEX-BTC — MODULE 68.1: EMPIRICAL REGIME × FUNDING × OI DECISION MATRIX (299-WEEK STATE GRID)
**Waterfall Tier:** Pillar 3 & Tier D Operational Lookup Sub-Module (Child Empirical Table to **MOD 68: Derivatives Positioning Context, Tail-Only Funding Mechanics & Empirical Sample Hygiene**) — harmonized with **MOD 01** (Rising OI + Negative Basis), **MOD 02** (Crowded Positive Basis), **MOD 04** (Funding Velocity & Divergence), **MOD 17** (200D MA Secular Divider), **MOD 34** (AEGIS-3 Anti-Capitulation Sell-Freeze), **MOD 52** (`CB-05` Empirical Sample Hygiene), **MOD 57** (`M4` Below-200D Drift), **MOD 60** (7-Rank Veto Precedence), and **MOD 62** (DIBSE v2.0).
**Document & Code Provenance:**
* `btc-cortex`: `tools/state_matrix.py` + `data/state_matrix.md` (commit `c3c327a`)
* `btc-library`: `articles/positioning-decision-matrix.md` + `.pdf` (commit `c727d7e`)
**Governance Posture:** Read-Only Empirical Lookup Grid (**Zero standalone trade authorization**). Measures all 8 combinations of `200D SMA Regime × Funding Sign × Open Interest Direction` across **299 non-overlapping weeks (`2021-01-08` → `2026-09-30`)** so every state must earn its sample count before influencing decision aggression.

--------------------------------------------------------------------------------

###### 0. Machine-Readable State & Routing Block (Python / Hermes / NotebookLM Index)
```yaml
module_id: "MOD_68.1"
parent_module: "MOD_68"
entry_type: "EMPIRICAL_REGIME_POSITIONING_LOOKUP_GRID"
waterfall_pillar: "PILLAR_3_AND_TIER_D_POSITIONING_LOOKUP"
title: "Empirical Regime x Funding x OI Decision Matrix (299-Week State Grid)"

# CODE & LIBRARY PROVENANCE
provenance:
  code_repo: "btc-cortex"
  code_files: ["tools/state_matrix.py", "data/state_matrix.md"]
  code_commit: "c3c327a"
  library_repo: "btc-library"
  library_files: ["articles/positioning-decision-matrix.md", "articles/positioning-decision-matrix.pdf"]
  library_commit: "c727d7e"
  sample_window: "2021-01-08 to 2026-09-30"
  sample_observations_non_overlapping_weeks: 299
  oi_unit_in_state_matrix_py: "UNVERIFIED_PENDING_CODE_AUDIT" # Must confirm BTC contracts vs USD notional per MOD 68 CB-02

# MOD 60 PRECEDENCE & EXECUTION BOUNDARY
governance_registration:
  mod_60_precedence_rank: "PILLAR_3_CONTEXT_LOOKUP_SUBMODULE_TO_MOD_68"
  standalone_trade_authorization: false # No cell in this matrix authorizes a trade
  upstream_veto_subordination: "NEVER overrides MOD 60 Ranks 0-3 (DATA HALT, GATE_RED, ICDM >= 60, MOD 44/58 Lock, or Active Cascade)."

# KEY STRUCTURAL LAWS EXTRACTED FROM 299-WEEK GRID
structural_laws:
  bull_regime_crowded_shorts_count: 0 # 0/299 weeks above 200D SMA (structural fact, not missing data)
  above_200d_edge_status: "COIN_FLIP_BASE_RATE" # 49%-51% hit rate across all populated cells above 200D SMA
  below_200d_crowded_shorts: {n: 18, mean_7d_pct: 3.05, median_7d_pct: 3.55, hit_rate_pct: 72.0, ci_95_pct: [50, 87], mean_14d_pct: 3.03}
  binary_positive_funding_caveat: "Crowded longs (n=92 above / n=64 below) uses binary funding > 0% (88% of weeks are positive); does NOT invalidate MOD 02 / MOD 68 CSU-68C extreme upper-tail (>= +0.035%/8h) blow-off guards."

# V2 RESEARCH BACKLOG (FOR tools/state_matrix.py UPGRADES)
v2_research_backlog:
  - "Verify and lock OI_DELTA calculation strictly to BTC contracts (sum_open_interest), never USD notional"
  - "Add Axis 4: Futures-vs-Spot Basis to separate directional crowding from delta-neutral carry"
  - "Compute per-cell regime-matched excess returns (cell return minus unconditional >200D or <200D baseline)"
  - "Split positive funding into neutral clamp plateau (0% to +0.03%/day) vs symmetric top 5%-10% upper tail"
  - "Expand sample window past 2026-09-30 as new non-overlapping weeks close"
```

--------------------------------------------------------------------------------

###### 1. The 8-Cell Empirical Decision Matrix (`2021-01-08` → `2026-09-30`, `N = 299` Non-Overlapping Weeks)
| Regime (`200D SMA`) | Leverage State | `n` | Mean 7d | Median 7d | Hit Rate | Mean 14d | CoreTex Reading |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Above 200D** | Crowded shorts (`F < 0`, `OI ↑`) | **0** | — | — | — | — | **Never occurred** in 299 weeks (structural fact) |
| **Above 200D** | Positions leaving (`F < 0`, `OI ↓`) | **4** | `+4.23%` | `+0.08%` | `50%` | `+7.34%` | Colour only (insufficient `n`) |
| **Above 200D** | Crowded longs (`F > 0`, `OI ↑`) | **92** | `+0.50%` | `−0.32%` | `49%` | `+1.64%` | **No edge** (binary `> 0%` sign; base-rate chop) |
| **Above 200D** | Quiet deleveraging (`F > 0`, `OI ↓`) | **70** | `+0.71%` | `+0.61%` | `51%` | `+0.73%` | **No edge** (base-rate drift) |
| **Below 200D** | **Crowded shorts (`F < 0`, `OI ↑`)** | **18** | **`+3.05%`** | **`+3.55%`** | **`72%`** | **`+3.03%`** | **Directional colour only** (95% CI `50%–87%`; cannot size) |
| **Below 200D** | Positions leaving (`F < 0`, `OI ↓`) | **14** | `+1.10%` | `−0.06%` | `50%` | `+2.21%` | Colour only (empty room; no forced buyers) |
| **Below 200D** | Crowded longs (`F > 0`, `OI ↑`) | **64** | `+0.07%` | `+0.08%` | `52%` | `+1.00%` | **No edge** (binary `> 0%` sign) |
| **Below 200D** | Quiet deleveraging (`F > 0`, `OI ↓`) | **37** | `−0.62%` | `−0.02%` | `49%` | `−1.02%` | **No edge** (bear drift) |

*Note on Sample & Horizon:* Non-overlapping weekly forward returns eliminate the daily 7-day overlap distortion (`MOD 52 CB-05`). Weekly aggregates differ from intraday/48h–72h funding dips tracked in `MOD 01` and `MOD 04`.

--------------------------------------------------------------------------------

###### 2. Core Structural Findings & Spot-Only Operational Rules
1. **The Weekly Signal Lives Exclusively Below the 200-Day SMA:** Every populated cell above the 200-day moving average prints a `49%–51%` coin flip. Directional separation in weekly leverage states appears only inside bear regimes (`< 200D SMA`), reinforcing `MOD 17` and `MOD 57 M4`.
2. **Weekly "Crowded Shorts" Never Occurs in an Uptrend (`0 / 299` Weeks):** Zero occurrences above the 200D SMA is a structural market fact, not a data gap. Waiting for a full-week negative funding squeeze during a secular bull market waits indefinitely—bull-regime disbelief rallies (`MOD 04 CSU-04A`) occur via short-window (`48h–72h`) funding compression (`<= +0.003%/8h`), not week-long negative averages.
3. **Binary-Sign (`> 0%`) vs. Extreme Upper-Tail Clarification (`MOD 02` Harmonization):** In this grid, `Crowded longs` (`n = 92 + 64 = 156`) and `Quiet deleveraging` (`n = 70 + 37 = 107`) account for **263 of 299 weeks (`88%` of history)** because funding is split at `0.00%` rather than above Binance's `+0.01%/8h` clamp. Therefore, the `"no edge"` verdict on binary `Crowded longs` does **not** override or invalidate `MOD 02` / `MOD 68 CSU-68C` extreme upper-tail fragility gates (`>= 90th–95th` percentile / `>= +0.035%/8h` paired with negative Domestic USD Spot CVD).
4. **Tightened 1.0x Spot-Only Actionable Doctrine (`Below 200D + Crowded Shorts`, `n = 18`):**
   * Because a `72%` hit rate on `n = 18` carries a wide 95% confidence interval (`50%–87%`), the historical record leans upward—**enough to argue against panic-selling spot or executing Loop B (`BTC -> USDT`) distribution into a fresh bear-market low** (harmonizing with `MOD 34` AEGIS-3 anti-capitulation sell-freeze), **but NOT enough to authorize or size a Loop A (`USDT -> BTC`) spot buy** without independent Pillar 1/2/4 confirmation (`MOD 60`, `MOD 05` Domestic USD Spot CVD, `MOD 11` reclaim, `MOD 62` Rule 15).

--------------------------------------------------------------------------------

###### 3. Mandatory 4-Step Operational Read Sequence
Evaluate the positioning grid strictly in descending order—never skip Step 1 or Step 4:
```text
1. REGIME      Is spot above or below the 200-day SMA? (MOD 17)
2. FUNDING     Which side is paying over the realized weekly window? (MOD 68 CB-03)
3. OPEN INT.   Is BTC-denominated OI rising (crowd growing) or falling (crowd leaving)? (MOD 68 CB-02)
4. CELL COUNT  Does the cell have a valid count & separation, or is it base-rate / colour only?
```
* **Hard Rule:** Only a cell with an audited count may adjust aggression (and strictly to *reduce* premature risk-taking or prevent capitulation selling). **No cell in this matrix authorizes a trade.**

--------------------------------------------------------------------------------

###### 4. Planned v2 Upgrade Backlog (`tools/state_matrix.py`)
1. **OI Unit Verification (`MOD 68 CB-02`):** Audit `tools/state_matrix.py` (`c3c327a`) to confirm weekly OI change is measured in **BTC contracts (`sum_open_interest`)**, not USD notional.
2. **Axis 4 — Futures-vs-Spot Basis:** Cross basis against funding to separate directional speculation from delta-neutral cash-and-carry arbitrage (`MOD 02 CSU-02C` / `MOD 68 M5`).
3. **Regime-Matched Baseline Controls:** Report each cell's excess return relative to the unconditional `> 200D` or `< 200D` weekly mean so bull-market drift does not flatter cells above the 200D SMA.
4. **Symmetric Upper-Tail Funding Buckets:** Split the `88%` positive-funding mass into the clamped baseline (`0%` to `+0.03%/day`) versus true `>= 90th / 95th` percentile upper tails (`MOD 68 CB-03`).

--------------------------------------------------------------------------------

###### FINAL DIRECTIVE
**MOD 68.1 enforces empirical humility across all eight Regime × Funding × OI states: four populated cells show no edge, bull-regime crowded shorts have never occurred in 299 weeks, and the sole directional cell (`below 200D + Crowded shorts`, `n = 18`) serves strictly as an anti-capitulation patience cue—never a position-sizing trigger.**
