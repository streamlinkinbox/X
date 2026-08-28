"""Tests for the valuation engine.

The invariants tested here are the ones that, if violated, cause money to be
created or destroyed incorrectly. They are deliberately paranoid.
"""

from __future__ import annotations

import sys
from datetime import date
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest  # noqa: E402

from model.rcu.classes import REGISTER, TIER_A, TIER_B, Tier, get  # noqa: E402
from model.rcu.stress import (  # noqa: E402
    harvest_cycle,
    price_crash,
    redemption_run,
    survivable_crash,
)
from model.rcu.valuation import (  # noqa: E402
    Note,
    collateral_ratio,
    decay_multiplier,
    issue_value_cents,
    months_elapsed,
)


def mknote(code: str, face: int = 100_000, issued: date = date(2027, 1, 1)) -> Note:
    return Note(
        serial=f"{code}-TEST",
        class_code=code,
        face_cents=face,
        issued=issued,
        issuer_id="COOP-TEST",
        warehouse_id="WH-TEST",
    )


# --------------------------------------------------------------------------
# Register integrity
# --------------------------------------------------------------------------


def test_register_has_twenty_classes():
    assert len(REGISTER) == 20


def test_class_numbers_are_unique_and_sequential():
    assert sorted(c.number for c in REGISTER) == list(range(1, 21))


def test_class_codes_are_unique():
    codes = [c.code for c in REGISTER]
    assert len(set(codes)) == len(codes)


def test_tiers_partition_the_register():
    assert len(TIER_A) + len(TIER_B) == len(REGISTER)
    assert all(c.tier is Tier.A for c in TIER_A)
    assert all(c.tier is Tier.B for c in TIER_B)


def test_lookup_by_code_and_number():
    assert get("GR") is get(1)
    assert get("gr").name == "Grains & Cereals"


@pytest.mark.parametrize("c", REGISTER, ids=lambda c: c.code)
def test_parameters_are_in_sane_ranges(c):
    assert 0.0 <= c.decay_rate < 1.0
    assert 0.0 <= c.haircut < 1.0
    assert 0.0 <= c.storage_cost_pa < 1.0
    assert c.grace_months >= 0
    if c.max_validity_months is not None:
        assert c.max_validity_months > c.grace_months


# --------------------------------------------------------------------------
# Date arithmetic
# --------------------------------------------------------------------------


def test_months_elapsed_basic():
    assert months_elapsed(date(2027, 1, 1), date(2027, 1, 1)) == 0
    assert months_elapsed(date(2027, 1, 1), date(2027, 1, 31)) == 0
    assert months_elapsed(date(2027, 1, 1), date(2027, 2, 1)) == 1
    assert months_elapsed(date(2027, 1, 1), date(2028, 1, 1)) == 12


def test_months_elapsed_handles_short_months():
    # Issued on the 31st; February has no 31st. Must not overcount.
    assert months_elapsed(date(2027, 1, 31), date(2027, 2, 28)) == 0
    assert months_elapsed(date(2027, 1, 31), date(2027, 3, 31)) == 2


def test_months_elapsed_never_negative():
    assert months_elapsed(date(2027, 6, 1), date(2027, 1, 1)) == 0


# --------------------------------------------------------------------------
# Decay
# --------------------------------------------------------------------------


def test_no_decay_during_grace():
    n = mknote("GR")
    cls = get("GR")
    for m in range(cls.grace_months + 1):
        assert decay_multiplier(cls, m) == Decimal(1)


def test_decay_starts_after_grace():
    cls = get("GR")
    assert decay_multiplier(cls, cls.grace_months) == Decimal(1)
    assert decay_multiplier(cls, cls.grace_months + 1) < Decimal(1)


def test_decay_is_monotonically_non_increasing():
    for cls in REGISTER:
        prev = Decimal(1)
        for m in range(0, 130):
            cur = decay_multiplier(cls, m)
            assert cur <= prev, f"{cls.code} increased at month {m}"
            prev = cur


def test_stable_classes_never_decay():
    for cls in TIER_B:
        if cls.decay_rate == 0.0:
            for m in range(0, 240, 12):
                assert decay_multiplier(cls, m) == Decimal(1)


def test_grain_decay_matches_hand_calculation():
    # 2%/month after 6 months grace; at month 12 that is 6 decay steps.
    n = mknote("GR", face=100_000)
    expected = int(Decimal(100_000) * (Decimal("0.98") ** 6))
    assert abs(n.value_cents(date(2028, 1, 1)) - expected) <= 1


def test_annual_rate_classes_step_yearly_not_monthly():
    cls = get("SC")  # 0.5%/yr after 12 months grace
    assert decay_multiplier(cls, 12) == Decimal(1)
    assert decay_multiplier(cls, 23) == Decimal(1)  # not yet a full year of decay
    assert decay_multiplier(cls, 24) < Decimal(1)


