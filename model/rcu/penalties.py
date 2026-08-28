"""Non-Cash Penalty and Restorative Justice System: Ending Roadside Bribery and Policing-for-Profit.

This module models the community justice and anti-extortion penalty architecture:
1. ``PenaltyTier`` -- 4-tier non-cash penalty ladder replacing cash fines with public labor:
   - Tier 1: Minor Infractions (4-8 hours civic maintenance: drain/sewer clearing, pothole patching)
   - Tier 2: Reckless Disruption (16-40 hours hard labor + 30-day vehicle impound)
   - Tier 3: Predatory Crime (100-300 hours supervised guild labor + 100% direct victim restitution)
   - Tier 4: Extreme Recidivism / Treason / Police Extortion (Community Exile / Banishment)
2. ``ZeroRoadsideCash`` -- Absolute demonetization of traffic/civic enforcement; felony for officers
   to accept, demand, or carry cash on duty.
3. ``VictimRestitution`` -- 100% of property recovery goes to the harmed victim; exactly 0% goes
   to police department budgets or state slush funds.
4. ``AntiExtortionLocks`` -- Reverse bounties on bribe solicitation, RAB quota-hunting anomaly detection,
   and 6-month mandatory patrol rotation.
5. ``SortitionTribunal`` -- 3-citizen random jury dispute resolution with automatic dismissal if
   dashcam/bodycam footage is missing.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# --------------------------------------------------------------------------
# 1. Penalty Tiers & Civic Labor Types
# --------------------------------------------------------------------------


class PenaltyTier(str, Enum):
    TIER_1_MINOR = "tier_1_minor"               # Speeding, red light, littering, noise
    TIER_2_RECKLESS = "tier_2_reckless"         # Reckless/drunk driving, brawls, vandalism
    TIER_3_PREDATORY = "tier_3_predatory"       # Theft, burglary, fraud, assault
    TIER_4_EXILE_EXTORTION = "tier_4_exile"     # Officer bribe extortion, armed treason, irredeemable predation


class CivicLaborType(str, Enum):
    SEWER_AND_DRAIN_CLEARING = "sewer_and_drain_clearing"
    ROAD_AND_POTHOLE_REPAIR = "road_and_pothole_repair"
    FIRE_DEFENSE_BRUSH_CLEARING = "fire_defense_brush_clearing"
    AGRICULTURAL_SILT_REMOVAL = "agricultural_silt_removal"
    PUBLIC_BUILDING_SANITATION = "public_building_sanitation"
    SUPERVISED_GUILD_RESTORATION = "supervised_guild_restoration"


@dataclass(frozen=True)
class PenaltyTierSpec:
    tier: PenaltyTier
    name: str
    target_offenses: str
    min_labor_hours: int
    max_labor_hours: int
    nominal_labor_hours: int
    primary_labor_duty: CivicLaborType
    restitution_multiplier: float
    vehicle_impound_days: int
    exile_applicable: bool = False


PENALTY_TIER_ROSTER: tuple[PenaltyTierSpec, ...] = (
    PenaltyTierSpec(
        tier=PenaltyTier.TIER_1_MINOR,
        name="Tier 1: Minor Civic Infractions",
        target_offenses="Speeding, signal violation, illegal dumping, excessive noise",
        min_labor_hours=4,
        max_labor_hours=8,
        nominal_labor_hours=6,
        primary_labor_duty=CivicLaborType.SEWER_AND_DRAIN_CLEARING,
        restitution_multiplier=1.0,
        vehicle_impound_days=0,
        exile_applicable=False,
    ),
    PenaltyTierSpec(
        tier=PenaltyTier.TIER_2_RECKLESS,
        name="Tier 2: Reckless / Disruption",
        target_offenses="Reckless/drunk driving, street fighting, intentional property damage",
        min_labor_hours=16,
        max_labor_hours=40,
        nominal_labor_hours=24,
        primary_labor_duty=CivicLaborType.ROAD_AND_POTHOLE_REPAIR,
        restitution_multiplier=1.5,
        vehicle_impound_days=30,
        exile_applicable=False,
    ),
    PenaltyTierSpec(
        tier=PenaltyTier.TIER_3_PREDATORY,
        name="Tier 3: Predatory Crime",
        target_offenses="Theft, burglary, commercial fraud, physical assault",
        min_labor_hours=100,
        max_labor_hours=300,
        nominal_labor_hours=200,
        primary_labor_duty=CivicLaborType.SUPERVISED_GUILD_RESTORATION,
        restitution_multiplier=2.0,
        vehicle_impound_days=90,
        exile_applicable=False,
    ),
    PenaltyTierSpec(
        tier=PenaltyTier.TIER_4_EXILE_EXTORTION,
        name="Tier 4: Extreme Predation & Officer Extortion",
        target_offenses="Police bribe solicitation, armed extortion, repeat violent predation, treason",
        min_labor_hours=500,
        max_labor_hours=2000,
        nominal_labor_hours=1000,
        primary_labor_duty=CivicLaborType.SEWER_AND_DRAIN_CLEARING,
        restitution_multiplier=3.0,
        vehicle_impound_days=365,
        exile_applicable=True,
    ),
)


# --------------------------------------------------------------------------
# 2. Restitution Allocation: 100% Victim, 0% Police Revenue
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class RestitutionAccounting:
    damage_assessed_rcu: float
    restitution_multiplier: float = 2.0

    @property
    def total_restitution_paid_rcu(self) -> float:
        return self.damage_assessed_rcu * self.restitution_multiplier

    @property
    def victim_allocation_rcu(self) -> float:
        # 100% goes directly to the harmed victim
        return self.total_restitution_paid_rcu

    @property
    def police_department_revenue_rcu(self) -> float:
        # Exactly 0% goes to the police station or citing officers
        return 0.0

    @property
    def municipal_slush_fund_allocation_rcu(self) -> float:
        # Zero cash flow into state slush funds
        return 0.0


# --------------------------------------------------------------------------
# 3. Anti-Extortion Locks (Ending Roadside Shakedowns)
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class AntiExtortionPolicy:
    officer_cash_possession_on_duty_is_felony: bool = True
    roadside_cash_collection_prohibited: bool = True
    digital_or_paper_citation_only: bool = True
    mandatory_dashcam_bodycam_evidence: bool = True
    reverse_bounty_on_reported_bribe_solicitation_rcu: float = 500.0
    patrol_officer_mandatory_rotation_months: int = 6
    rab_quota_hunting_anomaly_detection: bool = True

    @property
    def is_anti_bribery_complete(self) -> bool:
        return (
            self.officer_cash_possession_on_duty_is_felony
            and self.roadside_cash_collection_prohibited
            and self.digital_or_paper_citation_only
            and self.mandatory_dashcam_bodycam_evidence
            and self.rab_quota_hunting_anomaly_detection
        )


# --------------------------------------------------------------------------
# 4. Sortition Dispute Tribunal (3-Citizen Random Jury)
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class CitationDispute:
    citation_id: str
    officer_id: str
    citizen_id: str
    alleged_offense: str
    officer_provided_dashcam_footage: bool
    citizen_appealed_within_7_days: bool
    jury_size: int = 3

    def resolve_dispute(self, citizen_jury_votes_to_uphold: int) -> dict[str, str | bool]:
        # Rule: Missing dashcam/bodycam footage results in automatic dismissal
        if not self.officer_provided_dashcam_footage:
            return {
                "citation_id": self.citation_id,
                "verdict": "DISMISSED_AUTOMATICALLY",
                "upheld": False,
                "reason": "Officer failed to provide mandatory dashcam/bodycam evidence",
                "officer_disciplinary_flag": True,
            }

        if citizen_jury_votes_to_uphold >= 2:
            return {
                "citation_id": self.citation_id,
                "verdict": "UPHELD",
                "upheld": True,
                "reason": f"Citizen sortition jury upheld citation ({citizen_jury_votes_to_uphold}/3 votes)",
                "officer_disciplinary_flag": False,
            }
        else:
            return {
                "citation_id": self.citation_id,
                "verdict": "OVERTURNED",
                "upheld": False,
                "reason": f"Citizen sortition jury overturned citation ({citizen_jury_votes_to_uphold}/3 votes)",
                "officer_disciplinary_flag": False,
            }


# --------------------------------------------------------------------------
# 5. Community Exile / Banishment Protocol (Tier 4 Extreme Cases)
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class ExileAssessment:
    candidate_id: str
    offense_description: str
    prior_unreformed_tier3_convictions: int
    refused_mandatory_restorative_labor: bool
    is_armed_treason_or_lethal_predation: bool
    council_supermajority_approved: bool

    @property
    def qualifies_for_community_exile(self) -> bool:
        # Exile is reserved strictly for irredeemable predatory recidivism or armed treason
        # and requires Community Council 75% supermajority approval (§20)
        has_grounds = (
            self.is_armed_treason_or_lethal_predation
            or (self.prior_unreformed_tier3_convictions >= 3 and self.refused_mandatory_restorative_labor)
        )
        return has_grounds and self.council_supermajority_approved
