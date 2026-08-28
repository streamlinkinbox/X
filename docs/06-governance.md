# 6. Governance

## 6.1 The core problem

The system removes a central bank and replaces it with cooperatives and
inspectors. This does not remove the possibility of abuse — it relocates it.
The relevant question is never "is this decentralised?" but **"who can steal,
how much, and who would notice?"**

| Actor | Can steal by | Bounded by | Detected by |
|---|---|---|---|
| Inspector | Over-grading a deposit | Grade factor caps, dual grading | Peer variance statistics |
| Warehouse operator | Selling collateral | Performance bond | Re-inspection cycle |
| Cooperative board | Issuing beyond collateral | Ledger issuance ceiling | Checkpoint rejection |
| Key holder | Forging notes | Ledger ceiling (needs 2 failures) | Issuance rate alerts |
| Federation majority | Rewriting checkpoints | Nothing technical | Independently held old checkpoints |
| Local strongman | Seizing a warehouse | Nothing technical | Everyone, immediately |

The last two rows have no technical remedy. They are political problems and
require political answers.

---

## 6.2 Structure

```
                    FEDERATION ASSEMBLY
              (one cooperative, one vote)
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
   RULES BOARD      AUDIT BOARD      DISPUTE COUNCIL
   parameters       inspections      complaints
   9 members        7 members        5 rotating
   4-yr staggered   external maj.    lot-selected
        │
        └──> may not be members of any cooperative board
                          │
              ┌───────────┴───────────┐
         COOPERATIVES            INSPECTOR POOL
         issue notes             independently employed
         run warehouses          rotated across districts
         one member one vote     paid by federation, not coop
```

### The one structural rule that matters most

**Inspectors are employed by the federation, paid from a pooled fund, and
rotated between districts on a schedule they do not control.**

An inspector paid by the cooperative whose deposits they grade will
eventually grade generously. Not from malice — from the ordinary human
difficulty of telling your employer and your neighbour that their maize is
Grade C. Separating employment from the graded party is the single highest-
value governance decision in the entire design.

Rotation matters equally. An inspector who has worked one district for three
years knows everyone, and knowing everyone is exactly what makes independent
grading impossible.

---

## 6.3 One member, one vote — and its limits

The original design specifies one member one vote. Correct, but incomplete,
because it does not prevent capture. It prevents *capital-weighted* capture
while leaving *turnout-weighted* and *patronage-weighted* capture wide open.

Additional protections:

| Mechanism | Purpose |
|---|---|
| Quorum floor (33% of members) | Prevents a small organised faction deciding for everyone |
| Supermajority (67%) for parameter changes | Decay rates and haircuts cannot be changed by a bare majority |
| Sortition for the dispute council | Randomly selected members cannot be pre-bought |
| Term limits (two terms, non-consecutive) | Prevents entrenchment |
| Public roll of members | Prevents ghost members voting |
| External audit majority | The audit board cannot be captured from inside |
| Parameter change lag (90 days) | No emergency rule change benefits the people proposing it |

The 90-day lag deserves emphasis. **Most monetary capture happens through
emergency rule changes** justified by the emergency the capturers benefit
from. A mandatory delay between deciding and applying a parameter change
removes the profit from manufacturing crises.

---

## 6.4 Inspector integrity

Inspection is the system's foundation, so it is where attack effort will
concentrate.

**Controls, in descending order of effectiveness:**

1. **Published per-inspector variance statistics.** Every inspector's
   average grade, compared to peers, on comparable deposits, published
   monthly. An inspector running consistently high is visible in the data
   long before anyone can prove intent. Nearly free, and the most effective
   control available.
2. **Blind double grading** above a value threshold.
3. **Random cross-district re-grading** of 10% of deposits.
4. **Rotation** every 6 months.
5. **Adequate pay.** An inspector paid less than the value of a routine
   bribe is a design flaw, not a moral failing.
6. **Bonding.** Inspectors post a bond, forfeited on proven fraud.
7. **Anonymous reporting**, with the report going to the audit board, never
   to the local cooperative.

**On the original design's "inspectors chosen by the community":** this is
appealing and it is wrong. Community-chosen inspectors are embedded in local
patronage networks — which is precisely the relationship independence
requires them not to have. Better: **community-vetoed, federation-appointed.**
The community can reject an inspector it distrusts but cannot select a
favourite.

---

## 6.5 Dispute resolution

| Level | Who | Timeline | Scope |
|---|---|---|---|
| 1 | Warehouse manager | 24 hours | Grading, counting |
| 2 | Cooperative dispute officer | 7 days | Issuance, redemption |
| 3 | Dispute council (5, by lot) | 30 days | Fraud, impairment, inspector conduct |
| 4 | External arbitration | 90 days | Systemic; cross-cooperative |
| 5 | National courts | — | Available at every stage, never waived |

Level 5 must remain open. A system that requires members to waive access to
courts is a system that intends to abuse them. It also fatally undermines
the legal characterisation argued in Section 8.

---

## 6.6 Capture resistance: honest assessment

### What the design resists well

- **Capital capture** — one member one vote
- **Silent inflation** — the ledger ceiling makes over-issuance visible
- **Single-point corruption** — dual grading, threshold signing, rotation
- **Gradual drift** — parameter changes need supermajority plus 90 days

### What it resists poorly

**Armed seizure.** If a militia or a politically-connected businessman takes
a warehouse, the notes backed by it are worthless and no cryptography helps.
Mitigations are real but partial: many small warehouses rather than few
large ones; geographic dispersion of any one class's collateral;
cross-cooperative mutual insurance; and — most importantly — **never
concentrating enough value in one building to be worth taking by force.**

A useful design rule: **no single warehouse should hold more than 15% of any
class's collateral, and no more than 5% of total federation collateral.**

**Federation-level collusion.** If most cooperatives agree to inflate, they
can. The only defence is external: published checkpoints held by parties
outside the federation — a university, a diaspora association, a
journalists' network, a foreign NGO — any of whom can prove a rewrite by
producing an older signed root. **Cheap, low-tech, and effective**, and it
should be set up before the first note is issued, because it cannot be
retrofitted after a rewrite.

**Elite capture through legitimate channels.** The wealthiest producers
deposit the most, sit on boards, and shape parameters in their favour — all
without breaking a single rule. This is the hardest problem and it has no
clean solution. Partial mitigation: cap any single depositor at 10% of a
cooperative's issuance, and reserve board seats for smallholders by
deposit-size band.

**The founder problem.** In the early years the system depends on a handful
of people who understand it. That is unavoidable and it is also the classic
route by which cooperatives become fiefdoms. Mitigation: **written
succession from day one**, mandatory documentation, and a founder term limit
that is set before anyone knows who the founders will be.
