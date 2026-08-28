# 8. Legal and regulatory strategy

> This document is a strategic analysis, not legal advice. Every claim below
> must be verified with counsel qualified in the jurisdiction before any
> deposit is accepted.

## 8.1 The central legal question

Is an RCU note (a) a warehouse receipt, (b) a security, (c) electronic
money, (d) a deposit, or (e) a currency?

The answer determines whether the system is lawful, licensable, or criminal.
**It is also partly within the designers' control**, because legal
characterisation follows structure and language.

| Characterisation | Consequence | Verdict |
|---|---|---|
| **Warehouse receipt** | Licensable under existing Tanzanian law | **Target this** |
| Security | Prospectus, capital markets licensing | Avoid |
| E-money | Central bank licence, capital requirements | Avoid in Phase 1 |
| Deposit-taking | Banking licence; almost certainly unobtainable | **Fatal — avoid** |
| Currency | Likely unlawful; counterfeiting statutes may apply | **Fatal — avoid** |

---

## 8.2 The warehouse receipt route

Tanzania's **Warehouse Receipts Act No. 10 of 2005** (amended by Act No. 3 of
2015, with 2016 Regulations) already establishes exactly the infrastructure
this system needs:

- The **Warehouse Receipts Regulatory Board (WRRB)** licenses warehouse
  operators, inspectors and collateral managers
- Warehouses must carry insurance and post a performance bond
- Negotiable receipt books are approved by the Board
- The system covers 18 commodities across 23 regions and has operated for
  two decades, handling hundreds of thousands of tonnes annually
- The WRRB has been digitising, so electronic records are not an alien
  concept to the regulator

**A licensed warehouse issuing negotiable receipts against graded, insured,
inspected commodity deposits is not doing anything novel.** It is doing
exactly what the Act contemplates.

### What makes an RCU note different from a standard receipt

| Standard receipt | RCU note | Legal risk |
|---|---|---|
| One receipt, one deposit | Denominated into standard units | Moderate — is it still a receipt? |
| Named depositor | Bearer | Moderate — negotiability is provided for |
| Held for finance or sale | Circulates hand to hand | **High — this is the moneyness problem** |
| Fixed quantity claim | Decaying value claim | Low — quantity claims can vary |
| Redeemed by depositor | Redeemed by any holder | Moderate |

The high-risk row is the real one. **Denomination plus bearer status plus
circulation is what makes something look like currency.** A regulator will
not be fooled by calling it a receipt.

### The mitigation

Structure the instrument so that each note is, in substance and in
documentation, a **negotiable bearer warehouse receipt for a specific
quantity of graded commodity**, and:

- Denominate in **commodity units first** ("50 kg Grade A maize"), with the
  RCU figure secondary and explicitly labelled as an indicative value
- Never describe it as currency, money, legal tender, or a means of payment
  in any document, sign, or app screen
- Preserve genuine physical redemption — the right must be real and used
- Keep the RCU/shilling relationship floating and unquoted by the
  cooperative; if the system quotes an exchange rate, it is running a
  currency

**Language discipline is a legal control, not a presentational one.** The
word "currency" in a founder's public statement is admissible evidence about
what the instrument is.

---

## 8.3 What triggers a banking licence

The bright line: **accepting money from the public, repayable on demand.**

RCU accepts *commodities* and returns *commodities*. That is warehousing,
not deposit-taking. The line is crossed if the system:

- accepts shillings in exchange for notes (**never do this**)
- pays interest on holdings (never)
- lends against note balances (never in Phase 1–2)
- guarantees a fixed shilling value (never)
- operates an exchange bureau (never)

**Do not accept national currency, ever, at any gate.** Commodity in,
commodity out. This one rule keeps the system on the correct side of the
most dangerous line in financial regulation, and it should be treated as
inviolable rather than as a Phase 1 convenience.

---

## 8.4 Payment systems law

At scale, transfers between users start to look like a payment service. The
mitigations:

- Peer-to-peer transfer is **transfer of a bearer instrument**, the same as
  handing over a receipt — the system does not hold or move funds
- **Because transfers are not recorded** (Section 5.3), the cooperative is
  not operating an account-based payment system
