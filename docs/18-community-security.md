# 18. Community security and forensics

The security proposal is **largely sound**, and its strongest insight is one
it underplays: most of this work is **mediation and fraud forensics, not
force**. That is quantified below.

One doctrinal claim must be corrected, because building on a false premise
would weaken the argument rather than strengthen it.

---

## 18.1 What must be corrected

> *"Studies show increasing police numbers has almost no effect on crime."*

**This is not what the modern evidence says**, and the claim should be
dropped.

Quasi-experimental work using federal hiring grants as a natural experiment
finds meaningful effects: a crime-police elasticity around **−1.17** on
cost-weighted crime, roughly **−1.3 for violent crime** and **−0.8 for
property crime**, with an estimate that one life is saved per ~9.5
additional officers. Chalfin and McCrary find each dollar spent on police
associated with about **$1.60** in reduced victimisation costs.

**Why this matters for the design, rather than being an academic quibble:**
if you argue for community security on the false premise that policing does
nothing, then the first person who cites this literature demolishes your
case — and with it, the parts that are genuinely right.

### The argument that actually survives scrutiny

The case for a community security cooperative does **not** rest on policing
being ineffective. It rests on four claims that are all defensible:

1. **Accountability.** Whoever pays and can dismiss the force controls it.
   The Pinkertons, company towns, warlords and modern private military
   companies are the historical record, and it is damning.
2. **Fit to task.** The actual workload is 65% mediation, 14% forensics, 21%
   anything involving force. Equipping and training for the 21% while
   neglecting the 79% is the error most policing makes.
3. **Cost.** A district cannot afford a professional force. It can staff a
   rotating one.
4. **Currency integrity.** The commodity currency has a specific enforcement
   need — grade, weight and counterfeit fraud — that no state police force
   will ever prioritise. **This is the genuinely novel function.**

Note that claim 1 cuts both ways and should be stated honestly: a
community-controlled force is captured by whoever controls the community.
§6's protections apply here with more force, not less, because this body
carries restraints.

---

## 18.2 What the work actually is

Modelled for a community of 1,000, using incident rates typical of a rural
district with an active commodity market:

| Category | Hours/year | |
|---|---|---|
| Commercial disputes | 140 | |
| Family and neighbour conflict | 121 | |
| Land and livestock | 110 | |
| Theft | 60 | force |
| **Quality fraud** | **59** | forensic |
| Assault | 40 | force |
| **Counterfeit / ledger** | **22** | forensic |
| Serious violent | 20 | force |
| **Total** | **573** | |

| Function | Share |
|---|---|
| **Mediation** | **64.8%** |
| **Forensics** | **14.2%** |
| Anything involving force | **20.9%** |

**Nearly four-fifths of the work involves no force at all.** This should
determine selection, training and equipment — and it means the most
important qualification is patience and credibility, not physical capability.

### Roster sizing

573 hours a year sounds like one person. It is not, because **coverage sets
the roster, not caseload**: someone must be reachable at any hour, and
rotating part-time members are available a fraction of the time.

| Population | Hours/yr | Members |
|---|---|---|
| 500 | 286 | 5 |
| 1,000 | 573 | 5 |
| 3,000 | 1,718 | 5 |
| 20,000 | 11,453 | 13 |

**5 members is the floor** for any community, driven purely by on-call
coverage. This is smaller than the 15–25 proposed, and the difference
matters: a smaller force is cheaper, easier to hold accountable, and less
likely to become a class.

---

## 18.3 Forensics: the function that protects the currency

This is the part of the proposal that is most original and most necessary.
Grade fraud does not merely cheat one buyer — **it undermines every note of
that class simultaneously**, because the note's value is a claim on graded
goods.

### Does layered verification work?

Modelling 100 fraud attempts against §3's dual inspection, §3.2's random
audit, and consumer-level testing:

| Layer | Caught |
|---|---|
| Dual inspection at deposit | 81.9 |
| Random audit (10% of batches) | 1.6 |
| Consumer verification | 2.1 |
| **Undetected** | **14.4** |

**Detection is 85.6%.** Single-inspector control would catch 76.1%.

Two findings follow, and the second is the important one.

### Finding 1: audit effort has weak returns

