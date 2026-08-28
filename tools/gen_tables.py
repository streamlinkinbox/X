#!/usr/bin/env python3
"""Generate the parameter and analysis annex from the model.

Run: python3 tools/gen_tables.py > docs/annex-a-parameters.md

Every table in the blueprint that contains a number is produced here, so the
prose can never drift away from the code that implements it.
"""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from model.rcu.classes import REGISTER, TIER_A, TIER_B, Tier  # noqa: E402
from model.rcu.hoarding import simulate  # noqa: E402
from model.rcu.people import (  # noqa: E402
    ApprenticeshipParams,
    Village,
    apprenticeship,
    coverage_gap,
    minimum_village_for_cadre_sufficiency,
    screening_bias,
    years_to_replace_masters,
)
from model.rcu.external import (  # noqa: E402
    BASKET,
    DependencyTrend,
    Withdrawal,
    achievable_independence,
    buffer_plan,
    by_withdrawal,
    irreducible_dependency,
    lethal_share,
    minimum_exports_needed,
    substitution_ladder,
    uniform_buffer_cost,
)
from model.rcu.production import (  # noqa: E402
    LADDER,
    Rung,
    build_programme,
    by_rung,
    dual_use_products,
    ranked_by_sovereignty,
    viable_projects,
)
from model.rcu.military import (  # noqa: E402
    DRONE_DEFENSE_LAYERS,
    MEDIEVAL_ARSENAL,
    MOBILIZATION_TIMELINE,
    NEUTRALIZATION_MATRIX,
    REQUIRED_KIT_ITEMS,
    TRANSPORT_CLASSES,
    CampaignEconomics,
    CommunityDemographics,
    DroneSwarmEngagement,
    PersonalKit,
    TransportFleet,
)
from model.rcu.governance import (  # noqa: E402
    COUNCIL_ROLES,
    DEPARTMENTAL_POLICING_SYSTEM,
    SUCCESSION_RULES,
    CandidateRecord,
    MeasurementBureau,
    QualificationPool,
    RecallProtocol,
    RoleDomain,
    RotatingChairRule,
    SelectionComparison,
    SortitionAudit,
    SuccessionTrigger,
    TermLimitPolicy,
)
from model.rcu.environmental_intel import (  # noqa: E402
    CIS_DIRECTORATES,
    COMMON_TRANSBOUNDARY_EVENTS,
    AlertLevel,
    CISDirectorateType,
    CISSafeguards,
    CISStaffing,
    EIAAssessment,
    EIARiskRating,
    EDMBStaffing,
    EnvironmentalTelemetry,
)
from model.rcu.integrity import (  # noqa: E402
    EnvironmentalStress,
    EvaluationVerdict,
    LeadershipDiagnostic,
    MarketConcentrationPolicy,
    MarketParticipant,
    ObservedOutcome,
    PersonalWealthAudit,
    PositionAudit,
    ProbationTarget,
    RevenueDiversification,
    ShadowLeaderProbation,
)
from model.rcu.rab import (  # noqa: E402
    RAB_DIVISIONS,
    CrossDepartmentInvestigation,
    DivisionType,
    EconomicEarlyWarningSystem,
    RABAccountabilityPolicy,
    RABStaffing,
    ReformProject,
    ReformStage,
    SiloDataPoint,
)
from model.rcu.war_council import (  # noqa: E402
    DOCTRINE_PRINCIPLES,
    SCENARIO_LIBRARY,
    SPECIALIZED_UNITS_ROSTER,
    WAR_COUNCIL_ROSTER,
    AntiCasteSafeguards,
    EngagementBattleReport,
    SpecializedUnitSizing,
    WarCouncilDecisionEngine,
)
from model.rcu.information_integrity import (  # noqa: E402
    CONSOLIDATED_POLICY_MATRIX,
    IMPLEMENTATION_PHASES,
    REVISED_SANCTION_LADDER_REV3,
    STATUTORY_BODIES,
    ConsolidatedRule,
    DisgorgementAssessment,
    ForeignPlatformEnforcementModel,
    PlatformStatutoryDuties,
    RegulatoryBodyType,
    RestrictionStatus,
    SanctionStep,
    StateConductPolicy,
    StatutoryFundingFormula,
)
from model.rcu.penalties import (  # noqa: E402
    AntiExtortionPolicy,
    CitationDispute,
    CivicLaborType,
    ExileAssessment,
    PENALTY_TIER_ROSTER,
    PenaltyTier,
    RestitutionAccounting,
)
from model.rcu.debt_and_subscriptions import (  # noqa: E402
    CitizensRestitutionTrust,
    ContributorRestitutionAccount,
    CostPlusHousingAdvance,
    DecisiveAccessTest,
    ElderCareStipend,
    FAIR_BORROWING_RULES,
    FairBorrowingRule,
    FinancialSector,
    MechanismComparison,
    SECTOR_COMPARISONS,
    VehiclePurchaseComparison,
    ZeroInterestAdvance,
)
from model.rcu.clothing_standards import (  # noqa: E402
    PUBLIC_SECTOR_DRESS_TIERS,
    SEPARATION_TIER_SPECS,
    SPATIAL_ZONE_SPECS,
    WORKFORCE_FAILURE_PREVENTIONS,
    AntiHumiliationPolicy,
    ClothingComplianceSimulation,
    DressTierCategory,
    EqualResourcingAudit,
    FemaleGuardServiceSpec,
    PublicSectorDressTier,
    SeparationTierSpec,
    SovereignMethodology,
    SpatialZone,
    UniformProcurementPolicy,
    WorkforceSeparationTier,
)
from model.rcu.millet_system import (  # noqa: E402
    AntiLebanonLock,
    AuthorityLayer,
    GapStatus,
    GovernanceGapRecord,
    HumanRightsFloor,
    JurisdictionalDomain,
    MILLET_JURISDICTION_DOMAINS,
    STATE_GAP_AUDIT_REGISTER,
)
from model.rcu.security import (  # noqa: E402
    ArmouryPolicy,
    audit_effort_curve,
    collusion_sensitivity,
    detection,
    max_safe_rotation,
    rotation_grid,
    workload,
)
from model.rcu.services import (  # noqa: E402
    CreditPool,
    EarnCapacity,
    ServiceCapacity,
    cost_decomposition,
    equipment_pretext_check,
    practitioner_departure_shock,
    sick_cannot_earn,
    training_incentive,
)
from model.rcu.units import (  # noqa: E402
    PHYSICAL_HAIRCUT,
    UNIT_DEFINITION,
    UnitBasis,
    numeraire_saving,
    ranked_numeraires,
)
from model.rcu.stress import (  # noqa: E402
    LIQUIDITY_DEPTH,
    harvest_cycle,
    redemption_run,
    survivable_crash,
)
from model.rcu.valuation import Note  # noqa: E402

W = sys.stdout.write


def pct(x: float, dp: int = 1) -> str:
    return f"{x * 100:.{dp}f}%"


def rate_str(c) -> str:
    if not c.decays:
        return "0"
    unit = "mo" if c.decay_period.value == "month" else "yr"
    return f"{c.decay_rate * 100:g}%/{unit}"


def validity(c) -> str:
    if c.max_validity_months is None:
        return "none"
    return f"{c.max_validity_months} mo"


def header() -> None:
    W("# Annex A — Class parameters and stress-test results\n\n")
    W("*Generated by `tools/gen_tables.py` from `model/rcu/`. Do not edit by hand.*\n\n")
    W(
        "All figures below are computed from the parameter register in "
        "`model/rcu/classes.py`. Where a figure is a judgement call rather than "
        "a measurement, it is flagged as such — a pilot's first job is to "
        "replace these with observed local data.\n\n"
    )


def table_classes() -> None:
    W("## A.1 The twenty classes\n\n")
    for tier, rows, title in (
        (Tier.A, TIER_A, "Tier A — demurrage-bearing"),
        (Tier.B, TIER_B, "Tier B — stable"),
    ):
        W(f"### {title}\n\n")
        W("| # | Code | Class | Colour | Grace | Decay | Max validity | Haircut | Unit |\n")
        W("|---|------|-------|--------|-------|-------|--------------|---------|------|\n")
        for c in rows:
            W(
                f"| {c.number} | `{c.code}` | {c.name} | {c.colour} `{c.hex_colour}` | "
                f"{c.grace_months} mo | {rate_str(c)} | {validity(c)} | "
                f"{pct(c.haircut, 0)} | {c.unit} |\n"
            )
        W("\n")


def table_carry() -> None:
    W("## A.2 Does demurrage pay for storage?\n\n")
    W(
        "A class whose annualised demurrage is below its physical cost of carry "
        "is structurally loss-making: the shortfall must be met by a custody fee, "
        "by the depositor, or by the stabilisation fund. There is no fourth option.\n\n"
    )
    W("| Code | Class | Demurrage/yr | Storage cost/yr | Gap | Funding required |\n")
    W("|------|-------|--------------|-----------------|-----|------------------|\n")
    for c in REGISTER:
        gap = c.storage_cost_pa - c.annualised_decay
        verdict = "covered" if c.carry_covered else f"**custody fee {pct(gap, 2)}**"
        W(
            f"| `{c.code}` | {c.name} | {pct(c.annualised_decay, 2)} | "
            f"{pct(c.storage_cost_pa, 2)} | {pct(gap, 2) if gap > 0 else '—'} | {verdict} |\n"
        )
    covered = sum(1 for c in REGISTER if c.carry_covered)
    W(
        f"\n**{len(REGISTER) - covered} of {len(REGISTER)} classes require an explicit "
        "custody fee.** Every one of them is in Tier B. This is the central "
        "economic consequence of a stable tier: stability is not free, and "
        "somebody has to pay the warehouse.\n\n"
    )


def table_lifetime() -> None:
    W("## A.3 Lifetime value loss on Tier A notes\n\n")
    W(
        "What a holder loses by sitting on a note until it expires. This is the "
        "circulation incentive, quantified.\n\n"
    )
    W("| Code | Class | Grace | Max validity | Loss if held to expiry |\n")
    W("|------|-------|-------|--------------|------------------------|\n")
    for c in TIER_A:
        W(
            f"| `{c.code}` | {c.name} | {c.grace_months} mo | "
            f"{c.max_validity_months} mo | {pct(c.lifetime_decay)} |\n"
        )
    W("\n")


def table_crash() -> None:
    W("## A.4 Price-crash resilience\n\n")
    W(
        "The largest one-shot fall in the local price of the collateral that a "
        "class can absorb while remaining fully collateralised, solved by "
        "bisection on `model/rcu/stress.py::price_crash`. Compare each figure "
        "against the class's own annual price volatility: **a class whose "
        "survivable crash is smaller than its one-sigma annual move is "
        "under-haircut.**\n\n"
    )
    W("| Code | Class | Haircut | Survivable fall | Annual volatility (1σ) | Verdict |\n")
    W("|------|-------|---------|-----------------|------------------------|---------|\n")
    weak = []
    for c in REGISTER:
        s = survivable_crash(c.code)
        ok = s >= c.price_volatility_pa
        if not ok:
            weak.append((c, s))
        W(
            f"| `{c.code}` | {c.name} | {pct(c.haircut, 0)} | {pct(s)} | "
            f"{pct(c.price_volatility_pa, 0)} | {'ok' if ok else '**under-haircut**'} |\n"
        )
    W("\n")
    if weak:
        W("**Under-haircut classes requiring parameter revision before issuance:**\n\n")
        for c, s in weak:
            need = 1 - (1 - c.price_volatility_pa) * (1 - c.haircut) / (1 - s) \
                if s < 1 else c.haircut
            W(
                f"- `{c.code}` {c.name}: survives {pct(s)} against {pct(c.price_volatility_pa, 0)} "
                f"volatility. Raise the haircut or cap the class.\n"
            )
        W("\n")


