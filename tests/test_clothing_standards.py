"""Tests for Public Clothing Standards and Exposure Thresholds (§28)."""

import pytest

from model.rcu.clothing_standards import (
    AntiHumiliationPolicy,
    ClothingComplianceSimulation,
    DressTierCategory,
    EnforcementEncounter,
    PUBLIC_SECTOR_DRESS_TIERS,
    PublicSectorDressTier,
    SovereigntyDesignRule,
    SovereignMethodology,
    SPATIAL_ZONE_SPECS,
    SpatialZone,
    UniformProcurementPolicy,
)


def test_spatial_zones_coverage():
    assert len(SPATIAL_ZONE_SPECS) == 3
    zones = {s.zone for s in SPATIAL_ZONE_SPECS}
    assert SpatialZone.ZONE_1_STRICT in zones
    assert SpatialZone.ZONE_2_STANDARD in zones
    assert SpatialZone.ZONE_3_RELAXED in zones


def test_remedy_before_penalty_garment_acceptance():
    encounter = EnforcementEncounter(
        encounter_id="ENC-001",
        citizen_gender="female",
        spatial_zone=SpatialZone.ZONE_2_STANDARD,
        officer_gender="female",
        garment_offered_free=True,
        garment_accepted=True,
        physical_contact_occurred=False,
    )
    result = encounter.process_encounter()
    assert result["status"] == "RESOLVED_IMMEDIATELY_NO_RECORD"
    assert result["case_closed"] is True
    assert result["fine_or_debt_rcu"] == 0.0
    assert result["record_created"] is False
    assert result["officer_disciplinary_action"] is False


def test_garment_refusal_issues_civil_notice_only():
    encounter = EnforcementEncounter(
        encounter_id="ENC-002",
        citizen_gender="male",
        spatial_zone=SpatialZone.ZONE_2_STANDARD,
        officer_gender="male",
        garment_offered_free=True,
        garment_accepted=False,  # Refused
        physical_contact_occurred=False,
    )
    result = encounter.process_encounter()
    assert result["status"] == "CIVIL_NOTICE_ISSUED"
    assert result["case_closed"] is False
    assert result["fine_or_debt_rcu"] > 0
    assert result["record_created"] is True
    assert result["officer_disciplinary_action"] is False


def test_physical_contact_by_officer_is_unlawful():
    encounter = EnforcementEncounter(
        encounter_id="ENC-003",
        citizen_gender="female",
        spatial_zone=SpatialZone.ZONE_1_STRICT,
        officer_gender="male",
        garment_offered_free=True,
        garment_accepted=False,
        physical_contact_occurred=True,  # Prohibited touching
    )
    result = encounter.process_encounter()
    assert result["status"] == "UNLAWFUL_OFFICER_CONDUCT"
    assert result["officer_disciplinary_action"] is True
    assert result["fine_or_debt_rcu"] == 0.0


def test_anti_humiliation_policy_completeness():
    policy = AntiHumiliationPolicy()
    assert policy.is_anti_extortion_complete is True
    assert policy.physical_touching_prohibited is True
    assert policy.arrest_and_detention_prohibited is True
    assert policy.criminal_record_creation_prohibited is True
    assert policy.mixed_sex_patrol_pairs_mandatory is True
    assert policy.female_approached_by_female_only is True
    assert policy.bodycam_mandatory is True
    assert policy.officer_body_measuring_or_comments_prohibited is True
    assert policy.five_year_democratic_sunset is True


def test_compliance_simulation_metrics():
    sim = ClothingComplianceSimulation(total_non_compliant_encounters=1000)
    assert sim.encounters_resolved_without_record >= 900
    assert sim.civil_notices_issued <= 100
    assert sim.arrest_count == 0  # Zero arrests across the entire population


def test_sovereignty_methodology_purpose_first():
    sovereign = SovereignMethodology(rule=SovereigntyDesignRule.PURPOSE_FIRST)
    eval_sov = sovereign.evaluate_policy_design()
    assert eval_sov["status"] == "SOVEREIGN_PURPOSE_DRIVEN"
    assert eval_sov["autonomous"] is True

    reactive = SovereignMethodology(rule=SovereigntyDesignRule.REACTIVE_INVERSION)
    eval_react = reactive.evaluate_policy_design()
    assert eval_react["status"] == "REJECTED_REACTIVE_TRAP"
    assert eval_react["autonomous"] is False


def test_public_sector_dress_tiers_and_accountability():
    assert len(PUBLIC_SECTOR_DRESS_TIERS) == 3
    tier_map = {t.tier: t for t in PUBLIC_SECTOR_DRESS_TIERS}

    tier_1 = tier_map[DressTierCategory.TIER_1_AUTHORITY_UNIFORM]
    assert tier_1.mandatory_uniform is True
    assert tier_1.mandatory_visible_id is True
    assert "accountability device" in tier_1.core_purpose.lower()

    tier_2 = tier_map[DressTierCategory.TIER_2_ADMINISTRATIVE_CODE]
    assert tier_2.mandatory_uniform is False
    assert tier_2.mandatory_visible_id is False

    tier_3 = tier_map[DressTierCategory.TIER_3_SENIOR_PLAINNESS]
    assert tier_3.mandatory_uniform is False
    assert "visual restraint" in tier_3.core_purpose.lower() or "simply" in tier_3.core_purpose.lower()


def test_uniform_procurement_policy_and_industrial_link():
    proc = UniformProcurementPolicy()
    assert proc.is_procurement_sound is True
    assert proc.state_funded_full_cost is True
    assert proc.domestic_guild_manufacture is True
    assert proc.open_contracting_mandatory is True
    assert proc.dignity_and_fit_specifications is True
    assert proc.sovereign_local_visual_design is True

