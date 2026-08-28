"""Tests for Non-Cash Penalty and Restorative Justice System (§26)."""

import pytest

from model.rcu.penalties import (
    AntiExtortionPolicy,
    CitationDispute,
    CivicLaborType,
    ExileAssessment,
    PENALTY_TIER_ROSTER,
    PenaltyTier,
    RestitutionAccounting,
)


def test_penalty_tier_roster():
    assert len(PENALTY_TIER_ROSTER) == 4
    tiers = {t.tier for t in PENALTY_TIER_ROSTER}
    assert PenaltyTier.TIER_1_MINOR in tiers
    assert PenaltyTier.TIER_2_RECKLESS in tiers
    assert PenaltyTier.TIER_3_PREDATORY in tiers
    assert PenaltyTier.TIER_4_EXILE_EXTORTION in tiers

    tier1 = next(t for t in PENALTY_TIER_ROSTER if t.tier == PenaltyTier.TIER_1_MINOR)
    assert tier1.min_labor_hours == 4
    assert tier1.max_labor_hours == 8
    assert tier1.primary_labor_duty == CivicLaborType.SEWER_AND_DRAIN_CLEARING

    tier2 = next(t for t in PENALTY_TIER_ROSTER if t.tier == PenaltyTier.TIER_2_RECKLESS)
    assert tier2.vehicle_impound_days == 30

    tier4 = next(t for t in PENALTY_TIER_ROSTER if t.tier == PenaltyTier.TIER_4_EXILE_EXTORTION)
    assert tier4.exile_applicable is True


def test_victim_restitution_zero_police_revenue():
    damage = 500.0  # 500 RCU damage
    acc = RestitutionAccounting(damage_assessed_rcu=damage, restitution_multiplier=2.0)

    assert acc.total_restitution_paid_rcu == 1000.0
    # 100% goes directly to the victim
    assert acc.victim_allocation_rcu == 1000.0
    # Exactly 0% goes to police department or municipality slush funds
    assert acc.police_department_revenue_rcu == 0.0
    assert acc.municipal_slush_fund_allocation_rcu == 0.0


def test_anti_extortion_policy():
    policy = AntiExtortionPolicy()
    assert policy.is_anti_bribery_complete is True
    assert policy.officer_cash_possession_on_duty_is_felony is True
    assert policy.roadside_cash_collection_prohibited is True
    assert policy.digital_or_paper_citation_only is True
    assert policy.mandatory_dashcam_bodycam_evidence is True
    assert policy.reverse_bounty_on_reported_bribe_solicitation_rcu > 0
    assert policy.patrol_officer_mandatory_rotation_months == 6
    assert policy.rab_quota_hunting_anomaly_detection is True


def test_sortition_tribunal_missing_dashcam_dismissal():
    dispute = CitationDispute(
        citation_id="CIT-101",
        officer_id="OFF-44",
        citizen_id="CIT-882",
        alleged_offense="Illegal turn",
        officer_provided_dashcam_footage=False,  # Missing evidence
        citizen_appealed_within_7_days=True,
    )
    result = dispute.resolve_dispute(citizen_jury_votes_to_uphold=3)
    assert result["verdict"] == "DISMISSED_AUTOMATICALLY"
    assert result["upheld"] is False
    assert result["officer_disciplinary_flag"] is True


def test_sortition_tribunal_jury_verdict():
    dispute_with_cam = CitationDispute(
        citation_id="CIT-102",
        officer_id="OFF-44",
        citizen_id="CIT-882",
        alleged_offense="Red light violation",
        officer_provided_dashcam_footage=True,
        citizen_appealed_within_7_days=True,
    )
    # 2 of 3 votes -> UPHELD
    res_upheld = dispute_with_cam.resolve_dispute(citizen_jury_votes_to_uphold=2)
    assert res_upheld["verdict"] == "UPHELD"
    assert res_upheld["upheld"] is True

    # 1 of 3 votes -> OVERTURNED
    res_overturned = dispute_with_cam.resolve_dispute(citizen_jury_votes_to_uphold=1)
    assert res_overturned["verdict"] == "OVERTURNED"
    assert res_overturned["upheld"] is False


def test_community_exile_qualification():
    # Minor offender does not qualify
    ex_minor = ExileAssessment(
        candidate_id="OFF-01",
        offense_description="Littering and traffic violations",
        prior_unreformed_tier3_convictions=1,
        refused_mandatory_restorative_labor=False,
        is_armed_treason_or_lethal_predation=False,
        council_supermajority_approved=False,
    )
    assert ex_minor.qualifies_for_community_exile is False

    # Armed treason with Council 75% approval qualifies for Exile
    ex_treason = ExileAssessment(
        candidate_id="OFF-99",
        offense_description="Armed mutiny and warehouse sabotage",
        prior_unreformed_tier3_convictions=0,
        refused_mandatory_restorative_labor=True,
        is_armed_treason_or_lethal_predation=True,
        council_supermajority_approved=True,
    )
    assert ex_treason.qualifies_for_community_exile is True
