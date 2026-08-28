"""Community Intelligence Service (CIS) and Environmental & Disaster Management Bureau (EDMB).

This module models the external sensory and ecological protection organs:
1. ``cis_structure`` -- 4 intelligence directorates (HUMINT, SIGINT, OSINT, CI).
2. ``cis_staffing`` -- 16-24 external intelligence personnel per 10,000 population.
3. ``edmb_structure`` -- 5 environmental divisions (Monitoring, EIA, Disaster Prep,
   Rescue & Response, Regeneration).
4. ``edmb_staffing`` -- 21-32 permanent environmental staff + 50-100 emergency volunteers.
5. ``eia_framework`` -- 4-tier Environmental Impact Assessment rating and 75% council override.
6. ``environmental_telemetry`` -- threshold models for floods, landslides, epidemics, and droughts.
7. ``awareness_triangle`` -- cross-information sharing between RAB, CIS, and EDMB.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import ROUND_HALF_UP, Decimal
from enum import Enum


def _q(x: Decimal, places: str = "0.01") -> Decimal:
    return x.quantize(Decimal(places), rounding=ROUND_HALF_UP)


# --------------------------------------------------------------------------
# 1. Community Intelligence Service (CIS)
# --------------------------------------------------------------------------


class CISDirectorateType(str, Enum):
    HUMINT = "humint"
    SIGINT = "sigint"
    OSINT = "osint"
    COUNTER_INTEL = "counter_intel"


@dataclass(frozen=True)
class CISDirectorateSpec:
    directorate_type: CISDirectorateType
    name: str
    mandate: str
    sources_and_methods: tuple[str, ...]
    primary_deliverables: tuple[str, ...]


CIS_DIRECTORATES: tuple[CISDirectorateSpec, ...] = (
    CISDirectorateSpec(
        directorate_type=CISDirectorateType.HUMINT,
        name="Human Intelligence Directorate",
        mandate="Gathers information through long-distance traders, refugee debriefs, diaspora networks, and embedded observers",
        sources_and_methods=(
            "Long-distance trading caravan relationships",
            "Structured non-coercive refugee intake interviews",
            "Secure diaspora communication channels",
            "Diplomatic mission debriefs and border observations",
        ),
        primary_deliverables=(
            "Weekly Regional Situation Reports (200km radius)",
            "External Actor Intent & Capability Assessments",
            "Cross-Border Trade & Alliance Opportunity Alerts",
        ),
    ),
    CISDirectorateSpec(
        directorate_type=CISDirectorateType.SIGINT,
        name="Signals Intelligence Directorate",
        mandate="Monitors external electronic transmissions, radio channels, drone frequencies, and satellite imagery",
        sources_and_methods=(
            "Shortwave and VHF/UHF radio interception",
            "Border mobile phone traffic spike detection",
            "2.4 GHz and 5.8 GHz RF drone control scanners",
            "Open satellite imagery analysis (Sentinel, NASA Earthdata)",
        ),
        primary_deliverables=(
            "Immediate Pre-Deployment Tactical Radio Alerts",
            "Inbound Drone Surveillance Warnings (10–15 min lead)",
            "Foreign Military Road & Infrastructure Expansion Alerts",
        ),
    ),
    CISDirectorateSpec(
        directorate_type=CISDirectorateType.OSINT,
        name="Open Source Intelligence Directorate",
        mandate="Synthesizes global and regional public data: media, government gazettes, procurement, and commodity markets",
        sources_and_methods=(
            "National legislative and mining concession gazettes",
            "Global commodity price and supply chain monitoring",
            "Regional conflict tracking and refugee flow mapping",
            "Public corporate and political announcements",
        ),
        primary_deliverables=(
            "Daily Curated News Digest",
            "National Policy & Concession Early Warnings",
            "External Economic & FX Vulnerability Bulletins",
        ),
    ),
    CISDirectorateSpec(
        directorate_type=CISDirectorateType.COUNTER_INTEL,
        name="Counter-Intelligence Directorate",
        mandate="Protects the community against external espionage, infiltration, disinformation, cyber sabotage, and supply poisoning",
        sources_and_methods=(
            "Cross-referencing intake claims against OSINT/HUMINT",
            "Digital currency ledger intrusion monitoring",
            "Disinformation campaign tracing on public channels",
            "Cryptographic protocol vulnerability audits",
        ),
        primary_deliverables=(
            "Espionage Threat Bulletins",
            "Disinformation Debunking Alerts",
            "Supply Chain Contamination & Cyber Alerts",
        ),
    ),
)


@dataclass(frozen=True)
class CISStaffing:
    population: int = 10000
    chief_of_intel: int = 1
    humint_officers: int = 6       # Range 5-8
    sigint_technicians: int = 4    # Range 3-5
    osint_analysts: int = 5        # Range 4-6
    counter_intel_officers: int = 4 # Range 3-4

    @property
    def total_staff(self) -> int:
        return (
            self.chief_of_intel
            + self.humint_officers
            + self.sigint_technicians
            + self.osint_analysts
            + self.counter_intel_officers
        )


@dataclass(frozen=True)
class CISSafeguards:
    domestic_surveillance_allowed: bool = False
    offensive_covert_actions_allowed: bool = False
    council_subcommittee_oversight: bool = True
    data_retention_limit_years: int = 2
    whistleblower_protection: bool = True
    annual_public_transparency_report: bool = True

    @property
    def is_constitutionally_compliant(self) -> bool:
        if self.domestic_surveillance_allowed:
            return False
        if self.offensive_covert_actions_allowed:
            return False
        if not self.council_subcommittee_oversight:
            return False
        if self.data_retention_limit_years > 2:
            return False
        return True


# --------------------------------------------------------------------------
# 2. Environmental & Disaster Management Bureau (EDMB)
# --------------------------------------------------------------------------


class AlertLevel(str, Enum):
    GREEN = "green"    # Normal conditions
    YELLOW = "yellow"  # Elevated risk (contingency prep)
    ORANGE = "orange"  # High risk (activate protocols, pre-position caches)
    RED = "red"        # Imminent disaster (immediate evacuation/response)


class EIARiskRating(str, Enum):
    LOW = "low"            # Minimal impact, proceed
    MODERATE = "moderate"  # Significant impact, mandatory mitigation plan
    HIGH = "high"          # Severe impact, project redesign required
    CRITICAL = "critical"  # Unacceptable impact, project denied (needs 75% Council override)


@dataclass(frozen=True)
class EIAAssessment:
    project_name: str
    proposing_department: str
    risk_rating: EIARiskRating
    stagnant_water_risk: bool
    floodplain_encroachment: bool
    slope_destabilization_risk: bool
    aquifer_depletion_risk: bool
    mitigation_plan_approved: bool

    @property
    def requires_supermajority_override(self) -> bool:
        return self.risk_rating == EIARiskRating.CRITICAL

    @property
    def can_proceed(self) -> bool:
        if self.risk_rating == EIARiskRating.LOW:
            return True
        if self.risk_rating in {EIARiskRating.MODERATE, EIARiskRating.HIGH}:
            return self.mitigation_plan_approved
        return False  # Critical denied unless overridden by 75% Council


@dataclass(frozen=True)
class EnvironmentalTelemetry:
    river_gauge_meters: float
    river_flood_threshold_meters: float
    rainfall_24h_mm: float
    soil_moisture_saturation_pct: float
    slope_angle_degrees: float
    drinking_water_pathogen_count: int  # CFU per 100ml (0 is clean)
    mosquito_larvae_count_delta_pct: float

    @property
    def flood_alert_level(self) -> AlertLevel:
        ratio = self.river_gauge_meters / max(self.river_flood_threshold_meters, 0.1)
        if ratio >= 1.0 or self.rainfall_24h_mm >= 120.0:
            return AlertLevel.RED
        if ratio >= 0.85 or self.rainfall_24h_mm >= 80.0:
            return AlertLevel.ORANGE
        if ratio >= 0.70 or self.rainfall_24h_mm >= 45.0:
            return AlertLevel.YELLOW
        return AlertLevel.GREEN

    @property
    def landslide_alert_level(self) -> AlertLevel:
        # Saturated steep slopes predict landslides
        if self.slope_angle_degrees >= 30.0 and self.soil_moisture_saturation_pct >= 90.0:
            return AlertLevel.RED
        if self.slope_angle_degrees >= 25.0 and self.soil_moisture_saturation_pct >= 75.0:
            return AlertLevel.ORANGE
        if self.soil_moisture_saturation_pct >= 65.0:
            return AlertLevel.YELLOW
        return AlertLevel.GREEN

    @property
    def epidemic_vector_alert_level(self) -> AlertLevel:
        if self.drinking_water_pathogen_count > 10 or self.mosquito_larvae_count_delta_pct >= 250.0:
            return AlertLevel.RED
        if self.drinking_water_pathogen_count > 0 or self.mosquito_larvae_count_delta_pct >= 100.0:
            return AlertLevel.ORANGE
        if self.mosquito_larvae_count_delta_pct >= 50.0:
            return AlertLevel.YELLOW
        return AlertLevel.GREEN


@dataclass(frozen=True)
class EDMBStaffing:
    population: int = 10000
    chief_environmental_officer: int = 1
    monitoring_technicians: int = 10       # Range 8-12
    eia_assessors: int = 4                 # Range 3-5
    disaster_response_coordinators: int = 5 # Range 4-6
    regeneration_specialists: int = 6      # Range 5-8
    trained_emergency_volunteers: int = 75 # Range 50-100

    @property
    def permanent_staff(self) -> int:
        return (
            self.chief_environmental_officer
            + self.monitoring_technicians
            + self.eia_assessors
            + self.disaster_response_coordinators
            + self.regeneration_specialists
        )

    @property
    def total_mobilizable_response_force(self) -> int:
        return self.permanent_staff + self.trained_emergency_volunteers


# --------------------------------------------------------------------------
# 3. The Awareness Triangle (RAB + CIS + EDMB)
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class TransboundaryEvent:
    event_name: str
    detected_by: str      # CIS, EDMB, or RAB
    cis_action: str
    edmb_action: str
    rab_action: str
    council_action: str


COMMON_TRANSBOUNDARY_EVENTS: tuple[TransboundaryEvent, ...] = (
    TransboundaryEvent(
        event_name="Upstream Dam Construction by Neighboring State",
        detected_by="CIS (HUMINT from traders & satellite SIGINT)",
        cis_action="Monitors construction timeline and military security around dam site",
        edmb_action="Models downstream river flow reduction and wetland drought impact",
        rab_action="Calculates loss of agricultural irrigation and protein fishery yield",
        council_action="Initiates bilateral water treaty negotiations and activates water storage reserves",
    ),
    TransboundaryEvent(
        event_name="Regional Cholera Outbreak in Border District",
        detected_by="CIS (OSINT news digests) & EDMB (Water pathogen monitoring)",
        cis_action="Tracks refugee and border traveler movements from infected zone",
        edmb_action="Increases chlorination monitoring and sanitation along border rivers",
        rab_action="Assesses community ORS and IV fluid stockpile buffer days (§17)",
        council_action="Establishes border health screening checkpoints and quarantines",
    ),
    TransboundaryEvent(
        event_name="Prolonged Regional Drought Pattern",
        detected_by="EDMB (Rainfall & soil telemetry)",
        cis_action="Monitors neighboring state food riots and potential cross-border cattle raids",
        edmb_action="Predicts drought duration and regulates reservoir drawdown schedules",
        rab_action="Models grain warehouse inventory runway and triggers Tier A preservation",
        council_action="Mandates drought-resistant millet/sorghum planting and caps irrigation",
    ),
)
