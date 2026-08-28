"""Tests for Anti-Corruption, Incompetence Diagnostics, and Resource Curse Prevention."""

from __future__ import annotations

import sys
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from model.rcu.integrity import (  # noqa: E402
    EnvironmentalStress,
    EvaluationVerdict,
    LeadershipDiagnostic,
    MarketConcentrationPolicy,
    MarketParticipant,
    ObservedOutcome,
    PersonalWealthAudit,
    PositionAudit,
    ProbationTarget,
    RevenueDiversification,
    ShadowLeaderProbation,
)


# --------------------------------------------------------------------------
# 1. Leadership Incompetence vs Difficulty Diagnostics
# --------------------------------------------------------------------------


def test_mild_conditions_good_outcome_is_untested():
    diag = LeadershipDiagnostic(
        stress_level=EnvironmentalStress.MILD,
        outcome=ObservedOutcome.ACCEPTABLE,
        correct_diagnosis=True,
        efficient_resource_use=True,
        adapted_to_shocks=True,
        honest_communication=True,
        consulted_domain_experts=True,
        personal_wealth_divergence=False,
        community_loss_pct=5.0,
        peer_community_loss_pct=5.0,
    )
    assert diag.verdict == EvaluationVerdict.COMPETENT_UNTESTED


def test_mild_conditions_bad_outcome_is_incompetent():
    diag = LeadershipDiagnostic(
        stress_level=EnvironmentalStress.MILD,
        outcome=ObservedOutcome.POOR,
        correct_diagnosis=False,
        efficient_resource_use=False,
        adapted_to_shocks=False,
        honest_communication=True,
        consulted_domain_experts=False,
        personal_wealth_divergence=False,
        community_loss_pct=25.0,
        peer_community_loss_pct=5.0,
    )
    assert diag.verdict == EvaluationVerdict.INCOMPETENT_REMOVE


def test_severe_conditions_good_outcome_is_exceptional():
    diag = LeadershipDiagnostic(
        stress_level=EnvironmentalStress.SEVERE,
        outcome=ObservedOutcome.EXCELLENT,
        correct_diagnosis=True,
        efficient_resource_use=True,
        adapted_to_shocks=True,
        honest_communication=True,
        consulted_domain_experts=True,
        personal_wealth_divergence=False,
        community_loss_pct=10.0,
        peer_community_loss_pct=40.0,
    )
    assert diag.verdict == EvaluationVerdict.EXCEPTIONAL_RETAIN


def test_severe_conditions_with_personal_enrichment_is_immediately_removed():
    """If leader prospers while community starves, remove regardless of stress."""
    diag = LeadershipDiagnostic(
        stress_level=EnvironmentalStress.SEVERE,
        outcome=ObservedOutcome.POOR,
        correct_diagnosis=True,
        efficient_resource_use=True,
        adapted_to_shocks=True,
        honest_communication=True,
        consulted_domain_experts=True,
        personal_wealth_divergence=True,  # Red line
        community_loss_pct=35.0,
        peer_community_loss_pct=35.0,
    )
    assert diag.verdict == EvaluationVerdict.INCOMPETENT_REMOVE


def test_severe_conditions_significantly_worse_than_neighbors_is_removed():
    """Losing 45% when neighbors lost only 15% is leadership failure, not weather."""
    diag = LeadershipDiagnostic(
        stress_level=EnvironmentalStress.SEVERE,
        outcome=ObservedOutcome.POOR,
        correct_diagnosis=True,
        efficient_resource_use=True,
        adapted_to_shocks=True,
        honest_communication=True,
        consulted_domain_experts=True,
        personal_wealth_divergence=False,
        community_loss_pct=45.0,
        peer_community_loss_pct=15.0,
    )
    assert diag.verdict == EvaluationVerdict.INCOMPETENT_REMOVE


def test_severe_conditions_honest_and_competent_effort_triggers_peer_review():
    diag = LeadershipDiagnostic(
        stress_level=EnvironmentalStress.SEVERE,
        outcome=ObservedOutcome.POOR,
        correct_diagnosis=True,
        efficient_resource_use=True,
        adapted_to_shocks=True,
        honest_communication=True,
        consulted_domain_experts=True,
        personal_wealth_divergence=False,
        community_loss_pct=30.0,
        peer_community_loss_pct=28.0,
    )
    assert diag.verdict == EvaluationVerdict.PEER_REVIEW_REQUIRED


# --------------------------------------------------------------------------
# 2. Shadow Leader System & 90-Day Probation
# --------------------------------------------------------------------------


def test_deputy_passing_quantitative_targets_confirmed():
    probation = ShadowLeaderProbation(
        deputy_id="DEP-AG-02",
        domain="Agriculture",
        probation_days=90,
        targets=(
            ProbationTarget("Reduce spoilage rate", 15.0, 10.0, 8.5, higher_is_better=False),
            ProbationTarget("Increase seed reserve kg", 1000.0, 1500.0, 1600.0, higher_is_better=True),
            ProbationTarget("Apprentice graduation count", 0.0, 5.0, 5.0, higher_is_better=True),
            ProbationTarget("Emergency irrigation repair days", 14.0, 7.0, 5.0, higher_is_better=False),
        ),
    )
    assert probation.targets_passed_count == 4
    assert probation.pass_rate == Decimal("1.00")
    assert probation.confirmed


