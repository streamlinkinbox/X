# 12. Bundle pricing, dual-price receipts, and the hoarding question

Three refinements that change the system substantially. The first solves a
problem Annex B rated **potentially fatal**.

---

## 12.1 A price is a bundle, not a number

Prices are quoted as **baskets of commodity claims**, not as a single
fungible amount:

> **House, 3 rooms, Kigoma:** 100 iron + 500 wood + 40 plastic

Not "640 units." The seller says *which real goods* they want. They are
building a house extension, so they want timber; they need roofing sheets,
so they want iron.

### Why this is more than presentation

Under a single-number price, a buyer pays with whatever they hold. Under a
bundle price, they must tender **those specific classes**. That difference
turns out to be the mechanism that fixes demurrage arbitrage (§12.3).

It also restores something a single number destroys: **the seller's actual
needs re-enter the transaction.** This is barter's real advantage, and it is
what the system's own description — *"essentially barter with printed
currency"* — is reaching for. The notes provide divisibility, portability
and delayed settlement, which barter lacks. The bundle preserves the
matching of real needs, which money normally erases.

### Quote in face, settle in value

The rule that makes bundles work with decay:

- **Prices are quoted in fresh-note equivalents.** "500 wood" means 500
  units of undecayed wood-note value.
- **Tendered notes are credited at their current decayed value.**

So a buyer paying with 18-month-old wood notes must hand over **more** of
them. From the model: 500 units of demand, settled with notes issued 18
months earlier, leaves a shortfall of 43.35 units — the buyer needs roughly
548 face units to settle 500.

This keeps posted prices stable (a seller can chalk a price on a board and
leave it) while making note age cost the holder at the moment of payment.
Quoting in decayed value would make every posted price a moving target;
ignoring decay at settlement would make demurrage fiction. **This is the
only combination that works.**

---

## 12.2 The dual-price receipt

Every quote shows the **asked** bundle beside an independently assessed
**reference** bundle, so the buyer can see the markup:

```
+----------------------------------------------------+
| House, 3 rooms, Kigoma district                    |
+----------------------------------------------------+
| ASKED         ASSESSED        DIFFERENCE           |
|    100 FE stable     20 FE           +400%         |
|     40 PL decays      5 PL           +700%         |
|    500 WD decays    200 WD           +150%         |
+----------------------------------------------------+
| TOTAL ASKED               640 units                |
| ASSESSED VALUE            225 units                |
| MARKUP                 +184.4%                     |
| VERY HIGH MARGIN — CHECK OTHER SELLERS             |
+----------------------------------------------------+
| Bundle: 84% decaying / 16% stable                  |
| Unsold: loses value from month 13; 87% at 24 mo    |
+----------------------------------------------------+
```

A fair transaction looks entirely different:

```
+----------------------------------------------------+
| 20 kg tomatoes                                     |
+----------------------------------------------------+
| ASKED         ASSESSED        DIFFERENCE           |
|      8 FP decays      8 FP             +0%         |
|     12 GR decays     11 GR             +9%         |
+----------------------------------------------------+
| TOTAL ASKED                20 units                |
| ASSESSED VALUE             19 units                |
| MARKUP                   +5.3%                     |
| AT OR BELOW ASSESSED VALUE                         |
+----------------------------------------------------+
```

### Per-class markup is the sharpest tool here

The house receipt shows something a single total would hide: the seller is
marking up **plastic by 700%** while wood is only +150%. The buyer can now
negotiate the specific component that is out of line, or offer a different
bundle. **Aggregate markup tells you that you are being overcharged;
per-class markup tells you where.**

### Where the reference price comes from

This is the hard part, and it is the system's existing open problem P4
(price discovery in thin markets) wearing a new hat.

| Source | Use | Weakness |
|---|---|---|
| Weekly committee index | Commodities | Committee can be captured |
| Recent comparable redemptions | Commodities | Needs volume |
| Recent comparable sales | Houses, land, livestock | Few comparables in a village |
| Cost-of-inputs build-up | Manufactured goods, buildings | Ignores scarcity and location |
| Seller's own declared cost | Anything | Self-reported, gameable |

**For fungible commodities the reference is reliable.** For a house it is
not: no two houses are comparable, and a thin market has no index. The
honest treatment is to **grade the reference by confidence** and print that
grade on the receipt:

| Confidence | Basis | Printed as |
|---|---|---|
| High | ≥10 comparable transactions in 90 days | "assessed value" |
| Medium | 3–9 comparables, or input-cost build-up | "estimated value" |
| Low | <3 comparables | "rough guide only" |

Printing a confident-looking number for a house valuation nobody can
substantiate would be worse than printing nothing — it would give a
manipulable figure the authority of an official assessment.

