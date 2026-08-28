"""Commodity class register for the RCU (Real Commodity Unit) system.

This module is the single source of truth for the 20 commodity classes,
their decay parameters, collateral haircuts and storage-cost assumptions.
Documentation tables are generated from this file (see tools/gen_tables.py)
so that the prose and the code can never drift apart.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Tier(str, Enum):
    """Behavioural tier of a commodity class."""

    A = "A"  # perishable / decaying
    B = "B"  # stable / non-decaying


class DecayPeriod(str, Enum):
    """The period over which the decay rate is expressed."""

    MONTH = "month"
    YEAR = "year"


@dataclass(frozen=True)
class CommodityClass:
    """A single note series.

    Attributes
    ----------
    code:
        Two-letter series code printed on the note (e.g. ``GR`` for grains).
    number:
        Class number 1..20, matching the original blueprint ordering.
    name:
        Human readable class name.
    tier:
        ``Tier.A`` (decaying) or ``Tier.B`` (stable).
    colour:
        Printed colour of the note series.
    hex_colour:
        Reference colour for digital renderings and the wallet UI.
    examples:
        Representative backing commodities.
    grace_months:
        Number of whole months after issuance during which the note holds
        full face value. Decay begins *after* this period elapses.
    decay_rate:
        Fractional loss per ``decay_period`` once the grace period ends.
    decay_period:
        Whether ``decay_rate`` is expressed per month or per year.
    max_validity_months:
        Age at which the note stops being transferable. ``None`` means the
        note does not expire.
    storage_cost_pa:
        Estimated all-in physical storage cost as a fraction of stored value
        per year (warehousing, shrinkage, insurance, security, inspection).
        Used to test whether demurrage actually covers the cost of carry.
    haircut:
        Fraction of the assessed market value withheld at issuance. Notes are
        issued against ``(1 - haircut)`` of assessed value so that a fall in
        the commodity price does not immediately leave the series
        undercollateralised.
    price_volatility_pa:
        Rough annualised standard deviation of the local price of the class,
        used to size the haircut and the stabilisation buffer.
    unit:
        Natural physical unit for grading and deposit.
    liquidity:
        Qualitative depth of the local resale market: how quickly a warehouse
        could sell the collateral to honour redemptions.
    """

    code: str
    number: int
    name: str
    tier: Tier
    colour: str
    hex_colour: str
    examples: tuple[str, ...]
    grace_months: int
    decay_rate: float
    decay_period: DecayPeriod
    max_validity_months: int | None
    storage_cost_pa: float
    haircut: float
    price_volatility_pa: float
    unit: str
    liquidity: str
    notes: str = ""

    @property
    def monthly_decay(self) -> float:
        """Decay rate expressed per month."""
        if self.decay_rate == 0.0:
            return 0.0
        if self.decay_period is DecayPeriod.MONTH:
            return self.decay_rate
        # Convert an annual rate to the equivalent compounding monthly rate.
        return 1.0 - (1.0 - self.decay_rate) ** (1.0 / 12.0)

    @property
    def annualised_decay(self) -> float:
        """Decay rate expressed per year, once decay has begun."""
        if self.decay_rate == 0.0:
            return 0.0
        if self.decay_period is DecayPeriod.YEAR:
            return self.decay_rate
        return 1.0 - (1.0 - self.decay_rate) ** 12

    @property
    def decays(self) -> bool:
        return self.decay_rate > 0.0

    @property
    def expires(self) -> bool:
        return self.max_validity_months is not None

    @property
    def carry_covered(self) -> bool:
        """Does post-grace demurrage cover the physical cost of carry?

        A class where demurrage is smaller than storage cost is running at a
        structural loss: somebody (the cooperative, the depositor, or the
        stabilisation fund) is subsidising storage.
        """
        return self.annualised_decay >= self.storage_cost_pa

    @property
    def lifetime_decay(self) -> float:
        """Total fraction of face value lost if held to maximum validity."""
        if not self.decays:
            return 0.0
        if self.max_validity_months is None:
            return 0.0
        decaying_months = max(0, self.max_validity_months - self.grace_months)
        return 1.0 - (1.0 - self.monthly_decay) ** decaying_months


#: The twenty commodity classes. Parameters marked "revised" differ from the
#: first-draft blueprint; the rationale for each change is in the ``notes``
#: field and in docs/annex-i-open-problems.md.
REGISTER: tuple[CommodityClass, ...] = (
    # ------------------------------------------------------------------
    # TIER A -- perishable, decaying
    # ------------------------------------------------------------------
    CommodityClass(
        code="GR",
        number=1,
        name="Grains & Cereals",
        tier=Tier.A,
        colour="Golden Yellow",
        hex_colour="#E8B923",
        examples=("maize", "rice", "wheat", "sorghum", "millet"),
        grace_months=6,
        decay_rate=0.02,
        decay_period=DecayPeriod.MONTH,
        max_validity_months=24,
        storage_cost_pa=0.07,
        haircut=0.30,
        price_volatility_pa=0.35,
        unit="kg",
        liquidity="deep",
        notes=(
            "Grace shortened from 12 to 6 months: hermetic grain storage loses "
            "1-2%/month to shrinkage and pests from month 4, and a 12-month "
            "grace meant most notes never decayed at all, defeating the "
            "anti-hoarding purpose. Storage cost is the highest of any class "
            "(Hart put maize/wheat carry near 6-7%/yr)."
        ),
    ),
    CommodityClass(
        code="FP",
        number=2,
        name="Fresh Produce",
        tier=Tier.A,
        colour="Green",
        hex_colour="#3E9B3E",
        examples=("fruit", "vegetables", "tubers", "bananas"),
        grace_months=1,
        decay_rate=0.05,
        decay_period=DecayPeriod.MONTH,
        max_validity_months=6,
        storage_cost_pa=0.45,
        haircut=0.50,
        price_volatility_pa=0.60,
        unit="kg",
        liquidity="deep but local",
        notes=(
            "Grace shortened from 3 months to 1. Even 5%/month understates "
            "real spoilage: unrefrigerated tomatoes are worthless in weeks. "
            "RECOMMENDATION: do not issue bearer notes against fresh produce "
            "at all in Phase 1; use forward vouchers instead. Retained here "
            "with punitive parameters to show why."
        ),
    ),
    CommodityClass(
        code="LV",
        number=3,
        name="Meat & Livestock",
        tier=Tier.A,
        colour="Dark Red",
        hex_colour="#8C1C1C",
        examples=("cattle", "goats", "sheep", "poultry", "fish"),
        grace_months=6,
        decay_rate=0.03,
        decay_period=DecayPeriod.MONTH,
        max_validity_months=18,
        storage_cost_pa=0.12,
        haircut=0.35,
        price_volatility_pa=0.30,
        unit="head (live) / kg (carcass)",
        liquidity="deep",
        notes=(
            "Live animals APPRECIATE while growing and die stochastically. "
            "Decay is the wrong model: use a mortality-and-feed-adjusted "
            "revaluation instead. Live animals must be a separate custody "
            "regime (branded, ear-tagged, herd audited) from cold-stored meat."
        ),
    ),
    CommodityClass(
        code="DA",
        number=4,
        name="Dairy & Animal Products",
        tier=Tier.A,
        colour="Cream",
        hex_colour="#F2E6C9",
        examples=("milk", "cheese", "eggs", "honey", "leather"),
        grace_months=1,
        decay_rate=0.04,
        decay_period=DecayPeriod.MONTH,
        max_validity_months=12,
        storage_cost_pa=0.30,
        haircut=0.40,
        price_volatility_pa=0.25,
        unit="litre / kg",
        liquidity="moderate",
        notes=(
            "Class is too heterogeneous: honey keeps for millennia, raw milk "
            "for hours. Split into DA-1 (shelf-stable: honey, hard cheese, "
            "cured leather) and DA-2 (cold chain) before national rollout."
        ),
    ),
    CommodityClass(
        code="WT",
        number=5,
        name="Water",
        tier=Tier.A,
        colour="Light Blue",
        hex_colour="#7EC8E3",
        examples=("potable water", "irrigation rights", "reservoir credits"),
        grace_months=12,
        decay_rate=0.01,
        decay_period=DecayPeriod.MONTH,
        max_validity_months=36,
        storage_cost_pa=0.03,
        haircut=0.40,
        price_volatility_pa=0.40,
        unit="m3",
        liquidity="thin",
        notes=(
            "Water is a delivery right, not a stored good, and is politically "
            "explosive: monetising water rights in a drought-prone region "
            "risks the currency being blamed for thirst. Phase 3 at the "
            "earliest, and only with a statutory human-consumption carve-out."
        ),
    ),
    CommodityClass(
        code="WD",
        number=6,
        name="Wood & Timber",
        tier=Tier.A,
        colour="Brown",
        hex_colour="#7B4B2A",
        examples=("lumber", "firewood", "bamboo", "plywood"),
        grace_months=12,
        decay_rate=0.015,
        decay_period=DecayPeriod.MONTH,
        max_validity_months=36,
        storage_cost_pa=0.05,
        haircut=0.25,
        price_volatility_pa=0.20,
        unit="m3",
        liquidity="moderate",
        notes=(
            "Monetising timber creates a direct financial incentive to fell "
            "trees. Requires a hard legality gate: only certified-source or "
            "plantation timber is eligible collateral."
        ),
    ),
    CommodityClass(
        code="TX",
        number=7,
        name="Textiles & Fibers",
        tier=Tier.A,
        colour="Purple",
        hex_colour="#6B3FA0",
        examples=("cotton bales", "wool", "sisal", "jute"),
        grace_months=18,
        decay_rate=0.01,
        decay_period=DecayPeriod.MONTH,
        max_validity_months=48,
        storage_cost_pa=0.04,
        haircut=0.25,
        price_volatility_pa=0.25,
        unit="bale / kg",
        liquidity="moderate (export-linked)",
        notes="Grace trimmed from 24 to 18 months to keep some circulation pressure.",
    ),
    CommodityClass(
        code="PL",
        number=8,
        name="Plastics & Polymers",
        tier=Tier.A,
        colour="Orange",
        hex_colour="#E8791E",
        examples=("recycled pellets", "raw polymers", "PVC"),
        grace_months=18,
        decay_rate=0.01,
        decay_period=DecayPeriod.MONTH,
        max_validity_months=48,
        storage_cost_pa=0.04,
        haircut=0.30,
        price_volatility_pa=0.35,
        unit="kg",
        liquidity="thin",
        notes=(
            "Physically stable -- belongs in Tier B on decay grounds. It is "
            "kept in Tier A only because its price tracks crude oil, which is "
            "a price risk, not a decay risk. Handle price risk with the "
            "haircut, not with demurrage."
        ),
    ),
    CommodityClass(
        code="BF",
        number=9,
        name="Biofuels & Energy",
        tier=Tier.A,
        colour="Dark Green",
        hex_colour="#1E5631",
        examples=("charcoal", "bioethanol", "biogas", "briquettes"),
        grace_months=3,
        decay_rate=0.02,
        decay_period=DecayPeriod.MONTH,
        max_validity_months=18,
        storage_cost_pa=0.08,
        haircut=0.30,
        price_volatility_pa=0.30,
        unit="kg / litre",
        liquidity="deep",
        notes=(
            "Charcoal is the single largest driver of deforestation in the "
            "target region. Same legality gate as timber, or exclude charcoal "
            "and admit only briquettes and biogas."
        ),
    ),
    CommodityClass(
        code="MH",
        number=10,
        name="Medicinal & Herbal",
        tier=Tier.A,
        colour="Teal",
        hex_colour="#1F7A72",
        examples=("medicinal plants", "essential oils", "prepared remedies"),
        grace_months=3,
        decay_rate=0.03,
        decay_period=DecayPeriod.MONTH,
        max_validity_months=12,
        storage_cost_pa=0.10,
        haircut=0.45,
        price_volatility_pa=0.50,
        unit="kg / litre",
        liquidity="thin",
        notes=(
            "Grading is subjective and the resale market is thin, which makes "
            "this the easiest class in which to inflate a deposit valuation. "
            "Cap at 2% of any cooperative's issued stock."
        ),
    ),
    # ------------------------------------------------------------------
    # TIER B -- stable
    # ------------------------------------------------------------------
    CommodityClass(
        code="FE",
        number=11,
        name="Iron & Steel",
        tier=Tier.B,
        colour="Silver Grey",
        hex_colour="#A8A9AD",
        examples=("iron ore", "steel bar", "rebar", "scrap"),
        grace_months=0,
        decay_rate=0.0,
        decay_period=DecayPeriod.YEAR,
        max_validity_months=None,
        storage_cost_pa=0.02,
        haircut=0.20,
        price_volatility_pa=0.25,
        unit="tonne",
        liquidity="deep",
        notes=(
            "Zero decay does not mean zero cost: rust, theft and yard rent "
            "still run ~2%/yr. Tier B must therefore levy an explicit "
            "custody fee, since it has no demurrage to fund storage."
        ),
    ),
    CommodityClass(
        code="CU",
        number=12,
        name="Copper & Aluminium",
        tier=Tier.B,
        colour="Copper Bronze",
        hex_colour="#B87333",
        examples=("copper wire", "aluminium sheet", "cable"),
        grace_months=0,
        decay_rate=0.0,
        decay_period=DecayPeriod.YEAR,
        max_validity_months=None,
        storage_cost_pa=0.03,
        haircut=0.20,
        price_volatility_pa=0.28,
        unit="tonne",
        liquidity="deep",
        notes="Highest theft risk per unit volume of any class; vault-grade custody required.",
    ),
    CommodityClass(
        code="CM",
        number=13,
        name="Construction Materials",
        tier=Tier.B,
        colour="Sand Beige",
        hex_colour="#D8C9A3",
        examples=("sand", "gravel", "cement", "brick", "limestone"),
        grace_months=0,
        decay_rate=0.0,
        decay_period=DecayPeriod.YEAR,
        max_validity_months=None,
        storage_cost_pa=0.02,
        haircut=0.30,
        price_volatility_pa=0.15,
        unit="tonne / m3",
        liquidity="deep but local",
        notes=(
            "Cement is NOT stable: bagged Portland cement is unusable after "
            "about 6 months in humid conditions. Move cement to Tier A or "
            "exclude it. Sand and gravel are stable but have very low value "
            "density -- the storage cost per unit of currency issued is high."
        ),
    ),
    CommodityClass(
        code="PM",
        number=14,
        name="Precious Metals",
        tier=Tier.B,
        colour="Gold",
        hex_colour="#D4AF37",
        examples=("gold", "platinum", "silver", "palladium"),
        grace_months=0,
        decay_rate=0.0,
        decay_period=DecayPeriod.YEAR,
        max_validity_months=None,
        storage_cost_pa=0.01,
        haircut=0.10,
        price_volatility_pa=0.18,
        unit="gram",
        liquidity="deep, globally priced",
        notes=(
            "The anchor class and the sanctions-attention class simultaneously. "
            "Artisanal gold in the Great Lakes region carries conflict-minerals "
            "exposure; require OECD due-diligence documentation or exclude."
        ),
    ),
    CommodityClass(
        code="SM",
        number=15,
        name="Strategic Minerals",
        tier=Tier.B,
        colour="Dark Blue",
        hex_colour="#1B365D",
        examples=("coltan", "cobalt", "lithium", "rare earths", "tin"),
        grace_months=0,
        decay_rate=0.0,
        decay_period=DecayPeriod.YEAR,
        max_validity_months=None,
        storage_cost_pa=0.02,
        haircut=0.35,
        price_volatility_pa=0.45,
        unit="kg",
        liquidity="export-only",
        notes=(
            "No local resale market: redemption requires an export buyer, so "
            "these notes are only as good as an FX channel. High haircut and "
            "a hard cap on share of issuance."
        ),
    ),
    CommodityClass(
        code="CG",
        number=16,
        name="Ceramics & Glass",
        tier=Tier.B,
        colour="Terracotta",
        hex_colour="#C1613C",
        examples=("tiles", "glass panes", "pottery", "ceramic pipe"),
        grace_months=0,
        decay_rate=0.0,
        decay_period=DecayPeriod.YEAR,
        max_validity_months=None,
        storage_cost_pa=0.04,
        haircut=0.35,
        price_volatility_pa=0.15,
        unit="unit / m2",
        liquidity="thin",
        notes="Chemically stable but physically fragile: breakage is the real shrinkage term.",
    ),
    CommodityClass(
        code="SC",
        number=17,
        name="Salt & Chemicals",
        tier=Tier.B,
        colour="White",
        hex_colour="#F5F5F0",
        examples=("salt", "soda ash", "fertiliser", "lime"),
        grace_months=12,
        decay_rate=0.005,
        decay_period=DecayPeriod.YEAR,
        max_validity_months=120,
        storage_cost_pa=0.05,
        haircut=0.30,
        price_volatility_pa=0.25,
        unit="tonne",
        liquidity="deep (fertiliser), moderate (other)",
        notes=(
            "Fertiliser genuinely degrades (caking, nitrogen loss) far faster "
            "than 0.5%/yr in humid storage; it should be Tier A. Salt and lime "
            "are effectively permanent. Split the class."
        ),
    ),
    CommodityClass(
        code="ST",
        number=18,
        name="Stone & Marble",
        tier=Tier.B,
        colour="Slate Grey",
        hex_colour="#5A6169",
        examples=("granite", "marble", "basalt", "dimension stone"),
        grace_months=0,
        decay_rate=0.0,
        decay_period=DecayPeriod.YEAR,
        max_validity_months=None,
        storage_cost_pa=0.01,
        haircut=0.40,
        price_volatility_pa=0.15,
        unit="tonne / m3",
        liquidity="very thin",
        notes=(
            "Nearly indestructible and nearly unsellable at short notice. "
            "Ideal physical collateral, poor monetary collateral: redemption "
            "could take months. High haircut, low issuance cap."
        ),
    ),
    CommodityClass(
        code="RB",
        number=19,
        name="Processed Rubber",
        tier=Tier.B,
        colour="Black",
        hex_colour="#1C1C1C",
        examples=("vulcanised rubber", "tyres", "latex goods"),
        grace_months=12,
        decay_rate=0.005,
        decay_period=DecayPeriod.YEAR,
        max_validity_months=120,
        storage_cost_pa=0.03,
        haircut=0.30,
        price_volatility_pa=0.25,
        unit="tonne",
        liquidity="moderate",
        notes="Ozone and UV cracking are real; covered storage is mandatory, not optional.",
    ),
    CommodityClass(
        code="EN",
        number=20,
        name="Energy Credits",
        tier=Tier.B,
        colour="Electric Yellow",
        hex_colour="#F2E63D",
        examples=("solar kWh", "hydro kWh", "geothermal credits"),
        grace_months=0,
        decay_rate=0.0,
        decay_period=DecayPeriod.YEAR,
        max_validity_months=60,
        storage_cost_pa=0.0,
        haircut=0.25,
        price_volatility_pa=0.20,
        unit="kWh",
        liquidity="deep where grid exists",
        notes=(
            "The only class with no physical stock at all. It is a forward "
            "claim on future generation, backed by a producer's promise, not "
            "by an inspectable pile. It therefore carries counterparty risk "
            "that no warehouse inspection can eliminate -- treat it as a "
            "utility prepayment instrument, and cap it hard."
        ),
    ),
)

BY_CODE: dict[str, CommodityClass] = {c.code: c for c in REGISTER}
BY_NUMBER: dict[int, CommodityClass] = {c.number: c for c in REGISTER}

TIER_A: tuple[CommodityClass, ...] = tuple(c for c in REGISTER if c.tier is Tier.A)
TIER_B: tuple[CommodityClass, ...] = tuple(c for c in REGISTER if c.tier is Tier.B)


def get(code_or_number: str | int) -> CommodityClass:
    """Look up a commodity class by series code or class number."""
    if isinstance(code_or_number, int):
        return BY_NUMBER[code_or_number]
    return BY_CODE[code_or_number.upper()]
