"""UTC storage and Malaysia Time (MYT / UTC+8) display utilities."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any
from zoneinfo import ZoneInfo


def myt_tz() -> timezone | ZoneInfo:
    """Return Malaysia Time timezone (Asia/Kuala_Lumpur, fixed UTC+8 fallback)."""
    try:
        return ZoneInfo("Asia/Kuala_Lumpur")
    except Exception:
        return timezone(timedelta(hours=8), name="MYT")


def utc_now() -> datetime:
    """Return current UTC datetime with second precision."""
    return datetime.now(timezone.utc).replace(microsecond=0)


def parse_utc_timestamp(value: Any) -> datetime | None:
    """
    Parse ISO-8601, 'YYYY-MM-DD HH:MM:SS UTC/MYT', 'YYYY-MM-DD', or Unix epoch
    into a timezone-aware UTC datetime. Returns None if missing or unparseable.
    """
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, datetime):
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)
    if isinstance(value, (int, float)):
        if value <= 0:
            return None
        epoch = float(value)
        if epoch > 1e12:
            epoch /= 1000.0
        try:
            return datetime.fromtimestamp(epoch, tz=timezone.utc)
        except (OverflowError, OSError, ValueError):
            return None
    if not isinstance(value, str):
        return None
    text = value.strip()
    if not text or text in {"NOT CONFIGURED", "DATA UNAVAILABLE", "UNVALIDATED"}:
        return None
    if text.endswith(" UTC"):
        text = text[:-4].strip() + "+00:00"
    elif text.endswith(" MYT"):
        text = text[:-4].strip() + "+08:00"
    elif text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(text)
    except ValueError:
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
            try:
                return datetime.strptime(text, fmt).replace(tzinfo=timezone.utc)
            except ValueError:
                continue
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def to_utc_iso(value: Any) -> str | None:
    """Normalize a datetime/timestamp to canonical UTC ISO-8601 ('...Z')."""
    dt = parse_utc_timestamp(value)
    if dt is None:
        return None
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def ensure_utc_iso(value: Any, *, field_name: str = "timestamp") -> str:
    """Validate and return canonical UTC ISO-8601 string, raising ValueError if invalid."""
    iso = to_utc_iso(value)
    if iso is None:
        raise ValueError(f"Invalid or missing UTC timestamp for '{field_name}': {value!r}")
    return iso


def format_myt(value: Any) -> str:
    """Format a UTC timestamp for operator display in Malaysia Time (MYT, UTC+8)."""
    dt = parse_utc_timestamp(value)
    if dt is None:
        return "DATA UNAVAILABLE"
    return dt.astimezone(myt_tz()).strftime("%Y-%m-%d %H:%M:%S MYT (UTC+8)")
