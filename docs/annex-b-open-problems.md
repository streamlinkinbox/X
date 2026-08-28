# Annex B — Open problems

Ranked by how much damage they do if unsolved. Problems 1–3 are, in the
author's assessment, **potentially fatal to the design as specified.** They
should be worked on before anything else, and they should be worked on by
people who are trying to break the system rather than defend it.

---

## P1. Demurrage arbitrage inverts the design's purpose

**Severity: was potentially fatal. SOLVED by bundle pricing (§12.3),
conditional on near-universal adoption.**

> **Resolution.** Quoting prices as bundles of specific commodity classes
> rather than as a single fungible amount removes the payer's ability to
> choose which notes to part with. Modelled over 24 months, the burden ratio
> between a sophisticated and a naive holder falls from **2.16 to 1.00**.
>
> **The condition is strict and non-obvious: partial adoption is worse than
> none.** At 25% of sellers insisting on exact bundles the ratio rises to
> **2.41**, because hoarders route around the minority of strict sellers and
> concentrate their decayed notes on the flexible majority. Bundle pricing
> must be the launch default and near-universal, or it must not be
> introduced. See §12.3.
>
> The original analysis is retained below because the failure mode returns
> immediately if bundle pricing lapses.

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

### The least-bad option *without* bundle pricing

Accept the arbitrage but **compress the gap**: keep Tier A demurrage low
(1–2%/month, not 5%) and charge Tier B a custody fee that is genuinely
material (2–4%/year, not 1%). If holding Tier B costs 3%/year and Tier A
costs 12%/year, the arbitrage exists but is worth less than the effort of
exploiting it for small traders.

This remains the correct fallback if bundle pricing fails to become the
market convention. It should still be measured directly in Phase 2 by
tracking the Tier A/B holdings split against wealth quintile — that metric
is now the early warning that bundle adoption is slipping.

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

**Sharpened by §14.2.** A common organising instinct is to build a tight core
of 10-15 committed people and treat that as the movement. For a currency this
is arithmetically insufficient: a 15-person cadre is 60% of the traders only
in a market of roughly 312 adults, too small to sustain a warehouse. The cadre
is the engine; the acceptor network is the product. Effort must be split
accordingly, and the acceptor count tracked separately from cadre size.

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

**Severity: was high (raised). LARGELY DISSOLVED by weight denomination
(§13). Survives only for unique goods.**

> **Resolution.** The problem existed because issuance required somebody to
> decide what a tonne of maize was worth, and in a thin market that somebody
> was either a capturable committee or the very buyers whose market power the
> system exists to counteract.
>
> Weight denomination removes the question. A note claims 100 kg of maize,
> not 100 units of value, so **issuance requires a scale rather than a
> price.** Prices are left entirely to buyer and seller, and the system
> publishes observed trade rates rather than assessments.
>
> What survives: unique goods (houses, land, custom work) still have no
> reliable reference, so the confidence grading in §12.2 remains necessary
> there. And grading — "is this Grade A or B?" — remains a human judgement,
> though a far more constrained one than pricing.
>
> The original analysis is retained below.

**Original severity: high. Solvable with effort.**

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

**Severity raised by the dual-price receipt (§12.2).** Reference prices were
previously used only to set issuance, where a haircut absorbs error. They are
now printed on every receipt as the buyer's fairness benchmark, which makes
them load-bearing for consumer protection and a much richer target for
capture. A committee that inflates reference prices makes every seller look
honest; one that deflates them makes every seller look like a thief.

Two additional requirements follow: reference prices must carry a
**confidence grade** (high / medium / low) so that unique goods such as
houses are not given false precision, and the **method must be published**
alongside the numbers so that manipulation is detectable by anyone who cares
to check.

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

## P11. No common unit of account

**Severity: high. Introduced by weight denomination (§13.6). Untested.**

Weight denomination removes the price committee, and with it the common
measure. An economy of 20 goods has **190 bilateral exchange rates** instead
of 20 prices. This is the textbook argument for money, and the design has
deliberately walked back into it.

Three mitigations, none proven:

1. **A numéraire will emerge spontaneously.** Markets converge on a reference
   good without being told to. Iron scores best for a rural East African
   market: stable, wanted by everyone, cheap to store, divisible, verifiable
   with a scale and a magnet.
2. **The app carries the load**, showing observed trade ranges for any pair.
3. **Printed rate boards** at the market for those without phones.

**The unresolved risk is usability.** A currency that needs a smartphone to
answer "how much maize for a hoe?" excludes the people it is for. It is
entirely possible that weight denomination is monetarily elegant and
practically unusable.

**Phase 1 must test this directly:** time a typical negotiation against the
shilling equivalent, and watch whether traders spontaneously adopt a
reference good. If the market insists on a single number, the fallback is to
let iron units serve openly as the accounting unit — preserving the
anti-capture property, since nobody sets iron's value, it is just 1 kg of
iron.

---

## P12. Building an acceptor network, not just a cadre

