"""Tests for Public Clothing Standards and Exposure Thresholds (§28)."""

import pytest

from model.rcu.clothing_standards import (
    AntiHumiliationPolicy,
    ClothingComplianceSimulation,
    EnforcementEncounter,
    SPATIAL_ZONE_SPECS,
    SpatialZone,
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
