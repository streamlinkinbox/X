"""Research and Analysis Bureau (RAB): Cross-departmental synthesis,
forensic anomaly detection, and closed-loop systemic reform.

This module models the central analytical organ of the community:
1. ``divisions`` -- 5 specialized analytical branches (Forensics, Economy,
   Human Capital, Reform Design, Science & Technology).
2. ``staffing`` -- lean staffing model sizing (35-55 analysts per 10,000 population).
3. ``silo_synthesis`` -- multi-source data correlation engine connecting
   independent departmental streams into systemic patterns.
4. ``early_warning`` -- thresholds for wealth concentration, resource depletion,
   and sector de-industrialization.
5. ``reform_loop`` -- 6-stage closed-loop reform state machine.
6. ``rab_accountability`` -- constitutional constraints preventing the analytical
   bureau from becoming an unaccountable secret police.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import ROUND_HALF_UP, Decimal
from enum import Enum


def _q(x: Decimal, places: str = "0.01") -> Decimal:
    return x.quantize(Decimal(places), rounding=ROUND_HALF_UP)


# --------------------------------------------------------------------------
# 1. RAB Structure & The Five Divisions
# --------------------------------------------------------------------------


class DivisionType(str, Enum):
    FORENSIC_AUDIT = "forensic_audit"
    ECONOMIC_ANALYSIS = "economic_analysis"
    HUMAN_CAPITAL = "human_capital"
    REFORM_DESIGN = "reform_design"
    SCIENCE_TECH = "science_tech"


@dataclass(frozen=True)
class DivisionSpec:
    division_type: DivisionType
    name: str
    mandate: str
    core_data_sources: tuple[str, ...]
    primary_deliverables: tuple[str, ...]


RAB_DIVISIONS: tuple[DivisionSpec, ...] = (
    DivisionSpec(
        division_type=DivisionType.FORENSIC_AUDIT,
        name="Forensic Audit Division",
        mandate="Scans financial, transactional, and warehouse inventory data for fraud, hoarding, skimming, and collusion",
        core_data_sources=(
            "RCU currency transaction trails",
            "Warehouse physical inventory balances and moisture logs",
            "Inspector deposit grading variance tables",
            "Trader cross-district pricing records",
        ),
        primary_deliverables=(
            "Monthly Named Fraud Alerts (forwarded to Justice)",
            "Quarterly Departmental Integrity Reports",
            "Annual Sector Corruption Risk Index",
        ),
    ),
    DivisionSpec(
        division_type=DivisionType.ECONOMIC_ANALYSIS,
        name="Economic Analysis Division",
        mandate="Monitors macroeconomic health, circulation velocity, trade balances, wealth concentration, and resource depletion",
        core_data_sources=(
            "Currency circulation and velocity logs",
            "Agricultural and workshop quota outputs",
            "Import/export trade window balances (§16)",
            "Ecological regeneration metrics (timber/aquifer)",
        ),
        primary_deliverables=(
            "Monthly Public Economic Dashboard",
            "Quarterly Sector Health Reports",
            "Early Warning Alerts (6–12 month threat horizon)",
            "Annual Economic Resilience Stress Tests",
        ),
    ),
    DivisionSpec(
        division_type=DivisionType.HUMAN_CAPITAL,
        name="Human Capital Division",
        mandate="Evaluates performance of coordinators, masters, teachers, and apprentices using difficulty-adjusted metrics",
        core_data_sources=(
            "Steward performance targets vs actual outcomes",
            "Apprentice graduation and competency testing logs",
            "Mobilization drill timing and tactical scores",
            "Anonymous community confidence surveys",
        ),
        primary_deliverables=(
            "Quarterly Leadership Scorecards",
            "Competence Recall Trigger Alerts",
            "Excellence and Talent Recognition Flags",
            "Annual Human Capital Pipeline Report",
        ),
    ),
    DivisionSpec(
        division_type=DivisionType.REFORM_DESIGN,
        name="Reform Design Division",
        mandate="Designs actionable, evidence-based structural reforms and cross-department solutions based on division findings",
        core_data_sources=(
            "Identified anomalies from Forensics, Economy, and Human Capital",
            "Historical post-mortem failure logs",
            "Apprentice guild feedback and technological bottlenecks",
        ),
        primary_deliverables=(
            "Costed Multi-Department Reform Proposals",
            "Pilot Test Specifications and Target Benchmarks",
            "5-Year and 10-Year Strategic Development Roadmaps",
        ),
    ),
    DivisionSpec(
        division_type=DivisionType.SCIENCE_TECH,
        name="Science & Technology Division",
        mandate="Conducts applied research on agricultural resilience, herbal medicine, materials, renewable microgrids, and local tooling",
        core_data_sources=(
            "Field trial yield and disease resistance data",
            "Traditional herbal efficacy assays",
            "Local material stress and metallurgical tests",
            "Micro-hydro, biogas, and solar telemetry",
        ),
        primary_deliverables=(
            "Locally Adapted Crop Seeds and Pest Solutions",
            "Standardized Herbal Compounding Protocols",
            "Apprentice Advanced Research Project Placements",
            "Indigenous Production Ladder Innovations",
        ),
    ),
)


# --------------------------------------------------------------------------
# 2. Staffing Model (Community of 10,000)
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class RABStaffing:
    population: int = 10000
    chief_analysts: int = 1
    senior_analysts: int = 6       # 1 per division + 1 deputy
    junior_analysts: int = 14      # 2-3 per division
    data_collectors: int = 18      # Field verifiers and survey collectors
    field_researchers: int = 8     # Science & technical research leads

    @property
    def total_staff(self) -> int:
        return (
            self.chief_analysts
            + self.senior_analysts
            + self.junior_analysts
            + self.data_collectors
            + self.field_researchers
        )

    @property
    def staff_share_of_population(self) -> Decimal:
        if self.population == 0:
            return Decimal(0)
        return _q(Decimal(self.total_staff) / Decimal(self.population), "0.0001")


# --------------------------------------------------------------------------
# 3. Cross-Silo Pattern Recognition Engine
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class SiloDataPoint:
    department: str
    metric: str
    anomaly_detected: bool
    description: str


@dataclass(frozen=True)
class CrossDepartmentInvestigation:
    investigation_id: str
    data_points: tuple[SiloDataPoint, ...]
    kinship_or_collusion_flag: bool = False

    @property
    def anomaly_count(self) -> int:
        return sum(1 for dp in self.data_points if dp.anomaly_detected)

    @property
    def departments_involved(self) -> set[str]:
        return {dp.department for dp in self.data_points}

    @property
    def systemic_threat_score(self) -> Decimal:
        """Score from 0.0 to 1.0 based on cross-silo breadth and collusion flags."""
        base = min(1.0, (self.anomaly_count * 0.25) + (len(self.departments_involved) * 0.15))
        if self.kinship_or_collusion_flag:
            base = min(1.0, base + 0.35)
        return _q(Decimal(str(base)), "0.01")

    @property
    def triggers_formal_justice_referral(self) -> bool:
        return self.systemic_threat_score >= Decimal("0.70")


# --------------------------------------------------------------------------
# 4. Economic Early Warning Triggers
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class EconomicEarlyWarningSystem:
    top_10_pct_wealth_share: float      # Warning if > 30%
    top_5_pct_wealth_share: float       # Warning if > 25%
    single_resource_dependence: float   # Warning if > 30%
    annual_fishery_catch_delta: float   # Alert if negative trend
    timber_depletion_vs_replant: float  # Alert if extraction > replant (ratio > 1.0)

    @property
    def wealth_inequality_alert(self) -> bool:
        return self.top_10_pct_wealth_share > 0.30 or self.top_5_pct_wealth_share > 0.25

    @property
    def resource_curse_alert(self) -> bool:
        return self.single_resource_dependence > 0.30

    @property
    def ecological_depletion_alert(self) -> bool:
        return self.timber_depletion_vs_replant > 1.0 or self.annual_fishery_catch_delta < -0.10

    @property
    def total_active_alerts(self) -> int:
        return sum([
            self.wealth_inequality_alert,
            self.resource_curse_alert,
            self.ecological_depletion_alert,
        ])


# --------------------------------------------------------------------------
# 5. Closed-Loop Reform State Machine
# --------------------------------------------------------------------------


class ReformStage(str, Enum):
    PROBLEM_IDENTIFIED = "problem_identified"
    ROOT_CAUSE_ANALYSIS = "root_cause_analysis"
    SOLUTION_DESIGN = "solution_design"
    PILOT_TESTING = "pilot_testing"
    COUNCIL_APPROVAL = "council_approval"
    IMPLEMENTATION = "implementation"
    IMPACT_EVALUATED = "impact_evaluated"


@dataclass(frozen=True)
class ReformProject:
    project_id: str
    title: str
    target_department: str
    current_stage: ReformStage
    baseline_failure_metric: float
    pilot_target_metric: float
    pilot_actual_metric: float
    higher_is_better: bool = False

    @property
    def pilot_successful(self) -> bool:
        if self.higher_is_better:
            return self.pilot_actual_metric >= self.pilot_target_metric
        return self.pilot_actual_metric <= self.pilot_target_metric

    @property
    def reform_becomes_permanent(self) -> bool:
        return self.current_stage == ReformStage.IMPACT_EVALUATED and self.pilot_successful


# --------------------------------------------------------------------------
# 6. RAB Checks and Constitutional Limits
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class RABAccountabilityPolicy:
    has_arrest_or_punishment_power: bool = False
    all_reports_public_by_default: bool = True
    chief_analyst_rotation_years: int = 2
    analyst_max_tenure_years: int = 5
    mandatory_annual_external_audit: bool = True
    whistleblower_retaliation_prohibited: bool = True
    council_dissolution_power: bool = True

    @property
    def is_constitutionally_bounded(self) -> bool:
        """Must have zero police powers, full transparency, and short rotation."""
        if self.has_arrest_or_punishment_power:
            return False
        if not self.all_reports_public_by_default:
            return False
        if self.chief_analyst_rotation_years > 2:
            return False
        if self.analyst_max_tenure_years > 5:
            return False
        return True
