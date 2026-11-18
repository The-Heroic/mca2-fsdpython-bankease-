from decimal import Decimal
import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from apps.accounts_auth.models import Branch, Role, User
from apps.banking_accounts.models import BankAccount
from apps.transfers.models import Transaction


@pytest.fixture
def sprint3_setup(db):
    cust_role, _ = Role.objects.get_or_create(
        role_code='CUSTOMER', defaults={'role_name': 'Customer', 'description': 'Customer'}
    )
    off_role, _ = Role.objects.get_or_create(
        role_code='BANK_OFFICER', defaults={'role_name': 'Bank Officer', 'description': 'Officer'}
    )
    branch = Branch.objects.create(
        ifsc_code='BNKE0000004',
        branch_name='Mumbai Nariman Point',
        address_line='Nariman Point',
        city='Mumbai',
        state='Maharashtra',
        pincode='400021',
        contact_phone='+91-2222845004',
    )
    customer = User.objects.create_user(
        username='cust_s3',
        email='cust.s3@bankease.in',
        phone_number='+91-9820033301',
        full_name='Sneha Kulkarni',
        password='Password@123',
        role=cust_role,
        home_branch=branch,
        kyc_status='PENDING',
    )
    officer = User.objects.create_user(
        username='off_s3',
        email='off.s3@bankease.in',
        phone_number='+91-9820033302',
        full_name='Priya Nair',
        password='Password@123',
        role=off_role,
        home_branch=branch,
        kyc_status='VERIFIED',
    )
    account = BankAccount.objects.create(
        user=customer,
        branch=branch,
        account_number='180004999001',
        account_type='SAVINGS',
        balance=Decimal('250000.00'),
        account_status='ACTIVE',
        opened_at=timezone.localdate(),
    )
    Transaction.objects.create(
        account=account,
        reference_utr='BNKFLAGTEST001',
        transaction_type='DEBIT',
        channel='RTGS',
        amount=Decimal('600000.00'),
        balance_after=Decimal('250000.00'),
        description='High-Value Flagged Test',
        status='FLAGGED',
        is_flagged=True,
    )
    return {'customer': customer, 'officer': officer, 'account': account}


@pytest.mark.django_db
def test_support_ticket_lifecycle(sprint3_setup):
    data = sprint3_setup
    client = APIClient()

    client.force_authenticate(user=data['customer'])
    tkt_res = client.post(
        reverse('support-ticket-list-create'),
        {
            'category': 'FUNDS_TRANSFER',
            'priority': 'HIGH',
            'subject': 'IMPS delayed acknowledgement',
            'description': 'UTR not reflecting on payee side.',
        },
        format='json',
    )
    assert tkt_res.status_code == status.HTTP_201_CREATED
    tkt_id = tkt_res.data['ticket_id']

    client.force_authenticate(user=data['officer'])
    reply_res = client.post(
        reverse('support-ticket-messages', kwargs={'ticket_id': tkt_id}),
        {'message_body': 'Checked NPCI switch; settlement confirmed.'},
        format='json',
    )
    assert reply_res.status_code == status.HTTP_201_CREATED

    res_status = client.patch(
        reverse('support-ticket-status', kwargs={'ticket_id': tkt_id}),
        {'ticket_status': 'RESOLVED', 'resolution_notes': 'Credited to payee.'},
        format='json',
    )
    assert res_status.status_code == status.HTTP_200_OK
    assert res_status.data['ticket_status'] == 'RESOLVED'


@pytest.mark.django_db
def test_kyc_verification_and_audit_logs(sprint3_setup):
    data = sprint3_setup
    client = APIClient()

    client.force_authenticate(user=data['customer'])
    kyc_res = client.post(
        reverse('kyc-list-create'),
        {
            'document_type': 'PAN_CARD',
            'document_number_masked': 'AHIPK8901H',
            'file_path': '/media/kyc/sneha_pan.pdf',
        },
        format='json',
    )
    assert kyc_res.status_code == status.HTTP_201_CREATED
    doc_id = kyc_res.data['kyc_doc_id']

    # Customer cannot view security audit logs
    deny_res = client.get(reverse('security-audit-logs'))
    assert deny_res.status_code == status.HTTP_403_FORBIDDEN

    # Officer verifies KYC -> creates audit log & updates user.kyc_status
    client.force_authenticate(user=data['officer'])
    ver_res = client.patch(
        reverse('kyc-verify', kwargs={'kyc_doc_id': doc_id}),
        {'verification_status': 'VERIFIED'},
        format='json',
    )
    assert ver_res.status_code == status.HTTP_200_OK
    data['customer'].refresh_from_db()
    assert data['customer'].kyc_status == 'VERIFIED'

    logs_res = client.get(reverse('security-audit-logs'))
    assert logs_res.status_code == status.HTTP_200_OK
    assert len(logs_res.data) >= 1

    flag_res = client.get(reverse('flagged-transactions'))
    assert flag_res.status_code == status.HTTP_200_OK
    assert len(flag_res.data) == 1


@pytest.mark.django_db
def test_notifications_and_dashboard_reporting(sprint3_setup):
    data = sprint3_setup
    client = APIClient()
    client.force_authenticate(user=data['customer'])

    n_res = client.post(
        reverse('notification-list-create'),
        {
            'notification_type': 'SECURITY',
            'priority': 'HIGH',
            'title': 'New Login Alert',
            'message': 'Logged in from Windows Chrome.',
            'channel': 'IN_APP',
        },
        format='json',
    )
    assert n_res.status_code == status.HTTP_201_CREATED

    list_n = client.get(reverse('notification-list-create'))
    assert list_n.data['unread_count'] == 1

    mark_res = client.post(reverse('notification-mark-all-read'))
    assert mark_res.data['marked_read'] == 1

    # Customer dashboard
    dash_res = client.get(reverse('reporting-dashboard'))
    assert dash_res.status_code == status.HTTP_200_OK
    assert Decimal(dash_res.data['kpis']['total_balance']) == Decimal('250000.00')

    # Report export & CSV download
    exp_res = client.post(
        reverse('reporting-exports'),
        {
            'report_type': 'ACCOUNT_STATEMENT',
            'file_format': 'CSV',
            'period_start': '2026-01-01',
            'period_end': '2026-12-31',
        },
        format='json',
    )
    assert exp_res.status_code == status.HTTP_201_CREATED
    dl_res = client.get(reverse('reporting-download', kwargs={'report_id': exp_res.data['report_id']}))
    assert dl_res.status_code == status.HTTP_200_OK
    assert 'text/csv' in dl_res['Content-Type']
