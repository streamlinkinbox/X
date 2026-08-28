# 2. Commodity classes

Full generated parameter tables are in [Annex A](annex-a-parameters.md).
This section covers what the tables cannot: which classes are *sound*, which
are *dangerous*, and which should never be issued at all.

## 2.1 What makes a commodity monetisable

A class is only fit to back currency if it satisfies **all six** of these.
Failing even one is disqualifying, and several of the original twenty fail.

| Test | Question | Fails if |
|---|---|---|
| **Verifiable** | Can an inspector confirm quantity and quality in under an hour with field tools? | Requires a laboratory |
| **Gradable** | Do two independent inspectors reach the same grade? | Grading is subjective |
| **Storable** | Does it survive to the next inspection at predictable loss? | Loss rate is erratic |
| **Fungible** | Is one unit substitutable for another? | Each item is unique |
| **Liquid** | Can meaningful volume be sold locally within 30 days? | Only one buyer exists |
| **Legitimate** | Is production lawful and non-extractive? | Monetising it drives harm |

## 2.2 Classification by soundness

### Sound — issue in Phase 1

| Class | Why |
|---|---|
| `GR` Grains & Cereals | Gradable by moisture meter and sieve; deep local market; existing WRS precedent; the natural anchor |
| `FE` Iron & Steel | Weighable, fungible, deep scrap market, minimal grading dispute |
| `CM` Construction Materials | Except cement — see below. Sand and gravel are trivially verified, always in demand |
| `PM` Precious Metals | Assayable, globally priced, ideal store of value — **but see the sourcing problem** |

### Workable — Phase 2 with specific controls

| Class | Required control |
|---|---|
| `WD` Wood & Timber | Certified-source-only gate; plantation timber preferred |
| `TX` Textiles & Fibers | Standard bale grading; export price reference |
| `BF` Biofuels | **Exclude charcoal**; briquettes and biogas only |
| `CU` Copper & Aluminium | Vault-grade custody; highest theft risk per volume |
| `SC` Salt & Chemicals | Split the class — see below |
| `RB` Processed Rubber | Covered storage mandatory |
| `LV` Meat & Livestock | Separate custody regime — see below |

### Problematic — redesign before considering

| Class | Problem |
|---|---|
| `DA` Dairy | Class spans honey (millennia) and raw milk (hours). Incoherent as one series |
| `MH` Medicinal & Herbal | Grading subjective, market thin — easiest class to inflate a valuation in |
| `CG` Ceramics & Glass | Breakage is the real shrinkage; thin resale market |
| `PL` Plastics | Physically stable, so belongs in Tier B; priced off crude, so carries oil risk |
| `ST` Stone & Marble | Nearly indestructible, nearly unsellable. Only 13% of holders redeemable in 30 days |
| `SM` Strategic Minerals | No local market at all; redemption needs an export buyer and an FX channel |

### Should not be issued

| Class | Reason |
|---|---|
| `FP` Fresh Produce | Spoils faster than notes can circulate. A 6-month note against tomatoes is a promise nobody can keep. **Use forward vouchers instead** — a claim on next week's harvest, not a currency |
| `WT` Water | Not a stored good but a delivery right. Monetising water in a drought-prone region means the currency gets blamed for thirst. Politically radioactive |
| `EN` Energy Credits | **No physical stock exists.** It is a forward claim on future generation — a promise, not a pile. Carries counterparty risk no inspection can eliminate. This is the one class that abandons the system's founding principle |

**Recommendation: launch with four classes, not twenty.** `GR`, `FE`, `CM`,
and one of `WD`/`LV` depending on the region. Twenty classes means twenty
grading manuals, twenty inspector training programmes and twenty price
discovery problems, before anyone has proved that one works.

---

## 2.3 The specific problems in detail

### Livestock: decay is the wrong model

