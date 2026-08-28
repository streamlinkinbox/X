"""Tests for the local production ladder."""

from __future__ import annotations

import sys
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from model.rcu.production import (  # noqa: E402
    LADDER,
    RUNG_REQUIREMENTS,
    Rung,
    build_programme,
    by_rung,
    dual_use_products,
    ranked_by_payback,
    ranked_by_sovereignty,
    unviable_projects,
    viable_projects,
)


def find(name_fragment: str):
    for p in LADDER:
        if name_fragment.lower() in p.name.lower():
            return p
    raise KeyError(name_fragment)


# --------------------------------------------------------------------------
# Ladder structure
# --------------------------------------------------------------------------


def test_every_rung_has_stated_requirements():
    for r in Rung:
        assert RUNG_REQUIREMENTS[r]


def test_every_rung_has_at_least_one_candidate():
    grouped = by_rung()
    for r in Rung:
        assert grouped[r], f"rung {r} has no candidates"


def test_difficulty_increases_with_rung():
    """Higher rungs cost more capital for less achievable share."""
    grow = [p for p in LADDER if p.rung is Rung.GROW]
    precision = [p for p in LADDER if p.rung is Rung.PRECISION]
    assert min(p.capex for p in precision) > max(p.capex for p in grow)
    assert max(p.achievable_share for p in precision) < min(
        p.achievable_share for p in grow
    )


# --------------------------------------------------------------------------
# The central claim: some lethal goods ARE locally producible
# --------------------------------------------------------------------------


def test_medical_oxygen_is_locally_viable():
    """Proven at district scale in Kenya, Rwanda and Ethiopia."""
    o2 = find("oxygen")
    assert o2.lethal
    assert o2.viable
    assert o2.rung is Rung.FABRICATE


def test_oral_rehydration_salts_are_viable_and_lethal_category():
    ors = find("rehydration")
    assert ors.lethal
    assert ors.viable
    assert ors.capex < 25_000


def test_at_least_two_lethal_goods_are_locally_producible():
    """Refutes the blanket claim that lethal imports cannot be localised."""
    lethal_viable = [p for p in LADDER if p.lethal and p.viable]
    assert len(lethal_viable) >= 2


def test_api_and_vaccine_manufacture_remain_out_of_reach():
    """The honest limit stays where section 16 put it."""
    assert not find("Active pharmaceutical").viable
    assert not find("Vaccine").viable


def test_vaccines_cannot_be_made_at_all_locally():
    assert find("Vaccine").achievable_share == 0.0


# --------------------------------------------------------------------------
# Viability arithmetic
# --------------------------------------------------------------------------


def test_viability_requires_beating_operating_cost():
    """A plant that costs more to run than it saves makes things worse."""
    for p in unviable_projects():
        assert p.net_saving_per_year <= 0


def test_most_low_rung_projects_are_viable():
    low = [p for p in LADDER if p.rung <= Rung.PROCESS]
    assert sum(1 for p in low if p.viable) >= len(low) - 1


def test_all_precision_projects_are_unviable():
    for p in LADDER:
        if p.rung is Rung.PRECISION:
            assert not p.viable


def test_payback_is_infinite_for_unviable_projects():
    for p in unviable_projects():
        assert p.payback_years().is_infinite()


def test_viable_projects_have_finite_payback():
    for p in viable_projects():
        assert not p.payback_years().is_infinite()


# --------------------------------------------------------------------------
# Sovereignty weighting changes the answer
# --------------------------------------------------------------------------


def test_sovereignty_ranking_promotes_lethal_goods():
    """Weighting resilience puts life-critical production near the top."""
    top3 = ranked_by_sovereignty()[:3]
    assert any(p.lethal for p in top3)


def test_payback_ranking_alone_would_deprioritise_oxygen():
    """The tradeoff being documented: pure financial ranking buries oxygen."""
    by_money = [p.name for p in ranked_by_payback()]
    by_resilience = [p.name for p in ranked_by_sovereignty()]
    o2 = find("oxygen").name
    assert by_resilience.index(o2) < by_money.index(o2)


def test_programme_prioritising_lethal_buys_more_critical_capability():
    lethal_first = build_programme(400_000, prioritise_lethal=True)
    money_first = build_programme(400_000, prioritise_lethal=False)
    assert lethal_first.lethal_covered > money_first.lethal_covered


def test_prioritising_lethal_costs_some_financial_return():
    """Resilience is not free, and the price should be stated."""
    lethal_first = build_programme(400_000, prioritise_lethal=True)
    money_first = build_programme(400_000, prioritise_lethal=False)
    assert lethal_first.total_net_saving < money_first.total_net_saving


def test_programme_respects_budget():
    for budget in (50_000, 200_000, 400_000):
        r = build_programme(budget)
        assert r.total_capex <= budget


def test_larger_budget_buys_more_independence():
    small = build_programme(100_000).independence_gain
    large = build_programme(500_000).independence_gain
    assert large > small


def test_programme_cannot_reach_full_independence():
    r = build_programme(10_000_000)
    assert r.independence_gain < Decimal("0.90")


# --------------------------------------------------------------------------
# Dual use
# --------------------------------------------------------------------------


def test_dual_use_products_identified():
    names = [p.name.lower() for p in dual_use_products()]
    assert any("ethanol" in n for n in names)
    assert any("oxygen" in n for n in names)


def test_dual_use_products_are_viable():
    """Everyday demand keeps the plant alive until the emergency arrives."""
    for p in dual_use_products():
        assert p.viable


def test_residual_imports_are_recorded_for_critical_goods():
    """No project should claim total independence without stating its inputs."""
    for p in LADDER:
        if p.lethal and p.achievable_share > 0:
            assert p.residual_imports