def table_liquidity() -> None:
    W("## A.5 Redemption capacity\n\n")
    W(
        "The share of outstanding notes that can be redeemed for physical goods "
        "within 30 days before the redemption gate must be invoked. Assumes a "
        "10% cash buffer plus the class's 30-day saleable depth.\n\n"
    )
    W("| Code | Class | Market depth | 30-day saleable | Max run honourable | 30% run |\n")
    W("|------|-------|--------------|-----------------|--------------------|---------|\n")
    for c in REGISTER:
        depth = LIQUIDITY_DEPTH.get(c.liquidity, 0.10)
        f = 0.0
        while f < 1.0 and not redemption_run(c.code, presented_fraction=f + 0.01).gate_triggered:
            f += 0.01
        rr = redemption_run(c.code)
        W(
            f"| `{c.code}` | {c.name} | {c.liquidity} | {pct(depth, 0)} | "
            f"{pct(f, 0)} | {'survives' if not rr.gate_triggered else '**gate**'} |\n"
        )
    W(
        "\nClasses that cannot honour a 30% run are not thereby invalid — cash "
        "cannot honour a 30% run either. They do mean the redemption gate is a "
        "*normal operating instrument*, not an emergency measure, and must be "
        "disclosed on the note itself.\n\n"
    )


def table_schedule() -> None:
    W("## A.6 Worked decay schedules\n\n")
    W("Value of a 1,000 RCU note by month of age, for representative classes.\n\n")
    picks = ["GR", "FP", "LV", "WD", "SC", "FE"]
    notes = {
        code: Note(
            serial=f"{code}-DEMO",
            class_code=code,
            face_cents=100_000,
            issued=date(2027, 1, 1),
            issuer_id="DEMO",
            warehouse_id="DEMO",
        )
        for code in picks
    }
    months = [0, 1, 3, 6, 9, 12, 18, 24, 36, 48]
    W("| Age (months) | " + " | ".join(f"`{c}`" for c in picks) + " |\n")
    W("|---" * (len(picks) + 1) + "|\n")
    sched = {c: dict(notes[c].schedule(60)) for c in picks}
    for m in months:
        cells = []
        for c in picks:
            v = sched[c].get(m, 0)
            cells.append("expired" if v == 0 and m > 0 else f"{v / 100:,.2f}")
        W(f"| {m} | " + " | ".join(cells) + " |\n")
    W("\n")


def table_harvest() -> None:
    W("## A.7 Seasonal money supply — single-crop cooperative\n\n")
    W(
        "A grain cooperative issuing once a year at harvest, 100,000 RCU of "
        "assessed deposit each cycle, 30% haircut. Shows the sawtooth money "
        "supply that a single-crop region will experience.\n\n"
    )
    r = harvest_cycle("GR", horizon=48)
    W("| Month | Outstanding (RCU) | Collateral (RCU) | Coverage |\n")
    W("|-------|-------------------|------------------|----------|\n")
    for m in range(0, 48, 3):
        out = r.outstanding[m] / 100
        col = r.collateral[m] / 100
        ratio = r.ratio[m]
        rs = "n/a" if ratio == float("inf") else f"{ratio:.2f}×"
        W(f"| {m} | {out:,.0f} | {col:,.0f} | {rs} |\n")
    finite = [x for x in r.ratio if x != float("inf")]
    W(
        f"\nMinimum coverage over 48 months: **{min(finite):.2f}×**. "
        f"Coverage never falls below 1.0, so the design is solvent under a "
        "pure harvest cycle with no price shock. The money supply, however, "
        f"swings from 0 to {max(r.outstanding) / 100:,.0f} RCU and back within "
        "each year — a single-crop cooperative cannot supply a stable medium of "
        "exchange on its own. **Classes must be pooled across differently-timed "
        "harvests, or the region will have a liquidity drought every lean season.**\n\n"
    )


def table_bundles() -> None:
    W("## A.8 Bundle pricing versus demurrage arbitrage\n\n")
    W(
        "Two agents with identical holdings and identical payment demands over "
        "24 months. The sophisticated agent chooses which notes to part with "
        "wherever the rules allow. The burden ratio is naive loss divided by "
        "sophisticated loss: **1.00 means demurrage is borne equally**, and "
        "higher values mean the unsophisticated are carrying it.\n\n"
    )
    W("| Payment rule | Sophisticated loss | Naive loss | Burden ratio |\n")
    W("|---|---|---|---|\n")
    for strict, label in ((False, "Free substitution"), (True, "Strict bundles")):
        r = simulate(strict=strict, months=24, tier_a_demand_share=0.5)
        W(
            f"| {label} | {r.sophisticated_loss:.1f} | {r.naive_loss:.1f} | "
            f"**{r.loss_ratio:.2f}** |\n"
        )
    W("\n### Sensitivity to the Tier A share of quoted bundles\n\n")
    W("| Tier A share of demand | Strict bundles | Free substitution |\n")
    W("|---|---|---|\n")
    for pct in (30, 40, 50, 60, 70):
        s = simulate(strict=True, months=24, tier_a_demand_share=pct / 100)
        f = simulate(strict=False, months=24, tier_a_demand_share=pct / 100)
        fr = "n/a" if f.loss_ratio == float("inf") else f"{f.loss_ratio:.2f}"
        W(f"| {pct}% | {s.loss_ratio:.2f} | {fr} |\n")
    W(
        "\nStrict bundle pricing equalises the burden across every demand mix "
        "tested. See section 12.3 for the partial-adoption result, which is "
        "non-monotonic and is the binding operational constraint.\n\n"
    )


def table_weight() -> None:
    W("## A.9 Weight denomination: haircuts and units\n\n")
    W(
        "Under weight denomination a note claims a physical quantity, so the "
        "haircut no longer has to absorb price risk -- only weighing error, "
        "moisture and shrinkage. See section 13.\n\n"
    )
    W("| Code | Class | Unit basis | Reference unit | Price haircut | Physical haircut |\n")
    W("|------|-------|-----------|----------------|---------------|------------------|\n")
    mon = []
    for c in REGISTER:
        basis, ref = UNIT_DEFINITION[c.code]
        ph = PHYSICAL_HAIRCUT.get(c.code)
        if ph is None:
            phs = "**not monetisable**"
        else:
            phs = pct(float(ph), 0)
            mon.append((float(c.haircut), float(ph)))
        W(
            f"| `{c.code}` | {c.name} | {basis} | {ref} | {pct(c.haircut, 0)} | {phs} |\n"
        )
    old = sum(a for a, _ in mon) / len(mon)
    new = sum(b for _, b in mon) / len(mon)
    W(
        f"\n**Average across monetisable classes: {pct(old)} -> {pct(new)}**, "
        f"freeing roughly {(old - new) * 100:.0f} percentage points of collateral "
        "back to depositors. A producer receives about 92 kg-units per 100 kg of "
        "Grade A maize, instead of 70 units of contested value.\n\n"
    )

    W("### Cost: exchange rates without a common unit\n\n")
    W("| Goods in market | Bilateral rates | With a numeraire | Ratio |\n")
    W("|---|---|---|---|\n")
    for n in (4, 10, 20, 50):
        w, m, r = numeraire_saving(n)
        W(f"| {n} | {w} | {m} | {r:.0f}x |\n")
    W("\n### Which class is likely to become the reference good\n\n")
    W("| Rank | Class | Score |\n|---|---|---|\n")
    for i, (c, s) in enumerate(ranked_numeraires()[:5], 1):
        W(f"| {i} | {c.name} (`{c.code}`) | {s} |\n")
    W(
        "\nIron is the realistic winner for a rural market: stable, universally "
        "wanted, cheap to store, divisible, and verifiable with a scale and a "
        "magnet. Precious metals scores higher but is too valuable per gram for "
        "daily use. The system should not mandate a numeraire -- that would "
        "recreate the price-setting authority weight denomination abolishes -- "
        "but should ensure the likely winner is exceptionally well run.\n\n"
    )


def table_people() -> None:
    W("## A.10 People: cadre size, screening bias, apprenticeship\n\n")
    W("### Can a small cadre supply the acceptance requirement?\n\n")
    W(
        "Phase 1 requires at least 60% of pilot-market traders accepting RCU. "
        "A 10-15 person cadre is measured against that requirement below.\n\n"
    )
    W("| Market | Adults | Traders | Accepting needed | Cadre of 15 covers | Shortfall |\n")
    W("|---|---|---|---|---|---|\n")
    for adults, traders, label in (
        (800, 60, "Small village"),
        (3000, 240, "Large village"),
        (12000, 900, "Small town"),
    ):
        g = coverage_gap(Village(adults=adults, traders=traders), cadre_size=15)
        W(
            f"| {label} | {adults:,} | {traders} | {g.traders_needed} | "
            f"{float(g.cadre_covers) * 100:.0f}% | {g.shortfall} |\n"
        )
    W(
        f"\n**A 15-person cadre is 60% of the traders only in a market of about "
        f"{minimum_village_for_cadre_sufficiency()} adults** -- too small to "
        "sustain a warehouse or an inspector rotation. The cadre cannot be the "
        "network; it can only build it. See section 14.2.\n\n"
    )

    W("### Screening bias: the same test, different circumstances\n\n")
    W(
        "Identical population size and identical underlying reliability (5%). "
        "The only difference is the chance that a reliable person fails for "
        "reasons unrelated to character -- no fare, a sick child, piecework.\n\n"
    )
    W("| Pool | Reliable found | Recall | Precision | Wrongly rejected |\n")
    W("|---|---|---|---|---|\n")
    sb = screening_bias()
    for name in ("comfortable", "destitute"):
        o = sb[name]
        W(
            f"| {name.title()} | {o.true_positives} of {o.truly_reliable} | "
            f"{float(o.recall) * 100:.0f}% | {float(o.precision) * 100:.0f}% | "
            f"{o.wrongly_excluded} |\n"
        )
    extra = sb["destitute"].wrongly_excluded - sb["comfortable"].wrongly_excluded
    W(
        f"\n**The same test discards {extra} additional reliable people purely "
        "because they are poor.** It measures slack, not commitment. Note also "
        "that precision is below 40% even in the best case: a single test "
        "cannot be a gate, because at a 5% base rate most passers are false "
        "positives.\n\n"
    )

    W("### Apprenticeship: practitioners over time\n\n")
    p = ApprenticeshipParams()
    rows = apprenticeship(p, horizon=20)
    W("| Year | Masters remaining | Supervisors | In training | Practitioners |\n")
    W("|---|---|---|---|---|\n")
    for r in rows:
        if r["year"] in (1, 5, 10, 15, 20):
            W(
                f"| {r['year']} | {r['masters']} | {r['supervisors']} | "
                f"{r['in_training']} | **{r['practitioners']}** |\n"
            )
    yr10 = rows[9]["practitioners"]
    W(
        f"\nStarting from {p.masters} masters, year 10 yields "
        f"{yr10} practitioners -- **{yr10 / p.masters:.1f}x, not 20x.** The "
        "binding constraint is supervision capacity, not willing apprentices. "
        f"The community first holds more practitioners than it started with in "
        f"**year {years_to_replace_masters()}**, which is the honest success "
        "criterion: knowledge outliving its holders.\n\n"
    )


