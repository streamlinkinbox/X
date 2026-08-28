"""Tests for service credits and labour-backed currency."""

from __future__ import annotations

import sys
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from model.rcu.services import (  # noqa: E402
    COST_SHARES,
    CreditPool,
    EarnCapacity,
    ServiceCapacity,
    TrainingChoice,
    cost_decomposition,
    equipment_pretext_check,
    practitioner_departure_shock,
    sick_cannot_earn,
    system_subsidy_required,
    training_incentive,
)


# --------------------------------------------------------------------------
# Clearing: can specialist hours meet demand?
# --------------------------------------------------------------------------


def test_scarce_doctor_credits_cannot_clear():
    """At realistic ratios, doctor-hour credits are unredeemable."""
    s = ServiceCapacity("doctor", practitioners=1, population=25_000)
    assert not s.can_clear
    assert s.coverage < Decimal("0.10")


def test_even_generous_doctor_ratio_fails_to_clear():
    s = ServiceCapacity("doctor", practitioners=1, population=5_000)
    assert not s.can_clear


def test_community_health_worker_credits_can_clear():
    """The key asymmetry: abundant skills can back a currency, scarce ones cannot."""
    s = ServiceCapacity("chw", practitioners=1, population=500)
    assert s.can_clear
    assert s.coverage > Decimal(1)


def test_queue_years_grows_as_capacity_shrinks():
    scarce = ServiceCapacity("a", 1, 25_000).queue_years()
    ample = ServiceCapacity("b", 1, 500).queue_years()
    assert scarce > ample


def test_redeemable_share_never_exceeds_one():
    for pop in (100, 5_000, 25_000):
        s = ServiceCapacity("x", 1, pop)
        assert s.redeemable_share <= Decimal(1)


def test_zero_practitioners_means_no_clearing():
    s = ServiceCapacity("none", practitioners=0, population=1000)
    assert not s.can_clear
    assert s.people_per_practitioner == 1000


# --------------------------------------------------------------------------
# The sick-cannot-earn trap
# --------------------------------------------------------------------------


SEGMENTS = [
    EarnCapacity("healthy", 700, 0.95, 0.6),
    EarnCapacity("frail elderly", 150, 0.15, 3.0),
    EarnCapacity("chronically ill", 100, 0.20, 4.0),
    EarnCapacity("children", 50, 0.05, 1.5),
]


def test_healthy_are_self_sufficient_in_credits():
    gaps = {g.segment: g for g in sick_cannot_earn(SEGMENTS)}
    assert not gaps["healthy"].must_be_subsidised


def test_frail_and_ill_cannot_earn_what_they_need():
    """Fureai Kippu's documented failure, reproduced."""
    gaps = {g.segment: g for g in sick_cannot_earn(SEGMENTS)}
    assert gaps["frail elderly"].must_be_subsidised
    assert gaps["chronically ill"].must_be_subsidised
    assert gaps["children"].must_be_subsidised


def test_need_is_inversely_related_to_earning_capacity():
    gaps = {g.segment: g for g in sick_cannot_earn(SEGMENTS)}
    assert gaps["chronically ill"].self_sufficiency < gaps["healthy"].self_sufficiency


def test_subsidy_requirement_is_material():
    total = system_subsidy_required(sick_cannot_earn(SEGMENTS))
    assert total > 0


def test_no_subsidy_needed_if_everyone_can_work():
    healthy_only = [EarnCapacity("all", 1000, 1.0, 1.0)]
    gaps = sick_cannot_earn(healthy_only)
    assert not gaps[0].must_be_subsidised


# --------------------------------------------------------------------------
# Flat rate versus training incentive
# --------------------------------------------------------------------------


def test_flat_rate_makes_long_training_irrational():
    """1 hour = 1 hour destroys the private return on seven years of study."""
    flat = TrainingChoice(years_training=7, working_years=30, skill_multiplier=1.0)
    assert not flat.rational_to_train
    assert flat.net_gain < 0


