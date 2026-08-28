"""Tests for external trade and import-dependency management."""

from __future__ import annotations

import sys
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from model.rcu.external import (  # noqa: E402
    BASKET,
    TIME_TO_HARM_DAYS,
    DependencyTrend,
    Import,
    SovereignReserveDefense,
    Withdrawal,
    achievable_independence,
    buffer_plan,
    by_withdrawal,
    irreducible_dependency,
    lethal_share,
    minimum_exports_needed,
    substitution_ladder,
    trade_balance,
    uniform_buffer_cost,
)


# --------------------------------------------------------------------------
# Classification
# --------------------------------------------------------------------------


def test_every_import_has_a_withdrawal_class():
    for imp in BASKET:
        assert isinstance(imp.withdrawal, Withdrawal)


def test_time_to_harm_orders_correctly():
    """Lethal goods must be replaced fastest."""
    assert (
        TIME_TO_HARM_DAYS[Withdrawal.LETHAL]
        < TIME_TO_HARM_DAYS[Withdrawal.SEVERE]
        < TIME_TO_HARM_DAYS[Withdrawal.DISRUPTIVE]
        < TIME_TO_HARM_DAYS[Withdrawal.TOLERABLE]
    )


def test_lethal_imports_are_a_small_share_of_spend():
    """The key insight: what kills you is cheap. Value is the wrong metric."""
    assert lethal_share() < Decimal("0.20")


def test_withdrawal_totals_sum_to_the_bill():
    totals = by_withdrawal()
    assert sum(totals.values()) == sum(i.annual_fx_cost for i in BASKET)


# --------------------------------------------------------------------------
# Buffers
# --------------------------------------------------------------------------


def test_lethal_imports_get_the_largest_buffers_in_days():
    lethal = [i for i in BASKET if i.withdrawal is Withdrawal.LETHAL]
    tolerable = [i for i in BASKET if i.withdrawal is Withdrawal.TOLERABLE]
    assert min(i.buffer_days() for i in lethal) > max(
        i.buffer_days() for i in tolerable
    )


def test_discretionary_imports_need_no_buffer():
    """Never stockpile what you can simply do without."""
    for imp in BASKET:
        if imp.withdrawal is Withdrawal.TOLERABLE:
            assert imp.buffer_days() == 0.0
            assert imp.buffer_cost() == 0.0


def test_targeted_buffer_is_cheaper_than_uniform_stockpiling():
    """Severity-weighted buffers beat holding three months of everything."""
    assert buffer_plan().total_cost < uniform_buffer_cost(months=3)


def test_targeted_buffer_still_protects_lethal_items_longer():
    plan = buffer_plan()
    lethal = [i for i in BASKET if i.withdrawal is Withdrawal.LETHAL]
    for imp in lethal:
        assert imp.buffer_days() > 90


def test_faster_resupply_reduces_buffer_need():
    slow = buffer_plan(resupply_days=180).total_cost
    fast = buffer_plan(resupply_days=30).total_cost
    assert fast < slow


def test_buffer_cost_is_never_negative():
    for imp in BASKET:
        assert imp.buffer_cost() >= 0


# --------------------------------------------------------------------------
# Trade balance and triage
# --------------------------------------------------------------------------


def test_weak_exports_cannot_cover_critical_imports():
    tb = trade_balance(50_000)
    assert not tb.covers_critical
    assert tb.discretionary_headroom < 0


def test_adequate_exports_cover_critical_but_not_everything():
    tb = trade_balance(minimum_exports_needed())
    assert tb.covers_critical
    assert not tb.covers_all


def test_headroom_is_what_may_be_spent_on_discretionary():
    tb = trade_balance(400_000)
    assert tb.discretionary_headroom > 0
    assert tb.covers_critical


def test_critical_excludes_discretionary_goods():
    """Triage: clothing must never compete with insulin for scarce FX."""
    critical = minimum_exports_needed()
    total = sum(i.annual_fx_cost for i in BASKET)
    assert critical < total


