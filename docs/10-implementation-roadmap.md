# 10. Implementation roadmap

Each phase has **entry gates** (conditions to begin) and **exit gates**
(falsifiable criteria to proceed). A phase that fails its exit gate does not
advance by enthusiasm.

---

## Phase 0 — Foundations (months 0–9)

**No notes are issued in this phase.** Everything here is preparation, and
skipping it is the most common way projects of this kind fail.

| Workstream | Deliverable |
|---|---|
| Legal | Counsel opinion on instrument characterisation; WRRB licence application filed |
| Site | One district selected; one warehouse licensed, insured, bonded |
| Grading | Manuals for 4 classes, illustrated, translated; 6 inspectors trained and certified |
| Governance | Cooperative registered; board elected; dispute council seated; **wind-down plan adopted** |
| Technical | Signing library, ledger node, Android app, USSD gateway — all tested offline |
| Adoption | **≥25 anchor acceptors signed in writing** |
| Baseline | Household survey: income, prices, post-harvest loss, seasonal cash access |

The baseline survey is not bureaucracy. Without it, there is no way to know
in year three whether the system helped or harmed — and the honest answer to
that question is the project's most valuable output regardless of which way
it comes out.

**Exit gate:**
- Warehouse licensed under the Warehouse Receipts Act
- Legal opinion states the instrument is *not* deposit-taking
- 25+ written acceptor commitments
- Inspector grading variance <10% on a blind test set
- Wind-down plan funded and adopted

---

## Phase 1 — Single-class pilot (months 9–21)

**Scope: one warehouse, one district, `GR` grains only.**

This is deliberately narrower than the original roadmap's four classes.
Grain alone tests every mechanism — grading, issuance, decay, redemption,
the gate, adoption — with one grading manual and one price series to
manage.

| Target | Value |
|---|---|
| Users | 500–1,500 |
| Notes in circulation | ≤ 50,000 RCU |
| Acceptors | 60% of pilot market traders |
| Warehouse | 1 |
| Classes | 1 |

**Deliberate limits:** individual holdings capped at 2,000 RCU; no
cross-district transfer; no Tier B.

**Why no Tier B in Phase 1.** Tier B is the store-of-value tier and it is
where the demurrage-arbitrage problem (Section 9.3) lives. Introducing it
before the circulation tier is proven means the two problems become
entangled and neither is diagnosable.

**Exit gate:**
- ≥60% trader acceptance sustained for 3 months
- Median velocity ≥4 turns/year
- Collateral coverage ≥1.15× every month
- Zero series impairments
- ≥100 successful physical redemptions
- Fraud loss <1% of outstanding
- Gate invoked ≤ once, resolved within its own rules

---

## Phase 2 — Multi-class, multi-warehouse (months 21–48)

Add `FE` (iron) as the first Tier B class, plus `CM` and one region-
appropriate Tier A class. Three to four warehouses; two to three districts.

| Target | Value |
|---|---|
| Users | 10,000–25,000 |
| Circulation | ≤ 2,000,000 RCU |
| Classes | 4 |
| Warehouses | 3–4 |

**New in this phase:**
- Tier B with explicit custody fees
- Cross-warehouse redemption
- Federated checkpointing (now that more than one cooperative exists)
- NFC secure cards for high-value users
- Formal central bank engagement

**The three things this phase is really testing:**

1. **Does cross-commodity pooling fix the seasonal sawtooth?** This is the
   central open question from Section 1.5, and Phase 2 is the first point at
   which it can be answered with data rather than modelling.
2. **Does demurrage arbitrage appear?** Measure the Tier A/Tier B holdings
   split by wealth quintile. If the poorest quintile holds disproportionate
   Tier A, the design has the inversion problem and needs intervention.
3. **Does inspector rotation survive contact with reality?** Rotation is
   expensive and inconvenient, and it is the first control that gets quietly
   dropped.

**Exit gate:**
- Money supply seasonal variation <40% peak-to-trough
- Tier A/B holdings ratio not correlated with wealth quintile (r < 0.3)
- Coverage ≥1.15× across all classes
- Central bank no-objection or sandbox admission obtained
- Inspector rotation executed as scheduled

---

## Phase 3 — Regional network (years 4–8)

Expand to 8–12 classes and multiple regions. Inter-cooperative settlement.
Revenue authority withholding agreement. Possible legislative amendment.

**Not in scope even at this stage:** replacing the central bank; national
legal tender status; cross-border note circulation; strategic minerals;
water.

### On the original Phase 3 goal

The original roadmap ends with the central bank "gradually replaced by a
federation of cooperative issuing authorities." This should be removed as a
stated objective, for two reasons.

**Strategically:** it is the single sentence most likely to get the project
suppressed. Section 8's entire engagement strategy depends on the system
being credibly *complementary*, and a written intention to replace the
central bank destroys that credibility permanently.

**Substantively:** it is probably not desirable. A central bank does things
this system cannot — lender of last resort, foreign exchange management,
payment system oversight, monetary response to shocks. A commodity-backed
cooperative federation has no capacity for any of them. **A country with
only RCU would face every harvest failure as a monetary crisis**, because
its money supply and its food supply would be the same variable.

The honest and more attractive ambition: **RCU as a resilient parallel
system that carries local trade when the national currency is scarce or
unstable, and recedes when it is not.** That is achievable, defensible, and
genuinely valuable. It is also much likelier to be allowed to exist.

---

## 10.2 Budget sketch

Rough order of magnitude, USD, for Phase 0 + Phase 1 (21 months):

| Item | Cost |
|---|---|
| Legal (opinion, licensing, registration) | 25,000 |
| Warehouse upgrade, insurance, bond | 60,000 |
| Software build (4–6 person-months) | 45,000 |
| Note printing (Tier 1 security, 100k notes) | 20,000 |
| Inspector salaries (6 × 21 months) | 75,000 |
| Training, manuals, translation | 20,000 |
| Baseline + endline surveys | 30,000 |
| Community engagement | 25,000 |
| Stabilisation fund seed | 50,000 |
| Contingency (25%) | 88,000 |
| **Total** | **≈ 438,000** |

Two observations. **The software is under 11% of the budget** — this is not
a technology project, and treating it as one is a category error. And **the
stabilisation fund seed is the item most likely to be cut and the item least
safe to cut**: it is the first loss absorber standing between a bad harvest
and a holder losing value.

---

## 10.3 What to measure

| Metric | Why | Frequency |
|---|---|---|
| Trader acceptance rate | The binding constraint on everything | Monthly survey |
| Velocity (turns/year) | Does demurrage actually work? | Quarterly, sampled |
| Coverage ratio by class | Solvency | Continuous |
| Redemption gate invocations | Liquidity stress | Continuous |
| Grading variance by inspector | Corruption early warning | Monthly |
| Tier A/B split by wealth quintile | Arbitrage inversion | Quarterly |
| Post-harvest loss vs. baseline | The actual development outcome | Annual |
| Harvest-to-lean price gap | Whether producers are better off | Annual |
| Household cash access in lean season | Whether the seasonal problem is solved | Annual |

The last three matter most. **The purpose is not to have a currency; it is
to make producers better off.** A system with beautiful monetary properties
and no measured welfare improvement has failed, and should be honest enough
to say so.
