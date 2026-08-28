"""Tests for National Media and Information Integrity Act Framework (§25)."""

import pytest

from model.rcu.information_integrity import (
    CONSOLIDATED_POLICY_MATRIX,
    IMPLEMENTATION_PHASES,
    SANCTION_LADDER,
    STATUTORY_BODIES,
    ConsolidatedRule,
    ForeignPlatformEnforcementModel,
    PlatformStatutoryDuties,
    RegulatoryBodyType,
    RestrictionStatus,
    SanctionStep,
    StateConductPolicy,
    StatutoryFundingFormula,
)


def test_statutory_bodies_and_formula_funding():
    assert len(STATUTORY_BODIES) == 3
    body_types = {b.body_type for b in STATUTORY_BODIES}
    assert RegulatoryBodyType.MSA in body_types
    assert RegulatoryBodyType.III in body_types
    assert RegulatoryBodyType.TRIBUNAL in body_types

    for b in STATUTORY_BODIES:
        assert b.board_term_years == 6
        assert b.is_ministerial_direction_prohibited is True

    funding = StatutoryFundingFormula()
    assert funding.is_genuinely_independent is True
    assert funding.broadcast_fee_levy_percent > 0
    assert funding.digital_ad_revenue_levy_percent > 0
    assert funding.annual_ministerial_budget_discretion is False


def test_sanction_ladder_automatic_escalation():
    assert len(SANCTION_LADDER) == 7
    steps = [s.step for s in SANCTION_LADDER]
    assert steps == [
        SanctionStep.STEP_1_ADVISORY,
        SanctionStep.STEP_2_PUBLISHED_FINDING,
        SanctionStep.STEP_3_CORRECTION,
        SanctionStep.STEP_4_TURNOVER_FINE,
        SanctionStep.STEP_5_LICENSE_CONDITION,
        SanctionStep.STEP_6_COMMERCIAL_SUSPENSION,
        SanctionStep.STEP_7_LICENSE_REVOCATION,
    ]

    # Repeat breaches from step 2 onward trigger automatic escalation
    for s in SANCTION_LADDER:
        if s.step >= SanctionStep.STEP_2_PUBLISHED_FINDING:
            assert s.is_automatic_on_repeat_breach is True


def test_foreign_platform_money_layer_enforcement():
    foreign = ForeignPlatformEnforcementModel()
    assert foreign.is_enforceable_without_foreign_treaty is True
    assert foreign.mandatory_resident_legal_representative is True
    assert foreign.ad_spend_tax_deductibility_disallowance is True
    assert foreign.payment_processor_settlement_prohibition is True
    # Crucial: network-layer packet blocking is strictly prohibited
    assert foreign.network_layer_packet_filtering_prohibited is True


def test_platform_amplification_statutory_duties():
    duties = PlatformStatutoryDuties()
    assert duties.annual_independent_ranking_audit is True
    assert duties.published_systemic_risk_assessment is True
    assert duties.non_personalized_feed_default_option is True
    assert duties.no_engagement_optimization_under_16 is True
    assert duties.public_political_ad_register_5yr is True
    assert duties.independent_researcher_data_access is True
    assert duties.virality_friction_controls is True
    assert duties.provenance_credential_display is True
    assert duties.no_encryption_backdoors_or_escrow is True


def test_state_conduct_discipline_safeguards():
    state_policy = StateConductPolicy()
    assert state_policy.state_ad_spend_published_formula_only is True
    assert state_policy.state_ad_deviation_is_criminal_offence is True
    assert state_policy.foi_deemed_grant_on_deadline_lapse is True
    assert state_policy.foi_fees_capped_at_reproduction_cost is True
    assert state_policy.whistleblower_reversed_burden_of_proof is True
    assert state_policy.mandatory_anti_slapp_early_dismissal is True
    assert state_policy.astroturfing_by_public_bodies_criminalized is True
    assert state_policy.functional_press_definition_no_licensing is True


def test_consolidated_policy_matrix():
    assert len(CONSOLIDATED_POLICY_MATRIX) == 13

    # Check government reporting is NEVER restricted
    gov_rule = next(
        r for r in CONSOLIDATED_POLICY_MATRIX if "Investigative reporting on government" in r.category
    )
    assert gov_rule.status == RestrictionStatus.NEVER_RESTRICT

    # Check pipe ownership is NEVER restricted/monopolized
    pipe_rule = next(
        r for r in CONSOLIDATED_POLICY_MATRIX if "Ownership and control of information" in r.category
    )
    assert pipe_rule.status == RestrictionStatus.NEVER_RESTRICT

    # Check fiction is NOT restricted
    fiction_rule = next(
        r for r in CONSOLIDATED_POLICY_MATRIX if "Fiction depicting wrongdoing" in r.category
    )
    assert fiction_rule.status == RestrictionStatus.DO_NOT_RESTRICT

    # Check algorithmic amplification is ACCOUNTABLE
    algo_rule = next(
        r for r in CONSOLIDATED_POLICY_MATRIX if "Algorithmic amplification systems" in r.category
    )
    assert algo_rule.status == RestrictionStatus.ACCOUNTABLE


def test_implementation_phases_sequence():
    assert len(IMPLEMENTATION_PHASES) == 5
    # Phase 1 must discipline the state first
    phase1 = IMPLEMENTATION_PHASES[0]
    assert phase1.phase_number == 1
    assert "State Self-Discipline" in phase1.phase_name
    assert any("formula-only state advertising" in a for a in phase1.core_actions)
    assert any("Anti-SLAPP" in a for a in phase1.core_actions)
