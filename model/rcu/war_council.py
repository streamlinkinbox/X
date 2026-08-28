"""War Council, Scenario Planning, and Specialized Strike Units.

This module models the command, contingency planning, and specialized operational
architecture for an independent community:
1. ``WarCouncil`` -- 8-member deliberative decision body balancing strategic,
   intelligence, environmental, economic, justice, and civilian perspectives.
2. ``DecisionEngine`` -- voting thresholds, consensus rules, the 24-hour "No" delay rule,
   the 7/8 supermajority "Blood" rule (civilian casualties > 10), and the defensive-only
   Community Council offensive authorization constraint.
3. ``ScenarioLibrary`` -- 10 pre-planned threat responses (S1 to S10) covering raids,
   invasions, floods, droughts, epidemics, internal coups, cyber/ledger attacks, and CBRN.
4. ``WarRoom`` -- Chinese "Genius Council" multidisciplinary crisis session (8-15 minds,
   24-72 hours, no rank, mandatory sleep, external wildcards).
5. ``SpecializedUnits`` -- 7 precision units (Strike Team, Hammer, Scorpion, Worm,
   Healer, Echo, Horse) totalling 155-195 personnel (<5% of militia).
6. ``AntiCasteSafeguards`` -- firewalls against Praetorian / Janissary / Mamluk caste
   capture (mandatory <=3 yr civilian rotation, no hereditary status, no separate barracks).
7. ``BattleSimulation`` -- integrated combat timeline and loss/neutralization ratios.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# --------------------------------------------------------------------------
# 1. War Council Structure & Roles
# --------------------------------------------------------------------------


class WarCouncilRole(str, Enum):
    CHAIR = "chair"                                  # Rotating 3-month facilitator
    DEFENSE_COORDINATOR = "defense_coordinator"      # Militia readiness & strategy
    CIS_CHIEF = "cis_chief"                          # External intelligence picture
    EDMB_CHIEF = "edmb_chief"                        # Environmental, weather & terrain
    RAB_CHIEF = "rab_chief"                          # Economic, logistics & cost modeling
    SENIOR_MILITIA_CMD = "senior_militia_commander"  # Rank-and-file readiness & morale
    JUSTICE_COORDINATOR = "justice_coordinator"      # Law, ethics, anti-atrocity compliance
    COMMUNITY_REP = "community_representative"       # Civilian sortition delegate (monthly)


@dataclass(frozen=True)
class WarCouncilMember:
    role: WarCouncilRole
    title: str
    rotation_months: int
    primary_perspective: str
    veto_or_delay_power: bool = True


WAR_COUNCIL_ROSTER: tuple[WarCouncilMember, ...] = (
    WarCouncilMember(
        role=WarCouncilRole.CHAIR,
        title="Council Chair (Rotating)",
        rotation_months=3,
        primary_perspective="Deliberation facilitation, deadlock resolution, procedural order",
    ),
    WarCouncilMember(
        role=WarCouncilRole.DEFENSE_COORDINATOR,
        title="Defense Coordinator",
        rotation_months=12,
        primary_perspective="Overall asymmetric military strategy, militia force readiness",
    ),
    WarCouncilMember(
        role=WarCouncilRole.CIS_CHIEF,
        title="CIS Chief of Intelligence",
        rotation_months=24,
        primary_perspective="External threat vectors, adversary troop staging, logistics",
    ),
    WarCouncilMember(
        role=WarCouncilRole.EDMB_CHIEF,
        title="EDMB Chief Environmental Officer",
        rotation_months=24,
        primary_perspective="Topography, weather, seasonal flood/landslide risk, terrain defense",
    ),
    WarCouncilMember(
        role=WarCouncilRole.RAB_CHIEF,
        title="RAB Chief Analyst",
        rotation_months=24,
        primary_perspective="Resource burn rate, supply chain sustainability, cost limits",
    ),
    WarCouncilMember(
        role=WarCouncilRole.SENIOR_MILITIA_CMD,
        title="Senior Militia Commander (Rotating)",
        rotation_months=6,
        primary_perspective="Rank-and-file tactical readiness, ground morale, equipment status",
    ),
    WarCouncilMember(
        role=WarCouncilRole.JUSTICE_COORDINATOR,
        title="Justice Coordinator",
        rotation_months=12,
        primary_perspective="Geneva/customary law compliance, anti-atrocity, captive treatment",
    ),
    WarCouncilMember(
        role=WarCouncilRole.COMMUNITY_REP,
        title="Community Representative (Sortition)",
        rotation_months=1,
        primary_perspective="Civilian consent, popular support, public impact evaluation",
    ),
)


# --------------------------------------------------------------------------
# 2. Decision Engine & Voting Rules
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class WarDecisionProposal:
    proposal_id: str
    description: str
    is_offensive_action: bool
    predicted_civilian_casualties: int
    rab_economic_burn_acceptable: bool
    justice_compliance_verified: bool
    is_reversible: bool
    community_council_authorized: bool = False  # Mandatory for offensive operations


@dataclass(frozen=True)
class CouncilVoteResult:
    approved: bool
    votes_in_favor: int
    total_votes: int
    delayed_by_no_rule: bool
    rejection_reason: Optional[str] = None


class WarCouncilDecisionEngine:
    COUNCIL_SIZE: int = 8
    STANDARD_MAJORITY_THRESHOLD: int = 5     # 5 of 8
    BLOOD_RULE_SUPERMAJORITY: int = 7         # 7 of 8 if civilian casualties > 10

    @classmethod
    def evaluate_proposal(
        cls,
        proposal: WarDecisionProposal,
        votes_in_favor: int,
        member_invoking_24h_delay: bool = False,
    ) -> CouncilVoteResult:
        if member_invoking_24h_delay:
            return CouncilVoteResult(
                approved=False,
                votes_in_favor=votes_in_favor,
                total_votes=cls.COUNCIL_SIZE,
                delayed_by_no_rule=True,
                rejection_reason="Delayed for 24 hours under the mandatory 'No' reflection rule",
            )

        # 1. Defensive-only constraint: Offensive actions strictly require Community Council assent
        if proposal.is_offensive_action and not proposal.community_council_authorized:
            return CouncilVoteResult(
                approved=False,
                votes_in_favor=votes_in_favor,
                total_votes=cls.COUNCIL_SIZE,
                delayed_by_no_rule=False,
                rejection_reason="Offensive military action lacks explicit Community Council authorization",
            )

        # 2. Justice and Anti-Atrocity Compliance
        if not proposal.justice_compliance_verified:
            return CouncilVoteResult(
                approved=False,
                votes_in_favor=votes_in_favor,
                total_votes=cls.COUNCIL_SIZE,
                delayed_by_no_rule=False,
                rejection_reason="Operation violates customary law or anti-atrocity compliance checks",
            )

        # 3. RAB Economic Cost Rule
        if not proposal.rab_economic_burn_acceptable:
            return CouncilVoteResult(
                approved=False,
                votes_in_favor=votes_in_favor,
                total_votes=cls.COUNCIL_SIZE,
                delayed_by_no_rule=False,
                rejection_reason="RAB assessment indicates operation exceeds sustainable resource burn rate",
            )

        # 4. The "Blood Rule": civilian casualties > 10 requires 7/8 supermajority
        required_threshold = (
            cls.BLOOD_RULE_SUPERMAJORITY
            if proposal.predicted_civilian_casualties > 10
            else cls.STANDARD_MAJORITY_THRESHOLD
        )

        if votes_in_favor >= required_threshold:
            return CouncilVoteResult(
                approved=True,
                votes_in_favor=votes_in_favor,
                total_votes=cls.COUNCIL_SIZE,
                delayed_by_no_rule=False,
            )
        else:
            return CouncilVoteResult(
                approved=False,
                votes_in_favor=votes_in_favor,
                total_votes=cls.COUNCIL_SIZE,
                delayed_by_no_rule=False,
                rejection_reason=f"Insufficient votes ({votes_in_favor}/{cls.COUNCIL_SIZE}; required {required_threshold})",
            )


# --------------------------------------------------------------------------
# 3. The Living Scenario Library (Roman Contingency Model)
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class ThreatScenario:
    code: str
    name: str
    adversary_scale: str
    early_warning_lead_time: str
    primary_response_phase: str
    active_specialized_units: tuple[str, ...]
    militia_mobilization_scale: int
    reversibility: str


SCENARIO_LIBRARY: tuple[ThreatScenario, ...] = (
    ThreatScenario(
        code="S1",
        name="Small armed raid",
        adversary_scale="10–50 raiders",
        early_warning_lead_time="1–4 hours",
        primary_response_phase="Local militia (20–30) + Horse scouts; 5 km max pursuit",
        active_specialized_units=("The Horse", "The Healer"),
        militia_mobilization_scale=30,
        reversibility="High (quick local disengagement)",
    ),
    ThreatScenario(
        code="S2",
        name="Medium coordinated assault",
        adversary_scale="100–500 fighters + light vehicles",
        early_warning_lead_time="2–6 hours",
        primary_response_phase="Defense in depth (3 layers); IED fields; drone net defense; Hammer counter-strike",
        active_specialized_units=("The Hammer", "The Scorpion", "The Worm", "The Echo", "The Strike Team", "The Healer", "The Horse"),
        militia_mobilization_scale=2000,
        reversibility="Moderate (staged defensive fallback)",
    ),
    ThreatScenario(
        code="S3",
        name="Large-scale invasion",
        adversary_scale="1,000+ fighters + armor + air support",
        early_warning_lead_time="12–48 hours",
        primary_response_phase="Full asymmetric transition: underground caches, decapitation raids, tank blinding, protracted guerrilla warfare",
        active_specialized_units=("Strike Team", "The Hammer", "The Scorpion", "The Worm", "The Echo", "The Healer", "The Horse"),
        militia_mobilization_scale=3500,
        reversibility="Low (existential defense commitment)",
    ),
    ThreatScenario(
        code="S4",
        name="Flash flood / River breach",
        adversary_scale="Ecological flood wave",
        early_warning_lead_time="24–72 hours",
        primary_response_phase="EDMB Red alert; high-ground evacuation; reserve vault waterproofing; water purification",
        active_specialized_units=("The Worm", "The Healer", "The Horse"),
        militia_mobilization_scale=200,
        reversibility="High (civil recovery)",
    ),
    ThreatScenario(
        code="S5",
        name="Multi-season drought",
        adversary_scale="Prolonged hydrological deficit",
        early_warning_lead_time="3–6 months",
        primary_response_phase="Water rationing; drought-crop rotation; RAB food security runway; border water conflict monitoring",
        active_specialized_units=("The Echo",),
        militia_mobilization_scale=50,
        reversibility="High (agricultural policy adjustment)",
    ),
    ThreatScenario(
        code="S6",
        name="Epidemic / Vector outbreak",
        adversary_scale="Pathogen / Vector spike",
        early_warning_lead_time="2–4 weeks",
        primary_response_phase="Sector quarantine; medical triage; vector spraying; transparent civic communications",
        active_specialized_units=("The Healer", "The Worm"),
        militia_mobilization_scale=100,
        reversibility="High (staged de-escalation)",
    ),
    ThreatScenario(
        code="S7",
        name="Internal coup attempt",
        adversary_scale="Rogue faction / mutiny",
        early_warning_lead_time="0–12 hours",
        primary_response_phase="Secure warehouses and communications; isolate rogue leaders non-lethally; justice tribunal",
        active_specialized_units=("The Echo", "Strike Team"),
        militia_mobilization_scale=500,
        reversibility="Moderate (due process adjudication)",
    ),
    ThreatScenario(
        code="S8",
        name="External trade route closure",
        adversary_scale="Hostile economic embargo",
        early_warning_lead_time="1–4 weeks",
        primary_response_phase="RAB economic buffer activation; production substitution ladder; diplomatic envoy dispatch",
        active_specialized_units=("The Horse", "The Echo"),
        militia_mobilization_scale=50,
        reversibility="High (diplomatic resolution)",
    ),
    ThreatScenario(
        code="S9",
        name="Cyber / Digital ledger attack",
        adversary_scale="Electronic state / cartel hackers",
        early_warning_lead_time="Minutes to hours",
        primary_response_phase="Isolate network nodes; revert to offline physical note ledger; trace intrusion origin",
        active_specialized_units=("The Echo",),
        militia_mobilization_scale=20,
        reversibility="High (system isolation and cryptographic rebuild)",
    ),
    ThreatScenario(
        code="S10",
        name="CBRN (Chemical/Biological/Radiological/Nuclear) attack",
        adversary_scale="Asymmetric / WMD strike",
        early_warning_lead_time="Minutes to hours",
        primary_response_phase="Underground shelter seal; positive air filtration; decontamination; survival cache distribution",
        active_specialized_units=("The Healer", "The Worm", "The Echo"),
        militia_mobilization_scale=1000,
        reversibility="Low (severe catastrophe management)",
    ),
)


# --------------------------------------------------------------------------
# 4. The War Room ("Genius Council")
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class WarRoomRules:
    no_rank_equality: bool = True
    no_finality_rule: bool = True
    write_everything_down: bool = True
    mandatory_sleep_hours: int = 6
    food_and_water_guaranteed: bool = True
    total_communication_isolation: bool = True
    min_duration_hours: int = 24
    max_duration_hours: int = 72
    min_participants: int = 8
    max_participants: int = 15


@dataclass(frozen=True)
class WarRoomParticipant:
    name: str
    role_category: str  # "commander", "intelligence", "environmental", "logistics", "engineering", "medical", "wildcard"
    expertise: str


# --------------------------------------------------------------------------
# 5. Specialized Units Architecture (Elite in Skill, Not in Status)
# --------------------------------------------------------------------------


class SpecializedUnitType(str, Enum):
    STRIKE_TEAM = "strike_team"      # Decapitation / target command neutralizer (4)
    THE_HAMMER = "the_hammer"        # Shock assault / rapid breakthrough (40)
    THE_SCORPION = "the_scorpion"    # Counter-drone / air defense (20-30)
    THE_WORM = "the_worm"            # Sappers / IEDs / engineering / traps (20-30)
    THE_HEALER = "the_healer"        # Combat trauma medical / triage (10-15)
    THE_ECHO = "the_echo"            # Comms / EW jamming / cyber (10-15)
    THE_HORSE = "the_horse"          # Mounted recon / rapid response / supply (30-50)


@dataclass(frozen=True)
class SpecializedUnitSpec:
    unit_type: SpecializedUnitType
    name: str
    min_size: int
    max_size: int
    nominal_size: int
    mission: str
    operational_limit: str
    max_service_years: int = 3
    training_duration_months: int = 3


SPECIALIZED_UNITS_ROSTER: tuple[SpecializedUnitSpec, ...] = (
    SpecializedUnitSpec(
        unit_type=SpecializedUnitType.STRIKE_TEAM,
        name="The Strike Team (Target Command Neutralizer)",
        min_size=4,
        max_size=8,
        nominal_size=4,
        mission="Infiltrate behind lines to eliminate high-value command/radio elements during active defense",
        operational_limit="72-hour maximum mission exfiltration limit; abort if encountering >5 hostiles",
        max_service_years=3,
        training_duration_months=6,
    ),
    SpecializedUnitSpec(
        unit_type=SpecializedUnitType.THE_HAMMER,
        name="The Hammer (Shock Assault)",
        min_size=30,
        max_size=50,
        nominal_size=40,
        mission="Concentrated 10-20 minute shock charge to shatter enemy line for militia breakthrough",
        operational_limit="Deployed max once per 30 days; 2 km max pursuit; flanked by militia battalion",
        max_service_years=3,
        training_duration_months=3,
    ),
    SpecializedUnitSpec(
        unit_type=SpecializedUnitType.THE_SCORPION,
        name="The Scorpion (Counter-Drone & Air Defense)",
        min_size=20,
        max_size=30,
        nominal_size=25,
        mission="Layered drone neutralization (500m wires, 200m smoke, 100m nets, 50m shotguns)",
        operational_limit="Strict anti-air focus; falls back to militia line if ground infantry advances",
        max_service_years=3,
        training_duration_months=2,
    ),
    SpecializedUnitSpec(
        unit_type=SpecializedUnitType.THE_WORM,
        name="The Worm (Sappers, IEDs & Fortification)",
        min_size=20,
        max_size=30,
        nominal_size=25,
        mission="Construct hidden IED fields, ditch traps, caltrops, underground bunkers, and demolitions",
        operational_limit="Operates under night/smoke cover; zero standalone direct fire engagement",
        max_service_years=3,
        training_duration_months=3,
    ),
    SpecializedUnitSpec(
        unit_type=SpecializedUnitType.THE_HEALER,
        name="The Healer (Combat Trauma Medical)",
        min_size=10,
        max_size=15,
        nominal_size=12,
        mission="Field triage, emergency trauma surgery, blood storage, and casualty evacuation",
        operational_limit="Treats friend and wounded enemy alike; protected by dedicated 4-man security",
        max_service_years=3,
        training_duration_months=2,
    ),
    SpecializedUnitSpec(
        unit_type=SpecializedUnitType.THE_ECHO,
        name="The Echo (Signals, Electronic Warfare & Cyber)",
        min_size=10,
        max_size=15,
        nominal_size=12,
        mission="Mesh radio network maintenance, RF jamming of enemy comms, cyber defense of currency ledger",
        operational_limit="Continuous operation; first to deploy and last to de-escalate",
        max_service_years=3,
        training_duration_months=2,
    ),
    SpecializedUnitSpec(
        unit_type=SpecializedUnitType.THE_HORSE,
        name="The Horse (Mounted Recon & Rapid Logistics)",
        min_size=30,
        max_size=50,
        nominal_size=40,
        mission="Early perimeter scouting, rapid tactical response, courier messaging, and frontline supply",
        operational_limit="5 km max pursuit; disengages immediately when encountering heavy infantry",
        max_service_years=3,
        training_duration_months=2,
    ),
)


@dataclass(frozen=True)
class SpecializedUnitSizing:
    population: int = 10000
    militia_size: int = 3500

    @property
    def total_specialized_nominal(self) -> int:
        return sum(u.nominal_size for u in SPECIALIZED_UNITS_ROSTER)

    @property
    def total_specialized_min(self) -> int:
        return sum(u.min_size for u in SPECIALIZED_UNITS_ROSTER)

    @property
    def total_specialized_max(self) -> int:
        return sum(u.max_size for u in SPECIALIZED_UNITS_ROSTER)

    @property
    def fraction_of_militia(self) -> float:
        return self.total_specialized_nominal / max(self.militia_size, 1)

    @property
    def fraction_of_population(self) -> float:
        return self.total_specialized_nominal / max(self.population, 1)


# --------------------------------------------------------------------------
# 6. Anti-Caste Safeguards (Anti-Praetorian / Anti-Janissary / Anti-Mamluk)
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class AntiCasteSafeguards:
    max_consecutive_service_years: int = 3       # Mandatory return to civilian economic production
    separate_barracks_allowed: bool = False      # Operators live in community homes
    separate_pay_or_privilege: bool = False      # Equal standard compensation
    hereditary_recruitment_allowed: bool = False # Merit and sortition-based entry only
    holding_civilian_political_office: bool = False # Absolute separation of military & civil rule
    right_of_refusal_for_offensive_action: bool = True # Legal right to refuse illegal offensive war
    no_elite_branding_names: bool = True         # Named strictly by operational function


# --------------------------------------------------------------------------
# 7. Integrated Combat Timeline & Simulation
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class EngagementBattleReport:
    enemy_initial_force: int = 500
    enemy_tanks: int = 5
    enemy_drones: int = 20
    community_militia_deployed: int = 2000
    specialized_operators_deployed: int = 158
    enemy_casualties_killed: int = 200
    enemy_casualties_captured: int = 150
    enemy_tanks_neutralized: int = 5
    enemy_drones_neutralized: int = 20
    community_militia_killed: int = 30
    community_militia_wounded: int = 80
    commander_eliminated_by_strike_team: bool = True

    @property
    def enemy_attrition_rate(self) -> float:
        total_neutralized = self.enemy_casualties_killed + self.enemy_casualties_captured
        return total_neutralized / max(self.enemy_initial_force, 1)

    @property
    def casualty_exchange_ratio(self) -> float:
        enemy_losses = self.enemy_casualties_killed + self.enemy_casualties_captured
        community_losses = self.community_militia_killed + self.community_militia_wounded
        return enemy_losses / max(community_losses, 1)
