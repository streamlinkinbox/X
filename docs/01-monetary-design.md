# 1. Monetary design

## 1.1 The unit of account

> **SUPERSEDED BY §13.** This section described a basket-based value unit,
> which required a committee to price deposits. The system is now
> **weight-denominated**: a note is a claim on a physical quantity ("100 kg
> maize, Grade A"), prices are whatever buyer and seller agree, and no
> institution sets value. The material below is retained because the
> reasoning about pegs and basket construction still applies if a value unit
> is ever reintroduced, and because §13.6 explains what is lost by dropping
> it.


The Real Commodity Unit (RCU) is defined as **the value of a fixed reference
basket of locally-produced goods**, fixed at launch and revised only by
supermajority of the issuing federation.

A worked reference basket for a maize-belt pilot:

| Component | Quantity | Weight |
|---|---|---|
| Grade A maize | 1.0 kg | 40% |
| Firewood/briquette equivalent | 1.0 kg | 15% |
| Construction sand | 5.0 kg | 10% |
| Unskilled labour | 0.05 hour | 25% |
| Cooking oil | 0.05 litre | 10% |

**1 RCU ≈ the price of that basket at launch.** If the basket costs 1,200
Tanzanian shillings on day one, then 1 RCU ≈ 1,200 TZS on day one — and
thereafter the two float apart, which is the point.

### Why not peg to the shilling or the dollar?

A peg requires a defence fund. Defending a peg means holding foreign
currency, which means the system needs exactly the thing it was designed to
live without. Sarafu, a pegged community currency, is anchored to the
Kenyan shilling and backed via mobile money precisely because the peg has to
be defensible — and that anchoring is also why researchers found users
treated it as an *inferior substitute*, transitional rather than permanent.

An unpegged basket unit is harder to explain and harder to trust at the
start. But it means a shilling devaluation does not devalue the village's
money, which is the entire strategic point.

### Why include labour in the basket?

Labour is the one "commodity" every household holds and can never be
excluded from. Anchoring 25% of the unit to a day's unskilled wage means
that if the currency drifts, it drifts *with* local earning power. It also
gives the unit meaning to a person who owns no commodity at all.

### The uncomfortable property of a basket unit

Prices quoted in RCU will look unstable to anyone who thinks in shillings.
The market woman does not care about basket theory; she cares that a bag of
rice cost 40 units last month and 44 this month. **Expect the first year to
be dominated by dual pricing**, with shillings as the mental reference and
RCU as the settlement medium. That is not a failure; it is how every
successful parallel currency has started.

---

## 1.2 The two tiers

### Tier A — demurrage-bearing

Backed by goods that physically degrade. After a grace period, the note's
transferable value falls on a published monthly schedule.

**The rule that makes this defensible:** demurrage is not a tax and not a
behavioural nudge. It is *an honest accounting of a physical fact.* The
maize behind the note really is disappearing. A note that held its face
value while its collateral rotted would be a lie, and the lie would be
discovered at redemption.

This reframing matters enormously for adoption. "Your money shrinks to force
you to spend it" is a hard sell and sounds punitive. "Your note shrinks
because the maize behind it shrinks, and here is the inspection report" is
merely true.

### Tier B — stable

Backed by goods that do not meaningfully degrade. Face value is constant,
and there is no expiry.

**The rule that makes this honest:** stability is not free. Storage costs
money whether or not the commodity decays. Tier B therefore charges an
explicit **custody fee**, levied monthly against the holder's account
balance or deducted at redemption.

From the model (Annex A.2), **nine of twenty classes have storage costs not
covered by demurrage**:

| Class | Demurrage/yr | Storage/yr | Custody fee required |
|---|---|---|---|
| Iron & Steel | 0% | 2.00% | 2.00% |
| Copper & Aluminium | 0% | 3.00% | 3.00% |
| Construction Materials | 0% | 2.00% | 2.00% |
| Precious Metals | 0% | 1.00% | 1.00% |
| Strategic Minerals | 0% | 2.00% | 2.00% |
| Ceramics & Glass | 0% | 4.00% | 4.00% |
| Salt & Chemicals | 0.50% | 5.00% | 4.50% |
| Stone & Marble | 0% | 1.00% | 1.00% |
| Processed Rubber | 0.50% | 3.00% | 2.50% |

This is not a flaw in the idea; it is the idea's true cost surfacing. **A
gold-backed note that costs 1%/year to hold is exactly what a gold-backed
note has always cost** — vaults charge rent. The original blueprint's
promise that Tier B "holds value indefinitely at no cost" is the one claim
in it that is physically impossible.

### What makes the two-tier split safe

A two-tier system with a free choice of payment medium is dangerous: anyone
who understands the difference holds Tier B and spends Tier A, so demurrage
lands on the unsophisticated. This is Annex B's problem P1, and it was
originally rated potentially fatal.

**Bundle pricing (§12) is what makes the split safe.** When sellers quote in
specific classes rather than a single fungible amount, the payer cannot
choose which notes to part with, and the burden equalises. The two-tier
design should be understood as depending on that convention — it is not an
optional refinement bolted on afterwards.

### The consequence nobody likes

Tier A decays at 11–46%/year. Tier B costs 1–5%/year. **Both tiers lose
value over time.** The difference is magnitude and predictability, not
direction.

This is worth confronting head-on, because a critic will: *the system has no
positive-yield asset.* A household that wants to store value across a decade
is better off buying a cow or a roof than holding any RCU note. And that
is arguably correct and even desirable — RCU is designed to be a circulation
medium and a short-to-medium-term store, not a retirement vehicle. But it
must be said out loud, because if it is discovered rather than disclosed,
trust dies.

---

## 1.3 Demurrage mechanics

### Grace periods and why the originals were too long

The first draft gave grains a 12-month grace. Modelling shows the
consequence: with a 12-month grace and a 24-month validity, a note only
decays during the second half of its life, and most notes are redeemed or
retired before decay ever bites. The anti-hoarding mechanism never fires.

Revised grace periods are set to **roughly the point at which the physical
commodity begins measurable loss**:

| Class | Original grace | Revised | Physical justification |
|---|---|---|---|
| Grains | 12 mo | **6 mo** | Hermetic storage holds ~6 months; pest and moisture loss accelerates after |
| Fresh produce | 3 mo | **1 mo** | Unrefrigerated produce is gone in weeks |
| Dairy | 3 mo | **1 mo** | Cold-chain dependent |
| Livestock | 6 mo | **6 mo** | Retained, but see the model objection below |
| Textiles | 24 mo | **18 mo** | Baled cotton is stable; grace trimmed for circulation pressure |
| Biofuels | 6 mo | **3 mo** | Charcoal fines and moisture uptake |

### The step function

Value steps down on the monthly anniversary of issuance. It does **not**
accrue pro rata by day.

This is a deliberate usability decision. A note whose value changes daily
cannot be priced by a trader without a calculator, cannot be verified by a
device with an unreliable clock, and produces a different answer on two
phones in the same market. A monthly step is predictable, computable on
paper, and identical on every device.

Formally, for a note of face value $F$, class grace $g$ months, monthly rate
$r$, at age $m$ months:

$$V(m) = F \cdot (1-r)^{\max(0,\, m-g)}$$

with $V(m) = 0$ once $m \geq$ the class maximum validity.

All arithmetic is integer, in cents, rounded half-up, as implemented in
`model/rcu/valuation.py`. **Every device must produce a bit-identical
result**; floating-point drift between an Android phone and a POS terminal
is a settlement dispute waiting to happen.

### Worked example

A 1,000 RCU grain note, issued 1 January 2027:

| Date | Age | Value | Note |
|---|---|---|---|
| 1 Jan 2027 | 0 mo | 1,000.00 | Issued |
| 1 Jul 2027 | 6 mo | 1,000.00 | Grace ends |
| 1 Aug 2027 | 7 mo | 980.00 | First decay step |
| 1 Jan 2028 | 12 mo | 886.38 | |
| 1 Jan 2029 | 24 mo | 0.00 | Expired; residual claim only |

Holding that note for its full life costs the holder **30.5%**. Spending it
in month 3 costs nothing. That difference is the circulation incentive,
and it is large enough to matter without being confiscatory.

### Who captures the demurrage?

The value does not evaporate — it must go somewhere, and where it goes is a
political choice with real consequences:

| Recipient | Share | Rationale |
|---|---|---|
| Warehouse operator | 50% | Pays for actual storage, security, shrinkage |
| Class stabilisation fund | 30% | Buffers price falls; first loss absorber |
| Community fund | 20% | The visible public benefit that buys consent |

Publishing this split on the note itself is strongly recommended. "Where
does my lost value go?" is the first question any intelligent user asks, and
"the warehouse that is keeping your maize dry" is a satisfying answer. "We
don't say" is fatal.

---

## 1.4 The haircut: the real solvency control

> **REVISED BY §13.2.** Under weight denomination the haircut no longer
> carries price risk: a note claiming 1 kg of iron is not impaired by a fall
> in the iron price. Haircuts fall from an average of ~29.5% to **~6.9%**,
> covering only weighing error, moisture and shrinkage. The analysis below
> explains why price-risk haircuts had to be so large, which is the clearest
> argument for abandoning value denomination.

Currency is issued against **assessed value minus a haircut**, never against
full assessed value:

$$\text{issued} = \text{assessed market value} \times (1 - h)$$

The haircut absorbs three distinct risks simultaneously: price decline,
grading error, and shrinkage between inspections.

From the model (Annex A.4), the largest price fall each class can absorb
while staying fully collateralised, compared against its own annual
volatility:

| Class | Haircut | Survives fall of | Annual σ | Verdict |
|---|---|---|---|---|
| Grains | 30% | 33.5% | 35% | marginal |
| Wood & Timber | 25% | 21.1% | 20% | ok |
| Textiles | 25% | 20.3% | 25% | **under-haircut** |
| Iron & Steel | 20% | 15.2% | 25% | **under-haircut** |
| Copper & Aluminium | 20% | 12.7% | 28% | **under-haircut** |
| Precious Metals | 10% | 7.3% | 18% | **badly under-haircut** |
| Strategic Minerals | 35% | 31.0% | 45% | **under-haircut** |
| Salt & Chemicals | 30% | 19.3% | 25% | **under-haircut** |

**The counterintuitive result: the "safest" classes are the most dangerous.**
Precious metals feel like the bedrock of the system, so the instinct is to
haircut them lightly. But gold is globally priced and genuinely volatile —
an 18% annual standard deviation against a 10% haircut means a one-sigma year
breaks collateralisation. Meanwhile fresh produce, with its punitive 50%
haircut and rapid decay, is over-protected to the point of absurdity.

**Recommended revision before any issuance:** set haircut ≥ 1.5σ of the
class's annual price volatility, floor 15%. For precious metals that means
raising the haircut from 10% to at least 27% — which will be unpopular with
gold depositors and is nonetheless correct.

---

## 1.5 The money supply problem

This is the most serious unresolved design issue, and it deserves more space
than the original blueprint gave it.

### The sawtooth

Modelling a single-crop grain cooperative over 48 months (Annex A.7):
issuance spikes at harvest, then the outstanding stock decays and retires
through the year, reaching near-zero before the next harvest.

Coverage never falls below **1.38×** — the system stays solvent. But the
money supply swings from zero to full and back **every year**.

A currency that vanishes in the lean season is worthless as a currency. The
lean season is exactly when a household has no cash, no food stock, and the
greatest need for a medium of exchange. If RCU disappears then, people will
keep shillings for the lean season and use RCU only in the glut — which is
to say, it will be a harvest-marketing tool, not money.

### Three partial fixes, and their costs

**1. Cross-commodity pooling.** Combine classes whose production peaks at
different times: grain harvest in month 3, livestock offtake year-round,
timber and charcoal continuous, minerals continuous. This flattens the
aggregate curve substantially and is the primary recommendation.
*Cost:* requires several classes live simultaneously, which contradicts a
narrow, safe pilot. This is a genuine tension between prudence and function.

**2. Multi-season warehousing.** Deliberately hold part of the harvest for
release across the year rather than issuing against it all at once.
*Cost:* storage cost and shrinkage rise; the cooperative takes price risk.

**3. A stabilisation reserve that issues counter-cyclically.** The fund
holds Tier B collateral and issues against it in the lean season.
*Cost:* this is discretionary monetary policy. The system has just
reinvented a central bank, with a smaller balance sheet and less
accountability. If this route is taken, **say so plainly** rather than
pretending the system is purely rule-based.

### The honest position

**None of these fully solves it.** A regional economy with one harvest has a
seasonal real economy, and a commodity-backed money will reflect that. The
best achievable outcome is damping, not elimination. The blueprint should
promise damping.