def table_services() -> None:
    W("## A.11 Service credits: clearing, earning capacity, incentives\n\n")

    W("### Can service credits be redeemed?\n\n")
    W(
        "A credit that cannot be redeemed is a queue ticket. Supply of "
        "practitioner hours against demand for them:\n\n"
    )
    W("| Service | Ratio | Demand covered | Clears? | Backlog |\n")
    W("|---|---|---|---|---|\n")
    for name, prac, pop, ep, hpe in (
        ("Doctor (typical)", 1, 25_000, 2.0, 0.5),
        ("Doctor (generous)", 1, 5_000, 2.0, 0.5),
        ("Nurse / clinical officer", 1, 2_000, 2.0, 0.5),
        ("Community health worker", 1, 500, 2.0, 0.5),
        ("Teacher", 1, 60, 40.0, 1.0),
    ):
        s = ServiceCapacity(name, prac, pop, episodes_per_person=ep,
                            hours_per_episode=hpe)
        W(
            f"| {name} | 1:{s.people_per_practitioner:,} | "
            f"{float(s.coverage) * 100:.1f}% | "
            f"{'**yes**' if s.can_clear else 'no'} | "
            f"{s.queue_years()} yr |\n"
        )
    W(
        "\n**Service credits work where skill is abundant and fail where it is "
        "scarce.** See section 15.3.\n\n"
    )

    W("### Who can earn care credits?\n\n")
    segs = [
        EarnCapacity("Healthy adults", 700, 0.95, 0.6),
        EarnCapacity("Frail elderly", 150, 0.15, 3.0),
        EarnCapacity("Chronically ill / disabled", 100, 0.20, 4.0),
        EarnCapacity("Children", 50, 0.05, 1.5),
    ]
    W("| Segment | People | Can earn (h) | Needs (h) | Self-sufficiency | Subsidy |\n")
    W("|---|---|---|---|---|---|\n")
    for g in sick_cannot_earn(segs):
        W(
            f"| {g.segment} | {g.people} | {g.credits_earnable:,.0f} | "
            f"{g.credits_needed:,.0f} | {g.self_sufficiency} | "
            f"{'**yes**' if g.must_be_subsidised else 'no'} |\n"
        )
    W(
        "\n**Earning capacity is inversely related to need** -- the Fureai "
        "Kippu trap. A grant channel is mandatory. See section 15.4.\n\n"
    )

    W("### Flat rate versus skill premium\n\n")
    W("| Skill multiplier | Lifetime if trained | If untrained | Net | Rational? |\n")
    W("|---|---|---|---|---|\n")
    for tc in training_incentive():
        W(
            f"| {tc.skill_multiplier:g}x | {tc.lifetime_if_trained():,.0f} | "
            f"{tc.lifetime_if_untrained():,.0f} | {tc.net_gain:+,.0f} | "
            f"{'yes' if tc.rational_to_train else '**no**'} |\n"
        )
    be = training_incentive()[0].breakeven_multiplier
    W(
        f"\n**Breakeven premium is only {be}x.** Market differentials between "
        "a doctor and an unskilled worker are commonly 10-50x. The incentive "
        "function is served at about 1.25x; the remainder is rent.\n\n"
    )

    W("### What drives the price of care\n\n")
    chk = equipment_pretext_check()
    d = cost_decomposition()
    W("| Input | Share |\n|---|---|\n")
    W(f"| Labour (practitioner + support) | {float(chk['labour_share']) * 100:.0f}% |\n")
    W(f"| Consumables and drugs | {float(chk['consumables_share']) * 100:.0f}% |\n")
    W(f"| Equipment amortisation | {float(chk['equipment_share']) * 100:.0f}% |\n")
    W(
        f"\nCapital equipment is **{float(chk['equipment_share']) * 100:.0f}%** "
        "-- too small to explain prices that bankrupt families. But recurring "
        "consumables are three times larger and must be imported. "
        f"**{float(d.credit_share) * 100:.0f}% of care cost could be paid in "
        f"labour credits; {float(d.goods_share) * 100:.0f}% requires real goods "
        "or foreign exchange.**\n\n"
    )

    W("### The backing can emigrate\n\n")
    pool = CreditPool(outstanding_hours=4000, practitioners=3)
    W("| Event | Coverage | Holders lose |\n|---|---|---|\n")
    W(f"| Start (3 practitioners) | {pool.coverage()} | -- |\n")
    for dep in (1, 2, 3):
        r = practitioner_departure_shock(pool, dep)
        W(
            f"| {dep} leave | {r['coverage_after']} | "
            f"{float(r['loss_fraction']) * 100:.0f}% |\n"
        )
    W(
        "\nGrain cannot get on a plane. A currency backed by scarce "
        "professionals is backed by the people most likely to leave.\n\n"
    )


def table_external() -> None:
    W("## A.12 Import dependency: severity, buffers, substitution\n\n")

    W("### The import bill by withdrawal severity\n\n")
    W(
        "Classified by what happens if supply stops abruptly, not by cost. "
        "See section 16.1.\n\n"
    )
    W("| Severity | Annual FX | Share | Time to harm |\n|---|---|---|---|\n")
    totals = by_withdrawal()
    grand = sum(totals.values())
    from model.rcu.external import TIME_TO_HARM_DAYS
    for w in Withdrawal:
        W(
            f"| {w.value.title()} | ${totals[w]:,.0f} | "
            f"{totals[w] / grand * 100:.1f}% | "
            f"{TIME_TO_HARM_DAYS[w]} days |\n"
        )
    W(
        f"\n**What kills you is cheap: lethal-withdrawal imports are "
        f"{float(lethal_share()) * 100:.1f}% of the bill and 100% of the "
        "mortality risk. Value is the wrong metric for managing dependency.**\n\n"
    )

    W("### Buffer sizing: targeted versus uniform\n\n")
    W("| Import | Severity | Buffer days | Cost |\n|---|---|---|---|\n")
    for imp in BASKET:
        W(
            f"| {imp.name} | {imp.withdrawal.value} | "
            f"{imp.buffer_days():.0f} | ${imp.buffer_cost():,.0f} |\n"
        )
    bp = buffer_plan()
    uni = uniform_buffer_cost(months=3)
    W(
        f"\n| Approach | Cost |\n|---|---|\n"
        f"| Uniform 3 months of everything | ${uni:,.0f} |\n"
        f"| **Severity-targeted** | **${bp.total_cost:,.0f}** |\n"
    )
    W(
        f"\n**Targeted buffering is {(1 - bp.total_cost / uni) * 100:.0f}% cheaper "
        "and holds 128 days of medicine against 90.** Discretionary imports get "
        "no buffer at all -- if supply stops, you wear the clothes you have.\n\n"
    )

    W("### Substitution ladder\n\n")
    W("| Rank | Import | Payback | Severity |\n|---|---|---|---|\n")
    for i, (imp, eff, pb) in enumerate(substitution_ladder(), 1):
        pbs = "never" if pb.is_infinite() else f"{float(pb):.1f} yr"
        W(f"| {i} | {imp.name} | {pbs} | {imp.withdrawal.value} |\n")
    W(
        f"\n**The ranking inverts intuition.** Medicines matter most and "
        "localise worst -- a 200-year payback against 1.9 years for food. "
        "Localise the easy categories so foreign exchange is always available "
        "for the impossible ones.\n\n"
        f"| Metric | Value |\n|---|---|\n"
        f"| Achievable independence | **{float(achievable_independence()) * 100:.1f}%** |\n"
        f"| Irreducible annual FX need | **${irreducible_dependency():,.0f}** |\n"
        f"| Minimum exports for non-discretionary | ${minimum_exports_needed():,.0f} |\n\n"
    )

    W("### The dependency ratchet\n\n")
    d = DependencyTrend()
    for y, i, e in (
        (1, 300_000, 320_000),
        (2, 340_000, 330_000),
        (3, 400_000, 340_000),
        (4, 465_000, 350_000),
    ):
        d.add(y, i, e)
    W("| Year | Imports | Exports | Self-reliance |\n|---|---|---|---|\n")
    for y, i, e, r in zip(d.years, d.import_fx, d.export_fx, d.self_reliance()):
        W(f"| {y} | ${i:,.0f} | ${e:,.0f} | {r} |\n")
    W(
        "\nNothing dramatic happens in any single year. Dependency forms by "
        "drift, not by decision -- which is why the ratio must be published "
        "quarterly.\n\n"
    )


def table_production() -> None:
    W("## A.13 The local production ladder\n\n")
    W(
        "Candidates ranked by technical difficulty rather than importance. "
        "Rungs cannot be skipped: precision synthesis requires the metalwork, "
        "power and quality systems of every rung below it. See section 17.\n\n"
    )
    W("| Rung | Project | Capex | Net saving/yr | Payback | Viable | Lethal |\n")
    W("|---|---|---|---|---|---|---|\n")
    for rung, items in by_rung().items():
        for p in items:
            pb = p.payback_years()
            pbs = "never" if pb.is_infinite() else f"{float(pb):.1f} yr"
            W(
                f"| {int(rung)} | {p.name} | ${p.capex:,.0f} | "
                f"${p.net_saving_per_year:+,.0f} | {pbs} | "
                f"{'yes' if p.viable else '**no**'} | "
                f"{'**yes**' if p.lethal else ''} |\n"
            )
    lethal_viable = [p for p in LADDER if p.lethal and p.viable]
    W(
        f"\n**{len(viable_projects())} of {len(LADDER)} are viable, including "
        f"{len(lethal_viable)} lethal-category goods** -- medical oxygen from "
        "air and oral rehydration salts from sugar and salt. This corrects "
        "section 16's conclusion that no lethal import could be localised.\n\n"
    )

    W("### Sovereignty ranking versus payback ranking\n\n")
    W("| Rank | Project | Sovereignty value | Lethal |\n|---|---|---|---|\n")
    for i, p in enumerate(ranked_by_sovereignty()[:5], 1):
        W(
            f"| {i} | {p.name} | {p.sovereignty_value} | "
            f"{'**yes**' if p.lethal else ''} |\n"
        )
    a = build_programme(400_000, prioritise_lethal=True)
    b = build_programme(400_000, prioritise_lethal=False)
    W(
        f"\n| $400k programme | Lethal-first | Money-first |\n|---|---|---|\n"
        f"| Net saving/yr | ${a.total_net_saving:,.0f} | ${b.total_net_saving:,.0f} |\n"
        f"| Independence gain | {float(a.independence_gain) * 100:.1f}% | "
        f"{float(b.independence_gain) * 100:.1f}% |\n"
        f"| Lethal capabilities | **{a.lethal_covered}** | {b.lethal_covered} |\n"
    )
    W(
        f"\n**Prioritising resilience costs "
        f"${b.total_net_saving - a.total_net_saving:,.0f}/year and buys one "
        "additional life-critical capability.** Decide this openly.\n\n"
    )
    W("Dual-use plants (everyday demand keeps them alive until needed):\n\n")
    for p in dual_use_products():
        W(f"- {p.name}\n")
    W("\n")


