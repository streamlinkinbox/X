# 11. Prior art

The original blueprint claims seven features have "never been combined
before." The combination may well be novel. **Every individual component is
not**, and each has a history containing hard-won lessons.

Knowing this literature is a practical advantage, not an academic courtesy:
it tells you which failures are already known, and it protects you from a
critic who knows it better than you do.

---

## 11.1 Commodity-reserve currency — Benjamin Graham (1937–1944)

Graham proposed issuing currency against warehouse receipts for a basket of
storable commodities, with two-way convertibility, in *Storage and Stability*
(1937) and *World Commodities and World Currency* (1944).

**The overlap with RCU is close to total** — commodity backing, warehouse
receipts, money supply tied to production, basket-based unit.

**What Graham got that the original blueprint should adopt:**
- Two-way convertibility is the mechanism that keeps a commodity currency
  honest. Redemption must be real and used.
- A *basket* rather than a single commodity, for exactly the diversification
  reasons Section 1.5 rediscovers.

**Milton Friedman's 1951 critique is the document to read.** He argued the
scheme would be too complex and costly to administer, too exposed to
political interference, and would not deliver the price stability claimed.
Richard Cooper later noted that proponents themselves put annual storage
costs at **3–4% of the outstanding value**, and that Hart's estimates
reached **6–7% per year for wheat and maize**.

**Why this matters directly:** the model's storage cost of 7%/year for
grains is not pessimism. It is consistent with the published literature, and
it is the number that forces the custody-fee conclusion in Section 1.2.
Anyone who claims commodity backing is free has not costed the warehouse.

**What Graham teaches about politics:** Keynes remarked in 1944 that
Graham's plan had no chance against the political influence of gold
interests at Bretton Woods. The technical merits were never the deciding
factor. They rarely are.

---

## 11.2 Demurrage — Gesell and Wörgl (1916–1933)

Silvio Gesell's *Freigeld* proposed money that loses value over time to
force circulation. Gesell himself suggested a modest 5–6% annual shrinkage.

**Wörgl, Austria, July 1932 – September 1933** is the canonical trial. The
municipality issued *Certified Compensation Bills* requiring a monthly stamp
worth 1% of face value.

| What happened | Figure |
|---|---|
| Scrip actually in circulation | ~7,400–12,000 schillings |
| Circulation speed vs. national schilling | ~8–14× faster |
| Unemployment in Wörgl | fell ~16% while rising ~19% nationally |
| Public works funded | ~100,000 schillings |
| Duration | 13.5 months |
| Ended by | Austrian National Bank, 1 September 1933 |

**Four lessons that bear directly on RCU:**

**1. The rate matters enormously.** Wörgl's 1%/month worked. Irving Fisher
advocated 2% *per week*, and where that was tried the money was simply not
accepted. RCU's Tier A rates of 1–5%/month sit at and above the upper end of
what has ever been shown to work. **Fresh Produce at 5%/month is in the zone
where historical experience says acceptance collapses.**

**2. Tax acceptance was the demand anchor.** Wörgl's scrip worked largely
because the municipality accepted it for taxes — citizens paid taxes *early*
to offload it. This is the strongest possible argument for the Section 9.2
bootstrap: **the issuer must accept its own currency for obligations people
already owe.**

**3. Success caused suppression.** Wörgl was not shut down for failing. It
was shut down after six neighbouring villages copied it, the French premier
visited, and the central bank recognised a threat to its monopoly. The
finance minister was reportedly motivated partly by a League of Nations loan
negotiation. **External financial relationships were the transmission
mechanism** — a detail with obvious relevance for any country under an IMF
programme.

**4. It was small and it was still stopped.** Twelve thousand schillings.
Any strategy premised on staying below the threshold of notice must be
honest about how low that threshold has historically been.

---

## 11.3 Warehouse receipt systems — East Africa (1990s–present)

Operating WRS exist in Tanzania, Uganda, Kenya, Zambia, Ghana and Malawi.
Tanzania's Warehouse Receipts Act No. 10 of 2005 established the WRRB, which
now covers 18 commodities across 23 regions.

**What works:** licensing and bonding of warehouse operators; grading
standards; electronic receipts (Uganda's eWRS was well received, especially
by banks); reduced post-harvest loss; better farmer prices through
aggregation.

**What fails, repeatedly:**

- **Collateral management fraud** is the best-documented failure mode.
  Uganda's regulator considered regulating collateral managers specifically
  because of "the high level of fraud experienced" in the sector.
- **Smallholders often cannot participate.** Under Ghana's Grains Council
  WRS, *no* targeted smallholder received a tradable certified receipt —
  volumes were too small. Aggregators got them instead.
- **Bank reluctance** to lend against receipts, slowing adoption.
- **Over-engineering.** Research on African WRS concludes that benefits are
  realised when expensive collateral management and elaborate grading are
  *not* imposed wholesale, and recommends community warehouses over
  commercial ones.

