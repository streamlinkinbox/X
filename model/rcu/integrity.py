"""Anti-Corruption, Incompetence Diagnostics, and Resource Curse Prevention.

This module models structural integrity controls for an independent community:
1. ``difficulty_adjustment`` -- evaluating leadership under environmental stress
   (baseline benchmarking vs absolute perfection).
2. ``shadow_probation`` -- 90-day Deputy transition and quantitative target
   verification.
3. ``phantom_employment`` -- production-based employment auditing and zero-value
   job elimination.
4. ``resource_curse`` -- economic concentration metrics (Herfindahl-Hirschman
   Index) comparing single-commodity economies against diversified RCU baskets.
5. ``anti_monopoly`` -- market concentration thresholds and 20% single-entity caps.
6. ``wealth_ceiling`` -- personal currency accumulation limits (5x average).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import ROUND_HALF_UP, Decimal
from enum import Enum


def _q(x: Decimal, places: str = "0.01") -> Decimal:
    return x.quantize(Decimal(places), rounding=ROUND_HALF_UP)


# --------------------------------------------------------------------------
# 1. Incompetence vs. Difficulty Diagnostics
# --------------------------------------------------------------------------


class EnvironmentalStress(str, Enum):
    MILD = "mild"            # Normal weather, stable trade, peace
    MODERATE = "moderate"    # Minor drought, supply chain friction
    SEVERE = "severe"        # Multi-year drought, epidemic, external blockade


class ObservedOutcome(str, Enum):
    EXCELLENT = "excellent"
    ACCEPTABLE = "acceptable"
    POOR = "poor"
    CATASTROPHIC = "catastrophic"


class EvaluationVerdict(str, Enum):
    COMPETENT_UNTESTED = "competent_untested"
    EXCEPTIONAL_RETAIN = "exceptional_retain"
    INCOMPETENT_REMOVE = "incompetent_remove"
    PEER_REVIEW_REQUIRED = "peer_review_required"


@dataclass(frozen=True)
class LeadershipDiagnostic:
    stress_level: EnvironmentalStress
    outcome: ObservedOutcome
    correct_diagnosis: bool
    efficient_resource_use: bool
    adapted_to_shocks: bool
    honest_communication: bool
    consulted_domain_experts: bool
    personal_wealth_divergence: bool       # True if leader prospered while community suffered
    community_loss_pct: float
    peer_community_loss_pct: float         # Neighboring community under identical conditions

    @property
    def comparative_performance_delta(self) -> float:
        """Negative means we did worse than neighbors; positive means we did better."""
        return round(self.peer_community_loss_pct - self.community_loss_pct, 2)

    @property
    def verdict(self) -> EvaluationVerdict:
        # Immediate removal conditions
        if self.personal_wealth_divergence:
            return EvaluationVerdict.INCOMPETENT_REMOVE
        if not self.honest_communication and self.outcome in {ObservedOutcome.POOR, ObservedOutcome.CATASTROPHIC}:
            return EvaluationVerdict.INCOMPETENT_REMOVE

        if self.stress_level == EnvironmentalStress.MILD:
            if self.outcome in {ObservedOutcome.EXCELLENT, ObservedOutcome.ACCEPTABLE}:
                return EvaluationVerdict.COMPETENT_UNTESTED
            return EvaluationVerdict.INCOMPETENT_REMOVE

        if self.stress_level in {EnvironmentalStress.MODERATE, EnvironmentalStress.SEVERE}:
            if self.outcome in {ObservedOutcome.EXCELLENT, ObservedOutcome.ACCEPTABLE}:
                return EvaluationVerdict.EXCEPTIONAL_RETAIN
            # Under severe stress with poor outcome: check comparative benchmark and discipline
            if self.comparative_performance_delta < -15.0: # 15% worse than neighbors
                return EvaluationVerdict.INCOMPETENT_REMOVE
            if self.efficient_resource_use and self.adapted_to_shocks and self.correct_diagnosis:
                return EvaluationVerdict.PEER_REVIEW_REQUIRED
            return EvaluationVerdict.INCOMPETENT_REMOVE

        return EvaluationVerdict.PEER_REVIEW_REQUIRED


# --------------------------------------------------------------------------
# 2. Shadow Leader System & 90-Day Probation
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class ProbationTarget:
    metric_name: str
    baseline_value: float
    target_value: float
    actual_value: float
    higher_is_better: bool = True

    @property
    def target_achieved(self) -> bool:
        if self.higher_is_better:
            return self.actual_value >= self.target_value
        return self.actual_value <= self.target_value

    @property
    def completion_fraction(self) -> float:
        total_delta = self.target_value - self.baseline_value
        if total_delta == 0:
            return 1.0 if self.target_achieved else 0.0
        achieved_delta = self.actual_value - self.baseline_value
        return max(0.0, min(1.0, achieved_delta / total_delta))


@dataclass(frozen=True)
class ShadowLeaderProbation:
    deputy_id: str
    domain: str
    probation_days: int = 90
    targets: tuple[ProbationTarget, ...] = field(default_factory=tuple)

    @property
    def targets_passed_count(self) -> int:
        return sum(1 for t in self.targets if t.target_achieved)

    @property
    def pass_rate(self) -> Decimal:
        if not self.targets:
            return Decimal(0)
        return _q(Decimal(self.targets_passed_count) / Decimal(len(self.targets)), "0.01")

    @property
    def confirmed(self) -> bool:
        """Must meet at least 80% of specific quantitative targets to be confirmed."""
        return self.pass_rate >= Decimal("0.80")


# --------------------------------------------------------------------------
# 3. Phantom Employment & Production-Based Payroll
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class PositionAudit:
    job_title: str
    department: str
    monthly_compensation_rcu: float
    measured_monthly_output_value_rcu: float
    has_tangible_deliverable: bool

    @property
    def is_phantom_job(self) -> bool:
        """A phantom job produces no measurable physical, administrative, or care value."""
        if not self.has_tangible_deliverable:
            return True
        if self.measured_monthly_output_value_rcu <= 0.0:
            return True
        return False

    @property
    def output_to_cost_ratio(self) -> Decimal:
        if self.monthly_compensation_rcu <= 0:
            return Decimal("999.99")
        return _q(
            Decimal(str(self.measured_monthly_output_value_rcu))
            / Decimal(str(self.monthly_compensation_rcu)),
            "0.01",
        )


# --------------------------------------------------------------------------
# 4. Resource Curse & Dutch Disease Concentration Metric
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class RevenueDiversification:
    """Computes Herfindahl-Hirschman Index (HHI) for commodity and revenue sources.

    HHI < 1,500 = Diversified / Resilient
    HHI 1,500 - 2,500 = Moderately Concentrated
    HHI > 2,500 = Highly Concentrated / Severe Resource Curse Vulnerability
    """
    revenue_shares: dict[str, float]  # Name -> share (0.0 to 1.0)

    @property
    def hhi_score(self) -> int:
        total = sum(self.revenue_shares.values())
        if total == 0:
            return 10000
        # Normalize and calculate sum of squared percentage points
        return int(sum(((val / total) * 100.0) ** 2 for val in self.revenue_shares.values()))

    @property
    def is_resource_cursed(self) -> bool:
        return self.hhi_score > 2500

    @property
    def primary_commodity_share(self) -> float:
        if not self.revenue_shares:
            return 0.0
        return max(self.revenue_shares.values()) / max(sum(self.revenue_shares.values()), 0.001)


# --------------------------------------------------------------------------
# 5. Anti-Monopoly Rules & Market Caps
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class MarketParticipant:
    entity_id: str
    family_group_id: str
    market_share_fraction: float


@dataclass(frozen=True)
class MarketConcentrationPolicy:
    market_name: str
    participants: tuple[MarketParticipant, ...]
    max_allowed_share_fraction: float = 0.20  # 20% legal maximum

    @property
    def violating_entities(self) -> list[MarketParticipant]:
        return [p for p in self.participants if p.market_share_fraction > self.max_allowed_share_fraction]

    @property
    def monopoly_breach(self) -> bool:
        return len(self.violating_entities) > 0


# --------------------------------------------------------------------------
# 6. Personal Wealth Accumulation Ceiling
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class PersonalWealthAudit:
    coordinator_id: str
    personal_holdings_rcu: float
    community_average_holdings_rcu: float
    max_allowed_multiplier: float = 5.0

    @property
    def wealth_ratio(self) -> Decimal:
        if self.community_average_holdings_rcu <= 0:
            return Decimal("0.00")
        return _q(
            Decimal(str(self.personal_holdings_rcu))
            / Decimal(str(self.community_average_holdings_rcu)),
            "0.01",
        )

    @property
    def ceiling_exceeded(self) -> bool:
        return self.wealth_ratio > Decimal(str(self.max_allowed_multiplier))
