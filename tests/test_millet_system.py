"""Tests for Pluralism, Personal Status Law, and State Gap Audit (§29)."""

import pytest

from model.rcu.millet_system import (
    AntiLebanonLock,
    AuthorityLayer,
    GapStatus,
    GovernanceGapRecord,
    HumanRightsFloor,
    JurisdictionalDomain,
    MILLET_JURISDICTION_DOMAINS,
    STATE_GAP_AUDIT_REGISTER,
)


def test_millet_jurisdiction_domains_completeness():
    assert len(MILLET_JURISDICTION_DOMAINS) == 7
    layers = {d.authority_layer for d in MILLET_JURISDICTION_DOMAINS}
    assert AuthorityLayer.STATE_UNIFORM in layers
    assert AuthorityLayer.MILLET_AUTONOMOUS in layers
    assert AuthorityLayer.STATE_FLOOR_OVERRIDE in layers
    assert AuthorityLayer.CIVIL_DEFAULT in layers

    # Criminal law and economy must be 100% state uniform
    domain_map = {d.domain_name: d for d in MILLET_JURISDICTION_DOMAINS}
    assert domain_map["Criminal Law & Public Order"].authority_layer == AuthorityLayer.STATE_UNIFORM
    assert domain_map["Economy, Money & Taxation"].authority_layer == AuthorityLayer.STATE_UNIFORM
    assert domain_map["Family & Personal Status"].authority_layer == AuthorityLayer.MILLET_AUTONOMOUS
    assert domain_map["Fundamental Human Rights Floor"].authority_layer == AuthorityLayer.STATE_FLOOR_OVERRIDE
    assert domain_map["Civil Personal Status (The Civil Millet)"].authority_layer == AuthorityLayer.CIVIL_DEFAULT


def test_human_rights_floor():
    floor = HumanRightsFloor()
    assert floor.is_floor_complete is True
    assert floor.minimum_marriage_age >= 18
    assert floor.verifiable_state_consent_required is True
    assert floor.forced_marriage_criminalized is True
    assert floor.domestic_violence_state_criminal_jurisdiction_only is True
    assert floor.child_custody_decisions_appealable_to_state_courts is True
    assert floor.unrestricted_right_of_exit_to_civil_millet is True


def test_anti_lebanon_lock():
    lock = AntiLebanonLock()
    assert lock.is_state_immune_to_confessional_gridlock is True
    assert lock.confessional_parliamentary_quotas_prohibited is True
    assert lock.cabinet_ministry_ethnic_allocation_prohibited is True
    assert lock.civil_service_confessional_reservation_prohibited is True
    assert lock.millet_authority_strictly_confined_to_personal_status is True


def test_gap_audit_register_rigor():
    assert len(STATE_GAP_AUDIT_REGISTER) == 10

    # Ensure all domains are indexed 1-10
    indices = [g.domain_number for g in STATE_GAP_AUDIT_REGISTER]
    assert indices == list(range(1, 11))

    # Genuinely untouched areas must be identified
    untouched = [g for g in STATE_GAP_AUDIT_REGISTER if g.status == GapStatus.GENUINELY_UNTOUCHED]
    untouched_titles = {g.domain_title for g in untouched}

    assert "Constitutional Entrenchment & Supremacy" in untouched_titles
    assert "Macro-Capacity Allocation & Sequencing Synthesis" in untouched_titles

    # Verify that domains resolved by Millet System are marked
    resolved = [g for g in STATE_GAP_AUDIT_REGISTER if g.status == GapStatus.BUILT_AND_FORMALIZED]
    resolved_titles = {g.domain_title for g in resolved}
    assert "Religion, Pluralism & Confessional Order" in resolved_titles
    assert "Family, Personal Status & Domestic Rights" in resolved_titles