# --------------------------------------------------------------------------
# Expiry
# --------------------------------------------------------------------------


def test_expired_note_is_worthless():
    n = mknote("FP")  # 6 month validity
    assert n.value_cents(date(2027, 8, 1)) == 0
    assert n.is_expired(date(2027, 8, 1))


def test_stable_notes_do_not_expire():
    n = mknote("FE")
    assert not n.is_expired(date(2099, 1, 1))
    assert n.value_cents(date(2099, 1, 1)) == 100_000


def test_value_never_exceeds_face():
    for cls in REGISTER:
        n = mknote(cls.code)
        for m in range(0, 130):
            sched = dict(n.schedule(130))
            assert sched[m] <= n.face_cents


def test_value_never_negative():
    for cls in REGISTER:
        n = mknote(cls.code)
        for _, v in n.schedule(130):
            assert v >= 0


# --------------------------------------------------------------------------
# Determinism -- the settlement-critical property
# --------------------------------------------------------------------------


def test_valuation_is_deterministic():
    n = mknote("GR")
    d = date(2028, 3, 15)
    results = {n.value_cents(d) for _ in range(1000)}
    assert len(results) == 1


def test_valuation_is_integer_cents():
    n = mknote("GR", face=99_999)
    for m in range(0, 30):
        sched = dict(n.schedule(30))
        assert isinstance(sched[m], int)


def test_odd_face_values_do_not_leak_value():
    """Rounding must not create value out of nothing."""
    for face in (1, 7, 33, 101, 999, 100_001):
        n = mknote("GR", face=face)
        for _, v in n.schedule(30):
            assert v <= face


# --------------------------------------------------------------------------
# Issuance
# --------------------------------------------------------------------------


def test_haircut_reduces_issuance():
    cls = get("GR")
    assert issue_value_cents(1_000_000, cls) == 700_000


def test_issuance_never_exceeds_assessed_value():
    for cls in REGISTER:
        assert issue_value_cents(1_000_000, cls) <= 1_000_000


def test_collateral_ratio():
    assert collateral_ratio(700_000, 1_000_000) > Decimal(1)
    assert collateral_ratio(1_000_000, 700_000) < Decimal(1)


# --------------------------------------------------------------------------
# Stress tests -- these encode the document's central claims
# --------------------------------------------------------------------------


def test_harvest_cycle_stays_solvent():
    r = harvest_cycle("GR", horizon=48)
    assert not r.breached(1.0), "grain cooperative went undercollateralised"


def test_harvest_cycle_shows_seasonal_swing():
    """The money supply sawtooth documented in section 1.5 must be real."""
    r = harvest_cycle("GR", horizon=48)
    assert min(r.outstanding) == 0
    assert max(r.outstanding) > 0


def test_price_crash_within_haircut_is_survivable():
    r = price_crash("GR", crash_pct=0.10)
    assert not r.breached(1.0)


def test_price_crash_beyond_haircut_breaks_collateral():
    r = price_crash("GR", crash_pct=0.60)
    assert r.breached(1.0)


def test_precious_metals_is_under_haircut():
    """Documented finding: PM survives less than its own annual volatility."""
    cls = get("PM")
    assert survivable_crash("PM") < cls.price_volatility_pa


def test_thin_classes_cannot_honour_a_large_run():
    assert redemption_run("ST", presented_fraction=0.30).gate_triggered
    assert redemption_run("SM", presented_fraction=0.30).gate_triggered


def test_deep_classes_can_honour_a_moderate_run():
    assert not redemption_run("PM", presented_fraction=0.30).gate_triggered
    assert not redemption_run("GR", presented_fraction=0.30).gate_triggered


def test_redemption_run_honoured_fraction_is_bounded():
    for cls in REGISTER:
        rr = redemption_run(cls.code, presented_fraction=0.50)
        assert 0.0 <= rr.honoured_fraction <= 1.0


# --------------------------------------------------------------------------
# Documented economic claims
# --------------------------------------------------------------------------


def test_tier_b_classes_need_a_custody_fee():
    """Section 1.2: stability is not free."""
    uncovered = [c for c in REGISTER if not c.carry_covered]
    assert len(uncovered) == 9
    assert all(c.tier is Tier.B for c in uncovered)


def test_all_tier_a_demurrage_covers_storage():
    for c in TIER_A:
        assert c.carry_covered, f"{c.code} demurrage does not cover storage"


def test_lifetime_decay_is_material_for_tier_a():
    """If holding to expiry costs nothing, the incentive does not exist."""
    for c in TIER_A:
        assert c.lifetime_decay > 0.15, f"{c.code} decay too weak to deter hoarding"
