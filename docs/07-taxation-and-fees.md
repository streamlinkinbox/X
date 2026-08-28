# 7. Taxation and fees

## 7.1 Why point-of-sale taxation fails

The original design collects a 0.5–1% tax automatically at every
transaction, and treats this as making evasion impossible.

It cannot work as specified, for three independent reasons. Any one of them
is fatal.

### Reason 1: it contradicts offline capability

Automatic deduction requires that the transaction be observed by something
that can deduct. Offline, nothing observes it. The design cannot
simultaneously promise "works with no internet" and "no transaction escapes
the tax." **These are the same requirement pointing in opposite
directions.**

### Reason 2: it cannot be enforced against paper

Two people exchange a banknote for a chicken. No phone involved. No tax
event exists to intercept. The system's own strongest feature — that the
paper works without technology — guarantees a permanently untaxed channel.

To close it you would have to ban unassisted paper transfer, which destroys
the resilience that justified paper in the first place.

### Reason 3: taxing circulation contradicts the design's core purpose

The system exists to make money circulate. A per-transaction levy is a tax
*on circulation*. Every hand a note passes through shaves value off. A note
changing hands twenty times in a year at 0.5% loses 9.5% — on top of
demurrage. **The system would be penalising precisely the behaviour it was
built to encourage.**

This is the deepest of the three objections, and it survives even if the
technology were perfect.

---

## 7.2 Gate-based taxation

Collect at the two moments that are **always online, always at a fixed
place, always supervised**: issuance and redemption.

```
                 ISSUANCE GATE                      REDEMPTION GATE
                      │                                    │
  commodity ──> inspection ──> notes issued          notes ──> commodity out
                      │         (levy here)                 │   (levy here)
                      ▼                                     ▼
              1.0% of issued value                  0.5% of redeemed value
                      │                                     │
                      └──────────> community fund <─────────┘
                                          │
                    ┌─────────────────────┼─────────────────────┐
                    ▼                     ▼                     ▼
             public services       insurance pool        federation ops
                  60%                   25%                   15%
```

Everything between the gates — all circulation — is **untaxed and
unobserved**.

### Why this is strictly better

| Property | Per-transaction | Gate-based |
|---|---|---|
| Works offline | No | Yes (gates are always online) |
| Evadable by paper transfer | Completely | No — you must use a gate eventually |
| Penalises circulation | Yes | **No** |
| Requires surveillance | Yes | No |
| Collection points to audit | Every phone | ~10 warehouses |
| Visible to the payer | Small and constant | Larger and occasional |

The evasion argument inverts entirely. A note can circulate untaxed
forever — but it entered through a gate and it can only become goods
through a gate. **The commodity is the chokepoint, and the commodity cannot
be smuggled past an inspection it needs in order to exist.**

Auditing ten warehouses is a task a community can actually perform.
Auditing fifty thousand phone transactions is not.

### Rates

| Gate | Rate | Base | Rationale |
|---|---|---|---|
| Issuance | 1.0% | Issued face value | Paid by the depositor, who has just gained liquidity |
| Redemption | 0.5% | Value of goods released | Paid by the redeemer |
| Combined round trip | ~1.5% | | Compare: 18% VAT, or the 20–40% harvest-price gap producers currently absorb |

At an assumed 3× annual turnover of the note stock, gate revenue is roughly
**0.5% of transaction volume** — comparable to the original proposal's
yield, collected at 0.02% of the enforcement cost.

---

## 7.3 The complete fee schedule

Nothing hidden. Every deduction a user can experience:

| Fee | Rate | When | To whom |
|---|---|---|---|
| Issuance levy | 1.0% | On deposit | Community fund |
| Redemption levy | 0.5% | On withdrawal | Community fund |
| Tier B custody | 1–5%/yr (class-specific) | Monthly | Warehouse (70%) / stabilisation (30%) |
| Tier A demurrage | 11–46%/yr after grace | Monthly | Warehouse (50%) / stabilisation (30%) / community (20%) |
| Inspection | Flat, cost-recovery | Per deposit | Inspector pool |
| Note replacement | Flat, small | On damage | Cooperative |
| Dispute filing | Flat, refunded if upheld | On filing | Dispute council |

**Total annual cost of holding 1,000 RCU for a year:**

| Held as | Cost | Effective |
|---|---|---|
| Grain notes, spent within 6 months | 0 | Free |
| Grain notes, held 12 months | 106 RCU | 10.6% |
| Grain notes, held to expiry (24 mo) | 305 RCU | 30.5% over two years |
| Iron notes, held 12 months | 20 RCU | 2.0% |
| Gold notes, held 12 months | 10 RCU | 1.0% |
| Shillings under 8% inflation | 80 RCU-equivalent | 8.0% |

**The comparison in the last row is the honest sales pitch.** Tier B beats
holding a depreciating national currency. Tier A is *worse* than holding
shillings if you sit on it — which is the entire design intent. The system
does not claim to be cheap; it claims to be honest about its costs, and to
charge them for identifiable services rather than through the hidden tax of
inflation.

---

## 7.4 Fund transparency

The credibility of the levy rests entirely on visible spending. This is not
decoration; it is the mechanism by which people consent to being charged.

**Requirements:**

- Every disbursement published: amount, recipient, purpose, date.
- Published *physically* — a painted board at the warehouse and the market —
  not only digitally. Most people will never open the app for this.
- Quarterly assembly with a read-aloud account, in the local language.
- Any member may demand an audit with 20 co-signatures.
- Spending priorities set by annual community vote, not by the cooperative
  board.

The original blueprint's example — *"your tax funded the Kigoma primary
school roof"* — is exactly right in spirit and should be implemented
literally: **project-tagged receipts.** A person who paid an issuance levy
in March can be told in June which specific thing it built.

---

## 7.5 The state's cut

At scale the government will want revenue from this. Planning for that in
advance is far better than being surprised by it.

**Recommended posture: offer collection before it is demanded.**

The cooperative federation can act as a withholding agent, remitting a
negotiated share of gate revenue to the district authority. This offers the
state something it values — reliable revenue from a currently informal
economy, collected at almost no administrative cost — in exchange for the
thing the system needs, which is tolerance.

This is the same bargain Wörgl accidentally struck and then lost. Wörgl's
scrip was *so* good at collecting tax arrears that citizens paid taxes early,
and the municipality's finances recovered visibly. That success is precisely
what drew the Austrian National Bank's attention and got the experiment
banned in September 1933. **Fiscal usefulness is protection only if it is
offered to the right level of government, deliberately, in writing, and
early.** Offered accidentally to a threatened central bank, it is a death
warrant.
