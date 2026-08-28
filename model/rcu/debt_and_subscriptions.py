"""Abolishing Debt-Based and Subscription-Based Systems: Real Production and Shared Provision.

This module formalizes the economic model replacing debt-based and subscription-based
financial extraction with direct public provisioning, zero-interest resource advances,
physical risk pooling, and intergenerational elder care:
1. ``ExtractionModelType`` -- Categorizes extractive financial mechanisms:
   - Commercial Medical Aid Subscriptions
   - Private Commercial Insurance
   - Private Pension / Speculative Fund Management
   - Compound-Interest Commercial Loans (Payday, Auto, Housing)
   - Sovereign Debt / Bond Markets
2. ``ReplacementMechanismType`` -- Models sovereign, commodity-backed replacements:
   - Direct Guild Hospitals & Public Healthcare Provision
   - Physical Commodity Reserve Risk Pools (48h rebuild)
   - Master-Apprentice Elder Production Stipends (Real Commodity Units)
   - Zero-Interest Non-Compounding Advances (Pay principal only, when revenue is made)
   - Direct Commodity-Backed Development Budgets
3. ``ZeroInterestAdvance`` -- Models zero-interest financing for vehicles, housing, and tools
   (Interest = 0%, No compound clock, No primary home seizure, Flexible pause on hardship).
4. ``ElderCareCompact`` -- Models physical commodity allocation for retirees backed by guild production.
5. ``DecisiveAccessTest`` -- Evaluates whether a financial mechanism provides real access or extracts rent.
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
# 2. Zero-Interest Non-Compounding Advance Model (Vehicles, Housing, Tools)
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
        # Simple amortization comparison showing extraction avoided
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
# 3. Elder Care Production Compact (Intergenerational Security)
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
        # Real physical commodity delivery is immune to paper financial collapse
        return (
            self.guaranteed_free_healthcare
            and self.guaranteed_shelter
            and not self.funded_by_speculative_markets
            and self.funded_by_active_guild_production
        )


# --------------------------------------------------------------------------
# 4. Decisive Access Test Evaluation
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
        # Pass: provides direct access, zero perpetual subscription/interest extraction,
        # zero profit-driven denial incentive, and backed by real production.
        return (
            self.provides_direct_physical_access
            and not self.charges_interest_or_perpetual_subscription
            and not self.creates_denial_incentive_for_profit
            and self.is_backed_by_real_production_or_reserves
        )
