# RCU — Real Commodity Unit

A design blueprint for a **commodity-backed, digitally-verified,
demurrage-bearing currency system** intended for rural East African
contexts, with a quantitative model that stress-tests its own claims.

> **Status: design document, version 0.2.** Nothing here has been piloted.
> Several findings in the model contradict the original concept, and those
> contradictions are documented rather than smoothed over.

---

## The idea in one paragraph

Every unit of currency is a bearer claim on a specific, graded, inspected
quantity of a real commodity in a licensed warehouse. Notes are
cryptographically signed and verifiable offline by any phone. Notes backed by
perishable goods lose value on a published schedule calibrated to the actual
spoilage rate of the backing commodity, so holding them is costly and
spending them is not. Notes backed by durable goods hold face value and pay
an explicit custody fee instead. Issuance is decentralised across producer
cooperatives, and currency enters circulation only when a commodity is
deposited and verified.

The founding observation: **in much of rural East Africa, wealth exists but
does not circulate.** A farmer with eight tonnes of maize is wealthy in goods
and destitute in cash, and must sell at the harvest price floor. RCU turns
the maize into a spendable claim without forcing the sale.

---

## Start here

**[docs/00-executive-summary.md](docs/00-executive-summary.md)** — including
the five model findings that change the original design.

| Document | Contents |
|---|---|
| [00 Executive summary](docs/00-executive-summary.md) | The idea, what is genuinely new, what it cannot do |
| [01 Monetary design](docs/01-monetary-design.md) | Unit of account, tiers, demurrage, haircuts, money supply |
| [02 Commodity classes](docs/02-commodity-classes.md) | All 20 classes, grading, which ones should not ship |
| [03 Issuance & redemption](docs/03-issuance-and-redemption.md) | Deposit, inspection, loss waterfall, redemption gate |
| [04 Note design](docs/04-note-design.md) | Physical note, security features, required warnings |
| [05 Technical architecture](docs/05-technical-architecture.md) | Ledger, offline protocol, double-spend bounds, keys |
| [06 Governance](docs/06-governance.md) | Cooperatives, inspector independence, capture resistance |
| [07 Taxation & fees](docs/07-taxation-and-fees.md) | Gate-based taxation, full fee schedule |
| [08 Legal & regulatory](docs/08-legal-and-regulatory.md) | Legal characterisation, WRS route, AML |
| [09 Risk register](docs/09-risk-register.md) | Scored risks and kill criteria |
| [10 Roadmap](docs/10-implementation-roadmap.md) | Phased plan with falsifiable gates |
| [11 Prior art](docs/11-prior-art.md) | Graham, Gesell, Wörgl, Sarafu, WRS |
| [12 Bundle pricing & receipts](docs/12-bundle-pricing-and-receipts.md) | Bundle prices, dual-price receipts, hoarding |
| [13 Weight denomination](docs/13-weight-denomination.md) | **Physical units, grading, provenance — supersedes §1.1** |
| [14 People & recruitment](docs/14-people-and-recruitment.md) | Cadre vs. network, screening bias, apprenticeship |
| [15 Service credits](docs/15-service-credits.md) | Labour-backed currency, health costs, care pooling |
| [16 External trade](docs/16-external-trade-and-dependency.md) | Import dependency, buffers, substitution, trade window |
| [17 Local production](docs/17-local-production-doctrine.md) | **The production ladder — what can be made locally** |
| [18 Community security](docs/18-community-security.md) | Mediation, fraud forensics, rotation, armoury |
| [19 Military doctrine](docs/19-military-doctrine.md) | **Citizen militia, asymmetric defense, asset neutralization** |
| [20 Competence Council](docs/20-competence-council-and-departmental-policing.md) | **Merit governance, departmental policing, measurement bureaus** |
| [21 Anti-corruption](docs/21-anti-corruption-and-resource-curse-prevention.md) | **Difficulty diagnostics, shadow succession, resource curse** |
| [22 Research & Analysis Bureau](docs/22-research-and-analysis-bureau.md) | **Cross-silo intelligence, 5 divisions, closed-loop reform** |
| [23 Intelligence & Environment](docs/23-intelligence-and-environmental-disaster-management.md) | **Community Intelligence (CIS), Ecology & Disaster (EDMB)** |
| [24 War Council & Specialized Units](docs/24-war-council-scenario-planning-and-specialized-units.md) | **War Council, Scenario Planning, 7 Specialized Units** |
| [25 Media & Information Integrity](docs/25-media-information-integrity-and-social-harm.md) | **Content conduct, court dignity, source-not-filter architecture** |
| [Annex A](docs/annex-a-parameters.md) | **Generated** parameter and stress tables |
| [Annex B](docs/annex-b-open-problems.md) | Unsolved problems, ranked by severity |

