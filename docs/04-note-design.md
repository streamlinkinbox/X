# 4. Physical note design

## 4.1 Design principles

1. **Readable by someone who cannot read.** Colour, icon, shape and size
   must convey class and value without text.
2. **Never state a value that will become false.** The face value of a Tier A
   note is a *starting* value. The note must not appear to promise it
   forever.
3. **Disclose the unpleasant facts on the note itself.** Decay, the
   redemption gate, and the counterfeit limitation. A user who discovers a
   term during a crisis concludes they were cheated.
4. **Survive the environment.** Rain, sweat, folding, market dust, three
   years in a tin.

---

## 4.2 Front

```
┌──────────────────────────────────────────────────────────┐
│  ╔════╗                                     ╔══════════╗ │
│  ║ 🌾 ║  GRAINS & CEREALS            [GR]   ║  1 0 0   ║ │
│  ╚════╝  Nafaka                             ╚══════════╝ │
│                                                          │
│   ●●●●●  ← five dots = 100 unit denomination             │
│                                                          │
│   VALUE FALLS 2% EACH MONTH AFTER 6 MONTHS               │
│   Thamani hupungua 2% kila mwezi baada ya miezi 6        │
│                                                          │
│   ┌────────────────────────────────────────────┐         │
│   │ ISSUED   2027-03-14      EXPIRES 2029-03-14│         │
│   │ ████████████░░░░░░░░  value bar            │         │
│   └────────────────────────────────────────────┘         │
│                                                          │
│   KIGOMA FARMERS COOPERATIVE #047                        │
│   Warehouse 12, Kigoma District                          │
│                                                          │
│   [watermark]        [holographic strip]    [UV mark]    │
│   GR-7K2M-9XQP-4B8T                                      │
└──────────────────────────────────────────────────────────┘
```

### Key elements

| Element | Purpose |
|---|---|
| Class icon, embossed | Tactile identification for the blind and the illiterate |
| Colour field | Instant class recognition across a market stall |
| Dot denomination | Countable without reading numerals |
| Decay statement | Bilingual, in the largest type on the note after the value |
| Value bar | Printed graphic showing the decay schedule shape |
| Issue and expiry dates | Both, always, in ISO format |
| Serial | Human-readable, Crockford base32 (no confusable characters) |

### Denominations and physical differentiation

| Value | Dots | Length | Corner |
|---|---|---|---|
| 10 | ● | 120 mm | square |
| 50 | ●●● | 130 mm | square |
| 100 | ●●●●● | 140 mm | one clipped |
| 500 | ●●●●●●● | 150 mm | one clipped |
| 1000 | ●●●●●●●●● | 160 mm | two clipped |

Length and corner shape let a user distinguish denominations by touch inside
a pocket — a real requirement in a market, and a dignity requirement for
blind users.

**Tier A and Tier B notes differ in shape**, not merely colour: Tier B notes
are 15 mm taller. A user must never confuse a decaying note with a stable
one, and 8% of men have colour vision deficiency.

---

## 4.3 Back

```
┌──────────────────────────────────────────────────────────┐
│  ┌───────────────┐   THIS NOTE REPRESENTS                │
│  │               │   50 kg Grade A maize                 │
│  │   QR  CODE    │   Warehouse 12, Kigoma                │
│  │               │                                       │
│  │               │   CHECK BEFORE YOU ACCEPT             │
│  └───────────────┘   Scan this code, or dial *384*77#    │
│                      Angalia kabla ya kupokea            │
│                                                          │
│  VALUE SCHEDULE                                          │
│  ┌────────────────────────────────────────┐              │
│  │100%▔▔▔▔▔▔▔╲                            │              │
│  │            ╲╲╲╲╲                       │              │
│  │  0%             ╲╲╲╲╲╲╲╲               │              │
│  │    0    6    12    18    24 months     │              │
│  └────────────────────────────────────────┘              │
│                                                          │
│  ⚠ Redemption may be limited when many people withdraw   │
│    at once. You will receive a dated claim and 1%/month. │
│                                                          │
│  ⚠ Scanning proves this note was issued. It does not     │
│    prove the paper is not a copy. Check the hologram.    │
└──────────────────────────────────────────────────────────┘
```

