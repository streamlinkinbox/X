# 9. Risk register

Scored **likelihood × impact**, each 1–5. Risks scoring ≥ 15 are
project-threatening and must have an owner and a mitigation before launch.

## 9.1 Scored register

| # | Risk | L | I | Score | Mitigation | Residual |
|---|---|---|---|---|---|---|
| R1 | **Regulatory shutdown** | 4 | 5 | **20** | WRS licensing route; proactive CB engagement Yr2; no national currency accepted | 12 |
| R2 | **Adoption failure — nobody accepts it** | 4 | 5 | **20** | Anchor tenants pre-committed; pay wages in RCU; accept for cooperative fees | 10 |
| R3 | **Inspector corruption at scale** | 3 | 5 | **15** | Federation employment, rotation, variance stats, blind double grading | 8 |
| R4 | **Warehouse loss (fire, flood, theft)** | 3 | 4 | 12 | Insurance, bonds, 15% max class concentration | 6 |
| R5 | **Collateral price crash** | 4 | 3 | 12 | Haircuts ≥1.5σ, stabilisation fund, cross-class diversification | 6 |
| R6 | **Seasonal money supply collapse** | 4 | 3 | 12 | Cross-commodity pooling, multi-season release | 8 |
| R7 | **Counterfeiting at scale** | 2 | 4 | 8 | Security features, decay shelf-life, insurance pool | 4 |
| R8 | **Offline double-spend fraud** | 3 | 2 | 6 | Holding limits, hop caps, insurance | 3 |
| R9 | **Elite capture of cooperative** | 3 | 4 | 12 | Depositor caps, sortition, term limits, external audit | 8 |
| R10 | **Armed seizure of warehouse** | 2 | 5 | 10 | Dispersion, low per-site value, mutual insurance | 8 |
| R11 | **Technology failure / no phones** | 2 | 2 | 4 | Paper works standalone; USSD fallback; printed checkpoints | 2 |
| R12 | **Founder dependence / succession** | 4 | 3 | 12 | Documentation, term limits, deliberate deputy training | 6 |
| R13 | **AML/CFT designation** | 3 | 5 | **15** | Gate identity, denomination caps, proactive engagement | 9 |
| R14 | **Grading dispute cascade** | 3 | 3 | 9 | Manuals, lowest-of-three rule, dispute council | 5 |
| R15 | **Bank run / redemption gate panic** | 3 | 4 | 12 | Pro-rata gate, queue premium, gate disclosed on note | 6 |
| R16 | **Environmental harm (deforestation)** | 3 | 4 | 12 | Exclude charcoal, certified timber only | 5 |
| R17 | **Currency of the poor stigma** | 3 | 4 | 12 | Elite participation early; accepted for prestige goods | 8 |
| R18 | **Conflict-mineral / sanctions exposure** | 2 | 5 | 10 | Exclude artisanal gold and strategic minerals in Ph1–2 | 4 |
| R19 | **Partial bundle-pricing adoption** | 3 | 4 | 12 | Universal launch default; anchor acceptors commit; app quotes bundles by default | 6 |

---

## 9.2 The four risks that actually decide the outcome

Most risk registers spread attention evenly. That is a mistake. Four risks
dominate, and effort should be allocated accordingly.

### R2 — Adoption failure (score 20)

**This is the most likely way the project dies, and it is the least
discussed in the original blueprint.**

A currency is worth something only because others accept it. On day one,
nobody accepts RCU. A farmer paid in notes she cannot spend has been given
nothing — she has been made worse off than if she had sold for shillings.

The original blueprint's market-day scenario quietly assumes universal
adoption has already happened. That assumption is where most community
currencies fail.

**The bootstrap must be engineered, not hoped for:**

1. Sign **anchor acceptors before issuing a single note**: the cooperative
   itself, at least one milling business, a school accepting fees, a clinic,
   and 20+ market traders. Written commitments.
2. The cooperative pays its own staff partly in RCU — the operator must eat
   its own cooking, visibly.
3. Cooperative fees and warehouse charges payable *only* in RCU. This
   creates guaranteed baseline demand, which is precisely what made Wörgl
   work: the scrip was accepted for municipal taxes.