---

## The five findings that changed the design

Produced by the model in `model/rcu/`, not by opinion.

1. **Tier B cannot be free.** Nine of twenty classes have zero demurrage but
   non-zero storage cost. They require an explicit custody fee of 1–5%/year.
   "Holds value indefinitely at no cost" is physically impossible.

2. **The haircut, not the decay rate, keeps the system solvent.** Notes must
   be issued against ~70% of assessed value. Counterintuitively the *safest*
   commodities are the most dangerous: precious metals at a 10% haircut
   survive only a 7.3% price fall against 18% annual volatility.

3. **Automatic per-transaction taxation and offline capability are mutually
   exclusive.** Taxation moves to the issuance and redemption gates, which
   are always online and always supervised. This is a better design anyway —
   and it removes the need for a transaction-surveillance database that would
   be a permanent instrument of repression.

4. **"Impossible to counterfeit" is not achievable.** A QR code is a
   photograph. Cryptography proves valid issuance, not that the paper is not
   a copy. The claim downgrades to "detectable, bounded, insurable."

5. **A single-crop cooperative cannot supply a stable money.** Modelled over
   48 months, the money supply swings from zero to full and back every year —
   a liquidity drought every lean season, exactly when it is needed most.

Full detail, including three findings the original concept missed entirely
(demurrage arbitrage, the stigma trap, and the success-to-capture pipeline),
is in [Annex B](docs/annex-b-open-problems.md).

## Weight denomination: the note is a claim on matter

A note says **"100 kg maize, Grade A"**, not "100 units". 1 kg of iron is 1
metal unit. Issuance is a weighing operation, so **there is no price
committee** — the system's most capturable institution simply does not exist.
Prices are whatever buyer and seller agree.

Because a note claiming 1 kg of iron is not impaired by a fall in the iron
price, haircuts cover only physics — weighing error, moisture, shrinkage:

| | Value-denominated | Weight-denominated |
|---|---|---|
| Average haircut | 29.5% | **6.9%** |
| Grade A maize, 1,000 kg | ~700 units | **920 kg-units** |
| Issuance needs | A price | **A scale** |

Deposits are normalised to dry-matter and standard-grade equivalent (green
timber can be 60% water), and the decay clock runs from **harvest, not
deposit** — so storing grain privately for seven months no longer buys a
fresh grace period.

**The honest cost:** no common unit of account means a 20-good market has 190
bilateral rates instead of 20 prices. Iron is the likely spontaneous
reference good. Tracked as open problem P11; Phase 1 must measure whether it
is usable. See [§13](docs/13-weight-denomination.md).

## Bundle pricing: the fix for the worst flaw

Prices are quoted as **bundles of specific classes** — "100 iron + 500 wood +
40 plastic" — with an assessed reference bundle beside them so a buyer can
see the markup per class:

```
| ASKED         ASSESSED        DIFFERENCE           |
|    100 FE stable     20 FE           +400%         |
|     40 PL decays      5 PL           +700%         |
|    500 WD decays    200 WD           +150%         |
| MARKUP                 +184.4%                     |
| VERY HIGH MARGIN — CHECK OTHER SELLERS             |
```

