"""Abolishing Debt-Based and Subscription-Based Systems: Real Production and Shared Provision.

This module formalizes the economic model replacing debt-based and subscription-based
financial extraction with direct public provisioning, zero-interest resource advances,
physical risk pooling, and intergenerational elder care:
1. ``ExtractionModelType`` -- Categorizes extractive financial mechanisms vs sovereign replacements.
2. ``ZeroInterestAdvance`` -- Models zero-interest financing for vehicles, housing, and tools
   (Interest = 0%, No compound clock, No primary home seizure, Flexible pause on hardship).
3. ``VehicleFinancingComparison`` -- Contrasts predatory auto loans against fair installment contracts.
4. ``CostPlusHousingInstallment`` -- Models transparent cost-plus housing advances with eviction protection.
5. ``FairBorrowingRules`` -- The 10 statutory rules for fair borrowing and installment purchasing.
6. ``ElderCareCompact`` -- Models physical commodity allocation for retirees backed by guild production.
7. ``DecisiveAccessTest`` -- Evaluates whether a financial mechanism provides real access or extracts rent.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# --------------------------------------------------------------------------
# 1. Extractive Models vs. Sovereign Replacements
# --------------------------------------------------------------------------


class FinancialSector(str, Enum):
    HEALTHCARE = "healthcare"
    RISK_AND_DISASTER = "risk_and_disaster"
    ELDER_SECURITY = "elder_security"
    LEGAL_PROTECTION = "legal_protection"
    EQUIPMENT_AND_HOUSING = "equipment_and_housing"
    INFRASTRUCTURE_FINANCE = "infrastructure_finance"


@dataclass(frozen=True)
class MechanismComparison:
    sector: FinancialSector
    extractive_system_name: str
    primary_extraction_mode: str
    sovereign_replacement_name: str
    replacement_operating_model: str
    abolition_status: str = "ABOLISHED_AND_REPLACED"


SECTOR_COMPARISONS: tuple[MechanismComparison, ...] = (
    MechanismComparison(
        sector=FinancialSector.HEALTHCARE,
        extractive_system_name="Commercial Medical Aid / Private Health Insurance",
        primary_extraction_mode="Monthly debit subscriptions + claim denial bureaucracy + 500% inflated drug prices",
        sovereign_replacement_name="Direct Public Provisioning & Guild Clinics (§14, §15)",
        replacement_operating_model="100% covered care at point of need; 90-day physical API and medicine buffers",
    ),
    MechanismComparison(
        sector=FinancialSector.RISK_AND_DISASTER,
        extractive_system_name="Commercial Property / Crop / Disaster Insurance",
        primary_extraction_mode="Monthly premiums invested in financial speculation + adjusters seeking claim loopholes",
        sovereign_replacement_name="Physical Commodity Mutual Risk Pools (§02, §23)",
        replacement_operating_model="Direct mobilization of carpentry/masonry guilds and seed/grain reserves within 48 hours",
    ),
    MechanismComparison(
        sector=FinancialSector.ELDER_SECURITY,
        extractive_system_name="Compulsory Private Pension Funds / Asset Managers",
        primary_extraction_mode="2–3% compounding annual management fees + market crash & inflation risk dumped on retiree",
        sovereign_replacement_name="Master-Apprentice Intergenerational Production Stipend",
        replacement_operating_model="Guaranteed monthly physical commodity allocation (grains, oils, housing, health) from active guild output",
    ),
    MechanismComparison(
        sector=FinancialSector.LEGAL_PROTECTION,
        extractive_system_name="Commercial Legal-Aid Retainers / Hourly Billing",
        primary_extraction_mode="Monthly subscription fees with fine print excluding criminal/property disputes",
        sovereign_replacement_name="Universal Sortition Advocates & Community Mediation (§06, §20, §26)",
        replacement_operating_model="Free assigned mediators and 3-citizen random sortition juries; zero hourly billing",
    ),
    MechanismComparison(
        sector=FinancialSector.EQUIPMENT_AND_HOUSING,
        extractive_system_name="Compound-Interest Auto Loans & 30-Year Mortgages",
        primary_extraction_mode="Compound interest doubling purchase price + immediate foreclosure/repossession on default",
        sovereign_replacement_name="Zero-Interest Non-Compounding Resource Advances",
        replacement_operating_model="Repay exact principal borrowed; zero interest; flexible pause on hardship; zero home seizure",
    ),
    MechanismComparison(
        sector=FinancialSector.INFRASTRUCTURE_FINANCE,
        extractive_system_name="Sovereign Bond Markets & Structural Debt Programs",
        primary_extraction_mode="Future tax revenues pledged to external bondholders + austerity conditions",
        sovereign_replacement_name="Commodity-Backed Public Development Budgets (§01, §17)",
        replacement_operating_model="Direct issuance against verified materials, labor, and productive capacity without external debt",
    ),
)


# --------------------------------------------------------------------------
# 2. Zero-Interest Non-Compounding Advance Model
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class ZeroInterestAdvance:
    item_description: str
    principal_amount_rcu: float
    monthly_installment_rcu: float
    interest_rate_percent: float = 0.0          # Strictly zero interest
    compound_interest_allowed: bool = False
    seizure_of_primary_residence_allowed: bool = False
    pause_on_documented_hardship: bool = True

    @property
    def total_repayment_amount_rcu(self) -> float:
        # Repay exactly what was advanced; zero extra financial extraction
        return self.principal_amount_rcu

    @property
    def standard_payoff_months(self) -> int:
        if self.monthly_installment_rcu <= 0:
            return 0
        return int(self.principal_amount_rcu / self.monthly_installment_rcu)

    def calculate_commercial_loan_comparison(
        self, commercial_interest_rate_percent: float, loan_years: int
    ) -> dict[str, float]:
        r = (commercial_interest_rate_percent / 100.0) / 12.0
        n = loan_years * 12
        if r > 0 and n > 0:
            monthly_commercial = (self.principal_amount_rcu * r * (1 + r)**n) / ((1 + r)**n - 1)
            total_commercial_repayment = monthly_commercial * n
            interest_saved = total_commercial_repayment - self.principal_amount_rcu
        else:
            total_commercial_repayment = self.principal_amount_rcu
            interest_saved = 0.0

        return {
            "principal_rcu": self.principal_amount_rcu,
            "zero_interest_total_rcu": self.total_repayment_amount_rcu,
            "commercial_loan_total_rcu": round(total_commercial_repayment, 2),
            "interest_extraction_eliminated_rcu": round(interest_saved, 2),
            "savings_multiplier": round(total_commercial_repayment / max(self.principal_amount_rcu, 1.0), 2),
        }


# --------------------------------------------------------------------------
# 3. Vehicle & Housing Installment Financing Models
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class VehiclePurchaseComparison:
    cash_price_rcu: float = 200_000.0
    predatory_interest_and_fees_rcu: float = 150_000.0
    fair_transparent_admin_fee_rcu: float = 0.0

    @property
    def predatory_total_repayment_rcu(self) -> float:
        return self.cash_price_rcu + self.predatory_interest_and_fees_rcu

    @property
    def fair_total_repayment_rcu(self) -> float:
        return self.cash_price_rcu + self.fair_transparent_admin_fee_rcu

    @property
    def predatory_surcharge_ratio(self) -> float:
        return self.predatory_total_repayment_rcu / max(self.fair_total_repayment_rcu, 1.0)


@dataclass(frozen=True)
class CostPlusHousingAdvance:
    land_preparation_cost_rcu: float = 20_000.0
    materials_and_timber_cost_rcu: float = 60_000.0
    guild_construction_labor_rcu: float = 40_000.0
    infrastructure_connection_rcu: float = 10_000.0
    transparent_admin_fee_rcu: float = 2_000.0
    compound_interest_rate_percent: float = 0.0

    @property
    def total_cost_plus_price_rcu(self) -> float:
        return (
            self.land_preparation_cost_rcu
            + self.materials_and_timber_cost_rcu
            + self.guild_construction_labor_rcu
            + self.infrastructure_connection_rcu
            + self.transparent_admin_fee_rcu
        )

    def compare_against_30yr_commercial_mortgage(
        self, mortgage_interest_rate_percent: float = 9.0
    ) -> dict[str, float]:
        principal = self.total_cost_plus_price_rcu
        r = (mortgage_interest_rate_percent / 100.0) / 12.0
        n = 30 * 12
        monthly = (principal * r * (1 + r)**n) / ((1 + r)**n - 1)
        total_commercial = monthly * n
        return {
            "cost_plus_principal_rcu": principal,
            "commercial_30yr_total_rcu": round(total_commercial, 2),
            "interest_extracted_rcu": round(total_commercial - principal, 2),
            "cost_multiplier": round(total_commercial / max(principal, 1.0), 2),
        }


# --------------------------------------------------------------------------
# 4. The Ten Rules for Fair Borrowing and Installment Purchasing
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class FairBorrowingRule:
    rule_number: int
    rule_title: str
    statutory_mandate: str
    prohibited_abuse: str


FAIR_BORROWING_RULES: tuple[FairBorrowingRule, ...] = (
    FairBorrowingRule(
        rule_number=1,
        rule_title="One Clear Total Price",
        statutory_mandate="The buyer must know the exact maximum total amount they will repay from day one.",
        prohibited_abuse="Hidden variable interest escalations and surprise balloon payments.",
    ),
    FairBorrowingRule(
        rule_number=2,
        rule_title="No Compound Interest",
        statutory_mandate="Unpaid balances cannot generate interest upon interest or grow with the passage of time.",
        prohibited_abuse="Compounding usury multiplying debt independently of production.",
    ),
    FairBorrowingRule(
        rule_number=3,
        rule_title="No Hidden Conditions",
        statutory_mandate="Every material clause must be drafted in plain language with zero fine-print exclusions.",
        prohibited_abuse="Incomprehensible legal boilerplate engineered to trap vulnerable borrowers.",
    ),
    FairBorrowingRule(
        rule_number=4,
        rule_title="No Forced Add-Ons",
        statutory_mandate="Buyers cannot be compelled to purchase bundled tracking, warranties, or memberships.",
        prohibited_abuse="Predatory fee-stuffing inflating the finance contract.",
    ),
    FairBorrowingRule(
        rule_number=5,
        rule_title="Fair Hardship Protection",
        statutory_mandate="Job loss, illness, crop failure, or disaster automatically pauses installments.",
        prohibited_abuse="Punitive penalty fees and immediate default declarations during crises.",
    ),
    FairBorrowingRule(
        rule_number=6,
        rule_title="No Essential-Asset Seizure",
        statutory_mandate="Primary family housing, basic transport, and guild tools are protected from foreclosure.",
        prohibited_abuse="Throwing families onto the street for temporary financial distress.",
    ),
    FairBorrowingRule(
        rule_number=7,
        rule_title="No Perpetual Repayment",
        statutory_mandate="Every advance must have a fixed terminal payoff date or clear settlement cap.",
        prohibited_abuse="Evergreen loans and revolving debt traps that never end.",
    ),
    FairBorrowingRule(
        rule_number=8,
        rule_title="Fresh Start After Honest Failure",
        statutory_mandate="Insolvency procedures allow honest failure to be discharged without lifelong ruin.",
        prohibited_abuse="Lifelong debt bondage and post-repossession phantom debt claims.",
    ),
    FairBorrowingRule(
        rule_number=9,
        rule_title="Equal Bargaining Power",
        statutory_mandate="All standard deferred contracts are publicly registered and sortition-audited (§20).",
        prohibited_abuse="Unilateral adhesion contracts imposed by monopoly creditors.",
    ),
    FairBorrowingRule(
        rule_number=10,
        rule_title="Absolute Ban on Debt Slavery",
        statutory_mandate="A person's physical labor, bodily autonomy, family, or movement cannot be pledged.",
        prohibited_abuse="Indentured servitude, inherited debt, and coercive debt commands.",
    ),
)


# --------------------------------------------------------------------------
# 5. Elder Care Production Compact (Intergenerational Security)
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class ElderCareStipend:
    monthly_grain_ration_kg: float = 25.0
    monthly_oil_ration_liters: float = 4.0
    monthly_fuel_biofuel_liters: float = 10.0
    monthly_stipend_rcu: float = 150.0
    guaranteed_free_healthcare: bool = True
    guaranteed_shelter: bool = True
    funded_by_speculative_markets: bool = False
    funded_by_active_guild_production: bool = True

    @property
    def is_inflation_and_crash_proof(self) -> bool:
        return (
            self.guaranteed_free_healthcare
            and self.guaranteed_shelter
            and not self.funded_by_speculative_markets
            and self.funded_by_active_guild_production
        )


# --------------------------------------------------------------------------
# 6. Decisive Access Test Evaluation
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class DecisiveAccessTest:
    mechanism_name: str
    provides_direct_physical_access: bool
    charges_interest_or_perpetual_subscription: bool
    creates_denial_incentive_for_profit: bool
    is_backed_by_real_production_or_reserves: bool

    @property
    def is_socially_defensible(self) -> bool:
        return (
            self.provides_direct_physical_access
            and not self.charges_interest_or_perpetual_subscription
            and not self.creates_denial_incentive_for_profit
            and self.is_backed_by_real_production_or_reserves
        )


# --------------------------------------------------------------------------
# 7. Float Asset Seizure, Commercial Real Estate & Restitution Engine
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class ContributorRestitutionAccount:
    citizen_id: str
    total_lifetime_premiums_paid_rcu: float
    total_claims_received_rcu: float
    mortgage_or_vehicle_debt_rcu: float = 0.0

    @property
    def net_restitution_balance_rcu(self) -> float:
        # Net owed back to citizen = what they paid minus what they already spent/claimed
        return max(0.0, self.total_lifetime_premiums_paid_rcu - self.total_claims_received_rcu)

    def apply_instant_debt_cancellation(self) -> dict[str, float]:
        net_balance = self.net_restitution_balance_rcu
        debt = self.mortgage_or_vehicle_debt_rcu
        debt_cancelled = min(net_balance, debt)
        remaining_debt = debt - debt_cancelled
        remaining_restitution_balance = net_balance - debt_cancelled

        return {
            "initial_net_balance_rcu": net_balance,
            "initial_debt_rcu": debt,
            "debt_cancelled_rcu": debt_cancelled,
            "remaining_debt_rcu": remaining_debt,
            "remaining_restitution_balance_rcu": remaining_restitution_balance,
        }


@dataclass(frozen=True)
class CitizensRestitutionTrust:
    total_seized_commercial_real_estate_value_rcu: float = 5_000_000_000.0  # Skyscraper & mall portfolio
    annual_commercial_rental_yield_pct: float = 0.08                        # 8% annual net rental income
    total_registered_contributors: int = 1_000_000
    total_net_contributed_float_rcu: float = 4_000_000_000.0

    @property
    def annual_rental_cashflow_rcu(self) -> float:
        return self.total_seized_commercial_real_estate_value_rcu * self.annual_commercial_rental_yield_pct

    @property
    def monthly_rental_cashflow_rcu(self) -> float:
        return self.annual_rental_cashflow_rcu / 12.0

    def calculate_citizen_monthly_dividend(
        self, citizen_net_balance_rcu: float
    ) -> dict[str, float]:
        if self.total_net_contributed_float_rcu <= 0 or citizen_net_balance_rcu <= 0:
            return {
                "monthly_dividend_rcu": 0.0,
                "annual_dividend_rcu": 0.0,
                "share_of_portfolio_pct": 0.0,
            }

        share_of_pool = citizen_net_balance_rcu / self.total_net_contributed_float_rcu
        monthly_dividend = self.monthly_rental_cashflow_rcu * share_of_pool
        annual_dividend = monthly_dividend * 12.0

        return {
            "monthly_dividend_rcu": round(monthly_dividend, 2),
            "annual_dividend_rcu": round(annual_dividend, 2),
            "share_of_portfolio_pct": round(share_of_pool * 100, 4),
        }

