# 13. Weight denomination and provenance

**This section supersedes the value-denominated design in §1.1.** It is the
most consequential revision in the document, and it makes the system simpler
rather than more complex.

---

## 13.1 The change

| | Value denomination (old) | Weight denomination (new) |
|---|---|---|
| A note says | "100 units, backed by maize" | "**100 kg maize**, Grade A" |
| Issuance requires | Somebody to price the maize | **A scale** |
| Price of goods | Quoted in units | **Whatever buyer and seller agree** |
| Who sets value | A committee | **Nobody** |
| Haircut covers | Price risk + physical risk | **Physical risk only** |

The note stops being a *claim on value* and becomes a *claim on matter*.
1 kg of iron is 1 metal unit. It was 1 kg of iron last year and it will be
1 kg of iron next year.

### What this removes

The system previously needed a weekly committee to decide what a tonne of
maize was worth. That committee was the design's most capturable
institution: **whoever sets the reference price controls how much currency
every deposit creates.** Annex B rated this problem P4 and I raised its
severity when receipts started depending on it.

Weight denomination deletes the institution. There is no reference price to
capture because there is no reference price. Issuance is arithmetic
performed on a scale reading, and two honest inspectors with the same scale
get the same answer.

**The buyer decides prices. The scale decides issuance. These are now
separate questions, and only the second one is the system's business.**

---

## 13.2 The haircut collapses

Under value denomination, notes had to be issued against ~70% of assessed
value because a price fall could leave the series undercollateralised. A
note promising *1 kg of iron* is not broken by a fall in the iron price —
it still claims 1 kg of iron, and 1 kg of iron is still in the shed.

The haircut therefore only has to cover what physics takes: weighing error,
moisture variation, and shrinkage between inspections.

| Class | Price-risk haircut (old) | Physical haircut (new) | Freed |
|---|---|---|---|
| Grains | 30% | **8%** | 22 pts |
| Iron & Steel | 20% | **4%** | 16 pts |
| Precious Metals | 10% | **1%** | 9 pts |
| Stone & Marble | 40% | **3%** | 37 pts |
| Strategic Minerals | 35% | **6%** | 29 pts |
| **Average (monetisable classes)** | **29.5%** | **6.9%** | **~23 pts** |

**A depositor now receives roughly 92 kg-units for 100 kg of Grade A maize,
instead of 70 units of uncertain worth.** That is a large, concrete
improvement in the producer's terms, and it comes from removing a risk the
system was never well placed to carry rather than from taking a gamble.

It also retires the awkward finding that precious metals was the most
under-haircut class in the register. Gold's price volatility was never the
warehouse's problem; only assay accuracy is.

---

## 13.3 Grade and moisture: the two corrections weight alone misses

A pure scale reading is not enough, and pretending otherwise would build in
the oldest fraud in agricultural trade.

### Water is not the commodity

Grain sold at 18% moisture instead of the 13.5% reference is roughly 5%
water by weight. Wood is far worse — green timber can be **60% moisture**,
meaning a "1,000 kg" delivery is barely 470 kg of the reference substance.

Every deposit is therefore normalised to **dry-matter equivalent at a
published reference moisture**. Moisture meters are cheap, fast, and give
the same reading in anyone's hands, which is exactly the property a
decentralised system needs.

### Grade still matters

Grade C maize is still maize, but a kilogram of it is not a kilogram of
Grade A. Rather than issue separate note series per grade — which would
fragment liquidity across sixty series and destroy fungibility — deposits
are converted to **standard-grade-equivalent weight**:

| Grade | Factor |
|---|---|
| A | 1.00 |
| B | 0.85 |
| C | 0.65 |
| Reject | 0 |

Worked example, 1,000 kg of maize deposited:

| Grade | Moisture | Units issued |
|---|---|---|
| A | 13.5% | **920 kg-units** |
| A | 18.0% | 872 |
| B | 13.5% | 782 |
| C | 16.0% | 581 |

**The honest caveat:** grading reintroduces a judgement call, and therefore
reintroduces a corruptible human decision. It is a much smaller judgement
than pricing — "is this Grade A or B?" against a photograph is far more
constrained than "what is maize worth this week?" — but it is not zero.
Everything in §6.4 about inspector rotation and published variance
statistics still applies, and grading is now the *only* remaining
discretionary input.

