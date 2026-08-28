"""Pluralism, Personal Status Law, and the Modernized Millet Architecture (§29).

This module formalizes:
1. ``ModernMilletArchitecture`` -- State governs public order, criminal law, economy, and defence;
   autonomous recognized communities (millets) govern family and personal status law.
2. ``CivilMillet`` -- Guaranteed state-administered default jurisdiction for the unaffiliated
   and individuals exercising the right of exit.
3. ``HumanRightsFloor`` -- Non-negotiable state overrides (minimum marriage age 18, verifiable
   state consent, criminal jurisdiction over domestic violence, custody appealable to ordinary courts).
4. ``AntiLebanonLock`` -- Strict prohibition of confessional quotas in political representation or state ministries.
5. ``StateGapAudit`` -- 10-domain rigorous classification of solved, partially addressed, and
   genuinely untouched governance pillars.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# --------------------------------------------------------------------------
# 1. Jurisdictional Separation Layers
# --------------------------------------------------------------------------


class AuthorityLayer(str, Enum):
    STATE_UNIFORM = "state_uniform"     # State holds exclusive uniform authority (no exception)
    MILLET_AUTONOMOUS = "millet_auto"   # Millet holds internal autonomous authority
    STATE_FLOOR_OVERRIDE = "state_floor"# State floor strictly overrides millet rules
    CIVIL_DEFAULT = "civil_default"     # Civil jurisdiction for unaffiliated/exit


@dataclass(frozen=True)
class JurisdictionalDomain:
    domain_name: str
    authority_layer: AuthorityLayer
    responsible_body: str
    governing_scope: str
    override_rule: str


MILLET_JURISDICTION_DOMAINS: tuple[JurisdictionalDomain, ...] = (
    JurisdictionalDomain(
        domain_name="Criminal Law & Public Order",
        authority_layer=AuthorityLayer.STATE_UNIFORM,
        responsible_body="Sovereign Courts & Public Police (§20, §28)",
        governing_scope="Offences, policing, prisons, public safety, traffic",
        override_rule="100% Uniform State jurisdiction; Zero religious exemption",
    ),
    JurisdictionalDomain(
        domain_name="Economy, Money & Taxation",
        authority_layer=AuthorityLayer.STATE_UNIFORM,
        responsible_body="Commodity Currency Board & Guild Assemblies (§01, §07, §27)",
        governing_scope="Currency issuance, zero-interest advances, commodity reserves, trade gates",
        override_rule="100% Uniform State jurisdiction; Zero commercial usury permitted",
    ),
    JurisdictionalDomain(
        domain_name="Public Dress Threshold (Part X / §28)",
        authority_layer=AuthorityLayer.STATE_UNIFORM,
        responsible_body="Female Guard Service & Municipal Venues (§28)",
        governing_scope="Bright-line anatomical exposure floor across spatial zones",
        override_rule="State sets civil floor; Millets free to require stricter internal standards for members",
    ),
    JurisdictionalDomain(
        domain_name="Family & Personal Status",
        authority_layer=AuthorityLayer.MILLET_AUTONOMOUS,
        responsible_body="Recognized Religious & Customary Millet Tribunals",
        governing_scope="Marriage rites, divorce, inheritance, child custody, internal charity",
        override_rule="Autonomous within community, subject to Non-Negotiable Human Rights Floor",
    ),
    JurisdictionalDomain(
        domain_name="Fundamental Human Rights Floor",
        authority_layer=AuthorityLayer.STATE_FLOOR_OVERRIDE,
        responsible_body="Constitutional Judiciary & Ordinary State Courts",
        governing_scope="Marriage age >= 18, verified consent, domestic violence criminalization, appellate review",
        override_rule="State floor overrides any contrary millet rule automatically",
    ),
    JurisdictionalDomain(
        domain_name="Civil Personal Status (The Civil Millet)",
        authority_layer=AuthorityLayer.CIVIL_DEFAULT,
        responsible_body="Civil Registry & State Family Magistrates",
        governing_scope="Civil marriage, no-fault divorce, equal inheritance, unaffiliated citizens",
        override_rule="Universal guaranteed right of exit; accessible to all citizens at any time",
    ),
    JurisdictionalDomain(
        domain_name="Political Representation & Governance",
        authority_layer=AuthorityLayer.STATE_UNIFORM,
        responsible_body="Civic Sortition Juries & Competence Council (§06, §20)",
        governing_scope="Parliament, cabinet ministries, military, public procurement",
        override_rule="Anti-Lebanon Lock: Zero confessional seats or ethnic ministry allocations permitted",
    ),
)


# --------------------------------------------------------------------------
# 2. Modern Millet Structural Safeguards
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class HumanRightsFloor:
    minimum_marriage_age: int = 18
    verifiable_state_consent_required: bool = True
    forced_marriage_criminalized: bool = True
    domestic_violence_state_criminal_jurisdiction_only: bool = True
    child_custody_decisions_appealable_to_state_courts: bool = True
    unrestricted_right_of_exit_to_civil_millet: bool = True

    @property
    def is_floor_complete(self) -> bool:
        return (
            self.minimum_marriage_age >= 18
            and self.verifiable_state_consent_required
            and self.forced_marriage_criminalized
            and self.domestic_violence_state_criminal_jurisdiction_only
            and self.child_custody_decisions_appealable_to_state_courts
            and self.unrestricted_right_of_exit_to_civil_millet
        )


@dataclass(frozen=True)
class AntiLebanonLock:
    confessional_parliamentary_quotas_prohibited: bool = True
    cabinet_ministry_ethnic_allocation_prohibited: bool = True
    civil_service_confessional_reservation_prohibited: bool = True
    millet_authority_strictly_confined_to_personal_status: bool = True

    @property
    def is_state_immune_to_confessional_gridlock(self) -> bool:
        return (
            self.confessional_parliamentary_quotas_prohibited
            and self.cabinet_ministry_ethnic_allocation_prohibited
            and self.civil_service_confessional_reservation_prohibited
            and self.millet_authority_strictly_confined_to_personal_status
        )


# --------------------------------------------------------------------------
# 3. Comprehensive State Gap Audit: The 10 Governance Domains
# --------------------------------------------------------------------------


class GapStatus(str, Enum):
    BUILT_AND_FORMALIZED = "built_and_formalized"       # Modeled, tested, documented with statutory mechanics
    PARTIALLY_ADDRESSED = "partially_addressed"         # Addressed in principle/subsystem, but lacks macro-level policy
    GENUINELY_UNTOUCHED = "genuinely_untouched"         # Completely absent from existing framework; open governance frontier


@dataclass(frozen=True)
class GovernanceGapRecord:
    domain_number: int
    domain_title: str
    status: GapStatus
    existing_coverage_summary: str
    unresolved_crucial_elements: str
    systemic_risk_severity: str


STATE_GAP_AUDIT_REGISTER: tuple[GovernanceGapRecord, ...] = (
    GovernanceGapRecord(
        domain_number=1,
        domain_title="Macro-Economy, Sovereign Float & Land",
        status=GapStatus.PARTIALLY_ADDRESSED,
        existing_coverage_summary="Abolished usurious debt/insurance (§27), commodity currency (§01-§05), 10 Fair Borrowing Rules, local production ladder (§17), gate fees (§07).",
        unresolved_crucial_elements="Reclaimed sovereign savings float investment governance; comprehensive land tenure & redistribution; general employment/wage legislation; universal fiscal revenue model.",
        systemic_risk_severity="CRITICAL (Largest capital reallocation lacks sovereign fund board design)",
    ),
    GovernanceGapRecord(
        domain_number=2,
        domain_title="Education & Cultural Transmission",
        status=GapStatus.PARTIALLY_ADDRESSED,
        existing_coverage_summary="Master-apprentice guild pipelines (§14, §17), media verification literacy (§25), Tier 4 capacity-gated duplication (§28), millet community schooling (§29).",
        unresolved_crucial_elements="National core curriculum standards; language of instruction policy; higher education research funding; private/elite school integration.",
        systemic_risk_severity="HIGH (Education is the primary transmission engine for voluntary normative durability)",
    ),
    GovernanceGapRecord(
        domain_number=3,
        domain_title="Family, Personal Status & Domestic Rights",
        status=GapStatus.BUILT_AND_FORMALIZED,
        existing_coverage_summary="Modernized Millet architecture (§29) delegating personal status to autonomous communities; Civil Millet for exit/unaffiliated; non-negotiable Human Rights Floor.",
        unresolved_crucial_elements="Inter-millet mixed marriage property reconciliation protocols; adoption jurisdictional handoffs.",
        systemic_risk_severity="RESOLVED IN DOCTRINE (§29)",
    ),
    GovernanceGapRecord(
        domain_number=4,
        domain_title="General Criminal Justice & Penal Philosophy",
        status=GapStatus.PARTIALLY_ADDRESSED,
        existing_coverage_summary="Restorative civic labor (§26), community exile protocol (75% vote §26), abolition of debtor/morality imprisonment (§26, §28), departmental policing (§20).",
        unresolved_crucial_elements="General penal code for violent felonies; prison conditions & rehabilitation standards; bail/trial procedure rules; explicit position on capital/corporal punishment.",
        systemic_risk_severity="HIGH (Rejected carceral penalties for media/dress, but general felony penal code unwritten)",
    ),
    GovernanceGapRecord(
        domain_number=5,
        domain_title="Constitutional Entrenchment & Supremacy",
        status=GapStatus.GENUINELY_UNTOUCHED,
        existing_coverage_summary="Sortition juries (§06, §20), 5-year statutory sunsets (§25, §28), War Council checks (§24), Competence Council (§20).",
        unresolved_crucial_elements="Formal written constitution with rigid amendment thresholds (e.g. 75% referendum supermajority); constitutional court review; bill of rights hierarchy; emergency powers.",
        systemic_risk_severity="CRITICAL (Without constitutional entrenchment, any future simple majority can repeal all safeguards)",
    ),
    GovernanceGapRecord(
        domain_number=6,
        domain_title="Religion, Pluralism & Confessional Order",
        status=GapStatus.BUILT_AND_FORMALIZED,
        existing_coverage_summary="Modernized Millet System (§29): State public order floor + autonomous community personal status + Civil Millet + Anti-Lebanon political quota ban.",
        unresolved_crucial_elements="Registration dispute appeals for fringe/emerging spiritual groups.",
        systemic_risk_severity="RESOLVED IN DOCTRINE (§29)",
    ),
    GovernanceGapRecord(
        domain_number=7,
        domain_title="Physical Healthcare Infrastructure & Pharmaceuticals",
        status=GapStatus.PARTIALLY_ADDRESSED,
        existing_coverage_summary="Direct guild healthcare provisioning (§27), medical mutual reserve pools (§27), Tier 1 female medical wards (§28), Tier 2 hospital wings (§28).",
        unresolved_crucial_elements="Physical clinic capacity expansion plan; medical doctor training/retention/emigration controls; national pharmaceutical API synthesis; reproductive health policy.",
        systemic_risk_severity="HIGH (Abolished medical schemes, but hospital staffing and API synthesis remain constrained)",
    ),
    GovernanceGapRecord(
        domain_number=8,
        domain_title="Digital & Physical Infrastructure (Energy, Telecom, ID)",
        status=GapStatus.PARTIALLY_ADDRESSED,
        existing_coverage_summary="Local energy/biofuel production (§17), LoRa mesh disaster comms (§23), anti-backdoor cryptographic privacy (§25), subterranean military hardening (§19).",
        unresolved_crucial_elements="National grid/water management; biometric/digital ID civil liberties framework; lawful interception legal bounds; national cybersecurity defense command.",
        systemic_risk_severity="MEDIUM-HIGH (Digital identity implied by enforcement, but uncodified in civil liberties law)",
    ),
    GovernanceGapRecord(
        domain_number=9,
        domain_title="External Relations, Treaties & Capital Controls",
        status=GapStatus.PARTIALLY_ADDRESSED,
        existing_coverage_summary="Trade window buffer stocks (§16), import substitution ladder (§17), foreign platform ad levies (§25), asymmetric defense doctrine (§19).",
        unresolved_crucial_elements="Formal capital controls for repatriated float; legal defense against Bilateral Investment Treaty (BIT) claims; immigration and naturalization law; diplomatic posture.",
        systemic_risk_severity="HIGH (Float repatriation will trigger international investor-state arbitration claims)",
    ),
    GovernanceGapRecord(
        domain_number=10,
        domain_title="Macro-Capacity Allocation & Sequencing Synthesis",
        status=GapStatus.GENUINELY_UNTOUCHED,
        existing_coverage_summary="Individual 3-year timelines (§10, §25, §28), falsifiable pilot gates (Phase 1-3 §10).",
        unresolved_crucial_elements="Unified cross-domain fiscal and administrative capacity budget: simultaneous implementation of Female Guard Service, Media Regulator, Commodity Silos, and Health Guilds competing for the same scarce administrative cadre.",
        systemic_risk_severity="CRITICAL (Simultaneous domain rollouts will exhaust scarce administrative talent without a master queue)",
    ),
)
