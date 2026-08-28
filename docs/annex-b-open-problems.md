# Annex B — Open problems

Ranked by how much damage they do if unsolved. Problems 1–3 are, in the
author's assessment, **potentially fatal to the design as specified.** They
should be worked on before anything else, and they should be worked on by
people who are trying to break the system rather than defend it.

---

## P1. Demurrage arbitrage inverts the design's purpose

**Severity: potentially fatal. No clean solution known.**

The system offers two tiers and lets people choose which to pay with.
Anyone who understands the difference will hold Tier B and spend Tier A.

Consider a market. A sophisticated trader holds iron notes (stable) and grain
notes (decaying). She pays for everything in grain notes and accumulates iron
notes. Her less sophisticated counterparties do the reverse without realising
it. Over time:

- The wealthy and informed hold the stable notes
- The poor and uninformed hold the decaying notes
- **Demurrage becomes a regressive tax on financial illiteracy**

This is a precise inversion of the stated purpose. The design intends
demurrage to prevent the rich from hoarding. It may instead ensure the poor
bear all of it, because the rich simply hold the other tier.

### Why the obvious fixes fail

| Fix | Why it fails |
|---|---|
| Mandate a Tier A share in payments | Unenforceable in cash transactions; invites side-payment workarounds |
| Cap Tier B holdings per person | Trivially evaded through nominees |
| Apply demurrage to Tier B too | Then Tier B is not a store of value and the two-tier design collapses |
| Educate everyone | Optimistic; and asymmetric information is the normal state of markets |
| Price Tier A at a market discount | This already happens implicitly — and the discount is borne by whoever is least able to negotiate |

### The least-bad option

Accept the arbitrage but **compress the gap**: keep Tier A demurrage low
(1–2%/month, not 5%) and charge Tier B a custody fee that is genuinely
material (2–4%/year, not 1%). If holding Tier B costs 3%/year and Tier A
costs 12%/year, the arbitrage exists but is worth less than the effort of
exploiting it for small traders.

**This is mitigation, not solution.** It should be stated as such, and
measured directly in Phase 2 by tracking the Tier A/B holdings split against
wealth quintile.

---

## P2. The seasonal money supply problem

**Severity: potentially fatal in single-crop regions. Partial solutions
exist.**

Covered in Section 1.5. Restated here because it is unsolved.

A commodity-backed money supply tracks commodity production. In a
single-harvest region that means the money supply collapses in the lean
season — exactly when households have no food stock, no cash, and the
greatest need for a medium of exchange.

**Cross-commodity pooling is the main hope**, and it is untested. It also
requires launching several classes at once, which conflicts with the
prudent recommendation of a single-class pilot. That conflict is real and
this document does not resolve it: Phase 1 chooses prudence, and therefore
Phase 1 *cannot* test the fix for the most serious economic problem in the
design. Phase 2 must be explicitly designed as the test.

**The deeper question nobody has answered:** is a seasonal money supply
actually bad, if the real economy is seasonal? Perhaps money *should*
contract when there is less to trade. The counter-argument is that the lean
season is precisely when consumption smoothing matters most, and a currency
that vanishes then has failed at the one job that would justify it.

This deserves proper economic modelling. It has not received it here.

---

## P3. Adoption bootstrap

**Severity: most likely cause of death. Known playbook, no guarantees.**

No currency has value until others accept it, and on day one nobody does.
Section 9.2 gives the standard playbook — anchor acceptors, issuer
acceptance for fees, density over breadth. Wörgl's evidence says the single
most important element is that **the issuer accepts its own currency for
obligations people already owe.**

**The unresolved part:** RCU's issuer is a cooperative, not a municipality.
Cooperative fees are a much smaller and more avoidable obligation than
taxes. The demand anchor is correspondingly weaker than Wörgl's, and Wörgl
still needed thirteen months and a depression to reach scale.

**Untested idea worth exploring:** persuade the district authority to accept
RCU for market stall fees, water charges or school fees before launch.
This would replicate Wörgl's mechanism almost exactly. It requires political
work in Phase 0, not technical work, and it may be the single highest-value
action available.

---

## P4. Price discovery without a market

**Severity: high. Solvable with effort.**

Issuance requires knowing what a tonne of maize is worth. In a thin rural
market, that price is whatever the two or three local buyers say it is —
and those buyers are the parties whose market power the system exists to
counteract.

Using their prices to set issuance means the system inherits the distortion
it was built to fix.

**Partial answers:** triangulate against the nearest commodity exchange
quote; use rolling averages of actual redemption transactions; publish
prices weekly and openly so that manipulation is visible; and over time let
the system's own redemption prices become the reference. The last is a
bootstrapping problem — it works only once there is enough volume.

