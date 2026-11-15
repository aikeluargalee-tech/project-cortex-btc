# AGENTS.md — Project CoreTex BTC Brain

Before modifying files or proposing architectural changes in `aikeluargalee-tech/project-cortex-btc`, read:
1. [`GOVERNANCE.md`](GOVERNANCE.md) — Three-tier separation of powers (`rulebook/` logic vs. `cortex_matrix_engine.py` compiler vs. telemetry bridges), New-MOD integration paths, and non-negotiable audit invariants.
2. [`SKILL.md`](SKILL.md) — Live operational runbook, `MOD 31`/`MOD 36` fail-closed telemetry rules, `0.75%` 1.0x Spot risk cap, and permanent VPIN exclusion.

## Repo-Specific Guardrails
- **Keep Skill Mirrors Identical:** Any update to `SKILL.md` must be copied identically to `.hermes/skills/project-cortex-btc/SKILL.md`.
- **Keep Entrypoints & Cron Paths Intact:** Do not rename Python scripts (`btc_data_fetcher.py`, `cortex_schema_adapter.py`, `cortex_matrix_engine.py`, `telegram_cortex_alert.py`), repo slug, or `.github/workflows/btc_fetcher_cron.yml` paths unless explicitly instructed.
- **Documentation / Rulebook Sync Commits:** Do not commit `.zip` archives into Git; verify Markdown links and TOC anchors, and append `[skip ci]` to commit messages for pure `rulebook/` and documentation updates.
