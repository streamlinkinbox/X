"""Weight-denominated units, quality adjustment and provenance.

This module implements a change of foundation. In the earlier design a note
was a claim on a *value* ("100 units, backed by maize"), which required
somebody to decide what maize was worth. Here a note is a claim on a
*physical quantity* ("1 kg of standard-grade maize"), and nobody decides
anything: the scale decides.

Three consequences follow, and they are the reason for the change.

1. **No price committee.** Issuance is a weighing operation. The system's
   hardest open problem -- price discovery in thin markets, where the only
   available prices come from the buyers whose market power the system
   exists to counteract -- simply stops being a monetary question. It
   becomes a market question, settled between buyer and seller.

2. **No price-risk haircut.** A note promising 1 kg of iron is not broken by
   a fall in the iron price; it still claims 1 kg of iron. The haircut
   collapses to what physics requires -- measurement error and shrinkage --
   and stops carrying price volatility it was never well suited to carry.

3. **Provenance dating.** If the unit is physical, the clock should run from
   the physical event. Decay starts at harvest, not at deposit.

The cost is real and is quantified in ``exchange_rate_count`` below: without
a value unit there is no single price, and an economy of N goods has
N(N-1)/2 bilateral exchange rates rather than N prices.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from decimal import ROUND_DOWN, ROUND_HALF_UP, Decimal

from .classes import REGISTER, CommodityClass, Tier, get
from .valuation import months_elapsed

#: Grams per base unit. All weight arithmetic is in integer grams to keep
#: settlement deterministic, exactly as monetary amounts are in integer cents.
GRAMS = 1000


class UnitBasis:
    """How a class's unit is physically defined."""

    WEIGHT = "weight"          # kg of standard grade
    VOLUME = "volume"          # m3, for goods where weight misleads
    COUNT = "count"            # head, for livestock
    ENERGY = "energy"          # kWh
    NOT_MONETISABLE = "none"   # cannot be reduced to a stable physical unit


#: Physical unit definition per class. The ``reference`` string is what gets
#: printed on the note: the note is a claim on exactly this.
UNIT_DEFINITION: dict[str, tuple[str, str]] = {
    # code: (basis, printed reference unit)
    "GR": (UnitBasis.WEIGHT, "1 kg maize, Grade A, 13.5% moisture"),
    "FP": (UnitBasis.NOT_MONETISABLE, "—"),
    "LV": (UnitBasis.COUNT, "1 head, standard weight band"),
    "DA": (UnitBasis.WEIGHT, "1 kg shelf-stable equivalent"),
    "WT": (UnitBasis.VOLUME, "1 m3 delivered"),
    "WD": (UnitBasis.WEIGHT, "1 kg air-dry, 15% moisture, species band"),
    "TX": (UnitBasis.WEIGHT, "1 kg lint, standard staple"),
    "PL": (UnitBasis.WEIGHT, "1 kg pellet, single polymer"),
    "BF": (UnitBasis.ENERGY, "1 kg briquette, stated calorific value"),
    "MH": (UnitBasis.WEIGHT, "1 kg dried"),
    "FE": (UnitBasis.WEIGHT, "1 kg iron/steel"),
    "CU": (UnitBasis.WEIGHT, "1 kg copper or aluminium, stated"),
    "CM": (UnitBasis.WEIGHT, "1 kg aggregate"),
    "PM": (UnitBasis.WEIGHT, "1 g fine metal, stated fineness"),
    "SM": (UnitBasis.WEIGHT, "1 kg, stated assay"),
    "CG": (UnitBasis.COUNT, "1 standard piece"),
    "SC": (UnitBasis.WEIGHT, "1 kg"),
    "ST": (UnitBasis.WEIGHT, "1 kg dressed stone"),
    "RB": (UnitBasis.WEIGHT, "1 kg dry rubber content"),
    "EN": (UnitBasis.ENERGY, "1 kWh delivered"),
}

#: Grade factors convert an actual deposit into standard-grade equivalent
#: weight. This is what preserves fungibility within a class: a note is
#: always a claim on standard grade, whatever was actually deposited.
GRADE_FACTOR: dict[str, Decimal] = {
    "A": Decimal("1.00"),
    "B": Decimal("0.85"),
    "C": Decimal("0.65"),
    "REJECT": Decimal("0"),
}

