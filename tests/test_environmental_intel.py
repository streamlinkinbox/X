"""Tests for the Community Intelligence Service (CIS) and Environmental & Disaster Management Bureau (EDMB)."""

from __future__ import annotations

import sys
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from model.rcu.environmental_intel import (  # noqa: E402
    CIS_DIRECTORATES,
    COMMON_TRANSBOUNDARY_EVENTS,
    AlertLevel,
    CISDirectorateType,
    CISSafeguards,
    CISStaffing,
    EIAAssessment,
    EIARiskRating,
    EDMBStaffing,
    EnvironmentalTelemetry,
)


# --------------------------------------------------------------------------
# 1. Community Intelligence Service (CIS) Tests
# --------------------------------------------------------------------------


def test_four_intelligence_directorates_exist():
    assert len(CIS_DIRECTORATES) == 4
    types = [d.directorate_type for d in CIS_DIRECTORATES]
    assert CISDirectorateType.HUMINT in types
    assert CISDirectorateType.SIGINT in types
    assert CISDirectorateType.OSINT in types
    assert CISDirectorateType.COUNTER_INTEL in types


def test_cis_staffing_within_lean_limits():
    staff = CISStaffing(population=10000)
    assert 16 <= staff.total_staff <= 24
    assert staff.chief_of_intel == 1
    assert staff.humint_officers >= 5
    assert staff.sigint_technicians >= 3
    assert staff.osint_analysts >= 4
    assert staff.counter_intel_officers >= 3


def test_cis_safeguards_enforce_no_domestic_spying():
    safe = CISSafeguards()
    assert safe.is_constitutionally_compliant
    assert not safe.domestic_surveillance_allowed
    assert not safe.offensive_covert_actions_allowed
    assert safe.data_retention_limit_years == 2


def test_cis_safeguards_violation_caught():
    rogue = CISSafeguards(domestic_surveillance_allowed=True)
    assert not rogue.is_constitutionally_compliant


# --------------------------------------------------------------------------
# 2. Environmental Impact Assessment (EIA) Tests
# --------------------------------------------------------------------------


def test_low_risk_eia_proceeds():
    eia = EIAAssessment(
        project_name="Village Grain Shed",
        proposing_department="Reserves",
        risk_rating=EIARiskRating.LOW,
        stagnant_water_risk=False,
        floodplain_encroachment=False,
        slope_destabilization_risk=False,
        aquifer_depletion_risk=False,
        mitigation_plan_approved=True,
    )
    assert eia.can_proceed
    assert not eia.requires_supermajority_override


def test_moderate_risk_with_mitigation_proceeds():
    eia = EIAAssessment(
        project_name="Floodplain Farmland Expansion",
        proposing_department="Agriculture",
        risk_rating=EIARiskRating.MODERATE,
        stagnant_water_risk=False,
        floodplain_encroachment=True,
        slope_destabilization_risk=False,
        aquifer_depletion_risk=False,
        mitigation_plan_approved=True,  # 50m buffer zones approved
    )
    assert eia.can_proceed
    assert not eia.requires_supermajority_override


def test_critical_risk_requires_supermajority_override():
    eia = EIAAssessment(
        project_name="Swamp-Creating Hydro Dam",
        proposing_department="Works",
        risk_rating=EIARiskRating.CRITICAL,
        stagnant_water_risk=True,
        floodplain_encroachment=True,
        slope_destabilization_risk=True,
        aquifer_depletion_risk=False,
        mitigation_plan_approved=False,
    )
    assert not eia.can_proceed
    assert eia.requires_supermajority_override


# --------------------------------------------------------------------------
# 3. Environmental Telemetry & Early Warning Alerts Tests
# --------------------------------------------------------------------------


def test_flood_telemetry_triggers_red_alert():
    telem = EnvironmentalTelemetry(
        river_gauge_meters=5.2,
        river_flood_threshold_meters=5.0,  # Over threshold
        rainfall_24h_mm=135.0,
        soil_moisture_saturation_pct=70.0,
        slope_angle_degrees=15.0,
        drinking_water_pathogen_count=0,
        mosquito_larvae_count_delta_pct=10.0,
    )
    assert telem.flood_alert_level == AlertLevel.RED


def test_landslide_telemetry_triggers_red_alert():
    telem = EnvironmentalTelemetry(
        river_gauge_meters=2.0,
        river_flood_threshold_meters=5.0,
        rainfall_24h_mm=60.0,
        soil_moisture_saturation_pct=95.0,  # Saturated
        slope_angle_degrees=34.0,           # Steep slope
        drinking_water_pathogen_count=0,
        mosquito_larvae_count_delta_pct=10.0,
    )
    assert telem.landslide_alert_level == AlertLevel.RED


def test_vector_monitoring_triggers_red_alert():
    telem = EnvironmentalTelemetry(
        river_gauge_meters=2.0,
        river_flood_threshold_meters=5.0,
        rainfall_24h_mm=10.0,
        soil_moisture_saturation_pct=40.0,
        slope_angle_degrees=10.0,
        drinking_water_pathogen_count=0,
        mosquito_larvae_count_delta_pct=300.0, # 300% surge
    )
    assert telem.epidemic_vector_alert_level == AlertLevel.RED


# --------------------------------------------------------------------------
# 4. EDMB Staffing & Mobilization Tests
# --------------------------------------------------------------------------


def test_edmb_staffing_and_volunteer_reserve():
    staff = EDMBStaffing(population=10000)
    assert 21 <= staff.permanent_staff <= 32
    assert staff.total_mobilizable_response_force >= 75
    assert staff.chief_environmental_officer == 1
    assert staff.monitoring_technicians >= 8
    assert staff.eia_assessors >= 3


# --------------------------------------------------------------------------
# 5. Awareness Triangle Tests
# --------------------------------------------------------------------------


def test_awareness_triangle_events_synthesize_all_three_organs():
    assert len(COMMON_TRANSBOUNDARY_EVENTS) >= 3
    for ev in COMMON_TRANSBOUNDARY_EVENTS:
        assert len(ev.cis_action) > 10
        assert len(ev.edmb_action) > 10
        assert len(ev.rab_action) > 10
        assert len(ev.council_action) > 10