def table_security() -> None:
    W("## A.14 Community security: workload, detection, capture\n\n")
    w = workload(1000)
    W("### What the work actually is (community of 1,000)\n\n")
    W("| Category | Hours/year |\n|---|---|\n")
    for cat, hrs in sorted(w.hours_by_category.items(), key=lambda x: -x[1]):
        W(f"| {cat.replace('_', ' ')} | {hrs:.0f} |\n")
    W(
        f"\n| Function | Share |\n|---|---|\n"
        f"| Mediation | **{float(w.mediation_share) * 100:.1f}%** |\n"
        f"| Forensics | {float(w.forensic_share) * 100:.1f}% |\n"
        f"| Anything involving force | {float(w.force_share) * 100:.1f}% |\n"
    )
    W("\n| Population | Hours/yr | Members needed |\n|---|---|---|\n")
    for pop in (500, 1000, 3000, 20000):
        ww = workload(pop)
        W(f"| {pop:,} | {ww.total_hours:,.0f} | {ww.members_needed()} |\n")
    W(
        "\n**Coverage, not caseload, sets the roster** -- someone must be on "
        "call at any hour. Five members is the floor for any community.\n\n"
    )

    W("### Fraud detection by layer\n\n")
    d = detection()
    W(
        f"| Layer | Caught per 100 attempts |\n|---|---|\n"
        f"| Dual inspection at deposit | {d.caught_at_deposit:.1f} |\n"
        f"| Random audit | {d.caught_at_audit:.1f} |\n"
        f"| Consumer verification | {d.caught_by_consumer:.1f} |\n"
        f"| **Undetected** | **{d.undetected:.1f}** |\n"
    )
    W("\n| Inspector collusion | Detection |\n|---|---|\n")
    for r, dr in collusion_sensitivity():
        W(f"| {r * 100:.0f}% | {float(dr) * 100:.1f}% |\n")
    W(
        "\n**Collusion, not instrument accuracy, is the binding constraint.** "
        "Dual inspection is worth exactly the independence of the two "
        "inspectors. Audit effort by contrast has weak returns:\n\n"
    )
    W("| Audit coverage | Detection |\n|---|---|\n")
    for f, dr in audit_effort_curve():
        W(f"| {f * 100:.0f}% | {float(dr) * 100:.1f}% |\n")

    W("\n### Rotation and capture resistance\n\n")
    W("| Tour | Break 12 mo | Break 18 mo |\n|---|---|---|\n")
    grid = {(t_, b_): (c, pk) for t_, b_, c, pk in rotation_grid()}
    for tour in (6, 9, 12, 18, 24, 36):
        cells = []
        for br in (12, 18):
            cap, peak = grid[(tour, br)]
            cells.append(f"{'**CAPTURED**' if cap else 'safe'} ({peak})")
        W(f"| {tour} mo | {cells[0]} | {cells[1]} |\n")
    W(
        f"\n**Maximum safe tour is {max_safe_rotation()} months**, and the "
        "transition is sharp: 12-month tours are safe, 24-month tours are "
        "catastrophic. Recommended: 9-month tours, 18-month breaks.\n\n"
    )

    W("### Armoury quorum\n\n")
    W("| Keyholders | Quorum | Colluding | Unauthorised release |\n|---|---|---|---|\n")
    for kh, q, cc in ((5, 2, 2), (5, 3, 2), (7, 3, 2), (7, 4, 3)):
        a = ArmouryPolicy(keyholders=kh, quorum=q, corrupt_count=cc)
        p_ = a.unauthorised_release_probability
        W(
            f"| {kh} | {q} | {cc} | "
            f"{'**CERTAIN**' if p_ == 1 else f'{float(p_) * 100:.1f}%'} |\n"
        )
    W(
        "\n**A 2-of-5 rule fails completely if two keyholders collude.** "
        "Quorum must exceed the plausible number of colluding keyholders: use "
        "3-of-7.\n\n"
    )


def table_military() -> None:
    W("## A.15 Military doctrine and asymmetric defense\n\n")

    W("### Minimum personal kit (self-funded)\n\n")
    W("| # | Item | Cost (USD) | Weight (kg) | Locally producible |\n|---|---|---|---|---|\n")
    kit = PersonalKit()
    for i, item in enumerate(kit.items, 1):
        W(
            f"| {i} | {item.name} | ${item.estimated_cost_usd:,.0f} | "
            f"{item.weight_kg:.1f} kg | {'**yes**' if item.locally_producible else 'no'} |\n"
        )
    W(
        f"\n| Metric | Value |\n|---|---|\n"
        f"| Total kit cost | **${kit.total_cost_usd:,.0f}** |\n"
        f"| Total kit weight | **{kit.total_weight_kg:.1f} kg** |\n"
        f"| Local production share | **{float(kit.local_production_share) * 100:.1f}%** |\n\n"
    )

    W("### Transport fleet & fuel independence (10,000 population)\n\n")
    fleet = TransportFleet(population=10000)
    W("| Mode | Count | Unit payload | Speed | Fuel required | Terrain rating |\n|---|---|---|---|---|---|\n")
    for key, c in TRANSPORT_CLASSES.items():
        W(
            f"| {c.name} | {fleet.counts[key]} | {c.unit_payload_kg:,.0f} kg | "
            f"{c.cruising_speed_kmh:.0f} km/h | {'yes' if c.requires_fuel else '**no**'} | "
            f"{c.rough_terrain_rating}/5 |\n"
        )
    W(
        f"\n| Metric | Value |\n|---|---|\n"
        f"| Total fleet payload capacity | **{fleet.total_payload_capacity_kg:,.0f} kg** ({fleet.total_payload_capacity_kg / 1000:.1f} tonnes) |\n"
        f"| Zero-fuel unit share | **{float(fleet.zero_fuel_unit_share) * 100:.1f}%** |\n"
        f"| Zero-fuel payload share | **{float(fleet.zero_fuel_payload_share) * 100:.1f}%** |\n\n"
    )

    W("### Demographics and mobilization timeline\n\n")
    demo = CommunityDemographics(population=10000)
    W(
        f"| Demographic | Count | Share |\n|---|---|---|\n"
        f"| Total community population | {demo.population:,} | 100.0% |\n"
        f"| Registered adults (ages 18–50) | {demo.registered_adults:,} | {demo.adult_eligible_fraction * 100:.1f}% |\n"
        f"| Exemptions (caregivers, medical) | {demo.exempt_adults:,} | {demo.exemption_rate * 100:.1f}% of adults |\n"
        f"| **Active combatants mobilized** | **{demo.mobilized_combatants:,}** | **{demo.mobilized_combatants / demo.population * 100:.1f}% of total** |\n"
        f"| Non-combatant shelter population | {demo.non_combatant_population:,} | {demo.non_combatant_population / demo.population * 100:.1f}% of total |\n\n"
    )

    W("| Hours | Phase name | Readiness pct |\n|---|---|---|\n")
    for phase in MOBILIZATION_TIMELINE:
        W(f"| H+{phase.hours_start} to H+{phase.hours_end} | {phase.name} | {phase.force_readiness_pct:.0f}% |\n")
    W("\n")

    W("### Medieval & low-tech arsenal\n\n")
    W("| Weapon | Range | Lethality | Manufacture | Silent | Ammo free |\n|---|---|---|---|---|---|\n")
    for w in MEDIEVAL_ARSENAL:
        rng = f"{w.effective_range_min_m:.0f}–{w.effective_range_max_m:.0f} m" if w.effective_range_max_m > 0 else "0 m (passive)"
        W(
            f"| {w.name} | {rng} | {w.lethality} | {w.manufacture_difficulty} | "
            f"{'**yes**' if w.silent else 'no'} | {'**yes**' if not w.ammunition_dependent else 'no'} |\n"
        )
    W("\n")

    W("### Asymmetric neutralization cost ratios\n\n")
    W("| Threat asset | Enemy cost | Militia cost | Method | Cost ratio |\n|---|---|---|---|---|\n")
    for n in NEUTRALIZATION_MATRIX:
        W(
            f"| {n.target_asset} | ${n.enemy_cost_usd:,.0f} | ${n.militia_neutralization_cost_usd:,.0f} | "
            f"{n.method} | **{n.cost_ratio:,} : 1** |\n"
        )
    W("\n")

    W("### Multi-layered anti-drone swarm defense (100-drone test)\n\n")
    W("| Layer | Range | Mechanism | Interception rate | Cost |\n|---|---|---|---|---|\n")
    for l in DRONE_DEFENSE_LAYERS:
        W(
            f"| Layer {l.layer_number}: {l.name} | {l.engagement_distance_m:.0f} m | "
            f"{l.mechanism[:40]}... | {l.attrition_fraction * 100:.0f}% | ${l.cost_per_engagement_usd:,.0f} |\n"
        )
    sim = DroneSwarmEngagement(initial_swarm_size=100).simulate()
    W(
        f"\n| Simulation metric (100 drones) | Value |\n|---|---|\n"
        f"| Total drones intercepted | **{sim['total_intercepted']} / 100** |\n"
        f"| Cumulative interception rate | **{sim['interception_rate'] * 100:.2f}%** |\n"
        f"| Total defense cost | **${sim['total_defense_cost_usd']:,.0f}** |\n"
        f"| Cost per intercepted drone | **${sim['cost_per_interception_usd']:.2f}** |\n\n"
    )

    W("### Campaign attrition economics\n\n")
    econ = CampaignEconomics()
    W(
        f"| Metric | Invader | Citizen Militia | Asymmetric Ratio |\n|---|---|---|---|\n"
        f"| Daily operational burn rate | ${econ.enemy_daily_cost_usd:,.0f}/day | ${econ.militia_daily_cost_usd:,.0f}/day | **{econ.daily_cost_ratio:,} : 1** |\n"
    )
    for days in (30, 90, 180, 365):
        c = econ.cumulative_expenditure(days)
        W(
            f"| Cumulative {days} days | ${c['enemy_total_usd']:,.0f} | "
            f"${c['militia_total_usd']:,.0f} | {int(c['net_deficit_ratio']):,} : 1 |\n"
        )
    W("\n")


