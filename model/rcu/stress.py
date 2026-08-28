"""Stress tests for the RCU system.

These are deliberately adversarial. The purpose is not to show that the
design works; it is to find the parameter regions where it breaks, so that
the blueprint can state its own failure conditions honestly.

Three scenarios:

1. ``harvest_cycle``  -- seasonal issuance against a single grain crop, to
   find out whether the money supply is stable or whether it collapses
   every lean season.
2. ``price_crash``    -- a 40% fall in the local price of the dominant
   collateral class, to find out whether the haircut is deep enough.
3. ``redemption_run`` -- 30% of holders present notes for physical
   redemption in one month, to find out whether the warehouse can honour it.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal

from .classes import CommodityClass, get
from .valuation import Note, decay_multiplier, issue_value_cents


@dataclass
class Cohort:
    """A batch of notes issued at one time against one deposit."""

    cls: CommodityClass
    issued_month: int
    face_cents: int
    collateral_market_cents: int

    def outstanding_cents(self, month: int) -> int:
        age = month - self.issued_month
        if age < 0:
            return 0
        if self.cls.max_validity_months is not None and age >= self.cls.max_validity_months:
            return 0
        mult = decay_multiplier(self.cls, age)
        return int(Decimal(self.face_cents) * mult)

    def collateral_cents(self, month: int, price_index: Decimal) -> int:
        """Market value of the remaining physical collateral.

        Physical shrinkage is modelled at the class storage-cost rate, which
        is the honest way to do it: the grain really does disappear whether
        or not the note says it does.
        """
        age = month - self.issued_month
        if age < 0:
            return 0
        monthly_shrink = Decimal(str(self.cls.storage_cost_pa)) / 12
        remaining = (Decimal(1) - monthly_shrink) ** age
        return int(Decimal(self.collateral_market_cents) * remaining * price_index)


@dataclass
class Result:
    months: list[int] = field(default_factory=list)
    outstanding: list[int] = field(default_factory=list)
    collateral: list[int] = field(default_factory=list)
    ratio: list[float] = field(default_factory=list)

    def min_ratio(self) -> float:
        return min(self.ratio) if self.ratio else float("nan")

    def breached(self, threshold: float = 1.0) -> bool:
        return any(r < threshold for r in self.ratio)

    def first_breach_month(self, threshold: float = 1.0) -> int | None:
        for m, r in zip(self.months, self.ratio):
            if r < threshold:
                return m
        return None


def _run(cohorts: list[Cohort], horizon: int, price_path: list[Decimal]) -> Result:
    res = Result()
    for m in range(horizon):
        px = price_path[m] if m < len(price_path) else price_path[-1]
        out = sum(c.outstanding_cents(m) for c in cohorts)
        col = sum(c.collateral_cents(m, px) for c in cohorts)
        res.months.append(m)
        res.outstanding.append(out)
        res.collateral.append(col)
        res.ratio.append(float(col) / out if out > 0 else float("inf"))
    return res


def harvest_cycle(
    class_code: str = "GR",
    horizon: int = 48,
    harvest_month: int = 3,
    deposit_cents: int = 10_000_000,
) -> Result:
    """Annual harvest deposits into a single grain class."""
    cls = get(class_code)
    cohorts: list[Cohort] = []
    for year in range(horizon // 12 + 1):
        m = harvest_month + 12 * year
        if m >= horizon:
            break
        cohorts.append(
            Cohort(
                cls=cls,
                issued_month=m,
                face_cents=issue_value_cents(deposit_cents, cls),
                collateral_market_cents=deposit_cents,
            )
        )
    return _run(cohorts, horizon, [Decimal(1)] * horizon)


def price_crash(
    class_code: str = "GR",
    horizon: int = 36,
    crash_month: int = 12,
    crash_pct: float = 0.40,
    deposit_cents: int = 10_000_000,
) -> Result:
    """A one-shot fall in the local price of the collateral commodity."""
    cls = get(class_code)
    cohorts = [
        Cohort(
            cls=cls,
            issued_month=0,
            face_cents=issue_value_cents(deposit_cents, cls),
            collateral_market_cents=deposit_cents,
        )
    ]
    path = [
        Decimal(1) if m < crash_month else Decimal(1) - Decimal(str(crash_pct))
        for m in range(horizon)
    ]
    return _run(cohorts, horizon, path)


def survivable_crash(class_code: str, tolerance: float = 0.001) -> float:
    """Largest price fall a class can absorb and stay collateralised.

    Solved by bisection on the crash magnitude, evaluated at the worst
    month of the horizon. This turns the haircut from a guess into a stated
    guarantee: "class GR survives a fall of X% in the maize price".
    """
    lo, hi = 0.0, 0.99
    while hi - lo > tolerance:
        mid = (lo + hi) / 2
        r = price_crash(class_code, crash_pct=mid)
        if r.breached(1.0):
            hi = mid
        else:
            lo = mid
    return lo


@dataclass
class RunResult:
    demanded_cents: int
    liquid_cents: int
    shortfall_cents: int
    honoured_fraction: float
    gate_triggered: bool


#: Fraction of physical stock convertible to goods or cash within 30 days
#: without moving the local price, keyed off the class liquidity descriptor.
#: These are judgement calls, not measurements -- they are the first thing a
#: pilot should replace with observed data.
LIQUIDITY_DEPTH: dict[str, float] = {
    "deep, globally priced": 0.60,
    "deep": 0.35,
    "deep where grid exists": 0.35,
    "deep (fertiliser), moderate (other)": 0.25,
    "deep but local": 0.20,
    "moderate": 0.15,
    "moderate (export-linked)": 0.12,
    "export-only": 0.05,
    "thin": 0.07,
    "very thin": 0.03,
}


def redemption_run(
    class_code: str = "GR",
    outstanding_cents: int = 10_000_000,
    presented_fraction: float = 0.30,
    saleable_within_month: float | None = None,
    cash_buffer_fraction: float = 0.10,
) -> RunResult:
    """Can the cooperative honour a wave of redemptions?

    ``saleable_within_month`` is the fraction of physical stock that can
    actually be converted to goods or cash inside 30 days without moving the
    local price -- this is the binding constraint, and it is brutal for thin
    classes like stone or strategic minerals. When ``None`` it is derived
    from the class liquidity descriptor.
    """
    cls = get(class_code)
    if saleable_within_month is None:
        saleable_within_month = LIQUIDITY_DEPTH.get(cls.liquidity, 0.10)
    demanded = int(outstanding_cents * presented_fraction)
    liquid = int(outstanding_cents * (saleable_within_month + cash_buffer_fraction))
    shortfall = max(0, demanded - liquid)
    return RunResult(
        demanded_cents=demanded,
        liquid_cents=liquid,
        shortfall_cents=shortfall,
        honoured_fraction=min(1.0, liquid / demanded) if demanded else 1.0,
        gate_triggered=shortfall > 0,
    )