def test_modest_skill_premium_restores_the_incentive():
    weighted = TrainingChoice(years_training=7, working_years=30, skill_multiplier=1.5)
    assert weighted.rational_to_train


def test_breakeven_multiplier_is_modest():
    """The premium needed is far smaller than market wage differentials."""
    tc = TrainingChoice(years_training=7, working_years=30)
    assert Decimal("1.1") < tc.breakeven_multiplier < Decimal("1.5")


def test_stipend_lowers_the_required_premium():
    no_stipend = TrainingChoice(7, 30).breakeven_multiplier
    with_stipend = TrainingChoice(7, 30, training_stipend_hours=800).breakeven_multiplier
    assert with_stipend < no_stipend


def test_longer_training_needs_higher_premium():
    short = TrainingChoice(2, 30).breakeven_multiplier
    long = TrainingChoice(10, 30).breakeven_multiplier
    assert long > short


def test_incentive_sweep_is_monotonic():
    choices = training_incentive()
    gains = [c.net_gain for c in choices]
    assert gains == sorted(gains)


# --------------------------------------------------------------------------
# Cost decomposition: is equipment a pretext?
# --------------------------------------------------------------------------


def test_cost_shares_sum_to_one():
    assert sum(COST_SHARES.values()) == Decimal(1)


def test_equipment_alone_does_not_explain_high_prices():
    """The user's instinct is correct: capital equipment is a small share."""
    check = equipment_pretext_check()
    assert not check["equipment_explains_price"]
    assert check["equipment_share"] < Decimal("0.15")


def test_recurring_consumables_exceed_equipment():
    """But the real non-labour cost is recurring, not capital."""
    check = equipment_pretext_check()
    assert check["recurring_goods_exceed_equipment"]


def test_labour_is_the_largest_single_input():
    check = equipment_pretext_check()
    assert check["labour_share"] > check["consumables_share"]
    assert check["labour_share"] > check["equipment_share"]


def test_a_large_minority_of_cost_cannot_be_paid_in_credits():
    """Bounds how much of healthcare a service currency can ever finance."""
    d = cost_decomposition()
    assert d.goods_share > Decimal("0.25")
    assert d.credit_share < Decimal("0.75")


def test_credit_and_goods_shares_sum_to_one():
    d = cost_decomposition()
    assert d.credit_share + d.goods_share == Decimal(1)


# --------------------------------------------------------------------------
# Credit pools and the walking-away problem
# --------------------------------------------------------------------------


def test_pool_solvent_when_hours_exceed_claims():
    p = CreditPool(outstanding_hours=1000, practitioners=3)
    assert p.is_solvent()


def test_pool_insolvent_when_overissued():
    p = CreditPool(outstanding_hours=100_000, practitioners=1)
    assert not p.is_solvent()


def test_departure_impairs_credit_holders():
    """Unlike grain, the backing can emigrate."""
    p = CreditPool(outstanding_hours=4000, practitioners=3)
    assert p.is_solvent()
    shock = practitioner_departure_shock(p, departures=1)
    assert shock["impaired"]
    assert shock["loss_fraction"] > Decimal(0)


def test_total_departure_wipes_out_credits():
    p = CreditPool(outstanding_hours=4000, practitioners=3)
    shock = practitioner_departure_shock(p, departures=3)
    assert shock["coverage_after"] == Decimal(0)
    assert shock["loss_fraction"] == Decimal(1)


def test_attrition_reduces_multi_year_backing():
    p = CreditPool(outstanding_hours=1000, practitioners=2, attrition=0.5)
    assert p.backing_hours(3) < 2 * 1600 * 3


def test_more_practitioners_means_more_resilience():
    small = practitioner_departure_shock(CreditPool(4000, 3), 1)["loss_fraction"]
    large = practitioner_departure_shock(CreditPool(4000, 20), 1)["loss_fraction"]
    assert large < small
