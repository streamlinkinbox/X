"""Tests for weight denomination, quality adjustment and provenance."""

from __future__ import annotations

import sys
from datetime import date
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest  # noqa: E402

from model.rcu.classes import REGISTER, get  # noqa: E402
from model.rcu.units import (  # noqa: E402
    GRADE_FACTOR,
    PHYSICAL_HAIRCUT,
    UNIT_DEFINITION,
    Provenance,
    TradeBook,
    TradeObservation,
    UnitBasis,
    effective_age_months,
    exchange_rate_count,
    issuable_units,
    numeraire_saving,
    quality_adjusted_grams,
    ranked_numeraires,
)


# --------------------------------------------------------------------------
# Unit definitions
# --------------------------------------------------------------------------


def test_every_class_has_a_unit_definition():
    for c in REGISTER:
        assert c.code in UNIT_DEFINITION


def test_fresh_produce_is_not_monetisable():
    basis, _ = UNIT_DEFINITION["FP"]
    assert basis == UnitBasis.NOT_MONETISABLE


def test_most_classes_are_weight_based():
    weight = sum(
        1 for c in REGISTER if UNIT_DEFINITION[c.code][0] == UnitBasis.WEIGHT
    )
    assert weight >= 14


# --------------------------------------------------------------------------
# Quality adjustment
# --------------------------------------------------------------------------


def test_grade_a_at_reference_moisture_is_unadjusted():
    assert quality_adjusted_grams(1_000_000, "A", Decimal("13.5")) == 1_000_000


def test_lower_grade_yields_fewer_units():
    a = quality_adjusted_grams(1_000_000, "A")
    b = quality_adjusted_grams(1_000_000, "B")
    c = quality_adjusted_grams(1_000_000, "C")
    assert a > b > c


def test_reject_grade_yields_nothing():
    assert quality_adjusted_grams(1_000_000, "REJECT") == 0


def test_unknown_grade_is_treated_as_reject():
    assert quality_adjusted_grams(1_000_000, "Z") == 0


def test_wet_grain_yields_fewer_units_than_dry():
    """Water is not the commodity."""
    dry = quality_adjusted_grams(1_000_000, "A", Decimal("13.5"))
    wet = quality_adjusted_grams(1_000_000, "A", Decimal("18.0"))
    assert wet < dry


def test_drier_than_reference_yields_more():
    assert quality_adjusted_grams(
        1_000_000, "A", Decimal("10.0")
    ) > quality_adjusted_grams(1_000_000, "A", Decimal("13.5"))


def test_quality_adjustment_rounds_down():
    """The system must never promise more than it holds."""
    assert quality_adjusted_grams(999, "C") <= int(999 * 0.65)


# --------------------------------------------------------------------------
# Issuance
# --------------------------------------------------------------------------


def test_issuance_is_below_deposit_weight():
    for c in REGISTER:
        assert issuable_units(1_000_000, c, "A") < 1_000_000


def test_non_monetisable_class_falls_back_to_a_conservative_haircut():
    """Even if FP were issued by mistake, it must not over-issue."""
    assert issuable_units(1_000_000, get("FP"), "A") <= 900_000


MONETISABLE = [
    c for c in REGISTER
    if UNIT_DEFINITION[c.code][0] != UnitBasis.NOT_MONETISABLE
]


def test_non_monetisable_classes_have_no_haircut():
    """Fresh produce is excluded outright rather than given a huge haircut."""
    assert "FP" not in PHYSICAL_HAIRCUT


def test_physical_haircuts_are_smaller_than_price_haircuts():
    """The central claim: weight denomination removes price risk."""
    for c in MONETISABLE:
        assert PHYSICAL_HAIRCUT[c.code] < Decimal(str(c.haircut))


def test_average_haircut_falls_substantially():
    old = sum(Decimal(str(c.haircut)) for c in MONETISABLE) / len(MONETISABLE)
    new = sum(PHYSICAL_HAIRCUT[c.code] for c in MONETISABLE) / len(MONETISABLE)
    assert old > Decimal("0.29")
    assert new < Decimal("0.08")


def test_precious_metals_has_the_smallest_physical_haircut():
    assert PHYSICAL_HAIRCUT["PM"] == min(PHYSICAL_HAIRCUT.values())


