"""Tests for the community security model."""

from __future__ import annotations

import sys
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from model.rcu.security import (  # noqa: E402
    ArmouryPolicy,
    CaptureModel,
    audit_effort_curve,
    collusion_sensitivity,
    detection,
    max_safe_rotation,
    rotation_grid,
    workload,
)


# --------------------------------------------------------------------------
# Workload: what security work actually is
# --------------------------------------------------------------------------


def test_mediation_dominates_the_workload():
    """The central claim: most security work is dispute resolution."""
    w = workload(1000)
    assert w.mediation_share > Decimal("0.50")


def test_force_is_a_minority_of_the_work():
    w = workload(1000)
    assert w.force_share < Decimal("0.30")


def test_forensics_is_a_material_share():
    """Currency fraud investigation is a real, sizeable function."""
    w = workload(1000)
    assert w.forensic_share > Decimal("0.10")


def test_shares_sum_to_one():
    w = workload(1000)
    total = w.mediation_share + w.forensic_share + w.force_share
    assert abs(total - Decimal(1)) < Decimal("0.01")


def test_workload_scales_with_population():
    assert workload(3000).total_hours > workload(1000).total_hours


def test_roster_is_set_by_coverage_not_caseload_in_small_communities():
    """A tiny village still needs people on call, however few incidents."""
    small = workload(300)
    assert small.members_needed() >= 5


def test_roster_grows_for_large_communities():
    assert workload(20_000).members_needed() > workload(1000).members_needed()


# --------------------------------------------------------------------------
# Fraud detection
# --------------------------------------------------------------------------


def test_dual_inspection_beats_single():
    assert detection(dual_inspection=True).detection_rate > detection(
        dual_inspection=False
    ).detection_rate


def test_layered_detection_is_good_but_not_perfect():
    d = detection()
    assert Decimal("0.75") < d.detection_rate < Decimal("0.95")


def test_some_fraud_always_escapes():
    """Design for a residual fraud rate rather than assuming zero."""
    assert detection().undetected > 0


def test_collusion_destroys_dual_inspection():
    """Two inspectors are only as good as their independence."""
    curve = dict(collusion_sensitivity())
    assert curve[0.0] > curve[1.0]
    assert curve[1.0] < Decimal("0.40")


def test_full_collusion_leaves_only_audit_and_consumer_layers():
    d = detection(collusion_rate=1.0)
    assert d.caught_at_deposit == 0
    assert d.caught_at_audit > 0 or d.caught_by_consumer > 0


def test_more_auditing_improves_detection():
    curve = dict(audit_effort_curve())
    assert curve[0.40] > curve[0.0]


def test_audit_has_diminishing_returns():
    """Doubling audit effort does not double detection."""
    curve = dict(audit_effort_curve())
    first = curve[0.10] - curve[0.05]
    second = curve[0.20] - curve[0.10]
    assert second < first * Decimal("2.5")


# --------------------------------------------------------------------------
# Capture resistance
# --------------------------------------------------------------------------


def test_short_tours_resist_capture():
    assert not CaptureModel(rotation_months=6, break_months=18).captured


def test_long_tours_lead_to_capture():
    assert CaptureModel(rotation_months=36, break_months=12).captured


def test_longer_breaks_protect_against_capture():
    short_break = CaptureModel(rotation_months=18, break_months=12).captured
    long_break = CaptureModel(rotation_months=18, break_months=18).captured
    assert short_break and not long_break


def test_max_safe_rotation_is_around_a_year_and_a_half():
    assert 6 <= max_safe_rotation() <= 24


def test_rotation_grid_covers_both_outcomes():
    results = [captured for _, _, captured, _ in rotation_grid()]
    assert any(results) and not all(results)


def test_capture_is_monotonic_in_tour_length():
    peaks = [
        CaptureModel(rotation_months=t, break_months=12).peak_influence
        for t in (6, 12, 24, 36)
    ]
    assert peaks == sorted(peaks)


# --------------------------------------------------------------------------
# Armoury
# --------------------------------------------------------------------------


def test_quorum_must_exceed_plausible_corrupt_count():
    """2-of-5 fails completely if two keyholders collude."""
    weak = ArmouryPolicy(keyholders=5, quorum=2, corrupt_count=2)
    assert weak.unauthorised_release_probability == Decimal(1)
    assert not weak.acceptable


def test_raising_quorum_above_corrupt_count_restores_control():
    strong = ArmouryPolicy(keyholders=7, quorum=3, corrupt_count=2)
    assert strong.unauthorised_release_probability < Decimal(1)


def test_larger_quorum_is_safer():
    a = ArmouryPolicy(keyholders=9, quorum=2, corrupt_count=1)
    b = ArmouryPolicy(keyholders=9, quorum=4, corrupt_count=1)
    assert b.unauthorised_release_probability < a.unauthorised_release_probability


def test_no_corruption_still_requires_deceiving_honest_holders():
    clean = ArmouryPolicy(keyholders=5, quorum=2, corrupt_count=0)
    assert clean.unauthorised_release_probability < Decimal("0.01")
