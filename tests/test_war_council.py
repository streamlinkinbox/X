"""Tests for War Council, Scenario Planning, and Specialized Strike Units (§24)."""

import pytest

from model.rcu.war_council import (
    AntiCasteSafeguards,
    CouncilVoteResult,
    DOCTRINE_PRINCIPLES,
    EngagementBattleReport,
    SCENARIO_LIBRARY,
    SPECIALIZED_UNITS_ROSTER,
    SpecializedUnitSizing,
    SpecializedUnitType,
    WAR_COUNCIL_ROSTER,
    WarCouncilDecisionEngine,
    WarCouncilRole,
    WarDecisionProposal,
    WarRoomRules,
)


def test_war_council_seven_seats():
    assert len(WAR_COUNCIL_ROSTER) == 7
    roles = {m.role for m in WAR_COUNCIL_ROSTER}
    assert WarCouncilRole.STRATEGIST in roles
    assert WarCouncilRole.INTELLIGENCE_OFFICER in roles
    assert WarCouncilRole.OPERATIONS_OFFICER in roles
    assert WarCouncilRole.LOGISTICS_OFFICER in roles
    assert WarCouncilRole.DECEPTION_OFFICER in roles
    assert WarCouncilRole.TERRAIN_OFFICER in roles
    assert WarCouncilRole.COMMUNITY_LIAISON in roles

    # Verify specific veto powers
    logistics = next(m for m in WAR_COUNCIL_ROSTER if m.role == WarCouncilRole.LOGISTICS_OFFICER)
    assert logistics.has_specific_veto is True
    assert "Cost" in (logistics.veto_scope or "")

    liaison = next(m for m in WAR_COUNCIL_ROSTER if m.role == WarCouncilRole.COMMUNITY_LIAISON)
    assert liaison.has_specific_veto is True
    assert "Offensive" in (liaison.veto_scope or "")


def test_decision_engine_standard_majority_four_of_seven():
    proposal = WarDecisionProposal(
        proposal_id="PROP-01",
        description="Deploy 200 militia to northern ridge to intercept approaching raiders",
        is_offensive_action=False,
        predicted_civilian_casualties=0,
        logistics_officer_affordability_approved=True,
        is_reversible=True,
    )
    # 3 votes: insufficient
    res3 = WarCouncilDecisionEngine.evaluate_proposal(proposal, votes_in_favor=3)
    assert not res3.approved
    assert "Insufficient votes" in (res3.rejection_reason or "")

    # 4 votes: standard majority approval (4 of 7)
    res4 = WarCouncilDecisionEngine.evaluate_proposal(proposal, votes_in_favor=4)
    assert res4.approved


def test_decision_engine_24h_delay_no_rule():
    proposal = WarDecisionProposal(
        proposal_id="PROP-02",
        description="Immediate raid on staging point",
        is_offensive_action=False,
        predicted_civilian_casualties=2,
        logistics_officer_affordability_approved=True,
        is_reversible=True,
    )
    # 7 votes in favor, but one member invokes the 24-hour delay "No" rule
    res = WarCouncilDecisionEngine.evaluate_proposal(
        proposal, votes_in_favor=7, member_invoking_24h_delay=True
    )
    assert not res.approved
    assert res.delayed_by_no_rule
    assert "Delayed for 24 hours" in (res.rejection_reason or "")


def test_decision_engine_blood_rule_supermajority_six_of_seven():
    # Predicted civilian casualties >= 10 requires 6/7 supermajority
    high_casualty_prop = WarDecisionProposal(
        proposal_id="PROP-03",
        description="Heavy counter-battery bombardment near village border",
        is_offensive_action=False,
        predicted_civilian_casualties=12,
        logistics_officer_affordability_approved=True,
        is_reversible=True,
    )
    # 5 votes: fails Blood Rule (requires 6)
    res5 = WarCouncilDecisionEngine.evaluate_proposal(high_casualty_prop, votes_in_favor=5)
    assert not res5.approved
    assert "required 6" in (res5.rejection_reason or "")

    # 6 votes: passes Blood Rule
    res6 = WarCouncilDecisionEngine.evaluate_proposal(high_casualty_prop, votes_in_favor=6)
    assert res6.approved