**The direct implication for RCU:** the last point cuts against this
blueprint's instincts. RCU adds *more* process — dual grading, rotation,
cross-district re-grading — to a system whose documented failure mode
includes excessive process. **The controls in Section 6.4 are necessary for
monetary integrity and are simultaneously a real adoption risk.** That
tension is unresolved and should be watched closely in Phase 1.

The smallholder-exclusion finding is equally important: without deliberate
design for small deposits, RCU will end up serving aggregators and traders
rather than the farmers it exists for. **Minimum deposit sizes must be set
low enough for a one-acre farmer**, even though that raises per-unit
inspection cost.

---

## 11.4 Digital community currency — Sarafu, Kenya (2010–present)

Grassroots Economics' Sarafu ran roughly 55,000 users and about 300 million
units of recorded transactions between January 2020 and June 2021, moving
from paper vouchers to feature-phone interfaces and later to blockchain.

**What Sarafu proves:** community currency works at tens of thousands of
users in low-income Kenyan settings; feature-phone interfaces are viable;
circulation requires *cycles* in the transaction network, not just
transactions; local institutions act as hubs; women's participation and
early adopters are disproportionately important. A randomised controlled
trial found positive effects on food expenditure and local trade.

**What Sarafu warns about:** research found users perceived it as an
*inferior substitute* for real money, concluding such systems "can only be
transitional." Circulation was highly modular and geographically localised —
value did not travel far. Sarafu is also pegged to the shilling and backed
via mobile money, so it does not test an unpegged unit.

**The most actionable finding: circulation requires closed loops.** Network
analysis showed that money circulates only where cycles exist — A pays B, B
pays C, C pays A. This is a precise, measurable operationalisation of the
"density over breadth" rule in Section 9.2, and Phase 1 should measure cycle
formation directly rather than only counting transactions.

---

## 11.5 Offline digital currency — the CBDC literature (2020–present)

Central banks have studied offline payment extensively, and the findings are
unambiguous.

**The core result: double-spending cannot be prevented offline by software
or cryptography alone.** It requires tamper-resistant secure hardware — and
the Riksbank's blunt observation is that "100% tamper-proof devices do not
exist." The Bank of Canada frames it as a trilemma: a system can have offline
spending, absence of double-spending, and recovery data — but not all three.

**Standard mitigations**, all adopted in Section 5.5: holding limits on
offline wallets (typically a few hundred currency units), caps on
consecutive offline transactions, mandatory periodic reconciliation, and
post-hoc detection with de-anonymisation of double-spenders.

**Two warnings worth internalising.** A compromised offline device is
effectively a printing press whose output is undetectable until
reconciliation. And the secure-element manufacturer is itself a systemic
trust dependency — in principle able to conduct double-spend attacks at
scale. For a cooperative system buying commodity NFC hardware, that
dependency is entirely unavoidable and should be stated rather than ignored.

---

## 11.6 Honest novelty assessment

| Component | Prior art | Novel here? |
|---|---|---|
| Commodity backing | Graham 1937 | No |
| Warehouse receipts as finance | Tanzania WRS 2005 | No |
| Demurrage | Gesell; Wörgl 1932 | No |
| Digital community currency | Sarafu 2010 | No |
| Offline digital payment | CBDC research | No |
| Decentralised issuance | Cooperative banking | No |
| **Decay rate calibrated to physical spoilage of the specific backing** | — | **Yes** |
| **Two tiers separating exchange medium from store of value by construction** | Partial | **Largely yes** |
| **Bearer warehouse receipts circulating at retail with offline verification** | — | **Yes** |

Three genuine contributions is a strong result. **It is a much stronger
claim than "seven things never combined," because it is defensible.** A
reviewer who knows the literature will dismiss an overclaim instantly and
will take a precise, well-cited claim seriously.

The first contribution is the most intellectually interesting. Gesellian
demurrage has always been open to the objection that the rate is arbitrary —
why 1% and not 2%? Tying it to the measured spoilage rate of the backing
commodity gives it a physical referent for the first time. **That is a real
idea, and it is worth writing up on its own.**

---

## 11.7 Reading list

**Essential:**
- Graham, B. (1937) *Storage and Stability*
- Friedman, M. (1951) "Commodity-Reserve Currency" — the strongest critique
- Coulter & Onumah (2002) "The role of warehouse receipt systems in enhanced
  commodity marketing and rural livelihoods in Africa", *Food Policy* 27
- Lietaer, B. "The Wörgl Experiment"
- Ruddick, W. et al. on Sarafu; Mqamelo (2022) RCT results

**Also relevant:**
- Cooper, R. (1988) "Toward an International Commodity Standard?", *Cato
  Journal* 8(2)
- FAO (2016) *Designing warehouse receipt legislation*
- Aboagye (2023) "Structuring African Warehouse Receipt Systems to Succeed"
- BIS Working Paper 1123 on offline CBDC
- Gesell, S. (1916) *The Natural Economic Order*