**Severity: high. Introduced by §14. Playbook partial.**

Organising method is well understood for building a small trusted core:
referral, observed action, graduated tests. It is much less understood for
the thing a currency actually needs, which is **several hundred traders who
find the money useful.**

Those require different things. A cadre member needs to be trustworthy with
keys and risk. A trader needs only to believe the note is verifiable and that
her customers will take it. **The second is a product problem, not a loyalty
problem** — and the blueprint's technical apparatus exists precisely so that
strangers can transact without trusting each other.

Unresolved: nobody has demonstrated a reliable method for moving from a
15-person core to a 200-trader acceptance base in a low-trust rural market.
Sarafu's network analysis suggests the answer involves **closed transaction
cycles** rather than raw counts, which is measurable but not yet a recipe.

---

## P13. Scarce services cannot be monetised

**Severity: high. Introduced by §15. Structurally unsolvable as a currency.**

A service credit is a claim on a future hour of a living person. Unlike a
commodity note, the backing does not survive the institution, cannot be
inspected before it exists, is not storable, and **can emigrate**.

For abundant labour this is manageable. For scarce specialists it is fatal:
at one doctor per 25,000 people, doctor-hour credits cover **6.4%** of demand
and represent a 15-year queue. Worse, need is inversely related to earning
capacity, so a care currency charges the sick most at the moment they can
produce least -- the documented failure of Japan's Fureai Kippu.

**Not solvable by better design.** The blueprint's answer is to stop trying:
use risk-pooling (a commodity-backed health fund) for scarce care, credits
only for abundant labour, and training bonds to reduce the scarcity itself.

What remains genuinely open: **roughly 40% of the cost of care -- consumables,
drugs, equipment -- must be bought abroad and cannot be met by any local
currency.** No design in this document solves that. It requires exports or
external finance.

---

## P14. The irreducible import floor

**Severity: high. Structural. Partially mitigable, never solvable.**

About **51%** of a district's import bill can realistically be localised. The
remainder -- roughly **$227,000/year** in the modelled basket -- cannot be, at
any plausible level of local investment.

The composition is what makes this serious. What cannot be localised is
disproportionately what cannot be skipped: medicines, vaccines and active
pharmaceutical ingredients, where Africa imports 95-99% of medicines and close
to 100% of APIs. Substitution payback for medicines is on the order of **200
years**; for vaccines it is effectively never.

**Partially resolved by §17.** The original analysis treated "medicines" as
one category, which was too coarse. Disaggregated by technical difficulty,
**two lethal-category goods are locally producible today**: medical oxygen
from air (PSA plants proven at district scale in Kenya, Rwanda and Ethiopia
at roughly USD 100-110k and ~USD 7.34 per patient treated) and oral
rehydration salts from sugar and salt. Achievable independence rises from
~51% to ~60%.

**What remains irreducible:** active pharmaceutical ingredients, vaccines,
sterile IV production, and precision equipment. These sit on rung 5 of the
production ladder and are national or continental projects, not district
ones.

**Mitigation for the remainder:** severity-weighted physical buffers (§16.3),
supplier diversification across regions, constitutional FX triage, and
localising the *easy* categories so that foreign exchange is always available
for the impossible ones.

**What remains open:** the community must earn hard currency indefinitely.
If export earnings collapse -- a commodity price fall, a trade route closing,
a sanction -- no monetary design in this document prevents the lethal basket
from lapsing. This is the hardest external constraint on the entire project
and it has no internal answer.

---

## P15. Asymmetric defense escalation, standoff strikes, and adversary adaptation

**Severity: high. Inherent to asymmetric defense.**

The citizen militia doctrine (§19) proves that high-tech assets (tanks, stealth
aircraft, drone swarms) can be neutralized at 10,000:1+ cost ratios during
ground operations. However, an industrialized adversary facing low-cost ground
neutralization will adapt its doctrine in two specific ways:

1. **Standoff kinetic bombardment:** Transitioning from ground assault to
   high-altitude standoff glide bombs, long-range cruise missiles, and heavy
   artillery fired from beyond visual and militia range.
2. **Technological adaptation:** Fitting tanks with cope cages and thermal
   blaster sensors, and equipping drone swarms with dynamic frequency-hopping
   and fiber-optic tethering immune to RF jamming.

**Mitigation:**
- Subterranean infrastructure: Hardening warehouses, medical clinics, and
  command nodes beneath 3+ meters of reinforced earth.
- Signature reduction: Complete dispersal into civilian fabric (the Ghost
  doctrine) where standoff strikes inflict unacceptable collateral damage.
- Political exhaustion: Escalating the adversary's financial and moral costs
  per day until domestic political support collapses.

**What remains open:** A determined adversary willing to use scorched-earth
tactics or indiscriminate standoff shelling cannot be stopped by kinetic
neutralization alone. Asymmetric victory remains fundamentally **political**,
not purely military.

---

## P16. Peer selection cartels and guild conservatism

**Severity: medium-high. Governance vulnerability.**