A calf **gains** value as it grows. An ox loses value as it ages past prime.
A goat has a 3–8% annual chance of simply dying. None of that is
exponential decay from a fixed grace period.

Livestock also cannot be warehoused in any normal sense. It must be fed and
watered — a live-animal warehouse has *ongoing input costs*, unlike a grain
shed. And the collateral can walk away, get sick, or be quietly swapped for
a worse animal.

**Correct treatment:** a mortality-and-growth-adjusted revaluation, not
demurrage. Herd-level rather than animal-level backing. Compulsory ear-tag
or brand registration, quarterly herd audit, and a mortality pool funded by
a levy on issuance. **This is a different financial instrument** that
happens to share the note format. Treating it as just another Tier A class
will produce disputes within the first year.

### Cement is not a stable material

Bagged Portland cement absorbs atmospheric moisture and is substantially
unusable after roughly six months in humid conditions, and faster in coastal
or lakeside storage. Listing it under "Construction Materials — 0% decay,
indefinite validity" is a factual error that a builder will discover the
first time he redeems a two-year-old note for a hardened bag.

**Fix:** move cement to Tier A with a 3-month grace and 4%/month decay, or
exclude it. Sand, gravel, limestone and fired brick remain properly Tier B.

### Fertiliser is not a stable chemical

Urea cakes and loses nitrogen; NPK blends segregate and absorb moisture.
Real-world degradation in humid storage far exceeds the 0.5%/year assigned
to Salt & Chemicals.

**Fix:** split into `SC-A` (fertiliser — Tier A, 2%/month after 6 months)
and `SC-B` (salt, soda ash, lime — genuinely permanent, Tier B).

### Precious metals: the sourcing problem

Artisanal gold in the Great Lakes region carries serious conflict-minerals
exposure. A currency system that accepts undocumented gold will, sooner or
later, be found to have monetised gold from a sanctioned or conflict-linked
source. The reputational and legal consequence would be terminal — and it
would arrive precisely when the system is large enough to be noticed.

**Fix:** require OECD Due Diligence Guidance documentation for every gold
deposit, or exclude artisanal gold entirely and accept only refiner-marked
bullion. The second option is more restrictive and much safer.

### Strategic minerals: no local market

Coltan and cobalt have no local buyers. A holder of `SM` notes wanting
physical redemption receives a sack of ore with no one nearby to sell it to.
The model shows only **15%** of outstanding `SM` notes could be honoured in
a 30-day run.

Worse, monetising conflict-adjacent minerals invites exactly the geopolitical
attention the risk register wants to avoid.

**Fix:** exclude from Phase 1 and 2. If ever included, cap at 5% of
federation issuance and disclose the redemption constraint on the note face.

---

## 2.4 Grading

Everything rests on grading. If grading is corrupt or inconsistent, the
currency is backed by whatever an inspector says it is backed by.

### Requirements

1. **Written, illustrated, translated manuals.** Photographs of Grade A, B
   and C for each class, in the local language.
2. **Field-tool grading only.** Moisture meter, sieve, scale, visual
   reference card. Anything needing a lab cannot be a Phase 1 class.
3. **Two independent inspectors** for deposits above a threshold, grading
   blind, before comparing.
4. **Published variance statistics per inspector.** An inspector who
   consistently grades higher than peers is visible in the data — this is
   the single most effective anti-corruption control available, and it is
   nearly free.
5. **Random re-grading** of 10% of deposits by a rotating inspector from
   another district.

### Grade-to-value mapping

| Grade | Issuance factor | Meaning |
|---|---|---|
| A | 1.00 | Meets full specification |
| B | 0.85 | Minor defects, fully saleable |
| C | 0.65 | Saleable at discount |
| Reject | 0.00 | Not eligible collateral |

Applied *before* the class haircut. Grade C maize at a 30% haircut yields
0.65 × 0.70 = **45.5%** of assessed market value in notes. Depositors will
find this harsh. It is the price of a currency that does not fail.
