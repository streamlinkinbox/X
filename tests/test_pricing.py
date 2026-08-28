"""Tests for bundle pricing, dual-price receipts and settlement."""

from __future__ import annotations

import sys
from datetime import date
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest  # noqa: E402

from model.rcu.classes import TIER_A, TIER_B, Tier, get  # noqa: E402
from model.rcu.hoarding import (  # noqa: E402
    minimum_tier_a_share_for_fairness,
    simulate,
)
from model.rcu.pricing import (  # noqa: E402
    Receipt,
    bundle_face_cents,
    bundle_tier_split,
    settle,
)
from model.rcu.valuation import CENTS, Note  # noqa: E402

HOUSE = Receipt(
    item="House, 3 rooms",
    asked={"FE": 100, "WD": 500, "PL": 40},
    reference={"FE": 20, "WD": 200, "PL": 5},
    quoted_on=date(2027, 3, 1),
)


# --------------------------------------------------------------------------
# Bundles
# --------------------------------------------------------------------------


def test_bundle_face_value():
    assert bundle_face_cents({"FE": 100, "WD": 500}) == 600 * CENTS


def test_bundle_tier_split_sums_to_one():
    a, b = bundle_tier_split({"FE": 100, "WD": 500, "PL": 40})
    assert a + b == Decimal(1)


def test_bundle_tier_split_identifies_decaying_share():
    # WD and PL are Tier A, FE is Tier B -> 540 of 640 decays.
    a, b = bundle_tier_split({"FE": 100, "WD": 500, "PL": 40})
    assert a == Decimal("0.8438")


def test_empty_bundle_is_safe():
    assert bundle_face_cents({}) == 0
    assert bundle_tier_split({}) == (Decimal(0), Decimal(0))


# --------------------------------------------------------------------------
# The dual-price receipt
# --------------------------------------------------------------------------


def test_markup_matches_hand_calculation():
    # asked 640, reference 225 -> 415/225
    assert HOUSE.asked_cents == 640 * CENTS
    assert HOUSE.reference_cents == 225 * CENTS
    assert HOUSE.markup == Decimal("1.8444")


def test_per_class_markup_exposes_where_the_margin_sits():
    m = HOUSE.markup_by_class
    assert m["FE"] == Decimal(4)     # 100 vs 20
    assert m["WD"] == Decimal("1.5")  # 500 vs 200
    assert m["PL"] == Decimal(7)     # 40 vs 5


def test_fair_price_is_labelled_fair():
    r = Receipt("maize", {"GR": 10}, {"GR": 10}, date(2027, 1, 1))
    assert r.markup == Decimal(0)
    assert "at or below" in r.fairness


def test_extreme_markup_warns():
    assert "very high" in HOUSE.fairness


def test_below_reference_price_is_negative_markup():
    r = Receipt("maize", {"GR": 8}, {"GR": 10}, date(2027, 1, 1))
    assert r.markup < 0
    assert "at or below" in r.fairness


def test_zero_reference_does_not_crash():
    r = Receipt("gift", {"GR": 5}, {}, date(2027, 1, 1))
    assert r.markup == Decimal(0)
    assert r.markup_by_class["GR"].is_infinite()


def test_receipt_renders_without_error():
    out = HOUSE.render()
    assert "MARKUP" in out
    assert "decays" in out and "stable" in out
    # every line must be the same width -- it gets printed on paper
    widths = {len(line) for line in out.splitlines()}
    assert len(widths) == 1


# --------------------------------------------------------------------------
# Seller's cost of waiting
# --------------------------------------------------------------------------


def test_decaying_bundle_loses_value_if_unsold():
    sched = HOUSE.holding_cost_schedule(24)
    assert sched[0][2] == Decimal(1)
    assert sched[-1][2] < Decimal(1)


def test_stable_bundle_holds_value():
    r = Receipt("scrap", {"FE": 100}, {"FE": 100}, date(2027, 1, 1))
    sched = r.holding_cost_schedule(24)
    assert all(f == Decimal(1) for _, _, f in sched)


def test_perishable_bundle_decays_fast():
    r = Receipt("tomatoes", {"FP": 20}, {"FP": 20}, date(2027, 1, 1))
    sched = r.holding_cost_schedule(6)
    assert sched[-1][2] < Decimal("0.9")


# --------------------------------------------------------------------------
# Settlement: quote in face, settle in value
# --------------------------------------------------------------------------


def mknote(code: str, face_units: int, issued: date) -> Note:
    return Note(f"{code}-T", code, face_units * CENTS, issued, "C", "W")


def test_fresh_notes_settle_exactly():
    s = settle({"WD": 500}, [mknote("WD", 500, date(2027, 3, 1))], date(2027, 3, 1))
    assert s.settled
    assert s.total_shortfall == 0


def test_aged_notes_leave_a_shortfall():
    """The core mechanism: old notes buy less."""
    s = settle({"WD": 500}, [mknote("WD", 500, date(2025, 9, 1))], date(2027, 3, 1))
    assert not s.settled
    assert s.total_shortfall > 0


def test_buyer_must_tender_more_face_when_notes_are_old():
    old = date(2025, 9, 1)
    need = 500
    tendered = 0
    notes = []
    while True:
        notes = [mknote("WD", tendered, old)] if tendered else []
        if settle({"WD": need}, notes, date(2027, 3, 1)).settled:
            break
        tendered += 1
        assert tendered < 2000
    assert tendered > need  # strictly more face value required


def test_stable_notes_settle_regardless_of_age():
    s = settle({"FE": 100}, [mknote("FE", 100, date(2020, 1, 1))], date(2027, 3, 1))
    assert s.settled


def test_wrong_class_does_not_satisfy_a_bundle():
    """A hoarder cannot pay a wood demand with iron notes."""
    s = settle({"WD": 500}, [mknote("FE", 500, date(2027, 3, 1))], date(2027, 3, 1))
    assert not s.settled
    assert s.shortfall_cents["WD"] == 500 * CENTS


def test_surplus_is_reported():
    s = settle({"WD": 100}, [mknote("WD", 150, date(2027, 3, 1))], date(2027, 3, 1))
    assert s.settled
    assert s.surplus_cents["WD"] > 0


# --------------------------------------------------------------------------
# P1: does bundle pricing defeat demurrage arbitrage?
# --------------------------------------------------------------------------


def test_free_substitution_reproduces_the_p1_inversion():
    """Without bundle pricing, the naive holder bears far more demurrage."""
    r = simulate(strict=False, months=24, tier_a_demand_share=0.5)
    assert r.loss_ratio > 1.5


def test_strict_bundles_equalise_the_burden():
    """With bundle pricing, both agents bear demurrage equally."""
    r = simulate(strict=True, months=24, tier_a_demand_share=0.5)
    assert r.loss_ratio == pytest.approx(1.0, abs=0.05)


def test_strict_bundles_beat_free_substitution_across_demand_mixes():
    for share in (0.3, 0.5, 0.7):
        strict = simulate(strict=True, tier_a_demand_share=share)
        free = simulate(strict=False, tier_a_demand_share=share)
        assert strict.loss_ratio <= free.loss_ratio


def test_bundle_pricing_makes_sophistication_worthless():
    """The sophisticated agent's advantage should vanish under strict rules."""
    r = simulate(strict=True, months=24)
    assert r.sophisticated_loss == pytest.approx(r.naive_loss, rel=0.05)


def test_fairness_threshold_is_reachable():
    assert minimum_tier_a_share_for_fairness() <= 0.5
