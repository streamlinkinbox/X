"""National Media and Information Integrity Act: Sovereign Enforcement Framework.

This module formalizes the statutory architecture of the National Media and Information
Integrity Act (Rev. 2):
1. ``DesignDoctrine`` -- Sovereign authority, enforcement precedes proclamation, elimination
   of administrative discretion, and the source-not-filter rule.
2. ``EnforcementBodies`` -- The three independent statutory organs:
   - Media Standards Authority (MSA)
   - Information Integrity Inspectorate (III)
   - Media Tribunal
3. ``FundingFormula`` -- Ring-fenced percentage of broadcast fees and digital ad revenue levy.
4. ``SanctionLadder`` -- 7-step mandatory, escalating, percentage-of-turnover penalties.
5. ``ForeignPlatformLevers`` -- Enforcement at the money layer: local representative liability,
   loss of domestic advertiser tax-deductibility, payment processor blocks, and zero network-layer blocking.
6. ``PlatformAmplification`` -- "Hosting stays immune; amplification does not." 8 statutory platform duties.
7. ``SyntheticProvenance`` -- Content credentials, synthetic labelling, and shifted burden of proof.
8. ``StateConductDiscipline`` -- Formula-only state advertising, deemed-grant FOI, whistleblower protection,
   anti-SLAPP shields, and anti-astroturfing criminalization.
9. ``PhasedSequence`` -- 5-phase implementation sequencing (disciplining the state in Phase 1).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# --------------------------------------------------------------------------
# 1. Statutory Enforcement Bodies & Funding
# --------------------------------------------------------------------------


class RegulatoryBodyType(str, Enum):
    MSA = "media_standards_authority"             # Adjudicates content conduct; issues corrections & fines
    III = "information_integrity_inspectorate"     # Technical audits, ranking verification, forensics
    TRIBUNAL = "media_tribunal"                   # Specialist fast-track judicial appeals


@dataclass(frozen=True)
class StatutoryBodySpec:
    body_type: RegulatoryBodyType
    name: str
    board_term_years: int
    appointment_mechanism: str
    removal_mechanism: str
    primary_statutory_duties: tuple[str, ...]
    is_ministerial_direction_prohibited: bool = True


STATUTORY_BODIES: tuple[StatutoryBodySpec, ...] = (
    StatutoryBodySpec(
        body_type=RegulatoryBodyType.MSA,
        name="Media Standards Authority (MSA)",
        board_term_years=6,
        appointment_mechanism="Parliamentary supermajority from judicial, journalist, and public nominations",
        removal_mechanism="Judicial process for defined statutory cause only",
        primary_statutory_duties=(
            "Adjudicate content-conduct breaches (courtroom, instructional, commercial)",
            "Enforce equal-prominence corrections and right-of-reply orders",
            "Impose percentage-of-turnover fines and broadcast license conditions",
        ),
    ),
    StatutoryBodySpec(
        body_type=RegulatoryBodyType.III,
        name="Information Integrity Inspectorate (III)",
        board_term_years=6,
        appointment_mechanism="Parliamentary supermajority; annual reporting to Parliament directly",
        removal_mechanism="Judicial process for defined statutory cause only",
        primary_statutory_duties=(
            "Independent technical and algorithmic audit of platform ranking systems",
            "Forensic accounting and beneficial ownership verification",
            "Evidence gathering and referral of commercial fraud to prosecution",
        ),
    ),
    StatutoryBodySpec(
        body_type=RegulatoryBodyType.TRIBUNAL,
        name="Media Tribunal",
        board_term_years=6,
        appointment_mechanism="Specialist judges within ordinary judiciary",
        removal_mechanism="Standard judicial tenure protections",
        primary_statutory_duties=(
            "Fast-track appeals from MSA and III rulings (max 90-day determination)",
            "Review of emergency public-interest overrides",
            "Onward appeal to higher appellate courts as of right",
        ),
    ),
)


@dataclass(frozen=True)
class StatutoryFundingFormula:
    broadcast_fee_levy_percent: float = 0.15     # 15% of annual broadcast license revenues
    digital_ad_revenue_levy_percent: float = 0.02 # 2% statutory levy on domestic digital ad turnover
    is_ring_fenced_trust_fund: bool = True
    annual_ministerial_budget_discretion: bool = False # Strictly prohibited

    @property
    def is_genuinely_independent(self) -> bool:
        return self.is_ring_fenced_trust_fund and not self.annual_ministerial_budget_discretion


# --------------------------------------------------------------------------
# 2. The Seven-Step Mandatory Escalating Sanction Ladder
# --------------------------------------------------------------------------


class SanctionStep(int, Enum):
    STEP_1_ADVISORY = 1       # Private advisory note
    STEP_2_PUBLISHED_FINDING = 2 # Publicly published finding of breach
    STEP_3_CORRECTION = 3     # Mandatory correction with equal prominence (same slot/duration)
    STEP_4_TURNOVER_FINE = 4  # Statutory fine as a percentage of domestic turnover
    STEP_5_LICENSE_CONDITION = 5 # Binding operational condition on broadcast/platform license
    STEP_6_COMMERCIAL_SUSPENSION = 6 # Temporary suspension of monetization/commercial operations
    STEP_7_LICENSE_REVOCATION = 7 # Full revocation of operating authorization


@dataclass(frozen=True)
class SanctionLadderSpec:
    step: SanctionStep
    name: str
    description: str
    is_automatic_on_repeat_breach: bool
    director_personal_liability: bool = False


SANCTION_LADDER: tuple[SanctionLadderSpec, ...] = (
    SanctionLadderSpec(
        step=SanctionStep.STEP_1_ADVISORY,
        name="Advisory Note",
        description="Confidential guidance notice for minor first-time procedural ambiguities",
        is_automatic_on_repeat_breach=False,
    ),
    SanctionLadderSpec(
        step=SanctionStep.STEP_2_PUBLISHED_FINDING,
        name="Published Finding",
        description="Public notice of breach entered into the permanent regulatory registry",
        is_automatic_on_repeat_breach=True,
    ),
    SanctionLadderSpec(
        step=SanctionStep.STEP_3_CORRECTION,
        name="Equal-Prominence Correction",
        description="Mandatory correction published on the same page, slot, and duration within 48 hours",
        is_automatic_on_repeat_breach=True,
    ),
    SanctionLadderSpec(
        step=SanctionStep.STEP_4_TURNOVER_FINE,
        name="Percentage-of-Turnover Fine",
        description="Fine calculated as 1% to 10% of gross domestic turnover (debt to state)",
        is_automatic_on_repeat_breach=True,
        director_personal_liability=True,
    ),
    SanctionLadderSpec(
        step=SanctionStep.STEP_5_LICENSE_CONDITION,
        name="Statutory License Condition",
        description="Binding operational restriction or mandatory external audit compliance monitor",
        is_automatic_on_repeat_breach=True,
        director_personal_liability=True,
    ),
    SanctionLadderSpec(
        step=SanctionStep.STEP_6_COMMERCIAL_SUSPENSION,
        name="Commercial Suspension",
        description="Temporary prohibition on accepting domestic ad spend or processing subscription revenue",
        is_automatic_on_repeat_breach=True,
        director_personal_liability=True,
    ),
    SanctionLadderSpec(
        step=SanctionStep.STEP_7_LICENSE_REVOCATION,
        name="License Revocation",
        description="Permanent termination of broadcast spectrum or domestic commercial registration",
        is_automatic_on_repeat_breach=True,
        director_personal_liability=True,
    ),
)


# --------------------------------------------------------------------------
# 3. Foreign Platform Enforcement: The Money-Layer Strategy
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class ForeignPlatformEnforcementModel:
    mandatory_resident_legal_representative: bool = True
    representative_personal_liability_for_contempt: bool = True
    ad_spend_tax_deductibility_disallowance: bool = True  # Domestic advertisers lose expense deduction
    payment_processor_settlement_prohibition: bool = True # Banks blocked from settling domestic ad billing
    withholding_tax_on_revenue_remittances: bool = True
    network_layer_packet_filtering_prohibited: bool = True # Zero ISP blocking/filtering

    @property
    def is_enforceable_without_foreign_treaty(self) -> bool:
        # All levers operate domestically on tax, corporate, and payment networks
        return (
            self.mandatory_resident_legal_representative
            and self.ad_spend_tax_deductibility_disallowance
            and self.payment_processor_settlement_prohibition
            and self.network_layer_packet_filtering_prohibited
        )


# --------------------------------------------------------------------------
# 4. Platform Amplification: "Hosting Immune; Amplification Accountable"
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class PlatformStatutoryDuties:
    annual_independent_ranking_audit: bool = True        # Audited by III-accredited data engineers
    published_systemic_risk_assessment: bool = True     # Focus on systemic risk, not individual posts
    non_personalized_feed_default_option: bool = True   # One-tap chronological/non-algorithmic feed
    no_engagement_optimization_under_16: bool = True    # Banning dopamine feedback loops for minors
    public_political_ad_register_5yr: bool = True       # Searchable funder, spend, and targeting criteria
    independent_researcher_data_access: bool = True     # Public reach data accessible to scholars
    virality_friction_controls: bool = True             # Forwarding limits & group caps (metadata-layer)
    provenance_credential_display: bool = True          # Displaying C2PA / origin authentication
    no_encryption_backdoors_or_escrow: bool = True      # Protecting citizens' end-to-end security


# --------------------------------------------------------------------------
# 5. State Conduct Discipline: Disciplining the State First
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class StateConductPolicy:
    state_ad_spend_published_formula_only: bool = True   # Zero discretion in placing state ads
    state_ad_deviation_is_criminal_offence: bool = True
    foi_deemed_grant_on_deadline_lapse: bool = True      # Silence = approved request
    foi_fees_capped_at_reproduction_cost: bool = True
    whistleblower_reversed_burden_of_proof: bool = True  # State must prove retaliation did not occur
    mandatory_anti_slapp_early_dismissal: bool = True    # Shields small publishers from lawfare
    astroturfing_by_public_bodies_criminalized: bool = True
    functional_press_definition_no_licensing: bool = True # Anyone practicing journalism is protected


# --------------------------------------------------------------------------
# 6. Consolidated Content Policy Rules
# --------------------------------------------------------------------------


class ContentTier(str, Enum):
    TIER_A_INSTRUCTIONAL = "tier_a_instructional"
    TIER_B_DEPICTIVE = "tier_b_depictive"
    TIER_C_ASPIRATIONAL = "tier_c_aspirational"
    COURT_PROCEDURE = "court_procedure"
    GOVERNMENT_REPORTING = "government_reporting"
    DISTRIBUTION_INFRASTRUCTURE = "distribution_pipe"


class RestrictionStatus(str, Enum):
    RESTRICT = "restrict"
    ACCOUNTABLE = "accountable"
    DO_NOT_RESTRICT = "do_not_restrict"
    NEVER_RESTRICT = "never_restrict"


@dataclass(frozen=True)
class ConsolidatedRule:
    category: str
    status: RestrictionStatus
    enforcement_mechanism: str
    rationale: str


CONSOLIDATED_POLICY_MATRIX: tuple[ConsolidatedRule, ...] = (
    ConsolidatedRule(
        category="Operational method detail (suicide, weapons, fraud, hacking)",
        status=RestrictionStatus.RESTRICT,
        enforcement_mechanism="MSA enforcement + criminal prosecution for weapon schematics",
        rationale="Restricts the instructional 'how-to'; carve-outs for academic/security research",
    ),
    ConsolidatedRule(
        category="Perpetrator glorification, manifestos, mass-casualty fame",
        status=RestrictionStatus.RESTRICT,
        enforcement_mechanism="MSA sanction ladder entering at Step 3 (Equal-Prominence Correction)",
        rationale="Denies notoriety incentives; eliminates social learning reward model",
    ),
    ConsolidatedRule(
        category="Courtroom live broadcast and crime-scene gore imagery",
        status=RestrictionStatus.RESTRICT,
        enforcement_mechanism="Court procedure contempt rules + broadcast license conditions",
        rationale="Protects judicial truth-seeking from becoming reality TV; preserves dignity",
    ),
    ConsolidatedRule(
        category="Naming suspects before formal charge; naming victims or minors",
        status=RestrictionStatus.RESTRICT,
        enforcement_mechanism="MSA sanction ladder + statutory civil damages to named individual",
        rationale="Preserves presumption of innocence ('Andreas B.' standard) and victim protection",
    ),
    ConsolidatedRule(
        category="Prejudicial commentary on live proceedings",
        status=RestrictionStatus.RESTRICT,
        enforcement_mechanism="Contempt of court applied by presiding judiciary",
        rationale="Prevents trial by media and jury/witness contamination",
    ),
    ConsolidatedRule(
        category="Undisclosed paid or financial promotion (crypto, forex, gambling)",
        status=RestrictionStatus.RESTRICT,
        enforcement_mechanism="Turnover fines + asset forfeiture + platform joint liability",
        rationale="Eliminates predatory consumer deception and manufactured debt traps",
    ),
    ConsolidatedRule(
        category="Unlabelled synthetic media in politics, elections, and commercial ads",
        status=RestrictionStatus.RESTRICT,
        enforcement_mechanism="Criminal offense for impersonation/electoral fraud + platform takedown",
        rationale="Shifts default from 'prove it is fake' to 'prove origin credentials'",
    ),
    ConsolidatedRule(
        category="Incitement to violence (two-limb test: intent + likelihood)",
        status=RestrictionStatus.RESTRICT,
        enforcement_mechanism="Ordinary criminal courts applying strict statutory dual-limb test",
        rationale="Both intent and real likelihood required; offensiveness alone is never sufficient",
    ),
    ConsolidatedRule(
        category="Algorithmic amplification systems of large platforms",
        status=RestrictionStatus.ACCOUNTABLE,
        enforcement_mechanism="III annual ranking audits + systemic risk mitigation + turnover fines",
        rationale="Hosting is passive and immune; amplification is editorial and accountable",
    ),
    ConsolidatedRule(
        category="Fiction depicting wrongdoing with narrative consequence",
        status=RestrictionStatus.DO_NOT_RESTRICT,
        enforcement_mechanism="Voluntary age classification only; mandatory label for reenactments",
        rationale="Preserves moral literature and cautionary structure; fiction transmits imitation weakly",
    ),
    ConsolidatedRule(
        category="Honest depiction of wealth and diverse lifestyle",
        status=RestrictionStatus.DO_NOT_RESTRICT,
        enforcement_mechanism="Curricular media and financial literacy in schools",
        rationale="Critical education is durable; hiding honest economic reality is futile",
    ),
    ConsolidatedRule(
        category="Investigative reporting on government officials, stewards, and budgets",
        status=RestrictionStatus.NEVER_RESTRICT,
        enforcement_mechanism="Constitutional press shield + Anti-SLAPP + whistleblower protection",
        rationale="Primary instrument of anti-corruption; discomfort to state is the mechanism",
    ),
    ConsolidatedRule(
        category="Ownership and control of information distribution channels",
        status=RestrictionStatus.NEVER_RESTRICT,
        enforcement_mechanism="Anti-concentration laws + prohibition on state network filtering",
        rationale="Monopoly state filter creates fatal single point of capture (§0.4)",
    ),
)


# --------------------------------------------------------------------------
# 7. Phased Implementation Sequence
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class ImplementationPhase:
    phase_number: int
    timeline_months: str
    phase_name: str
    core_actions: tuple[str, ...]
    strategic_rationale: str


IMPLEMENTATION_PHASES: tuple[ImplementationPhase, ...] = (
    ImplementationPhase(
        phase_number=1,
        timeline_months="0–12 mo",
        phase_name="Institutional Foundations & State Self-Discipline",
        core_actions=(
            "Establish MSA, III, and Media Tribunal with formula funding",
            "Enact formula-only state advertising law (criminal penalty for deviation)",
            "Enact Deemed-Grant FOI reform and Anti-SLAPP protection statutes",
            "Implement whistleblower protections with reversed burden of proof",
        ),
        strategic_rationale="Disciplines the state before the press; builds credible non-partisan regulators",
    ),
    ImplementationPhase(
        phase_number=2,
        timeline_months="12–24 mo",
        phase_name="Content Conduct & Commercial Deception Enforcement",
        core_actions=(
            "Implement courtroom reporting rules (no cameras, suspect/victim anonymity)",
            "Enact instructional method prohibitions (suicide, weapons, fraud)",
            "Enact perpetrator 'No Notoriety' protocol",
            "Mandate commercial disclosure for paid promotions, retouched images, and finance",
            "Commission domestic baseline media consumption and trust research",
        ),
        strategic_rationale="Closes legitimate harm vectors without touching distribution ownership",
    ),
    ImplementationPhase(
        phase_number=3,
        timeline_months="24–36 mo",
        phase_name="Platform Amplification & Money-Layer Foreign Levers",
        core_actions=(
            "Mandate local resident legal representatives for foreign platforms",
            "Enact tax-deductibility disallowance for ads on non-compliant platforms",
            "Initiate III annual independent audits of platform ranking algorithms",
            "Enforce non-personalized feed defaults and under-16 engagement protection",
        ),
        strategic_rationale="Establishes domestic leverage over foreign platforms at the money layer",
    ),
    ImplementationPhase(
        phase_number=4,
        timeline_months="36–48 mo",
        phase_name="Provenance, Synthetic Media & Consequence Layer",
        core_actions=(
            "Deploy content credentials standards on editing tools and platforms",
            "Enact criminal penalties for deceptive synthetic political impersonation",
            "Operationalize asset declarations with automatic lifestyle-audit triggers",
            "Enforce open contracting and beneficial ownership registers",
        ),
        strategic_rationale="Shifts default from synthetic detection to origin provenance",
    ),
    ImplementationPhase(
        phase_number=5,
        timeline_months="Continuous",
        phase_name="Accountability Audits & 5-Year Sunset Review",
        core_actions=(
            "Publish annual enforcement reports detailing all sanctions and appeals",
            "Mandatory parliamentary review and re-enactment vote at Year 5",
        ),
        strategic_rationale="Prevents permanent ossification and forces regular democratic re-examination",
    ),
)
