"""Bundle pricing, dual-price receipts and settlement.

Three ideas are implemented here, and they interlock:

1. **Bundle quoting.** A price is not a scalar. It is a basket of claims on
   different real commodities: "this house costs 100 iron + 500 wood + 40
   plastic". The seller states which *goods* they want, not merely how much
   value.

2. **The dual-price receipt.** Every quote carries both the *asked* bundle
   and an independent *reference* bundle — the assessed worth of the thing
   being sold. The buyer sees the markup as a number and decides whether
   they are being robbed.

3. **Quote-in-face, settle-in-value.** Prices are quoted in fresh-note
   equivalents. Tendered notes are valued at their current decayed worth.
   An old note therefore buys less, and the buyer must tender more of it.
   This is the mechanism by which demurrage actually reaches the market.

The distinction in (3) is the subtle one. If prices were quoted in decayed
value, a seller could not post a stable price. If settlement ignored decay,
demurrage would be fiction. Quoting in face and settling in value keeps
posted prices stable while making age costly at the moment of payment.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from decimal import ROUND_HALF_UP, Decimal

from .classes import CommodityClass, Tier, get
from .valuation import CENTS, Note, decay_multiplier, months_elapsed

#: A bundle maps a class code to a quantity of *face* units (not cents).
Bundle = dict[str, int]


def bundle_face_cents(bundle: Bundle) -> int:
    """Total face value of a bundle, in cents."""
    return sum(units * CENTS for units in bundle.values())


def bundle_tier_split(bundle: Bundle) -> tuple[Decimal, Decimal]:
    """Fraction of a bundle's face value in Tier A and Tier B respectively.

    This is the number that governs whether the bundle-pricing mechanism
    actually constrains demurrage arbitrage. A bundle that is 100% Tier B
    lets a hoarder pay without ever parting with a stable note.
    """
    total = bundle_face_cents(bundle)
    if total == 0:
        return Decimal(0), Decimal(0)
    a = sum(u * CENTS for c, u in bundle.items() if get(c).tier is Tier.A)
    b = total - a
    return (
        (Decimal(a) / total).quantize(Decimal("0.0001")),
        (Decimal(b) / total).quantize(Decimal("0.0001")),
    )


@dataclass(frozen=True)
class Receipt:
    """A dual-price quote for a good or service.

    ``asked`` is what the seller wants. ``reference`` is the independently
    assessed value of the item, published by the price committee or derived
    from recent comparable transactions. The gap between them is the seller's
    margin, and it is disclosed rather than hidden.
    """

    item: str
    asked: Bundle
    reference: Bundle
    quoted_on: date
    seller: str = ""
    reference_source: str = "committee weekly index"

    # ---- headline figures -------------------------------------------------

    @property
    def asked_cents(self) -> int:
        return bundle_face_cents(self.asked)

    @property
    def reference_cents(self) -> int:
        return bundle_face_cents(self.reference)

    @property
    def markup(self) -> Decimal:
        """Asked over reference, as a fraction. 0.25 means 25% above assessed."""
        if self.reference_cents == 0:
            return Decimal(0)
        return (
            Decimal(self.asked_cents - self.reference_cents)
            / Decimal(self.reference_cents)
        ).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)

    @property
    def markup_by_class(self) -> dict[str, Decimal]:
        """Per-class markup, so a buyer can see *where* the margin sits."""
        out: dict[str, Decimal] = {}
        for code in sorted(set(self.asked) | set(self.reference)):
            a = Decimal(self.asked.get(code, 0))
            r = Decimal(self.reference.get(code, 0))
            if r == 0:
                out[code] = Decimal("Infinity") if a > 0 else Decimal(0)
            else:
                out[code] = ((a - r) / r).quantize(
                    Decimal("0.0001"), rounding=ROUND_HALF_UP
                )
        return out

    @property
    def fairness(self) -> str:
        """A plain-language verdict for the receipt, printed in local language.

        Thresholds are deliberately coarse. The purpose is not precision; it
        is to let someone who cannot compute a percentage see immediately
        whether a price is ordinary or extreme.
        """
        m = float(self.markup)
        if m <= 0.10:
            return "at or below assessed value"
        if m <= 0.30:
            return "normal margin"
        if m <= 0.75:
            return "high margin"
        return "very high margin — check other sellers"

    # ---- time pressure on the seller --------------------------------------

    def offer_value_at(self, asof: date) -> int:
        """Value of the asked bundle if the notes were issued when quoted.

        A seller holding out for a high price in decaying classes is losing
        value while they wait. This makes the cost of not selling explicit.
        """
        total = 0
        for code, units in self.asked.items():
            cls = get(code)
            age = months_elapsed(self.quoted_on, asof)
            mult = decay_multiplier(cls, age)
            total += int(
                (Decimal(units * CENTS) * mult).quantize(
                    Decimal(1), rounding=ROUND_HALF_UP
                )
            )
        return total

    def holding_cost_schedule(self, months: int = 12) -> list[tuple[int, int, Decimal]]:
        """``(month, value_cents, fraction_of_original)`` for the asked bundle."""
        base = self.asked_cents
        out = []
        for m in range(months + 1):
            asof = _add_months(self.quoted_on, m)
            v = self.offer_value_at(asof)
            frac = (Decimal(v) / base).quantize(Decimal("0.0001")) if base else Decimal(0)
            out.append((m, v, frac))
        return out

    # ---- printable ---------------------------------------------------------

    def render(self) -> str:
        """The receipt as it would be printed or shown on a phone."""
        W = 52
        bar = "+" + "-" * W + "+"

        def row(s: str) -> str:
            return "| " + s[: W - 2].ljust(W - 2) + " |"

        lines = [bar, row(self.item), bar, row("ASKED         ASSESSED        DIFFERENCE")]
        for code in sorted(set(self.asked) | set(self.reference)):
            a = self.asked.get(code, 0)
            r = self.reference.get(code, 0)
            mk = self.markup_by_class[code]
            mks = "n/a" if mk.is_infinite() else f"{float(mk) * 100:+.0f}%"
            tier = "decays" if get(code).tier is Tier.A else "stable"
            lines.append(
                row(f"{a:>6} {code} {tier:<7}{r:>6} {code}      {mks:>10}")
            )
        lines += [
            bar,
            row(f"TOTAL ASKED      {self.asked_cents / CENTS:>12,.0f} units"),
            row(f"ASSESSED VALUE   {self.reference_cents / CENTS:>12,.0f} units"),
            row(f"MARKUP           {float(self.markup) * 100:>+12.1f}%"),
            row(self.fairness.upper()),
            bar,
        ]
        a_share, b_share = bundle_tier_split(self.asked)
        lines.append(
            row(
                f"Bundle: {float(a_share) * 100:.0f}% decaying / "
                f"{float(b_share) * 100:.0f}% stable"
            )
        )
        # Report the first horizon at which the bundle has actually lost
        # value, rather than a fixed 6 months which grace periods may hide.
        sched = self.holding_cost_schedule(24)
        eroded = next((m for m, _, f in sched if f < Decimal("0.995")), None)
        if eroded is None:
            lines.append(row("Seller's cost of waiting: none within 24 months"))
        else:
            v24 = float(sched[-1][2]) * 100
            lines.append(
                row(f"Unsold: loses value from month {eroded}; {v24:.0f}% at 24 mo")
            )
        lines.append(bar)
        return "\n".join(lines)


def _add_months(d: date, months: int) -> date:
    y = d.year + (d.month - 1 + months) // 12
    m = (d.month - 1 + months) % 12 + 1
    day = min(
        d.day,
        [31, 29 if y % 4 == 0 and (y % 100 != 0 or y % 400 == 0) else 28,
         31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1],
    )
    return date(y, m, day)


# --------------------------------------------------------------------------
# Settlement
# --------------------------------------------------------------------------


@dataclass
class Settlement:
    """The result of tendering notes against a quoted bundle."""

    required_face_cents: dict[str, int]
    tendered_value_cents: dict[str, int]
    shortfall_cents: dict[str, int] = field(default_factory=dict)
    surplus_cents: dict[str, int] = field(default_factory=dict)

    @property
    def settled(self) -> bool:
        return not any(v > 0 for v in self.shortfall_cents.values())

    @property
    def total_shortfall(self) -> int:
        return sum(self.shortfall_cents.values())

    @property
    def age_penalty_cents(self) -> int:
        """Extra face value the buyer had to hand over because notes were old."""
        tendered_face = sum(self.tendered_value_cents.values())
        required = sum(self.required_face_cents.values())
        return max(0, tendered_face - required)


def settle(quoted: Bundle, tendered: list[Note], asof: date) -> Settlement:
    """Value tendered notes against a quoted bundle.

    Prices are quoted in fresh-note equivalents; notes are credited at their
    *current* value. A buyer paying with aged Tier A notes must hand over
    more of them. This is where demurrage becomes real to the participants.
    """
    required = {code: units * CENTS for code, units in quoted.items()}
    credited: dict[str, int] = {code: 0 for code in quoted}
    for n in tendered:
        credited.setdefault(n.class_code, 0)
        credited[n.class_code] += n.value_cents(asof)

    shortfall, surplus = {}, {}
    for code, need in required.items():
        got = credited.get(code, 0)
        shortfall[code] = max(0, need - got)
        surplus[code] = max(0, got - need)
    return Settlement(
        required_face_cents=required,
        tendered_value_cents=credited,
        shortfall_cents=shortfall,
        surplus_cents=surplus,
    )
