# 5. Technical architecture

## 5.1 Design constraints

The architecture is dictated by the operating environment, not by
technology preference:

| Constraint | Implication |
|---|---|
| Intermittent connectivity (hours to weeks offline) | Offline transactions must be first-class, not degraded mode |
| Feature phones common, smartphones uneven | USSD/SMS path must be functionally complete, not a stub |
| Power scarcity | Verification must work on a device charged once every few days |
| Low literacy in some cohorts | Verification result must be readable as colour + sound + icon, not text |
| Adversaries include locally powerful people | No single administrator may be able to alter balances |
| Devices are shared and lost | Key recovery must exist and must not become a theft vector |

**These constraints eliminate a public blockchain immediately.** Not on
ideological grounds — on the grounds that a system requiring per-transaction
network consensus cannot settle a market-day purchase in a village with no
signal.

---

## 5.2 The ledger

### Structure

A **federated append-only log**, one partition per cooperative, with
cross-signed checkpoints.

```
Cooperative A log ──┐
Cooperative B log ──┼──> hourly checkpoint ──> cross-signed by
Cooperative C log ──┘     (Merkle root)        ≥5 of 9 federation nodes
                                                      │
                                                      ▼
                                          published to SMS broadcast,
                                          radio datacast, and any
                                          available internet mirror
```

Each cooperative writes only to its own partition. It cannot alter another's.
A checkpoint is a Merkle root over all partitions, signed by a threshold of
federation nodes. Once checkpointed, history is immutable in practice: to
rewrite it you must compromise five of nine independently-held keys *and*
every published copy of the root, including ones printed on paper in
warehouse offices.

### Why not a blockchain

| Requirement | Blockchain | Federated log |
|---|---|---|
| Offline transaction settlement | No | Yes |
| Works over SMS | No | Yes |
| Verification on a feature phone | No | Yes |
| Energy cost | High | Negligible |
| Resists a hostile local official | Yes | Yes (threshold signing) |
| Resists the entire federation colluding | Yes | **No** |

The last row is the real trade-off, and it should be stated rather than
buried. **A federated log is not trustless.** It is *accountable*: collusion
is possible but requires many parties, leaves evidence, and is detectable by
anyone holding an old checkpoint. For a system whose collateral is physical
and locally inspectable anyway, that is the right trade — you already have to
trust that the maize is in the shed.

### What is recorded

| Event | Recorded fields | Privacy |
|---|---|---|
| Issuance | serial, class, face, deposit ref, inspector IDs, warehouse, timestamp | Public |
| Re-inspection | warehouse, class, assessed stock, variance, inspector IDs | Public |
| Redemption | serial(s), quantity released, holder ref | Holder pseudonymous |
| Retirement | serials, reason | Public |
| Transfer | **see below** | **Not recorded by default** |

---

## 5.3 The transaction-privacy decision

The original blueprint recorded every transfer and treated the resulting
audit trail as a feature: "no tax evasion is possible."

**This must be reconsidered, and reversed.**

A complete, queryable record of every payment made by every person in a
district, held by a local institution, in a region with a history of
political violence and ethnic targeting, is **a permanent instrument of
repression**. It records who bought medicine, who paid a lawyer, who
supported whom. Whoever controls the district controls that database. The
system's own threat model — "local strongmen seize warehouses" — applies with
far greater force to the transaction log than to the grain.

**Design decision: peer-to-peer transfers are not recorded on the ledger.**

The ledger records the *lifecycle* of notes — birth, inspection, death — not
their *journey*. This is exactly how cash works, and cash's privacy
properties are a feature that took centuries to win.

| What we get | What we give up |
|---|---|
| Payment privacy equivalent to cash | Per-transaction taxation |
| No repression database | Complete audit trail |
| Genuine offline capability | Real-time velocity statistics |
| Much lower ledger volume | Ability to trace stolen notes past first hop |

Taxation moves to the gates (Section 7). Velocity is measured by sampling
and surveys, not by surveillance.

**Users who want a transaction record may opt in**, per-transaction, for
receipts, disputes and business accounting. Opt-in, never default.

---

## 5.4 Note identity and verification

### Cryptographic construction

Each note carries:

```
serial     : 16 chars, Crockford base32, class-prefixed  e.g. GR-7K2M-9XQP-4B8T
class      : 2-char class code
face       : integer cents
issued     : ISO date
issuer     : cooperative ID
warehouse  : warehouse ID
deposit    : deposit batch reference
sig        : Ed25519 signature over all the above, by the issuing
             cooperative's note-signing key
```

The QR code encodes exactly these fields plus the signature — roughly 180
bytes, comfortably within a version-8 QR at high error correction, which
survives a creased and dirty banknote.

**Verification is entirely offline:** the phone holds the federation's
public keys (≈2 KB, updated by SMS when rotated), checks the signature, and
computes decayed value from the issue date and the class rules. No network
is needed to know the note is genuine and what it is worth today.

### What verification proves — and what it does not

| Verification says | Confidence |
|---|---|
| This note was validly issued by a real cooperative | **Certain**, offline |
| Its face value and issue date are unaltered | **Certain**, offline |
| Its value today is X | **Certain**, offline |
| The collateral existed at last inspection | Certain if online; last-known if offline |
| **This physical paper is not a photocopy** | **Not proven, ever** |
| **This note has not already been spent elsewhere** | Only if online |

Those last two rows are the honest limits, and they must be communicated to
users in exactly those terms.

### The counterfeit problem, stated properly