- The app is a *verification tool*, not a wallet holding value on the
  operator's books

The privacy decision in Section 5.3 was made on human-rights grounds. It
turns out to also be the strongest available payment-systems defence: **an
operator that does not record transfers is not operating a transfer system.**
Two independent arguments converging on the same design is a good sign.

---

## 8.5 Engagement strategy

The original blueprint advises staying quiet and growing organically, and
warns against provoking the IMF or World Bank. This is half right and half
dangerous.

### What is right

Do not announce a challenge to the shilling or the dollar. Nothing invites
suppression faster than framing a project as monetary insurgency. Wörgl was
shut down in thirteen months at a scale of 12,000 schillings — not because
it failed, but because it worked and was visible.

### What is wrong

**Growing quietly and hoping not to be noticed is not a strategy; it is a
deferred crisis.** A system that reaches 100,000 users has been noticed. The
only question is whether the regulator first learns about it from you or
from a hostile newspaper story.

### Recommended posture: loud about the boring parts, quiet about the
### ambitious parts

| Talk about | Do not talk about |
|---|---|
| Post-harvest loss reduction | Replacing the central bank |
| Farmer price improvement | Currency competition |
| Warehouse receipt digitisation | Monetary sovereignty |
| Financial inclusion | De-dollarisation |
| Tax formalisation of informal trade | Independence from the state |

Every item in the left column is true, verifiable, and aligned with stated
national policy. Every item in the right column is also true — and saying
it out loud converts a development project into a political threat.

### Sequenced engagement

| Phase | Engage | Ask for |
|---|---|---|
| Pre-pilot | WRRB, district authority | Warehouse licences under existing law |
| Pilot | Ministry of Agriculture, cooperative registrar | Recognition as a cooperative marketing scheme |
| Year 2 | Central bank — **proactively** | A no-objection letter or regulatory sandbox |
| Year 3 | Revenue authority | Withholding-agent status for gate levies |
| Year 5 | Legislature | Amendment recognising denominated negotiable receipts |

**The Year 2 central bank approach is the crucial one, and the instinct to
delay it is wrong.** Arriving voluntarily, with data, framed as warehouse
receipt innovation, before the system is systemically significant, is
survivable. Being summoned after a newspaper describes it as a shadow
currency is not.

---

## 8.6 Cross-border

Phase 2 contemplates cross-border trade. This multiplies legal complexity by
far more than the number of countries involved:

- A note issued in Tanzania and redeemed in Burundi is an **export of goods**
  and probably a **cross-border payment**
- Anti-money-laundering obligations attach to cross-border value transfer in
  effectively every jurisdiction
- Bearer instruments crossing borders attract customs and AML attention
  automatically and unfavourably
- EAC harmonisation helps with goods; it does not help with a novel
  instrument

**Recommendation: defer cross-border to Phase 3 at the earliest**, and then
implement it as *inter-cooperative settlement between separately licensed
national entities* rather than as notes physically crossing the border. The
note stays in its country; the cooperatives settle with each other.

---

## 8.7 The AML/CFT problem

Stated plainly because it is the objection most likely to end the project,
and the original blueprint does not address it at all.

An anonymous, bearer, transferable instrument with untracked transfers is —
accurately — described in regulatory language as a money-laundering
vehicle. This is not a misunderstanding to be corrected; it is a correct
observation about the instrument's properties.

**The available answers:**

1. **Identity at the gates.** Issuance and redemption above a threshold
   require registered identity. Circulation in between is anonymous —
   exactly like cash, which is legal everywhere.
2. **Denomination caps.** No note above 1,000 units. Large-value anonymous
   bearer instruments are what regulators actually object to.
3. **Aggregate reporting.** Report totals, not individuals.
4. **Physical constraint as a natural cap.** Laundering through RCU requires
   moving physical commodity through inspected warehouses. It is a
   remarkably inefficient laundering channel — moving a million units means
   moving hundreds of tonnes of maize past two inspectors.
5. **Voluntary suspicious-activity reporting** by cooperatives.

Point 4 is the genuinely strong argument and should lead the conversation:
**the commodity backing that makes the currency real also makes it a poor
laundering vehicle.** Criminals prefer instruments that are light, dense in
value, and do not require a forklift.