Demanding *specific classes* removes the payer's ability to hoard stable
notes and spend only decaying ones. The burden ratio between a sophisticated
and a naive holder drops from **2.16 to 1.00** — resolving Annex B's P1.

**But partial adoption is worse than none:** at 25% of sellers insisting, the
ratio rises to **2.41**, because hoarders route around them. This must launch
as a universal default or not at all. See
[§12](docs/12-bundle-pricing-and-receipts.md).

---

## The model

```
model/rcu/
  classes.py     20 commodity classes: decay, haircuts, storage costs, liquidity
  valuation.py   canonical decay arithmetic (integer cents, deterministic)
  stress.py      harvest cycles, price crashes, redemption runs
tools/
  gen_tables.py  generates Annex A from the model
tests/
  test_valuation.py  55 tests, including the document's economic claims
```

```bash
make test     # run the suite
make tables   # regenerate Annex A from the model
make check    # test + verify the docs are not stale
```

Every number in the documentation is computed from
[`model/rcu/classes.py`](model/rcu/classes.py), so the prose and the code
cannot drift apart. Tests encode the document's claims directly — for
example, `test_precious_metals_is_under_haircut` fails if someone "fixes" the
parameter without updating the analysis.

Valuation is deterministic integer arithmetic in cents. Every device must
produce a bit-identical answer to "what is this note worth today?"; floating
point drift between a phone and a POS terminal is a settlement dispute.

---

## People: the cadre is the engine, the network is the product

A tight core of 10–15 is right for holding keys and risk — but it cannot be
the currency. Acceptance is what gives money value:

| Market | Traders | Accepting needed | Cadre of 15 covers |
|---|---|---|---|
| Small village (800) | 60 | 36 | 42% |
| Large village (3,000) | 240 | 144 | **10%** |
| Small town (12,000) | 900 | 540 | **3%** |

So the common organising doctrine — small core, secrecy, ignore the rest — is
fatal here. **A warehouse cannot be clandestine.** Security comes from
legitimacy and auditability.

Two more findings: screening tests measure **slack, not commitment** (the same
test wrongly rejects 23 reliable people from a destitute pool versus 3 from a
comfortable one), and apprenticeship yields **~1.9× in a decade, not 20×** —
supervision capacity is the bottleneck. See
[§14](docs/14-people-and-recruitment.md).

## Can labour back the currency?

§15 models service credits. They work for abundant labour and fail for scarce
specialists:

| Service | Ratio | Demand covered | Clears? |
|---|---|---|---|
| Doctor | 1:25,000 | **6.4%** | No — 15-year queue |
| Nurse | 1:2,000 | 80% | No |
| Community health worker | 1:500 | **320%** | **Yes** |