#: Physical-only haircuts. Under weight denomination the haircut no longer
#: carries price risk -- only weighing error, moisture variation, and
#: shrinkage between inspections. Compare these with the 10-50% price-risk
#: haircuts required under value denomination.
PHYSICAL_HAIRCUT: dict[str, Decimal] = {
    "GR": Decimal("0.08"),   # moisture swing + pest loss between inspections
    "LV": Decimal("0.12"),   # mortality between herd audits
    "DA": Decimal("0.10"),
    "WT": Decimal("0.10"),   # evaporation, seepage
    "WD": Decimal("0.10"),   # moisture; the worst weight-basis class
    "TX": Decimal("0.06"),
    "PL": Decimal("0.04"),
    "BF": Decimal("0.08"),
    "MH": Decimal("0.10"),
    "FE": Decimal("0.04"),   # rust, handling loss
    "CU": Decimal("0.04"),
    "CM": Decimal("0.05"),
    "PM": Decimal("0.01"),   # assay is precise; loss is negligible
    "SM": Decimal("0.06"),
    "CG": Decimal("0.08"),   # breakage
    "SC": Decimal("0.08"),   # caking, moisture
    "ST": Decimal("0.03"),
    "RB": Decimal("0.05"),
    "EN": Decimal("0.05"),
}


@dataclass(frozen=True)
class Provenance:
    """The certificate travelling with a deposit.

    The originating physical event -- harvest, slaughter, extraction,
    felling -- is what the decay clock runs from. Without this a producer
    could store grain privately for a year, deposit it, and receive a note
    with a full grace period, passing the accumulated spoilage risk to
    whoever accepts the note.
    """

    origin_date: date          # harvest / extraction / production
    deposit_date: date
    producer_id: str
    origin_place: str
    grade: str = "A"
    moisture_pct: Decimal | None = None
    species_or_assay: str = ""
    inspector_ids: tuple[str, ...] = ()
    prior_storage: str = ""    # where it sat before deposit, if anywhere

    def pre_deposit_age_months(self) -> int:
        """Months between the physical event and the deposit."""
        return months_elapsed(self.origin_date, self.deposit_date)

    def is_stale_on_deposit(self, cls: CommodityClass) -> bool:
        """Was the commodity already past its grace period when deposited?"""
        if not cls.decays:
            return False
        return self.pre_deposit_age_months() >= cls.grace_months


def effective_age_months(prov: Provenance, asof: date) -> int:
    """Age used for decay: measured from the physical origin, not issuance."""
    return months_elapsed(prov.origin_date, asof)


def quality_adjusted_grams(
    gross_grams: int,
    grade: str,
    moisture_pct: Decimal | None = None,
    reference_moisture: Decimal = Decimal("13.5"),
) -> int:
    """Convert an actual deposit to standard-grade-equivalent grams.

    Two corrections, both physical rather than economic:

    * **Grade.** Grade C maize is still maize, but a kilogram of it is not
      worth a kilogram of Grade A. Rather than issue a separate note series
      per grade -- which would fragment liquidity across sixty series -- the
      deposit is converted to standard-grade equivalent.
    * **Moisture.** Water is not the commodity. Selling wet grain by gross
      weight is the oldest trick in agricultural trade, and a weight-based
      currency would institutionalise it without this correction.
    """
    factor = GRADE_FACTOR.get(grade.upper(), Decimal(0))
    adjusted = Decimal(gross_grams) * factor
    if moisture_pct is not None:
        # Normalise to reference moisture: dry matter is what is real.
        dry_fraction = (Decimal(100) - moisture_pct) / (
            Decimal(100) - reference_moisture
        )
        adjusted *= dry_fraction
    return int(adjusted.quantize(Decimal(1), rounding=ROUND_DOWN))


def issuable_units(
    gross_grams: int,
    cls: CommodityClass,
    grade: str = "A",
    moisture_pct: Decimal | None = None,
) -> int:
    """Units issuable against a deposit, in grams of standard grade.

    Deliberately conservative at every step: quality adjustment rounds down,
    then the physical haircut is applied, then rounding down again. The
    system should always hold slightly more than it has promised.
    """
    adjusted = quality_adjusted_grams(gross_grams, grade, moisture_pct)
    haircut = PHYSICAL_HAIRCUT.get(cls.code, Decimal("0.10"))
    net = Decimal(adjusted) * (Decimal(1) - haircut)
    return int(net.quantize(Decimal(1), rounding=ROUND_DOWN))


# --------------------------------------------------------------------------
# The cost of abandoning a common unit of account
# --------------------------------------------------------------------------


def exchange_rate_count(n_goods: int, numeraire: bool) -> int:
    """How many exchange rates a market must know.

    Without a numéraire every pair of goods needs its own rate: N(N-1)/2.
    With one, every good needs only its rate against the numéraire: N-1.
    This is the classic efficiency argument for money, and a weight-
    denominated system gives it up unless a numéraire emerges.
    """
    if numeraire:
        return max(0, n_goods - 1)
    return n_goods * (n_goods - 1) // 2


