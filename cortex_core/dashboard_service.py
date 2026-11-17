"""
Dashboard Backend Service for CORTEX-BTC Unified Command Centre (Phase 5).

Coordinates ConfigurationRecord, MarketSnapshot, PortfolioLedger, Module A,
Module B, Module C, Module D, and AuditLogger into a single deterministic
service layer. Strictly manual execution only; never invents missing values.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from btc_config_loader import (
    DEFAULT_CONFIG_HISTORY_PATH,
    DEFAULT_CONFIG_PATH,
    initialize_default_config,
    load_config,
    read_config_history,
    update_config,
)
from cortex_core.audit import AuditLogger
from cortex_core.constants import (
    DATA_UNAVAILABLE,
    NOT_CONFIGURED,
    LoopType,
    OperatingMode,
    OrderStatus,
    PortfolioState,
)
from cortex_core.ledger import PortfolioLedger
from cortex_core.market_data import build_market_snapshot
from cortex_core.module_d import run_decision_cycle
from cortex_core.time_utils import format_myt, utc_now


class DashboardService:
    """Stateful service backing the CORTEX-BTC Unified Command Centre."""

    def __init__(
        self,
        *,
        metrics_path: Path = Path("btc_metrics_latest.json"),
        data_dir: Path = Path("data"),
    ) -> None:
        self.metrics_path = Path(metrics_path)
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.config_path = self.data_dir / DEFAULT_CONFIG_PATH.name
        self.history_path = self.data_dir / DEFAULT_CONFIG_HISTORY_PATH.name
        self.ledger_path = self.data_dir / "portfolio_ledger.json"
        self.audit_path = self.data_dir / "cortex_audit.jsonl"
        self.state_path = self.data_dir / "dashboard_state.json"

        self.audit_logger = AuditLogger(self.audit_path)
        self.ledger = PortfolioLedger(state_path=self.ledger_path, audit_logger=self.audit_logger)
        self.operating_state = self._load_operating_state()

    def _load_operating_state(self) -> PortfolioState:
        if self.state_path.exists():
            try:
                raw = json.loads(self.state_path.read_text(encoding="utf-8"))
                return PortfolioState(raw.get("operating_state", PortfolioState.USDT_100.value))
            except Exception:
                pass
        return PortfolioState.USDT_100

    def _save_operating_state(self, state: PortfolioState, decision_id: str | None = None) -> None:
        self.operating_state = state
        tmp = self.state_path.with_suffix(".json.tmp")
        tmp.write_text(
            json.dumps(
                {
                    "operating_state": state.value,
                    "last_decision_id": decision_id,
                    "updated_at_utc": utc_now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        tmp.replace(self.state_path)

    def get_config(self):
        if self.config_path.exists():
            return load_config(self.config_path)
        return initialize_default_config(
            self.config_path,
            self.history_path,
            audit_logger=self.audit_logger,
        )

    def load_raw_metrics(self) -> dict[str, Any]:
        if not self.metrics_path.exists():
            return {}
        try:
            data = json.loads(self.metrics_path.read_text(encoding="utf-8"))
            return data if isinstance(data, dict) else {}
        except Exception:
            return {}

    def get_command_centre_state(
        self,
        *,
        evidence_inputs_a: dict[str, Any] | None = None,
        evidence_inputs_b: dict[str, Any] | None = None,
        create_proposed_order: bool = False,
        now_utc: str | None = None,
    ) -> dict[str, Any]:
        """Compute complete Command Centre payload for the dashboard."""
        cfg = self.get_config()
        raw_metrics = self.load_raw_metrics()
        mkt = build_market_snapshot(raw_metrics, config=cfg, now_utc=now_utc)

        result = run_decision_cycle(
            market_snapshot=mkt,
            ledger=self.ledger,
            config=cfg,
            previous_operating_state=self.operating_state,
            evidence_inputs_a=evidence_inputs_a,
            evidence_inputs_b=evidence_inputs_b,
            create_proposed_order=create_proposed_order,
            audit_logger=self.audit_logger,
            now_utc=now_utc,
        )
        decision = result["decision"]
        self._save_operating_state(decision.new_operating_state, decision.decision_id)

        prt = result["portfolio"]
        prt_dict = prt.to_dict()
        # Surface explicit NOT CONFIGURED / DATA UNAVAILABLE strings for UI display
        prt_display = {
            "configured": prt.configured,
            "btc_total": prt.display_field("btc_total"),
            "btc_available": prt.display_field("btc_available"),
            "btc_reserved": prt.display_field("btc_reserved"),
            "btc_core_protected": prt.display_field("btc_core_protected"),
            "btc_tactical": prt.display_field("btc_tactical"),
            "btc_tactical_available": prt.display_field("btc_tactical_available"),
            "usdt_total": prt.display_field("usdt_total"),
            "usdt_available": prt.display_field("usdt_available"),
            "usdt_reserved": prt.display_field("usdt_reserved"),
            "usdt_tactical": prt.display_field("usdt_tactical"),
            "usdt_tactical_available": prt.display_field("usdt_tactical_available"),
            "total_portfolio_value_usdt": prt.display_field("total_portfolio_value_usdt"),
            "active_sleeve_value_usdt": prt.display_field("active_sleeve_value_usdt"),
            "protected_core_btc_value_usdt": prt.display_field("protected_core_btc_value_usdt"),
            "btc_exposure_pct": prt.display_field("btc_exposure_pct"),
            "usdt_exposure_pct": prt.display_field("usdt_exposure_pct"),
            "reconciliation_status": prt.reconciliation_status.value,
            "reconciliation_notes": prt.reconciliation_notes,
            "realised_usdt_pnl": prt.realised_usdt_pnl,
            "realised_delta_btc": prt.realised_delta_btc,
        }

        mkt_dict = mkt.to_dict()
        mkt_dict["source_event_ts_myt"] = format_myt(mkt.source_event_ts_utc)
        mkt_dict["retrieved_ts_myt"] = format_myt(mkt.retrieved_ts_utc)
        for fdict in mkt_dict["fields"].values():
            fdict["source_event_ts_myt"] = format_myt(fdict.get("source_event_ts_utc"))
            fdict["retrieved_ts_myt"] = format_myt(fdict.get("retrieved_ts_utc"))
            if fdict["value"] is None:
                fdict["display_value"] = DATA_UNAVAILABLE
            else:
                fdict["display_value"] = fdict["value"]

        orders_out = []
        for o in sorted(self.ledger.orders.values(), key=lambda x: x.created_at_utc, reverse=True):
            od = o.to_dict()
            od["created_at_myt"] = format_myt(o.created_at_utc)
            od["updated_at_myt"] = format_myt(o.updated_at_utc)
            orders_out.append(od)

        cycles_out = []
        for c in sorted(self.ledger.cycles.values(), key=lambda x: x.created_at_utc, reverse=True):
            cd = c.to_dict()
            cd["created_at_myt"] = format_myt(c.created_at_utc)
            cd["completed_at_myt"] = format_myt(c.completed_at_utc) if c.completed_at_utc else None
            cycles_out.append(cd)

        decision_dict = decision.to_dict()
        decision_dict["timestamp_myt"] = format_myt(decision.timestamp_utc)

        cfg_dict = cfg.to_dict()
        cfg_dict["changed_at_myt"] = format_myt(cfg.changed_at_utc)

        audit_events = list(reversed(self.audit_logger.read_events()))[:100]
        for ev in audit_events:
            ev["timestamp_myt"] = format_myt(ev.get("timestamp_utc"))

        return {
            "banner": {
                "system_name": "CORTEX-BTC",
                "instrument": "BTC/USDT SPOT ONLY",
                "execution_mode": "MANUAL OPERATOR EXECUTION ONLY",
                "operating_mode": cfg.operating_mode.value,
                "validation_status": cfg.validation_status,
                "spot_price_usdt": mkt.spot_price if mkt.spot_price is not None else DATA_UNAVAILABLE,
                "market_ts_utc": mkt.source_event_ts_utc or DATA_UNAVAILABLE,
                "market_ts_myt": format_myt(mkt.source_event_ts_utc),
                "last_update_utc": mkt.retrieved_ts_utc,
                "last_update_myt": format_myt(mkt.retrieved_ts_utc),
                "data_integrity": mkt.overall_integrity_status.value,
            },
            "decision": decision_dict,
            "module_a": result["module_a"].to_dict(),
            "module_b": result["module_b"].to_dict(),
            "allocation": result["allocation"].to_dict(),
            "portfolio": prt_dict,
            "portfolio_display": prt_display,
            "market_snapshot": mkt_dict,
            "orders": orders_out,
            "cycles": cycles_out,
            "config": cfg_dict,
            "config_history": list(reversed(read_config_history(self.history_path))),
            "audit_events": audit_events,
        }

    # ------------------------------------------------------------------
    # Operator Actions (Manual Execution & Configuration Controls)
    # ------------------------------------------------------------------

    def configure_balances(self, payload: dict[str, Any]) -> dict[str, Any]:
        snap = self.ledger.configure_balances(
            btc_core_protected=float(payload["btc_core_protected"]),
            btc_tactical=float(payload["btc_tactical"]),
            usdt_tactical=float(payload["usdt_tactical"]),
            usdt_core_protected=float(payload.get("usdt_core_protected", 0.0)),
            operator_id=str(payload["operator_id"]),
            reason=str(payload["reason"]),
        )
        return snap.to_dict()

    def reconcile_balances(self, payload: dict[str, Any]) -> dict[str, Any]:
        status = self.ledger.reconcile_balances(
            reported_btc_total=float(payload["reported_btc_total"]),
            reported_usdt_total=float(payload["reported_usdt_total"]),
            source=str(payload.get("source", "manual_operator")),
        )
        return {
            "reconciliation_status": status.value,
            "notes": self.ledger.reconciliation_notes,
        }

    def update_core_mandate(self, payload: dict[str, Any]) -> dict[str, Any]:
        snap = self.ledger.update_core_mandate(
            new_btc_core_protected=float(payload["new_btc_core_protected"]),
            new_btc_tactical=float(payload["new_btc_tactical"]),
            operator_id=str(payload["operator_id"]),
            reason=str(payload["reason"]),
            operator_acknowledged=bool(payload.get("operator_acknowledged", False)),
        )
        return snap.to_dict()

    def update_configuration(self, payload: dict[str, Any]) -> dict[str, Any]:
        self.get_config()
        mode_raw = payload.get("operating_mode")
        mode = OperatingMode(mode_raw) if mode_raw else None
        rec = update_config(
            dict(payload.get("updates") or {}),
            operator_id=str(payload["operator_id"]),
            change_reason=str(payload["change_reason"]),
            operator_acknowledged=bool(payload.get("operator_acknowledged", False)),
            operating_mode=mode,
            config_path=self.config_path,
            history_path=self.history_path,
            audit_logger=self.audit_logger,
        )
        return rec.to_dict()

    def open_cycle(self, payload: dict[str, Any]) -> dict[str, Any]:
        cyc = self.ledger.open_cycle(
            loop=LoopType(payload["loop"]),
            starting_qty=float(payload["starting_qty"]),
            original_setup_ref=str(payload.get("original_setup_ref", "MANUAL_SETUP")),
        )
        return cyc.to_dict()

    def handle_order_action(self, payload: dict[str, Any]) -> dict[str, Any]:
        action = str(payload["action"]).upper().strip()
        order_id = str(payload["order_id"])
        operator_id = str(payload.get("operator_id", "operator"))

        if action == "APPROVE":
            order = self.ledger.approve_order(order_id, operator_id=operator_id)
        elif action == "SUBMIT":
            order = self.ledger.mark_submitted(
                order_id,
                operator_id=operator_id,
                exchange_order_ref=str(payload["exchange_order_ref"]),
            )
        elif action == "WORKING":
            order = self.ledger.mark_working(order_id, operator_id=operator_id)
        elif action == "FILL":
            order = self.ledger.record_fill(
                order_id,
                fill_qty_btc=float(payload["fill_qty_btc"]),
                fill_price_usdt=float(payload["fill_price_usdt"]),
                fee_asset=str(payload.get("fee_asset", "USDT")),
                fee_amount=float(payload.get("fee_amount", 0.0)),
                exchange_fill_ref=str(payload.get("exchange_fill_ref", "MANUAL_FILL")),
                recorded_by=operator_id,
            )
        elif action == "REQUEST_CANCEL":
            order = self.ledger.request_cancellation(order_id, operator_id=operator_id)
        elif action in {"CANCELLED", "EXPIRED", "REJECTED"}:
            order = self.ledger.confirm_terminal_status(
                order_id,
                terminal_status=OrderStatus(action),
                confirmed_by=operator_id,
                reason=str(payload.get("reason", "")),
            )
        else:
            raise ValueError(f"Unsupported order action: {action!r}")

        return order.to_dict()

    def export_audit_bytes(self, fmt: str) -> tuple[bytes, str, str]:
        """Return (content_bytes, content_type, filename) for CSV or JSON audit export."""
        fmt_norm = fmt.lower().strip()
        if fmt_norm == "json":
            events = self.audit_logger.read_events()
            return (
                json.dumps(events, indent=2).encode("utf-8"),
                "application/json; charset=utf-8",
                "cortex_audit_export.json",
            )
        if fmt_norm == "csv":
            tmp_csv = self.data_dir / "_export_tmp.csv"
            self.audit_logger.export_csv(tmp_csv)
            content = tmp_csv.read_bytes()
            tmp_csv.unlink(missing_ok=True)
            return (
                content,
                "text/csv; charset=utf-8",
                "cortex_audit_export.csv",
            )
        raise ValueError(f"Unsupported export format {fmt!r}; expected json or csv.")
