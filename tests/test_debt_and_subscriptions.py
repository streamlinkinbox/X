"""Tests for Abolishing Debt-Based and Subscription-Based Systems (§27)."""

import pytest

from model.rcu.debt_and_subscriptions import (
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

    comp = adv.calculate_commercial_loan_comparison(
        commercial_interest_rate_percent=15.0, loan_years=5
    )
    assert comp["principal_rcu"] == 15000.0
    assert comp["zero_interest_total_rcu"] == 15000.0
    assert comp["commercial_loan_total_rcu"] > 21000.0
    assert comp["interest_extraction_eliminated_rcu"] > 6000.0


def test_vehicle_purchase_comparison():
    veh = VehiclePurchaseComparison(cash_price_rcu=200_000.0, predatory_interest_and_fees_rcu=150_000.0)
    assert veh.fair_total_repayment_rcu == 200_000.0
    assert veh.predatory_total_repayment_rcu == 350_000.0
    assert veh.predatory_surcharge_ratio == 1.75


def test_cost_plus_housing_advance():
    housing = CostPlusHousingAdvance(
        land_preparation_cost_rcu=20_000.0,
        materials_and_timber_cost_rcu=60_000.0,
        guild_construction_labor_rcu=40_000.0,
        infrastructure_connection_rcu=10_000.0,
        transparent_admin_fee_rcu=2_000.0,
    )
    assert housing.total_cost_plus_price_rcu == 132_000.0
    comp = housing.compare_against_30yr_commercial_mortgage(mortgage_interest_rate_percent=9.0)
    assert comp["cost_plus_principal_rcu"] == 132_000.0
    assert comp["commercial_30yr_total_rcu"] > 380_000.0  # More than 2.8x the actual cost!
    assert comp["cost_multiplier"] > 2.8


def test_fair_borrowing_rules():
    assert len(FAIR_BORROWING_RULES) == 10
    titles = [r.rule_title for r in FAIR_BORROWING_RULES]
    assert "One Clear Total Price" in titles
    assert "No Compound Interest" in titles
    assert "No Hidden Conditions" in titles
    assert "No Forced Add-Ons" in titles
    assert "Fair Hardship Protection" in titles
    assert "No Essential-Asset Seizure" in titles
    assert "No Perpetual Repayment" in titles
    assert "Fresh Start After Honest Failure" in titles
    assert "Equal Bargaining Power" in titles
    assert "Absolute Ban on Debt Slavery" in titles


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
    commercial_med = DecisiveAccessTest(
        mechanism_name="Commercial Medical Aid Scheme",
        provides_direct_physical_access=False,
        charges_interest_or_perpetual_subscription=True,
        creates_denial_incentive_for_profit=True,
        is_backed_by_real_production_or_reserves=False,
    )
    assert commercial_med.is_socially_defensible is False

    sovereign_health = DecisiveAccessTest(
        mechanism_name="Direct Public Guild Provisioning",
        provides_direct_physical_access=True,
        charges_interest_or_perpetual_subscription=False,
        creates_denial_incentive_for_profit=False,
        is_backed_by_real_production_or_reserves=True,
    )
    assert sovereign_health.is_socially_defensible is True


def test_contributor_restitution_and_debt_cancellation():
    # Citizen paid 120,000 RCU in life/health/auto insurance over 15 years, claimed only 20,000 RCU
    account = ContributorRestitutionAccount(
        citizen_id="CIT-9921",
        total_lifetime_premiums_paid_rcu=120_000.0,
        total_claims_received_rcu=20_000.0,
        mortgage_or_vehicle_debt_rcu=80_000.0,
    )
    assert account.net_restitution_balance_rcu == 100_000.0

    # Instant debt offset against home/vehicle loan
    offset = account.apply_instant_debt_cancellation()
    assert offset["debt_cancelled_rcu"] == 80_000.0
    assert offset["remaining_debt_rcu"] == 0.0  # Completely debt-free!
    assert offset["remaining_restitution_balance_rcu"] == 20_000.0


def test_citizens_restitution_trust_monthly_dividend():
    trust = CitizensRestitutionTrust(
        total_seized_commercial_real_estate_value_rcu=5_000_000_000.0,
        annual_commercial_rental_yield_pct=0.08,  # 400M RCU / year
        total_registered_contributors=1_000_000,
        total_net_contributed_float_rcu=4_000_000_000.0,
    )
    assert trust.annual_rental_cashflow_rcu == 400_000_000.0
    assert trust.monthly_rental_cashflow_rcu == 400_000_000.0 / 12.0

    # A citizen with a remaining 40,000 RCU net contribution balance
    div = trust.calculate_citizen_monthly_dividend(citizen_net_balance_rcu=40_000.0)
    assert div["share_of_portfolio_pct"] == 0.001  # 40k / 4B = 1/100,000th of pool
    assert div["annual_dividend_rcu"] == 4_000.0
    assert div["monthly_dividend_rcu"] == round(4_000.0 / 12.0, 2)

