"""Tests for War Council, Scenario Planning, and Specialized Strike Units (§24)."""

import pytest

from model.rcu.war_council import (
    AntiCasteSafeguards,
    CouncilVoteResult,
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


def test_war_council_roster_composition():
    assert len(WAR_COUNCIL_ROSTER) == 8
    roles = {m.role for m in WAR_COUNCIL_ROSTER}
    assert WarCouncilRole.CHAIR in roles
    assert WarCouncilRole.DEFENSE_COORDINATOR in roles
    assert WarCouncilRole.CIS_CHIEF in roles
    assert WarCouncilRole.EDMB_CHIEF in roles
    assert WarCouncilRole.RAB_CHIEF in roles
    assert WarCouncilRole.SENIOR_MILITIA_CMD in roles
    assert WarCouncilRole.JUSTICE_COORDINATOR in roles
    assert WarCouncilRole.COMMUNITY_REP in roles


def test_decision_engine_standard_majority():
    proposal = WarDecisionProposal(
        proposal_id="PROP-01",
        description="Deploy 200 militia to northern ridge to intercept approaching raiders",
        is_offensive_action=False,
        predicted_civilian_casualties=0,
        rab_economic_burn_acceptable=True,
        justice_compliance_verified=True,
        is_reversible=True,
    )
    # 4 votes: insufficient
    res = WarCouncilDecisionEngine.evaluate_proposal(proposal, votes_in_favor=4)
    assert not res.approved
    assert "Insufficient votes" in (res.rejection_reason or "")

    # 5 votes: standard majority approval
    res5 = WarCouncilDecisionEngine.evaluate_proposal(proposal, votes_in_favor=5)
    assert res5.approved


def test_decision_engine_24h_delay_no_rule():
    proposal = WarDecisionProposal(
        proposal_id="PROP-02",
        description="Immediate raid on staging point",
        is_offensive_action=False,
        predicted_civilian_casualties=2,
        rab_economic_burn_acceptable=True,
        justice_compliance_verified=True,
        is_reversible=True,
    )
    # 8 votes in favor, but one member invokes the 24-hour delay "No" rule
    res = WarCouncilDecisionEngine.evaluate_proposal(
        proposal, votes_in_favor=8, member_invoking_24h_delay=True
    )
    assert not res.approved
    assert res.delayed_by_no_rule
    assert "Delayed for 24 hours" in (res.rejection_reason or "")


def test_decision_engine_blood_rule_supermajority():
    # Predicted civilian casualties > 10 requires 7/8 supermajority
    high_casualty_prop = WarDecisionProposal(
        proposal_id="PROP-03",
        description="Heavy counter-battery bombardment near village border",
        is_offensive_action=False,
        predicted_civilian_casualties=12,
        rab_economic_burn_acceptable=True,
        justice_compliance_verified=True,
        is_reversible=True,
    )
    # 6 votes: fails Blood Rule
    res6 = WarCouncilDecisionEngine.evaluate_proposal(high_casualty_prop, votes_in_favor=6)
    assert not res6.approved
    assert "required 7" in (res6.rejection_reason or "")

    # 7 votes: passes Blood Rule
    res7 = WarCouncilDecisionEngine.evaluate_proposal(high_casualty_prop, votes_in_favor=7)
    assert res7.approved


def test_decision_engine_offensive_action_constraint():
    offensive_prop = WarDecisionProposal(
        proposal_id="PROP-04",
        description="Cross-border punitive strike on enemy supply depot",
        is_offensive_action=True,
        predicted_civilian_casualties=0,
        rab_economic_burn_acceptable=True,
        justice_compliance_verified=True,
        is_reversible=True,
        community_council_authorized=False,
    )
    # Even with 8 unanimous votes, offensive action without Community Council assent fails
    res = WarCouncilDecisionEngine.evaluate_proposal(offensive_prop, votes_in_favor=8)
    assert not res.approved
    assert "Community Council" in (res.rejection_reason or "")

    # Authorized by Community Council -> passes
    auth_prop = WarDecisionProposal(
        proposal_id="PROP-04-AUTH",
        description="Cross-border punitive strike with Council decree",
        is_offensive_action=True,
        predicted_civilian_casualties=0,
        rab_economic_burn_acceptable=True,
        justice_compliance_verified=True,
        is_reversible=True,
        community_council_authorized=True,
    )
    res_auth = WarCouncilDecisionEngine.evaluate_proposal(auth_prop, votes_in_favor=5)
    assert res_auth.approved


def test_decision_engine_rab_and_justice_vetoes():
    prop_justice_fail = WarDecisionProposal(
        proposal_id="PROP-05",
        description="Water poisoning of enemy approach route",
        is_offensive_action=False,
        predicted_civilian_casualties=0,
        rab_economic_burn_acceptable=True,
        justice_compliance_verified=False,  # Fails Geneva / anti-atrocity check
        is_reversible=False,
    )
    res_j = WarCouncilDecisionEngine.evaluate_proposal(prop_justice_fail, votes_in_favor=8)
    assert not res_j.approved
    assert "customary law" in (res_j.rejection_reason or "")

    prop_rab_fail = WarDecisionProposal(
        proposal_id="PROP-06",
        description="Full-scale protracted foreign siege consuming 80% of grain reserves",
        is_offensive_action=False,
        predicted_civilian_casualties=0,
        rab_economic_burn_acceptable=False,  # Unaffordable burn rate
        justice_compliance_verified=True,
        is_reversible=True,
    )
    res_rab = WarCouncilDecisionEngine.evaluate_proposal(prop_rab_fail, votes_in_favor=8)
    assert not res_rab.approved
    assert "RAB assessment" in (res_rab.rejection_reason or "")


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


def test_specialized_units_sizing_and_limits():
    assert len(SPECIALIZED_UNITS_ROSTER) == 7
    sizing = SpecializedUnitSizing(population=10000, militia_size=3500)

    assert 155 <= sizing.total_specialized_nominal <= 195
    assert sizing.fraction_of_militia < 0.05  # Less than 5% of militia
    assert sizing.fraction_of_population < 0.02  # Less than 2% of population

    # Check specific unit nominal sizes
    unit_map = {u.unit_type: u for u in SPECIALIZED_UNITS_ROSTER}
    assert unit_map[SpecializedUnitType.STRIKE_TEAM].nominal_size == 4
    assert unit_map[SpecializedUnitType.THE_HAMMER].nominal_size == 40
    assert 20 <= unit_map[SpecializedUnitType.THE_SCORPION].nominal_size <= 30
    assert 20 <= unit_map[SpecializedUnitType.THE_WORM].nominal_size <= 30
    assert 10 <= unit_map[SpecializedUnitType.THE_HEALER].nominal_size <= 15
    assert 10 <= unit_map[SpecializedUnitType.THE_ECHO].nominal_size <= 15
    assert 30 <= unit_map[SpecializedUnitType.THE_HORSE].nominal_size <= 50


def test_anti_caste_safeguards():
    safeguards = AntiCasteSafeguards()
    assert safeguards.max_consecutive_service_years <= 3
    assert safeguards.separate_barracks_allowed is False
    assert safeguards.separate_pay_or_privilege is False
    assert safeguards.hereditary_recruitment_allowed is False
    assert safeguards.holding_civilian_political_office is False
    assert safeguards.right_of_refusal_for_offensive_action is True
    assert safeguards.no_elite_branding_names is True


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
