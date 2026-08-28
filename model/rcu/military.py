"""Citizen Militia and Asymmetric Defense: logistics, low-cost neutralization,
and attrition economics.

This module models the military doctrine for an independent community or
nation: a mandatory, self-funded, self-equipped citizen defense force
operating on asymmetric principles.

Key models:
1. ``kit`` -- individual personal equipment requirements, costs, and weights.
2. ``transport`` -- diversified transport fleet (horses, trucks, bicycles,
   donkeys, foot) balancing speed, payload, fuel independence, and rough terrain.
3. ``mobilization`` -- demographic mobilization rates and the 24-hour readiness
   timeline.
4. ``arsenal`` -- low-tech and medieval weapons requiring zero industrial
   supply chains and zero imported ammunition.
5. ``neutralization`` -- economic and physical metrics of neutralizing high-tech
   weapons (tanks, next-gen fighters, drone swarms) at extreme cost asymmetry.
6. ``drone_defense`` -- five-layer anti-drone swarm interception model.
7. ``attrition`` -- campaign economics comparing conventional expeditionary
   burn rates against distributed militia sustainability.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import ROUND_HALF_UP, Decimal
from enum import Enum


def _q(x: Decimal, places: str = "0.01") -> Decimal:
    return x.quantize(Decimal(places), rounding=ROUND_HALF_UP)


# --------------------------------------------------------------------------
# 1. Personal Kit: Self-Funded & Self-Equipped
# --------------------------------------------------------------------------


class CostTier(str, Enum):
    VERY_LOW = "very_low"    # < $10
    LOW = "low"              # $10 - $50
    MODERATE = "moderate"    # $50 - $200
    VARIABLE = "variable"    # Primary weapon dependent


@dataclass(frozen=True)
class KitItem:
    name: str
    specification: str
    cost_tier: CostTier
    estimated_cost_usd: float
    weight_kg: float
    purpose: str
    locally_producible: bool = True


REQUIRED_KIT_ITEMS: tuple[KitItem, ...] = (
    KitItem(
        name="Primary weapon",
        specification="Rifle (bolt-action / semi-auto), shotgun, or crossbow",
        cost_tier=CostTier.VARIABLE,
        estimated_cost_usd=250.0,
        weight_kg=3.5,
        purpose="Primary engagement tool; must be maintained in working condition",
        locally_producible=False,
    ),
    KitItem(
        name="Secondary weapon",
        specification="Machete, sword, spear, or combat axe",
        cost_tier=CostTier.LOW,
        estimated_cost_usd=25.0,
        weight_kg=1.2,
        purpose="Close combat and utility; zero ammo requirement; never runs out",
        locally_producible=True,
    ),
    KitItem(
        name="Ammunition reserve",
        specification="Minimum 200 rounds for primary firearm (rotated annually)",
        cost_tier=CostTier.MODERATE,
        estimated_cost_usd=100.0,
        weight_kg=3.0,
        purpose="Combat reserve stored safely at home",
        locally_producible=False,
    ),
    KitItem(
        name="Blade maintenance kit",
        specification="Sharpening whetstone, oil, leather strop",
        cost_tier=CostTier.VERY_LOW,
        estimated_cost_usd=8.0,
        weight_kg=0.4,
        purpose="Maintaining blade readiness and utility",
        locally_producible=True,
    ),
    KitItem(
        name="Personal medical kit",
        specification="Tourniquet, pressure bandages, antiseptic, painkillers, ORS, antibiotics",
        cost_tier=CostTier.LOW,
        estimated_cost_usd=30.0,
        weight_kg=0.8,
        purpose="Immediate self-treatment and buddy aid at point of injury",
        locally_producible=True,
    ),
    KitItem(
        name="Water purification",
        specification="Filter pump, chemical purification tablets, or boiling canteen",
        cost_tier=CostTier.LOW,
        estimated_cost_usd=20.0,
        weight_kg=0.5,
        purpose="Preventing waterborne casualties in field operations",
        locally_producible=True,
    ),
    KitItem(
        name="Food ration supply",
        specification="7 days of dried grain, biltong/pemmican, or high-energy rations",
        cost_tier=CostTier.LOW,
        estimated_cost_usd=25.0,
        weight_kg=4.5,
        purpose="Independent operation for one week without supply lines",
        locally_producible=True,
    ),
    KitItem(
        name="Shelter & bivvy",
        specification="Waterproof tarp, bivvy bag, or ultralight tent",
        cost_tier=CostTier.LOW,
        estimated_cost_usd=35.0,
        weight_kg=1.5,
        purpose="Weather protection during dispersed field dispersal",
        locally_producible=True,
    ),
    KitItem(
        name="Navigation tools",
        specification="Magnetic compass, waterproof local topographic grid maps",
        cost_tier=CostTier.VERY_LOW,
        estimated_cost_usd=10.0,
        weight_kg=0.3,
        purpose="Navigation when GPS/cellular signals are jammed or destroyed",
        locally_producible=True,
    ),
    KitItem(
        name="Signaling & communications",
        specification="Hand-crank emergency radio receiver and signaling whistle",
        cost_tier=CostTier.LOW,
        estimated_cost_usd=20.0,
        weight_kg=0.6,
        purpose="Receiving decentralized commands and emergency acoustic signaling",
        locally_producible=False,
    ),
    KitItem(
        name="Tactical field clothing",
        specification="Durable, weather-appropriate neutral/camouflage garments",
        cost_tier=CostTier.MODERATE,
        estimated_cost_usd=60.0,
        weight_kg=2.0,
        purpose="Thermal management, durability, and visual concealment",
        locally_producible=True,
    ),
    KitItem(
        name="Field footwear",
        specification="Sturdy, broken-in combat/hiking boots with spare laces",
        cost_tier=CostTier.MODERATE,
        estimated_cost_usd=75.0,
        weight_kg=1.8,
        purpose="Preventing foot injuries during 30 km/day marches",
        locally_producible=True,
    ),
    KitItem(
        name="Fire-starting kit",
        specification="Ferrocerium flint rod, waterproof matches, windproof lighter",
        cost_tier=CostTier.VERY_LOW,
        estimated_cost_usd=7.0,
        weight_kg=0.2,
        purpose="Survival essential for heat, cooking, and signaling",
        locally_producible=True,
    ),
    KitItem(
        name="Cordage & rope",
        specification="20 meters of 550 paracord or braided natural fibre rope",
        cost_tier=CostTier.VERY_LOW,
        estimated_cost_usd=8.0,
        weight_kg=0.3,
        purpose="Shelter construction, traps, climbing, securing cargo",
        locally_producible=True,
    ),
    KitItem(
        name="Multi-tool / fixed blade",
        specification="Heavy-duty fixed blade knife or stainless multi-tool",
        cost_tier=CostTier.LOW,
        estimated_cost_usd=25.0,
        weight_kg=0.4,
        purpose="Versatile field craft, trap making, maintenance, breaching",
        locally_producible=True,
    ),
)


@dataclass(frozen=True)
class PersonalKit:
    items: tuple[KitItem, ...] = REQUIRED_KIT_ITEMS

    @property
    def total_cost_usd(self) -> float:
        return sum(item.estimated_cost_usd for item in self.items)

    @property
    def total_weight_kg(self) -> float:
        return sum(item.weight_kg for item in self.items)

    @property
    def locally_producible_count(self) -> int:
        return sum(1 for item in self.items if item.locally_producible)

    @property
    def local_production_share(self) -> Decimal:
        if not self.items:
            return Decimal(0)
        return _q(Decimal(self.locally_producible_count) / Decimal(len(self.items)), "0.001")


# --------------------------------------------------------------------------
# 2. Transport Fleet: Resilience & Fuel Independence
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class TransportClass:
    name: str
    unit_payload_kg: float
    cruising_speed_kmh: float
    requires_fuel: bool
    rough_terrain_rating: int     # 1 (poor) to 5 (excellent)
    mountain_rating: int          # 1 (poor) to 5 (excellent)
    silent_operation: bool
    recommended_per_10k: int
    min_per_10k: int
    max_per_10k: int


TRANSPORT_CLASSES: dict[str, TransportClass] = {
    "horse": TransportClass(
        name="Horse (Mounted Cavalry / Scout)",
        unit_payload_kg=125.0,
        cruising_speed_kmh=20.0,
        requires_fuel=False,
        rough_terrain_rating=5,
        mountain_rating=4,
        silent_operation=True,
        recommended_per_10k=250,
        min_per_10k=200,
        max_per_10k=300,
    ),
    "truck": TransportClass(
        name="Truck (Motor Transport / Logistics)",
        unit_payload_kg=2500.0,
        cruising_speed_kmh=65.0,
        requires_fuel=True,
        rough_terrain_rating=2,
        mountain_rating=1,
        silent_operation=False,
        recommended_per_10k=25,
        min_per_10k=20,
        max_per_10k=30,
    ),
    "bicycle": TransportClass(
        name="Bicycle (Courier / Local Logistics)",
        unit_payload_kg=40.0,
        cruising_speed_kmh=18.0,
        requires_fuel=False,
        rough_terrain_rating=3,
        mountain_rating=2,
        silent_operation=True,
        recommended_per_10k=150,
        min_per_10k=100,
        max_per_10k=200,
    ),
    "donkey_mule": TransportClass(
        name="Donkey / Mule (Pack Animal)",
        unit_payload_kg=90.0,
        cruising_speed_kmh=6.0,
        requires_fuel=False,
        rough_terrain_rating=5,
        mountain_rating=5,
        silent_operation=True,
        recommended_per_10k=75,
        min_per_10k=50,
        max_per_10k=100,
    ),
    "foot": TransportClass(
        name="Foot March (Infantry Backbone)",
        unit_payload_kg=35.0,
        cruising_speed_kmh=5.0,
        requires_fuel=False,
        rough_terrain_rating=5,
        mountain_rating=5,
        silent_operation=True,
        recommended_per_10k=3500,
        min_per_10k=3000,
        max_per_10k=4000,
    ),
}


@dataclass(frozen=True)
class TransportFleet:
    population: int = 10000
    counts: dict[str, int] = field(default_factory=lambda: {
        "horse": 250,
        "truck": 25,
        "bicycle": 150,
        "donkey_mule": 75,
        "foot": 3500,
    })

    @property
    def total_transport_units(self) -> int:
        return sum(self.counts.values())

    @property
    def total_payload_capacity_kg(self) -> float:
        return sum(
            self.counts[key] * TRANSPORT_CLASSES[key].unit_payload_kg
            for key in self.counts
        )

    @property
    def fuel_dependent_units(self) -> int:
        return sum(
            self.counts[key]
            for key in self.counts
            if TRANSPORT_CLASSES[key].requires_fuel
        )

    @property
    def zero_fuel_unit_share(self) -> Decimal:
        if self.total_transport_units == 0:
            return Decimal(1)
        zero_fuel = self.total_transport_units - self.fuel_dependent_units
        return _q(Decimal(zero_fuel) / Decimal(self.total_transport_units), "0.001")

    @property
    def zero_fuel_payload_capacity_kg(self) -> float:
        return sum(
            self.counts[key] * TRANSPORT_CLASSES[key].unit_payload_kg
            for key in self.counts
            if not TRANSPORT_CLASSES[key].requires_fuel
        )

    @property
    def zero_fuel_payload_share(self) -> Decimal:
        if self.total_payload_capacity_kg == 0:
            return Decimal(1)
        return _q(
            Decimal(self.zero_fuel_payload_capacity_kg)
            / Decimal(self.total_payload_capacity_kg),
            "0.001",
        )


# --------------------------------------------------------------------------
# 3. Mobilization Timeline & Demographics
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class MobilizationPhase:
    hours_start: int
    hours_end: int
    name: str
    actions: str
    force_readiness_pct: float


MOBILIZATION_TIMELINE: tuple[MobilizationPhase, ...] = (
    MobilizationPhase(
        hours_start=0,
        hours_end=1,
        name="Alert Broadcast",
        actions="Alert signal transmitted via radio network, messenger riders (horse), and signal fires",
        force_readiness_pct=0.0,
    ),
    MobilizationPhase(
        hours_start=1,
        hours_end=4,
        name="Kit Retrieval & Movement",
        actions="Registered fighters retrieve personal kits, mount/load transport, begin moving to assembly points",
        force_readiness_pct=25.0,
    ),
    MobilizationPhase(
        hours_start=4,
        hours_end=8,
        name="Assembly & Roll Call",
        actions="Assembly at designated locations; roll call against register; identify missing personnel",
        force_readiness_pct=60.0,
    ),
    MobilizationPhase(
        hours_start=8,
        hours_end=12,
        name="Tactical Sector Deployment",
        actions="Units receive defensive assignments: road blocks, fortified positions, ambush zones",
        force_readiness_pct=80.0,
    ),
    MobilizationPhase(
        hours_start=12,
        hours_end=18,
        name="Defensive Preparation",
        actions="Positions prepared: IEDs planted, spider holes dug, supply caches distributed, comms active",
        force_readiness_pct=95.0,
    ),
    MobilizationPhase(
        hours_start=18,
        hours_end=24,
        name="Full Combat Readiness",
        actions="Community fully mobilized in defensive posture; 3,000–4,000 fighters in position across territory",
        force_readiness_pct=100.0,
    ),
)


@dataclass(frozen=True)
class CommunityDemographics:
    population: int = 10000
    adult_eligible_fraction: float = 0.55   # Ages 18-50 (~55% of population)
    exemption_rate: float = 0.30            # Medical, childcare, pregnancy (~30% of adults)

    @property
    def registered_adults(self) -> int:
        return int(self.population * self.adult_eligible_fraction)

    @property
    def exempt_adults(self) -> int:
        return int(self.registered_adults * self.exemption_rate)

    @property
    def mobilized_combatants(self) -> int:
        return self.registered_adults - self.exempt_adults

    @property
    def non_combatant_population(self) -> int:
        return self.population - self.mobilized_combatants


# --------------------------------------------------------------------------
# 4. Low-Tech & Medieval Arsenal
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class MedievalWeapon:
    name: str
    effective_range_min_m: float
    effective_range_max_m: float
    lethality: str
    manufacture_difficulty: str
    ammunition_dependent: bool
    silent: bool
    best_use: str


MEDIEVAL_ARSENAL: tuple[MedievalWeapon, ...] = (
    MedievalWeapon(
        name="Spear / Assegai",
        effective_range_min_m=2.0,
        effective_range_max_m=15.0,
        lethality="High",
        manufacture_difficulty="Very Easy",
        ammunition_dependent=False,
        silent=True,
        best_use="Defensive formations, close ambush, anti-cavalry, thrusting",
    ),
    MedievalWeapon(
        name="Bow (Longbow / Recurve)",
        effective_range_min_m=30.0,
        effective_range_max_m=250.0,
        lethality="High",
        manufacture_difficulty="Moderate",
        ammunition_dependent=True,   # Uses locally craftable arrows
        silent=True,
        best_use="Silent harassment, perimeter sniping, elevated ambush",
    ),
    MedievalWeapon(
        name="Crossbow",
        effective_range_min_m=10.0,
        effective_range_max_m=150.0,
        lethality="Very High",
        manufacture_difficulty="Moderate",
        ammunition_dependent=True,   # Uses bolts
        silent=True,
        best_use="Ambush, fortified defensive positions, urban warfare",
    ),
    MedievalWeapon(
        name="Sword / Machete",
        effective_range_min_m=0.5,
        effective_range_max_m=1.2,
        lethality="High",
        manufacture_difficulty="Moderate",
        ammunition_dependent=False,
        silent=True,
        best_use="Close-quarters combat, utility, brush clearing",
    ),
    MedievalWeapon(
        name="Combat Axe",
        effective_range_min_m=0.5,
        effective_range_max_m=2.0,
        lethality="High",
        manufacture_difficulty="Easy",
        ammunition_dependent=False,
        silent=True,
        best_use="Close combat, breaching barricades/doors, obstacle clearing",
    ),
    MedievalWeapon(
        name="Shield (Hide / Wood / Metal)",
        effective_range_min_m=0.0,
        effective_range_max_m=1.0,
        lethality="Defensive",
        manufacture_difficulty="Easy",
        ammunition_dependent=False,
        silent=True,
        best_use="Close combat protection, arrow/fragment deflection",
    ),
    MedievalWeapon(
        name="Punji Stakes / Spike Traps",
        effective_range_min_m=0.0,
        effective_range_max_m=0.0,
        lethality="Moderate–High",
        manufacture_difficulty="Very Easy",
        ammunition_dependent=False,
        silent=True,
        best_use="Passive area denial, perimeter defense, psychological trauma",
    ),
    MedievalWeapon(
        name="Caltrops",
        effective_range_min_m=0.0,
        effective_range_max_m=0.0,
        lethality="Low–Moderate",
        manufacture_difficulty="Easy",
        ammunition_dependent=False,
        silent=True,
        best_use="Anti-vehicle tire puncture, denying foot paths, slowing cavalry",
    ),
    MedievalWeapon(
        name="Sling",
        effective_range_min_m=20.0,
        effective_range_max_m=100.0,
        lethality="Moderate",
        manufacture_difficulty="Very Easy",
        ammunition_dependent=False,  # Rocks are ubiquitous
        silent=True,
        best_use="Long-range silent harassment; unlimited free ammunition",
    ),
    MedievalWeapon(
        name="Atlatl (Spear-Thrower)",
        effective_range_min_m=15.0,
        effective_range_max_m=50.0,
        lethality="High",
        manufacture_difficulty="Easy",
        ammunition_dependent=True,   # Darts/javelins
        silent=True,
        best_use="Extended spear range with high kinetic penetration",
    ),
    MedievalWeapon(
        name="Boiling Oil / Water",
        effective_range_min_m=1.0,
        effective_range_max_m=10.0,
        lethality="Very High",
        manufacture_difficulty="Easy",
        ammunition_dependent=False,
        silent=False,
        best_use="Defending fortified walls, choke points, and urban roofs",
    ),
    MedievalWeapon(
        name="Incendiaries / Greek Fire",
        effective_range_min_m=5.0,
        effective_range_max_m=30.0,
        lethality="Very High",
        manufacture_difficulty="Moderate",
        ammunition_dependent=True,
        silent=False,
        best_use="Anti-vehicle engine decks, area denial, psychological panic",
    ),
)


# --------------------------------------------------------------------------
# 5. Asymmetric Neutralization & Cost Ratios
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class NeutralizationMethod:
    target_asset: str
    enemy_cost_usd: float
    militia_neutralization_cost_usd: float
    method: str
    mechanism: str
    result: str

    @property
    def cost_ratio(self) -> int:
        if self.militia_neutralization_cost_usd <= 0:
            return 0
        return int(self.enemy_cost_usd / self.militia_neutralization_cost_usd)


NEUTRALIZATION_MATRIX: tuple[NeutralizationMethod, ...] = (
    NeutralizationMethod(
        target_asset="F-22 Raptor Fighter Jet",
        enemy_cost_usd=150_000_000.0,
        militia_neutralization_cost_usd=200.0,
        method="Runway & Fuel Depot Sabotage",
        mechanism="IED cratering of 2,500m paved runways and sabotage of JP-8 fuel tanks",
        result="Fighter grounded; unable to take off or land within combat radius",
    ),
    NeutralizationMethod(
        target_asset="M1 Abrams Main Battle Tank",
        enemy_cost_usd=10_000_000.0,
        militia_neutralization_cost_usd=10.0,
        method="Sensor Blinding & Track Jamming",
        mechanism="Weighted nets over optical sensors + mud/paint on periscopes + rebar in track drive sprocket",
        result="Tank blinded and immobilized; crew abandoned or captured intact",
    ),
    NeutralizationMethod(
        target_asset="Drone Swarm (100 units)",
        enemy_cost_usd=20_000_000.0,  # $5M - $50M range
        militia_neutralization_cost_usd=500.0,
        method="Layered Net / Wire / Shotgun Defense",
        mechanism="Monofilament wire barriers + dense smoke + net guns + 12ga birdshot + RF jamming",
        result="Swarm rotors tangled and electronics fried; complete swarm neutralized",
    ),
    NeutralizationMethod(
        target_asset="Armored Personnel Carrier (APC)",
        enemy_cost_usd=3_000_000.0,
        militia_neutralization_cost_usd=5.0,
        method="Anti-Belly Trench & Molotov",
        mechanism="Concealed 2m wide ditch (hull high-centered) + gasoline bottle on engine deck",
        result="Vehicle immobilized and engine destroyed; infantry trapped inside",
    ),
    NeutralizationMethod(
        target_asset="Fuel Supply Convoy (10 trucks)",
        enemy_cost_usd=500_000.0,
        militia_neutralization_cost_usd=50.0,
        method="Roadside IED & Choke Point Ambush",
        mechanism="Dispersed IEDs on unpaved supply routes + felling trees across withdrawal path",
        result="Fuel supply cut off; forward combat units starved of diesel within 48 hours",
    ),
)


# --------------------------------------------------------------------------
# 6. Multi-Layered Anti-Drone Defense Model
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class DroneDefenseLayer:
    layer_number: int
    engagement_distance_m: float
    name: str
    mechanism: str
    attrition_fraction: float     # Fraction of incoming drones intercepted
    cost_per_engagement_usd: float


DRONE_DEFENSE_LAYERS: tuple[DroneDefenseLayer, ...] = (
    DroneDefenseLayer(
        layer_number=1,
        engagement_distance_m=500.0,
        name="Wire & Line Barriers",
        mechanism="Monofilament fishing line and thin wire strung across approach corridors at 10–50m height",
        attrition_fraction=0.35,
        cost_per_engagement_usd=50.0,
    ),
    DroneDefenseLayer(
        layer_number=2,
        engagement_distance_m=200.0,
        name="Smoke & Dust Screens",
        mechanism="Burning tires, waste oil, and damp brush obscuring optical/thermal cameras",
        attrition_fraction=0.40,
        cost_per_engagement_usd=50.0,
    ),
    DroneDefenseLayer(
        layer_number=3,
        engagement_distance_m=100.0,
        name="Weighted Nets & Net Launchers",
        mechanism="Weighted throw nets and compressed-air net guns entangling rotor blades",
        attrition_fraction=0.50,
        cost_per_engagement_usd=100.0,
    ),
    DroneDefenseLayer(
        layer_number=4,
        engagement_distance_m=50.0,
        name="Shotgun Birdshot Teams",
        mechanism="12-gauge shotguns firing dense birdshot spread to shred lightweight plastic/carbon rotors",
        attrition_fraction=0.85,
        cost_per_engagement_usd=150.0,
    ),
    DroneDefenseLayer(
        layer_number=5,
        engagement_distance_m=15.0,
        name="EMP Bursts & RF/GPS Jamming",
        mechanism="Improvised electromagnetic burst devices and 2.4/5.8GHz / GPS L1 noise transmitters",
        attrition_fraction=0.95,
        cost_per_engagement_usd=150.0,
    ),
)


@dataclass(frozen=True)
class DroneSwarmEngagement:
    initial_swarm_size: int = 100
    layers: tuple[DroneDefenseLayer, ...] = DRONE_DEFENSE_LAYERS

    def simulate(self) -> dict[str, float]:
        current_drones = float(self.initial_swarm_size)
        layer_breakdown = []
        for l in self.layers:
            intercepted = current_drones * l.attrition_fraction
            current_drones -= intercepted
            layer_breakdown.append({
                "layer": l.layer_number,
                "name": l.name,
                "intercepted": intercepted,
                "remaining": current_drones,
            })

        total_intercepted = float(self.initial_swarm_size) - current_drones
        total_defense_cost = sum(l.cost_per_engagement_usd for l in self.layers)
        interception_rate = total_intercepted / float(self.initial_swarm_size)

        return {
            "initial_swarm": float(self.initial_swarm_size),
            "surviving_drones": round(current_drones, 2),
            "total_intercepted": round(total_intercepted, 2),
            "interception_rate": round(interception_rate, 4),
            "total_defense_cost_usd": total_defense_cost,
            "cost_per_interception_usd": round(total_defense_cost / max(total_intercepted, 1.0), 2),
        }


# --------------------------------------------------------------------------
# 7. Campaign Attrition Economics
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class CampaignEconomics:
    enemy_daily_cost_usd: float = 25_000_000.0   # Operational burn rate of armored expeditionary brigade + air wings
    militia_daily_cost_usd: float = 10_000.0     # Self-supplied rations and community distributed supplies

    @property
    def daily_cost_ratio(self) -> int:
        if self.militia_daily_cost_usd <= 0:
            return 0
        return int(self.enemy_daily_cost_usd / self.militia_daily_cost_usd)

    def cumulative_expenditure(self, days: int) -> dict[str, float]:
        enemy_total = self.enemy_daily_cost_usd * days
        militia_total = self.militia_daily_cost_usd * days
        return {
            "days": float(days),
            "enemy_total_usd": enemy_total,
            "militia_total_usd": militia_total,
            "net_deficit_ratio": enemy_total / max(militia_total, 1.0),
        }
