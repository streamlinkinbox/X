# The Real Commodity Unit (RCU)

## A commodity-backed, digitally-verified, demurrage-bearing currency system

**Version 0.2 — design document, not a specification for launch**

---

## What this is

A monetary system in which every unit of currency is a bearer claim on a
specific, graded, inspected quantity of a real commodity held in a licensed
warehouse. Notes carry a cryptographic identity that any phone can verify.
Notes backed by perishable goods lose value on a published schedule, so
holding them is costly and spending them is not. Notes backed by durable
goods hold their face value and pay a custody fee instead.

Issuance is decentralised across producer cooperatives. There is no central
bank and no discretionary money creation: currency enters circulation only
when a commodity is deposited and verified, and leaves when the commodity is
withdrawn.

## What problem it solves

The founding observation is precise and correct: **in much of rural East
Africa, wealth exists but does not circulate.** A farmer with eight tonnes of
maize in a store is wealthy in goods and destitute in cash. She cannot pay
school fees with maize. She sells at harvest, when everyone else is selling
and the price is at its floor, and buys back at planting, when the price is at
its ceiling. The gap between those two prices is a wealth transfer from
producers to whoever holds cash. National currency is scarce in the village
precisely when goods are abundant there.

RCU attacks that mismatch directly: it turns the maize into a spendable claim
without forcing the sale, and it makes the claim uncomfortable to hoard.

## What is genuinely new here

Three things, honestly assessed:

1. **Class-specific demurrage tied to physical spoilage.** Historical
   demurrage currencies (Wörgl, Chiemgauer) applied one uniform rate to a
   fiat-backed scrip. Here the decay rate of the *money* is calibrated to the
   decay rate of the *thing backing it*. That correspondence is the original
   contribution, and it is a good one: it removes the arbitrariness that made
   Gesellian demurrage feel like a tax.

2. **A two-tier system that separates medium-of-exchange from
   store-of-value by construction**, rather than hoping one instrument does
   both jobs.

3. **Warehouse receipts as bearer instruments with offline verification.**
   Warehouse receipt systems exist across East Africa and are well
   regulated. They are financing instruments, not money. Making them
   circulate hand-to-hand at retail is the leap.

## What is not new, and should not be claimed as new

Intellectual honesty is a design requirement here, not a courtesy. The
following are all prior art, and the blueprint is stronger for citing them:

- **Commodity-reserve currency**: Benjamin Graham, *Storage and Stability*
  (1937), proposed money issued against warehouse receipts for a basket of
  commodities. Milton Friedman's 1951 critique — that it would be too
  complex and costly to administer — is the single most important
  document any implementer of this system must read and answer.
- **Demurrage**: Silvio Gesell's *Freigeld*; the Wörgl experiment of
  1932–33, where 1%/month stamp scrip circulated roughly 8–14× faster than
  the national schilling before the Austrian National Bank suppressed it in
  September 1933.
- **Warehouse receipt systems**: Tanzania's Warehouse Receipts Act No. 10
  of 2005 already licenses warehouses, inspectors and collateral managers,
  and covers 18 commodities across 23 regions.
- **Digital community currency at scale**: Kenya's Sarafu network ran
  ~55,000 users and ~300 million units of transactions across 2020–21.

The correct claim is not "nobody has done this." It is: *"each component
works somewhere; the combination has not been tried; here is why the
combination might work and here is exactly how it could fail."*

## The five findings that should change the original design

These come out of the quantitative model in `model/rcu/`, not from opinion.

**1. Tier B cannot be free.** Nine of the twenty classes have zero or
near-zero demurrage but non-zero storage cost. Iron rusts, copper is stolen,
warehouses charge rent. With no demurrage to fund custody, Tier B must levy
an **explicit custody fee of 1–5%/year**, deducted in-kind or in units. A
"stable" note is stable in face value, not free to hold. Any version of this
document that omits the custody fee is promising something physically
impossible.

**2. The haircut, not the decay rate, is what keeps the system solvent.**
Notes must be issued against roughly 70% of assessed value, not 100%. Under
the original design, a 30% fall in the maize price — an ordinary event —
leaves the grain series undercollateralised and the notes trading below face.
Precious Metals at a 10% haircut survives only a 7.3% price fall against 18%
annual volatility: it is the most under-haircut class in the register despite
being the "safest" commodity.

