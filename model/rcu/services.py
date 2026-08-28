"""Service credits: modelling labour-backed currency.

A commodity note is a claim on matter that already exists in a shed. A
service credit is a claim on **a future hour of a specific living person**.
That difference drives everything in this module.

Four questions are answered numerically.

1. ``clearing`` -- can a scarce specialist's hours actually meet demand? If
   one doctor serves 20,000 people, credits denominated in doctor-hours
   cannot clear, and a currency that cannot be redeemed is a queue ticket.

2. ``sick_cannot_earn`` -- the documented failure of Japan's Fureai Kippu:
   the frail and disabled could not earn credits precisely because they were
   frail, so they paid cash instead. Any care currency inherits this unless
   it is designed around it.

3. ``training_incentive`` -- flat-rate hours (1 hour = 1 hour regardless of
   skill) are morally attractive and remove the private return on long
   training. This computes what a flat rate does to the decision to spend
   seven years qualifying.

4. ``cost_decomposition`` -- how much of a treatment price is labour,
   consumables, equipment amortisation and overhead. Tests the claim that
   equipment is a pretext.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import ROUND_HALF_UP, Decimal


def _q(x: Decimal, places: str = "0.01") -> Decimal:
    return x.quantize(Decimal(places), rounding=ROUND_HALF_UP)


# --------------------------------------------------------------------------
# 1. Can specialist hours clear?
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class ServiceCapacity:
    """Supply and demand for one class of skilled service."""

    name: str
    practitioners: int
    population: int
    #: Productive hours per practitioner per year, after leave and admin.
    hours_per_year: int = 1600
    #: Episodes of care demanded per person per year.
    episodes_per_person: float = 2.0
    #: Practitioner hours consumed per episode.
    hours_per_episode: float = 0.5

    @property
    def supply_hours(self) -> float:
        return self.practitioners * self.hours_per_year

    @property
    def demand_hours(self) -> float:
        return self.population * self.episodes_per_person * self.hours_per_episode

    @property
    def coverage(self) -> Decimal:
        """Fraction of demanded hours that can actually be supplied."""
        if self.demand_hours == 0:
            return Decimal(1)
        return _q(Decimal(self.supply_hours) / Decimal(self.demand_hours), "0.001")

    @property
    def people_per_practitioner(self) -> int:
        if self.practitioners == 0:
            return self.population
        return int(self.population / self.practitioners)

    @property
    def can_clear(self) -> bool:
        """Can every credit issued be redeemed within the year?"""
        return self.coverage >= Decimal(1)

    @property
    def redeemable_share(self) -> Decimal:
        """Share of issued credits redeemable if issued against full demand."""
        return min(Decimal(1), self.coverage)

    def queue_years(self) -> Decimal:
        """Years to clear one year of demand at current capacity."""
        if self.supply_hours == 0:
            return Decimal("Infinity")
        return _q(Decimal(self.demand_hours) / Decimal(self.supply_hours))


def clearing(scenarios: list[ServiceCapacity]) -> dict[str, ServiceCapacity]:
    return {s.name: s for s in scenarios}


# --------------------------------------------------------------------------
# 2. The sick-cannot-earn problem
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class EarnCapacity:
    """Ability of a population segment to earn service credits."""

    segment: str
    people: int
    #: Fraction physically able to perform creditable service.
    able_fraction: float
    #: Relative need for care, 1.0 = population average.
    need_multiplier: float = 1.0


@dataclass(frozen=True)
class EarnGap:
    segment: str
    people: int
    credits_earnable: float
    credits_needed: float

    @property
    def self_sufficiency(self) -> Decimal:
        if self.credits_needed == 0:
            return Decimal("Infinity")
        return _q(
            Decimal(self.credits_earnable) / Decimal(self.credits_needed), "0.001"
        )

    @property
    def shortfall(self) -> float:
        return max(0.0, self.credits_needed - self.credits_earnable)

    @property
    def must_be_subsidised(self) -> bool:
        return self.self_sufficiency < Decimal(1)


def sick_cannot_earn(
    segments: list[EarnCapacity],
    hours_earnable_per_person: float = 100.0,
    hours_needed_per_person: float = 10.0,
) -> list[EarnGap]:
    """Quantify the Fureai Kippu trap.

    Japan's care-credit scheme found that the frail could not earn credits
    *because they were frail*, so they ended up paying cash -- and user fees
    grew to a large share of scheme income, excluding the poorest. A credit
    system whose unit is labour systematically underserves whoever cannot
    labour, which is the same population that needs care most.
    """
    out = []
    for s in segments:
        earnable = s.people * s.able_fraction * hours_earnable_per_person
        needed = s.people * hours_needed_per_person * s.need_multiplier
        out.append(
            EarnGap(
                segment=s.segment,
                people=s.people,
                credits_earnable=earnable,
                credits_needed=needed,
            )
        )
    return out


def system_subsidy_required(gaps: list[EarnGap]) -> float:
    """Total credits that must be granted rather than earned."""
    return sum(g.shortfall for g in gaps)


# --------------------------------------------------------------------------
# 3. Flat rate versus skill weighting
# --------------------------------------------------------------------------


@dataclass
class TrainingChoice:
    """Whether it is rational to undertake long training under a given rate."""

    years_training: int
    working_years: int
    #: Credits per hour earned by an unskilled worker.
    base_rate: float = 1.0
    #: Multiplier the skilled practitioner earns per hour.
    skill_multiplier: float = 1.0
    hours_per_year: int = 1600
    #: Credits earned per year while training (usually near zero).
    training_stipend_hours: float = 0.0

    def lifetime_if_trained(self) -> float:
        during = self.years_training * self.training_stipend_hours
        after = (
            self.working_years
            * self.hours_per_year
            * self.base_rate
            * self.skill_multiplier
        )
        return during + after

    def lifetime_if_untrained(self) -> float:
        total_years = self.years_training + self.working_years
        return total_years * self.hours_per_year * self.base_rate

    @property
    def net_gain(self) -> float:
        return self.lifetime_if_trained() - self.lifetime_if_untrained()

    @property
    def rational_to_train(self) -> bool:
        return self.net_gain > 0

    @property
    def breakeven_multiplier(self) -> Decimal:
        """Skill multiplier at which training just pays for itself."""
        total_years = self.years_training + self.working_years
        forgone = total_years * self.hours_per_year * self.base_rate
        stipend = self.years_training * self.training_stipend_hours
        denom = self.working_years * self.hours_per_year * self.base_rate
        if denom == 0:
            return Decimal("Infinity")
        return _q(Decimal(forgone - stipend) / Decimal(denom), "0.001")


def training_incentive(
    years_training: int = 7,
    working_years: int = 30,
    multipliers: tuple[float, ...] = (1.0, 1.5, 2.0, 3.0),
    stipend_hours: float = 0.0,
) -> list[TrainingChoice]:
    return [
        TrainingChoice(
            years_training=years_training,
            working_years=working_years,
            skill_multiplier=m,
            training_stipend_hours=stipend_hours,
        )
        for m in multipliers
    ]


# --------------------------------------------------------------------------
# 4. What actually drives the price of care
# --------------------------------------------------------------------------

#: Share of delivered cost by input, for a district-level facility in a
#: low-income setting. Hospital benchmarks in high-income systems put labour
#: near 56-60% and supplies plus drugs near 21-22%; equipment capital is a
#: small slice. Local values will differ and must be measured.
COST_SHARES: dict[str, Decimal] = {
    "practitioner_labour": Decimal("0.45"),
    "support_labour": Decimal("0.12"),
    "consumables_and_drugs": Decimal("0.25"),
    "equipment_amortisation": Decimal("0.08"),
    "facility_and_utilities": Decimal("0.07"),
    "administration": Decimal("0.03"),
}


@dataclass(frozen=True)
class CostDecomposition:
    total: Decimal
    payable_in_credits: Decimal
    requires_real_goods: Decimal

    @property
    def credit_share(self) -> Decimal:
        if self.total == 0:
            return Decimal(0)
        return _q(self.payable_in_credits / self.total, "0.001")

    @property
    def goods_share(self) -> Decimal:
        return _q(Decimal(1) - self.credit_share, "0.001")


def cost_decomposition(shares: dict[str, Decimal] | None = None) -> CostDecomposition:
    """Split delivered cost into what labour credits can and cannot pay for.

    Labour credits can pay people. They cannot pay for imported gloves,
    antibiotics, reagents or a replacement X-ray tube -- those require
    foreign exchange or physical commodities. This ratio bounds how much of
    healthcare a service currency can ever finance.
    """
    s = shares or COST_SHARES
    total = sum(s.values())
    labour = s.get("practitioner_labour", Decimal(0)) + s.get(
        "support_labour", Decimal(0)
    )
    # Administration is labour too, but facility and consumables are not.
    labour += s.get("administration", Decimal(0))
    return CostDecomposition(
        total=Decimal(total),
        payable_in_credits=labour,
        requires_real_goods=Decimal(total) - labour,
    )


def equipment_pretext_check(
    shares: dict[str, Decimal] | None = None,
) -> dict[str, object]:
    """Is 'equipment is expensive' a sufficient explanation for high prices?

    Returns the equipment share alongside labour and consumables so the
    claim can be judged rather than asserted. The honest answer is nuanced:
    capital equipment is genuinely a small share, so it does not justify high
    prices on its own -- but consumables, which are recurring and often
    imported, are large and are frequently conflated with 'equipment'.
    """
    s = shares or COST_SHARES
    equip = s.get("equipment_amortisation", Decimal(0))
    consum = s.get("consumables_and_drugs", Decimal(0))
    labour = s.get("practitioner_labour", Decimal(0)) + s.get(
        "support_labour", Decimal(0)
    )
    return {
        "equipment_share": equip,
        "consumables_share": consum,
        "labour_share": labour,
        "equipment_explains_price": equip > Decimal("0.25"),
        "recurring_goods_exceed_equipment": consum > equip,
        "verdict": (
            "Capital equipment is a small share and cannot by itself justify "
            "high prices. But recurring consumables and drugs are large and "
            "must be bought with real money or goods, not with labour credits."
        ),
    }


# --------------------------------------------------------------------------
# 5. Credit redemption risk
# --------------------------------------------------------------------------


@dataclass
class CreditPool:
    """Outstanding service credits against a practitioner cohort."""

    outstanding_hours: float
    practitioners: int
    hours_per_year: int = 1600
    #: Annual probability a practitioner leaves, dies or stops practising.
    attrition: float = 0.10

    def backing_hours(self, years: int = 1) -> float:
        """Practitioner-hours actually available over the horizon."""
        total = 0.0
        n = float(self.practitioners)
        for _ in range(years):
            total += n * self.hours_per_year
            n *= 1 - self.attrition
        return total

    def coverage(self, years: int = 1) -> Decimal:
        backing = self.backing_hours(years)
        if self.outstanding_hours == 0:
            return Decimal("Infinity")
        return _q(Decimal(backing) / Decimal(self.outstanding_hours), "0.001")

    def is_solvent(self, years: int = 1) -> bool:
        return self.coverage(years) >= Decimal(1)


def practitioner_departure_shock(
    pool: CreditPool, departures: int
) -> dict[str, object]:
    """What happens to credit holders when practitioners leave.

    Unlike a warehouse, the backing can walk away. A grain note survives the
    cooperative collapsing because the grain is still in the shed. A service
    credit backed by Dr. Mwangi becomes worthless the day Dr. Mwangi
    emigrates -- and emigration of health workers is common.
    """
    before = pool.coverage()
    remaining = max(0, pool.practitioners - departures)
    after_pool = CreditPool(
        outstanding_hours=pool.outstanding_hours,
        practitioners=remaining,
        hours_per_year=pool.hours_per_year,
        attrition=pool.attrition,
    )
    after = after_pool.coverage()
    return {
        "coverage_before": before,
        "coverage_after": after,
        "practitioners_left": remaining,
        "impaired": after < Decimal(1),
        "loss_fraction": _q(max(Decimal(0), Decimal(1) - after), "0.001"),
    }