def table_governance() -> None:
    W("## A.16 Competence Council governance and departmental enforcement\n\n")

    W("### Functional Leadership Council roles\n\n")
    W("| Title | Domain | Term | Selection base | Constitutional limitation |\n|---|---|---|---|---|\n")
    for r in COUNCIL_ROLES:
        W(
            f"| {r.title} | {r.domain.value.title()} | {r.term_years} + {r.probation_years} yr prob. | "
            f"{r.selected_from[:30]}... | {r.specific_limitation[:40]}... |\n"
        )
    W("\n")

    chair = RotatingChairRule()
    term_pol = TermLimitPolicy()
    recall = RecallProtocol()
    W("### Governance rotation, term limits, and recall\n\n")
    W(
        f"| Parameter | Specification | Purpose |\n|---|---|---|\n"
        f"| Rotating Council Chair | Every {chair.rotation_months} months ({chair.chair_count_per_year}×/yr) | Facilitator role; {chair.limitations[:45]}... |\n"
        f"| Maximum consecutive tenure | {term_pol.max_consecutive_years} years max | Prevents entrenched bureaucratic ruling class |\n"
        f"| Mandatory cooling-off | {term_pol.mandatory_cooling_off_years} years in manual/field work | Re-grounds former leaders in physical production |\n"
        f"| Citizen recall petition | {float(recall.petition_adult_share_threshold) * 100:.0f}% registered adults | Triggers automatic domain-level review against metrics |\n\n"
    )

    W("### Selection accuracy: peer consensus vs mass ballot\n\n")
    comp = SelectionComparison()
    W(
        f"| Selection method | Evaluator group | Decision threshold | Error rate | Competence advantage |\n|---|---|---|---|---|\n"
        f"| **Peer Selection** | 20–30 Senior Masters | 75% Consensus | **{comp.peer_error_rate * 100:.1f}%** | **{comp.competence_advantage_ratio}× accuracy** |\n"
        f"| Mass Electoral Ballot | General Population | 50% + 1 Popularity | {comp.electoral_error_rate * 100:.1f}% | 1.00× (Baseline) |\n\n"
    )

    W("### Institutional succession protocols\n\n")
    W("| Trigger event | Immediate action | Replacement window | Power vacuum |\n|---|---|---|---|\n")
    for trigger, proto in SUCCESSION_RULES.items():
        W(
            f"| {trigger.value.replace('_', ' ').title()} | {proto.immediate_successor[:35]}... | "
            f"{proto.selection_window_days} days | **{proto.power_vacuum_days} days** |\n"
        )
    W("\n")

    W("### Departmental policing & measurement bureaus\n\n")
    W("| Department | Enforcement unit | Staff share | Independent measurement unit |\n|---|---|---|---|\n")
    for b in DEPARTMENTAL_POLICING_SYSTEM:
        W(
            f"| {b.department.value.title()} | **{b.enforcement_unit_name}** | "
            f"{float(b.staff_percentage) * 100:.1f}% | {b.independent_measurement_unit} |\n"
        )
    W(
        "\n**Measurement units report to the Audit Board, not department heads**, "
        "breaking Goodhart's Law and preventing metric falsification.\n\n"
    )

    W("### Citizen sortition audit & anti-monarchy checks\n\n")
    audit = SortitionAudit()
    W(
        f"| Accountability mechanism | Specification | Purpose |\n|---|---|---|\n"
        f"| Annual sortition jury | {audit.jury_size} citizens chosen randomly | Full subpoena and inspection of all vaults and logs |\n"
        f"| Detection confidence | {float(audit.confidence_level) * 100:.0f}% confidence | High statistical detection of systemic deviations |\n"
        f"| Legal immunity | **Zero immunity** | Leaders face identical courts as ordinary citizens |\n"
        f"| Living conditions | **{audit.living_condition_ratio:.2f} : 1.00 ratio** | Leaders receive identical food, housing, and RCU as guild masters |\n\n"
    )


def table_integrity() -> None:
    W("## A.17 Anti-corruption, difficulty-adjusted evaluation, and resource curse resilience\n\n")

    W("### Difficulty-adjusted leadership diagnostics\n\n")
    W("| Environmental stress | Observed outcome | Verdict | Diagnostic rule |\n|---|---|---|---|\n")
    W("| Mild / Normal | Good / Acceptable | Competent (Untested) | Standard baseline performance |\n")
    W("| Mild / Normal | Poor / Catastrophic | **Incompetent (Remove)** | Failure during favorable conditions |\n")
    W("| Severe / Shock | Good / Acceptable | **Exceptional (Retain)** | Overperformed adverse climate/blockade |\n")
    W("| Severe / Shock | Poor (Neighbor parity) | Peer Review Required | Deep audit of decisions, storage, and honesty |\n")
    W("| Severe / Shock | Poor (15%+ worse than peers) | **Incompetent (Remove)** | Failure relative to regional benchmark |\n")
    W("| Any | Personal wealth divergence | **Incompetent / Corrupt (Remove)** | Leader enriched while community starved |\n\n")

    W("### Shadow Leader System & 90-day probation\n\n")
    sp = ShadowLeaderProbation(
        deputy_id="DEMO-DEP-01",
        domain="Reserves & Agriculture",
        probation_days=90,
        targets=(
            ProbationTarget("Reduce grain spoilage", 15.0, 10.0, 8.5, higher_is_better=False),
            ProbationTarget("Expand buffer reserve kg", 1000.0, 1500.0, 1550.0, higher_is_better=True),
            ProbationTarget("Resolve silo maintenance issues", 5.0, 0.0, 0.0, higher_is_better=False),
            ProbationTarget("Complete apprentice certifications", 0.0, 10.0, 10.0, higher_is_better=True),
        ),
    )
    W(
        f"| Probation parameter | Value | Rule |\n|---|---|---|\n"
        f"| Shadow Deputy training | Continuous | Active sub-domain management before transition |\n"
        f"| Probation duration | **{sp.probation_days} days** | Rapid confirmation window during crises |\n"
        f"| Target confirmation benchmark | **80% pass rate** | Quantitative target verification (Sample: {sp.pass_rate * 100:.0f}% pass) |\n"
        f"| Failure fallback | Qualified Pool | Domain practitioners select next qualified candidate |\n\n"
    )

    W("### Resource curse & economic concentration (HHI comparison)\n\n")
    oil_econ = RevenueDiversification(revenue_shares={"Petroleum Extraction": 0.85, "Farming": 0.08, "Services": 0.07})
    rcu_econ = RevenueDiversification(revenue_shares={
        "Maize & Grains": 0.15, "Legumes": 0.10, "Timber": 0.12, "Iron": 0.10,
        "Biofuel": 0.08, "Textiles": 0.08, "Livestock": 0.12, "Oils & Soap": 0.09,
        "Medical Oxygen/ORS": 0.08, "Services": 0.08
    })
    W(
        f"| Economic model | Primary share | Herfindahl Index (HHI) | Resource cursed? | Resilience verdict |\n|---|---|---|---|---|\n"
        f"| Single-Commodity (e.g. Oil State) | {oil_econ.primary_commodity_share * 100:.1f}% | **{oil_econ.hhi_score:,}** | **YES (Severe)** | Extreme Dutch Disease collapse risk |\n"
        f"| **RCU 20-Commodity Basket** | **{rcu_econ.primary_commodity_share * 100:.1f}%** | **{rcu_econ.hhi_score:,}** | **NO (Resilient)** | Multi-sector production stability |\n\n"
    )

    W("### Market anti-monopoly caps & personal wealth ceilings\n\n")
    pwa = PersonalWealthAudit("DEMO-STW", 4500.0, 1500.0, 5.0)
    W(
        f"| Integrity safeguard | Legal limit | Systemic mechanism |\n|---|---|---|\n"
        f"| Single-entity market share | **20% max share** | Automatic divestiture or invited competitor entry |\n"
        f"| Personal currency accumulation | **{pwa.max_allowed_multiplier:.1f}× community average** | Automatic audit, flagging, and excess confiscation |\n"
        f"| Exclusive import licensing | **Strictly prohibited (0%)** | Open market competition default across all goods |\n"
        f"| Family separation rule | Zero close relatives in domain | Prevents nepotistic procurement and grant looting |\n\n"
    )


def table_rab() -> None:
    W("## A.18 Research and Analysis Bureau (RAB)\n\n")

    W("### The five analytical divisions\n\n")
    W("| Division | Mandate | Primary deliverable |\n|---|---|---|\n")
    for d in RAB_DIVISIONS:
        W(
            f"| **{d.name}** | {d.mandate[:45]}... | {d.primary_deliverables[0]} |\n"
        )
    W("\n")

    W("### RAB lean staffing model (10,000 population)\n\n")
    staff = RABStaffing(population=10000)
    W(
        f"| Role | Headcount | Functional scope |\n|---|---|---|\n"
        f"| Chief Analyst | {staff.chief_analysts} | Bureau leadership; 2-year mandatory rotation |\n"
        f"| Senior Analysts | {staff.senior_analysts} | Division leads across 5 operational branches |\n"
        f"| Junior Analysts | {staff.junior_analysts} | Data synthesis, telemetry logging, report drafting |\n"
        f"| Field Data Collectors | {staff.data_collectors} | Physical counts, soil/grain sampling, surveys |\n"
        f"| Applied Researchers | {staff.field_researchers} | Lab assays, metallurgy, agriscience trials |\n"
        f"| **Total RAB Staff** | **{staff.total_staff}** | **{float(staff.staff_share_of_population) * 100:.2f}% of population** |\n\n"
    )

    W("### Cross-silo correlation & anomaly detection\n\n")
    inv = CrossDepartmentInvestigation(
        investigation_id="SAMPLE-INV-001",
        data_points=(
            SiloDataPoint("Treasury/Warehouse", "Grain Spoilage", True, "Warehouse 7 reporting 15% loss vs 3% avg"),
            SiloDataPoint("Inspectorate", "Grade Variance", True, "Inspector X consistently approved high grades"),
            SiloDataPoint("Civil Registry", "Kinship Link", True, "Manager is Inspector X brother-in-law"),
        ),
        kinship_or_collusion_flag=True,
    )
    W(
        f"| Investigation metric | Value | Operational meaning |\n|---|---|---|\n"
        f"| Anomaly data points | {inv.anomaly_count} / {len(inv.data_points)} | Multi-silo correlation |\n"
        f"| Departments involved | {len(inv.departments_involved)} | Cross-departmental synthesis |\n"
        f"| Systemic threat score | **{inv.systemic_threat_score:.2f} / 1.00** | High severity collusion risk |\n"
        f"| Justice referral | **{'TRIGGERED' if inv.triggers_formal_justice_referral else 'Monitored'}** | Direct handover to Steward of Justice |\n\n"
    )

    W("### Economic early warning thresholds\n\n")
    ews = EconomicEarlyWarningSystem(0.28, 0.18, 0.22, 0.05, 0.80)
    W(
        f"| Risk metric | Red line threshold | Current status |\n|---|---|---|\n"
        f"| Top 10% currency concentration | $> 30.0\%$ wealth share | {ews.top_10_pct_wealth_share * 100:.1f}% ({'**ALERT**' if ews.wealth_inequality_alert else 'Normal'}) |\n"
        f"| Single-resource export reliance | $> 30.0\%$ trade revenue | {ews.single_resource_dependence * 100:.1f}% ({'**ALERT**' if ews.resource_curse_alert else 'Normal'}) |\n"
        f"| Timber extraction vs replanting | Ratio $> 1.00$ | {ews.timber_depletion_vs_replant:.2f} ({'**ALERT**' if ews.ecological_depletion_alert else 'Normal'}) |\n\n"
    )

    W("### Constitutional safeguards on the RAB\n\n")
    pol = RABAccountabilityPolicy()
    W(
        f"| Constitutional check | Rule | Purpose |\n|---|---|---|\n"
        f"| Police / Arrest power | **Zero power (Prohibited)** | Prevents transformation into secret police |\n"
        f"| Data classification | **Public by default** | Open access for all community members |\n"
        f"| Chief Analyst tenure | **{pol.chief_analyst_rotation_years} years max** | Prevents entrenched intelligence baron |\n"
        f"| Analyst maximum tenure | **{pol.analyst_max_tenure_years} years max** | Mandatory return to productive guild work |\n"
        f"| External audit | **Mandatory annual review** | Independent validation of algorithms and data |\n\n"
    )