### The two warnings

These are the most important text on the note, and both were absent from the
original design.

**The redemption gate warning** exists because a holder who first learns of
the gate while standing in a queue during a panic will conclude the system
lied to them. Disclosed in advance, the gate is a known term. Discovered in
a crisis, it is fraud.

**The counterfeit warning** exists because "scan to verify" implies
certainty the scan cannot deliver. A scan verifies the *signature*; it
cannot verify the *paper*. A copied note scans perfectly. Users must be
taught to check the physical features, and the note is the only place that
teaching reliably reaches them.

Printing "impossible to counterfeit", as the original blueprint proposed,
would be the single most damaging sentence on the note: it trains users to
skip the check that actually protects them.

---

## 4.4 Security features

Layered by cost, because Phase 1 cannot afford full banknote-grade printing:

### Tier 1 — Phase 1, low cost

| Feature | Defeats | Cost |
|---|---|---|
| Watermarked security paper | Photocopying | Low |
| UV-reactive fibres | Casual forgery | Low |
| Intaglio-feel varnish on icon | Flat reproduction | Low |
| Microtext in the border | Scanner resolution limits | Low |
| Serial with check digit | Invented serials | Nil |
| Ed25519 signature in QR | Ledger forgery | Nil |

### Tier 2 — Phase 2, higher volume

Holographic foil stripe, colour-shifting ink on the denomination, embedded
security thread, and per-note random fibre pattern photographed at issuance
— the last being effectively a physical fingerprint that a copy cannot
reproduce.

### Tier 3 — Phase 3

NFC secure element embedded in polymer substrate.

**The NFC decision.** The original design put an NFC chip in every note from
the start. At roughly USD 0.08–0.20 per tag, a 10-unit note would cost more
in chip than it is worth. Chips also fail when the note is folded, which
banknotes are.

**Put the secure element in a reusable card, not in the note.** The card
holds balances and does offline transfers; the paper stays cheap, dumb and
durable. This is a significant change from the original architecture and it
is the correct one.

---

## 4.5 The transaction receipt

Separate from the note itself, every quote and settlement produces a
**dual-price receipt** (§12.2) showing the asked bundle, the assessed
reference bundle, and the markup per class. It is printable on a thermal
printer, renderable in abbreviated form over USSD, and is the buyer's
protection against being overcharged.

Two display rules follow from §12 and matter more than they appear to:

- **The wallet shows holdings by class, never as a single total.** A single
  total silently reintroduces the fungibility that bundle pricing exists to
  remove, and would quietly undo the fix for demurrage arbitrage.
- **Settlement screens show face required against current value tendered**,
  so the cost of paying with aged notes is visible at the moment it is
  incurred rather than discovered later.

## 4.6 The counterfeit economics

Counterfeiting is deterred by making it unprofitable, not impossible.

| Factor | Effect |
|---|---|
| Small denominations | A 10-unit note is not worth forging |
| Tier A decay | A forged note's value evaporates; forgery has a shelf life |
| Local circulation | Strangers with large notes are conspicuous |
| Online detection | Clones surface at the next sync |
| Insurance pool | The honest loser is compensated, so trust survives |

**Tier A demurrage is an unexpectedly strong anti-counterfeit measure.** A
counterfeiter must print, distribute and spend before the notes decay and
before the clone is detected. Forging a decaying currency is like stealing
ice.

The system's genuine vulnerability is **Tier B**: stable, non-expiring,
high-value notes are worth forging and worth holding. Tier B therefore
requires Tier 2 security features from day one, and Tier B notes above 500
units should require an online check for acceptance.
