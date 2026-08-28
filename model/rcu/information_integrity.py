"""Media, Information Integrity, and Social Harm: Regulatory and Architectural Model.

This module formalizes the policy framework reconciling anti-corruption investigative
freedom with social harm prevention:
1. ``ContentPolicy`` -- Classifies content across Tier A (Instructional), Tier B (Depictive/Fiction),
   Tier C (Aspirational/Commercial), Court Procedure, and Official Governance reporting.
2. ``GoverningAxiom`` -- "Restrict the instructional and the deceptive. Do not restrict the depictive."
3. ``DistributionArchitecture`` -- Distributed enforcement across 8 pillars; strict prohibition on
   state pipe ownership / single filter gates (central systems may act only as *sources*, never *filters*).
4. ``CourtReportingStandards`` -- Banning courtroom cameras, protecting suspect/victim dignity,
   enforcing sub judice rules, and publishing open factual written registries.
5. ``CommercialDeceptionSafeguards`` -- Mandatory paid-promotion disclosures, image retouching labels,
   influencer financial promotion bans (crypto, forex, gambling), and debt-advertising restrictions for minors.
6. ``AntiConcentrationPolicy`` -- Limits single-entity media market share and mandates ownership transparency.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# --------------------------------------------------------------------------
# 1. Content Categorization and Tiers
# --------------------------------------------------------------------------


class ContentTier(str, Enum):
    TIER_A_INSTRUCTIONAL = "tier_a_instructional"     # Method detail: suicide, weapons, hacking, manifestos
    TIER_B_DEPICTIVE = "tier_b_depictive"             # Fiction, drama, art, literature, moral cautionary tales
    TIER_C_ASPIRATIONAL = "tier_c_aspirational"       # Commercial promotion, curated affluence, debt ads
    COURT_PROCEDURE = "court_procedure"               # Live trials, suspect naming, crime-scene gore
    GOVERNMENT_REPORTING = "government_reporting"     # Investigative reporting on state officials & budgets
    DISTRIBUTION_INFRASTRUCTURE = "distribution_pipe" # Ownership/operation of communications channels


class RestrictionStatus(str, Enum):
    RESTRICT = "restrict"                             # Regulate content conduct / standards
    DO_NOT_RESTRICT = "do_not_restrict"               # Protected creative expression / free depiction
    NEVER_RESTRICT = "never_restrict"                 # Constitutional prohibition on state restriction


class RegulatoryInstrument(str, Enum):
    REPORTING_GUIDELINES_STATUTE = "reporting_guidelines_statute"
    NO_NOTORIETY_PRESS_CODE = "no_notoriety_press_code"
    COURT_PROCEDURE_SUB_JUDICE = "court_procedure_sub_judice"
    PRESS_CODE_PUBLICATION_BAN = "press_code_publication_ban"
    AGE_CLASSIFICATION_ONLY = "age_classification_only"
    DISCLOSURE_AND_ADVERTISING_CODE = "disclosure_and_advertising_code"
    MEDIA_LITERACY_CURRICULUM = "media_literacy_curriculum"
    CONSTITUTIONAL_PROTECTION = "constitutional_protection"
    ANTI_CONCENTRATION_LAW = "anti_concentration_law"


@dataclass(frozen=True)
class ContentPolicyRule:
    category_name: str
    tier: ContentTier
    restriction_status: RestrictionStatus
    instrument: RegulatoryInstrument
    governing_rationale: str
    evidence_base: str


MEDIA_POLICY_RULES: tuple[ContentPolicyRule, ...] = (
    ContentPolicyRule(
        category_name="Operational method detail (suicide, weapons, fraud, hacking)",
        tier=ContentTier.TIER_A_INSTRUCTIONAL,
        restriction_status=RestrictionStatus.RESTRICT,
        instrument=RegulatoryInstrument.REPORTING_GUIDELINES_STATUTE,
        governing_rationale="Restricts the instructional 'how-to'; prevents copycat contagion (Werther effect)",
        evidence_base="WHO suicide reporting guidelines; Austrian subway suicide reporting reductions",
    ),
    ContentPolicyRule(
        category_name="Perpetrator glorification and manifestos (mass shooters)",
        tier=ContentTier.TIER_A_INSTRUCTIONAL,
        restriction_status=RestrictionStatus.RESTRICT,
        instrument=RegulatoryInstrument.NO_NOTORIETY_PRESS_CODE,
        governing_rationale="Denies notoriety incentive; eliminates social learning reward model",
        evidence_base="Bandura social learning theory; mass shooting contagion clustering data",
    ),
    ContentPolicyRule(
        category_name="Real crime as entertainment (court TV, crime-scene footage)",
        tier=ContentTier.COURT_PROCEDURE,
        restriction_status=RestrictionStatus.RESTRICT,
        instrument=RegulatoryInstrument.COURT_PROCEDURE_SUB_JUDICE,
        governing_rationale="Protects judicial dignity, prevents jury poisoning, preserves victim privacy",
        evidence_base="German, French, Dutch, and UK courtroom camera prohibitions",
    ),
    ContentPolicyRule(
        category_name="Naming pre-trial suspects, victims, and minors",
        tier=ContentTier.COURT_PROCEDURE,
        restriction_status=RestrictionStatus.RESTRICT,
        instrument=RegulatoryInstrument.PRESS_CODE_PUBLICATION_BAN,
        governing_rationale="Preserves presumption of innocence and personal dignity ('Andreas B.' standard)",
        evidence_base="German Press Council code; European Court of Human Rights privacy jurisprudence",
    ),
    ContentPolicyRule(
        category_name="Prejudicial pre-trial commentary",
        tier=ContentTier.COURT_PROCEDURE,
        restriction_status=RestrictionStatus.RESTRICT,
        instrument=RegulatoryInstrument.COURT_PROCEDURE_SUB_JUDICE,
        governing_rationale="Prevents trial by media and contamination of witness testimony",
        evidence_base="UK, Canadian, and Indian Contempt of Court / sub judice statutes",
    ),
    ContentPolicyRule(
        category_name="Fiction depicting wrongdoing with consequence",
        tier=ContentTier.TIER_B_DEPICTIVE,
        restriction_status=RestrictionStatus.DO_NOT_RESTRICT,
        instrument=RegulatoryInstrument.AGE_CLASSIFICATION_ONLY,
        governing_rationale="Preserves moral literature and cautionary structure; fiction transmits imitation weakly",
        evidence_base="Decades of falling property crime during saturation of crime drama & fiction",
    ),
    ContentPolicyRule(
        category_name="Undisclosed commercial or financial promotion",
        tier=ContentTier.TIER_C_ASPIRATIONAL,
        restriction_status=RestrictionStatus.RESTRICT,
        instrument=RegulatoryInstrument.DISCLOSURE_AND_ADVERTISING_CODE,
        governing_rationale="Prevents predatory consumer deception, debt traps, and scam contagion",
        evidence_base="French influencer disclosure law; UK FCA / SA FSCA financial promotion rules",
    ),
    ContentPolicyRule(
        category_name="Honest depiction of wealth and lifestyle",
        tier=ContentTier.TIER_C_ASPIRATIONAL,
        restriction_status=RestrictionStatus.DO_NOT_RESTRICT,
        instrument=RegulatoryInstrument.MEDIA_LITERACY_CURRICULUM,
        governing_rationale="Educates audience on staged/financed affluence rather than hiding depiction",
        evidence_base="Gerbner cultivation theory; status anxiety and adolescent mental health research",
    ),
    ContentPolicyRule(
        category_name="Investigative reporting on government and public officials",
        tier=ContentTier.GOVERNMENT_REPORTING,
        restriction_status=RestrictionStatus.NEVER_RESTRICT,
        instrument=RegulatoryInstrument.CONSTITUTIONAL_PROTECTION,
        governing_rationale="Primary instrument of anti-corruption; discomfort to state is the mechanism",
        evidence_base="Historical collapse of anti-corruption mechanisms under state press censorship",
    ),
    ContentPolicyRule(
        category_name="Ownership and control of information distribution channels",
        tier=ContentTier.DISTRIBUTION_INFRASTRUCTURE,
        restriction_status=RestrictionStatus.NEVER_RESTRICT,
        instrument=RegulatoryInstrument.ANTI_CONCENTRATION_LAW,
        governing_rationale="Single distributor creates a single point of capture; plural distribution mandatory",
        evidence_base="State telecommunication monopolies inevitably becoming tools of autocratic suppression",
    ),
)


# --------------------------------------------------------------------------
# 2. Central Technical System: Source vs. Filter Architecture
# --------------------------------------------------------------------------


class SystemMode(str, Enum):
    AUTHORITATIVE_SOURCE = "authoritative_source" # Permitted: Wire service, emergency alert, court registry
    EXCLUSIVE_FILTER = "exclusive_filter"         # Strictly Prohibited: Single gate through which all data passes


@dataclass(frozen=True)
class CentralTechnicalSystemSpec:
    system_name: str
    mode: SystemMode
    is_mandatory_gate: bool
    is_authoritative_source_only: bool

    @property
    def is_constitutionally_valid(self) -> bool:
        # Rule: It may add authoritative information to the system; it may not be the only thing allowed through.
        return (self.mode == SystemMode.AUTHORITATIVE_SOURCE) and (not self.is_mandatory_gate)


VALID_OFFICIAL_WIRE = CentralTechnicalSystemSpec(
    system_name="Community Civic Wire & Court Registry",
    mode=SystemMode.AUTHORITATIVE_SOURCE,
    is_mandatory_gate=False,
    is_authoritative_source_only=True,
)

INVALID_STATE_FILTER = CentralTechnicalSystemSpec(
    system_name="Unified State Internet & Broadcast Filter",
    mode=SystemMode.EXCLUSIVE_FILTER,
    is_mandatory_gate=True,
    is_authoritative_source_only=False,
)


# --------------------------------------------------------------------------
# 3. Courtroom Dignity & Legal Reporting Standards
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class CourtroomReportingPolicy:
    cameras_in_courtroom_allowed: bool = False
    name_suspects_prior_to_conviction: bool = False
    name_minors_or_victims: bool = False
    broadcast_crime_scene_imagery: bool = False
    enforce_sub_judice_rules: bool = True
    public_open_written_registry: bool = True
    citizens_in_person_attendance_allowed: bool = True

    @property
    def is_compliant_with_dignity_standard(self) -> bool:
        return (
            not self.cameras_in_courtroom_allowed
            and not self.name_suspects_prior_to_conviction
            and not self.name_minors_or_victims
            and not self.broadcast_crime_scene_imagery
            and self.enforce_sub_judice_rules
            and self.public_open_written_registry
            and self.citizens_in_person_attendance_allowed
        )


# --------------------------------------------------------------------------
# 4. Commercial & Aspirational Deception Safeguards
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class CommercialDeceptionSafeguards:
    mandatory_paid_promotion_disclosure: bool = True
    mandatory_retouched_image_labeling: bool = True
    ban_undisclosed_influencer_financial_promos: bool = True  # Crypto, forex, gambling
    restrict_debt_and_credit_ads_to_minors: bool = True
    algorithmic_feed_age_gating_under_16: bool = True
    school_media_and_financial_literacy: bool = True


# --------------------------------------------------------------------------
# 5. Media Pluralism and Anti-Concentration Limits
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class MediaPluralismPolicy:
    max_single_entity_audience_share: float = 0.25  # 25% max audience concentration
    mandatory_beneficial_ownership_registry: bool = True
    independent_press_council_with_statutory_backing: bool = True
    enforced_right_of_reply_and_prominent_correction: bool = True
    independent_public_broadcaster_charter: bool = True
    prior_restraint_prohibited: bool = True          # Post-publication accountability only