---

## 13.4 Wood: the class that breaks weight denomination

You identified this correctly, and it is the hardest case in the register.

### Why one "wood kg" is not fungible

Air-dry density varies by more than **6×** across species:

| Species | Density | 1,000 kg gives you |
|---|---|---|
| Balsa / light softwood | 160 kg/m³ | 6.25 m³ |
| Pine | 510 kg/m³ | 1.96 m³ |
| Teak | 655 kg/m³ | 1.53 m³ |
| Eucalyptus | 700 kg/m³ | 1.43 m³ |
| Ironwood | 1,050 kg/m³ | 0.95 m³ |

Sell by weight and a builder wanting volume gets **3.19× more balsa than
ironwood** per unit. Sell by volume and a firewood buyer wanting energy gets
**2× more matter from ironwood than pine**. Neither unit is right, because
buyers of wood want different things: a carpenter wants volume and species,
a firewood buyer wants calorific content, a builder wants structural
strength.

### The resolution: sub-series, not one wood note

Wood cannot be a single class. It splits by **use and species band**:

| Sub-series | Unit | Buyer wants |
|---|---|---|
| `WD-F` Fuelwood | kg dry matter, stated calorific band | Energy |
| `WD-S` Softwood timber | m³ air-dry at 15%, species band | Volume |
| `WD-H` Hardwood timber | m³ air-dry at 15%, species named | Volume + species |
| `WD-P` Poles & posts | count, by length and diameter class | Countable pieces |

This is more complex than "wood = 1 kg", and the complexity is *real* rather
than imposed: it exists in the physical world and in every timber market.
Pretending it away would produce notes that nobody accepts, because the
first carpenter to redeem a "wood note" for balsa when he expected teak
would stop taking them.

**General rule: a class is only monetisable if buyers within it want the
same thing.** Where they want different things, the class must split until
they don't.

### Classes where weight is the wrong basis

| Class | Correct basis | Why |
|---|---|---|
| Livestock | **count**, by weight band | An animal is not divisible |
| Water | **volume** delivered | Weight and volume are equivalent; delivery is the claim |
| Ceramics & glass | **count** of standard pieces | Breakage, not shrinkage |
| Biofuels | **energy**, kg × calorific value | Buyers want heat |
| Energy credits | **kWh** | No physical stock at all |
| Fresh produce | **none — not monetisable** | Confirms §2.2 |

---

## 13.5 Provenance: the certificate

You are right that the clock should start at the physical event, not at the
warehouse door.

### The gaming problem this closes

Under the old design, decay ran from *issuance*. A producer could store
grain privately for seven months, watch it deteriorate, deposit it, and
receive a note with a full fresh grace period. The accumulated spoilage risk
would pass silently to whoever accepted the note.

**Decay now runs from the origin date.** Grain harvested in January and
deposited in August arrives with seven of its six grace months already
spent — the model flags it as *stale on deposit*, and it begins decaying
immediately.

### What the certificate records

Every deposit carries a permanent record, and it travels with the note:

```
CERTIFICATE OF ORIGIN
  Commodity      Maize, Grade A
  Harvested      2027-01-15        <- decay clock starts here
  Deposited      2027-08-15        <- 7 months already elapsed
  Producer       P-04471, Kigoma district
  Moisture       13.2%
  Gross weight   1,000 kg
  Dry-matter eq  1,000 kg
  Units issued   920 kg-units
  Inspectors     I-088, I-142
  Prior storage  On-farm crib, 7 months
```

Scanning a note shows all of it. **A buyer can see not just what the note
claims but where it came from and how old the underlying matter is.** For
grain and produce this is the difference between an informed and an
uninformed acceptance.

### Secondary benefits

- **Traceability** for food safety and export certification
- **Legality gates** for timber and gold become enforceable, since origin is
  recorded rather than asserted
- **Producer reputation**: a farmer whose deposits consistently grade A
  builds a visible record, which is the beginning of creditworthiness
- **Dispute evidence**: grading disputes have a documented baseline

### The cost

Provenance means **no anonymity for producers**. §5.3 deliberately removed
transaction recording on repression grounds; this puts identity back at the
issuance gate. That is the correct trade — gate identity plus anonymous
circulation is exactly the cash model, and §8.7 already relies on it for
AML — but it should be stated plainly rather than presented as free.