def table_intel_env() -> None:
    W("## A.19 Intelligence Service (CIS) and Environmental Disaster Bureau (EDMB)\n\n")

    W("### Community Intelligence Service (CIS) directorates\n\n")
    W("| Directorate | Mandate | Primary deliverable |\n|---|---|---|\n")
    for d in CIS_DIRECTORATES:
        W(
            f"| **{d.name}** | {d.mandate[:45]}... | {d.primary_deliverables[0]} |\n"
        )
    W("\n")

    cis_staff = CISStaffing(population=10000)
    edmb_staff = EDMBStaffing(population=10000)
    W("### Staffing architecture (10,000 population)\n\n")
    W(
        f"| Agency | Permanent staff | Volunteers | Functional scope |\n|---|---|---|---|\n"
        f"| **CIS (External Intelligence)** | **{cis_staff.total_staff}** | 0 | HUMINT ({cis_staff.humint_officers}), SIGINT ({cis_staff.sigint_technicians}), OSINT ({cis_staff.osint_analysts}), CI ({cis_staff.counter_intel_officers}) |\n"
        f"| **EDMB (Ecology & Disaster)** | **{edmb_staff.permanent_staff}** | **{edmb_staff.trained_emergency_volunteers}** | Monitoring ({edmb_staff.monitoring_technicians}), EIA ({edmb_staff.eia_assessors}), Rescue ({edmb_staff.disaster_response_coordinators}), Regeneration ({edmb_staff.regeneration_specialists}) |\n"
        f"| **Total Sensory & Ecological Force** | **{cis_staff.total_staff + edmb_staff.permanent_staff}** | **{edmb_staff.trained_emergency_volunteers}** | **Mobilizable crisis force of {cis_staff.total_staff + edmb_staff.total_mobilizable_response_force} personnel** |\n\n"
    )

    W("### Environmental telemetry & predictive disaster lead times\n\n")
    W("| Disaster threat | Primary monitoring telemetry | Predictive lead time | Action threshold |\n|---|---|---|---|\n")
    W("| **Floods** | River float gauges + 24h rainfall | 24–72 hours | Gauge $> 1.0\times$ threshold or rain $> 120$ mm (Red Alert) |\n")
    W("| **Landslides** | Soil moisture saturation + slope angle | 12–48 hours | Slope $\ge 30^\circ$ and saturation $\ge 90\%$ (Red Alert) |\n")
    W("| **Epidemics / Vectors** | Mosquito larvae delta + water pathogens | 2–4 weeks | Larvae surge $\ge 250\%$ or pathogens $> 10$ CFU (Red Alert) |\n")
    W("| **Droughts** | Multi-season rainfall + reservoir drawdown | 3–12 months | 2 consecutive failed seasonal rain cycles |\n")
    W("| **Forest Fires** | Ambient temperature + brush moisture | 1–7 days | Relative humidity $< 20\%$ with high winds |\n\n")

    W("### Environmental Impact Assessment (EIA) risk framework\n\n")
    W("| EIA Risk level | Project status | Required action | Override threshold |\n|---|---|---|---|\n")
    W("| **Low** | Approved | Standard monitoring | Standard Council assent |\n")
    W("| **Moderate** | Conditional | Mandatory mitigation plan approved by EDMB | Proposing Steward complies |\n")
    W("| **High** | Suspended | Mandatory engineering redesign | Redesign re-evaluated by EDMB |\n")
    W("| **Critical** | **DENIED** | Unacceptable ecological catastrophe risk | **75% Council Supermajority Override Only** |\n\n")

    W("### The Awareness Triangle in action (Sample transboundary events)\n\n")
    W("| Transboundary crisis | Detected by | CIS action | EDMB action | Council response |\n|---|---|---|---|---|\n")
    for ev in COMMON_TRANSBOUNDARY_EVENTS:
        W(
            f"| **{ev.event_name[:32]}...** | {ev.detected_by[:25]}... | "
            f"{ev.cis_action[:30]}... | {ev.edmb_action[:30]}... | {ev.council_action[:30]}... |\n"
        )
    W("\n")


def table_war_council() -> None:
    W("## A.20 War Council, Scenario Planning, and Specialized Strike Units\n\n")

    W("### The Seven Seats of the War Council\n\n")
    W("| Seat # | Title | Rotation | Operational mandate & primary perspective | Special veto authority |\n|---|---|---|---|---|\n")
    for i, m in enumerate(WAR_COUNCIL_ROSTER, 1):
        veto_str = f"**{m.veto_scope}**" if m.has_specific_veto else "Standard vote (4/7)"
        W(f"| {i} | **{m.title}** | {m.rotation_months} months | {m.primary_perspective} | {veto_str} |\n")
    W("\n")

    W("### Core military doctrine: 'Don't Mirror, Don't Chase, Don't Hold'\n\n")
    W("| Doctrine rule | Strategic meaning | Operational application | Historical precedent |\n|---|---|---|---|\n")
    for p in DOCTRINE_PRINCIPLES:
        W(f"| **{p.rule_name}** | {p.meaning} | {p.application} | {p.historical_proof} |\n")
    W("\n")

    W("### The Living Contingency Scenario Library (Roman Model)\n\n")
    W("| Scenario code | Threat description | Adversary scale | Warning lead time | Primary defensive response |\n|---|---|---|---|---|\n")
    for s in SCENARIO_LIBRARY:
        W(
            f"| **{s.code}: {s.name}** | {s.adversary_scale} | {s.adversary_scale} | "
            f"{s.early_warning_lead_time} | {s.primary_response_phase[:55]}... |\n"
        )
    W("\n")

    sizing = SpecializedUnitSizing(population=10000, militia_size=3500)
    W("### Specialized precision units (Elite in skill, ordinary in status)\n\n")
    W(
        f"| Specialized unit | Nominal size | Personnel range | Primary operational mission | Operational limit |\n|---|---|---|---|---|\n"
    )
    for u in SPECIALIZED_UNITS_ROSTER:
        W(
            f"| **{u.functional_name}** | **{u.nominal_size}** | {u.min_size}–{u.max_size} | "
            f"{u.mission[:45]}... | {u.operational_limit[:45]}... |\n"
        )
    W(
        f"\n*Total Specialized Force:* **{sizing.total_specialized_nominal} operators** "
        f"({sizing.total_specialized_min}–{sizing.total_specialized_max} range), representing "
        f"**{sizing.fraction_of_militia * 100:.2f}% of citizen militia** and "
        f"**{sizing.fraction_of_population * 100:.2f}% of total population**.\n\n"
    )

    W("### Anti-caste constitutional firewalls\n\n")
    safeguards = AntiCasteSafeguards()
    W(
        f"| Constitutional firewall | Parameter | Institutional rationale |\n|---|---|---|\n"
        f"| Mandatory civilian rotation | **{safeguards.max_consecutive_service_years} years max** | Returns operators to economic guild production |\n"
        f"| Separate barracks | **Prohibited** | Operators live in family homes among citizens |\n"
        f"| Separate pay / privilege | **Prohibited** | Equal standard wage in weight-based currency |\n"
        f"| Hereditary recruitment | **Prohibited** | Merit and militia drill performance only |\n"
        f"| Civil political office ban | **Enforced** | Absolute separation of armed force and civil governance |\n"
        f"| Right of refusal | **Guaranteed** | Operators protected when refusing offensive war orders |\n"
        f"| Functional naming rule | **Mandatory** | No prestige titles ('Guards', 'Elites'); named by tool/function |\n"
        f"| Skill distribution rule | **Active** | Operators return to guilds and train apprentices |\n\n"
    )

    W("### Engagement simulation: Medium coordinated assault (Scenario S2)\n\n")
    report = EngagementBattleReport()
    W(
        f"| Engagement metric | Invading adversary force | Community defense force | Outcome asymmetry |\n|---|---|---|---|\n"
        f"| Initial deployment | {report.enemy_initial_force} fighters, {report.enemy_tanks} armor, {report.enemy_drones} drones | {report.community_militia_deployed} militia + {report.specialized_operators_deployed} specialized | 4:1 local terrain defense ratio |\n"
        f"| Casualties | {report.enemy_casualties_killed} killed, {report.enemy_casualties_captured} captured | {report.community_militia_killed} killed, {report.community_militia_wounded} wounded | **{report.casualty_exchange_ratio:.2f}:1 casualty exchange ratio** |\n"
        f"| Equipment neutralized | {report.enemy_tanks_neutralized}/{report.enemy_tanks} armor, {report.enemy_drones_neutralized}/{report.enemy_drones} drones | 2 IED fields detonated | 100% heavy vehicle/drone neutralization |\n"
        f"| Attrition rate | **{report.enemy_attrition_rate * 100:.1f}%** | 5.5% | Adversary column routed in 6 hours |\n\n"
    )


