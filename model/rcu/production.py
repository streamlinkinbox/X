"""Local production: which imports can actually be manufactured locally.

Section 16 established that ~49% of the import bill is irreducible and that
substituting medicines has a ~200-year payback. That analysis treated
"medicines" as a single undifferentiated category, which is too coarse and
produces an unnecessarily bleak answer.

This module disaggregates. Some things inside the lethal basket **are**
locally producible with known, costed, proven technology -- medical oxygen
being the clearest case. Others are not, and no amount of determination
changes that.

The organising concept is the **production ladder**: a ranking by technical
difficulty rather than by importance. A community climbs it in order,
because attempting a rung before mastering the one below wastes capital and
discredits the whole programme.

Rung 1  Grow / gather        -- biology does the work
Rung 2  Simple processing    -- press, ferment, dry, mill
Rung 3  Mechanical assembly  -- fabricate, machine, repair
Rung 4  Controlled chemistry -- reactions needing purity and process control
Rung 5  Precision synthesis  -- APIs, semiconductors, vaccines
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal
from enum import IntEnum


def _q(x: Decimal, places: str = "0.01") -> Decimal:
    return x.quantize(Decimal(places), rounding=ROUND_HALF_UP)


class Rung(IntEnum):
    """Technical difficulty of local production."""

    GROW = 1
    PROCESS = 2
    FABRICATE = 3
    CHEMISTRY = 4
    PRECISION = 5


#: What each rung requires. A community cannot skip rungs: precision
#: synthesis needs the metalwork, power and quality systems of every rung
#: below it. This is why "just make our own medicines" fails.
RUNG_REQUIREMENTS: dict[Rung, str] = {
    Rung.GROW: "land, water, seed, knowledge",
    Rung.PROCESS: "presses, driers, fermenters, clean water, storage",
    Rung.FABRICATE: "workshop, power, metalwork, measurement tools",
    Rung.CHEMISTRY: "controlled environment, reagents, testing, trained chemists",
    Rung.PRECISION: "regulatory approval, sterile plant, analytical labs, scale",
}


@dataclass(frozen=True)
class LocalProduct:
    """A good that might be produced locally instead of imported."""

    name: str
    rung: Rung
    #: Annual FX currently spent importing it.
    import_fx: float
    #: Fraction of local demand a district-scale facility could meet.
    achievable_share: float
    #: Capital cost to build the capability.
    capex: float
    #: Annual operating cost, including maintenance and consumables.
    opex_per_year: float
    #: Years from decision to first output.
    lead_time_years: float
    #: Inputs that must still be imported even when producing locally.
    residual_imports: str = ""
    #: Withdrawal severity if supply fails, mirroring section 16.
    lethal: bool = False
    notes: str = ""

    @property
    def fx_saved_per_year(self) -> float:
        """Gross FX saved, before local operating costs."""
        return self.import_fx * self.achievable_share

    @property
    def net_saving_per_year(self) -> float:
        """FX saved after paying to run the facility.

        The number that actually matters. A plant that saves $40,000 of
        imports but costs $45,000 a year to run has made the community
        poorer and less resilient, not more.
        """
        return self.fx_saved_per_year - self.opex_per_year

    @property
    def viable(self) -> bool:
        return self.net_saving_per_year > 0

    def payback_years(self) -> Decimal:
        if self.net_saving_per_year <= 0:
            return Decimal("Infinity")
        return _q(Decimal(self.capex) / Decimal(self.net_saving_per_year))

    @property
    def sovereignty_value(self) -> Decimal:
        """Resilience gained per unit of capital, weighting lethal goods.

        Payback alone undervalues lethal goods: a plant that never pays for
        itself financially may still be the single most valuable thing a
        community builds, because the alternative is people dying when a
        supply line closes. Lethal goods are weighted 5x.
        """
        if self.capex <= 0:
            return Decimal("Infinity")
        weight = Decimal(5) if self.lethal else Decimal(1)
        return _q(
            Decimal(self.fx_saved_per_year) * weight / Decimal(self.capex), "0.001"
        )


#: Candidate local production projects for a rural district. Costs are order
#: of magnitude and must be replaced with local quotes before any decision.
LADDER: tuple[LocalProduct, ...] = (
    # ---- Rung 1: grow ----
    LocalProduct(
        "Food staples (displacing processed imports)",
        Rung.GROW,
        import_fx=60_000,
        achievable_share=0.90,
        capex=70_000,
        opex_per_year=12_000,
        lead_time_years=2,
        notes="Already the highest-return substitution in section 16.",
    ),
    LocalProduct(
        "Medicinal plants (artemisinin, aloe, neem)",
        Rung.GROW,
        import_fx=8_000,
        achievable_share=0.40,
        capex=25_000,
        opex_per_year=4_000,
        lead_time_years=3,
        residual_imports="extraction solvents, quality testing",
        notes=(
            "Growing the plant is rung 1; extracting a standardised active "
            "ingredient from it is rung 4. Do not confuse the two."
        ),
    ),
    LocalProduct(
        "Cotton and fibre for textiles",
        Rung.GROW,
        import_fx=50_000,
        achievable_share=0.75,
        capex=80_000,
        opex_per_year=15_000,
        lead_time_years=3,
    ),
    # ---- Rung 2: simple processing ----
    LocalProduct(
        "Biogas (cooking and small generation)",
        Rung.PROCESS,
        import_fx=45_000,
        achievable_share=0.55,
        capex=90_000,
        opex_per_year=8_000,
        lead_time_years=2,
        notes="Digesters are simple, robust, and use waste already present.",
    ),
    LocalProduct(
        "Bioethanol (fuel and disinfectant)",
        Rung.PROCESS,
        import_fx=35_000,
        achievable_share=0.45,
        capex=110_000,
        opex_per_year=14_000,
        lead_time_years=3,
        notes=(
            "Dual-use and strategically valuable: the same still that makes "
            "fuel makes 70% ethanol for wound cleaning and sterilisation."
        ),
    ),
    LocalProduct(
        "Compost and biochar fertiliser",
        Rung.PROCESS,
        import_fx=90_000,
        achievable_share=0.60,
        capex=120_000,
        opex_per_year=20_000,
        lead_time_years=4,
        notes="Highest-value severe-category substitution in the basket.",
    ),
    LocalProduct(
        "Soap, disinfectant, basic hygiene",
        Rung.PROCESS,
        import_fx=15_000,
        achievable_share=0.85,
        capex=20_000,
        opex_per_year=3_000,
        lead_time_years=1,
        notes="Cheap, fast, and directly reduces infection load.",
    ),
    LocalProduct(
        "Oral rehydration salts",
        Rung.PROCESS,
        import_fx=6_000,
        achievable_share=0.80,
        capex=18_000,
        opex_per_year=2_500,
        lead_time_years=1,
        lethal=True,
        residual_imports="pharmaceutical-grade salts, sachet film",
        notes=(
            "Sugar, salt and clean water. Treats the leading cause of child "
            "death from diarrhoea. The highest life-per-dollar item on the "
            "entire ladder."
        ),
    ),
    # ---- Rung 3: fabricate ----
    LocalProduct(
        "Medical oxygen (PSA plant)",
        Rung.FABRICATE,
        import_fx=20_000,
        achievable_share=0.85,
        capex=105_000,
        opex_per_year=9_000,
        lead_time_years=2,
        lethal=True,
        residual_imports="compressor spares, zeolite replacement, cylinders",
        notes=(
            "Proven at district scale in Kenya, Rwanda and Ethiopia: a "
            "150-200 bed facility plant costs roughly USD 100-110k, and "
            "life-cycle cost has been measured near USD 7.34 per patient "
            "treated. Oxygen is made from air -- it cannot be embargoed."
        ),
    ),
    LocalProduct(
        "Solar power and battery systems",
        Rung.FABRICATE,
        import_fx=40_000,
        achievable_share=0.50,
        capex=160_000,
        opex_per_year=12_000,
        lead_time_years=3,
        residual_imports="panels, cells, controllers",
        notes="Assembly and maintenance are local; cells are not.",
    ),
    LocalProduct(
        "Spare parts and tool fabrication",
        Rung.FABRICATE,
        import_fx=45_000,
        achievable_share=0.55,
        capex=90_000,
        opex_per_year=16_000,
        lead_time_years=3,
    ),
    LocalProduct(
        "Basic medical consumables (dressings, containers)",
        Rung.FABRICATE,
        import_fx=25_000,
        achievable_share=0.30,
        capex=70_000,
        opex_per_year=9_000,
        lead_time_years=3,
        residual_imports="sterile packaging, gloves, sutures",
    ),
    # ---- Rung 4: controlled chemistry ----
    LocalProduct(
        "IV fluids and saline",
        Rung.CHEMISTRY,
        import_fx=12_000,
        achievable_share=0.50,
        capex=220_000,
        opex_per_year=18_000,
        lead_time_years=5,
        lethal=True,
        residual_imports="pharmaceutical-grade salts, sterile bags, filters",
        notes=(
            "Technically salt and water, but sterility and pyrogen control "
            "are unforgiving. Contaminated IV fluid kills faster than the "
            "condition it treats. Attempt only with real regulatory capacity."
        ),
    ),
    LocalProduct(
        "Formulation of imported APIs into tablets",
        Rung.CHEMISTRY,
        import_fx=40_000,
        achievable_share=0.25,
        capex=400_000,
        opex_per_year=45_000,
        lead_time_years=6,
        lethal=True,
        residual_imports="all active pharmaceutical ingredients, excipients",
        notes=(
            "This is what most African pharmaceutical plants actually do: "
            "formulate imported APIs. It reduces neither API dependency nor "
            "FX exposure much, because the API is most of the value."
        ),
    ),
    # ---- Rung 5: precision synthesis ----
    LocalProduct(
        "Active pharmaceutical ingredient synthesis",
        Rung.PRECISION,
        import_fx=40_000,
        achievable_share=0.05,
        capex=2_000_000,
        opex_per_year=180_000,
        lead_time_years=10,
        lethal=True,
        residual_imports="precursor chemicals, catalysts, analytical equipment",
        notes=(
            "Africa imports close to 100% of APIs. This is a national or "
            "continental project, not a district one. Included to show why."
        ),
    ),
    LocalProduct(
        "Vaccine manufacture",
        Rung.PRECISION,
        import_fx=15_000,
        achievable_share=0.0,
        capex=5_000_000,
        opex_per_year=400_000,
        lead_time_years=12,
        lethal=True,
        residual_imports="everything",
        notes="Not achievable at district scale under any assumption.",
    ),
)


def by_rung(ladder: tuple[LocalProduct, ...] = LADDER) -> dict[Rung, list[LocalProduct]]:
    out: dict[Rung, list[LocalProduct]] = {r: [] for r in Rung}
    for p in ladder:
        out[p.rung].append(p)
    return out


def viable_projects(ladder: tuple[LocalProduct, ...] = LADDER) -> list[LocalProduct]:
    """Projects that save more FX than they cost to operate."""
    return [p for p in ladder if p.viable]


def unviable_projects(ladder: tuple[LocalProduct, ...] = LADDER) -> list[LocalProduct]:
    return [p for p in ladder if not p.viable]


def ranked_by_payback(
    ladder: tuple[LocalProduct, ...] = LADDER,
) -> list[LocalProduct]:
    return sorted(viable_projects(ladder), key=lambda p: float(p.payback_years()))


def ranked_by_sovereignty(
    ladder: tuple[LocalProduct, ...] = LADDER,
) -> list[LocalProduct]:
    """Rank by resilience per unit capital, weighting lethal goods."""
    return sorted(ladder, key=lambda p: -float(p.sovereignty_value))


@dataclass(frozen=True)
class ProgrammeResult:
    projects: tuple[LocalProduct, ...]
    total_capex: float
    total_net_saving: float
    fx_bill_before: float
    fx_bill_after: float
    lethal_covered: int

    @property
    def independence_gain(self) -> Decimal:
        if self.fx_bill_before == 0:
            return Decimal(0)
        return _q(
            Decimal(self.fx_bill_before - self.fx_bill_after)
            / Decimal(self.fx_bill_before),
            "0.001",
        )

    @property
    def blended_payback(self) -> Decimal:
        if self.total_net_saving <= 0:
            return Decimal("Infinity")
        return _q(Decimal(self.total_capex) / Decimal(self.total_net_saving))


def build_programme(
    budget: float,
    ladder: tuple[LocalProduct, ...] = LADDER,
    prioritise_lethal: bool = True,
) -> ProgrammeResult:
    """Select projects under a capital budget.

    With ``prioritise_lethal`` the selection ranks by sovereignty value,
    which buys resilience per dollar. Without it, selection ranks by payback,
    which buys money. The two produce materially different programmes, and
    the difference is the whole argument of the section.
    """
    candidates = (
        ranked_by_sovereignty(ladder) if prioritise_lethal else ranked_by_payback(ladder)
    )
    chosen: list[LocalProduct] = []
    spent = 0.0
    for p in candidates:
        if not p.viable and not (prioritise_lethal and p.lethal):
            continue
        if spent + p.capex <= budget:
            chosen.append(p)
            spent += p.capex

    before = sum(p.import_fx for p in ladder)
    saved = sum(p.fx_saved_per_year for p in chosen)
    return ProgrammeResult(
        projects=tuple(chosen),
        total_capex=spent,
        total_net_saving=sum(p.net_saving_per_year for p in chosen),
        fx_bill_before=before,
        fx_bill_after=before - saved,
        lethal_covered=sum(1 for p in chosen if p.lethal),
    )


def dual_use_products(ladder: tuple[LocalProduct, ...] = LADDER) -> list[LocalProduct]:
    """Products whose output serves both ordinary and critical needs.

    These are disproportionately valuable because the ordinary demand keeps
    the plant running, staffed and maintained during normal times, so the
    capability is there when the critical need arrives. A facility that only
    operates in emergencies will be broken when the emergency comes.
    """
    keys = ("ethanol", "oxygen", "soap", "biogas")
    return [p for p in ladder if any(k in p.name.lower() for k in keys)]
