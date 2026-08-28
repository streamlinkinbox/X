"""Does bundle pricing defeat demurrage arbitrage?

Annex B problem P1 identified a potentially fatal flaw: with a free choice of
payment medium, sophisticated holders keep Tier B (stable) notes and spend
Tier A (decaying) notes. Demurrage then falls entirely on the unsophisticated,
inverting the design's purpose.

The proposed fix is that sellers quote in *bundles* -- "100 iron + 500 wood +
40 plastic" -- rather than in a single fungible amount. If a seller demands
specific decaying classes, a hoarder cannot pay using only stable notes. They
must acquire and part with Tier A notes, and to acquire them they must have
recently sold something. Hoarding stops being free.

This module tests whether that actually holds, and finds the conditions under
which it does not.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from decimal import Decimal

from .classes import REGISTER, TIER_A, TIER_B, Tier, get
from .pricing import Bundle, bundle_tier_split
from .valuation import decay_multiplier


@dataclass
class Holder:
    """An agent holding notes of various classes, by face value in units."""

    name: str
    sophisticated: bool
    holdings: dict[str, float] = field(default_factory=dict)
    #: age in months of the notes held, per class (simplified: one cohort each)
    ages: dict[str, int] = field(default_factory=dict)

    def face(self) -> float:
        return sum(self.holdings.values())

    def value(self) -> float:
        """Current decayed value of everything held."""
        tot = 0.0
        for code, units in self.holdings.items():
            cls = get(code)
            age = self.ages.get(code, 0)
            tot += units * float(decay_multiplier(cls, age))
        return tot

    def tier_a_share(self) -> float:
        t = self.face()
        if t == 0:
            return 0.0
        a = sum(u for c, u in self.holdings.items() if get(c).tier is Tier.A)
        return a / t


def _pay(holder: Holder, demand: Bundle, strict: bool) -> tuple[bool, float]:
    """Attempt to pay a bundle demand.

    Returns (paid, decay_loss_borne). Under ``strict`` bundle rules the payer
    must tender the specific classes demanded. Under non-strict rules (the
    original design) any class may substitute, and a sophisticated payer will
    always substitute the most-decayed Tier A note they hold.
    """
    if strict:
        for code, units in demand.items():
            if holder.holdings.get(code, 0.0) < units:
                return False, 0.0
        loss = 0.0
        for code, units in demand.items():
            cls = get(code)
            age = holder.ages.get(code, 0)
            loss += units * (1.0 - float(decay_multiplier(cls, age)))
            holder.holdings[code] -= units
        return True, loss

    # Non-strict: pay total value using whatever is cheapest to give up.
    need = float(sum(demand.values()))
    order = sorted(
        holder.holdings,
        key=lambda c: -(1.0 - float(decay_multiplier(get(c), holder.ages.get(c, 0)))),
    ) if holder.sophisticated else list(holder.holdings)
    loss = 0.0
    for code in order:
        if need <= 0:
            break
        cls = get(code)
        age = holder.ages.get(code, 0)
        mult = float(decay_multiplier(cls, age))
        avail = holder.holdings[code]
        spend_face = min(avail, need / mult if mult > 0 else avail)
        holder.holdings[code] -= spend_face
        need -= spend_face * mult
        loss += spend_face * (1.0 - mult)
    return need <= 1e-6, loss


@dataclass
class SimResult:
    strict: bool
    months: int
    sophisticated_loss: float
    naive_loss: float
    sophisticated_tier_a_share: float
    naive_tier_a_share: float

    @property
    def loss_ratio(self) -> float:
        """Naive loss / sophisticated loss.

        1.0 means demurrage is borne equally. Large values mean the
        unsophisticated are carrying the burden -- the P1 inversion.
        """
        if self.sophisticated_loss <= 1e-9:
            return float("inf")
        return self.naive_loss / self.sophisticated_loss


def simulate(
    strict: bool,
    months: int = 24,
    tier_a_demand_share: float = 0.5,
    seed: int = 7,
    endowment: float = 1000.0,
) -> SimResult:
    """Run a two-agent market under strict or free-substitution payment rules.

    Both agents start with identical holdings and face identical payment
    demands. The only difference is that the sophisticated agent chooses
    which notes to part with, when the rules allow choosing.
    """
    rng = random.Random(seed)
    a_codes = [c.code for c in TIER_A]
    b_codes = [c.code for c in TIER_B]

    def fresh() -> dict[str, float]:
        h = {}
        per_a = endowment * tier_a_demand_share / len(a_codes)
        per_b = endowment * (1 - tier_a_demand_share) / len(b_codes)
        for c in a_codes:
            h[c] = per_a
        for c in b_codes:
            h[c] = per_b
        return h

    soph = Holder("sophisticated", True, fresh(), {})
    naive = Holder("naive", False, fresh(), {})

    soph_loss = naive_loss = 0.0

    for m in range(months):
        # Everything ages a month.
        for h in (soph, naive):
            for c in list(h.holdings):
                h.ages[c] = h.ages.get(c, 0) + 1

        # A payment demand arrives: a bundle mixing Tier A and Tier B.
        n_a = max(1, int(len(a_codes) * 0.3))
        n_b = max(1, int(len(b_codes) * 0.3))
        demand: Bundle = {}
        for c in rng.sample(a_codes, n_a):
            demand[c] = int(20 * tier_a_demand_share) or 1
        for c in rng.sample(b_codes, n_b):
            demand[c] = int(20 * (1 - tier_a_demand_share)) or 1

        for h, acc in ((soph, "s"), (naive, "n")):
            ok, loss = _pay(h, demand, strict)
            if not ok:
                # Cannot pay in the demanded classes: must acquire them by
                # selling goods, which means re-entering circulation. Model
                # this as receiving fresh notes of the demanded classes.
                for code, units in demand.items():
                    h.holdings[code] = h.holdings.get(code, 0.0) + units
                    h.ages[code] = 0
                ok, loss = _pay(h, demand, strict)
            if acc == "s":
                soph_loss += loss
            else:
                naive_loss += loss

    return SimResult(
        strict=strict,
        months=months,
        sophisticated_loss=soph_loss,
        naive_loss=naive_loss,
        sophisticated_tier_a_share=soph.tier_a_share(),
        naive_tier_a_share=naive.tier_a_share(),
    )


def minimum_tier_a_share_for_fairness(
    target_ratio: float = 1.25, months: int = 24
) -> float:
    """Smallest Tier A share of quoted bundles that keeps burden roughly even.

    Below this share, bundle pricing does not bind: there is enough Tier B in
    the demand that a hoarder can still avoid holding decaying notes.
    """
    for pct in range(5, 100, 5):
        r = simulate(strict=True, months=months, tier_a_demand_share=pct / 100)
        if r.loss_ratio <= target_ratio:
            return pct / 100
    return 1.0
