"""Recruitment, cohort and capacity arithmetic for the human side of RCU.

The currency documents model grain, iron and decay. This module models the
constraint that actually binds first: **people**.

Three questions are answered numerically rather than rhetorically.

1. ``coverage_gap`` -- a cadre-only strategy recruits the most committed few.
   The currency needs a large fraction of a *market* to accept it. These are
   different quantities, and the gap between them is the single most
   important number on the human side.

2. ``screen_outcomes`` -- small-commitment tests are a diagnostic instrument,
   so they have a false-positive and false-negative rate like any other. A
   test applied to a poor population confuses *inability* with *unwillingness*
   and discards exactly the people the system exists to serve.

3. ``apprenticeship`` -- skills compound, but only at the rate masters can
   supervise. This finds the real bottleneck, which is not enthusiasm.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import ROUND_HALF_UP, Decimal


# --------------------------------------------------------------------------
# 1. Cadre size versus market coverage
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class Village:
    """A pilot community."""

    adults: int
    traders: int
    #: Share of adults who will reliably do sustained unpaid organising work.
    doer_share: float = 0.05

    @property
    def doers(self) -> int:
        return int(self.adults * self.doer_share)


@dataclass(frozen=True)
class CoverageGap:
    cadre: int
    traders_needed: int
    traders_total: int
    doers_available: int

    @property
    def shortfall(self) -> int:
        """Accepting traders that a cadre-only strategy cannot supply."""
        return max(0, self.traders_needed - self.cadre)

    @property
    def cadre_covers(self) -> Decimal:
        if self.traders_needed == 0:
            return Decimal(1)
        return (Decimal(self.cadre) / self.traders_needed).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )

    @property
    def feasible(self) -> bool:
        return self.cadre >= self.traders_needed


def coverage_gap(
    village: Village,
    cadre_size: int = 15,
    acceptance_target: float = 0.60,
) -> CoverageGap:
    """Can a small cadre deliver the currency's acceptance requirement?

    The blueprint's Phase 1 kill criterion is that at least 60% of traders in
    the pilot market accept RCU. A cadre of 10-15 is smaller than that number
    in any market worth piloting in, so the cadre cannot *be* the acceptance
    base -- it can only be the thing that recruits it.
    """
    needed = int(village.traders * acceptance_target + 0.999)
    return CoverageGap(
        cadre=cadre_size,
        traders_needed=needed,
        traders_total=village.traders,
        doers_available=village.doers,
    )


def minimum_village_for_cadre_sufficiency(
    cadre_size: int = 15, acceptance_target: float = 0.60, trader_share: float = 0.08
) -> int:
    """Largest market in which a cadre alone could supply acceptance.

    Answers: "how small must the market be before 15 people *are* 60% of the
    traders?" If the answer is implausibly small, the cadre-only doctrine is
    arithmetically incompatible with the currency.
    """
    # traders = adults * trader_share ; need cadre >= 0.6 * traders
    max_traders = cadre_size / acceptance_target
    return int(max_traders / trader_share)


# --------------------------------------------------------------------------
# 2. Screening: tests have error rates
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class ScreenOutcome:
    population: int
    truly_reliable: int
    passed: int
    true_positives: int
    false_positives: int
    false_negatives: int

    @property
    def precision(self) -> Decimal:
        """Of those who pass, what share are genuinely reliable?"""
        if self.passed == 0:
            return Decimal(0)
        return (Decimal(self.true_positives) / self.passed).quantize(
            Decimal("0.001"), rounding=ROUND_HALF_UP
        )

    @property
    def recall(self) -> Decimal:
        """Of the genuinely reliable, what share does the test find?"""
        if self.truly_reliable == 0:
            return Decimal(0)
        return (Decimal(self.true_positives) / self.truly_reliable).quantize(
            Decimal("0.001"), rounding=ROUND_HALF_UP
        )

    @property
    def wrongly_excluded(self) -> int:
        return self.false_negatives


def screen_outcomes(
    population: int,
    base_rate: float,
    miss_rate: float,
    false_pass_rate: float = 0.10,
) -> ScreenOutcome:
    """Model a small-commitment test as a diagnostic instrument.

    ``miss_rate`` is the probability that a genuinely reliable person fails
    the test for reasons unrelated to character -- no bus fare, a sick child,
    piecework that day, no phone credit. For a comfortable population this is
    near zero. For a destitute population it is large, and it is *not*
    evidence about their commitment.
    """
    reliable = int(population * base_rate)
    unreliable = population - reliable
    tp = int(reliable * (1 - miss_rate))
    fn = reliable - tp
    fp = int(unreliable * false_pass_rate)
    return ScreenOutcome(
        population=population,
        truly_reliable=reliable,
        passed=tp + fp,
        true_positives=tp,
        false_positives=fp,
        false_negatives=fn,
    )


def screening_bias(
    population: int = 1000,
    base_rate: float = 0.05,
    comfortable_miss: float = 0.05,
    destitute_miss: float = 0.45,
) -> dict[str, ScreenOutcome]:
    """Compare screening applied to comfortable versus destitute candidates.

    The same test, the same underlying rate of reliability, different
    material circumstances. The difference in recall is the measure of how
    much talent an unadjusted test throws away.
    """
    return {
        "comfortable": screen_outcomes(population, base_rate, comfortable_miss),
        "destitute": screen_outcomes(population, base_rate, destitute_miss),
    }


# --------------------------------------------------------------------------
# 3. Apprenticeship capacity
# --------------------------------------------------------------------------


@dataclass
class ApprenticeshipParams:
    masters: int = 12
    apprentices_per_master: int = 3
    years_to_qualify: int = 4
    #: Fraction of apprentices who complete. Attrition is normal, not failure.
    completion_rate: float = 0.6
    #: Fraction of graduates who stay in the community rather than migrate.
    retention_rate: float = 0.7
    #: Years a new graduate must practise before supervising apprentices.
    years_before_teaching: int = 3
    #: Fraction of original masters lost per year (age, illness, moving).
    master_attrition: float = 0.08


def apprenticeship(
    p: ApprenticeshipParams | None = None, horizon: int = 20
) -> list[dict[str, float]]:
    """Project qualified practitioners over time.

    Deliberately pessimistic on the parameters that organisers are most
    optimistic about: completion, retention, and how soon a new graduate can
    supervise someone else. The output is intended to puncture the "20x in a
    decade" claim, not to support it.
    """
    p = p or ApprenticeshipParams()
    masters = float(p.masters)
    practitioners = 0.0
    # cohorts[year_of_qualification] = number qualifying that year
    pipeline: list[tuple[int, float]] = []
    graduates_by_year: dict[int, float] = {}
    rows = []

    for year in range(1, horizon + 1):
        # Masters age out.
        masters *= 1 - p.master_attrition

        # Graduates who have practised long enough become teaching-capable.
        teaching_capable = sum(
            n for y, n in graduates_by_year.items()
            if year - y >= p.years_before_teaching
        )
        supervisors = masters + teaching_capable * p.retention_rate

        # Intake is limited by supervision capacity, not by enthusiasm.
        capacity = supervisors * p.apprentices_per_master
        in_training = sum(n for _, n in pipeline)
        intake = max(0.0, capacity - in_training)
        pipeline.append((year + p.years_to_qualify, intake))

        # Anyone finishing this year qualifies.
        finishing = sum(n for y, n in pipeline if y == year)
        pipeline = [(y, n) for y, n in pipeline if y != year]
        qualified = finishing * p.completion_rate
        graduates_by_year[year] = qualified
        practitioners += qualified * p.retention_rate

        rows.append(
            {
                "year": year,
                "masters": round(masters, 1),
                "supervisors": round(supervisors, 1),
                "in_training": round(in_training + intake, 1),
                "qualified_this_year": round(qualified, 1),
                "practitioners": round(practitioners, 1),
            }
        )
    return rows


def years_to_replace_masters(p: ApprenticeshipParams | None = None) -> int | None:
    """When does the community first hold more practitioners than it began with?

    This is the honest success criterion: not "20x in ten years" but "the
    knowledge survived the death of the people who held it."
    """
    p = p or ApprenticeshipParams()
    for row in apprenticeship(p, horizon=40):
        if row["practitioners"] >= p.masters:
            return int(row["year"])
    return None


# --------------------------------------------------------------------------
# 4. Effort classification -- descriptive, and explicitly not moral
# --------------------------------------------------------------------------

#: Observable pattern -> what it may indicate and what to do. The middle
#: column exists to stop an organiser reading effort as character: identical
#: behaviour has different causes, and the response differs accordingly.
EFFORT_PATTERNS: dict[str, dict[str, str]] = {
    "high_consistent": {
        "may_indicate": "genuine commitment, or unsustainable over-extension",
        "response": "increase responsibility; watch for burnout; insist on rest",
        "do_not": "assume it will continue indefinitely without support",
    },
    "high_intermittent": {
        "may_indicate": "commitment constrained by unstable circumstances",
        "response": "offer tasks that tolerate interruption; address the constraint",
        "do_not": "read absence as unreliability",
    },
    "low_consistent": {
        "may_indicate": "hedging, limited capacity, or an undiagnosed barrier",
        "response": "ask directly what would make participation easier",
        "do_not": "escalate demands before understanding the ceiling",
    },
    "low_intermittent": {
        "may_indicate": "acute crisis, illness, or genuine disinterest",
        "response": "check welfare first; only then conclude disinterest",
        "do_not": "conclude disinterest without checking welfare",
    },
    "resource_diversion": {
        "may_indicate": "unmet acute need, or unclear entitlement rules",
        "response": "treat as a system diagnostic; fix distribution and clarity",
        "do_not": "treat as theft before checking whether need was met",
    },
    "sabotage": {
        "may_indicate": "conflicting interest, coercion, or factional dispute",
        "response": "remove from sensitive roles; investigate the pressure source",
        "do_not": "assume malice without checking for coercion",
    },
}
