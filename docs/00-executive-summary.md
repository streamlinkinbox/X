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

## The change that simplifies everything: weight denomination

**A note is a claim on matter, not on value.** It says "100 kg maize, Grade
A", not "100 units backed by maize". 1 kg of iron is 1 metal unit — it was
last year and will be next year.

This deletes the system's most capturable institution. There is no longer a
committee deciding what a tonne of maize is worth, because issuance is a
weighing operation: **the scale decides how much currency a deposit creates,
and the buyer and seller decide prices between themselves.** Those are now
separate questions, and only the first is the system's business.

It also collapses the haircut. A note claiming 1 kg of iron is not impaired
by a fall in the iron price — the iron is still there. Haircuts therefore
cover only physics, falling from an average of **29.5% to 6.9%**. A producer
receives ~92 kg-units per 100 kg of Grade A maize instead of 70 units of
contested value.

Two corrections keep this honest: deposits are normalised to **dry-matter
equivalent** (water is not the commodity — green timber can be 60% moisture)
and to **standard-grade equivalent** (Grade C maize is still maize, but not
a kilogram of Grade A).

**The cost is real and is stated in §13.6:** without a value unit there is no
common measure, so a 20-good market has 190 bilateral exchange rates instead
of 20 prices. The mitigation is that a reference good emerges spontaneously —
iron scores best — plus app and printed rate boards. This is now open problem
P11 and Phase 1 must measure whether it is usable.

## The refinement that solves the worst problem

Prices are quoted as **bundles of specific commodity classes** — "100 iron +
500 wood + 40 plastic" — not as a single fungible amount, and every quote
carries an independently assessed **reference bundle** so the buyer can see
the markup.

This was added after the first draft and it resolves what Annex B rated the
design's most dangerous flaw. With a free choice of payment medium,
sophisticated holders keep stable notes and spend decaying ones, so demurrage
falls on the poor — an exact inversion of the purpose. Requiring payment in
*specific classes* removes that choice: modelled over 24 months, the burden
ratio between a sophisticated and a naive holder falls from **2.16 to 1.00**.

**One condition, and it is severe: partial adoption is worse than none.** At
25% of sellers insisting on exact bundles the ratio rises to **2.41**,
because hoarders route around the strict minority and dump decayed notes on
the flexible majority. Bundle pricing must be the launch default and
near-universal, or it must not be introduced at all. A gradual rollout passes
directly through the region where it does harm. See §12.

The receipt also reframes the whole system usefully: this is
**barter with the frictions removed** — divisibility, portability and delayed
settlement added to a maize-for-timber swap — rather than a rival currency.
That is both an accurate description and the basis of the legal strategy in
§8.

## The constraint that binds first: people

Thirteen sections model grain, iron and ledgers. §14 models the thing that
actually limits the project.

**The cadre is the engine; the acceptor network is the product.** A tight core
of 10–15 trusted people is the right structure for holding keys and taking
risk — but it cannot *be* the currency. A 15-person cadre is 60% of the
traders only in a market of about **312 adults**, too small to sustain a
warehouse. In a village of 3,000 it covers **10%** of the acceptance
requirement.

This matters because the common organising instinct — build a tight core,
keep it secret, ignore everyone else — is **actively fatal here.** A
warehouse cannot be clandestine; a currency must be recognised by strangers.
The security model is legitimacy and auditability, not concealment.

Two further corrections come out of the model. Small-commitment screening
tests measure **slack, not commitment**: applied to a destitute pool, the
same test wrongly rejects 23 reliable people versus 3 in a comfortable pool.
And apprenticeship — the right model for skills — yields about **1.9× in a
decade, not 20×**, because supervision capacity, not enthusiasm, is the
bottleneck. The honest win is that the community holds more practitioners
than it started with by roughly year 5: knowledge outliving its holders.

## Can services back the currency?

§15 tests whether skilled labour — a doctor's hour — can be a monetary unit.
**Partly, and not where the injustice is sharpest.**

The grievance checks out. Health costs push over **150 million people** into
or deeper into poverty in the WHO Africa region alone, and capital equipment
is only about **8%** of the cost of care — far too small to justify bills that
bankrupt families. Labour is ~57%. The market pays specialists **10–50×** an
unskilled worker; the premium actually needed to make seven years of training
rational is **1.23×**. The rest is rent.