Two further findings: **the sick cannot earn** (need is inversely related to
earning capacity — the documented failure of Japan's Fureai Kippu), and the
backing **emigrates** in a way grain cannot.

On the cost of care, the popular grievance is largely correct — capital
equipment is only **8%** of delivered cost, labour ~57%, and the skill premium
needed to justify seven years of training is **1.23×** against market
differentials of 10–50×. But recurring imported consumables are **25%**, so
**~40% of care cost cannot be paid in any local currency.**

Answer: credits for abundant labour, a commodity-backed health **fund** for
scarce care, training bonds to reduce scarcity. See
[§15](docs/15-service-credits.md).

## Import dependency without addiction

§16 takes the addiction analogy seriously: withdrawal from caffeine is a
headache, withdrawal from alcohol can kill. Imports differ the same way, and
**what kills you is cheap**:

| Severity | Share of import bill | Time to harm |
|---|---|---|
| **Lethal** (medicines, vaccines) | **11.8%** | 7 days |
| Severe (fuel, fertiliser) | 50.5% | 45 days |
| Tolerable (food, clothing) | 23.7% | 365 days |

So buffer by severity — **128 days of medicine, zero days of clothing**. That
is **31% cheaper** than uniform stockpiling and protects lethal goods **42%
longer**.

Substitution ranking inverts intuition: food pays back in **1.9 years**,
medicines in **200**. Localise the easy things so the foreign exchange is
always there for the impossible ones. Achievable independence is **~51%** —
promise resilience, not autarky.

**Never detox abruptly:** cutting a critical import before its substitute
works is the withdrawal that kills the patient. See
[§16](docs/16-external-trade-and-dependency.md).

## The production ladder: making it locally

§17 corrects §16's pessimism. Ranked by technical difficulty rather than
importance — five rungs, **none skippable** — two lethal-category goods are
locally producible today:

| Product | Capex | Why |
|---|---|---|
| **Medical oxygen** (PSA) | ~$105k | Made from **air**; proven in Kenya, Rwanda, Ethiopia at ~$7.34/patient |
| **Oral rehydration salts** | ~$18k | Sugar, salt, water |

Viability means saving more FX than the plant costs to run — six of sixteen
candidates fail that test and would leave the community *worse* off. APIs and
vaccines stay imported forever. Independence rises ~51% → **~60%**.

Prefer **dual-use plants**: everyday demand keeps them maintained until the
emergency arrives.

## Security: 65% mediation, 21% force

§18 models what community security actually does. Five rotating members
suffice. Two findings: **inspector collusion**, not instrument accuracy, is
what defeats fraud detection (93% → 20%), and rotation prevents capture only
within a narrow band — 9-month tours safe, 24-month tours catastrophic. A
2-of-5 armoury quorum fails outright if two keyholders collude.

One correction: the claim that police numbers don't affect crime is
contradicted by modern evidence. The real case for this model —
accountability, fit-to-task, cost, currency integrity — is stronger without
it.

## Defense: the citizen militia and asymmetric neutralization

§19 models territorial defense: **a mandatory, self-funded, self-equipped
citizen militia** operating on radical asymmetry rather than industrial mirror-copying.

| Dimension | Militia design | Strategic advantage |
|---|---|---|
| **Funding** | 100% self-funded personal kit | Zero military budget to corrupt; zero defense contractor lobbying |
| **Mobility** | 99.3% zero-fuel fleet (horses, pack mules, bikes, foot) | Zero fuel logistics tail; immune to fuel refinery blockade |
| **Arsenal** | Firearms + locally forged medieval weapons | Never runs out of bullets; blades crafted by village blacksmiths |
| **Neutralization** | Blinding & jamming rather than kinetic destruction | **$10 net/mud defeats $10M tank; $500 layered defense stops 100-drone swarm** |

Cost ratios against conventional weapons exceed **10,000:1 to 1,000,000:1**,
yielding a **2,500:1 daily burn rate advantage** ($10k/day vs $25M/day) that
exhausts any invading superpower. See [§19](docs/19-military-doctrine.md).

## Governance: the Competence Council and departmental enforcement

§20 establishes the macro-governance and administrative hierarchy: **functional
leadership selected on demonstrated competence rather than politics, voting, or monarchy.**

| Dimension | Governance design | Strategic advantage |
|---|---|---|
| **Selection** | 3-stage merit filter (10-yr ledger record $\rightarrow$ 75% peer consensus by 20–30 masters $\rightarrow$ 1-yr probation) | Eliminates political parties, voter ignorance, demagoguery, and mediocracy |
| **Hierarchy** | 11 functional Stewards (Reserves, Production, Health, Works, etc.) + 5–7 member War Council | Clean division of responsibility; collective defense command with mandatory female seats |
| **Succession** | Deterministic state machine (Deputy takes over instantly) | Zero power vacuums; institutional continuity |
| **Enforcement** | **Military Police (Provost) & Bureau Enforcers** | Halts looting, war crimes, arms diversion, and grain hoarding |
| **Measurement** | **Independent Continuous Measurement Bureaus** | Real-time telemetry reporting directly to Audit Board, eliminating Goodhart's Law |
| **Accountability**| Annual 20-citizen sortition jury audit + zero legal immunity | Ensures equal living standards (1.0 : 1.0) and prevents oligarchic capture |

See [§20](docs/20-competence-council-and-departmental-policing.md).

## Anti-corruption: difficulty diagnostics and resource curse eradication

§21 provides mathematical and structural controls against looting, false incompetence
accusations, and Dutch Disease:

| Threat | Systemic failure mode | RCU systemic safeguard |
|---|---|---|
| **Incompetence diagnosis** | Scapegoating leaders during droughts/shocks | **Difficulty-adjusted benchmarking:** compares outcomes against neighboring communities facing identical climate/blockade |
| **Succession failure** | Unprepared replacements failing in crises | **Shadow Leader System:** pre-trained Deputy undergoes 90-day quantitative probation ($\ge 80\%$ target pass rate) |
| **Phantom employment** | Bribes disguised as salaries (e.g. SA light-switcher) | **Production-based payroll & open books:** positions with zero measurable output are automatically eliminated |
| **Centralized looting** | Governors stealing federal grants (Nigeria) | **Decentralized treasuries & $5\times$ wealth ceiling:** value stays in producing domain warehouses; personal accumulation capped |
| **Resource Curse** | Single-commodity dependency crash (Oil boom/bust) | **20-commodity backing basket (HHI $< 1,200$):** prevents Dutch Disease; zero debt-financed vanity monuments |
| **Import monopolies** | Exclusive licensing charters (Cars, cement) | **Zero exclusive licensing & 20% market cap:** competition is mandatory default |

See [§21](docs/21-anti-corruption-and-resource-curse-prevention.md).

## Intelligence: the Research & Analysis Bureau (RAB)

§22 formalizes the state's central analytical organ: **the brain that connects
siloed departmental data into systemic reform.**

```
       DEPARTMENTS (Data) ──► RAB (Synthesis) ──► REFORM DESIGN (Solutions)
              ▲                                              │
              └────────────── COUNCIL RATIFICATION ──────────┘
```

| Division | Function | Deliverable |
|---|---|---|
| **Forensic Audit** | Scans transactions, inventory, and grading variance | Monthly Named Fraud Alerts to Justice |
| **Economic Analysis** | Monitors velocity, quotas, trade windows, and wealth concentration | Monthly Public Economic Dashboard & 6–12 mo Early Warnings |
| **Human Capital** | Difficulty-adjusted evaluation of leaders, educators, and apprentices | Quarterly Leadership Scorecards & Recall Alerts |
| **Reform Design** | Translates anomalies into costed, actionable 6-stage solutions | Pilot-tested cross-department structural reforms |
| **Science & Tech** | Applied local research (seeds, herbal assays, metallurgy, microgrids) | 4th-year apprentice research integration & domestic IP |

Staffed by **35–55 analysts per 10k population**, bounded by **zero arrest powers,
public open data, 2-year leadership rotation, and annual external audits**.
See [§22](docs/22-research-and-analysis-bureau.md).

## External intelligence & ecology: the Awareness Triangle

§23 eliminates the state's external and ecological blind spots through two dedicated organs:

```
                  ┌────────────────────────────────────────┐
                  │         THE AWARENESS TRIANGLE         │
                  ├───────────────────┬────────────────────┤
                  │ CIS (External)    │ EDMB (Ecological)  │
                  │ Traders, SIGINT,  │ Real-time sensors, │
                  │ OSINT, CI         │ EIA, Disaster Prep │
                  └─────────┬─────────┴──────────┬─────────┘
                            └─────────┬──────────┘
                                      ▼
                             RAB (Synthesis) §22
```

| Agency | Mandate | Operational Deliverables |
|---|---|---|
| **Community Intelligence Service (CIS)** | Looks outward; monitors foreign actors, military staging, and markets | Weekly Situation Reports (200km), drone RF alerts, and daily OSINT news digests |
| **Environmental & Disaster Bureau (EDMB)** | Real-time sensor monitoring, mandatory EIAs, disaster rescue, and reforestation | Flood/landslide early warnings, 75% Council EIA override rule, 3-to-1 tree replanting |

See [§23](docs/23-intelligence-and-environmental-disaster-management.md).

## The War Council & specialized strike units: asymmetric imperial defense

§24 formalizes the command architecture that allows a small community to defend itself against large expeditionary forces:
- **The War Council:** 8-seat deliberative collective command with a rotating chair, the 24-hour "No" delay rule, the 7/8 Blood Rule, and mandatory Community Council authorization for any offensive action.
- **The Scenario Library:** 10 pre-planned Roman contingency blueprints (S1–S10) updated quarterly and wargamed semi-annually.
- **The War Room:** 24–72 hour multidisciplinary crisis sessions solving operational deadlocks with no rank hierarchy, mandatory 6h sleep, and outside wildcard thinkers.
- **7 Specialized Units (155–195 personnel, <5% of militia):** Strike Team (decapitation), Hammer (shock assault), Scorpion (counter-drone), Worm (sappers/IEDs), Healer (trauma medical), Echo (signals/EW), and Horse (mounted recon).
- **Anti-Janissary / Anti-Mamluk Safeguards:** Elite in skill, not in status. Mandatory 3-year return to civilian economic production, no separate barracks, no separate pay, and no civilian political office while serving.

See [§24](docs/24-war-council-scenario-planning-and-specialized-units.md).

## Media, information integrity & social harm

§25 resolves the conflict between investigative press freedom (preventing corruption) and social harm prevention (stopping media circus and predatory commercial deception):
- **Governing Axiom:** *"Restrict the instructional and the deceptive. Do not restrict the depictive."*
- **Courtroom Dignity:** Zero cameras in courts; unconvicted suspects and victims anonymized; *sub judice* strictly enforced; public open written registries maintained.
- **Instructional vs Fiction:** Method details (suicide how-tos, shooter manifestos, hacking exploits) restricted; fiction, literature, and art protected without censorship.
- **Commercial Transparency:** Mandatory disclosure of paid sponsorships and filtered images; ban on influencer crypto/gambling promotions.
- **Source, Never Filter:** The state may publish an authoritative wire service, but is constitutionally prohibited from operating a monopoly content filter or owning media distribution channels.

See [§25](docs/25-media-information-integrity-and-social-harm.md).

## Honest positioning

**Genuinely novel:**
- Decay rate calibrated to the physical spoilage rate of the specific backing
  commodity — this gives Gesellian demurrage a physical referent for the
  first time, answering the "why 1% and not 2%?" objection
- Two tiers separating medium-of-exchange from store-of-value by construction
- Bearer warehouse receipts circulating at retail with offline verification

**Not novel, and should not be claimed as such:**
- Commodity-reserve currency (Benjamin Graham, 1937)
- Demurrage (Gesell; Wörgl, 1932–33)
- Warehouse receipt systems (Tanzania's Warehouse Receipts Act, 2005)
- Digital community currency at scale (Sarafu, Kenya)

Three defensible contributions beat seven unfalsifiable ones. A reviewer who
knows the literature dismisses an overclaim instantly.

**What the system cannot do:** back imports; avoid being political; eliminate
trust (it relocates it from a central bank to a warehouse inspector); or
survive its own success without a legal identity.

---

## Contributing

The most useful contributions are attacks. Annex B lists ten open problems
ranked by severity; the top three are potentially fatal and none has a clean
solution. If you can break a claim in the model, open an issue with the
parameters that break it.