# --------------------------------------------------------------------------
# Substitution
# --------------------------------------------------------------------------


def test_medicines_are_the_worst_substitution_value():
    """Counterintuitive but decisive: what matters most localises worst."""
    ladder = substitution_ladder()
    worst = [imp for imp, eff, pb in ladder if eff == 0 or pb.is_infinite()]
    names = [i.name for i in worst]
    assert any("Vaccine" in n for n in names)


def test_food_and_fertiliser_are_the_best_substitution_value():
    ladder = substitution_ladder()
    top_two = [imp.name for imp, _, _ in ladder[:3]]
    assert any("food" in n.lower() for n in top_two)
    assert any("fertiliser" in n.lower() for n in top_two)


def test_full_independence_is_not_achievable():
    """The honest ceiling. Autarky is not on the menu."""
    assert achievable_independence() < Decimal("0.70")


def test_irreducible_dependency_is_material():
    assert irreducible_dependency() > 0


def test_lethal_imports_dominate_irreducible_dependency():
    """What cannot be localised is disproportionately what you cannot skip."""
    lethal_residual = sum(
        i.residual_dependency for i in BASKET if i.withdrawal is Withdrawal.LETHAL
    )
    lethal_spend = sum(
        i.annual_fx_cost for i in BASKET if i.withdrawal is Withdrawal.LETHAL
    )
    # Almost none of the lethal basket can be localised.
    assert lethal_residual / lethal_spend > 0.85


def test_substitution_never_exceeds_full_replacement():
    for imp in BASKET:
        assert 0.0 <= imp.local_substitutable_potential <= 1.0
        assert imp.local_substitutable_now <= imp.local_substitutable_potential


# --------------------------------------------------------------------------
# The dependency ratchet
# --------------------------------------------------------------------------


def test_trend_detects_worsening_dependency():
    d = DependencyTrend()
    for y, i, e in ((1, 300_000, 320_000), (2, 340_000, 330_000), (3, 465_000, 350_000)):
        d.add(y, i, e)
    assert d.worsening()
    assert d.alarm()


def test_trend_detects_improving_self_reliance():
    d = DependencyTrend()
    for y, i, e in ((1, 400_000, 300_000), (2, 350_000, 340_000), (3, 300_000, 400_000)):
        d.add(y, i, e)
    assert not d.worsening()
    assert not d.alarm()


def test_alarm_triggers_below_parity():
    d = DependencyTrend()
    d.add(1, 100_000, 90_000)
    assert d.alarm()


def test_empty_trend_is_safe():
    d = DependencyTrend()
    assert not d.worsening()
    assert not d.alarm()


# --------------------------------------------------------------------------
# Sovereign Reserve Defense & Extortion Neutralization
# --------------------------------------------------------------------------


def test_sovereign_reserve_defense_counter_offensive():
    defense = SovereignReserveDefense(
        frozen_foreign_reserves_rcu=1_000_000_000.0,
        hostile_foreign_corporate_assets_inside_borders_rcu=1_200_000_000.0,
        sovereign_debt_owed_to_hostile_jurisdiction_rcu=800_000_000.0,
        bilateral_commodity_clearing_share_pct=0.95,
        onshore_physical_gold_and_commodity_share_pct=1.0,
        sovereign_payment_switch_active=True,
    )
    res = defense.execute_counter_offensive()

    assert res["frozen_foreign_reserves_rcu"] == 1_000_000_000.0
    assert res["sovereign_debt_cancelled_rcu"] == 800_000_000.0
    assert res["corporate_assets_seized_into_escrow_rcu"] == 200_000_000.0
    assert res["total_sovereign_recovery_value_rcu"] == 1_000_000_000.0
    assert res["net_leverage_ratio"] == 1.0
    assert res["bilateral_clearing_sanctions_immune"] is True
    assert res["domestic_payment_switch_immune"] is True
    assert res["financial_blackmail_neutralized"] is True