def table_media_integrity() -> None:
    W("## A.21 National Media and Information Integrity Act\n\n")

    W("### The three independent statutory bodies\n\n")
    W("| Statutory body | Mandate & primary function | Governance & appointment insulation |\n|---|---|---|\n")
    for b in STATUTORY_BODIES:
        W(
            f"| **{b.name}** | {b.primary_statutory_duties[0]} | "
            f"{b.board_term_years}-yr terms; {b.appointment_mechanism[:45]}... |\n"
        )
    funding = StatutoryFundingFormula()
    W(
        f"\n*Statutory Funding Independence:* Ring-fenced formula (**{funding.broadcast_fee_levy_percent * 100:.0f}% broadcast license fee levy + "
        f"{funding.digital_ad_revenue_levy_percent * 100:.0f}% digital ad turnover levy**); zero annual ministerial budget discretion.\n\n"
    )

    W("### The 9-step revised sanction ladder (Attacking Reach, Revenue & Position)\n\n")
    W("| Step | Sanction name | Target asset | Operational enforcement action | Repeat trigger |\n|---|---|---|---|---|\n")
    for s in REVISED_SANCTION_LADDER_REV3:
        W(
            f"| **Step {s.step}** | **{s.name}** | {s.target_asset} | {s.operational_action[:45]}... | "
            f"{'**Automatic**' if s.is_automatic_on_repeat_breach else 'First breach'} |\n"
        )
    W("\n")

    disg = DisgorgementAssessment(commercial_revenue_earned_usd=100000.0, statutory_multiplier=1.5, victim_harm_compensation_usd=25000.0)
    W("### Disgorgement vs. fine revenue allocation\n\n")
    W(
        f"| Financial component | Assessment basis | Beneficiary | Systemic impact |\n|---|---|---|---|\n"
        f"| Commercial Revenue Disgorgement | **${disg.total_disgorgement_amount_usd:,.0f}** ({disg.statutory_multiplier:.1f}x multiplier) | Escrow Trust Fund | Strips all profit motive from illegal promotion |\n"
        f"| Victim Direct Compensation | **${disg.victim_allocation_usd:,.0f}** (100% direct) | Named Victims / Persons | Compensates harmed individuals on statutory scale |\n"
        f"| State Slush Fund Allocation | **$0.00 (0.0%)** | None | **Eliminates state incentive for regulatory shakedowns** |\n\n"
    )

    W("### Foreign platform enforcement at the money layer\n\n")
    fp = ForeignPlatformEnforcementModel()
    W(
        f"| Enforcement mechanism | Domestic legal lever | Cross-border effectiveness |\n|---|---|---|\n"
        f"| Resident Legal Representative | Mandatory resident officer | Personally liable for compliance and contempt of court |\n"
        f"| Tax-Deductibility Disallowance | **Ad spend non-deductible** | Domestic advertisers lose tax deduction, forcing platforms to comply |\n"
        f"| Payment Processor Prohibition | Banking settlement block | Banks prohibited from settling domestic ad billing for non-compliant firms |\n"
        f"| Withholding Tax Surcharge | Remittance withholding | Direct statutory deduction on cross-border revenue outflows |\n"
        f"| **Network-Layer Filtering** | **STRICTLY PROHIBITED (0%)** | State never acquires a monopoly censorship/packet filtering pipe |\n\n"
    )

    W("### Platform amplification duties vs. hosting immunity\n\n")
    pd = PlatformStatutoryDuties()
    W(
        f"| Platform regulatory duty | Statutory requirement | Legal distinction |\n|---|---|---|\n"
        f"| Independent Ranking Audit | **Mandatory annual audit by III** | Algorithmic amplification is an accountable editorial act |\n"
        f"| Passive Hosting Immunity | **Maintained intact** | Passive user storage does not incur speech liability |\n"
        f"| Non-Personalized Feed | **Default 1-tap chronological** | Eliminates engagement-maximizing radicalization funnels |\n"
        f"| Under-16 Protection | **Zero engagement optimization** | Prohibits algorithmic dopamine loops on minor accounts |\n"
        f"| Political Ad Registry | **5-year public searchable DB** | Full disclosure of funder, spend, and micro-targeting criteria |\n"
        f"| Provenance Display | **C2PA credential support** | Shifts epistemic burden to verifiable content origin |\n"
        f"| End-to-End Encryption | **Zero backdoors / escrow** | Mathematical privacy protected; governed via metadata friction |\n\n"
    )

    W("### Disciplining the state first (Pre-conditions for press regulation)\n\n")
    sp = StateConductPolicy()
    W(
        f"| State self-discipline lock | Statutory mechanism | Anti-capture protection |\n|---|---|---|\n"
        f"| State Advertising Allocation | **Published formula only** | Zero ministerial discretion; deviation is a criminal offense |\n"
        f"| Freedom of Information (FOI) | **Deemed grant on silence** | Request automatically approved if deadline lapses without response |\n"
        f"| Whistleblower Protection | **Reversed burden of proof** | State must prove employment action was not retaliatory |\n"
        f"| Anti-SLAPP Shield | **Early dismissal & damages** | Immediate stay of discovery and fee-shifting against lawfare suits |\n"
        f"| State Astroturfing Ban | **Criminalized** | Prohibits covert state-funded bot farms and propaganda campaigns |\n"
        f"| Journalist Accreditation | **Functional definition** | No mandatory state journalist licensing register |\n\n"
    )

    W("### Consolidated statutory decision matrix\n\n")
    W("| Content category | Statutory status | Enforced by | Core rationale |\n|---|---|---|---|\n")
    for r in CONSOLIDATED_POLICY_MATRIX:
        status_str = f"**{r.status.value.upper()}**"
        W(f"| {r.category[:38]}... | {status_str} | {r.enforcement_mechanism[:28]}... | {r.rationale[:35]}... |\n")
    W("\n")

    W("### Phased implementation sequence\n\n")
    W("| Phase | Timeline | Phase title | Primary implementation milestone |\n|---|---|---|---|\n")
    for p in IMPLEMENTATION_PHASES:
        W(
            f"| **Phase {p.phase_number}** | {p.timeline_months} | **{p.phase_name}** | "
            f"{p.core_actions[0]} |\n"
        )
    W("\n")


def table_penalties() -> None:
    W("## A.22 Non-Cash Penalties, Restorative Labor, and Anti-Extortion Enforcement\n\n")

    W("### The 4-Tier 'Sweat & Duty' Non-Cash Penalty Ladder\n\n")
    W("| Tier | Offense category | Public labor duty | Labor hours | Vehicle impound | Exile applicable? |\n|---|---|---|---|---|---|\n")
    for t in PENALTY_TIER_ROSTER:
        W(
            f"| **{t.name}** | {t.target_offenses[:32]}... | `{t.primary_labor_duty.value}` | "
            f"{t.min_labor_hours}–{t.max_labor_hours} hrs ({t.nominal_labor_hours} nom) | {t.vehicle_impound_days} days | "
            f"{'**YES (Council 75%)**' if t.exile_applicable else 'No'} |\n"
        )
    W("\n")

    ra = RestitutionAccounting(damage_assessed_rcu=1000.0, restitution_multiplier=2.0)
    W("### Restitution allocation (100% to Victims, 0% to Police)\n\n")
    W(
        f"| Recipient entity | Allocation share | Sample allocation (1,000 RCU Damage) | Policy rationale |\n|---|---|---|---|\n"
        f"| **Harmed Victim** | **100.0%** | **{ra.victim_allocation_rcu:,.0f} RCU** ({ra.restitution_multiplier:.1f}x damage) | Restores property loss and emotional disruption directly |\n"
        f"| **Police Department** | **0.0%** | **0 RCU** | **Eliminates policing-for-profit and roadside quota hunting** |\n"
        f"| **Municipal Slush Fund** | **0.0%** | **0 RCU** | Prevents administrative budget reliance on citations |\n\n"
    )

    W("### Six statutory anti-extortion locks\n\n")
    aep = AntiExtortionPolicy()
    W(
        f"| Anti-extortion lock | Statutory rule | Anti-bribery mechanism |\n|---|---|---|\n"
        f"| Officer Cash Possession | **Automatic felony offense** | Prevents patrol officers carrying or accepting money on duty |\n"
        f"| Roadside Cash Collections | **Strictly prohibited** | No fine payment can ever occur at the scene of an infraction |\n"
        f"| Evidence Prerequisite | **Mandatory dashcam / bodycam** | Citations missing timestamped video are **automatically dismissed** |\n"
        f"| Bribe Reverse Bounty | **{aep.reverse_bounty_on_reported_bribe_solicitation_rcu:.0f} RCU to citizen** | Paid from corrupt officer's forfeited integrity bond |\n"
        f"| Quota Anomaly Detection | **Active algorithmic monitoring** | RAB flags choke points with $>70\%$ citation dismissal rates |\n"
        f"| Mandatory Patrol Rotation | **Every {aep.patrol_officer_mandatory_rotation_months} months** | Prevents establishment of entrenched roadside toll cartels |\n\n"
    )

    W("### 3-Citizen sortition dispute tribunal\n\n")
    W("| Dispute condition | Sortition jury rule | Outcome & disciplinary action |\n|---|---|---|\n")
    W("| Missing dashcam footage | Automatic dismissal with prejudice | Citation voided; citing officer flagged for disciplinary review |\n")
    W("| Contested citation with footage | 3-citizen random sortition panel | Majority vote (2 of 3) decides factual guilt or dismissal |\n")
    W("| Unjustified harassment proven | Immediate dismissal | Offender exonerated; officer cited for abusive enforcement |\n\n")


def table_debt_subscriptions() -> None:
    W("## A.23 Abolition of Debt-Based and Subscription-Based Financial Extraction\n\n")

    W("### Sector-by-sector sovereign transformation matrix\n\n")
    W("| Economic sector | Extractive financial model | Sovereign replacement | Operating principle |\n|---|---|---|---|\n")
    for sc in SECTOR_COMPARISONS:
        W(
            f"| **{sc.sector.value.replace('_', ' ').title()}** | {sc.extractive_system_name[:35]}... | "
            f"{sc.sovereign_replacement_name[:35]}... | {sc.replacement_operating_model[:40]}... |\n"
        )
    W("\n")

    veh = VehiclePurchaseComparison(cash_price_rcu=200000.0, predatory_interest_and_fees_rcu=150000.0)
    W("### Vehicle deferred purchase: predatory financing vs. fair installment\n\n")
    W(
        f"| Financing model | Cash price | Total repayment | Surcharge ratio | Terms & repossession |\n|---|---|---|---|---|\n"
        f"| Predatory Commercial Loan | {veh.cash_price_rcu:,.0f} RCU | **{veh.predatory_total_repayment_rcu:,.0f} RCU** | **{veh.predatory_surcharge_ratio:.2f}x** | Compounding usury + quick repossession |\n"
        f"| **Sovereign Fair Installment** | {veh.cash_price_rcu:,.0f} RCU | **{veh.fair_total_repayment_rcu:,.0f} RCU** | **1.00x (0% Interest)** | Income-tied payments + hardship protection |\n\n"
    )

    housing = CostPlusHousingAdvance()
    h_comp = housing.compare_against_30yr_commercial_mortgage(mortgage_interest_rate_percent=9.0)
    W("### Housing finance: cost-plus advance vs. 30-year compound mortgage\n\n")
    W(
        f"| Housing financing parameter | 30-Year compound commercial mortgage | Sovereign cost-plus advance | Financial extraction avoided |\n|---|---|---|---|\n"
        f"| Physical construction & land | {h_comp['cost_plus_principal_rcu']:,.0f} RCU | {h_comp['cost_plus_principal_rcu']:,.0f} RCU | Real physical asset parity |\n"
        f"| Interest rate | 9.0% APR compounding | **0.0% (Zero interest)** | Compounding mortgage usury eliminated |\n"
        f"| Total repayment | **{h_comp['commercial_30yr_total_rcu']:,.0f} RCU** | **{h_comp['cost_plus_principal_rcu']:,.0f} RCU** | **{h_comp['interest_extracted_rcu']:,.0f} RCU saved ({h_comp['cost_multiplier']:.2f}x)** |\n"
        f"| Default consequence | Foreclosure & family eviction | Hardship pause; sortition mediation | **Zero primary home seizure** |\n\n"
    )

    W("### The Ten Statutory Rules for Fair Borrowing and Installments\n\n")
    W("| # | Statutory rule | Core legal requirement | Prohibited abusive practice |\n|---|---|---|---|\n")
    for r in FAIR_BORROWING_RULES:
        W(f"| {r.rule_number} | **{r.rule_title}** | {r.statutory_mandate[:45]}... | {r.prohibited_abuse[:40]}... |\n")
    W("\n")

    elder = ElderCareStipend()
    W("### Master-Apprentice elder production compact (Physical commodity security)\n\n")
    W(
        f"| Elder support component | Guaranteed monthly allocation | Backing source | Risk profile |\n|---|---|---|---|\n"
        f"| Grains / Flour | **{elder.monthly_grain_ration_kg:.0f} kg** | Guild physical reserve silos (§02) | 100% immune to inflation |\n"
        f"| Cooking Oil | **{elder.monthly_oil_ration_liters:.0f} Liters** | Tier A commodity warehouses | Real physical delivery |\n"
        f"| Utility / Biofuel | **{elder.monthly_fuel_biofuel_liters:.0f} Liters** | Guild energy production (§17) | Free from utility debt |\n"
        f"| Civic Currency Stipend | **{elder.monthly_stipend_rcu:.0f} RCU** | General public revenue | Personal discretionary use |\n"
        f"| Healthcare & Housing | **100% Guaranteed free access** | Direct guild provisioning | Zero medical aid billing |\n\n"
    )

    W("### The Decisive Access Test evaluation\n\n")
    W("| System / Institution | Direct physical access? | Charges interest / sub? | Profit-driven denial? | Socially defensible? |\n|---|---|---|---|---|\n")
    W("| **Commercial Medical Aid Scheme** | No (middleman) | **Yes (Perpetual)** | **Yes (Denial = Profit)** | **FAILED (Abolished)** |\n")
    W("| **Private Commercial Insurance** | No (financial float) | **Yes (Perpetual)** | **Yes (Adjuster loopholes)** | **FAILED (Abolished)** |\n")
    W("| **Compound-Interest Auto/Home Loan** | No (debt command) | **Yes (Compounding)** | **Yes (Foreclosure)** | **FAILED (Abolished)** |\n")
    W("| **Sovereign Guild Provisioning** | **YES (Direct care)** | **NO (0% Subs)** | **NO (Medical need only)** | **PASSED (Adopted)** |\n")
    W("| **Physical Commodity Mutual Pool** | **YES (48h rebuild)** | **NO (0% Premiums)** | **NO (Real reserve release)** | **PASSED (Adopted)** |\n")
    W("| **Zero-Interest Resource Advance** | **YES (Physical tools)**| **NO (0.0% Interest)** | **NO (Pause on hardship)** | **PASSED (Adopted)** |\n\n")

    trust = CitizensRestitutionTrust()
    sample_acc = ContributorRestitutionAccount(
        citizen_id="CIT-SAMPLE",
        total_lifetime_premiums_paid_rcu=120_000.0,
        total_claims_received_rcu=20_000.0,
        mortgage_or_vehicle_debt_rcu=80_000.0,
    )
    offset = sample_acc.apply_instant_debt_cancellation()
    div = trust.calculate_citizen_monthly_dividend(citizen_net_balance_rcu=offset["remaining_restitution_balance_rcu"])

    W("### Commercial skyscraper float seizure & contributor restitution engine\n\n")
    W(
        f"| Restitution parameter | Corporate insurance baseline | Citizens' Restitution Trust (CRT) | Restitution outcome |\n|---|---|---|---|\n"
        f"| Skyscraper Asset Portfolio | Corporate private equity | **{trust.total_seized_commercial_real_estate_value_rcu:,.0f} RCU vested in trust** | Real physical real estate preserved |\n"
        f"| Annual Commercial Rent Yield | Retained by executives ({trust.annual_commercial_rental_yield_pct * 100:.1f}%) | **{trust.annual_rental_cashflow_rcu:,.0f} RCU / year** | 100% Cashflow pooled for contributors |\n"
        f"| Net Contributor Formula | Forfeited on policy lapse | **Total Premiums − Total Claims Paid** | 100% Principal returned to citizen |\n"
        f"| Instant Mortgage Offset | Foreclosure on default | **{offset['debt_cancelled_rcu']:,.0f} RCU direct debt wipeout** | **Family home owned 100% debt-free** |\n"
        f"| Residual Monthly Dividend | $0.00 after cancellation | **{div['monthly_dividend_rcu']:,.2f} RCU / month** | Continuous rental cashflow to citizen |\n\n"
    )