| Audit coverage | Detection |
|---|---|
| 0% | 84.2% |
| 10% | 85.6% |
| 20% | 87.0% |
| 40% | 89.9% |

Quadrupling audit effort buys under 5 points. **Auditing is a backstop, not
a primary control.** Do not spend the budget there.

### Finding 2: collusion is the whole game

| Inspector collusion rate | Detection |
|---|---|
| 0% | **92.8%** |
| 10% | 85.6% |
| 25% | 74.7% |
| 50% | 56.6% |
| 100% | **20.4%** |

**Dual inspection is worth exactly as much as the independence of the two
inspectors, and nothing more.** With full collusion the system is barely
better than no inspection at all.

This validates §6.4's controls and makes them non-negotiable rather than
best-practice: **inspectors employed by the federation, rotated between
districts on a schedule they do not control, with published per-inspector
variance statistics.** Two inspectors from the same village who work together
every week are not two inspectors — they are one, with a second signature.

### The forensic toolkit

Cheap, field-usable, no laboratory:

| Tool | Detects |
|---|---|
| Moisture meter | Wet grain sold as dry — the commonest fraud |
| Calibrated scale | Short weight |
| Sieve set | Stones, dirt, adulterants |
| Refractometer | Sugar content, dilution |
| Magnet and file | Metal substitution |
| Sealed reference samples | Grade disputes, settled by comparison |
| Phone with ledger app | Batch history, inspector IDs, original grades |

The last item is what makes this different from ordinary inspection: **the
digital record gives an objective baseline**. The dispute stops being "he
said, she said" and becomes a comparison against a signed record of what was
deposited, by whom, at what grade, on what date.

---

## 18.4 Rotation: does it actually prevent capture?

The proposal's central safeguard is rotation. Modelling influence as
accumulating during service and decaying during ordinary work:

| Tour | Break 12 mo | Break 18 mo |
|---|---|---|
| 6 months | safe (0.07) | safe (0.07) |
| 9 months | safe (0.12) | safe (0.08) |
| 12 months | safe (0.63) | safe (0.10) |
| **18 months** | **CAPTURED (6.7)** | safe (0.89) |
| 24 months | CAPTURED (44.5) | CAPTURED (5.3) |
| 36 months | CAPTURED (239) | CAPTURED (44.5) |

**Rotation works, but only within a narrow band.** Maximum safe tour is
about **18 months, and only with an 18-month break.** Recommended:

> **9-month tours, 18-month breaks.** Comfortably inside the safe region
> with margin for the model being wrong.

