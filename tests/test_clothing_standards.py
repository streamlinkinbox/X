"""Tests for Public Clothing Standards and Exposure Thresholds (§28)."""

import pytest

from model.rcu.clothing_standards import (
    AntiHumiliationPolicy,
    ClothingComplianceSimulation,
    DressTierCategory,
    EnforcementEncounter,
    EqualResourcingAudit,
    FailureModePrevention,
    FemaleGuardServiceSpec,
    PUBLIC_SECTOR_DRESS_TIERS,
    PublicSectorDressTier,
    SEPARATION_TIER_SPECS,
    SeparationTierSpec,
    SovereigntyDesignRule,
    SovereignMethodology,
    SPATIAL_ZONE_SPECS,
    SpatialZone,
    UniformProcurementPolicy,
    WORKFORCE_FAILURE_PREVENTIONS,
    WorkforceSeparationTier,
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


def test_workforce_separation_tiers():
    assert len(SEPARATION_TIER_SPECS) == 4
    tier_map = {t.tier: t for t in SEPARATION_TIER_SPECS}

    t1 = tier_map[WorkforceSeparationTier.TIER_1_ABSOLUTE]
    assert "own sex" in t1.statutory_rule.lower()
    assert "life-threatening" in t1.waiver_policy.lower()

    t2 = tier_map[WorkforceSeparationTier.TIER_2_UNIT_SEPARATION]
    assert "single-sex" in t2.statutory_rule.lower()

    t3 = tier_map[WorkforceSeparationTier.TIER_3_FACILITY_SEPARATION]
    assert "separate entrances" in t3.statutory_rule.lower()

    t4 = tier_map[WorkforceSeparationTier.TIER_4_FULL_DUPLICATION]
    assert "capacity-gated" in t4.waiver_policy.lower()


def test_female_guard_service_parity_and_recruitment():
    fgs = FemaleGuardServiceSpec()
    assert fgs.distinct_permanent_service is True
    assert fgs.equal_rank_command_head is True
    assert fgs.full_statutory_powers is True
    assert fgs.identical_pay_and_pension is True
    assert fgs.no_career_ceiling is True
    assert fgs.female_cut_body_armor_mandatory is True
    assert fgs.quick_release_head_covering is True

    # 1,000 minimum posts requires 1,200 recruitment target (+20% attrition buffer)
    target = fgs.calculate_recruitment_target(statutory_minimum_posts=1000)
    assert target == 1200


def test_equal_resourcing_audit_parity():
    audit = EqualResourcingAudit(max_divergence_threshold=0.05)

    # Compliant parity
    res_ok = audit.verify_parity(
        male_budget_per_officer=10000.0,
        female_budget_per_officer=10200.0,  # 2% diff <= 5%
        male_training_days=30.0,
        female_training_days=31.0,          # 3.3% diff <= 5%
    )
    assert res_ok["parity_maintained"] is True
    assert res_ok["audit_trigger_activated"] is False

    # Drift violation (15% budget gap)
    res_drift = audit.verify_parity(
        male_budget_per_officer=10000.0,
        female_budget_per_officer=8500.0,   # 15% diff > 5%
        male_training_days=30.0,
        female_training_days=30.0,
    )
    assert res_drift["parity_maintained"] is False
    assert res_drift["audit_trigger_activated"] is True
    assert res_drift["disciplinary_action_required"] is True


def test_failure_mode_prevention_clauses():
    assert len(WORKFORCE_FAILURE_PREVENTIONS) == 6
    preventions = {p.failure_mode: p.prevention_clause for p in WORKFORCE_FAILURE_PREVENTIONS}

    assert "Women's institution under-resourced" in preventions
    assert "Tier 1 waived for staffing shortages" in preventions
    assert "Female service becomes auxiliary" in preventions
    assert "Retention collapse" in preventions
    assert "Specialist expertise halved" in preventions
    assert "Uniform procurement capture" in preventions