def numeraire_saving(n_goods: int) -> tuple[int, int, float]:
    """(without, with, ratio) exchange rates for an N-good economy."""
    w = exchange_rate_count(n_goods, False)
    m = exchange_rate_count(n_goods, True)
    return w, m, (w / m if m else float("inf"))


def numeraire_score(cls: CommodityClass) -> Decimal:
    """How well a class would serve as the market's reference good.

    A numéraire wants to be non-decaying, cheap to store, finely divisible,
    widely held and easy to verify. Nobody appoints it -- markets settle on
    one -- but the system can predict which class will win, and should make
    sure that class is well run rather than trying to mandate a different
    one.
    """
    score = Decimal(1)
    if cls.tier is Tier.A:
        score *= Decimal("0.3")          # decaying goods make poor references
    score *= Decimal(1) - Decimal(str(min(cls.storage_cost_pa, Decimal("0.5"))))
    liquidity_weight = {
        "deep, globally priced": Decimal("1.0"),
        "deep": Decimal("0.9"),
        "deep where grid exists": Decimal("0.6"),
        "deep (fertiliser), moderate (other)": Decimal("0.6"),
        "deep but local": Decimal("0.7"),
        "moderate": Decimal("0.5"),
        "moderate (export-linked)": Decimal("0.4"),
        "thin": Decimal("0.2"),
        "export-only": Decimal("0.1"),
        "very thin": Decimal("0.1"),
    }
    score *= liquidity_weight.get(cls.liquidity, Decimal("0.3"))
    if UNIT_DEFINITION.get(cls.code, ("", ""))[0] != UnitBasis.WEIGHT:
        score *= Decimal("0.6")          # awkward to divide and compare
    return score.quantize(Decimal("0.0001"))


def ranked_numeraires() -> list[tuple[CommodityClass, Decimal]]:
    """Classes ranked by fitness to become the market's reference good."""
    scored = [(c, numeraire_score(c)) for c in REGISTER]
    return sorted(scored, key=lambda t: t[1], reverse=True)


# --------------------------------------------------------------------------
# Observed trade data -- descriptive, never prescriptive
# --------------------------------------------------------------------------


@dataclass
class TradeObservation:
    """One completed exchange, recorded for information only."""

    gave_code: str
    gave_units: int
    got_code: str
    got_units: int
    when: date

    def rate(self) -> Decimal:
        """Units of ``got`` per unit of ``gave``."""
        if self.gave_units == 0:
            return Decimal(0)
        return (Decimal(self.got_units) / Decimal(self.gave_units)).quantize(
            Decimal("0.0001"), rounding=ROUND_HALF_UP
        )


@dataclass
class TradeBook:
    """Recent observed trades between two classes.

    This replaces the price committee. It does not set a price, recommend a
    price, or assess value. It reports what other people actually did, and
    lets the buyer draw their own conclusion. The distinction matters: a
    published *assessment* is an authority that can be captured, whereas a
    published *observation* is a fact that can be checked.
    """

    observations: list[TradeObservation] = field(default_factory=list)

    def add(self, obs: TradeObservation) -> None:
        self.observations.append(obs)

    def between(self, a: str, b: str, since: date | None = None) -> list[Decimal]:
        rates = []
        for o in self.observations:
            if since and o.when < since:
                continue
            if o.gave_code == a and o.got_code == b:
                rates.append(o.rate())
            elif o.gave_code == b and o.got_code == a and o.rate() != 0:
                rates.append(
                    (Decimal(1) / o.rate()).quantize(Decimal("0.0001"))
                )
        return rates

    def summary(self, a: str, b: str, since: date | None = None) -> dict[str, object]:
        """Descriptive statistics with an explicit confidence statement."""
        rates = sorted(self.between(a, b, since))
        n = len(rates)
        if n == 0:
            return {"n": 0, "confidence": "no data", "median": None,
                    "low": None, "high": None}
        median = rates[n // 2] if n % 2 else (
            (rates[n // 2 - 1] + rates[n // 2]) / 2
        ).quantize(Decimal("0.0001"))
        confidence = "high" if n >= 10 else "medium" if n >= 3 else "low"
        return {
            "n": n,
            "confidence": confidence,
            "median": median,
            "low": rates[0],
            "high": rates[-1],
            "spread": (rates[-1] - rates[0]).quantize(Decimal("0.0001")),
        }