4. Publish an acceptor directory and put a physical sticker on every
   accepting stall.
5. **Density over breadth.** One market where everyone accepts beats five
   markets where a few do. A currency needs a closed loop — spend, receive,
   spend again — and loops require density.

**Kill criterion: if fewer than 60% of surveyed traders in the pilot market
accept RCU by month 9, stop and redesign.**

### R1 — Regulatory shutdown (score 20)

Covered in Section 8. The one point worth repeating: **Wörgl was suppressed
because it succeeded.** Plan for success to be the trigger, not failure.

### R3 — Inspector corruption (score 15)

Everything rests on grading. If grading is corrupt, the currency is backed by
nothing and the fraud will not surface until redemption, by which point
thousands of notes are outstanding.

The under-appreciated point: **corruption here is usually not criminal
conspiracy but social pressure.** An inspector grading a neighbour's maize,
in a village where he must live afterwards, faces enormous pressure to be
generous. Rotation and external employment address the social mechanism,
which the anti-fraud controls alone do not.

### R13 — AML designation (score 15)

A single designation by a financial intelligence unit ends the project
regardless of its merits. See Section 8.7.

---

## 9.3 Failure modes not in the original blueprint

Five that were missed, in rough order of severity:

**1. Success in one class only.** Grain notes work; nobody uses stone notes.
The system becomes a grain marketing scheme with nineteen dead series and a
lot of unnecessary complexity. *This is the most likely partial outcome.*
Plan for graceful retirement of unused classes rather than defending the
full twenty.

**2. The stigma trap.** If RCU becomes "money for people too poor to have
shillings," acceptance collapses among exactly the merchants who make it
useful. Every complementary currency faces this. Mitigation: recruit
prosperous, high-status participants first, and ensure desirable goods —
not only staples — are purchasable in RCU.

**3. Demurrage arbitrage — now addressed.** Sophisticated actors hold Tier B
and pay in Tier A, transferring decay losses to less sophisticated
counterparties. Over time the poor hold the decaying notes and the wealthy
hold the stable ones — **an exact inversion of the design intent.**

**Bundle pricing (§12) resolves this**, taking the modelled burden ratio from
2.16 to 1.00. The residual risk is no longer the arbitrage itself but
**incomplete adoption of bundle quoting**: at 25% adoption the ratio worsens
to 2.41, since hoarders route around strict sellers. The risk therefore
changes character — from an unsolvable design flaw to an adoption-discipline
problem, tracked as R19 below.

**4. Warehouse becomes the bottleneck.** Every issuance and redemption
requires a physical visit. In a district with one warehouse and poor roads,
the gate is a day's travel. Adoption stalls for reasons that have nothing to
do with monetary design. Mitigation: mobile inspection units and satellite
collection points.

**5. The success-to-capture pipeline.** A working currency system is
valuable. Once it works, the incentive for a politically connected actor to
take it over rises sharply. **The system is most vulnerable at the moment it
starts working**, and governance protections must be locked in *before* that
moment, since they cannot be added after.

---

## 9.4 Kill criteria

Stated in advance, because projects that cannot articulate their own failure
conditions never stop.

| Checkpoint | Criterion | If not met |
|---|---|---|
| Month 9 | ≥60% of pilot-market traders accepting | Stop; redesign adoption |
| Month 12 | Collateral coverage ≥1.15× every month | Stop issuance; audit |
| Month 12 | Zero unresolved series impairments | Stop; investigate |
| Month 12 | ≥50% of quotes as bundles | **Halt bundle rollout** — below this it worsens arbitrage |
| Month 18 | Median note velocity ≥4 turns/year | Redesign demurrage |
| Month 18 | Inspector variance within 1.5× peer band | Replace inspection regime |
| Month 24 | Regulatory status resolved or credibly in progress | Wind down orderly |
| Any time | Fraud loss > 3% of outstanding in any quarter | Halt; full audit |
| Any time | Any holder loss from series impairment | Halt new issuance |

**An orderly wind-down plan must exist before launch:** all outstanding
notes redeemable at last verified value over a 90-day window, funded by
liquidating collateral. A currency experiment that cannot fail safely should
not be started, because people's harvests are inside it.