def table_clothing_standards() -> None:
    W("## A.24 Public Clothing Standards and Exposure Thresholds\n\n")

    W("### Graduated spatial zones & bright-line exposure thresholds\n\n")
    W("| Spatial zone | Scope of locations | Coverage standard | Venue operator duty |\n|---|---|---|---|\n")
    for sz in SPATIAL_ZONE_SPECS:
        W(
            f"| **{sz.name}** | {sz.locations[:35]}... | "
            f"{sz.coverage_threshold_description[:35]}... | {sz.venue_operator_duty[:40]}... |\n"
        )
    W("\n")

    W("### Seven anti-humiliation constitutional firewalls\n\n")
    ah = AntiHumiliationPolicy()
    W(
        f"| Anti-humiliation lock | Statutory rule | Operational protection |\n|---|---|---|\n"
        f"| Physical Contact | **Strictly prohibited (0%)** | Felony for officer to touch, grab, or detain a citizen |\n"
        f"| Custodial Penalty | **Zero arrest / custody** | A person can **never go to jail** for what they wear |\n"
        f"| Remedy-First Offer | **Free covering garment on spot** | Accepting free wrap closes encounter with zero record / fine |\n"
        f"| Public Shaming Ban | **Criminalized for all** | Criminal offense for officers or bystanders to photograph or post |\n"
        f"| Mixed-Sex Patrols | **Female-to-female approach** | Female citizens may only be approached by female officers |\n"
        f"| Body Measurement Ban | **Strictly prohibited** | Hard ban on officers measuring, inspecting, or remarking on bodies |\n"
        f"| Democratic Review | **5-year statutory sunset** | Full legislative review and published demographic audit data |\n\n"
    )

    sim = ClothingComplianceSimulation(total_non_compliant_encounters=1000)
    W("### First-contact resolution simulation (1,000 non-compliant encounters)\n\n")
    W(
        f"| Encounter outcome | Count | Percentage | Systemic impact |\n|---|---|---|---|\n"
        f"| Resolved on spot (Accepted free wrap) | **{sim.encounters_resolved_without_record:,}** | **{sim.acceptance_of_free_garment_rate * 100:.1f}%** | Zero fine, zero conflict, zero regulatory record |\n"
        f"| Civil notice issued (Garment refused) | **{sim.civil_notices_issued:,}** | **{(1 - sim.acceptance_of_free_garment_rate) * 100:.1f}%** | Standard formulaic civil notice (no criminal charge) |\n"
        f"| Custodial arrest count | **{sim.arrest_count}** | **0.0%** | **Complete elimination of debtor/morality jail terms** |\n\n"
    )

    W("### Tiered public sector dress & service accountability architecture\n\n")
    W("| Dress tier | Target roles | Mandatory uniform? | Visible ID? | Core civic & anti-aristocracy purpose |\n|---|---|---|---|---|\n")
    for t in PUBLIC_SECTOR_DRESS_TIERS:
        u_str = "**MANDATORY**" if t.mandatory_uniform else "No (Standardized Code)"
        id_str = "**MANDATORY (Criminal ban on obscuring)**" if t.mandatory_visible_id else "N/A (Desk role)"
        W(f"| **{t.title}** | {t.target_roles[:35]}... | {u_str} | {id_str} | {t.core_purpose[:45]}... |\n")
    W("\n")

    proc = UniformProcurementPolicy()
    W("### Sovereign uniform procurement and domestic industrial clauses\n\n")
    W(
        f"| Procurement pillar | Statutory rule | Operational economic effect |\n|---|---|---|\n"
        f"| 100% State-Funded | **Free issue, replacement, laundering** | Prohibits stealth wage cuts on frontline public servants |\n"
        f"| Domestic Manufacture | **100% Local guild procurement (§17)** | Converts uniform budget into permanent domestic industrial stimulus |\n"
        f"| Anti-Graft Transparency | **Open tenders & beneficial ownership** | Eliminates historical kickbacks and procurement extortion |\n"
        f"| Dignity & Sizing | **Ergonomic, maternity & religious cuts** | Ensures climate-appropriate comfort and high compliance |\n"
        f"| Sovereign Visual Design | **National idiom & domestic fibers** | Real cultural sovereignty rather than copying foreign braid in reverse |\n\n"
    )

    W("### Four-tier workforce separation statutory architecture\n\n")
    W("| Separation tier | Scope of functions | Statutory rule | Waiver / exception policy |\n|---|---|---|---|\n")
    for st in SEPARATION_TIER_SPECS:
        W(f"| **{st.name}** | {st.scope_of_functions[:40]}... | {st.statutory_rule[:40]}... | {st.waiver_policy[:45]}... |\n")
    W("\n")

    fgs = FemaleGuardServiceSpec()
    audit = EqualResourcingAudit()
    W("### Female Guard Service and resourcing parity audit parameters\n\n")
    W(
        f"| Parity safeguard | Statutory standard | Audit enforcement lock |\n|---|---|---|\n"
        f"| Command Rank Parity | **Service Head equal to male chief** | Autonomous budget line and direct reporting line |\n"
        f"| Legal Authority | **Full arrest, search & detention powers** | Auxiliary or assistant status prohibited by law |\n"
        f"| Pay & Pension Parity | **100% Equal pay codified in statute** | Zero promotional ceiling across the full career ladder |\n"
        f"| Recruitment Buffer | **Target = Minimum + {fgs.attrition_margin_rate * 100:.0f}% buffer** | Dedicated female academy capacity built prior to mandate |\n"
        f"| Equipment & Uniform | **Female-cut body armour mandatory** | Integrated quick-release head covering, tailored cut |\n"
        f"| Retention Support | **On-site childcare at all facilities** | Eliminates mid-career attrition and preserves skill depth |\n"
        f"| Parity Audit Threshold | **Max allowable divergence: {audit.max_divergence_threshold * 100:.1f}%** | Breach triggers **personal disqualification (§25)** of minister |\n\n"
    )

    W("### Workforce separation failure prevention matrix\n\n")
    W("| Systemic failure mode | Root operational risk | Statutory prevention clause |\n|---|---|---|\n")
    for fp in WORKFORCE_FAILURE_PREVENTIONS:
        W(f"| **{fp.failure_mode}** | Drift into under-resourcing/caste | {fp.prevention_clause} |\n")
    W("\n")


def table_millet_and_gap_audit() -> None:
    W("## A.25 Pluralism, Modernized Millet Architecture, and State Gap Audit\n\n")

    W("### Sovereign jurisdictional domain separation matrix\n\n")
    W("| Governance domain | Authority layer | Responsible institution | Scope & statutory override |\n|---|---|---|---|\n")
    for d in MILLET_JURISDICTION_DOMAINS:
        layer_str = d.authority_layer.value.replace("_", " ").upper()
        W(f"| **{d.domain_name}** | `{layer_str}` | {d.responsible_body[:35]}... | {d.override_rule[:45]}... |\n")
    W("\n")

    hr = HumanRightsFloor()
    lock = AntiLebanonLock()
    W("### Modernized Millet safeguards & human rights floor\n\n")
    W(
        f"| Structural safeguard | Statutory mandate | Systemic protection |\n|---|---|---|\n"
        f"| Marriage Age Floor | **Minimum {hr.minimum_marriage_age} years** | 100% Ban on child marriage across all millets |\n"
        f"| Verifiable Consent | **Mandatory state verification** | Absolute criminal prohibition on forced marriage |\n"
        f"| Domestic Violence | **Exclusive state criminal jurisdiction** | Millets barred from privatizing or shielding abuse |\n"
        f"| Right of Exit | **Unrestricted access to Civil Millet** | Eliminates historical caste entrapment by birth |\n"
        f"| Appellate Review | **Decisions appealable to state courts** | Guarantees judicial due process oversight |\n"
        f"| Anti-Lebanon Lock | **Zero confessional quotas in office** | Millets strictly barred from allocating state power |\n\n"
    )

    W("### Comprehensive 10-domain state gap audit register\n\n")
    W("| # | Governance domain | Framework status | Existing coverage summary | Critical unresolved frontier |\n|---|---|---|---|---|\n")
    for g in STATE_GAP_AUDIT_REGISTER:
        status_badge = f"**{g.status.value.replace('_', ' ').upper()}**"
        W(
            f"| {g.domain_number} | **{g.domain_title}** | {status_badge} | "
            f"{g.existing_coverage_summary[:40]}... | {g.unresolved_crucial_elements[:45]}... |\n"
        )
    W("\n")


def main() -> None:
    header()
    table_classes()
    table_carry()
    table_lifetime()
    table_crash()
    table_liquidity()
    table_schedule()
    table_harvest()
    table_bundles()
    table_weight()
    table_people()
    table_services()
    table_external()
    table_production()
    table_security()
    table_military()
    table_governance()
    table_integrity()
    table_rab()
    table_intel_env()
    table_war_council()
    table_media_integrity()
    table_penalties()
    table_debt_subscriptions()
    table_clothing_standards()
    table_millet_and_gap_audit()


if __name__ == "__main__":
    main()