### What this fixes, and what it does not

**Fixes:** information asymmetry against buyers who do not know local prices
— newcomers, the young, the isolated, and anyone buying something they buy
rarely. This is a real and common form of exploitation.

**Does not fix:** a seller with genuine market power. If there is one house
for sale, the receipt says "+184%" and the buyer still has no alternative.
**Transparency constrains prices only where competition exists.** The
receipt makes the markup *visible*; it does not make it *avoidable*.

It may also produce an effect worth watching: if reference prices become the
social norm for a fair price, they may **compress legitimate margins** for
sellers who add real value through transport, storage or risk-bearing. A
trader who buys maize in a surplus village and sells in a deficit one is
performing a service, and their markup is not theft. The receipt should
therefore show a **margin allowance** for transport and storage, not a bare
comparison.

---

## 12.3 Bundle pricing solves the hoarding-arbitrage problem

This is the significant result.

### The problem restated

Annex B's problem P1: with a free choice of payment medium, sophisticated
holders keep Tier B (stable) notes and spend Tier A (decaying) notes.
Demurrage falls on the unsophisticated. The design's purpose inverts.
Rated **potentially fatal, no clean solution known.**

### The test

Two agents, identical starting holdings, identical payment demands over 24
months. The only difference: the sophisticated agent chooses which notes to
part with, where the rules permit choosing.

| Payment rule | Sophisticated loss | Naive loss | Burden ratio |
|---|---|---|---|
| Free substitution (original design) | 8.3 | 17.9 | **2.16** |
| Strict bundles (this proposal) | 17.2 | 17.2 | **1.00** |

**Under free substitution the naive holder bears 2.16× the demurrage. Under
strict bundle pricing the burden is exactly equal.**

The mechanism is simple. If a seller demands 500 *wood* notes, a hoarder
holding only iron cannot pay. They must obtain wood notes — and the only way
to obtain them is to sell something, which means re-entering circulation. If
they hold wood notes long enough to be useful for payment, those notes decay
in their hands. **Either way the hoarder pays.** The result holds across
demand mixes from 30% to 70% Tier A.

### The critical caveat: partial adoption is worse than none

Bundle pricing only works if sellers actually insist. Testing partial
enforcement produces a genuinely surprising result:

| Share of sellers insisting on exact bundles | Burden ratio |
|---|---|
| 0% | 2.16 |
| 25% | **2.41** |
| 50% | 1.54 |
| 75% | 1.19 |
| 100% | 1.00 |

**At 25% adoption the outcome is worse than doing nothing at all.**

The reason is that a sophisticated holder routes around a minority of strict
sellers — they simply trade with the 75% who accept substitution, dumping
decayed notes there, while the strict sellers are avoided. Partial
enforcement concentrates the burden on the flexible sellers rather than
spreading it.

**This is the single most important operational finding in this document.**
Bundle pricing must be the default and near-universal convention from launch,
or it should not be introduced at all. A gradual rollout passes directly
through the region where it does harm.

Practical implication: **the wallet app must quote bundles by default**, the
cooperative must pay its own obligations in bundles, and anchor acceptors
must commit to bundle quoting as a condition of joining. Convention, not
enforcement, is the delivery mechanism — but the convention has to be
established at once.

---

## 12.4 Hoarding: what the system actually prevents

Your position, restated precisely: *the rich may hoard real goods — cattle,
land, iron — but they cannot hoard the money itself.*

This is correct, and it is a sharper claim than the original blueprint's
"wealth hoarding: impossible."

### What is prevented

| Behaviour | Prevented? | Mechanism |
|---|---|---|
| Sitting on idle currency | **Yes** | Demurrage on Tier A; custody fees on Tier B |
| Paying only in decayed notes | **Yes** (with bundles) | Seller specifies classes |
| Accumulating currency claims on food while others starve | **Yes** | Grain notes decay; the grain itself must move |
| Using currency scarcity to depress producer prices | **Partly** | Issuance is tied to production, not to a lender's willingness |

### What is not prevented, and should not be

| Behaviour | Prevented? | Why not |
|---|---|---|
| Owning many cattle | No | Cattle are productive capital; they reproduce and feed people |
| Owning land | No | Outside the monetary system entirely |
| Stockpiling iron sheets | No | Storage costs money; it is an investment, not hoarding |
| Building a business | No | This is the desired outcome |

**The distinction is between hoarding a *claim* and holding an *asset*.** A
warehouse of iron sheets is doing something: it cost money to fill, it costs
money to hold, and it will eventually become roofs. A pile of currency is
doing nothing except waiting for someone else's distress.

