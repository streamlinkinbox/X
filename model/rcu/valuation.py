"""Note valuation: the canonical decay and redemption arithmetic.

Every wallet, every point-of-sale device and every ledger node must produce
*bit-identical* answers to "what is this note worth today?". Floating point
drift across devices is a real settlement risk, so all monetary amounts are
integers in the smallest unit ("cents", 1/100 RCU) and all decay arithmetic
is done in integer basis points with explicit rounding rules.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import ROUND_HALF_UP, Decimal, getcontext

from .classes import CommodityClass, DecayPeriod, get

getcontext().prec = 28

#: Monetary amounts are integers in cents (1 RCU = 100 cents).
CENTS = 100


def months_elapsed(issued: date, asof: date) -> int:
    """Whole calendar months between two dates.

    Decay steps on the monthly anniversary of issuance, not pro rata by day.
    This is deliberate: a note's value must be a step function that an
    offline device with only a calendar can compute, and that a market trader
    can predict. Pro-rata daily decay would make every price negotiation a
    fractional-arithmetic problem.
    """
    if asof < issued:
        return 0
    months = (asof.year - issued.year) * 12 + (asof.month - issued.month)
    if asof.day < issued.day:
        months -= 1
    return max(0, months)


def decay_multiplier(cls: CommodityClass, age_months: int) -> Decimal:
    """Fraction of face value retained at ``age_months`` after issuance."""
    if not cls.decays:
        return Decimal(1)
    decaying = age_months - cls.grace_months
    if decaying <= 0:
        return Decimal(1)

    if cls.decay_period is DecayPeriod.MONTH:
        rate = Decimal(str(cls.decay_rate))
        periods = decaying
    else:
        # Annual-rate classes step once per completed year of decay.
        rate = Decimal(str(cls.decay_rate))
        periods = decaying // 12

    if periods <= 0:
        return Decimal(1)
    return (Decimal(1) - rate) ** periods


@dataclass(frozen=True)
class Note:
    """A bearer note in circulation."""

    serial: str
    class_code: str
    face_cents: int
    issued: date
    issuer_id: str
    warehouse_id: str

    @property
    def commodity_class(self) -> CommodityClass:
        return get(self.class_code)

    def age_months(self, asof: date) -> int:
        return months_elapsed(self.issued, asof)

    def is_expired(self, asof: date) -> bool:
        cls = self.commodity_class
        if cls.max_validity_months is None:
            return False
        return self.age_months(asof) >= cls.max_validity_months

    def value_cents(self, asof: date) -> int:
        """Current transferable value in cents.

        Rounding is HALF_UP to the cent, always in favour of a deterministic
        result rather than in favour of either party. An expired note is
        worth zero as *currency*; the holder retains a residual claim against
        the class reserve pool (see redemption rules in docs/06).
        """
        if self.is_expired(asof):
            return 0
        cls = self.commodity_class
        mult = decay_multiplier(cls, self.age_months(asof))
        raw = Decimal(self.face_cents) * mult
        return int(raw.quantize(Decimal(1), rounding=ROUND_HALF_UP))

    def value(self, asof: date) -> Decimal:
        """Current value in whole RCU, for display only."""
        return (Decimal(self.value_cents(asof)) / CENTS).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )

    def schedule(self, months: int) -> list[tuple[int, int]]:
        """Value trajectory as ``(age_month, value_cents)`` pairs."""
        cls = self.commodity_class
        out: list[tuple[int, int]] = []
        for m in range(months + 1):
            if cls.max_validity_months is not None and m >= cls.max_validity_months:
                out.append((m, 0))
                continue
            mult = decay_multiplier(cls, m)
            raw = Decimal(self.face_cents) * mult
            out.append((m, int(raw.quantize(Decimal(1), rounding=ROUND_HALF_UP))))
        return out


def issue_value_cents(assessed_market_cents: int, cls: CommodityClass) -> int:
    """How much currency may be issued against an assessed deposit.

    This is the single most important anti-inflation control in the system:
    notes are issued against the *haircut* value, never the full assessed
    value. The haircut absorbs price falls, grading error and shrinkage
    between inspections.
    """
    retained = Decimal(1) - Decimal(str(cls.haircut))
    raw = Decimal(assessed_market_cents) * retained
    return int(raw.quantize(Decimal(1), rounding=ROUND_HALF_UP))


def collateral_ratio(
    outstanding_cents: int, collateral_market_cents: int
) -> Decimal:
    """Collateral coverage of a class or a cooperative.

    Below 1.0 the series is insolvent: there is less commodity than there is
    currency claiming it. The system's circuit breakers key off this number.
    """
    if outstanding_cents <= 0:
        return Decimal("Infinity")
    return (Decimal(collateral_market_cents) / Decimal(outstanding_cents)).quantize(
        Decimal("0.0001"), rounding=ROUND_HALF_UP
    )
