"""Community security: workload, fraud detection, and capture resistance.

The security proposal in the source document is largely sound, and its
strongest claim is one it does not emphasise: **most of the work is
mediation and fraud forensics, not force.** This module quantifies that,
and tests three things that determine whether such a body stays accountable.

1. ``workload`` -- what a community security cooperative actually spends its
   time on, and therefore what it should be selected and trained for.

2. ``detection`` -- whether dual inspection plus random audit plus consumer
   verification actually catches commodity fraud. This matters more than
   policing: undetected grade fraud destroys the currency, and the currency
   is the thing keeping people fed.

3. ``capture`` -- whether rotation genuinely prevents an armed group from
   becoming a permanent class, or merely slows it.

One doctrine from the source is contradicted by evidence and is corrected
here: the claim that police numbers have no effect on crime. Modern
quasi-experimental work finds meaningful effects. The honest argument for
this model is accountability and fit-to-task, not a false claim that
policing does nothing.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import ROUND_HALF_UP, Decimal


def _q(x: Decimal, places: str = "0.01") -> Decimal:
    return x.quantize(Decimal(places), rounding=ROUND_HALF_UP)


# --------------------------------------------------------------------------
# 1. What security work actually consists of
# --------------------------------------------------------------------------

#: Annual incidents per 1,000 adults, by category, for a rural district with
#: an active commodity-currency market. Disputes dominate; violent crime is
#: rare in absolute terms even where it is feared most.
INCIDENT_RATES: dict[str, float] = {
    "commercial_dispute": 85.0,     # debt, quality, delivery disagreements
    "land_and_livestock": 40.0,     # boundaries, straying animals, damage
    "family_and_neighbour": 55.0,   # domestic and interpersonal conflict
    "quality_fraud": 18.0,          # grade, weight, moisture misrepresentation
    "counterfeit_or_ledger": 4.0,   # note forgery, double presentation
    "theft": 22.0,
    "assault": 9.0,
    "serious_violent": 1.2,
}

#: Hours of security-member time each incident type consumes.
INCIDENT_HOURS: dict[str, float] = {
    "commercial_dispute": 3.0,
    "land_and_livestock": 5.0,
    "family_and_neighbour": 4.0,
    "quality_fraud": 6.0,
    "counterfeit_or_ledger": 10.0,
    "theft": 5.0,
    "assault": 8.0,
    "serious_violent": 30.0,
}

#: Which incidents require any capacity for force at all.
FORCE_CATEGORIES: frozenset[str] = frozenset(
    {"theft", "assault", "serious_violent"}
)


@dataclass(frozen=True)
class Workload:
    population: int
    hours_by_category: dict[str, float]

    @property
    def total_hours(self) -> float:
        return sum(self.hours_by_category.values())

    @property
    def force_hours(self) -> float:
        return sum(
            h for c, h in self.hours_by_category.items() if c in FORCE_CATEGORIES
        )

    @property
    def mediation_hours(self) -> float:
        return sum(
            h
            for c, h in self.hours_by_category.items()
            if c in {"commercial_dispute", "land_and_livestock", "family_and_neighbour"}
        )

    @property
    def forensic_hours(self) -> float:
        return sum(
            h
            for c, h in self.hours_by_category.items()
            if c in {"quality_fraud", "counterfeit_or_ledger"}
        )

    @property
    def force_share(self) -> Decimal:
        if self.total_hours == 0:
            return Decimal(0)
        return _q(Decimal(self.force_hours) / Decimal(self.total_hours), "0.001")

    @property
    def mediation_share(self) -> Decimal:
        if self.total_hours == 0:
            return Decimal(0)
        return _q(Decimal(self.mediation_hours) / Decimal(self.total_hours), "0.001")

    @property
    def forensic_share(self) -> Decimal:
        if self.total_hours == 0:
            return Decimal(0)
        return _q(Decimal(self.forensic_hours) / Decimal(self.total_hours), "0.001")

    def members_needed(
        self,
        hours_per_member_year: float = 900,
        min_on_call: int = 2,
        availability: float = 0.4,
    ) -> int:
        """Rotating members required.

        Caseload alone understates the number badly. A security cooperative
        must also field at least ``min_on_call`` people at any hour, and
        rotating part-time members are only available a fraction of the
        time. Coverage, not caseload, is what sets the roster.
        """
        by_caseload = self.total_hours / hours_per_member_year
        by_coverage = min_on_call / max(availability, 0.01)
        return max(1, int(max(by_caseload, by_coverage) + 0.999))


def workload(population: int = 1000, adult_share: float = 0.55) -> Workload:
    adults = population * adult_share
    hours = {
        cat: (rate * adults / 1000) * INCIDENT_HOURS[cat]
        for cat, rate in INCIDENT_RATES.items()
    }
    return Workload(population=population, hours_by_category=hours)


# --------------------------------------------------------------------------
# 2. Fraud detection: does layered verification work?
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class DetectionResult:
    fraud_attempts: int
    caught_at_deposit: float
    caught_at_audit: float
    caught_by_consumer: float
    undetected: float

    @property
    def detection_rate(self) -> Decimal:
        if self.fraud_attempts == 0:
            return Decimal(1)
        caught = (
            self.caught_at_deposit + self.caught_at_audit + self.caught_by_consumer
        )
        return _q(Decimal(caught) / Decimal(self.fraud_attempts), "0.001")

    @property
    def undetected_rate(self) -> Decimal:
        return _q(Decimal(1) - self.detection_rate, "0.001")


def detection(
    fraud_attempts: int = 100,
    single_inspector_catch: float = 0.70,
    dual_inspection: bool = True,
    collusion_rate: float = 0.10,
    audit_fraction: float = 0.10,
    audit_catch: float = 0.90,
    consumer_check_rate: float = 0.25,
    consumer_catch: float = 0.50,
) -> DetectionResult:
    """Model the three-layer verification scheme.

    Layer 1 is dual inspection at deposit. Two independent inspectors both
    have to miss the fraud -- unless they collude, which is why the collusion
    rate matters more than individual accuracy.

    Layer 2 is random audit of stored batches. Layer 3 is the consumer who
    tests what they actually received and complains.

    The important output is not the headline detection rate but the
    sensitivity to collusion: dual inspection is only as strong as the
    independence of the two inspectors.
    """
    n = float(fraud_attempts)

    if dual_inspection:
        # Independent misses multiply, but colluding pairs never catch it.
        miss = (1 - single_inspector_catch) ** 2
        p_deposit = (1 - collusion_rate) * (1 - miss)
    else:
        p_deposit = single_inspector_catch

    caught_deposit = n * p_deposit
    remaining = n - caught_deposit

    caught_audit = remaining * audit_fraction * audit_catch
    remaining -= caught_audit

    caught_consumer = remaining * consumer_check_rate * consumer_catch
    remaining -= caught_consumer

    return DetectionResult(
        fraud_attempts=fraud_attempts,
        caught_at_deposit=caught_deposit,
        caught_at_audit=caught_audit,
        caught_by_consumer=caught_consumer,
        undetected=remaining,
    )


def collusion_sensitivity(
    rates: tuple[float, ...] = (0.0, 0.05, 0.10, 0.25, 0.50, 1.0),
) -> list[tuple[float, Decimal]]:
    """How detection degrades as inspector collusion rises."""
    return [(r, detection(collusion_rate=r).detection_rate) for r in rates]


def audit_effort_curve(
    fractions: tuple[float, ...] = (0.0, 0.05, 0.10, 0.20, 0.40),
) -> list[tuple[float, Decimal]]:
    """Detection as a function of how much stock is randomly re-audited."""
    return [(f, detection(audit_fraction=f).detection_rate) for f in fractions]


# --------------------------------------------------------------------------
# 3. Capture resistance
# --------------------------------------------------------------------------


@dataclass
class CaptureModel:
    """Does rotation actually prevent an armed group becoming a class?

    Capture is modelled as accumulated influence. A member's influence grows
    with continuous months served and decays while they are back in ordinary
    productive work. Rotation works if and only if decay outpaces growth.
    """

    rotation_months: int = 9
    break_months: int = 18
    growth_per_month: float = 0.06
    decay_per_month: float = 0.04
    horizon_years: int = 20
    #: Influence level at which a member is effectively unaccountable.
    capture_threshold: float = 1.0

    def trajectory(self) -> list[float]:
        influence = 0.0
        out = []
        month = 0
        total = self.horizon_years * 12
        while month < total:
            for _ in range(min(self.rotation_months, total - month)):
                influence *= 1 + self.growth_per_month
                influence = max(influence, 0.05)
                out.append(influence)
                month += 1
            for _ in range(min(self.break_months, total - month)):
                influence *= 1 - self.decay_per_month
                out.append(influence)
                month += 1
        return out

    @property
    def peak_influence(self) -> float:
        t = self.trajectory()
        return max(t) if t else 0.0

    @property
    def captured(self) -> bool:
        return self.peak_influence >= self.capture_threshold

    def months_to_capture(self) -> int | None:
        for i, v in enumerate(self.trajectory(), 1):
            if v >= self.capture_threshold:
                return i
        return None


def max_safe_rotation(
    break_months: int = 18,
    growth: float = 0.06,
    decay: float = 0.04,
    horizon_years: int = 20,
) -> int:
    """Longest continuous tour that still resists capture over the horizon."""
    for months in range(1, 121):
        m = CaptureModel(
            rotation_months=months,
            break_months=break_months,
            growth_per_month=growth,
            decay_per_month=decay,
            horizon_years=horizon_years,
        )
        if m.captured:
            return months - 1
    return 120


def rotation_grid(
    tours: tuple[int, ...] = (6, 9, 12, 18, 24, 36),
    breaks: tuple[int, ...] = (6, 12, 18, 24),
) -> list[tuple[int, int, bool, float]]:
    """(tour, break, captured, peak influence) across the parameter space."""
    out = []
    for t in tours:
        for b in breaks:
            m = CaptureModel(rotation_months=t, break_months=b)
            out.append((t, b, m.captured, round(m.peak_influence, 3)))
    return out


# --------------------------------------------------------------------------
# 4. Armoury access control
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class ArmouryPolicy:
    """Two-person access with logged, time-delayed release."""

    keyholders: int = 5
    quorum: int = 2
    delay_minutes: int = 30
    #: Number of keyholders who would join an illegitimate release.
    corrupt_count: int = 2

    @property
    def unauthorised_release_probability(self) -> Decimal:
        """Chance a colluding group can assemble a quorum unaided.

        Modelled as: can the corrupt subset alone reach the quorum? If it
        can, release is certain from their point of view; if it cannot, they
        must recruit an honest keyholder, who is assumed to refuse and
        report. This makes quorum size the decisive control.
        """
        if self.corrupt_count >= self.quorum:
            return Decimal(1)
        # They must persuade the shortfall from honest keyholders.
        shortfall = self.quorum - self.corrupt_count
        honest = max(0, self.keyholders - self.corrupt_count)
        if honest < shortfall:
            return Decimal(0)
        # Assume a small independent chance an honest holder is deceived.
        return _q(Decimal("0.05") ** shortfall, "0.0001")

    @property
    def acceptable(self) -> bool:
        return self.unauthorised_release_probability < Decimal("0.05")