A QR code can be photographed and reprinted. The signature will verify —
it is a valid signature on a valid note. Cloning is defeated not by
cryptography but by:

1. **Physical security features** on the paper (Section 4) — the actual
   first line of defence, as with any banknote.
2. **Online clone detection.** When two copies of one serial are presented
   and both eventually sync, the ledger sees it. The first presenter is
   presumed honest; the loss falls on the second.
3. **The clone-loss insurance pool**, funded from gate fees, which
   compensates the honest loser. Without it, the system's user-visible
   promise becomes "you might lose everything to a counterfeiter", and
   adoption stops.

**Never print "impossible to counterfeit" on the note.** Print the
verification instructions and the holding limits.

---

## 5.5 Offline transactions and the double-spend bound

### The hard constraint

Double-spending offline cannot be prevented by software or cryptography
alone. This is not an engineering gap to be closed with cleverness; it is
established in the CBDC literature and follows from first principles — an
offline device cannot know what another offline device has seen. Prevention
requires tamper-resistant secure hardware, and even that only *raises the
cost* of attack rather than eliminating it.

Therefore the design goal is not prevention. It is **bounding the loss**.

### Three-track offline model

| Track | Device | Offline limit | Consecutive offline hops | Who bears clone loss |
|---|---|---|---|---|
| **Paper only** | None | Unlimited | Unlimited | Recipient (as with cash) |
| **Phone app** | Smartphone | 200 RCU | 5 transfers | Insurance pool up to 200 RCU |
| **Secure card** | NFC card, secure element | 2,000 RCU | 20 transfers | Insurance pool up to 2,000 RCU |

The limits are the security mechanism. A compromised phone can mint at most
200 RCU of fraud before it must sync; a compromised secure element, 2,000.
Both are small enough to insure and large enough to be useful.

### Sync and reconciliation

On reconnection the device uploads its signed offline transaction chain.
The ledger checks each chain against known-spent serials.

When a double-spend is detected:

1. Both chains are published to the affected cooperative.
2. The **earlier valid presentation stands**; the later is void.
3. The honest loser claims from the insurance pool.
4. The originating device's key is revoked and its holder flagged.
5. If a device is implicated **twice**, its holder loses offline privileges
   for twelve months and the case goes to the dispute council.

### The mesh problem

Chains of offline transfers — A pays B, B pays C, C pays D, none online —
mean fraud detected at sync may be four hops from the fraudster, and the
loss lands on a stranger. This is why the hop limit exists: after five
offline hops the note must be brought online before further transfer.

Enforcement is only as strong as the app, and the app runs on the user's
phone. A patched app can ignore the limit. **This is an accepted residual
risk, capped by the holding limits and priced into the insurance pool.**

---

## 5.6 The feature-phone path

Roughly half of target users will not have a smartphone. The USSD path is
not a courtesy feature; it is the majority interface in Phase 1.

```
*384*77#
 1. Verify a note      -> enter serial -> SMS: class, face, value today,
                          collateral status at last inspection
 2. My balance
 3. Send               -> recipient code, amount, PIN
 4. Deposit receipt status
 5. Report a bad note
```

Verification over SMS returns the *ledger's* answer, so it requires network
but not data. It cannot check the paper's physical authenticity, and the
reply message says so in plain language.

**The known weakness:** SMS is unauthenticated, spoofable, and readable by
the mobile network operator. A user relying solely on SMS verification can be
phished by a forged reply. Mitigations: a per-user rotating four-digit
verification salt printed on the enrolment card and echoed in every genuine
reply; and shortcodes registered under the cooperative's own name.

---

## 5.7 Key management

| Key | Held by | Rotation | Compromise impact |
|---|---|---|---|
| Note-signing | Cooperative, 2-of-3 hardware tokens | Annual | Forged notes until revoked; bounded by issuance cap |
| Checkpoint | Federation, 5-of-9 threshold | Biennial | History rewrite; requires 5 independent parties |
| Device | User device secure storage | On loss | Bounded by offline holding limit |
| Inspector | Individual smartcard | Annual | False inspection reports; caught by rotation |

**Cooperative key compromise is the catastrophic case.** An attacker with a
note-signing key mints unlimited valid notes. Controls:

- **Issuance ceiling enforced at the ledger, not in the signing device.**
  A cooperative that signs beyond its verified collateral has its issuance
  rejected at checkpoint, no matter how valid the signature.
- **Daily issuance rate limits** with anomaly alerting.
- **Physical separation:** signing tokens held by three people who do not
  live in the same place.
- **Rapid revocation** by SMS broadcast, with paper fallback: revoked key
  IDs posted at every warehouse and market.

The ledger-side issuance ceiling is the important one. It means **key
compromise alone is not sufficient to inflate the currency** — you would
also need to corrupt the inspection record that sets the ceiling. Two
independent failures required, by design.

---

## 5.8 What to build first

Phase 1 needs far less than the full architecture:

**Build:**
- Note signing and verification library (Ed25519 + the class rules)
- Cooperative ledger node — a single-writer append-only log; SQLite is
  entirely adequate at pilot scale
- Android verification app, offline-first
- USSD gateway
- Inspector tablet app for deposits and re-inspections

**Do not build in Phase 1:**
- Blockchain of any kind
- NFC secure-element cards (Phase 2 — the paper works)
- Cross-cooperative federation (only one cooperative exists)
- Automated market pricing (use a weekly committee price)

**Estimated Phase 1 build: 4–6 person-months.** The hard part of this
project has never been the software.
