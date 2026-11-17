#!/usr/bin/env python3
"""
CORTEX-BTC — Versioned Configuration Loader & Governance Store.

Enforces non-negotiable spot-only / human-execution invariants, preserves
all undefined strategy parameters as 'NOT CONFIGURED', keeps strategy
validation status 'UNVALIDATED' unless formally promoted, and versions
every configuration change with operator, reason, and UTC timestamp.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from cortex_core.audit import AuditLogger
from cortex_core.constants import NOT_CONFIGURED, UNVALIDATED, OperatingMode
from cortex_core.models import ConfigurationRecord
from cortex_core.time_utils import ensure_utc_iso, utc_now

DEFAULT_CONFIG_PATH = Path("data/cortex_config.json")
DEFAULT_CONFIG_HISTORY_PATH = Path("data/cortex_config_history.jsonl")

# Non-negotiable system-level invariants (cannot be mutated via config updates)
IMMUTABLE_INVARIANTS: dict[str, Any] = {
    "instrument": "BTC/USDT",
    "spot_only": True,
    "leverage_allowed": False,
    "margin_allowed": False,
    "futures_execution_allowed": False,
    "short_selling_allowed": False,
    "autonomous_execution": False,
    "private_exchange_keys_allowed": False,
}


class ConfigValidationError(ValueError):
    """Raised when a configuration update violates CORTEX-BTC governance rules."""


def build_default_parameters() -> dict[str, Any]:
    """
    Build explicit initial parameter tree with unestablished thresholds marked
    NOT CONFIGURED (never silently invented).
    """
    return {
        "invariants": copy.deepcopy(IMMUTABLE_INVARIANTS),
        "portfolio_policy": {
            "active_tactical_sleeve_pct": NOT_CONFIGURED,
            "protected_core_btc_min": NOT_CONFIGURED,
            "min_btc_inventory_floor": NOT_CONFIGURED,
            "min_usdt_inventory_floor": NOT_CONFIGURED,
            "max_transaction_size_usdt": NOT_CONFIGURED,
            "max_transaction_size_btc": NOT_CONFIGURED,
            "portfolio_risk_budget_pct": NOT_CONFIGURED,
        },
        "exposure_bands": {
            "defensive": {"btc_pct": NOT_CONFIGURED, "usdt_pct": NOT_CONFIGURED},
            "cautious": {"btc_pct": NOT_CONFIGURED, "usdt_pct": NOT_CONFIGURED},
            "neutral": {"btc_pct": NOT_CONFIGURED, "usdt_pct": NOT_CONFIGURED},
            "constructive": {"btc_pct": NOT_CONFIGURED, "usdt_pct": NOT_CONFIGURED},
            "strongly_constructive": {"btc_pct": NOT_CONFIGURED, "usdt_pct": NOT_CONFIGURED},
        },
        "data_policy": {
            "spot_price_max_age_minutes": NOT_CONFIGURED,
            "spot_cvd_max_age_minutes": NOT_CONFIGURED,
            "order_book_max_age_minutes": NOT_CONFIGURED,
            "derivatives_context_max_age_minutes": NOT_CONFIGURED,
            "macro_context_max_age_days": NOT_CONFIGURED,
            "min_venue_quorum": NOT_CONFIGURED,
            "max_venue_dispersion_bps": NOT_CONFIGURED,
            "mandatory_feeds": ["binance_spot_price", "spot_ohlcv"],
            "missing_derivatives_blocks_decision": False,
            "missing_macro_blocks_decision": False,
            "stale_spot_cvd_blocks_decision": True,
        },
        "market_regime_rules": {
            "constructive": NOT_CONFIGURED,
            "cautious": NOT_CONFIGURED,
            "defensive": NOT_CONFIGURED,
            "dislocation_extreme_risk": NOT_CONFIGURED,
        },
        "buy_criteria": {
            "min_confirmations": NOT_CONFIGURED,
            "cvd_threshold_btc": NOT_CONFIGURED,
            "reclaim_rule": NOT_CONFIGURED,
            "max_stop_distance_pct": NOT_CONFIGURED,
        },
        "sell_criteria": {
            "profit_taking": NOT_CONFIGURED,
            "risk_reduction": NOT_CONFIGURED,
            "defensive_exit": NOT_CONFIGURED,
        },
        "execution_assumptions": {
            "default_order_type": "LIMIT",
            "order_expiry_minutes": NOT_CONFIGURED,
            "maker_fee_bps": NOT_CONFIGURED,
            "taker_fee_bps": NOT_CONFIGURED,
            "expected_slippage_bps": NOT_CONFIGURED,
        },
    }


def _assert_invariants_intact(params: dict[str, Any]) -> None:
    invariants = params.get("invariants")
    if not isinstance(invariants, dict):
        raise ConfigValidationError("Missing 'invariants' configuration block.")
    for key, expected in IMMUTABLE_INVARIANTS.items():
        if invariants.get(key) != expected:
            raise ConfigValidationError(
                f"Non-negotiable invariant '{key}' must remain {expected!r}; got {invariants.get(key)!r}."
            )


def _deep_merge_updates(
    base: dict[str, Any],
    updates: dict[str, Any],
    *,
    prefix: str = "",
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """
    Merge nested updates into a copy of base, returning:
      (merged, previous_leaf_values, new_leaf_values)
    """
    merged = copy.deepcopy(base)
    prev_leaves: dict[str, Any] = {}
    new_leaves: dict[str, Any] = {}

    for key, val in updates.items():
        dotted = f"{prefix}.{key}" if prefix else key
        if key == "invariants" and not prefix:
            if not isinstance(val, dict):
                raise ConfigValidationError("Invalid 'invariants' update.")
            for ikey, ival in val.items():
                if ikey in IMMUTABLE_INVARIANTS and ival != IMMUTABLE_INVARIANTS[ikey]:
                    raise ConfigValidationError(
                        f"Cannot override non-negotiable invariant 'invariants.{ikey}'."
                    )
            continue

        if isinstance(val, dict) and isinstance(merged.get(key), dict):
            sub_merged, sub_prev, sub_new = _deep_merge_updates(merged[key], val, prefix=dotted)
            merged[key] = sub_merged
            prev_leaves.update(sub_prev)
            new_leaves.update(sub_new)
        else:
            old_val = merged.get(key, NOT_CONFIGURED)
            if old_val != val:
                prev_leaves[dotted] = old_val
                new_leaves[dotted] = val
            merged[key] = copy.deepcopy(val)

    return merged, prev_leaves, new_leaves


def initialize_default_config(
    config_path: Path = DEFAULT_CONFIG_PATH,
    history_path: Path = DEFAULT_CONFIG_HISTORY_PATH,
    *,
    operator_id: str = "SYSTEM_INIT",
    now_utc: str | None = None,
    audit_logger: AuditLogger | None = None,
) -> ConfigurationRecord:
    """Create initial version 1 ConfigurationRecord if none exists on disk."""
    config_path = Path(config_path)
    history_path = Path(history_path)
    if config_path.exists():
        return load_config(config_path)

    ts_iso = ensure_utc_iso(now_utc or utc_now(), field_name="changed_at_utc")
    params = build_default_parameters()
    record = ConfigurationRecord(
        config_version=1,
        operating_mode=OperatingMode.RESEARCH,
        validation_status=UNVALIDATED,
        instrument="BTC/USDT",
        spot_only=True,
        autonomous_execution=False,
        parameters=params,
        previous_values={},
        new_values={"initialized": "version_1_unconfigured_defaults"},
        operator_id=operator_id,
        change_reason="Initial CORTEX-BTC configuration record (all unestablished parameters marked NOT CONFIGURED).",
        operator_acknowledged=True,
        changed_at_utc=ts_iso,
    )
    _write_config_and_history(record, config_path, history_path)
    if audit_logger is not None:
        audit_logger.record(
            "CONFIG_INITIALIZED",
            actor=operator_id,
            summary="Initialized CORTEX-BTC configuration v1 (UNVALIDATED / NOT CONFIGURED defaults).",
            details={"config_version": 1, "changed_at_utc": ts_iso},
            timestamp_utc=ts_iso,
        )
    return record


def _write_config_and_history(
    record: ConfigurationRecord,
    config_path: Path,
    history_path: Path,
) -> None:
    config_path.parent.mkdir(parents=True, exist_ok=True)
    history_path.parent.mkdir(parents=True, exist_ok=True)
    payload = record.to_dict()
    tmp_path = config_path.with_suffix(".json.tmp")
    tmp_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    tmp_path.replace(config_path)
    with history_path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(payload, sort_keys=True) + "\n")


def load_config(config_path: Path = DEFAULT_CONFIG_PATH) -> ConfigurationRecord:
    """Load ConfigurationRecord from JSON without mutating or inventing missing defaults."""
    config_path = Path(config_path)
    if not config_path.exists():
        raise FileNotFoundError(
            f"Configuration file not found at {config_path}. Call initialize_default_config() explicitly."
        )
    raw = json.loads(config_path.read_text(encoding="utf-8"))
    record = ConfigurationRecord.from_dict(raw)
    _assert_invariants_intact(record.parameters)
    if not record.spot_only or record.autonomous_execution:
        raise ConfigValidationError("Stored configuration violates spot-only or manual-execution invariant.")
    return record


def update_config(
    updates: dict[str, Any],
    *,
    operator_id: str,
    change_reason: str,
    operator_acknowledged: bool = True,
    operating_mode: OperatingMode | None = None,
    config_path: Path = DEFAULT_CONFIG_PATH,
    history_path: Path = DEFAULT_CONFIG_HISTORY_PATH,
    now_utc: str | None = None,
    audit_logger: AuditLogger | None = None,
) -> ConfigurationRecord:
    """
    Apply an audited, versioned update to CORTEX-BTC configuration.
    Rejects empty operator/reason, unacknowledged edits, or invariant violations.
    """
    if not operator_id or not operator_id.strip():
        raise ConfigValidationError("operator_id is required for configuration changes.")
    if not change_reason or not change_reason.strip():
        raise ConfigValidationError("change_reason is required for configuration changes.")
    if not operator_acknowledged:
        raise ConfigValidationError("operator_acknowledged must be True to apply configuration changes.")

    current = load_config(config_path)
    merged_params, prev_leaves, new_leaves = _deep_merge_updates(current.parameters, updates)
    _assert_invariants_intact(merged_params)

    next_mode = operating_mode or current.operating_mode
    if next_mode != current.operating_mode:
        prev_leaves["operating_mode"] = current.operating_mode.value
        new_leaves["operating_mode"] = next_mode.value

    if not new_leaves:
        raise ConfigValidationError("No configuration values changed.")

    ts_iso = ensure_utc_iso(now_utc or utc_now(), field_name="changed_at_utc")
    next_record = ConfigurationRecord(
        config_version=current.config_version + 1,
        operating_mode=next_mode,
        validation_status=current.validation_status,
        instrument="BTC/USDT",
        spot_only=True,
        autonomous_execution=False,
        parameters=merged_params,
        previous_values=prev_leaves,
        new_values=new_leaves,
        operator_id=operator_id.strip(),
        change_reason=change_reason.strip(),
        operator_acknowledged=True,
        changed_at_utc=ts_iso,
    )
    _write_config_and_history(next_record, Path(config_path), Path(history_path))
    if audit_logger is not None:
        audit_logger.record(
            "CONFIG_UPDATED",
            actor=operator_id.strip(),
            summary=f"Config updated v{current.config_version} -> v{next_record.config_version}: {change_reason.strip()}",
            details={
                "previous_version": current.config_version,
                "new_version": next_record.config_version,
                "previous_values": prev_leaves,
                "new_values": new_leaves,
            },
            timestamp_utc=ts_iso,
        )
    return next_record


def read_config_history(history_path: Path = DEFAULT_CONFIG_HISTORY_PATH) -> list[dict[str, Any]]:
    """Return all recorded ConfigurationRecord versions in chronological order."""
    history_path = Path(history_path)
    if not history_path.exists():
        return []
    entries: list[dict[str, Any]] = []
    with history_path.open("r", encoding="utf-8") as fh:
        for line in fh:
            text = line.strip()
            if text:
                entries.append(json.loads(text))
    return entries


def get_param(config: ConfigurationRecord, dotted_path: str, default: Any = NOT_CONFIGURED) -> Any:
    """Safely read a nested parameter from ConfigurationRecord."""
    cur: Any = config.parameters
    for part in dotted_path.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return default
    return cur