But service credits fail for scarce specialists, for three independent
reasons: at 1 doctor per 25,000 they cover **6.4%** of demand (a 15-year queue
ticket); **the sick cannot earn** (need is inversely related to earning
capacity — Japan's Fureai Kippu proved this over decades); and **the backing
emigrates**, where grain cannot.

So: credits for *abundant* labour, a commodity-backed health **fund** for
scarce care, and training bonds to reduce the scarcity. Pooling is the key —
what destroys families is not the price of care but being asked to pay it *at
the moment of illness*.

**The hard limit:** ~40% of care cost is imported consumables and drugs.
No local currency can pay for those.

## Managing the outside world without becoming dependent on it

§16 addresses the addiction analogy directly, and follows it to the policy a
clinician would actually choose — which is **not** abstinence.

Withdrawal severity differs by substance: quitting caffeine is a headache,
quitting alcohol can kill. The same is true of imports, and the key finding is
that **what kills you is cheap** — medicines and vaccines are just **11.8%**
of the import bill and 100% of the mortality risk. Africa imports **95–99% of
medicines** and nearly all active pharmaceutical ingredients.

So classify by withdrawal severity, never by cost:

- **Buffer by severity:** 128 days of medicine, zero days of clothing. This is
  **31% cheaper** than uniform stockpiling and protects lethal goods **42%
  longer**.
- **Substitute where it pays, not where it feels urgent.** Food pays back in
  **1.9 years**; medicines in **200**. Localising the easy categories is what
  guarantees the FX for the impossible ones.
- **Never detox abruptly.** Cutting a critical import before its substitute is
  proven is not sovereignty; it is the withdrawal that kills the patient.
- **Accept the floor:** ~51% independence is achievable. Promise resilience,
  not independence.

The deeper point: RCU's contribution is not eliminating imports. It is that
when imports fail, **the grain is still in the shed and the notes still work**
— turning a collapse into a shortage.

## Making it locally: the production ladder

§16 concluded that lethal imports cannot be localised. §17 shows that was
**too pessimistic**, because it treated "medicine" as one category.

Disaggregated by technical difficulty — a five-rung ladder from *grow* to
*precision synthesis*, where **rungs cannot be skipped** — two
lethal-category goods turn out to be locally producible today:

| Product | Capex | Why it works |
|---|---|---|
| **Medical oxygen** (PSA plant) | ~$105,000 | Made from **air**; proven at district scale in Kenya, Rwanda and Ethiopia at ~$7.34/patient |
| **Oral rehydration salts** | ~$18,000 | Sugar, salt, clean water; treats the leading cause of child death from diarrhoea |

**Air cannot be embargoed, sanctioned, or priced in dollars.**

Ten of sixteen candidates are viable — where viable means *saving more FX
than the plant costs to operate*, a test six candidates fail. APIs and
vaccines remain permanently out of reach at district scale.

Two design rules: **rank by sovereignty, not payback** (it costs ~$26,000/yr
and buys a second life-critical capability), and **prefer dual-use plants** —
the everyday demand is what keeps a facility staffed and maintained until the
emergency it was built for.

Independence rises from ~51% to **~60%**.

## Security: mostly mediation, not force

§18 quantifies what a community security cooperative actually does: **65%
mediation, 14% currency-fraud forensics, 21% anything involving force.** Five
rotating members suffice, since coverage rather than caseload sets the roster.

The binding constraint on fraud detection is **inspector collusion, not
instrument accuracy** — detection falls from 93% to 20% as collusion rises to
certainty. Rotation genuinely prevents capture, but only within a narrow
band: 9-month tours with 18-month breaks are safe, 24-month tours are not.

## Defense: the citizen militia and asymmetric neutralization

§19 models military defense: **a mandatory, self-funded, self-equipped
citizen militia** operating on pure asymmetry without a standing military
budget or foreign arms dependency.

The decisive insight: **destruction is expensive; neutralization is cheap.**
You do not need a $150,000 missile to destroy a $10 million tank; a $5 net
and a bucket of mud over its periscopes leaves it blind, immobile, and
useless.

Key findings:
- **99.3% zero-fuel fleet:** Horses, pack mules, bicycles, and marching foot
  units decouple military logistics from vulnerable fuel refineries and convoys.
- **73.3% locally producible kit:** 15-item standard personal kit costs ~$698,
  with blades, rations, shelter, and medical kits forged and sewn locally.
- **Layered drone defense:** A 5-layer system (wire barriers, smoke, net guns,
  12ga birdshot, and close-range jamming) neutralizes **>99% of incoming drone
  swarms** at a cost of $500 per engagement.
- **Asymmetric cost ratios > 10,000:1:** Neutralizing an F-22 (runway cratering
  at $200), a tank (sensor blinding at $10), or an APC ($5) creates an
  unsustainable financial burn rate for the invader ($25M/day vs $10k/day),
  ensuring the community survives as an un-swallowable porcupine.

## Governance: the Competence Council and departmental enforcement

§20 establishes the governance architecture for the state: **functional leadership
selected by peer merit rather than mass voting or hereditary monarchy.**

Key mechanisms:
- **3-Stage Selection:** Automated qualification via 10-year ledger contribution
  and apprenticeship $\rightarrow$ Peer selection by 20–30 senior masters with 75%
  consensus $\rightarrow$ 1-year quantitative probation.
- **11 Functional Domains:** Single accountable Stewards for reserves, production,
  health, works, knowledge, security, justice, diplomacy, and coordination, plus
  a 5–7 member collective War Council with mandatory female representation.
- **Departmental Policing:** Military Police (preventing looting, atrocities,
  and black-market arms sales) and civil enforcers across every department
  (halting grain hoarding and inventory skimming).
- **Independent Measurement Bureaus:** Dedicated telemetry and recording staff
  in every department reporting directly to the Audit Board, eliminating metric
  falsification and Goodhart's Law.
- **Sortition Audit & Anti-Monarchy Safeguards:** Annual random 20-citizen jury
  audits with full subpoena power, zero legal immunity, and strictly equal living
  standards (1.0 : 1.0 ratio).

## Anti-corruption: difficulty diagnostics and resource curse eradication

§21 formalizes structural protections against systemic looting, false incompetence
accusations, and single-commodity Dutch Disease:

- **Difficulty-Adjusted Diagnostics:** Evaluates leaders not against impossible
  perfection, but through comparative benchmarking against neighboring districts
  under identical climate/blockade shocks.
- **Shadow Leader System:** Every domain steward trains an active managing
  Deputy who must pass a **90-day quantitative probation ($\ge 80\%$ target
  completion)** upon assuming office.
- **Eliminating Phantom Jobs & Looting:** Production-based payroll eliminates
  zero-value patronage jobs (e.g., SA light-switching); decentralized commodity
  treasuries and a **$5\times$ personal wealth ceiling** eliminate Nigerian-style
  governor looting.
- **Eradicating Dutch Disease:** Bounded by a **20-commodity basket (HHI $< 1,200$)**,
  the economy cannot become addicted to single-resource windfalls.
- **Anti-Monopoly Caps:** Outlaws exclusive import charters (e.g., car import
  monopolies) and enforces a strict **20% single-entity market cap**.

## Intelligence: the Research & Analysis Bureau (RAB)

§22 models the central analytical organ connecting departmental data into systemic reform:

- **The Missing Organ:** Connects siloed reports (police crimes, warehouse inventory,
  apprentice test scores, clinic recoveries, soil tests) into a cohesive operational picture.
- **Five Specialized Divisions:** Forensic Audit (corruption hunters), Economic
  Analysis (macroeconomic doctors), Human Capital (difficulty-adjusted talent
  evaluators), Reform Design (closed-loop 6-stage system fixers), and Science &
  Technology (applied indigenous research).
- **Lean Cadre:** **35–55 total staff per 10,000 population** ($\approx 0.47\%$),
  combining cross-domain senior masters with advanced 4th-year apprentices.
- **Watching the Watchers:** Strictly **zero arrest or police powers**, public
  open data by default, **2-year Chief Analyst rotation**, and mandatory annual
  external audits by federated community teams.

## External intelligence & ecology: the Awareness Triangle

§23 completes the sensory apparatus of the state, pairing internal analysis (RAB)
with outward awareness and ecological guardianship:

- **Community Intelligence Service (CIS):** 16–24 external intelligence officers
  monitoring geopolitical horizons via HUMINT (traders, refugees, diaspora), SIGINT
  (radio, border cellular, drone RF), OSINT (government gazettes, mining concessions),
  and Counter-Intelligence (disinformation, cyber, supply chain defense).
  *Strict prohibition on domestic surveillance; zero offensive operations.*
- **Environmental & Disaster Management Bureau (EDMB):** 21–32 permanent staff
  and 50–100 trained emergency volunteers operating real-time river, rainfall,
  soil, and disease vector sensors.
- **Mandatory Environmental Impact Assessments (EIA):** All civil projects
  must receive an EIA. Critical-risk projects are denied by default and require a
  **75% Council supermajority override**.
- **Predictive Disaster Preparedness:** Floods (24–72h), landslides (12–48h),
  and droughts (3–12m) predicted and countered with pre-positioned 30-day caches
  and 4-phase rescue operations.

## The War Council & specialized strike units: asymmetric imperial defense

§24 formalizes how a small community commands and fights with the precision of an empire:

- **The War Council (8 Seats):** A collective deliberative civilian/military command
  (Rotating Chair, Defense Coordinator, CIS Intel Chief, EDMB Environmental Chief,
  RAB Logistics Chief, Senior Militia Commander, Justice Coordinator, and Sortition
  Civilian Delegate).
- **Constitutional Decision Safeguards:** 5-of-8 standard majority, mandatory
  **24-hour "No" reflection delay**, **7-of-8 supermajority Blood Rule** (civilian
  casualties $> 10$), and strict prohibition on unprovoked offensive operations without
  Community Council assent.
- **The Living Contingency Library (10 Scenarios):** Pre-planned Roman operational
  blueprints (S1–S10) updated quarterly and wargamed semi-annually.
- **The War Room ("Genius Council"):** 24–72 hour multidisciplinary isolation chamber
  solving tactical deadlock with zero rank hierarchy, mandatory 6h sleep, and outside
  wildcard thinkers (blacksmiths, farmers).
- **7 Specialized Units (155–195 Operators, <5% of Militia):** Precision cadres
  (Strike Team, Hammer shock assault, Scorpion counter-drone, Worm sappers, Healer trauma
  medics, Echo signals/EW, Horse mounted recon).
- **Anti-Janissary / Anti-Mamluk Firewalls:** Elite in skill, not in status. Mandatory
  **3-year return to civilian economic production**, no separate barracks, no separate
  wages, no hereditary succession, and no civilian political office while serving.

## Media, information integrity & social harm: the conduct-not-distribution framework

§25 resolves the tension between anti-corruption transparency and social harm prevention:

- **The Governing Axiom:** *"Restrict the instructional and the deceptive. Do not
  restrict the depictive."*
- **Courtroom Dignity (Anti-Circus):** Cameras in courtrooms are banned; unconvicted
  suspects, victims, and minors are anonymized (*"Andreas B."* rule); *sub judice* is
  strictly enforced. Justice remains open to in-person citizens and sortition juries
  with transparent written registries.
- **Instructional vs. Fictional Line:** Method details (suicide how-tos, mass shooter
  manifestos, cyber exploits) are restricted; fictional crime drama, art, and literature
  remain completely uncensored.
- **Commercial & Aspirational Deception:** Mandatory disclosure of paid promotions and
  filtered images; ban on influencer financial schemes (crypto, forex, gambling); credit
  ad bans for minors.
- **Distribution Architecture (Source, Never Filter):** The state may operate an official
  authoritative wire service or court registry; it is strictly prohibited from operating
  a monopoly content filter or owning media pipes. Press reporting on government is
  constitutionally protected.

## Non-cash penalties, restorative labor & anti-extortion enforcement

§26 eliminates roadside bribery, predatory fines, and "policing for profit" through
the total demonetization of law enforcement:

- **The Fatal Flaw of Cash Fines:** Cash fines create extortion markets, predatory
  revenue quotas, and wealth-based injustice where the rich buy impunity.
- **The 4-Tier "Sweat & Duty" Non-Cash Penalty Ladder:** Penalties take time and
  public physical labor (sewer and drain clearing, pothole patching, firebreaks).
- **Victim Restitution (100% Direct):** Assessed damages are paid 100% directly to
  the harmed victim (at 2.0x value) and **exactly 0% to police department budgets
  or municipal slush funds**, eliminating the economic incentive for quota hunting.
- **Six Statutory Anti-Extortion Locks:**
  1. Automatic felony offense for any patrol officer to carry or demand cash on duty.
  2. Missing dashcam/bodycam footage results in **automatic citation dismissal**.
  3. Reverse bounty (500 RCU) paid to citizens who report bribe-soliciting officers.
  4. RAB algorithmic anomaly detection flags predatory quota-hunting choke points.
  5. Mandatory 6-month patrol sector rotation.
  6. Contested citations adjudicated by a **3-person random sortition citizen jury**.
- **Community Exile (Banishment):** Reserved strictly for irredeemable violent
  predation, armed treason, or willful refusal of restorative labor, requiring a
  **75% Community Council supermajority vote**.

## Abolishing debt-based & subscription extraction: direct physical provisioning

§27 eliminates the parasitic financial middleman layer (commercial medical aid,
private insurance, speculative pensions, usurious loans, and sovereign debt):

- **Claims vs. Real Wealth:** Prohibits financialized claims multiplying faster than
  real production. Money represents physical goods and verified labor, not private
  claims on future survival.
- **Healthcare & Legal Defense:** 100% direct public and guild provisioning (§14, §15)
  with 90-day physical drug stockpiles (§16); zero medical aid debit orders, zero hourly legal fees.
- **Disaster Risk Pooling:** Replaces private insurance adjusters and claim denials
  with physical commodity mutual reserve pools (timber, stone, seed) mobilizing
  guild reconstruction within 48 hours (§02, §23).
- **Master-Apprentice Elder Security:** Replaces crash-prone speculative pension funds
  with guaranteed monthly physical commodity rations (grains, oil, fuel, housing, care)
  funded directly by active guild output.
- **Zero-Interest Advances (Housing, Vehicles, Tools):** Borrowers repay the exact
  principal advanced ($I=0.0\%$). Installments flexible on hardship; zero compound
  interest; zero foreclosure/seizure of primary family homes; zero inherited debt.
- **The Decisive Access Test:** *"Does the system provide direct physical access to
  necessities — or merely a more sophisticated mechanism to charge people?"*

## What this system cannot do

Stated plainly, because a blueprint that only lists strengths is marketing:

- **It cannot back imports.** No foreign supplier accepts maize-backed notes
  for fuel, medicine or machinery. RCU is a domestic circulation instrument
  and the region still needs foreign exchange for everything it does not
  produce — about **49% of the import bill is irreducible**, and it is
  disproportionately the part that kills people if it lapses (§16). What RCU
  *does* prevent is an FX shortage becoming a domestic monetary collapse.
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
| [`12-bundle-pricing-and-receipts.md`](12-bundle-pricing-and-receipts.md) | Bundle prices, dual-price receipts, the hoarding question |
| [`13-weight-denomination.md`](13-weight-denomination.md) | **Weight-denominated units, grading, provenance — supersedes §1.1** |
| [`14-people-and-recruitment.md`](14-people-and-recruitment.md) | Recruitment, screening, trust, apprenticeship — the human constraint |
| [`15-service-credits.md`](15-service-credits.md) | Can labour back a currency? Health costs, time banking, care |
| [`16-external-trade-and-dependency.md`](16-external-trade-and-dependency.md) | Import dependency, buffers, substitution, the trade window |
| [`17-local-production-doctrine.md`](17-local-production-doctrine.md) | **The production ladder — what can actually be made locally** |
| [`18-community-security.md`](18-community-security.md) | Mediation, fraud forensics, rotation, armoury, capture resistance |
| [`19-military-doctrine.md`](19-military-doctrine.md) | **Citizen militia, asymmetric defense, asset neutralization** |
| [`20-competence-council-and-departmental-policing.md`](20-competence-council-and-departmental-policing.md) | **Competence Council governance, departmental policing, measurement** |
| [`21-anti-corruption-and-resource-curse-prevention.md`](21-anti-corruption-and-resource-curse-prevention.md) | **Anti-corruption, difficulty diagnostics, resource curse prevention** |
| [`22-research-and-analysis-bureau.md`](22-research-and-analysis-bureau.md) | **Research and Analysis Bureau (RAB), cross-silo intelligence, reform** |
| [`23-intelligence-and-environmental-disaster-management.md`](23-intelligence-and-environmental-disaster-management.md) | **Community Intelligence (CIS), Environmental Disaster Bureau (EDMB)** |
| [`24-war-council-scenario-planning-and-specialized-units.md`](24-war-council-scenario-planning-and-specialized-units.md) | **War Council, Scenario Planning, and Specialized Strike Units** |
| [`25-media-information-integrity-and-social-harm.md`](25-media-information-integrity-and-social-harm.md) | **Media, Information Integrity, and Social Harm** |
| [`26-penalty-system-and-anti-extortion-enforcement.md`](26-penalty-system-and-anti-extortion-enforcement.md) | **Non-Cash Penalties, Restorative Labor, and Anti-Extortion Enforcement** |
| [`27-abolishing-debt-and-subscription-systems.md`](27-abolishing-debt-and-subscription-systems.md) | **Abolishing Debt-Based and Subscription-Based Systems** |
| [`annex-a-parameters.md`](annex-a-parameters.md) | Generated tables: all parameters and stress results |
| [`annex-b-open-problems.md`](annex-b-open-problems.md) | Unsolved problems, ranked by how badly they hurt |

The parameter model and stress tests live in [`model/rcu/`](../model/rcu/);
run `make tables` to regenerate Annex A, `make test` to check the arithmetic.