**3. Automatic taxation and offline capability are mutually exclusive.**
This is the hardest finding and the original design does not survive it
unmodified. Tax collected at the point of sale requires that the transaction
be *seen*. An offline transaction is not seen. A system that is genuinely
offline-capable cannot also guarantee that no transaction escapes taxation.
Section 5 resolves this by moving taxation from the transaction to the
**issuance and redemption gates**, which are always online, always at a
fixed location, and always supervised. That is a better design anyway: it
taxes at two chokepoints instead of surveilling a whole economy.

**4. "Impossible to counterfeit" is not achievable and should not be
printed on the note.** A QR code is a photograph; anyone can copy it. What
the digital layer actually prevents is *double-spending of a verified note
against an online ledger* and *forgery of the ledger record*. A cloned note
passed offline in a market will be caught only at the next sync — and by
then the fraudster is gone. The mitigations are holding limits, offline
transaction-count caps, and secure elements, all of which are covered in
Section 5. The claim must be downgraded from "impossible" to "detectable,
bounded, and insurable."

**5. A single-crop cooperative cannot supply a stable money.** Modelled over
48 months, a grain cooperative issuing once a year produces a money supply
that swings from zero to full and back within each year. The region gets a
liquidity drought every lean season — precisely when people need credit
most. **Issuance must be pooled across commodities with differently-timed
harvests**, or the currency will fail at exactly the moment it is most
needed.

## What this system cannot do

Stated plainly, because a blueprint that only lists strengths is marketing:

- **It cannot back imports.** No foreign supplier accepts maize-backed notes
  for fuel, medicine or machinery. RCU is a domestic circulation instrument
  and the region still needs foreign exchange for everything it does not
  produce.
- **It cannot be made non-political.** A parallel currency that succeeds
  becomes a fiscal and monetary fact, and the central bank will treat it as
  one. Wörgl was suppressed in thirteen months, at a scale of 12,000
  schillings, by a state that was not even hostile in principle.
- **It cannot eliminate trust.** It relocates trust from a central bank to a
  warehouse inspector. That is a real gain — you can walk to the warehouse —
  but the inspector can still be bribed, and collateral-management fraud is
  the best-documented failure mode in African warehouse receipt systems.
- **It cannot survive its own success without a legal identity.** At scale
  it is deposit-taking and payment-service provision. Pretending otherwise
  invites closure, not tolerance.

## Document map

| Document | Contents |
|---|---|
| [`01-monetary-design.md`](01-monetary-design.md) | Unit of account, the two tiers, demurrage, haircuts, the money supply problem |
| [`02-commodity-classes.md`](02-commodity-classes.md) | All 20 classes, grading, and which ones should not ship |
| [`03-issuance-and-redemption.md`](03-issuance-and-redemption.md) | Deposit, inspection, issuance, re-inspection, retirement, the redemption gate |
| [`04-note-design.md`](04-note-design.md) | Physical note, security features, what may and may not be printed |
| [`05-technical-architecture.md`](05-technical-architecture.md) | Ledger, verification, offline protocol, double-spend bounds, key management |
| [`06-governance.md`](06-governance.md) | Cooperative structure, inspector independence, dispute resolution, capture resistance |
| [`07-taxation-and-fees.md`](07-taxation-and-fees.md) | Gate-based taxation, fee schedule, why point-of-sale tax fails |
| [`08-legal-and-regulatory.md`](08-legal-and-regulatory.md) | Legal characterisation, the Tanzanian WRS route, engagement strategy |
| [`09-risk-register.md`](09-risk-register.md) | Scored risks, kill criteria, what makes us stop |
| [`10-implementation-roadmap.md`](10-implementation-roadmap.md) | Phased plan with falsifiable gates |
| [`11-prior-art.md`](11-prior-art.md) | Graham, Gesell, Wörgl, Sarafu, WRS — what each teaches |
| [`annex-a-parameters.md`](annex-a-parameters.md) | Generated tables: all parameters and stress results |
| [`annex-b-open-problems.md`](annex-b-open-problems.md) | Unsolved problems, ranked by how badly they hurt |

The parameter model and stress tests live in [`model/rcu/`](../model/rcu/);
run `make tables` to regenerate Annex A, `make test` to check the arithmetic.