While peer selection by senior masters (§20.2) eliminates electoral popularity
contests, it introduces a classic institutional vulnerability: **senior guild
insularity and mutual protection cartels.** Senior practitioners may favor
conservative candidates identical to themselves, resist disruptive technical
innovations, or form quiet non-aggression pacts during peer evaluations.

**Mitigation:**
- **Objective ledger qualification (Stage 1):** Metrics cannot be bypassed; a
  candidate must meet hard output tonnage, project completion, and clean record
  thresholds before peer voting occurs.
- **Sortition jury oversight (Stage 4):** Annual 20-citizen audits by lottery
  maintain full subpoena authority over all appointment logs and department
  telemetry.
- **1-Year quantitative probation (Stage 3):** If a confirmed crony fails hard
  KPI targets, replacement is automatic and non-negotiable.

---

## P17. Cross-regional comparative benchmarking data reliability

**Severity: medium. Diagnostic vulnerability.**

The difficulty-adjusted evaluation framework (§21.1) relies on comparing a
community's harvest, public health, or storage losses against neighboring
districts under identical climatic/blockade stress. However, in low-trust or
adversarial regional environments, neighboring authorities may falsify their
loss figures, conceal epidemics, or manipulate grain yields, distorting the
comparative baseline.

**Mitigation:**
- **Physical satellite & weather telemetry:** Rely on objective precipitation,
  soil moisture, and vegetation index (NDVI) data rather than self-reported
  foreign claims.
- **Cross-district forensic inspectors:** Independent federation auditors (§6.4)
  verify physical stock levels across federated regions.
- **Internal multi-year historical baseline:** Evaluate performance against
  multi-decade historical local performance during past climate shocks.

---

## P18. Epistemic capture and analyst bias in central intelligence synthesis

**Severity: medium-high. Analytical vulnerability.**

Because the Research & Analysis Bureau (§22) sits at the nexus of all
departmental data streams, it risks developing **technocratic insularity,
confirmation bias, or analytical capture.** If a small clique of senior analysts
develops dogmatic statistical models or quietly favors specific guild factions,
their reports could misdiagnose crises or suppress unconventional grassroots
solutions.

**Mitigation:**
- **Zero enforcement power (§22.2):** The RAB can only recommend and alert; it
  cannot enforce decrees, execute arrests, or block council deliberations.
- **Radical public open data:** All raw data and analytical models are public,
  enabling independent guild masters, apprentices, and citizens to audit RAB code
  and replicate findings.
- **2-Year leadership rotation & 5-Year analyst term limits:** Mandatory return
  to physical guild production prevents the formation of an entrenched
  technocratic class.
- **Annual external peer audit:** Independent analytical teams from federated
  districts audit methodologies, algorithms, and investigative accuracy.

---

## Summary

| # | Problem | Severity | Status |
|---|---|---|---|
| P1 | Demurrage arbitrage | ~~Potentially fatal~~ | **Solved** by bundle pricing (§12.3), if adoption is near-universal |
| P2 | Seasonal money supply | Potentially fatal | Partial, untested |
| P3 | Adoption bootstrap | Most likely killer | Playbook exists |
| P4 | Price discovery | ~~High~~ | **Largely dissolved** by weight denomination (§13); survives for unique goods |
| P5 | Cost of carry vs. value density | High | Needs modelling |
| P6 | Cooperative failure | High | Underspecified |
| P7 | Offline limit enforcement | Medium | Bounded, needs sizing |
| P8 | Livestock instrument | Medium | Needs separate design |
| P9 | No positive yield | Medium | Possibly inherent |
| P10 | Impact measurement | Medium | Methodologically hard |
| P11 | No common unit of account | **High (new)** | Mitigations untested; Phase 1 must measure |
| P12 | Recruiting the acceptor network, not just a cadre | **High (new)** | §14.2 gives the arithmetic; no proven playbook at scale |
| P13 | Scarce services cannot be monetised | **High (new)** | Structural; use pooling not credits. FX gap for consumables unsolved |
| P14 | Irreducible import floor | **High** | Reduced from ~49% to ~40% by §17 production ladder; APIs and vaccines permanent |
| P15 | Asymmetric defense escalation and adaptation | **High (new)** | Subterranean hardening + Ghost doctrine; political exhaustion is required |
| P16 | Peer selection cartels and guild conservatism | **Medium-High (new)** | Mitigated by objective ledger filters, 1-yr probation, and sortition juries |
| P17 | Cross-regional comparative benchmarking data reliability | **Medium (new)** | Satellite/NDVI telemetry + multi-year local baseline calibration |
| P18 | Epistemic capture and analyst bias in central intelligence | **Medium-High (new)** | Open data + 2-yr rotation + 5-yr analyst term limits + external audits |

**The three at the top are not reasons to abandon the design.** They are the
reasons a pilot exists — and a pilot that is not explicitly built to test
P1, P2 and P3 will produce encouraging numbers that mean nothing.