def test_decision_engine_offensive_action_constraint():
    offensive_prop = WarDecisionProposal(
        proposal_id="PROP-04",
        description="Cross-border punitive strike on enemy supply depot",
        is_offensive_action=True,
        predicted_civilian_casualties=0,
        logistics_officer_affordability_approved=True,
        is_reversible=True,
        community_council_authorized=False,
    )
    # Even with 7 unanimous votes, offensive action without Community Council assent fails
    res = WarCouncilDecisionEngine.evaluate_proposal(offensive_prop, votes_in_favor=7)
    assert not res.approved
    assert "Community Liaison Veto" in (res.rejection_reason or "")

    # Authorized by Community Council -> passes
    auth_prop = WarDecisionProposal(
        proposal_id="PROP-04-AUTH",
        description="Cross-border punitive strike with Council decree",
        is_offensive_action=True,
        predicted_civilian_casualties=0,
        logistics_officer_affordability_approved=True,
        is_reversible=True,
        community_council_authorized=True,
    )
    res_auth = WarCouncilDecisionEngine.evaluate_proposal(auth_prop, votes_in_favor=4)
    assert res_auth.approved


def test_decision_engine_logistics_officer_cost_veto():
    prop_unaffordable = WarDecisionProposal(
        proposal_id="PROP-05",
        description="Massive expeditionary siege consuming 75% of fuel and grain stores",
        is_offensive_action=False,
        predicted_civilian_casualties=0,
        logistics_officer_affordability_approved=False,  # Logistics Officer Veto
        is_reversible=True,
    )
    res = WarCouncilDecisionEngine.evaluate_proposal(prop_unaffordable, votes_in_favor=7)
    assert not res.approved
    assert "Logistics Officer veto" in (res.rejection_reason or "")


def test_doctrine_principles():
    assert len(DOCTRINE_PRINCIPLES) == 6
    names = [p.rule_name for p in DOCTRINE_PRINCIPLES]
    assert "DON'T MIRROR" in names
    assert "DON'T CHASE" in names
    assert "DON'T HOLD" in names
    assert "Strike the System, Not the Mass" in names
    assert "Deception First" in names
    assert "Mobility > Numbers" in names


def test_scenario_library_completeness():
    assert len(SCENARIO_LIBRARY) == 10
    codes = [s.code for s in SCENARIO_LIBRARY]
    assert codes == ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "S10"]
    for s in SCENARIO_LIBRARY:
        assert len(s.name) > 0
        assert len(s.adversary_scale) > 0
        assert len(s.early_warning_lead_time) > 0
        assert len(s.primary_response_phase) > 0


def test_war_room_rules():
    rules = WarRoomRules()
    assert rules.no_rank_equality is True
    assert rules.mandatory_sleep_hours == 6
    assert rules.total_communication_isolation is True
    assert rules.min_participants == 8
    assert rules.max_participants == 15
    assert rules.min_duration_hours == 24
    assert rules.max_duration_hours == 72


def test_specialized_units_functional_naming_and_sizing():
    assert len(SPECIALIZED_UNITS_ROSTER) == 7
    sizing = SpecializedUnitSizing(population=10000, militia_size=3500)

    assert 155 <= sizing.total_specialized_nominal <= 195
    assert sizing.fraction_of_militia < 0.05  # Less than 5% of militia
    assert sizing.fraction_of_population < 0.02  # Less than 2% of population

    # Verify no prestige names
    for u in SPECIALIZED_UNITS_ROSTER:
        assert "Guard" not in u.functional_name
        assert "Immortal" not in u.functional_name
        assert "Janissar" not in u.functional_name
        assert "Elite" not in u.functional_name


def test_anti_caste_safeguards():
    safeguards = AntiCasteSafeguards()
    assert safeguards.max_consecutive_service_years <= 3
    assert safeguards.separate_barracks_allowed is False
    assert safeguards.separate_pay_or_privilege is False
    assert safeguards.hereditary_recruitment_allowed is False
    assert safeguards.holding_civilian_political_office is False
    assert safeguards.right_of_refusal_for_offensive_action is True
    assert safeguards.no_elite_branding_names is True
    assert safeguards.skills_distributed_to_guilds is True


def test_integrated_battle_simulation():
    battle = EngagementBattleReport(
        enemy_initial_force=500,
        enemy_tanks=5,
        enemy_drones=20,
        community_militia_deployed=2000,
        specialized_operators_deployed=158,
        enemy_casualties_killed=200,
        enemy_casualties_captured=150,
        enemy_tanks_neutralized=5,
        enemy_drones_neutralized=20,
        community_militia_killed=30,
        community_militia_wounded=80,
    )
    assert battle.enemy_attrition_rate == 0.70  # (200 + 150) / 500 = 70% attrition
    assert battle.casualty_exchange_ratio == pytest.approx(350 / 110, 0.01)
    assert battle.enemy_tanks_neutralized == 5
    assert battle.enemy_drones_neutralized == 20
    assert battle.commander_eliminated_by_strike_team is True