This is a genuinely coherent position, and it is more defensible than
attempting to prevent wealth accumulation as such. The system does not
attack wealth. It attacks the specific power that comes from **holding the
medium of exchange while others need it** — the power to buy cheap at
harvest because the seller has no cash and cannot wait.

### The honest limit

A sufficiently wealthy person converts currency to land and cattle and is
untouched by any of this. **The system does not produce equality; it
removes one specific lever of exploitation.** Overclaiming here would be
easy and would be wrong.

There is also a real second-order risk: if holding currency is costly and
holding cattle is not, capital flows into **real assets, bidding up their
prices.** Land and livestock could become more expensive relative to
everything else, which harms exactly the landless poor the system is meant
to serve. Gesell anticipated this and proposed land reform alongside
demurrage. **This deserves monitoring from Phase 1** — track land and
cattle prices against the reference basket, and treat sustained divergence
as a warning.

---

## 12.5 "Essentially barter with printed currency"

This framing is the most useful sentence in the whole concept, and it should
lead the public explanation of the system.

### Why it is strategically valuable

Every hard question about the system becomes easy under this framing:

| Question | Answer under the barter framing |
|---|---|
| "Is this a currency?" | No — it is a receipt for goods you can trade |
| "Do you need central bank approval?" | Warehouse receipts are already lawful |
| "What backs it?" | The goods. Go and look at them |
| "What if the issuer fails?" | The goods are still there and still yours |
| "Why does it lose value?" | Because the maize behind it is spoiling |
| "Are you replacing the shilling?" | No — you can already barter maize; this makes it practical |

The last row matters most. **Barter is legal everywhere and threatens no
one.** A farmer swapping maize for timber requires no licence. This system
does exactly that, with a receipt standing in for the sack so the two
parties do not need to meet, want each other's goods simultaneously, or
transport anything.

This is not a rhetorical dodge. It is a substantively accurate description
of what the instrument is, and §8's entire legal strategy depends on it
being accurate.

### What money adds to barter

| Barter's problem | How RCU solves it |
|---|---|
| Double coincidence of wants | Receipts circulate; you need not want what the seller has |
| Indivisibility | Notes are denominated; you can pay half a goat |
| Transport | The goods stay in the warehouse |
| Timing | You can hold the claim and spend later |
| Valuation | The reference index gives a common measure |

And what it deliberately does **not** add: unlimited accumulation without
cost. Barter has never allowed anyone to hoard wealth in a form that does
not rot, rust or need feeding. **RCU restores that property to money**,
which is the entire idea in one sentence.

### The framing's limit

Barter does not require trust in an issuer; RCU does. When you swap maize
for timber you inspect the timber. When you accept a wood note you are
trusting a warehouse, an inspector and a cooperative. **RCU is barter with
the frictions removed and a trust requirement added back.** That is a good
trade, but it is a trade, and it should not be described as costless.

---

## 12.6 Implementation

### Changes to the note and app

- Wallet displays holdings **by class**, never as one total. A single total
  would silently reintroduce the fungibility that bundle pricing removes.
- Quote builder: sellers construct bundles; the app fetches reference prices
  and computes markup automatically.
- Settlement screen shows required face value versus tendered current value,
  with the age shortfall stated explicitly.
- Receipts are printable on a thermal printer and renderable over USSD in
  abbreviated form.

### Changes elsewhere in the design

| Section | Change |
|---|---|
| §1.2 two tiers | Add: bundle pricing is what makes the two-tier split safe |
| §3 issuance | Price committee must publish reference prices with confidence grades |
| §7 fees | Reference-price publication is a cost centre; fund it from gate levies |
| Annex B P1 | Downgrade from "potentially fatal, no solution" to "solved, conditional on near-universal adoption" |
| Annex B P4 | Elevate: price discovery now carries more weight, since receipts depend on it |

### New risks introduced

| Risk | Severity | Mitigation |
|---|---|---|
| Partial bundle adoption worsens arbitrage | **High** | Launch as universal default; anchor acceptors commit |
| Reference prices captured by committee | High | Publish sources; multiple independent indices; open method |
| Bundle matching fails — buyer lacks the demanded classes | Medium | Cooperative acts as class exchange of last resort, at a spread |
| Complexity deters users | Medium | App defaults to a sensible bundle; only sellers who care customise |
| False precision in reference prices for unique goods | Medium | Confidence grades printed on every receipt |

**The class-exchange risk deserves attention.** If a buyer holds grain notes
and the seller wants wood, someone must convert. If the cooperative provides
that service it becomes a market maker holding inventory risk — and a
market maker that sets the spread is a price-setter, which is precisely the
concentration of power the design avoids elsewhere. **Cap the spread
publicly, and publish every conversion.**
