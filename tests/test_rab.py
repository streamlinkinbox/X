"""Tests for the Research and Analysis Bureau (RAB) model."""

from __future__ import annotations

import sys
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from model.rcu.rab import (  # noqa: E402
    RAB_DIVISIONS,
    CrossDepartmentInvestigation,
    DivisionType,
    EconomicEarlyWarningSystem,
    RABAccountabilityPolicy,
    RABStaffing,
    ReformProject,
    ReformStage,
    SiloDataPoint,
)


# --------------------------------------------------------------------------
# 1. Structure & Divisions Tests
# --------------------------------------------------------------------------


def test_five_divisions_exist():
    assert len(RAB_DIVISIONS) == 5
    types = [d.division_type for d in RAB_DIVISIONS]
    assert DivisionType.FORENSIC_AUDIT in types
    assert DivisionType.ECONOMIC_ANALYSIS in types
    assert DivisionType.HUMAN_CAPITAL in types
    assert DivisionType.REFORM_DESIGN in types
    assert DivisionType.SCIENCE_TECH in types


def test_each_division_has_clear_mandate_and_deliverables():
    for d in RAB_DIVISIONS:
        assert len(d.mandate) > 20
        assert len(d.core_data_sources) >= 3
        assert len(d.primary_deliverables) >= 3


# --------------------------------------------------------------------------
# 2. Staffing Model Tests
# --------------------------------------------------------------------------


def test_rab_staffing_is_lean_and_within_bounds():
    staff = RABStaffing(population=10000)
    assert 35 <= staff.total_staff <= 55
    assert staff.chief_analysts == 1
    assert staff.senior_analysts >= 5
    assert staff.junior_analysts >= 10
    assert staff.data_collectors >= 15
    assert staff.field_researchers >= 5
    assert Decimal("0.0035") <= staff.staff_share_of_population <= Decimal("0.0055")


# --------------------------------------------------------------------------
# 3. Cross-Silo Synthesis Tests
# --------------------------------------------------------------------------


def test_cross_silo_corruption_ring_detected():
    """Connecting grain loss + inspector logs + kinship link triggers Justice referral."""
    inv = CrossDepartmentInvestigation(
        investigation_id="INV-WH7-001",
        data_points=(
            SiloDataPoint("Treasury/Warehouse", "Grain Spoilage", True, "Warehouse 7 reporting 15% loss vs 3% avg"),
            SiloDataPoint("Inspectorate", "Grade Variance", True, "Inspector X consistently approved high grades"),
            SiloDataPoint("Civil Registry", "Kinship Link", True, "Manager is Inspector X brother-in-law"),
        ),
        kinship_or_collusion_flag=True,
    )
    assert inv.anomaly_count == 3
    assert len(inv.departments_involved) == 3
    assert inv.systemic_threat_score >= Decimal("0.70")
    assert inv.triggers_formal_justice_referral


def test_isolated_benign_event_does_not_trigger_crisis():
    inv = CrossDepartmentInvestigation(
        investigation_id="INV-BENIGN-002",
        data_points=(
            SiloDataPoint("Agriculture", "Minor Frost", False, "Normal seasonal temperature dip"),
        ),
        kinship_or_collusion_flag=False,
    )
    assert inv.systemic_threat_score < Decimal("0.50")
    assert not inv.triggers_formal_justice_referral


# --------------------------------------------------------------------------
# 4. Economic Early Warning System Tests
# --------------------------------------------------------------------------


def test_wealth_inequality_triggers_warning():
    ews = EconomicEarlyWarningSystem(
        top_10_pct_wealth_share=0.35, # > 30% threshold
        top_5_pct_wealth_share=0.22,
        single_resource_dependence=0.15,
        annual_fishery_catch_delta=0.02,
        timber_depletion_vs_replant=0.85,
    )
    assert ews.wealth_inequality_alert
    assert not ews.resource_curse_alert
    assert ews.total_active_alerts == 1


def test_ecological_depletion_triggers_warning():
    ews = EconomicEarlyWarningSystem(
        top_10_pct_wealth_share=0.20,
        top_5_pct_wealth_share=0.12,
        single_resource_dependence=0.18,
        annual_fishery_catch_delta=-0.20, # 20% fishery decline
        timber_depletion_vs_replant=1.40,  # 40% over-logging
    )
    assert ews.ecological_depletion_alert
    assert ews.total_active_alerts >= 1


# --------------------------------------------------------------------------
# 5. Closed-Loop Reform Tests
# --------------------------------------------------------------------------


def test_successful_reform_becomes_permanent():
    reform = ReformProject(
        project_id="REF-WH7-MOISTURE",
        title="Warehouse 7 Moisture Barrier Retrofit",
        target_department="Treasury/Warehouse",
        current_stage=ReformStage.IMPACT_EVALUATED,
        baseline_failure_metric=15.0,  # 15% spoilage
        pilot_target_metric=5.0,       # Reduce to <= 5%
        pilot_actual_metric=3.8,       # Achieved 3.8%
        higher_is_better=False,
    )
    assert reform.pilot_successful
    assert reform.reform_becomes_permanent


def test_failed_pilot_does_not_become_permanent():
    reform = ReformProject(
        project_id="REF-FERT-TEST",
        title="Untested Compost Formulation",
        target_department="Agriculture",
        current_stage=ReformStage.IMPACT_EVALUATED,
        baseline_failure_metric=20.0,
        pilot_target_metric=10.0,
        pilot_actual_metric=18.5,      # Failed target
        higher_is_better=False,
    )
    assert not reform.pilot_successful
    assert not reform.reform_becomes_permanent


# --------------------------------------------------------------------------
# 6. RAB Accountability & Constitutional Bounds Tests
# --------------------------------------------------------------------------


def test_rab_constitutional_limits_are_enforced():
    policy = RABAccountabilityPolicy()
    assert not policy.has_arrest_or_punishment_power
    assert policy.all_reports_public_by_default
    assert policy.chief_analyst_rotation_years == 2
    assert policy.analyst_max_tenure_years == 5
    assert policy.is_constitutionally_bounded


def test_rab_with_police_powers_is_unconstitutional():
    rogue_policy = RABAccountabilityPolicy(
        has_arrest_or_punishment_power=True,  # Secret police violation
    )
    assert not rogue_policy.is_constitutionally_bounded
