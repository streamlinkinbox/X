"""Tests for the Competence Council Governance and Departmental Policing model."""

from __future__ import annotations

import sys
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from model.rcu.governance import (  # noqa: E402
    COUNCIL_ROLES,
    DEPARTMENTAL_POLICING_SYSTEM,
    SUCCESSION_RULES,
    CandidateRecord,
    MeasurementBureau,
    QualificationPool,
    RoleDomain,
    SelectionComparison,
    SortitionAudit,
    SuccessionTrigger,
)


# --------------------------------------------------------------------------
# 1. Qualification Pool & Objective Filtering Tests
# --------------------------------------------------------------------------


def test_fully_qualified_candidate_passes():
    valid = CandidateRecord(
        candidate_id="C-001",
        age=38,
        years_community_service=12,
        apprenticeship_completed=True,
        projects_completed_count=3,
        peer_reliability_rating=Decimal("0.85"),
        has_disqualifying_failures=False,
    )
    assert valid.is_qualified


def test_underage_candidate_rejected():
    young = CandidateRecord(
        candidate_id="C-002",
        age=28,
        years_community_service=10,
        apprenticeship_completed=True,
        projects_completed_count=2,
        peer_reliability_rating=Decimal("0.90"),
        has_disqualifying_failures=False,
    )
    assert not young.is_qualified


def test_candidate_with_corruption_record_rejected():
    corrupt = CandidateRecord(
        candidate_id="C-003",
        age=45,
        years_community_service=20,
        apprenticeship_completed=True,
        projects_completed_count=5,
        peer_reliability_rating=Decimal("0.88"),
        has_disqualifying_failures=True,  # Disqualified
    )
    assert not corrupt.is_qualified


def test_candidate_with_low_peer_rating_rejected():
    unpopular_or_unreliable = CandidateRecord(
        candidate_id="C-004",
        age=40,
        years_community_service=15,
        apprenticeship_completed=True,
        projects_completed_count=4,
        peer_reliability_rating=Decimal("0.70"),  # Needs >= 0.75
        has_disqualifying_failures=False,
    )
    assert not unpopular_or_unreliable.is_qualified


def test_qualification_pool_filtering():
    pool = QualificationPool(
        candidates=(
            CandidateRecord("C-1", 35, 11, True, 2, Decimal("0.80"), False),
            CandidateRecord("C-2", 25, 4, True, 1, Decimal("0.90"), False),
            CandidateRecord("C-3", 42, 18, True, 4, Decimal("0.82"), False),
            CandidateRecord("C-4", 50, 25, True, 3, Decimal("0.60"), False),
            CandidateRecord("C-5", 39, 14, True, 2, Decimal("0.88"), True),
        )
    )
    assert pool.total_candidates == 5
    assert pool.qualified_count == 2
    assert pool.qualification_rate == Decimal("0.400")


# --------------------------------------------------------------------------
# 2. Peer Selection vs Electoral Voting Tests
# --------------------------------------------------------------------------


def test_peer_selection_competence_advantage():
    comp = SelectionComparison()
    assert comp.competence_advantage_ratio >= Decimal("1.50")
    assert comp.peer_error_rate < comp.electoral_error_rate


# --------------------------------------------------------------------------
# 3. Functional Leadership Council Roles Tests
# --------------------------------------------------------------------------


def test_all_11_council_roles_exist():
    assert len(COUNCIL_ROLES) == 11
    titles = [r.title for r in COUNCIL_ROLES]
    assert "The Coordinator" in titles
    assert "The Deputy Coordinator" in titles
    assert "The Steward of Reserves" in titles
    assert "The Steward of Production" in titles
    assert "The Steward of Knowledge" in titles
    assert "The Steward of Health" in titles
    assert "The Steward of Infrastructure" in titles
    assert "The Steward of Security" in titles
    assert "The War Council" in titles
    assert "The Steward of Justice" in titles
    assert "The Steward of Relations" in titles


def test_war_council_has_mandatory_female_representation():
    war_council = next(r for r in COUNCIL_ROLES if r.title == "The War Council")
    assert war_council.is_collective_body
    assert war_council.min_members == 5
    assert war_council.max_members == 7
    assert war_council.mandatory_female_min >= 2


def test_all_roles_have_1_year_probation_and_clear_metrics():
    for role in COUNCIL_ROLES:
        assert role.probation_years == 1
        assert len(role.key_metrics) >= 2


# --------------------------------------------------------------------------
# 4. Succession State Machine Tests
# --------------------------------------------------------------------------


def test_succession_guarantees_zero_power_vacuum():
    for trigger, proto in SUCCESSION_RULES.items():
        assert proto.power_vacuum_days == 0
        assert proto.selection_window_days <= 180


def test_deputy_assumption_on_death_or_corruption():
    death_rule = SUCCESSION_RULES[SuccessionTrigger.DEATH_OR_INCAPACITATION]
    assert "Deputy" in death_rule.immediate_successor
    assert death_rule.power_vacuum_days == 0

    corrupt_rule = SUCCESSION_RULES[SuccessionTrigger.REMOVAL_CORRUPTION]
    assert "Deputy" in corrupt_rule.immediate_successor


# --------------------------------------------------------------------------
# 5. Departmental Policing & Measurement Bureaus Tests
# --------------------------------------------------------------------------


def test_military_police_exists_with_anti_atrocity_mandate():
    defense_branch = next(
        b for b in DEPARTMENTAL_POLICING_SYSTEM if b.department == RoleDomain.DEFENSE
    )
    assert "Military Police" in defense_branch.enforcement_unit_name
    risks = [r.lower() for r in defense_branch.primary_risks_policed]
    assert any("looting" in r for r in risks)
    assert any("atrocities" in r for r in risks)
    assert any("black-market" in r or "diversion" in r for r in risks)


def test_treasury_has_warehouse_anti_hoarding_enforcers():
    treasury_branch = next(
        b for b in DEPARTMENTAL_POLICING_SYSTEM if b.department == RoleDomain.TREASURY
    )
    assert "Warehouse" in treasury_branch.enforcement_unit_name
    risks = [r.lower() for r in treasury_branch.primary_risks_policed]
    assert any("hoarding" in r or "skimming" in r for r in risks)


def test_measurement_bureau_reporting_independence():
    bureau = MeasurementBureau(total_department_staff=1000)
    assert bureau.reporting_independence
    assert bureau.dedicated_auditors_count >= 30


# --------------------------------------------------------------------------
# 6. Sortition Audit & Living Standards Tests
# --------------------------------------------------------------------------


def test_sortition_audit_parameters():
    audit = SortitionAudit()
    assert audit.jury_size == 20
    assert not audit.leader_immunity_status  # Zero immunity
    assert audit.living_condition_ratio == Decimal("1.00")  # Equal living conditions
