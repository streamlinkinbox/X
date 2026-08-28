"""Tests for Media, Information Integrity, and Social Harm Policy Framework (§25)."""

import pytest

from model.rcu.information_integrity import (
    CentralTechnicalSystemSpec,
    CommercialDeceptionSafeguards,
    ContentPolicyRule,
    ContentTier,
    CourtroomReportingPolicy,
    INVALID_STATE_FILTER,
    MEDIA_POLICY_RULES,
    MediaPluralismPolicy,
    RegulatoryInstrument,
    RestrictionStatus,
    SystemMode,
    VALID_OFFICIAL_WIRE,
)


def test_media_policy_rules_completeness():
    assert len(MEDIA_POLICY_RULES) == 10
    tiers = {r.tier for r in MEDIA_POLICY_RULES}
    assert ContentTier.TIER_A_INSTRUCTIONAL in tiers
    assert ContentTier.TIER_B_DEPICTIVE in tiers
    assert ContentTier.TIER_C_ASPIRATIONAL in tiers
    assert ContentTier.COURT_PROCEDURE in tiers
    assert ContentTier.GOVERNMENT_REPORTING in tiers
    assert ContentTier.DISTRIBUTION_INFRASTRUCTURE in tiers


def test_governing_axiom_restrict_instructional_not_depictive():
    # 1. Tier A (Instructional) MUST be restricted
    instructional_rules = [r for r in MEDIA_POLICY_RULES if r.tier == ContentTier.TIER_A_INSTRUCTIONAL]
    for r in instructional_rules:
        assert r.restriction_status == RestrictionStatus.RESTRICT

    # 2. Tier B (Depictive / Fiction) MUST NOT be restricted
    fiction_rule = next(r for r in MEDIA_POLICY_RULES if r.tier == ContentTier.TIER_B_DEPICTIVE)
    assert fiction_rule.restriction_status == RestrictionStatus.DO_NOT_RESTRICT
    assert fiction_rule.instrument == RegulatoryInstrument.AGE_CLASSIFICATION_ONLY

    # 3. Government investigative reporting MUST NEVER be restricted
    gov_rule = next(r for r in MEDIA_POLICY_RULES if r.tier == ContentTier.GOVERNMENT_REPORTING)
    assert gov_rule.restriction_status == RestrictionStatus.NEVER_RESTRICT
    assert gov_rule.instrument == RegulatoryInstrument.CONSTITUTIONAL_PROTECTION

    # 4. Distribution channels MUST NEVER be owned by a state monopoly
    dist_rule = next(r for r in MEDIA_POLICY_RULES if r.tier == ContentTier.DISTRIBUTION_INFRASTRUCTURE)
    assert dist_rule.restriction_status == RestrictionStatus.NEVER_RESTRICT
    assert dist_rule.instrument == RegulatoryInstrument.ANTI_CONCENTRATION_LAW


def test_courtroom_dignity_policy():
    policy = CourtroomReportingPolicy()
    assert policy.is_compliant_with_dignity_standard is True
    assert policy.cameras_in_courtroom_allowed is False
    assert policy.name_suspects_prior_to_conviction is False
    assert policy.name_minors_or_victims is False
    assert policy.broadcast_crime_scene_imagery is False
    assert policy.enforce_sub_judice_rules is True
    assert policy.public_open_written_registry is True
    assert policy.citizens_in_person_attendance_allowed is True

    # Violating policy: allowing cameras fails dignity standard
    corrupted_policy = CourtroomReportingPolicy(cameras_in_courtroom_allowed=True)
    assert corrupted_policy.is_compliant_with_dignity_standard is False


def test_central_system_source_vs_filter_architectural_rule():
    # Valid: central wire service that is an authoritative source without being a mandatory gate
    assert VALID_OFFICIAL_WIRE.is_constitutionally_valid is True
    assert VALID_OFFICIAL_WIRE.mode == SystemMode.AUTHORITATIVE_SOURCE
    assert VALID_OFFICIAL_WIRE.is_mandatory_gate is False

    # Invalid: unified state filter that acts as a mandatory bottleneck
    assert INVALID_STATE_FILTER.is_constitutionally_valid is False
    assert INVALID_STATE_FILTER.mode == SystemMode.EXCLUSIVE_FILTER
    assert INVALID_STATE_FILTER.is_mandatory_gate is True


def test_commercial_deception_safeguards():
    safeguards = CommercialDeceptionSafeguards()
    assert safeguards.mandatory_paid_promotion_disclosure is True
    assert safeguards.mandatory_retouched_image_labeling is True
    assert safeguards.ban_undisclosed_influencer_financial_promos is True
    assert safeguards.restrict_debt_and_credit_ads_to_minors is True
    assert safeguards.algorithmic_feed_age_gating_under_16 is True
    assert safeguards.school_media_and_financial_literacy is True


def test_media_pluralism_and_post_publication_accountability():
    pluralism = MediaPluralismPolicy()
    assert pluralism.max_single_entity_audience_share <= 0.25
    assert pluralism.mandatory_beneficial_ownership_registry is True
    assert pluralism.independent_press_council_with_statutory_backing is True
    assert pluralism.enforced_right_of_reply_and_prominent_correction is True
    assert pluralism.prior_restraint_prohibited is True
