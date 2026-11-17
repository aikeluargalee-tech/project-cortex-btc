"""Shared constants and controlled enumerations for CORTEX-BTC."""

from __future__ import annotations

from enum import Enum

NOT_CONFIGURED = "NOT CONFIGURED"
DATA_UNAVAILABLE = "DATA UNAVAILABLE"
UNVALIDATED = "UNVALIDATED"


class DataStatus(str, Enum):
    VERIFIED = "VERIFIED"
    PARTIALLY_VERIFIED = "PARTIALLY VERIFIED"
    PROXY = "PROXY"
    STALE = "STALE"
    UNAVAILABLE = "UNAVAILABLE"
    CONFLICTING = "CONFLICTING"


class OperatingMode(str, Enum):
    RESEARCH = "RESEARCH"
    PAPER_TRADING = "PAPER_TRADING"
    LIVE_HUMAN_DECISION_SUPPORT = "LIVE_HUMAN_DECISION_SUPPORT"


class OrderStatus(str, Enum):
    PROPOSED = "PROPOSED"
    APPROVED = "APPROVED"
    SUBMITTED = "SUBMITTED"
    WORKING = "WORKING"
    PARTIALLY_FILLED = "PARTIALLY FILLED"
    FILLED = "FILLED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"
    REJECTED = "REJECTED"


ACTIVE_RESERVATION_ORDER_STATUSES: frozenset[OrderStatus] = frozenset(
    {
        OrderStatus.PROPOSED,
        OrderStatus.APPROVED,
        OrderStatus.SUBMITTED,
        OrderStatus.WORKING,
        OrderStatus.PARTIALLY_FILLED,
    }
)

TERMINAL_ORDER_STATUSES: frozenset[OrderStatus] = frozenset(
    {
        OrderStatus.FILLED,
        OrderStatus.CANCELLED,
        OrderStatus.EXPIRED,
        OrderStatus.REJECTED,
    }
)


class LoopType(str, Enum):
    LOOP_A = "LOOP_A"  # USDT -> BTC -> USDT
    LOOP_B = "LOOP_B"  # BTC -> USDT -> BTC


class CycleStatus(str, Enum):
    OPEN = "OPEN"
    PARTIALLY_CONVERTED = "PARTIALLY_CONVERTED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class ReconciliationStatus(str, Enum):
    RECONCILED = "RECONCILED"
    DISCREPANCY = "DISCREPANCY"
    NOT_CONFIGURED = "NOT CONFIGURED"


class Verdict(str, Enum):
    BUY = "BUY"
    HOLD = "HOLD"
    SELL = "SELL"
    ABSTAIN = "ABSTAIN"


class PortfolioState(str, Enum):
    USDT_100 = "100% USDT"
    BTC_ACCUMULATION = "BTC ACCUMULATION"
    BTC_HOLD = "BTC HOLD"
    BTC_REDUCTION = "BTC REDUCTION"
    BTC_DEFENSIVE = "BTC DEFENSIVE"
    ROTATION_TO_USDT = "ROTATION TO USDT"
    RE_ACCUMULATION = "RE-ACCUMULATION"
    DATA_HALT = "DATA HALT"
    HUMAN_REVIEW = "HUMAN REVIEW"


class ModuleState(str, Enum):
    WATCH = "WATCH"
    SETUP = "SETUP"
    CONFIRMED = "CONFIRMED"
    ELIGIBLE = "ELIGIBLE"
    INVALIDATED = "INVALIDATED"
    DATA_HALT = "DATA HALT"
    REVIEW = "REVIEW"


class ExitClassification(str, Enum):
    PROFIT_TAKING = "PROFIT-TAKING"
    RISK_REDUCTION = "RISK REDUCTION"
    DEFENSIVE_EXIT = "DEFENSIVE EXIT"
