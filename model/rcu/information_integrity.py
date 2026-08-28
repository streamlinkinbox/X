"""National Media and Information Integrity Act: Sovereign Enforcement Framework (Rev. 3).

This module formalizes the statutory architecture of the National Media and Information
Integrity Act (Rev. 3):
1. ``DesignDoctrine`` -- Sovereign authority, enforcement precedes proclamation, elimination
   of administrative discretion, and the source-not-filter rule.
2. ``SanctionsThatActuallyBite`` -- Replaces fines with sanctions that attack what media actors
   actually want: reach, revenue continuity, and personal standing.
3. ``NineStepSanctionLadder`` -- The 9-step mandatory, escalating, reach-and-revenue ladder:
   - Step 1: Published finding
   - Step 2: Equal-prominence and equal-reach correction
   - Step 3: Disgorgement of revenue + statutory victim compensation
   - Step 4: Algorithmic amplification suspension / prominence demotion
   - Step 5: Monetization suspension (72h, 7d, 30d)
   - Step 6: Independent compliance monitor at offender's cost
   - Step 7: Personal disqualification of accountable individual (no indemnification)
   - Step 8: Algorithmic feature suspension / operational suspension (product recall)
   - Step 9: License revocation with principal bar
4. ``DisgorgementVsFines`` -- Arithmetic revenue disgorgement + 100% direct victim compensation;
   zero money into state slush funds.
5. ``ForeignPlatformLevers`` -- Money layer enforcement: representative liability, tax deductibility
   disallowance, payment processor settlement block, and zero network-layer filtering.
6. ``StateConductDiscipline`` -- Formula-only state ads, deemed-grant FOI, anti-SLAPP, whistleblower shield.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# --------------------------------------------------------------------------
# 1. Statutory Enforcement Bodies & Formula Funding
# --------------------------------------------------------------------------


class RegulatoryBodyType(str, Enum):
    MSA = "media_standards_authority"             # Adjudicates content conduct; issues reach/revenue sanctions
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
            "Adjudicate content-conduct breaches (courtroom, instructional, commercial deception)",
            "Enforce equal-prominence and equal-reach corrections",
            "Order revenue disgorgement, victim compensation, and monetization suspensions",
        ),
    ),
    StatutoryBodySpec(
        body_type=RegulatoryBodyType.III,
        name="Information Integrity Inspectorate (III)",
        board_term_years=6,
        appointment_mechanism="Parliamentary supermajority; reports annually to Parliament directly",
        removal_mechanism="Judicial process for defined statutory cause only",
        primary_statutory_duties=(
            "Independent technical and algorithmic audit of platform ranking systems",
            "Forensic accounting and beneficial ownership verification",
            "Supervise compliance monitors and algorithmic feature suspensions",
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
            "Enforce compensation on wrongly imposed sanctions upon reversal",
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
# 2. Rev. 3: The 9-Step Sanction Ladder (Attacking Reach, Revenue & Position)
# --------------------------------------------------------------------------


class SanctionStep(int, Enum):
    STEP_1_PUBLISHED_FINDING = 1              # Published finding in permanent public registry
    STEP_2_EQUAL_REACH_CORRECTION = 2         # Forced correction at equal prominence & equal reach
    STEP_3_DISGORGEMENT_COMPENSATION = 3      # Revenue disgorgement + 100% victim compensation
    STEP_4_AMPLIFICATION_SUSPENSION = 4       # Barred from algorithmic promotion / prominence demotion
    STEP_5_MONETIZATION_SUSPENSION = 5        # Temporary advertising & subscription monetization freeze
    STEP_6_COMPLIANCE_MONITOR = 7             # External monitor installed at offender's expense
    STEP_7_PERSONAL_DISQUALIFICATION = 7      # 1–5 yr industry ban for accountable named individual
    STEP_8_ALGORITHMIC_FEATURE_SUSPENSION = 8 # Domestic feature suspension (platform product recall)
    STEP_9_LICENSE_REVOCATION_PRINCIPAL_BAR = 9 # Full revocation + principal reincorporation bar


@dataclass(frozen=True)
class SanctionLadderSpec:
    step: int
    name: str
    target_asset: str                         # "Audience / Reach", "Cash Flow / Revenue", "Personal Position", "Operations"
    operational_action: str
    trigger_condition: str
    is_automatic_on_repeat_breach: bool
    director_personal_liability: bool = False


REVISED_SANCTION_LADDER_REV3: tuple[SanctionLadderSpec, ...] = (
    SanctionLadderSpec(
        step=1,
        name="Published Finding",
        target_asset="Reputation / Record",
        operational_action="Formal determination published on MSA registry and on outlet homepage for 7 days",
        trigger_condition="First breach (minor or procedural)",
        is_automatic_on_repeat_breach=True,
    ),
    SanctionLadderSpec(
        step=2,
        name="Equal-Prominence & Equal-Reach Correction",
        target_asset="Audience / Reach",
        operational_action="Mandatory correction in identical slot, duration, and verified audience size within 72h",
        trigger_condition="First substantive factual or conduct breach",
        is_automatic_on_repeat_breach=True,
    ),
    SanctionLadderSpec(
        step=3,
        name="Revenue Disgorgement + Victim Compensation",
        target_asset="Profit Motive & Victim Justice",
        operational_action="100% of revenue earned from breach disgorged + statutory compensation paid to named victim",
        trigger_condition="Any breach that earned commercial revenue or named an individual",
        is_automatic_on_repeat_breach=True,
    ),
    SanctionLadderSpec(
        step=4,
        name="Amplification Suspension & Prominence Demotion",
        target_asset="Audience / Reach",
        operational_action="Barred from algorithmic recommendations and EPG preferential placement for 14–30 days",
        trigger_condition="Repeat breach within 12 months",
        is_automatic_on_repeat_breach=True,
    ),
    SanctionLadderSpec(
        step=5,
        name="Monetization Suspension",
        target_asset="Cash Flow / Revenue Continuity",
        operational_action="Total ban on domestic ad monetization and subscription processing for 72h, 7d, or 30d",
        trigger_condition="Second repeat breach within 12 months",
        is_automatic_on_repeat_breach=True,
        director_personal_liability=True,
    ),
    SanctionLadderSpec(
        step=6,
        name="Compliance Monitor at Offender's Expense",
        target_asset="Operational Autonomy",
        operational_action="III-appointed independent monitor embedded in editorial/ranking process for 6–12 months",
        trigger_condition="Third breach within 24 months",
        is_automatic_on_repeat_breach=True,
        director_personal_liability=True,
    ),
    SanctionLadderSpec(
        step=7,
        name="Personal Disqualification (No Indemnification)",
        target_asset="Personal Position & Career",
        operational_action="Accountable editor/officer barred from media executive roles for 1–5 years; zero corporate indemnification",
        trigger_condition="Deliberate falsification, obstruction, or fourth breach",
        is_automatic_on_repeat_breach=True,
        director_personal_liability=True,
    ),
    SanctionLadderSpec(
        step=8,
        name="Algorithmic Feature Suspension",
        target_asset="Product Architecture",
        operational_action="Domestic suspension of specific recommender algorithm feature (product recall)",
        trigger_condition="Systemic algorithmic harm or audit refusal",
        is_automatic_on_repeat_breach=True,
        director_personal_liability=True,
    ),
    SanctionLadderSpec(
        step=9,
        name="License Revocation + Principal Bar",
        target_asset="Corporate Existence",
        operational_action="Permanent termination of broadcast spectrum / operating registration; principals barred from reincorporating",
        trigger_condition="Persistent or egregious bad-faith defiance",
        is_automatic_on_repeat_breach=True,
        director_personal_liability=True,
    ),
)


# --------------------------------------------------------------------------
# 3. Disgorgement vs. Fines Model
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class DisgorgementAssessment:
    commercial_revenue_earned_usd: float
    statutory_multiplier: float = 1.5
    victim_harm_compensation_usd: float = 10000.0
    investigation_cost_recovery_usd: float = 5000.0

    @property
    def total_disgorgement_amount_usd(self) -> float:
        # Removes the profit motive completely: revenue earned * multiplier
        return self.commercial_revenue_earned_usd * self.statutory_multiplier

    @property
    def victim_allocation_usd(self) -> float:
        # Paid 100% directly to the person harmed, 0% to state treasury slush funds
        return self.victim_harm_compensation_usd

    @property
    def total_financial_liability_usd(self) -> float:
        return (
            self.total_disgorgement_amount_usd
            + self.victim_allocation_usd
            + self.investigation_cost_recovery_usd
        )


# --------------------------------------------------------------------------
# 4. Foreign Platform Enforcement: The Money-Layer Strategy
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class ForeignPlatformEnforcementModel:
    mandatory_resident_legal_representative: bool = True
    representative_personal_liability_for_contempt: bool = True
    ad_spend_tax_deductibility_disallowance: bool = True  # Domestic advertisers lose tax deduction
    payment_processor_settlement_prohibition: bool = True # Banks blocked from settling ad billing
    withholding_tax_on_revenue_remittances: bool = True
    network_layer_packet_filtering_prohibited: bool = True # Zero ISP blocking/filtering

    @property
    def is_enforceable_without_foreign_treaty(self) -> bool:
        return (
            self.mandatory_resident_legal_representative
            and self.ad_spend_tax_deductibility_disallowance
            and self.payment_processor_settlement_prohibition
            and self.network_layer_packet_filtering_prohibited
        )


# --------------------------------------------------------------------------
# 5. Platform Amplification: "Hosting Immune; Amplification Accountable"
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
# 6. State Conduct Discipline: Disciplining the State First
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
# 7. Consolidated Content Policy Rules
# --------------------------------------------------------------------------


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
        enforcement_mechanism="MSA sanction ladder entering at Step 2 (Equal-Reach Correction)",
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
        enforcement_mechanism="Disgorgement (1.5x) + monetization freeze + joint platform liability",
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
        enforcement_mechanism="III ranking audits + systemic risk mitigation + feature suspensions",
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
# 8. Phased Implementation Sequence
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
