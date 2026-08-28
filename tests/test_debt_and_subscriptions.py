"""Tests for Abolishing Debt-Based and Subscription-Based Systems (§27)."""

import pytest

from model.rcu.debt_and_subscriptions import (
    DecisiveAccessTest,
    ElderCareStipend,
    FinancialSector,
    MechanismComparison,
    SECTOR_COMPARISONS,
    ZeroInterestAdvance,
)


def test_sector_comparisons_coverage():
    assert len(SECTOR_COMPARISONS) == 6
    sectors = {s.sector for s in SECTOR_COMPARISONS}
    assert FinancialSector.HEALTHCARE in sectors
    assert FinancialSector.RISK_AND_DISASTER in sectors
    assert FinancialSector.ELDER_SECURITY in sectors
    assert FinancialSector.LEGAL_PROTECTION in sectors
    assert FinancialSector.EQUIPMENT_AND_HOUSING in sectors
    assert FinancialSector.INFRASTRUCTURE_FINANCE in sectors


def test_zero_interest_advance_vehicle_and_housing():
    # Vehicle or housing advance of 15,000 RCU
    adv = ZeroInterestAdvance(
        item_description="Essential transport utility vehicle",
        principal_amount_rcu=15000.0,
        monthly_installment_rcu=250.0,
    )
    assert adv.interest_rate_percent == 0.0
    assert adv.total_repayment_amount_rcu == 15000.0
    assert adv.standard_payoff_months == 60
    assert adv.seizure_of_primary_residence_allowed is False
    assert adv.pause_on_documented_hardship is True

    # Compare with commercial loan at 15% interest over 5 years
    comp = adv.calculate_commercial_loan_comparison(
        commercial_interest_rate_percent=15.0, loan_years=5
    )
    assert comp["principal_rcu"] == 15000.0
    assert comp["zero_interest_total_rcu"] == 15000.0
    assert comp["commercial_loan_total_rcu"] > 21000.0
    assert comp["interest_extraction_eliminated_rcu"] > 6000.0


def test_elder_care_stipend():
    elder = ElderCareStipend()
    assert elder.monthly_grain_ration_kg == 25.0
    assert elder.monthly_oil_ration_liters == 4.0
    assert elder.guaranteed_free_healthcare is True
    assert elder.guaranteed_shelter is True
    assert elder.funded_by_speculative_markets is False
    assert elder.funded_by_active_guild_production is True
    assert elder.is_inflation_and_crash_proof is True


def test_decisive_access_test():
    # Commercial Medical Aid: Fails test
    commercial_med = DecisiveAccessTest(
        mechanism_name="Commercial Medical Aid Scheme",
        provides_direct_physical_access=False,
        charges_interest_or_perpetual_subscription=True,
        creates_denial_incentive_for_profit=True,
        is_backed_by_real_production_or_reserves=False,
    )
    assert commercial_med.is_socially_defensible is False

    # Sovereign Direct Guild Health Provision: Passes test
    sovereign_health = DecisiveAccessTest(
        mechanism_name="Direct Public Guild Provisioning",
        provides_direct_physical_access=True,
        charges_interest_or_perpetual_subscription=False,
        creates_denial_incentive_for_profit=False,
        is_backed_by_real_production_or_reserves=True,
    )
    assert sovereign_health.is_socially_defensible is True