---

## 13.6 The cost: no common unit of account

This is the serious objection to weight denomination, and it must not be
minimised.

### The numbers

Without a common unit, every pair of goods needs its own exchange rate:

| Goods in the market | Bilateral rates | With a reference good | Ratio |
|---|---|---|---|
| 4 | 6 | 3 | 2× |
| 10 | 45 | 9 | 5× |
| 20 | 190 | 19 | 10× |
| 50 | 1,225 | 49 | 25× |

**This is the textbook argument for money**, and abandoning a value unit
means walking back into it. A market woman who must know 190 exchange rates
instead of 20 prices is being asked to do real cognitive work, and she will
reasonably prefer shillings.

### Why it is survivable

**A numéraire will emerge whether or not the system appoints one.** Markets
converge on a reference good spontaneously — historically salt, cattle,
cowries, cigarettes in prison camps. Scoring the classes on the properties
a numéraire needs (non-decaying, cheap to store, liquid, finely divisible,
easy to verify):

| Rank | Class | Score |
|---|---|---|
| 1 | Precious Metals | 0.99 |
| 2 | Iron & Steel | 0.88 |
| 3 | Copper & Aluminium | 0.87 |
| 4 | Construction Materials | 0.69 |

Iron is the realistic winner in a rural East African market: **stable,
universally wanted, cheap to store, divisible, and instantly verifiable with
a scale and a magnet.** Precious metals scores higher on paper but is too
valuable per gram for daily use — nobody prices a cabbage in gold.

**The recommendation is to let iron become the informal reference and not
to fight it.** The system should not *mandate* a numéraire, because
mandating one recreates the price-setting authority that weight denomination
just abolished. But it should ensure the likely winner is exceptionally well
run: tight grading, deep liquidity, reliable redemption.

### The app carries the cognitive load

The exchange-rate burden is a human-memory problem, and it is exactly the
kind of problem software is good at. The wallet shows, for any pair:

```
  100 kg maize   ->   ~9-11 kg iron
  Based on 14 trades in the last 30 days.  Confidence: HIGH
  Range observed: 8.5 - 11.2      Median: 10.0
```

**This is observation, not assessment**, and the distinction is the whole
point. The system reports *what other people actually traded*. It never says
what something is worth. A published assessment is an authority that can be
captured; a published observation is a fact that can be checked. Buyer and
seller still decide, informed rather than instructed.

This is also strictly better than the dual-price receipt of §12.2 for
commodities, because a trade record cannot be manipulated by a committee —
only by faking trades, which requires actually moving goods.

---

## 13.7 What this changes elsewhere

| Section | Change |
|---|---|
| §1.1 unit of account | **Superseded.** No basket unit; notes denominated in physical quantity |
| §1.4 haircut | Haircuts fall from ~30% to ~7%; they now cover physics only |
| §3.1 issuance | Price committee **deleted**; step 3 becomes weigh-and-grade |
| §3.3 redemption | Redemption is exact: 100 kg-units returns 100 kg |
| §12.2 receipts | Reference bundle replaced by observed trade ranges for commodities |
| Annex B P4 | **Largely dissolved** for issuance; survives only for unique goods |
| Annex B P1 | Unaffected — bundle pricing still required |
| §9 risks | New risk: no numéraire → high cognitive load → shillings preferred |

### The new risk this introduces

**Usability.** A currency that requires a smartphone to compare prices is a
currency that excludes people without smartphones. §5.6's USSD path must
support rate lookup, and the printed trade-rate board at the market becomes
essential infrastructure rather than a nicety.

There is a real possibility that weight denomination is monetarily elegant
and practically unusable in a market where most people cannot quickly answer
"how much maize for a hoe?" **This should be tested directly in Phase 1**,
by measuring how long a typical transaction takes to negotiate compared with
shillings, and whether traders spontaneously adopt a reference good.

If they do not — if the market stubbornly wants a single number — the
fallback is to let iron units serve openly as the accounting unit while
keeping every note a physical claim. That preserves the anti-capture
property (no committee sets iron's value; it is just 1 kg of iron) while
restoring a common denominator.