def test_grade_and_moisture_compound():
    full = issuable_units(1_000_000, get("GR"), "A", Decimal("13.5"))
    poor = issuable_units(1_000_000, get("GR"), "C", Decimal("16.0"))
    assert poor < full * 0.7


# --------------------------------------------------------------------------
# Provenance
# --------------------------------------------------------------------------


def test_pre_deposit_age_is_measured():
    p = Provenance(date(2027, 1, 15), date(2027, 8, 15), "P1", "Kigoma")
    assert p.pre_deposit_age_months() == 7


def test_stale_deposit_is_flagged():
    """Grain stored privately for 7 months has used up its grace period."""
    p = Provenance(date(2027, 1, 15), date(2027, 8, 15), "P1", "Kigoma")
    assert p.is_stale_on_deposit(get("GR"))


def test_fresh_deposit_is_not_stale():
    p = Provenance(date(2027, 1, 15), date(2027, 2, 15), "P1", "Kigoma")
    assert not p.is_stale_on_deposit(get("GR"))


def test_stable_classes_are_never_stale():
    p = Provenance(date(2000, 1, 1), date(2027, 1, 1), "P1", "mine")
    assert not p.is_stale_on_deposit(get("FE"))


def test_decay_clock_runs_from_origin_not_deposit():
    """The anti-gaming property: private storage does not reset the clock."""
    p = Provenance(date(2027, 1, 15), date(2027, 8, 15), "P1", "Kigoma")
    assert effective_age_months(p, date(2028, 1, 15)) == 12


# --------------------------------------------------------------------------
# The cost of no numeraire
# --------------------------------------------------------------------------


def test_bilateral_rate_count_is_quadratic():
    assert exchange_rate_count(4, numeraire=False) == 6
    assert exchange_rate_count(20, numeraire=False) == 190


def test_numeraire_makes_it_linear():
    assert exchange_rate_count(20, numeraire=True) == 19


def test_numeraire_saving_grows_with_market_size():
    _, _, small = numeraire_saving(4)
    _, _, large = numeraire_saving(50)
    assert large > small > 1


def test_a_stable_liquid_class_wins_the_numeraire_race():
    top = ranked_numeraires()[0][0]
    assert top.tier.value == "B"
    assert top.code in {"PM", "FE", "CU"}


def test_decaying_classes_rank_poorly_as_numeraire():
    ranked = {c.code: s for c, s in ranked_numeraires()}
    assert ranked["PM"] > ranked["GR"]
    assert ranked["FE"] > ranked["FP"]


# --------------------------------------------------------------------------
# Trade book: observation, not assessment
# --------------------------------------------------------------------------


def test_empty_trade_book_reports_no_data():
    tb = TradeBook()
    s = tb.summary("GR", "FE")
    assert s["n"] == 0
    assert s["confidence"] == "no data"


def test_trade_book_records_and_summarises():
    tb = TradeBook()
    for got in (9, 10, 11):
        tb.add(TradeObservation("GR", 100, "FE", got, date(2027, 5, 1)))
    s = tb.summary("GR", "FE")
    assert s["n"] == 3
    assert s["confidence"] == "medium"
    assert s["median"] == Decimal("0.1000")


def test_trade_book_inverts_reverse_trades():
    tb = TradeBook()
    tb.add(TradeObservation("GR", 100, "FE", 10, date(2027, 5, 1)))
    tb.add(TradeObservation("FE", 10, "GR", 100, date(2027, 5, 2)))
    rates = tb.between("GR", "FE")
    assert len(rates) == 2
    assert rates[0] == rates[1]


def test_confidence_rises_with_observations():
    tb = TradeBook()
    for i in range(10):
        tb.add(TradeObservation("GR", 100, "FE", 10, date(2027, 5, 1)))
    assert tb.summary("GR", "FE")["confidence"] == "high"


def test_spread_is_reported_so_buyers_see_dispersion():
    tb = TradeBook()
    tb.add(TradeObservation("GR", 100, "FE", 5, date(2027, 5, 1)))
    tb.add(TradeObservation("GR", 100, "FE", 15, date(2027, 5, 1)))
    tb.add(TradeObservation("GR", 100, "FE", 10, date(2027, 5, 1)))
    s = tb.summary("GR", "FE")
    assert s["low"] == Decimal("0.0500")
    assert s["high"] == Decimal("0.1500")
    assert s["spread"] == Decimal("0.1000")