def test_deputy_failing_targets_rejected():
    probation = ShadowLeaderProbation(
        deputy_id="DEP-AG-03",
        domain="Agriculture",
        probation_days=90,
        targets=(
            ProbationTarget("Reduce spoilage rate", 15.0, 10.0, 16.0, higher_is_better=False), # Failed
            ProbationTarget("Increase seed reserve kg", 1000.0, 1500.0, 1100.0, higher_is_better=True), # Failed
            ProbationTarget("Apprentice graduation count", 0.0, 5.0, 2.0, higher_is_better=True), # Failed
            ProbationTarget("Emergency irrigation repair days", 14.0, 7.0, 6.0, higher_is_better=False), # Passed
        ),
    )
    assert probation.targets_passed_count == 1
    assert probation.pass_rate == Decimal("0.25")
    assert not probation.confirmed


# --------------------------------------------------------------------------
# 3. Phantom Employment Auditing
# --------------------------------------------------------------------------


def test_light_switching_job_detected_as_phantom():
    phantom = PositionAudit(
        job_title="Substation Light Switcher",
        department="Municipal Services",
        monthly_compensation_rcu=1000.0,
        measured_monthly_output_value_rcu=0.0,
        has_tangible_deliverable=False,
    )
    assert phantom.is_phantom_job
    assert phantom.output_to_cost_ratio == Decimal("0.00")


def test_genuine_productive_job_clears_audit():
    genuine = PositionAudit(
        job_title="Grain Silo Maintainer",
        department="Reserves",
        monthly_compensation_rcu=800.0,
        measured_monthly_output_value_rcu=2400.0,
        has_tangible_deliverable=True,
    )
    assert not genuine.is_phantom_job
    assert genuine.output_to_cost_ratio >= Decimal("1.00")


# --------------------------------------------------------------------------
# 4. Resource Curse & Diversification Metrics
# --------------------------------------------------------------------------


def test_single_commodity_oil_economy_is_resource_cursed():
    oil_economy = RevenueDiversification(
        revenue_shares={
            "Crude Oil Extraction": 0.85,
            "Subsistence Agriculture": 0.08,
            "Services": 0.07,
        }
    )
    assert oil_economy.hhi_score > 7000
    assert oil_economy.is_resource_cursed
    assert oil_economy.primary_commodity_share == 0.85


def test_rcu_multi_commodity_basket_is_diversified():
    rcu_basket = RevenueDiversification(
        revenue_shares={
            "Maize & Grains": 0.15,
            "Legumes & Pulses": 0.10,
            "Timber & Wood": 0.12,
            "Scrap & Iron": 0.10,
            "Biofuel & Biogas": 0.08,
            "Textiles & Cotton": 0.08,
            "Livestock": 0.12,
            "Processed Soap & Oils": 0.09,
            "Medical Oxygen & Salts": 0.08,
            "Apprentice Services": 0.08,
        }
    )
    assert rcu_basket.hhi_score < 1500
    assert not rcu_basket.is_resource_cursed
    assert rcu_basket.primary_commodity_share <= 0.20


# --------------------------------------------------------------------------
# 5. Anti-Monopoly 20% Cap
# --------------------------------------------------------------------------


def test_exclusive_car_license_violates_anti_monopoly_cap():
    market = MarketConcentrationPolicy(
        market_name="Automotive Imports",
        participants=(
            MarketParticipant("MONO-01", "Family A", 0.65),  # 65% share
            MarketParticipant("COMP-02", "Family B", 0.20),
            MarketParticipant("COMP-03", "Family C", 0.15),
        ),
        max_allowed_share_fraction=0.20,
    )
    assert market.monopoly_breach
    assert len(market.violating_entities) == 1
    assert market.violating_entities[0].entity_id == "MONO-01"


def test_competitive_market_clears_cap():
    market = MarketConcentrationPolicy(
        market_name="Grain Milling",
        participants=(
            MarketParticipant("MILL-01", "Coop A", 0.18),
            MarketParticipant("MILL-02", "Coop B", 0.19),
            MarketParticipant("MILL-03", "Coop C", 0.15),
            MarketParticipant("MILL-04", "Coop D", 0.17),
            MarketParticipant("MILL-05", "Coop E", 0.16),
            MarketParticipant("MILL-06", "Coop F", 0.15),
        ),
        max_allowed_share_fraction=0.20,
    )
    assert not market.monopoly_breach
    assert len(market.violating_entities) == 0


# --------------------------------------------------------------------------
# 6. Personal Wealth Accumulation Ceiling
# --------------------------------------------------------------------------


def test_modest_personal_holdings_permitted():
    audit = PersonalWealthAudit(
        coordinator_id="COORD-01",
        personal_holdings_rcu=4500.0,
        community_average_holdings_rcu=1500.0,
        max_allowed_multiplier=5.0,
    )
    assert audit.wealth_ratio == Decimal("3.00")
    assert not audit.ceiling_exceeded


def test_excessive_personal_enrichment_triggers_breach():
    audit = PersonalWealthAudit(
        coordinator_id="COORD-02",
        personal_holdings_rcu=15000.0,
        community_average_holdings_rcu=1500.0,
        max_allowed_multiplier=5.0,
    )
    assert audit.wealth_ratio == Decimal("10.00")
    assert audit.ceiling_exceeded
