# 3. Issuance, inspection and redemption

## 3.1 The issuance pipeline

```
  PRODUCER                COOPERATIVE                  LEDGER
     │                         │                          │
     │  1. deliver goods       │                          │
     ├────────────────────────>│                          │
     │                         │ 2. weigh + grade         │
     │                         │    (2 inspectors)        │
     │                         │                          │
     │                         │ 3. price at committee    │
     │                         │    reference rate        │
     │                         │                          │
     │                         │ 4. apply grade factor    │
     │                         │    then class haircut    │
     │                         │                          │
     │                         │ 5. check issuance        │
     │                         │    ceiling ─────────────>│
     │                         │<───────── approve/reject │
     │                         │                          │
     │                         │ 6. sign + print notes    │
     │  7. receive notes       │    (2-of-3 key quorum)   │
     │<────────────────────────┤                          │
     │     less 1.0% levy      │ 8. record issuance ─────>│
     │                         │                          │
```

### Step detail

**1. Delivery.** Producer brings goods to a licensed warehouse. Rejected at
the door if visibly below Grade C, wet, contaminated or of unverifiable
origin (critical for timber and gold).

**2. Grading.** Two inspectors grade independently and blind. If grades
differ by more than one step, a third inspector is called and the **lowest**
of the three stands. Conservative by design: the cost of over-grading is
systemic insolvency, the cost of under-grading is one unhappy depositor.

**3. Pricing.** Valued at the **weekly committee reference price**, not a
spot price. Committee prices are set every Monday from three sources: local
market survey, nearest commodity exchange quote, and the previous week's
actual redemption transactions. Published before deposits open.

Using a weekly fixed price rather than live pricing prevents intra-week
arbitrage against the cooperative and gives depositors a predictable number.

**4. Discounting.** `notes = market value × grade factor × (1 − haircut)`

**5. Ceiling check.** The ledger enforces that a cooperative's total
outstanding issuance never exceeds its last verified collateral, valued at
current committee prices, net of haircuts. **This check happens on the
ledger, not in the signing device.** It is the control that makes key
compromise insufficient to inflate the currency.

**6. Signing.** Two of three key-holders must co-sign. Notes are printed
from pre-numbered, security-featured blank stock held under dual control.

**7. Levy.** 1.0% deducted from issued value to the community fund.

**8. Record.** The issuance event is written to the cooperative partition
and swept into the next hourly checkpoint.

---

## 3.2 Re-inspection

Collateral is re-verified on a schedule set by how fast the class moves:

| Class group | Interval | Method |
|---|---|---|
| Fresh produce, dairy | Weekly | Full physical count |
| Grains, biofuels | Monthly | Sample + weight reconciliation |
| Livestock | Quarterly | Herd count, tag audit, mortality reconciliation |
| Timber, textiles, rubber | Quarterly | Sample |
| Metals, stone, minerals | Semi-annual | Full count + assay sample |

### When stock is short

Discrepancies are inevitable — rodents, moisture, breakage, theft. What
matters is that the response is **automatic and pre-agreed**, not
negotiated after the fact:

| Shortfall vs. book | Response |
|---|---|
| ≤ 2% | Within tolerance; charged to warehouse operating account |
| 2–5% | Charged to warehouse; operator's performance bond debited |
| 5–15% | Class stabilisation fund covers; issuance suspended pending investigation |
| > 15% | **Series frozen.** Independent audit. Assume fraud until disproven |

Critically: **holders are not devalued for shortfalls within the haircut.**
That is what the haircut is for. The original design's "everyone holding
those notes sees the updated value drop" is the wrong instinct — it makes
every holder bear a loss caused by the warehouse's failure, which destroys
confidence in every note of that class simultaneously.

Loss waterfall, in order:

1. Warehouse operating account
2. Warehouse performance bond
3. Class stabilisation fund (funded from demurrage and custody fees)
4. Federation insurance pool
5. **Only then**, pro-rata haircut on holders — a "series impairment event",
   publicly declared, with reasons published

Reaching stage 5 should be understood as a system failure requiring
independent investigation, not as routine operation.

---

## 3.3 Redemption

### The right that makes the currency real

Any holder may present notes at the issuing cooperative and receive physical
commodity at the current committee reference price. **This right is what
distinguishes this system from scrip.** If it is ever suspended without a
published rule, the currency becomes a promise, and promises are what the
system was built to escape.

### The redemption gate

Redemption cannot be unlimited, because collateral cannot be sold instantly.
From the model (Annex A.5), the share of outstanding notes redeemable within
30 days varies enormously:

| Class | Max 30-day run honourable |
|---|---|
| Precious Metals | 70% |
| Grains, Iron, Copper, Livestock | 45% |
| Construction Materials, Fresh Produce | 30% |
| Wood, Dairy, Rubber | 25% |
| Water, Plastics, Medicinal, Ceramics | 17% |
| Strategic Minerals | 15% |
| Stone & Marble | 13% |

When presentations in a rolling 30-day window exceed the class threshold:

1. Redemption continues **pro rata** — every claimant receives a proportional
   share immediately, nobody is turned away empty-handed.
2. The remainder is **queued with a dated claim**, honoured in order as
   stock is sold or new deposits arrive.
3. Queued claims **accrue a 1%/month premium**, paid from the stabilisation
   fund. Waiting is compensated.
4. The gate and the queue length are **published daily**.

### Why pro-rata beats first-come-first-served

A first-come queue creates a bank run: the rational response to any doubt is
to run to the warehouse immediately. Pro-rata with a compensated queue
removes the advantage of panicking. Everyone gets some now; waiting pays a
premium. **The gate is not a failure mode — it is a normal operating
instrument, and it must be printed on the note.** A holder who discovers the
gate for the first time during a crisis will conclude they were defrauded.

---

## 3.4 Retirement

Notes leave circulation when:

| Trigger | Mechanism |
|---|---|
| Redemption | Serials marked spent; commodity released |
| Expiry | Value reaches zero at maximum validity |
| Damage | Exchanged for a fresh note, same issue date preserved |
| Series impairment | Withdrawn and reissued at impaired value |

### The expired-note residual

A note that reaches maximum validity is worth zero as currency. That is
harsh, and without a remedy it will feel like theft — especially to someone
who was ill, travelling, or simply unaware.

**Residual claim:** for twelve months after expiry, the holder may present
an expired note and receive **20% of its last non-zero value** from the
class stabilisation fund. Funded by the demurrage that accumulated on that
very note.

This is not generosity. It is the mechanism that prevents "my money expired"
becoming the story that kills adoption in the second year.
