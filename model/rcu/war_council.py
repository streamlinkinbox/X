"""War Council, Scenario Planning, and Specialized Strike Units: Elite in Skill, Not in Status.

This module models the command, contingency planning, and specialized operational
architecture for an independent community:
1. ``WarCouncil`` -- 7-seat deliberative decision body (Strategist, Intelligence,
   Operations, Logistics, Deception, Terrain, Community Liaison).
2. ``DecisionEngine`` -- voting thresholds (4/7 majority, 6/7 Blood Rule for civilian
   casualties > 10, 24-hr "No" reflection delay, Logistics Officer Cost Veto, and
   Community Liaison Offensive Veto).
3. ``DefenseDoctrine`` -- "Don't Mirror, Don't Chase, Don't Hold", Strike the System,
   Deception First, and Mobility > Numbers.
4. ``ScenarioLibrary`` -- 10 pre-planned threat responses (S1 to S10) covering raids,
   invasions, floods, droughts, epidemics, internal coups, cyber/ledger attacks, and CBRN.
5. ``WarRoom`` -- Chinese "Genius Council" multidisciplinary crisis session (8-15 minds,
   24-72 hours, no rank, mandatory sleep, external wildcards).
6. ``SpecializedUnits`` -- Functional naming, lean sizing (155-195 personnel, <5% of militia),
   and skill-distribution mechanics.
7. ``AntiCasteSafeguards`` -- 7 constitutional firewalls against Praetorian / Janissary /
   Mamluk degeneration (mandatory 2-3 yr rotation, no separate barracks, no separate pay).
8. ``BattleSimulation`` -- integrated combat timeline and loss/neutralization ratios.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# --------------------------------------------------------------------------
# 1. The Seven Seats of the War Council
# --------------------------------------------------------------------------


class WarCouncilRole(str, Enum):
    STRATEGIST = "strategist"                  # Rotating chair (6m), long-term strategy (3-5 moves ahead)
    INTELLIGENCE_OFFICER = "intelligence_officer" # Links directly to CIS, adversary tracking
    OPERATIONS_OFFICER = "operations_officer"  # Plans into action, unit timing, deployment, extraction
    LOGISTICS_OFFICER = "logistics_officer"    # Supply, ammo, fuel, food, routes, fallback; COST VETO
    DECEPTION_OFFICER = "deception_officer"    # Feints, decoys, misinformation, false radio traffic
    TERRAIN_OFFICER = "terrain_officer"        # Topography, rivers, ridges, passes within 100km
    COMMUNITY_LIAISON = "community_liaison"    # Civilian firewall, ensures mandate, OFFENSIVE VETO


@dataclass(frozen=True)
class WarCouncilMember:
    role: WarCouncilRole
    title: str
    rotation_months: int
    primary_perspective: str
    why_seat_exists: str
    has_specific_veto: bool = False
    veto_scope: Optional[str] = None


WAR_COUNCIL_ROSTER: tuple[WarCouncilMember, ...] = (
    WarCouncilMember(
        role=WarCouncilRole.STRATEGIST,
        title="Strategist (Rotating Chair)",
        rotation_months=6,
        primary_perspective="Overall strategy, contingency planning, long-term thinking 3–5 moves ahead",
        why_seat_exists="Ensures community fights the war it can win, not the war the enemy wants",
    ),
    WarCouncilMember(
        role=WarCouncilRole.INTELLIGENCE_OFFICER,
        title="Intelligence Officer",
        rotation_months=24,
        primary_perspective="Direct CIS link; enemy movements, numbers, morale, supply lines, intentions",
        why_seat_exists="No decision without intelligence; prevents guesswork that gets people killed",
    ),
    WarCouncilMember(
        role=WarCouncilRole.OPERATIONS_OFFICER,
        title="Operations Officer",
        rotation_months=12,
        primary_perspective="Turns plans into action; coordinates units, timing, deployment, extraction",
        why_seat_exists="Prevents plans from remaining theoretical ideas that fail on contact with reality",
    ),
    WarCouncilMember(
        role=WarCouncilRole.LOGISTICS_OFFICER,
        title="Logistics Officer",
        rotation_months=12,
        primary_perspective="Supply, transport, routes, fallback positions, ammo, food, water, fuel",
        why_seat_exists="If logistics cannot sustain the operation, it does not happen. Absolute cost veto",
        has_specific_veto=True,
        veto_scope="Cost & Sustainability Veto",
    ),
    WarCouncilMember(
        role=WarCouncilRole.DECEPTION_OFFICER,
        title="Deception Officer",
        rotation_months=12,
        primary_perspective="Feints, decoys, misinformation, false radio traffic, dummy positions, psyops",
        why_seat_exists="Sun Tzu: all warfare is based on deception; forces enemy to fight our conditions",
    ),
    WarCouncilMember(
        role=WarCouncilRole.TERRAIN_OFFICER,
        title="Terrain Officer",
        rotation_months=24,
        primary_perspective="Knows every river, forest, hill, pass, road, swamp, and ridge within 100 km",
        why_seat_exists="Uses the land as a weapon (Finnish lakes, Viet Cong jungle/tunnels, Boer veldt)",
    ),
    WarCouncilMember(
        role=WarCouncilRole.COMMUNITY_LIAISON,
        title="Community Liaison",
        rotation_months=3,
        primary_perspective="Civilian firewall representing Community Council; verifies public consent",
        why_seat_exists="Prevents War Council from becoming a military junta; absolute offensive veto",
        has_specific_veto=True,
        veto_scope="Offensive Action Veto",
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
    logistics_officer_affordability_approved: bool
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
    COUNCIL_SIZE: int = 7
    STANDARD_MAJORITY_THRESHOLD: int = 4     # 4 of 7
    BLOOD_RULE_SUPERMAJORITY: int = 6         # 6 of 7 if civilian casualties >= 10

    @classmethod
    def evaluate_proposal(
        cls,
        proposal: WarDecisionProposal,
        votes_in_favor: int,
        member_invoking_24h_delay: bool = False,
    ) -> CouncilVoteResult:
        # 1. Mandatory 24-hour reflection "No" rule
        if member_invoking_24h_delay:
            return CouncilVoteResult(
                approved=False,
                votes_in_favor=votes_in_favor,
                total_votes=cls.COUNCIL_SIZE,
                delayed_by_no_rule=True,
                rejection_reason="Delayed for 24 hours under the mandatory 'No' reflection rule",
            )

        # 2. Defensive-only constraint: Offensive actions strictly require Community Council assent
        if proposal.is_offensive_action and not proposal.community_council_authorized:
            return CouncilVoteResult(
                approved=False,
                votes_in_favor=votes_in_favor,
                total_votes=cls.COUNCIL_SIZE,
                delayed_by_no_rule=False,
                rejection_reason="Offensive military action lacks explicit Community Council authorization (Community Liaison Veto)",
            )

        # 3. Logistics Officer Absolute Cost Veto
        if not proposal.logistics_officer_affordability_approved:
            return CouncilVoteResult(
                approved=False,
                votes_in_favor=votes_in_favor,
                total_votes=cls.COUNCIL_SIZE,
                delayed_by_no_rule=False,
                rejection_reason="Logistics Officer veto: operation exceeds sustainable supply and resource burn limits",
            )

        # 4. The "Blood Rule": civilian casualties >= 10 requires 6/7 supermajority
        required_threshold = (
            cls.BLOOD_RULE_SUPERMAJORITY
            if proposal.predicted_civilian_casualties >= 10
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
# 3. The Core Doctrine: "Don't Mirror, Don't Chase, Don't Hold"
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class DoctrinePrinciple:
    rule_name: str
    meaning: str
    application: str
    historical_proof: str


DOCTRINE_PRINCIPLES: tuple[DoctrinePrinciple, ...] = (
    DoctrinePrinciple(
        rule_name="DON'T MIRROR",
        meaning="Never fight the enemy on their terms; refuse to match expensive weapons with expensive weapons.",
        application="If they have tanks, deny tank terrain. If aircraft, hide underground. If drones, throw nets.",
        historical_proof="Finns vs Soviet tanks (skis & Molotovs); Viet Cong vs US jets (tunnels & jungle); Boers vs British artillery.",
    ),
    DoctrinePrinciple(
        rule_name="DON'T CHASE",
        meaning="Avoid prolonged engagements; speed is armor; strike, achieve objective, withdraw immediately.",
        application="Never pursue retreating enemy into unknown terrain; do not try to 'finish them off' in open ground.",
        historical_proof="Khalid ibn al-Walid rapid cavalry disengagements; Boer dawn raids vanishing by noon; Afghan 20-minute ambushes.",
    ),
    DoctrinePrinciple(
        rule_name="DON'T HOLD",
        meaning="Never try to hold open ground against superior firepower.",
        application="Hold only terrain that hurts the enemy: forests, mountain passes, swamps, urban choke points, and tunnels.",
        historical_proof="Viet Cong held jungle/tunnels not Saigon; Finns held frozen forests not open plains; Mujahideen held mountain passes.",
    ),
    DoctrinePrinciple(
        rule_name="Strike the System, Not the Mass",
        meaning="Target command, communications, fuel, and supply routes rather than killing every enemy soldier.",
        application="An army without leadership, communication, fuel, and food collapses within 48 hours.",
        historical_proof="Decapitation strikes and fuel convoy interdictions in asymmetric guerrilla campaigns.",
    ),
    DoctrinePrinciple(
        rule_name="Deception First",
        meaning="The battle is often won before first contact through feints, decoys, and false electronic traffic.",
        application="Force adversary to expend munitions and energy attacking empty dummy positions.",
        historical_proof="Sun Tzu; Zhuge Liang campaigns; WWII Allied deception operations.",
    ),
    DoctrinePrinciple(
        rule_name="Mobility > Numbers",
        meaning="Speed, terrain knowledge, and timing beat numerical mass 9 times out of 10.",
        application="40 fast, terrain-literate fighters defeat 400 slow, confused, and heavy expeditionary troops.",
        historical_proof="Khalid ibn al-Walid 51 undefeated battles; Boer light horse commandos.",
    ),
)


# --------------------------------------------------------------------------
# 4. The Living Scenario Library (Roman Contingency Model)
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
        primary_response_phase="Local sector militia (20–30) + Mounted Unit scouts; 5 km max pursuit",
        active_specialized_units=("Mounted Unit", "Medical Team"),
        militia_mobilization_scale=30,
        reversibility="High (quick local disengagement)",
    ),
    ThreatScenario(
        code="S2",
        name="Medium coordinated assault",
        adversary_scale="100–500 fighters + light vehicles",
        early_warning_lead_time="2–6 hours",
        primary_response_phase="Defense in depth (3 layers); IED fields; drone net defense; Shock Unit counter-strike",
        active_specialized_units=("Shock Unit", "Counter-Drone Team", "Sapper Team", "Signals Team", "Strike Team", "Medical Team", "Mounted Unit"),
        militia_mobilization_scale=2000,
        reversibility="Moderate (staged defensive fallback)",
    ),
    ThreatScenario(
        code="S3",
        name="Large-scale invasion",
        adversary_scale="1,000+ fighters + armor + air support",
        early_warning_lead_time="12–48 hours",
        primary_response_phase="Full asymmetric transition: underground caches, decapitation raids, tank blinding, protracted guerrilla warfare",
        active_specialized_units=("Strike Team", "Shock Unit", "Counter-Drone Team", "Sapper Team", "Signals Team", "Medical Team", "Mounted Unit"),
        militia_mobilization_scale=3500,
        reversibility="Low (existential defense commitment)",
    ),
    ThreatScenario(
        code="S4",
        name="Flash flood / River breach",
        adversary_scale="Ecological flood wave",
        early_warning_lead_time="24–72 hours",
        primary_response_phase="EDMB Red alert; high-ground evacuation; reserve vault waterproofing; water purification",
        active_specialized_units=("Sapper Team", "Medical Team", "Mounted Unit"),
        militia_mobilization_scale=200,
        reversibility="High (civil recovery)",
    ),
    ThreatScenario(
        code="S5",
        name="Multi-season drought",
        adversary_scale="Prolonged hydrological deficit",
        early_warning_lead_time="3–6 months",
        primary_response_phase="Water rationing; drought-crop rotation; RAB food security runway; border water conflict monitoring",
        active_specialized_units=("Signals Team",),
        militia_mobilization_scale=50,
        reversibility="High (agricultural policy adjustment)",
    ),
    ThreatScenario(
        code="S6",
        name="Epidemic / Vector outbreak",
        adversary_scale="Pathogen / Vector spike",
        early_warning_lead_time="2–4 weeks",
        primary_response_phase="Sector quarantine; medical triage; vector spraying; transparent civic communications",
        active_specialized_units=("Medical Team", "Sapper Team"),
        militia_mobilization_scale=100,
        reversibility="High (staged de-escalation)",
    ),
    ThreatScenario(
        code="S7",
        name="Internal coup attempt",
        adversary_scale="Rogue faction / mutiny",
        early_warning_lead_time="0–12 hours",
        primary_response_phase="Secure warehouses and communications; isolate rogue leaders non-lethally; justice tribunal",
        active_specialized_units=("Signals Team", "Strike Team"),
        militia_mobilization_scale=500,
        reversibility="Moderate (due process adjudication)",
    ),
    ThreatScenario(
        code="S8",
        name="External trade route closure",
        adversary_scale="Hostile economic embargo",
        early_warning_lead_time="1–4 weeks",
        primary_response_phase="RAB economic buffer activation; production substitution ladder; diplomatic envoy dispatch",
        active_specialized_units=("Mounted Unit", "Signals Team"),
        militia_mobilization_scale=50,
        reversibility="High (diplomatic resolution)",
    ),
    ThreatScenario(
        code="S9",
        name="Cyber / Digital ledger attack",
        adversary_scale="Electronic state / cartel hackers",
        early_warning_lead_time="Minutes to hours",
        primary_response_phase="Isolate network nodes; revert to offline physical note ledger; trace intrusion origin",
        active_specialized_units=("Signals Team",),
        militia_mobilization_scale=20,
        reversibility="High (system isolation and cryptographic rebuild)",
    ),
    ThreatScenario(
        code="S10",
        name="CBRN attack",
        adversary_scale="Asymmetric / WMD strike",
        early_warning_lead_time="Minutes to hours",
        primary_response_phase="Underground shelter seal; positive air filtration; decontamination; survival cache distribution",
        active_specialized_units=("Medical Team", "Sapper Team", "Signals Team"),
        militia_mobilization_scale=1000,
        reversibility="Low (severe catastrophe management)",
    ),
)


# --------------------------------------------------------------------------
# 5. The War Room ("Genius Council")
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


# --------------------------------------------------------------------------
# 6. Specialized Units: Functional Naming & Skill Distribution
# --------------------------------------------------------------------------


class SpecializedUnitType(str, Enum):
    STRIKE_TEAM = "strike_team"              # Decapitation / target command neutralizer (4)
    SHOCK_UNIT = "shock_unit"                # Shock assault / rapid breakthrough (40)
    COUNTER_DRONE = "counter_drone_team"     # Counter-drone / air defense (20-30)
    SAPPER_TEAM = "sapper_team"              # Sappers / IEDs / engineering / traps (20-30)
    MEDICAL_TEAM = "medical_team"            # Combat trauma medical / triage (10-15)
    SIGNALS_TEAM = "signals_team"            # Comms / EW jamming / cyber (10-15)
    MOUNTED_UNIT = "mounted_unit"            # Mounted recon / rapid response / supply (30-50)


@dataclass(frozen=True)
class SpecializedUnitSpec:
    unit_type: SpecializedUnitType
    functional_name: str
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
        functional_name="Strike Team (Target Command Neutralizer)",
        min_size=4,
        max_size=8,
        nominal_size=4,
        mission="Infiltrate behind lines to eliminate high-value command/radio elements during active defense",
        operational_limit="72-hour maximum mission exfiltration limit; abort if encountering >5 hostiles",
        max_service_years=3,
        training_duration_months=6,
    ),
    SpecializedUnitSpec(
        unit_type=SpecializedUnitType.SHOCK_UNIT,
        functional_name="Shock Unit (Breakthrough Assault)",
        min_size=30,
        max_size=50,
        nominal_size=40,
        mission="Concentrated 10-20 minute shock charge to shatter enemy line for militia breakthrough",
        operational_limit="Deployed max once per 30 days; 2 km max pursuit; flanked by militia battalion",
        max_service_years=3,
        training_duration_months=3,
    ),
    SpecializedUnitSpec(
        unit_type=SpecializedUnitType.COUNTER_DRONE,
        functional_name="Counter-Drone Team (Air Defense)",
        min_size=20,
        max_size=30,
        nominal_size=25,
        mission="Layered drone neutralization (500m wires, 200m smoke, 100m nets, 50m shotguns)",
        operational_limit="Strict anti-air focus; falls back to militia line if ground infantry advances",
        max_service_years=3,
        training_duration_months=2,
    ),
    SpecializedUnitSpec(
        unit_type=SpecializedUnitType.SAPPER_TEAM,
        functional_name="Sapper Team (Traps & Fortifications)",
        min_size=20,
        max_size=30,
        nominal_size=25,
        mission="Construct hidden IED fields, ditch traps, caltrops, underground bunkers, and demolitions",
        operational_limit="Operates under night/smoke cover; zero standalone direct fire engagement",
        max_service_years=3,
        training_duration_months=3,
    ),
    SpecializedUnitSpec(
        unit_type=SpecializedUnitType.MEDICAL_TEAM,
        functional_name="Medical Team (Combat Trauma Medical)",
        min_size=10,
        max_size=15,
        nominal_size=12,
        mission="Field triage, emergency trauma surgery, blood storage, and casualty evacuation",
        operational_limit="Treats friend and wounded enemy alike; protected by dedicated security",
        max_service_years=3,
        training_duration_months=2,
    ),
    SpecializedUnitSpec(
        unit_type=SpecializedUnitType.SIGNALS_TEAM,
        functional_name="Signals Team (Electronic Warfare & Cyber)",
        min_size=10,
        max_size=15,
        nominal_size=12,
        mission="Mesh radio network maintenance, RF jamming of enemy comms, cyber defense of currency ledger",
        operational_limit="Continuous operation; first to deploy and last to de-escalate",
        max_service_years=3,
        training_duration_months=2,
    ),
    SpecializedUnitSpec(
        unit_type=SpecializedUnitType.MOUNTED_UNIT,
        functional_name="Mounted Unit (Recon & Rapid Logistics)",
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
# 7. Anti-Caste Safeguards (Anti-Praetorian / Anti-Janissary / Anti-Mamluk)
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class AntiCasteSafeguards:
    max_consecutive_service_years: int = 3          # Mandatory return to civilian economic production
    separate_barracks_allowed: bool = False         # Operators live in ordinary community homes
    separate_pay_or_privilege: bool = False         # Equal standard compensation in weight-based currency
    hereditary_recruitment_allowed: bool = False    # Merit and militia drill performance only
    holding_civilian_political_office: bool = False # Absolute separation of military & civil rule
    right_of_refusal_for_offensive_action: bool = True # Legal right to refuse illegal offensive war
    no_elite_branding_names: bool = True            # Functional naming only (no 'Guards', 'Immortals', 'Elites')
    skills_distributed_to_guilds: bool = True       # Veterans train apprentices upon return to civilian life


# --------------------------------------------------------------------------
# 8. Integrated Combat Timeline & Simulation
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
