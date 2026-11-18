from decimal import Decimal
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.accounts_auth.models import Branch, Role, User
from apps.banking_accounts.models import BankAccount


@pytest.fixture
def setup_users_and_branch(db):
    cust_role, _ = Role.objects.get_or_create(
        role_code='CUSTOMER',
        defaults={'role_name': 'Retail / Corporate Customer', 'description': 'Customer'},
    )
    off_role, _ = Role.objects.get_or_create(
        role_code='BANK_OFFICER',
        defaults={'role_name': 'Bank Officer', 'description': 'Officer'},
    )
    branch = Branch.objects.create(
        ifsc_code='BNKE0000002',
        branch_name='Noida Sector 62',
        address_line='Plot C-20, Sector 62',
        city='Noida',
        state='Uttar Pradesh',
        pincode='201309',
        contact_phone='+91-1202405002',
    )
    aarav = User.objects.create_user(
        username='aarav_s1',
        email='aarav.s1@bankease.in',
        phone_number='+91-9811100001',
        full_name='Aarav Gupta',
        password='Password@123',
        role=cust_role,
        home_branch=branch,
        kyc_status='PENDING',
    )
    ananya = User.objects.create_user(
        username='ananya_s1',
        email='ananya.s1@bankease.in',
        phone_number='+91-9811100002',
        full_name='Ananya Singh',
        password='Password@123',
        role=cust_role,
        home_branch=branch,
        kyc_status='VERIFIED',
    )
    officer = User.objects.create_user(
        username='officer_s1',
        email='officer.s1@bankease.in',
        phone_number='+91-9811100003',
        full_name='Priya Nair',
        password='Password@123',
        role=off_role,
        home_branch=branch,
        kyc_status='VERIFIED',
    )
    return {'aarav': aarav, 'ananya': ananya, 'officer': officer, 'branch': branch}


@pytest.mark.django_db
def test_account_opening_officer_kyc_approval_and_intrabank_transfer(setup_users_and_branch):
    data = setup_users_and_branch
    client = APIClient()

    # 1. Aarav opens a Savings account -> starts as PENDING_KYC
    client.force_authenticate(user=data['aarav'])
    open_res = client.post(
        reverse('account-list-create'),
        {
            'branch_id': data['branch'].branch_id,
            'account_type': 'SAVINGS',
            'initial_deposit': '50000.00',
            'nominee_name': 'Meena Gupta',
            'nominee_relation': 'Mother',
        },
        format='json',
    )
    assert open_res.status_code == status.HTTP_201_CREATED
    aarav_acc_id = open_res.data['account_id']
    assert open_res.data['account_status'] == 'PENDING_KYC'

    # 2. Ananya opens a Savings account (already VERIFIED KYC) -> starts as ACTIVE
    client.force_authenticate(user=data['ananya'])
    ananya_res = client.post(
        reverse('account-list-create'),
        {'branch_id': data['branch'].branch_id, 'account_type': 'SAVINGS', 'initial_deposit': '10000.00'},
        format='json',
    )
    assert ananya_res.status_code == status.HTTP_201_CREATED
    ananya_acc_no = ananya_res.data['account_number']
    assert ananya_res.data['account_status'] == 'ACTIVE'

    # 3. Officer approves Aarav's account -> ACTIVE
    client.force_authenticate(user=data['officer'])
    approve_res = client.patch(
        reverse('account-status-update', kwargs={'account_id': aarav_acc_id}),
        {'account_status': 'ACTIVE'},
        format='json',
    )
    assert approve_res.status_code == status.HTTP_200_OK
    assert approve_res.data['account_status'] == 'ACTIVE'

    # 4. Aarav registers Ananya as an intrabank beneficiary & transfers INR 15,000
    client.force_authenticate(user=data['aarav'])
    ben_res = client.post(
        reverse('beneficiary-list-create'),
        {
            'nickname': 'Ananya Sister',
            'beneficiary_name': 'Ananya Singh',
            'account_number': ananya_acc_no,
            'bank_name': 'BankEase Ltd',
            'ifsc_code': 'BNKE0000002',
        },
        format='json',
    )
    assert ben_res.status_code == status.HTTP_201_CREATED
    assert ben_res.data['transfer_type'] == 'INTRABANK'

    tx_res = client.post(
        reverse('transfer-execute'),
        {
            'source_account_id': aarav_acc_id,
            'beneficiary_id': ben_res.data['beneficiary_id'],
            'channel': 'INTERNAL',
            'amount': '15000.00',
            'remarks': 'Sister Gift',
        },
        format='json',
    )
    assert tx_res.status_code == status.HTTP_201_CREATED
    assert Decimal(tx_res.data['transaction']['balance_after']) == Decimal('35000.00')

    # Verify Ananya's balance increased atomically
    ananya_acc = BankAccount.objects.get(account_number=ananya_acc_no)
    assert ananya_acc.balance == Decimal('25000.00')

    # Verify statement endpoint
    stmt_res = client.get(reverse('account-statement', kwargs={'account_id': aarav_acc_id}))
    assert stmt_res.status_code == status.HTTP_200_OK
    assert len(stmt_res.data['transactions']) == 1


@pytest.mark.django_db
def test_transfer_rejects_insufficient_balance_and_cooling_beneficiary(setup_users_and_branch):
    data = setup_users_and_branch
    client = APIClient()
    client.force_authenticate(user=data['ananya'])

    acc_res = client.post(
        reverse('account-list-create'),
        {'branch_id': data['branch'].branch_id, 'account_type': 'SAVINGS', 'initial_deposit': '2000.00'},
        format='json',
    )
    acc_id = acc_res.data['account_id']

    # Add beneficiary with 30-min cooling period
    ben_res = client.post(
        reverse('beneficiary-list-create'),
        {
            'beneficiary_name': 'External Payee',
            'account_number': '998877665544',
            'bank_name': 'SBI',
            'ifsc_code': 'SBIN0001234',
            'cooling_minutes': 30,
        },
        format='json',
    )
    assert ben_res.data['status'] == 'COOLING'
    ben_id = ben_res.data['beneficiary_id']

    # Should fail while cooling
    fail_cool = client.post(
        reverse('transfer-execute'),
        {'source_account_id': acc_id, 'beneficiary_id': ben_id, 'channel': 'IMPS', 'amount': '500.00'},
        format='json',
    )
    assert fail_cool.status_code == status.HTTP_400_BAD_REQUEST

    # Activate beneficiary, then try exceeding balance
    act_res = client.patch(reverse('beneficiary-activate', kwargs={'beneficiary_id': ben_id}))
    assert act_res.data['status'] == 'ACTIVE'

    fail_bal = client.post(
        reverse('transfer-execute'),
        {'source_account_id': acc_id, 'beneficiary_id': ben_id, 'channel': 'IMPS', 'amount': '5000.00'},
        format='json',
    )
    assert fail_bal.status_code == status.HTTP_400_BAD_REQUEST
