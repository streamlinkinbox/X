"""Competence Council Governance, Departmental Policing, and Continuous Measurement.

This module models functional governance without electoral politics, voting,
or monarchy:
1. ``qualification`` -- objective track-record filtering for leadership pools.
2. ``peer_selection`` -- multi-stage peer selection with 75% consensus versus
   mass electoral popularity voting.
3. ``council_roles`` -- 11 functional leadership mandates, terms, and KPI metrics.
4. ``succession`` -- deterministic, zero-vacuum succession state machine.
5. ``probation`` -- 1-year quantitative performance evaluation.
6. ``departmental_policing`` -- internal enforcement (Military Police, warehouse
   enforcers, anti-hoarding) and independent measurement bureaus in every branch.
7. ``sortition_audit`` -- statistical model of 20-citizen annual random audits.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import ROUND_HALF_UP, Decimal
from enum import Enum


def _q(x: Decimal, places: str = "0.01") -> Decimal:
    return x.quantize(Decimal(places), rounding=ROUND_HALF_UP)


# --------------------------------------------------------------------------
# 1. Qualification Pool & Objective Filtering
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class CandidateRecord:
    candidate_id: str
    age: int
    years_community_service: int
    apprenticeship_completed: bool
    projects_completed_count: int
    peer_reliability_rating: Decimal     # 0.00 to 1.00
    has_disqualifying_failures: bool     # Prior corruption, malfeasance, abuse

    @property
    def is_qualified(self) -> bool:
        """Objective qualification criteria:
        - Minimum age 30
        - Minimum 10 years active service
        - Full apprenticeship completed
        - At least 1 major completed project
        - Minimum 75% peer reliability rating over prior 5 years
        - Zero disqualifying failures
        """
        if self.age < 30:
            return False
        if self.years_community_service < 10:
            return False
        if not self.apprenticeship_completed:
            return False
        if self.projects_completed_count < 1:
            return False
        if self.peer_reliability_rating < Decimal("0.75"):
            return False
        if self.has_disqualifying_failures:
            return False
        return True


@dataclass(frozen=True)
class QualificationPool:
    candidates: tuple[CandidateRecord, ...]

    @property
    def total_candidates(self) -> int:
        return len(self.candidates)

    @property
    def qualified_candidates(self) -> list[CandidateRecord]:
        return [c for c in self.candidates if c.is_qualified]

    @property
    def qualified_count(self) -> int:
        return len(self.qualified_candidates)

    @property
    def qualification_rate(self) -> Decimal:
        if self.total_candidates == 0:
            return Decimal(0)
        return _q(
            Decimal(self.qualified_count) / Decimal(self.total_candidates),
            "0.001",
        )


# --------------------------------------------------------------------------
# 2. Peer Selection vs. Mass Electoral Voting
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class SelectionComparison:
    peer_panel_size: int = 25              # 20-30 senior practitioners in field
    peer_consensus_threshold: float = 0.75 # 75% consensus requirement
    peer_error_rate: float = 0.04          # ~4% error rate from direct observation
    electoral_voter_count: int = 10000     # Mass voting public
    electoral_information_deficit: float = 0.65 # Public reliance on rhetoric/bias
    electoral_error_rate: float = 0.48     # Near random / patronage outcome

    @property
    def competence_advantage_ratio(self) -> Decimal:
        """Ratio of selection accuracy: peer assessment vs mass ballot."""
        peer_accuracy = 1.0 - self.peer_error_rate
        electoral_accuracy = 1.0 - self.electoral_error_rate
        return _q(Decimal(str(peer_accuracy)) / Decimal(str(electoral_accuracy)), "0.01")


# --------------------------------------------------------------------------
# 3. Functional Leadership Council Roles
# --------------------------------------------------------------------------


class RoleDomain(str, Enum):
    COORDINATION = "coordination"
    TREASURY = "treasury"
    ECONOMY = "economy"
    EDUCATION = "education"
    HEALTH = "health"
    WORKS = "works"
    SECURITY = "security"
    DEFENSE = "defense"
    JUSTICE = "justice"
    DIPLOMACY = "diplomacy"


@dataclass(frozen=True)
class CouncilRole:
    title: str
    domain: RoleDomain
    term_years: int
    probation_years: int
    selected_from: str
    mandate: str
    key_metrics: tuple[str, ...]
    is_collective_body: bool = False
    min_members: int = 1
    max_members: int = 1
    mandatory_female_min: int = 0


COUNCIL_ROLES: tuple[CouncilRole, ...] = (
    CouncilRole(
        title="The Coordinator",
        domain=RoleDomain.COORDINATION,
        term_years=3,
        probation_years=1,
        selected_from="Senior practitioners with cross-functional experience in >= 3 departments",
        mandate="Overall inter-departmental coordination; external representation; council chair (no unilateral decrees)",
        key_metrics=(
            "Total community production output",
            "Dispute resolution completion rate",
            "External threat early warning and prevention",
        ),
    ),
    CouncilRole(
        title="The Deputy Coordinator",
        domain=RoleDomain.COORDINATION,
        term_years=3,
        probation_years=1,
        selected_from="Selected by Coordinator from qualification pool; confirmed by 75% Council vote",
        mandate="Shadows Coordinator; manages day-to-day operations; assumes Coordinator post instantly on vacancy",
        key_metrics=(
            "Operational efficiency index",
            "Cross-department task completion rate",
            "Institutional continuity readiness",
        ),
    ),
    CouncilRole(
        title="The Steward of Reserves",
        domain=RoleDomain.TREASURY,
        term_years=4,
        probation_years=1,
        selected_from="Senior warehouse managers, forensic inspectors, currency operators",
        mandate="Manages commodity warehouses, reserve physical adequacy, and RCU note 100% collateral backing",
        key_metrics=(
            "Reserve collateral backing adequacy ratio",
            "Warehouse physical spoilage and loss rate (< 2%)",
            "Note counterfeit and grade fraud detection rate",
        ),
    ),
    CouncilRole(
        title="The Steward of Production",
        domain=RoleDomain.ECONOMY,
        term_years=4,
        probation_years=1,
        selected_from="Senior agricultural masters, fabrication leads, trade cooperative heads",
        mandate="Directs productive output (farming, manufacturing, energy); oversees import substitution ladder",
        key_metrics=(
            "Net agricultural and manufacturing tonnage",
            "Import substitution progress (FX savings)",
            "Productive employment and apprentice placement rate",
        ),
    ),
    CouncilRole(
        title="The Steward of Knowledge",
        domain=RoleDomain.EDUCATION,
        term_years=4,
        probation_years=1,
        selected_from="Senior guild masters from the apprenticeship system",
        mandate="Oversees 4-year apprenticeship programs, technical libraries, and knowledge preservation archives",
        key_metrics=(
            "Apprentice graduation rate and master competency test scores",
            "Critical skill coverage ratio across the community",
            "Knowledge archive completeness and resilience",
        ),
    ),
    CouncilRole(
        title="The Steward of Health",
        domain=RoleDomain.HEALTH,
        term_years=4,
        probation_years=1,
        selected_from="Senior medical practitioners (physicians, herbalists, midwives)",
        mandate="Oversees clinical network, preventive health, maternal care, and emergency epidemic control",
        key_metrics=(
            "Infant and maternal mortality rates",
            "Infectious disease incidence rate",
            "Essential medicine buffer reserve (minimum 128 days)",
        ),
    ),
    CouncilRole(
        title="The Steward of Infrastructure",
        domain=RoleDomain.WORKS,
        term_years=4,
        probation_years=1,
        selected_from="Senior builders, civil engineers, water and energy specialists",
        mandate="Maintains and expands physical infrastructure: water reticulation, renewable energy, roads, and fortifications",
        key_metrics=(
            "Clean water access percentage",
            "Electrical microgrid uptime percentage",
            "Road and defensive works condition index",
        ),
    ),
    CouncilRole(
        title="The Steward of Security",
        domain=RoleDomain.SECURITY,
        term_years=3,
        probation_years=1,
        selected_from="Senior security cooperative members with mediation and forensic experience",
        mandate="Oversees Community Security Cooperative: mediation (65%), forensics (14%), and non-lethal order (21%)",
        key_metrics=(
            "Community dispute mediation settlement rate (> 80%)",
            "Violent crime and property theft rate",
            "Community safety and trust index",
        ),
    ),
    CouncilRole(
        title="The War Council",
        domain=RoleDomain.DEFENSE,
        term_years=5,
        probation_years=1,
        selected_from="Senior militia commanders, tacticians, and logistics masters (staggered rotation)",
        mandate="5–7 member collective defense body; militia training, 24-hr mobilization, asymmetric defense",
        key_metrics=(
            "24-hour mobilization drill readiness score",
            "Militia annual marksmanship qualification rate (> 90%)",
            "Layered anti-drone and anti-armor defense readiness",
        ),
        is_collective_body=True,
        min_members=5,
        max_members=7,
        mandatory_female_min=2,
    ),
    CouncilRole(
        title="The Steward of Justice",
        domain=RoleDomain.JUSTICE,
        term_years=5,
        probation_years=1,
        selected_from="Community elders and legal mediation specialists with 10+ years experience",
        mandate="Administers judicial appeals, investigates leadership misconduct, interprets constitutional charters",
        key_metrics=(
            "Appeals resolution time (< 30 days)",
            "Judicial integrity and impartiality index",
            "Zero backlog in major property and fraud cases",
        ),
    ),
    CouncilRole(
        title="The Steward of Relations",
        domain=RoleDomain.DIPLOMACY,
        term_years=3,
        probation_years=1,
        selected_from="Experienced negotiators with multi-lingual and inter-regional relationships",
        mandate="Manages external diplomacy, bilateral trade corridors, non-aggression pacts, and early threat warning",
        key_metrics=(
            "Bilateral trade and barter agreements secured",
            "Cross-border conflict avoidance and peaceful de-escalation",
            "External threat early-warning lead time",
        ),
    ),
)


# --------------------------------------------------------------------------
# 4. Probation & Succession State Machine
# --------------------------------------------------------------------------


class SuccessionTrigger(str, Enum):
    NORMAL_TERM_EXPIRY = "normal_term_expiry"
    DEATH_OR_INCAPACITATION = "death_or_incapacitation"
    REMOVAL_INCOMPETENCE = "removal_incompetence"
    REMOVAL_CORRUPTION = "removal_corruption"
    VOLUNTARY_RESIGNATION = "voluntary_resignation"


@dataclass(frozen=True)
class SuccessionProtocol:
    trigger: SuccessionTrigger
    lead_time_days: int
    immediate_successor: str
    selection_window_days: int
    power_vacuum_days: int
    public_disruption_level: str


SUCCESSION_RULES: dict[SuccessionTrigger, SuccessionProtocol] = {
    SuccessionTrigger.NORMAL_TERM_EXPIRY: SuccessionProtocol(
        trigger=SuccessionTrigger.NORMAL_TERM_EXPIRY,
        lead_time_days=180,  # 6 months prior
        immediate_successor="Incoming selected candidate (after 90-day shadow overlap)",
        selection_window_days=180,
        power_vacuum_days=0,
        public_disruption_level="Zero — institutional handover",
    ),
    SuccessionTrigger.DEATH_OR_INCAPACITATION: SuccessionProtocol(
        trigger=SuccessionTrigger.DEATH_OR_INCAPACITATION,
        lead_time_days=0,
        immediate_successor="Deputy Coordinator assumes role instantly",
        selection_window_days=30,  # Pick new Deputy in 30 days
        power_vacuum_days=0,
        public_disruption_level="Zero — immediate continuity",
    ),
    SuccessionTrigger.REMOVAL_INCOMPETENCE: SuccessionProtocol(
        trigger=SuccessionTrigger.REMOVAL_INCOMPETENCE,
        lead_time_days=0,
        immediate_successor="Deputy assumes role; 75% Council vote triggers replacement",
        selection_window_days=30,
        power_vacuum_days=0,
        public_disruption_level="Low — scheduled review outcome",
    ),
    SuccessionTrigger.REMOVAL_CORRUPTION: SuccessionProtocol(
        trigger=SuccessionTrigger.REMOVAL_CORRUPTION,
        lead_time_days=0,
        immediate_successor="Deputy assumes role; corrupt leader arrested & permanently banned",
        selection_window_days=30,
        power_vacuum_days=0,
        public_disruption_level="Low — judicial enforcement",
    ),
    SuccessionTrigger.VOLUNTARY_RESIGNATION: SuccessionProtocol(
        trigger=SuccessionTrigger.VOLUNTARY_RESIGNATION,
        lead_time_days=30,
        immediate_successor="Deputy assumes role immediately",
        selection_window_days=30,
        power_vacuum_days=0,
        public_disruption_level="Zero — seamless transition",
    ),
}


# --------------------------------------------------------------------------
# 5. Departmental Policing, Enforcers & Measurement Bureaus
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class DepartmentInspectionBranch:
    department: RoleDomain
    enforcement_unit_name: str
    mandate: str
    staff_percentage: Decimal           # Percentage of department staff assigned to policing/audit
    independent_measurement_unit: str
    primary_risks_policed: tuple[str, ...]


DEPARTMENTAL_POLICING_SYSTEM: tuple[DepartmentInspectionBranch, ...] = (
    DepartmentInspectionBranch(
        department=RoleDomain.DEFENSE,
        enforcement_unit_name="Military Police (Internal Provost)",
        mandate="Enforces rules of engagement; prevents looting, atrocities, abuse of civilians/POWs, and illicit arms sales",
        staff_percentage=Decimal("0.035"), # 3.5% of defense forces
        independent_measurement_unit="Defense Readiness & Inventory Telemetry Bureau",
        primary_risks_policed=(
            "Looting and property destruction in operational areas",
            "Atrocities or unlawful physical abuse of civilians/captives",
            "Black-market diversion of ammunition, fuel, or weapons",
            "Unauthorized command actions outside Council authorization",
        ),
    ),
    DepartmentInspectionBranch(
        department=RoleDomain.TREASURY,
        enforcement_unit_name="Warehouse Forensic Inspectorate",
        mandate="Continuous physical stock audits, grain moisture checks, seal integrity, and ledger reconciliation",
        staff_percentage=Decimal("0.050"), # 5.0% of treasury personnel
        independent_measurement_unit="Independent Commodity Verification Bureau",
        primary_risks_policed=(
            "Hoarding or unauthorized skimming of grain and metals",
            "Grade inflation and falsification of warehouse receipts",
            "Collusion between depositors and warehouse gatekeepers",
            "Theft or illicit outflow of physical collateral",
        ),
    ),
    DepartmentInspectionBranch(
        department=RoleDomain.ECONOMY,
        enforcement_unit_name="Production Standards & Material Inspectorate",
        mandate="Enforces quality specs on tools, food processing hygiene, and energy grid safety; verifies output figures",
        staff_percentage=Decimal("0.030"), # 3.0% of production workers
        independent_measurement_unit="Output Metrics & Material Telemetry Bureau",
        primary_risks_policed=(
            "Falsification of agricultural yields or manufacturing counts",
            "Black-market sale of subsidized community raw materials",
            "Substandard construction or adulterated food processing",
            "Favoritism in apprentice allocation and tool distribution",
        ),
    ),
    DepartmentInspectionBranch(
        department=RoleDomain.HEALTH,
        enforcement_unit_name="Medical Ethics & Pharmaceutical Auditor",
        mandate="Controls narcotics, antibiotic stewardship, sterility compliance, and clinical fee prohibitions",
        staff_percentage=Decimal("0.040"), # 4.0% of health staff
        independent_measurement_unit="Clinical Outcomes & Morbidity Statistics Bureau",
        primary_risks_policed=(
            "Theft and private resale of imported critical medicines",
            "Counterfeit or sub-potent compounding (oxygen/ORS purity)",
            "Charging unauthorized private fees for community care",
            "Neglect of rural triage clinics in favor of central nodes",
        ),
    ),
    DepartmentInspectionBranch(
        department=RoleDomain.WORKS,
        enforcement_unit_name="Civil Works & Quality Assurance Bureau",
        mandate="Inspects structural safety, water purity testing, fuel storage safety, and project cost accounting",
        staff_percentage=Decimal("0.030"), # 3.0% of infrastructure staff
        independent_measurement_unit="Infrastructure Performance & Water Telemetry Bureau",
        primary_risks_policed=(
            "Use of substandard concrete, timber, or wiring in works",
            "Diversion of fuel, solar equipment, or pipe for private use",
            "Falsifying water purity or microgrid reliability metrics",
            "Ghost labour reporting on civil construction projects",
        ),
    ),
)


@dataclass(frozen=True)
class MeasurementBureau:
    """Independent Recording and Telemetry Architecture.

    Measurement units do NOT report to the steward or manager they measure.
    They report directly to the Audit Board and Steward of Justice.
    This breaks Goodhart's Law and prevents departmental metric falsification.
    """
    total_department_staff: int = 1000
    auditor_share: Decimal = Decimal("0.035") # 3.5% average across all bureaus

    @property
    def dedicated_auditors_count(self) -> int:
        return int(Decimal(str(self.total_department_staff)) * self.auditor_share)

    @property
    def reporting_independence(self) -> bool:
        """True by constitutional charter: reports to Audit Board, not department head."""
        return True


# --------------------------------------------------------------------------
# 6. Sortition Audit & Anti-Monarchy Accountability
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class SortitionAudit:
    """Annual Community Audit by 20 Random Citizens (Lottery Selection)."""

    jury_size: int = 20
    audit_scope: tuple[str, ...] = (
        "Physical inspection of 100% of grain and metal vaults",
        "Public ledger transaction and issuance reconciliation",
        "Interviews with 50 randomly chosen apprentices and patients",
        "Inspection of leadership living quarters (verifying equal conditions)",
        "Review of all disciplinary and use-of-force logs",
    )
    confidence_level: Decimal = Decimal("0.95")  # 95% statistical detection of systemic anomalies

    @property
    def leader_immunity_status(self) -> bool:
        """Zero legal immunity: leaders face identical judicial tribunals."""
        return False

    @property
    def living_condition_ratio(self) -> Decimal:
        """Ratio of leader living standard to average guild master: exactly 1.0."""
        return Decimal("1.00")
