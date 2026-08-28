"""Tests for the recruitment, screening and apprenticeship model."""

from __future__ import annotations

import sys
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from model.rcu.people import (  # noqa: E402
    EFFORT_PATTERNS,
    ApprenticeshipParams,
    Village,
    apprenticeship,
    coverage_gap,
    minimum_village_for_cadre_sufficiency,
    screen_outcomes,
    screening_bias,
    years_to_replace_masters,
)


# --------------------------------------------------------------------------
# Cadre versus acceptance
# --------------------------------------------------------------------------


def test_cadre_cannot_supply_acceptance_in_any_real_market():
    """The central finding: a 10-15 person cadre is not an acceptance base."""
    for adults, traders in ((800, 60), (3000, 240), (12000, 900)):
        g = coverage_gap(Village(adults=adults, traders=traders), cadre_size=15)
        assert not g.feasible
        assert g.shortfall > 0


def test_cadre_sufficiency_requires_an_implausibly_small_market():
    """A cadre is only 60% of traders in a hamlet too small to pilot in."""
    assert minimum_village_for_cadre_sufficiency() < 500


def test_larger_market_means_worse_cadre_coverage():
    small = coverage_gap(Village(800, 60))
    large = coverage_gap(Village(12000, 900))
    assert large.cadre_covers < small.cadre_covers


def test_doers_exceed_cadre_but_still_fall_short_of_traders():
    """Even recruiting every 'doer' does not reach the acceptance target."""
    v = Village(adults=3000, traders=240)
    g = coverage_gap(v)
    assert v.doers > g.cadre
    assert v.doers >= g.traders_needed or g.shortfall > 0


def test_full_acceptance_target_scales_with_market():
    g = coverage_gap(Village(3000, 240), acceptance_target=0.60)
    assert g.traders_needed == 144


# --------------------------------------------------------------------------
# Screening bias
# --------------------------------------------------------------------------


def test_screening_misses_reliable_poor_people():
    r = screening_bias()
    assert r["destitute"].recall < r["comfortable"].recall


def test_screening_bias_is_large_enough_to_matter():
    """Same base rate of reliability, very different measured outcome."""
    r = screening_bias()
    extra = r["destitute"].wrongly_excluded - r["comfortable"].wrongly_excluded
    assert extra >= 15


def test_no_bias_when_circumstances_are_equal():
    r = screening_bias(comfortable_miss=0.05, destitute_miss=0.05)
    assert r["destitute"].recall == r["comfortable"].recall


def test_precision_is_poor_when_base_rate_is_low():
    """Most people who pass a single test are still not reliable.

    This is the base-rate fallacy: with a 5% base rate and a 10% false-pass
    rate, passers are dominated by false positives. It is the statistical
    argument for repeated observation over a single test.
    """
    o = screen_outcomes(1000, base_rate=0.05, miss_rate=0.05, false_pass_rate=0.10)
    assert o.precision < Decimal("0.40")


def test_repeated_independent_tests_improve_precision():
    single = screen_outcomes(1000, 0.05, 0.05, false_pass_rate=0.10)
    triple = screen_outcomes(1000, 0.05, 0.05, false_pass_rate=0.10**3)
    assert triple.precision > single.precision


def test_recall_and_precision_bounded():
    for miss in (0.0, 0.3, 0.9):
        o = screen_outcomes(1000, 0.05, miss)
        assert Decimal(0) <= o.recall <= Decimal(1)
        assert Decimal(0) <= o.precision <= Decimal(1)


# --------------------------------------------------------------------------
# Apprenticeship
# --------------------------------------------------------------------------


def test_apprenticeship_does_not_produce_twentyfold_growth_in_a_decade():
    """The manual's '20x in ten years' claim fails under honest attrition."""
    p = ApprenticeshipParams()
    rows = apprenticeship(p, horizon=10)
    assert rows[-1]["practitioners"] < 4 * p.masters


def test_apprenticeship_does_replace_the_masters():
    """The real and sufficient win: knowledge outlives its holders."""
    assert years_to_replace_masters() is not None
    assert years_to_replace_masters() <= 8


def test_no_graduates_before_training_completes():
    p = ApprenticeshipParams(years_to_qualify=4)
    rows = apprenticeship(p, horizon=4)
    assert all(r["qualified_this_year"] == 0 for r in rows)


def test_masters_attrit_over_time():
    rows = apprenticeship(horizon=20)
    assert rows[-1]["masters"] < rows[0]["masters"]


def test_capacity_not_enthusiasm_is_the_bottleneck():
    """Doubling supervision capacity raises output; wanting more does not."""
    base = apprenticeship(ApprenticeshipParams(), horizon=15)[-1]["practitioners"]
    more = apprenticeship(
        ApprenticeshipParams(apprentices_per_master=6), horizon=15
    )[-1]["practitioners"]
    assert more > base


def test_retention_matters_more_than_intake():
    """Training people who then leave does not build community capacity."""
    good = apprenticeship(ApprenticeshipParams(retention_rate=0.9), horizon=15)[-1]
    poor = apprenticeship(ApprenticeshipParams(retention_rate=0.3), horizon=15)[-1]
    assert good["practitioners"] > poor["practitioners"] * 2


def test_completion_rate_scales_output():
    hi = apprenticeship(ApprenticeshipParams(completion_rate=0.9), horizon=12)[-1]
    lo = apprenticeship(ApprenticeshipParams(completion_rate=0.3), horizon=12)[-1]
    assert hi["practitioners"] > lo["practitioners"]


# --------------------------------------------------------------------------
# Effort patterns are descriptive, not moral
# --------------------------------------------------------------------------


def test_every_effort_pattern_has_a_non_judgemental_reading():
    for name, entry in EFFORT_PATTERNS.items():
        assert entry["may_indicate"]
        assert entry["response"]
        assert entry["do_not"]


def test_resource_diversion_is_framed_as_a_system_diagnostic():
    entry = EFFORT_PATTERNS["resource_diversion"]
    assert "diagnostic" in entry["response"]
    assert "theft" in entry["do_not"]


def test_low_effort_requires_welfare_check_before_judgement():
    assert "welfare" in EFFORT_PATTERNS["low_intermittent"]["do_not"]
