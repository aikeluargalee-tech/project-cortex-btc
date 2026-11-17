"""
Immutable UTC Audit & Snapshot Persistence Layer (Section 16 / Section 17).
"""

from __future__ import annotations

import csv
import hashlib
import json
import uuid
from pathlib import Path
from typing import Any

from cortex_core.models import AuditEvent
from cortex_core.time_utils import ensure_utc_iso, utc_now


def canonical_sha256(payload: Any) -> str:
    """Compute deterministic SHA-256 digest over a JSON-serializable payload."""
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


class AuditLogger:
    """Append-only JSONL audit trail storing UTC-timestamped system records."""

    def __init__(self, log_path: Path) -> None:
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def record(
        self,
        event_type: str,
        actor: str,
        summary: str,
        details: dict[str, Any],
        *,
        timestamp_utc: str | None = None,
    ) -> AuditEvent:
        ts_iso = ensure_utc_iso(timestamp_utc or utc_now(), field_name="timestamp_utc")
        event_id = f"AUD-{uuid.uuid4().hex[:12].upper()}"
        body = {
            "event_id": event_id,
            "event_type": event_type,
            "timestamp_utc": ts_iso,
            "actor": actor,
            "summary": summary,
            "details": details,
        }
        digest = canonical_sha256(body)
        event = AuditEvent(
            event_id=event_id,
            event_type=event_type,
            timestamp_utc=ts_iso,
            actor=actor,
            summary=summary,
            details=details,
            event_sha256=digest,
        )
        with self.log_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(event.to_dict(), sort_keys=True) + "\n")
        return event

    def read_events(self, *, event_type: str | None = None) -> list[dict[str, Any]]:
        if not self.log_path.exists():
            return []
        records: list[dict[str, Any]] = []
        with self.log_path.open("r", encoding="utf-8") as fh:
            for line in fh:
                text = line.strip()
                if not text:
                    continue
                item = json.loads(text)
                if event_type is None or item.get("event_type") == event_type:
                    records.append(item)
        return records

    def export_json(self, output_path: Path, *, event_type: str | None = None) -> Path:
        events = self.read_events(event_type=event_type)
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(events, indent=2), encoding="utf-8")
        return output_path

    def export_csv(self, output_path: Path, *, event_type: str | None = None) -> Path:
        events = self.read_events(event_type=event_type)
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fieldnames = ["event_id", "event_type", "timestamp_utc", "actor", "summary", "details_json", "event_sha256"]
        with output_path.open("w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=fieldnames)
            writer.writeheader()
            for ev in events:
                writer.writerow(
                    {
                        "event_id": ev.get("event_id", ""),
                        "event_type": ev.get("event_type", ""),
                        "timestamp_utc": ev.get("timestamp_utc", ""),
                        "actor": ev.get("actor", ""),
                        "summary": ev.get("summary", ""),
                        "details_json": json.dumps(ev.get("details", {}), sort_keys=True),
                        "event_sha256": ev.get("event_sha256", ""),
                    }
                )
        return output_path