Note the non-linearity: 12-month tours are safe, 24-month tours are
catastrophic. **This is not a parameter to relax under operational
pressure** — and operational pressure to extend tours ("he's the only one who
knows the job") is exactly how it will be relaxed.

---

## 18.5 The armoury

The proposal's two-person rule needs one correction.

| Keyholders | Quorum | Corrupt | Unauthorised release |
|---|---|---|---|
| 5 | 2 | **2** | **CERTAIN** |
| 5 | 3 | 2 | 5% |
| 7 | 3 | 2 | 5% |
| 7 | 4 | 3 | 5% |

**A 2-of-5 rule fails completely if any two keyholders collude** — and two
people agreeing is not an exotic scenario.

> **Rule: quorum must exceed the plausible number of colluding keyholders.
> Use 3-of-7, never 2-of-5.**

Additional controls, all cheap:

- **Time delay.** 30 minutes between authorisation and release. Enough to
  stop a heated decision; not enough to matter in a genuine emergency.
- **Automatic notification.** Opening the armoury alerts the whole council,
  not just the keyholders.
- **Keyholders are not security members.** Whoever holds the keys should not
  be whoever wants the weapons.

### On not carrying firearms daily

The proposal's position is correct and the workload data supports it: 79% of
the work involves no force, and the categories that do are overwhelmingly
theft and simple assault, where a firearm escalates rather than resolves.

**The strongest argument is not philosophical but practical:** a member who
carries a weapon into 573 hours of mediation work each year will eventually
use it in a dispute about a goat.

---

## 18.6 On the defence force question

The source document's analysis of armies is **the most honest section in
it**, and its conclusion should be adopted without softening:

> *"You cannot build an army that fights for 'what's right' in the abstract.
> This has been tried thousands of times and has never succeeded long-term."*

That is correct. The structural reasons given — violence changes people, the
ruthless rise, armies need enemies, whoever holds the guns defines justice,
and tribalism is the most reliable motivator — are all well-founded.

**This blueprint's position:** community security as described here is in
scope. **A defence force is not.**

The reasons are specific to this project rather than general pacifism:

1. **It breaks the legal strategy.** §8 depends on RCU being a licensed
   warehouse receipt operation. An armed wing makes it a militia, and every
   legal protection evaporates the same day.
2. **It cannot achieve its stated purpose.** No community defence force has
   ever defeated a national army in open combat. The proposal admits this.
3. **It is the most likely route to capture.** §6.6 already identifies armed
   seizure as the risk with no technical remedy. Creating an armed body
   inside the cooperative supplies the means to whoever captures it.
4. **It changes what the project is.** A warehouse cooperative with a militia
   is not a currency experiment; it is a political-military formation, and
   will be treated as one by everyone including its neighbours.

If a community faces genuine armed threat, that is real and this document
has nothing useful to offer. It is a different project, run by different
people, and **the currency system should not be inside it** — because if the
armed formation is defeated or outlawed, the grain and the notes go with it.

**Keep the warehouse boring. Boring survives.**

---

## 18.7 Integration and accountability

| Function | Body | Accountable to |
|---|---|---|
| Mediation | Security cooperative | Dispute council (§6.5) |
| Fraud forensics | Security cooperative + inspectors | Audit board |
| Grading | Federation inspectors (§6.4) | Published variance statistics |
| Judgement | Community council | Assembly |
| Armoury custody | Separate keyholders | Council, auto-notified |

**The people who investigate must never be the people who judge.** The
proposal states this and it is correct — it is the single most important
structural separation in the whole security design, and the one most likely
to erode quietly.

Adopting the source document's accountability list, with the model's
corrections:

- Complaints heard by rotating ordinary members, never by other security
  members
- All interactions recorded; council may review any footage
- Every detention and use of force logged in the digital system
- **9-month tours, 18-month breaks** (corrected from 6–12 months)
- Removal by council majority, no appeal, no job security
- Equal pay and living conditions — no separate class
- Failures treated as diagnostics (§14.5), not merely as individual guilt

---

## 18.8 New risks

| Risk | L | I | Score | Mitigation |
|---|---|---|---|---|
| **Inspector collusion defeats dual verification** | 3 | 5 | **15** | Federation employment, cross-district rotation, published variance |
| **Armoury quorum too small; weapons released** | 2 | 5 | **10** | 3-of-7 minimum; time delay; keyholders separate from members |
| Rotation extended under operational pressure | 4 | 4 | **16** | Tour length is a constitutional parameter needing 90-day supermajority |
| Security body becomes a defence force | 2 | 5 | **10** | Explicitly out of scope; would void the legal strategy |
| Mediation function neglected for policing glamour | 3 | 3 | 9 | Selection and training weighted to the 79% |
| Community-controlled force captured with community | 3 | 4 | 12 | §6 protections; external checkpoint holders |

---

## 18.9 Summary

**Adopt:** community ownership; rotation; no daily firearms; mediation as the
primary function; forensic fraud investigation; body cameras and logging;
investigators separate from judges; failures as diagnostics.

**Correct:**
- **Drop the claim that police numbers don't affect crime** — modern evidence
  contradicts it, and the real argument (accountability, fit-to-task, cost,
  currency integrity) is stronger without it.
- **5 members, not 15–25.** Coverage sets the roster; the work is 573 hours.
- **9-month tours with 18-month breaks.** Beyond 18 months the model shows
  capture, and the transition is sharp.
- **3-of-7 armoury quorum, not 2-of-5.** Two colluding keyholders defeat a
  two-person rule with certainty.
- **Collusion, not accuracy, is the binding constraint on fraud detection.**
  Independence of inspectors is worth more than better instruments.

**Reject:** a defence force. Correct analysis, right conclusion — and it
belongs outside this project, because an armed wing would void the legal
strategy that keeps the warehouse open.

**The deepest point in the proposal deserves repeating:** *the people who
hold the guns should never be a separate class from the people who grow the
food.* The rotation model is how that becomes structural rather than
aspirational — and the modelling says it works, within a band narrower than
anyone would guess.
