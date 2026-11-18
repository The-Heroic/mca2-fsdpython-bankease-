from decimal import Decimal
import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from apps.accounts_auth.models import Branch, Role, User
from apps.banking_accounts.models import BankAccount
from apps.bills.models import BillerDirectory
from apps.investments.models import InvestmentPlan
from apps.loans.models import LoanProduct


@pytest.fixture
def sprint2_setup(db):
    cust_role, _ = Role.objects.get_or_create(
        role_code='CUSTOMER', defaults={'role_name': 'Customer', 'description': 'Customer'}
    )
    off_role, _ = Role.objects.get_or_create(
        role_code='BANK_OFFICER', defaults={'role_name': 'Bank Officer', 'description': 'Officer'}
    )
    branch = Branch.objects.create(
        ifsc_code='BNKE0000003',
        branch_name='Ghaziabad Crossing',
        address_line='NH-24',
        city='Ghaziabad',
        state='Uttar Pradesh',
        pincode='201009',
        contact_phone='+91-1202845003',
    )
    customer = User.objects.create_user(
        username='cust_s2',
        email='cust.s2@bankease.in',
        phone_number='+91-9811133301',
        full_name='Ananya Singh',
        password='Password@123',
        role=cust_role,
        home_branch=branch,
        kyc_status='VERIFIED',
    )
    officer = User.objects.create_user(
        username='off_s2',
        email='off.s2@bankease.in',
        phone_number='+91-9811133302',
        full_name='Amit Tiwari',
        password='Password@123',
        role=off_role,
        home_branch=branch,
        kyc_status='VERIFIED',
    )
    account = BankAccount.objects.create(
        user=customer,
        branch=branch,
        account_number='180003999001',
        account_type='SAVINGS',
        balance=Decimal('100000.00'),
        account_status='ACTIVE',
        opened_at=timezone.localdate(),
    )
    biller = BillerDirectory.objects.create(
        biller_code='UPPCL_TEST',
        biller_name='UPPCL Electricity',
        category='ELECTRICITY',
        coverage_state='Uttar Pradesh',
    )
    loan_prod = LoanProduct.objects.create(
        product_code='LN_PERS_TEST',
        product_name='Express Personal Loan',
        loan_category='PERSONAL',
        min_amount=Decimal('10000.00'),
        max_amount=Decimal('1000000.00'),
        base_interest_rate=Decimal('10.00'),
        min_tenure_months=6,
        max_tenure_months=60,
    )
    inv_plan = InvestmentPlan.objects.create(
        plan_code='FD_TEST_1YR',
        plan_name='1-Year Fixed Deposit',
        investment_type='FIXED_DEPOSIT',
        min_investment=Decimal('10000.00'),
        expected_return_rate=Decimal('7.00'),
        lock_in_months=12,
        premature_penalty_pct=Decimal('1.00'),
    )
    return {
        'customer': customer,
        'officer': officer,
        'account': account,
        'biller': biller,
        'loan_prod': loan_prod,
        'inv_plan': inv_plan,
    }


@pytest.mark.django_db
def test_bill_payment_workflow(sprint2_setup):
    data = sprint2_setup
    client = APIClient()
    client.force_authenticate(user=data['customer'])

    link_res = client.post(
        reverse('customer-biller-list-create'),
        {
            'biller': data['biller'].biller_id,
            'consumer_number': '4012889011',
            'short_name': 'Home Power',
            'autopay_enabled': False,
        },
        format='json',
    )
    assert link_res.status_code == status.HTTP_201_CREATED

    pay_res = client.post(
        reverse('bill-pay-execute'),
        {
            'customer_biller_id': link_res.data['customer_biller_id'],
            'account_id': data['account'].account_id,
            'bill_amount': '2495.00',
            'bill_period': 'Nov-2026',
            'payment_mode': 'MANUAL',
        },
        format='json',
    )
    assert pay_res.status_code == status.HTTP_201_CREATED
    assert Decimal(pay_res.data['payment']['total_paid']) == Decimal('2500.00')  # includes ₹5 manual fee

    data['account'].refresh_from_db()
    assert data['account'].balance == Decimal('97500.00')


@pytest.mark.django_db
def test_loan_application_disbursal_and_emi_payment(sprint2_setup):
    data = sprint2_setup
    client = APIClient()

    # 1. Customer calculates EMI & applies
    client.force_authenticate(user=data['customer'])
    calc_res = client.post(
        reverse('loan-calculate-emi'),
        {'principal': '60000', 'interest_rate': '10.0', 'tenure_months': 6},
        format='json',
    )
    assert calc_res.status_code == status.HTTP_200_OK
    assert Decimal(calc_res.data['emi_amount']) > Decimal('10000.00')

    app_res = client.post(
        reverse('loan-application-list-create'),
        {
            'disbursement_account_id': data['account'].account_id,
            'loan_product_id': data['loan_prod'].loan_product_id,
            'requested_amount': '60000.00',
            'tenure_months': 6,
            'applicant_annual_income': '900000.00',
            'cibil_score': 780,
            'purpose_description': 'Home renovation',
        },
        format='json',
    )
    assert app_res.status_code == status.HTTP_201_CREATED
    loan_id = app_res.data['loan_id']

    # 2. Officer approves and disburses
    client.force_authenticate(user=data['officer'])
    rev_res = client.patch(
        reverse('loan-review', kwargs={'loan_id': loan_id}),
        {'decision': 'APPROVE_AND_DISBURSE', 'officer_remarks': 'CIBIL 780 verified'},
        format='json',
    )
    assert rev_res.status_code == status.HTTP_200_OK
    assert rev_res.data['loan_status'] == 'DISBURSED'

    data['account'].refresh_from_db()
    assert data['account'].balance == Decimal('160000.00')

    # 3. Customer views schedule & pays first EMI
    client.force_authenticate(user=data['customer'])
    rep_res = client.get(reverse('loan-repayments', kwargs={'loan_id': loan_id}))
    assert len(rep_res.data) == 6
    first_rep_id = rep_res.data[0]['repayment_id']

    pay_emi_res = client.post(reverse('loan-pay-emi', kwargs={'repayment_id': first_rep_id}))
    assert pay_emi_res.status_code == status.HTTP_200_OK
    assert pay_emi_res.data['repayment']['repayment_status'] == 'PAID'


@pytest.mark.django_db
def test_investment_booking_and_premature_closure(sprint2_setup):
    data = sprint2_setup
    client = APIClient()
    client.force_authenticate(user=data['customer'])

    inv_res = client.post(
        reverse('investment-list-create'),
        {
            'funding_account_id': data['account'].account_id,
            'plan_id': data['inv_plan'].plan_id,
            'principal_amount': '50000.00',
            'tenure_months': 12,
            'auto_renew': False,
        },
        format='json',
    )
    assert inv_res.status_code == status.HTTP_201_CREATED
    assert Decimal(inv_res.data['projected_maturity_amount']) == Decimal('53500.00')

    data['account'].refresh_from_db()
    assert data['account'].balance == Decimal('50000.00')

    close_res = client.post(
        reverse('investment-close', kwargs={'investment_id': inv_res.data['investment_id']})
    )
    assert close_res.status_code == status.HTTP_200_OK
    assert close_res.data['investment']['investment_status'] == 'PREMATURE_CLOSED'

    data['account'].refresh_from_db()
    # 50000 - 1% penalty (500) = 49500 credited back -> 50000 + 49500 = 99500
    assert data['account'].balance == Decimal('99500.00')
