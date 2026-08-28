"""Tests for the Citizen Militia and Asymmetric Defense model."""

from __future__ import annotations

import sys
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from model.rcu.military import (  # noqa: E402
    DRONE_DEFENSE_LAYERS,
    MEDIEVAL_ARSENAL,
    MOBILIZATION_TIMELINE,
    NEUTRALIZATION_MATRIX,
    REQUIRED_KIT_ITEMS,
    TRANSPORT_CLASSES,
    CampaignEconomics,
    CommunityDemographics,
    DroneSwarmEngagement,
    PersonalKit,
    TransportFleet,
)


# --------------------------------------------------------------------------
# 1. Personal Kit Tests
# --------------------------------------------------------------------------


def test_personal_kit_contains_all_core_items():
    kit = PersonalKit()
    assert len(kit.items) == 15
    item_names = [i.name.lower() for i in kit.items]
    assert any("primary weapon" in n for n in item_names)
    assert any("secondary weapon" in n for n in item_names)
    assert any("medical kit" in n for n in item_names)
    assert any("water purification" in n for n in item_names)
    assert any("food" in n for n in item_names)
    assert any("blade maintenance" in n for n in item_names)
    assert any("shelter" in n for n in item_names)


def test_personal_kit_weight_is_man_portable():
    """A fighter must be able to march 30 km with full kit."""
    kit = PersonalKit()
    assert kit.total_weight_kg <= 25.0
    assert kit.total_weight_kg >= 15.0


def test_personal_kit_cost_is_achievable():
    """Individual kit cost is self-fundable without a central military budget."""
    kit = PersonalKit()
    assert 400.0 <= kit.total_cost_usd <= 1000.0


def test_majority_of_kit_is_locally_producible():
    kit = PersonalKit()
    assert kit.local_production_share >= Decimal("0.70")


# --------------------------------------------------------------------------
# 2. Transport Fleet Tests
# --------------------------------------------------------------------------


def test_transport_classes_include_horses_and_pack_animals():
    assert "horse" in TRANSPORT_CLASSES
    assert "truck" in TRANSPORT_CLASSES
    assert "bicycle" in TRANSPORT_CLASSES
    assert "donkey_mule" in TRANSPORT_CLASSES
    assert "foot" in TRANSPORT_CLASSES


def test_transport_fleet_zero_fuel_dominance():
    """Over 99% of transport units operate without petroleum supply chains."""
    fleet = TransportFleet(population=10000)
    assert fleet.zero_fuel_unit_share >= Decimal("0.99")
    assert fleet.fuel_dependent_units <= 30


def test_transport_fleet_total_payload_capacity():
    """Fleet can move significant tonnage across the district."""
    fleet = TransportFleet(population=10000)
    assert fleet.total_payload_capacity_kg >= 150_000.0


def test_pack_animals_and_horses_excel_in_rough_terrain():
    assert TRANSPORT_CLASSES["horse"].rough_terrain_rating >= 4
    assert TRANSPORT_CLASSES["donkey_mule"].mountain_rating == 5
    assert TRANSPORT_CLASSES["truck"].mountain_rating <= 2


# --------------------------------------------------------------------------
# 3. Mobilization & Demographics Tests
# --------------------------------------------------------------------------


def test_mobilization_timeline_reaches_full_readiness_in_24_hours():
    timeline = MOBILIZATION_TIMELINE
    assert len(timeline) == 6
    assert timeline[0].hours_start == 0
    assert timeline[-1].hours_end == 24
    assert timeline[-1].force_readiness_pct == 100.0


def test_community_demographics_mobilization_scale():
    """A community of 10,000 yields ~3,500 to ~4,000 active combatants."""
    demo = CommunityDemographics(population=10000)
    assert 3000 <= demo.mobilized_combatants <= 4000
    assert demo.registered_adults == 5500
    assert demo.exempt_adults == 1650
    assert demo.non_combatant_population == 6150


# --------------------------------------------------------------------------
# 4. Medieval & Low-Tech Arsenal Tests
# --------------------------------------------------------------------------


def test_medieval_arsenal_variety():
    assert len(MEDIEVAL_ARSENAL) >= 10
    names = [w.name.lower() for w in MEDIEVAL_ARSENAL]
    assert any("spear" in n for n in names)
    assert any("bow" in n for n in names)
    assert any("crossbow" in n for n in names)
    assert any("punji" in n for n in names)
    assert any("caltrops" in n for n in names)
    assert any("sling" in n for n in names)


def test_majority_of_medieval_weapons_do_not_require_factory_ammo():
    zero_ammo = [w for w in MEDIEVAL_ARSENAL if not w.ammunition_dependent]
    assert len(zero_ammo) >= 6


def test_silent_weapons_dominate_arsenal():
    silent_weapons = [w for w in MEDIEVAL_ARSENAL if w.silent]
    assert len(silent_weapons) >= 8


# --------------------------------------------------------------------------
# 5. Asymmetric Neutralization & Cost Ratios
# --------------------------------------------------------------------------


def test_all_neutralization_methods_have_extreme_cost_advantage():
    for method in NEUTRALIZATION_MATRIX:
        assert method.cost_ratio >= 10_000


def test_tank_neutralization_cost_ratio():
    tank_method = next(m for m in NEUTRALIZATION_MATRIX if "Tank" in m.target_asset)
    assert tank_method.cost_ratio == 1_000_000
    assert tank_method.militia_neutralization_cost_usd <= 15.0


def test_fighter_jet_neutralization_cost_ratio():
    f22_method = next(m for m in NEUTRALIZATION_MATRIX if "F-22" in m.target_asset)
    assert f22_method.cost_ratio == 750_000
    assert f22_method.militia_neutralization_cost_usd <= 250.0


# --------------------------------------------------------------------------
# 6. Anti-Drone Swarm Defense Model Tests
# --------------------------------------------------------------------------


def test_drone_defense_layers_count():
    assert len(DRONE_DEFENSE_LAYERS) == 5
    ranges = [l.engagement_distance_m for l in DRONE_DEFENSE_LAYERS]
    assert ranges == sorted(ranges, reverse=True)


def test_drone_swarm_simulation_neutralizes_over_99_percent():
    sim = DroneSwarmEngagement(initial_swarm_size=100).simulate()
    assert sim["interception_rate"] >= 0.99
    assert sim["surviving_drones"] < 1.0
    assert sim["total_defense_cost_usd"] <= 1000.0


def test_drone_interception_cost_per_drone():
    sim = DroneSwarmEngagement(initial_swarm_size=100).simulate()
    assert sim["cost_per_interception_usd"] <= 10.0


# --------------------------------------------------------------------------
# 7. Campaign Economics Tests
# --------------------------------------------------------------------------


def test_campaign_burn_rate_asymmetry():
    econ = CampaignEconomics()
    assert econ.daily_cost_ratio >= 2_000


def test_cumulative_expenditure_multi_month():
    econ = CampaignEconomics()
    res_90 = econ.cumulative_expenditure(90)
    assert res_90["enemy_total_usd"] == 25_000_000.0 * 90
    assert res_90["militia_total_usd"] == 10_000.0 * 90
    assert res_90["net_deficit_ratio"] >= 2_000.0