---

## P5. Cost of carry versus the value of the currency

**Severity: high. Structural.**

Grain storage costs about 7% per year (Section 11.1). Sand and gravel have
low value density — storing 100 RCU of sand costs far more than storing 100
RCU of gold.

**Implication:** low-value-density classes are structurally uneconomic to
monetise. The custody fee needed to cover storage would exceed what anyone
would pay to hold the note.

The model does not currently compute value density per class, and it should.
**Recommended addition:** a `value_per_m3` field, with an exclusion rule for
any class whose storage cost exceeds ~6%/year of stored value.

This probably disqualifies Construction Materials (sand, gravel) and
possibly Stone — two classes the original blueprint treats as bedrock Tier B.

---

## P6. What happens when a cooperative fails

**Severity: high. Underspecified.**

Section 3.2 gives a loss waterfall for collateral shortfalls. It does not
address the failure of an entire cooperative — fraud, insolvency, or
abandonment.

Open questions:
- Who honours the notes? The federation? With what assets?
- Is there mutual liability between cooperatives? If yes, one bad
  cooperative can drag down good ones. If no, the notes of a failed
  cooperative are worthless and the whole system's credibility suffers
  anyway.
- Who administers the wind-down?
- Can a cooperative leave the federation voluntarily while notes are
  outstanding?

**Recommendation:** a federation resolution fund, capitalised at 5% of
system-wide outstanding, with pre-agreed resolution authority. Without this,
the first cooperative failure becomes a system-wide run.

---

## P7. Offline transaction limits are unenforceable in software

**Severity: medium. Bounded by design.**

Section 5.5 sets offline holding limits and hop caps, enforced by the app.
A modified app can ignore them. Only secure hardware enforces limits
reliably, and secure hardware is Phase 3.

This is an accepted, bounded risk. It is listed here because the bound
depends on the insurance pool being adequately funded, and the pool's
sizing has not been modelled. **Recommended: model expected fraud loss as a
function of offline limits and fund the pool at 3× the modelled 99th
percentile.**

---

## P8. Livestock is a different instrument

**Severity: medium. Solvable, but requires separate design.**

Section 2.3 explains why. Live animals appreciate while growing, die
stochastically, require feeding, and can be substituted. Exponential decay
from a fixed grace period models none of that.

Livestock is economically the most important class for many pastoralist
communities, so "exclude it" is a real cost. It needs its own design
document, not a row in a table.

---

## P9. No positive-yield instrument exists

**Severity: medium. Possibly inherent.**

Every RCU instrument loses value: Tier A through demurrage, Tier B through
custody fees. There is nothing that grows.

For a circulation medium this is fine and intended. For a household saving
for a roof, a dowry or old age, it means RCU is never the right vehicle.
They will save in cattle, iron sheets, or shillings.

Is that acceptable? Probably — money need not be an investment. But it
means **RCU can never be the only financial instrument in the community**,
and any claim that it provides "intergenerational wealth" (as the original
Tier B rationale does) is false. Tier B is a *less-bad* store of value than
an inflating national currency, not a good one.

---

## P10. Measuring whether it actually helped

**Severity: medium. Methodologically hard.**

The purpose is to make producers better off. Proving that requires
counterfactuals, and a currency system cannot be randomised across a market
the way a cash transfer can — the whole point is network effects, which
violate the independence assumption underlying most impact evaluation.

Sarafu's RCT managed it by randomising *individual enrolment*, which works
for a voucher but not for a currency whose value depends on density.

**Recommended:** staggered rollout across markets, with markets as the unit
of randomisation, and a pre-registered analysis plan. Expensive, and the
only credible route.

---

## Summary

| # | Problem | Severity | Status |
|---|---|---|---|
| P1 | Demurrage arbitrage | Potentially fatal | Mitigation only |
| P2 | Seasonal money supply | Potentially fatal | Partial, untested |
| P3 | Adoption bootstrap | Most likely killer | Playbook exists |
| P4 | Price discovery | High | Solvable |
| P5 | Cost of carry vs. value density | High | Needs modelling |
| P6 | Cooperative failure | High | Underspecified |
| P7 | Offline limit enforcement | Medium | Bounded, needs sizing |
| P8 | Livestock instrument | Medium | Needs separate design |
| P9 | No positive yield | Medium | Possibly inherent |
| P10 | Impact measurement | Medium | Methodologically hard |

**The three at the top are not reasons to abandon the design.** They are the
reasons a pilot exists — and a pilot that is not explicitly built to test
P1, P2 and P3 will produce encouraging numbers that mean nothing.
