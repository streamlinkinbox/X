"""External trade, import dependency and withdrawal risk.

The governing analogy is medical, and it is more exact than it first appears.

Abrupt withdrawal from different substances has very different consequences.
Stopping caffeine causes headaches. Stopping opioids is agonising but rarely
kills. Stopping alcohol or benzodiazepines after heavy dependence can kill
outright, through seizures and delirium. **The correct response is therefore
never uniform**: some dependencies can be dropped immediately, some must be
tapered, and for some the safe course is managed maintenance while capacity
is built elsewhere.

Imports behave the same way. Losing imported fashion goods is a nuisance.
Losing imported fuel is a severe but survivable shock. Losing imported
insulin, anaesthetics or oxygen kills identifiable people within days.

Treating all imports as one undifferentiated "dependency to be reduced" is
the equivalent of telling every patient to quit everything at once. That is
how the cure kills.

This module therefore:

1. classifies imports by **withdrawal severity**, not by volume or value;
2. sizes **buffer stocks** so that time-to-harm exceeds time-to-resupply;
3. tests whether export earnings can actually fund the critical basket;
4. ranks **substitution** options by cost per unit of dependency removed;
5. measures whether dependency is **rising or falling** over time.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import ROUND_HALF_UP, Decimal
from enum import Enum


def _q(x: Decimal, places: str = "0.01") -> Decimal:
    return x.quantize(Decimal(places), rounding=ROUND_HALF_UP)


class Withdrawal(str, Enum):
    """Consequence of losing an import abruptly and completely."""

    #: People die within days. No substitute, no tolerable delay.
    LETHAL = "lethal"
    #: Severe harm and some excess deaths over weeks. Partial substitutes.
    SEVERE = "severe"
    #: Major economic disruption, little direct mortality.
    DISRUPTIVE = "disruptive"
    #: Inconvenient. Local substitutes exist or the good is discretionary.
    TOLERABLE = "tolerable"


#: Days from cutoff to first serious harm. Together with resupply lead time
#: this sets buffer size -- not the value of the import, and not its volume.
TIME_TO_HARM_DAYS: dict[Withdrawal, int] = {
    Withdrawal.LETHAL: 7,
    Withdrawal.SEVERE: 45,
    Withdrawal.DISRUPTIVE: 120,
    Withdrawal.TOLERABLE: 365,
}

#: Realistic days to find and land an alternative supply after a cutoff.
DEFAULT_RESUPPLY_DAYS: int = 90


@dataclass(frozen=True)
class Import:
    """One imported good or class of goods."""

    name: str
    withdrawal: Withdrawal
    #: Annual cost in hard currency.
    annual_fx_cost: float
    #: Fraction of demand that could be met locally today, 0..1.
    local_substitutable_now: float = 0.0
    #: Fraction that could be met locally after investment.
    local_substitutable_potential: float = 0.0
    #: One-off cost to reach that potential, in hard currency.
    substitution_capex: float = 0.0
    #: Years to build that capacity.
    substitution_years: float = 0.0
    notes: str = ""

    @property
    def time_to_harm_days(self) -> int:
        return TIME_TO_HARM_DAYS[self.withdrawal]

    @property
    def daily_fx_cost(self) -> float:
        return self.annual_fx_cost / 365

    def buffer_days(
        self, resupply_days: int = DEFAULT_RESUPPLY_DAYS, safety_factor: float = 1.5
    ) -> float:
        """Days of stock required to survive a supply cut.

        The buffer only has to cover the **gap** between how long resupply
        takes and how long the community can last unharmed. If a good can be
        replaced faster than it causes harm, no buffer is needed at all --
        which is why discretionary imports should never be stockpiled.
        """
        gap = resupply_days * safety_factor - self.time_to_harm_days
        return max(0.0, gap)

    def buffer_cost(
        self, resupply_days: int = DEFAULT_RESUPPLY_DAYS, safety_factor: float = 1.5
    ) -> float:
        """Hard-currency value of the stock that must be held."""
        return self.daily_fx_cost * self.buffer_days(resupply_days, safety_factor)

    @property
    def residual_dependency(self) -> float:
        """FX cost that remains after all feasible substitution."""
        return self.annual_fx_cost * (1 - self.local_substitutable_potential)

    @property
    def substitution_efficiency(self) -> Decimal:
        """Annual FX saved per unit of capex. Higher is better value."""
        saved = self.annual_fx_cost * (
            self.local_substitutable_potential - self.local_substitutable_now
        )
        if self.substitution_capex <= 0:
            return Decimal("Infinity") if saved > 0 else Decimal(0)
        return _q(Decimal(saved) / Decimal(self.substitution_capex), "0.001")

    def payback_years(self) -> Decimal:
        eff = self.substitution_efficiency
        if eff == 0:
            return Decimal("Infinity")
        if eff.is_infinite():
            return Decimal(0)
        return _q(Decimal(1) / eff)


# --------------------------------------------------------------------------
# A representative import basket for a rural East African district
# --------------------------------------------------------------------------

BASKET: tuple[Import, ...] = (
    Import(
        "Essential medicines (insulin, anaesthetics, oxygen)",
        Withdrawal.LETHAL,
        annual_fx_cost=40_000,
        local_substitutable_now=0.0,
        local_substitutable_potential=0.10,
        substitution_capex=800_000,
        substitution_years=8,
        notes=(
            "Africa imports 95-99% of medicines and close to 100% of active "
            "pharmaceutical ingredients. Formulation can be localised; API "
            "synthesis realistically cannot at district scale."
        ),
    ),
    Import(
        "Vaccines and cold chain",
        Withdrawal.LETHAL,
        annual_fx_cost=15_000,
        local_substitutable_potential=0.0,
        notes="No credible local substitution. Buffer and diversify suppliers only.",
    ),
    Import(
        "Surgical consumables (gloves, sutures, reagents)",
        Withdrawal.SEVERE,
        annual_fx_cost=25_000,
        local_substitutable_now=0.05,
        local_substitutable_potential=0.35,
        substitution_capex=180_000,
        substitution_years=4,
        notes="Basic dressings and some containers are locally makeable.",
    ),
    Import(
        "Fuel (diesel, petrol)",
        Withdrawal.SEVERE,
        annual_fx_cost=120_000,
        local_substitutable_now=0.02,
        local_substitutable_potential=0.45,
        substitution_capex=350_000,
        substitution_years=5,
        notes="Solar, biogas and bioethanol displace pumping and lighting loads.",
    ),
    Import(
        "Fertiliser and agrochemicals",
        Withdrawal.SEVERE,
        annual_fx_cost=90_000,
        local_substitutable_now=0.10,
        local_substitutable_potential=0.60,
        substitution_capex=120_000,
        substitution_years=4,
        notes="Composting, manure, legume rotation, biochar. High-return substitution.",
    ),
    Import(
        "Spare parts and tools",
        Withdrawal.DISRUPTIVE,
        annual_fx_cost=45_000,
        local_substitutable_now=0.15,
        local_substitutable_potential=0.55,
        substitution_capex=90_000,
        substitution_years=3,
        notes="Local fabrication, machining, and a standardised parts library.",
    ),
    Import(
        "Communications equipment",
        Withdrawal.DISRUPTIVE,
        annual_fx_cost=20_000,
        local_substitutable_potential=0.05,
        substitution_capex=60_000,
        substitution_years=5,
        notes="Repair capacity is substitutable; manufacture is not.",
    ),
    Import(
        "Processed foods and beverages",
        Withdrawal.TOLERABLE,
        annual_fx_cost=60_000,
        local_substitutable_now=0.30,
        local_substitutable_potential=0.90,
        substitution_capex=70_000,
        substitution_years=2,
        notes="Highest substitution potential in the basket.",
    ),
    Import(
        "Clothing and household goods",
        Withdrawal.TOLERABLE,
        annual_fx_cost=50_000,
        local_substitutable_now=0.20,
        local_substitutable_potential=0.75,
        substitution_capex=80_000,
        substitution_years=3,
        notes="Local textiles; the TX commodity class feeds this directly.",
    ),
)


# --------------------------------------------------------------------------
# 1. Criticality profile
# --------------------------------------------------------------------------


def by_withdrawal(basket: tuple[Import, ...] = BASKET) -> dict[Withdrawal, float]:
    """Annual FX cost grouped by withdrawal severity."""
    out: dict[Withdrawal, float] = {w: 0.0 for w in Withdrawal}
    for imp in basket:
        out[imp.withdrawal] += imp.annual_fx_cost
    return out


def lethal_share(basket: tuple[Import, ...] = BASKET) -> Decimal:
    """Share of the import bill that kills people if interrupted.

    Usually small in money terms and enormous in consequence -- which is the
    entire point of classifying by severity rather than by value.
    """
    totals = by_withdrawal(basket)
    grand = sum(totals.values())
    if grand == 0:
        return Decimal(0)
    return _q(Decimal(totals[Withdrawal.LETHAL]) / Decimal(grand), "0.001")


# --------------------------------------------------------------------------
# 2. Buffer sizing
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class BufferPlan:
    total_cost: float
    by_item: dict[str, float]
    months_cover_weighted: Decimal

    def cost_of(self, name: str) -> float:
        return self.by_item.get(name, 0.0)


def buffer_plan(
    basket: tuple[Import, ...] = BASKET,
    resupply_days: int = DEFAULT_RESUPPLY_DAYS,
    safety_factor: float = 1.5,
) -> BufferPlan:
    """Cost of holding enough stock that nothing critical runs out first.

    Buffers are sized by **time-to-harm against resupply time**, not
    uniformly. Holding three months of everything is expensive and mostly
    wasted; holding four months of insulin is cheap and saves lives.
    """
    items = {imp.name: imp.buffer_cost(resupply_days, safety_factor) for imp in basket}
    total = sum(items.values())
    annual = sum(imp.annual_fx_cost for imp in basket)
    months = _q(Decimal(total) / Decimal(annual) * 12) if annual else Decimal(0)
    return BufferPlan(total_cost=total, by_item=items, months_cover_weighted=months)


def uniform_buffer_cost(
    basket: tuple[Import, ...] = BASKET, months: int = 3
) -> float:
    """Cost of the naive approach: the same months of cover for everything."""
    annual = sum(imp.annual_fx_cost for imp in basket)
    return annual * months / 12


# --------------------------------------------------------------------------
# 3. Can exports pay for the critical basket?
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class TradeBalance:
    export_fx: float
    critical_fx: float
    total_fx: float

    @property
    def covers_critical(self) -> bool:
        return self.export_fx >= self.critical_fx

    @property
    def covers_all(self) -> bool:
        return self.export_fx >= self.total_fx

    @property
    def critical_coverage(self) -> Decimal:
        if self.critical_fx == 0:
            return Decimal("Infinity")
        return _q(Decimal(self.export_fx) / Decimal(self.critical_fx), "0.001")

    @property
    def discretionary_headroom(self) -> float:
        return self.export_fx - self.critical_fx


def trade_balance(
    export_fx: float, basket: tuple[Import, ...] = BASKET
) -> TradeBalance:
    """Test export earnings against the import bill, critical first.

    The ordering matters. A community that spends its foreign exchange on
    discretionary imports and then cannot buy insulin has not made a trade
    error, it has made a triage error.
    """
    critical = sum(
        imp.annual_fx_cost
        for imp in basket
        if imp.withdrawal in (Withdrawal.LETHAL, Withdrawal.SEVERE)
    )
    total = sum(imp.annual_fx_cost for imp in basket)
    return TradeBalance(export_fx=export_fx, critical_fx=critical, total_fx=total)


def minimum_exports_needed(basket: tuple[Import, ...] = BASKET) -> float:
    """Export earnings required to cover everything that is not discretionary."""
    return sum(
        imp.annual_fx_cost
        for imp in basket
        if imp.withdrawal in (Withdrawal.LETHAL, Withdrawal.SEVERE)
    )


# --------------------------------------------------------------------------
# 4. Substitution ladder
# --------------------------------------------------------------------------


def substitution_ladder(
    basket: tuple[Import, ...] = BASKET,
) -> list[tuple[Import, Decimal, Decimal]]:
    """Rank substitution projects by FX saved per unit of capital.

    Answers "what should we localise first?" with arithmetic instead of
    sentiment. The intuitive answer -- start with medicines, because they
    matter most -- is usually the worst value, because pharmaceutical
    manufacture is the hardest thing on the list.
    """
    rows = []
    for imp in basket:
        rows.append((imp, imp.substitution_efficiency, imp.payback_years()))
    return sorted(
        rows,
        key=lambda r: (
            -float(r[1]) if not r[1].is_infinite() else float("-inf"),
        ),
    )


def achievable_independence(basket: tuple[Import, ...] = BASKET) -> Decimal:
    """Share of the import bill that could realistically be localised."""
    total = sum(imp.annual_fx_cost for imp in basket)
    residual = sum(imp.residual_dependency for imp in basket)
    if total == 0:
        return Decimal(0)
    return _q(Decimal(total - residual) / Decimal(total), "0.001")


def irreducible_dependency(basket: tuple[Import, ...] = BASKET) -> float:
    """Annual FX that must be earned no matter how much is localised."""
    return sum(imp.residual_dependency for imp in basket)


# --------------------------------------------------------------------------
# 5. Is dependency rising or falling?
# --------------------------------------------------------------------------


@dataclass
class DependencyTrend:
    """Track the ratchet. Dependency grows quietly and is noticed late."""

    years: list[int] = field(default_factory=list)
    import_fx: list[float] = field(default_factory=list)
    export_fx: list[float] = field(default_factory=list)

    def add(self, year: int, imports: float, exports: float) -> None:
        self.years.append(year)
        self.import_fx.append(imports)
        self.export_fx.append(exports)

    def self_reliance(self) -> list[Decimal]:
        return [
            _q(Decimal(e) / Decimal(i), "0.001") if i else Decimal("Infinity")
            for i, e in zip(self.import_fx, self.export_fx)
        ]

    def worsening(self) -> bool:
        """Is the community becoming more dependent, not less?"""
        r = self.self_reliance()
        return len(r) >= 2 and r[-1] < r[0]

    def alarm(self, floor: Decimal = Decimal("1.0")) -> bool:
        r = self.self_reliance()
        return bool(r) and r[-1] < floor


# --------------------------------------------------------------------------
# 6. Sovereign Reserve Defense & Financial Extortion Counter-Offensive
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class SovereignReserveDefense:
    """Models the 5-step sovereign response to foreign reserve freezes and financial blackmail."""

    frozen_foreign_reserves_rcu: float = 1_000_000_000.0
    hostile_foreign_corporate_assets_inside_borders_rcu: float = 1_200_000_000.0
    sovereign_debt_owed_to_hostile_jurisdiction_rcu: float = 800_000_000.0
    bilateral_commodity_clearing_share_pct: float = 0.95
    onshore_physical_gold_and_commodity_share_pct: float = 1.0
    sovereign_payment_switch_active: bool = True

    def execute_counter_offensive(self) -> dict[str, str | bool | float]:
        # Step 1: 1-to-1 Debt Cancellation against hostile jurisdiction
        debt_cancelled = min(
            self.frozen_foreign_reserves_rcu,
            self.sovereign_debt_owed_to_hostile_jurisdiction_rcu,
        )
        remaining_uncovered_freeze = self.frozen_foreign_reserves_rcu - debt_cancelled

        # Step 2: Reciprocal Domestic Asset Seizure into Sovereign Escrow
        corporate_assets_placed_in_escrow = min(
            self.hostile_foreign_corporate_assets_inside_borders_rcu,
            max(remaining_uncovered_freeze, 0.0),
        )

        # Net leverage: Hostage assets held vs Frozen paper
        total_sovereign_offsets = debt_cancelled + corporate_assets_placed_in_escrow
        net_leverage_ratio = total_sovereign_offsets / max(self.frozen_foreign_reserves_rcu, 1.0)

        return {
            "frozen_foreign_reserves_rcu": self.frozen_foreign_reserves_rcu,
            "sovereign_debt_cancelled_rcu": debt_cancelled,
            "corporate_assets_seized_into_escrow_rcu": corporate_assets_placed_in_escrow,
            "total_sovereign_recovery_value_rcu": total_sovereign_offsets,
            "net_leverage_ratio": round(net_leverage_ratio, 2),
            "bilateral_clearing_sanctions_immune": self.bilateral_commodity_clearing_share_pct >= 0.90,
            "domestic_payment_switch_immune": self.sovereign_payment_switch_active,
            "financial_blackmail_neutralized": net_leverage_ratio >= 1.0,
        }

