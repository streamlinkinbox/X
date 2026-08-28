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
