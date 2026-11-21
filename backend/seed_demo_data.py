import os
import sys
from decimal import Decimal
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bankease_config.settings')

import django
django.setup()

from django.utils import timezone
from apps.accounts_auth.models import Role, Branch, User
from apps.banking_accounts.models import BankAccount
from apps.transfers.models import Beneficiary, Transaction
from apps.bills.models import BillerDirectory, CustomerBiller
from apps.loans.models import LoanProduct, LoanApplication
from apps.investments.models import InvestmentPlan, Investment
from apps.support.models import SupportTicket
from apps.notifications.models import Notification

def run_seed():
    print("Seeding BankEase Demo Data...")

    # 1. ROLES
    roles_def = [
        ('ADMIN', 'System Administrator', 'Full system configuration, user role management, and compliance oversight'),
        ('BANK_OFFICER', 'Bank Officer', 'Branch operations, KYC verification, loan sanctioning, and ticket resolution'),
        ('CUSTOMER', 'Retail / Corporate Customer', 'Standard net banking access for accounts, transfers, bills, loans, and investments'),
        ('AUDITOR', 'Compliance & Risk Auditor', 'Read-only access to security audit trails, flagged transactions, and regulatory reports'),
    ]
    roles_map = {}
    for code, name, desc in roles_def:
        role_obj, _ = Role.objects.get_or_create(role_code=code, defaults={'role_name': name, 'description': desc})
        roles_map[code] = role_obj
    print(f"Roles verified: {list(roles_map.keys())}")

    # 2. BRANCHES
    b1, _ = Branch.objects.get_or_create(
        ifsc_code='BNKE0000001',
        defaults={
            'branch_name': 'Connaught Place Main Branch',
            'address_line': 'Block A, Inner Circle, Connaught Place',
            'city': 'New Delhi',
            'state': 'Delhi',
            'pincode': '110001',
            'contact_phone': '+91-1123415001'
        }
    )
    b2, _ = Branch.objects.get_or_create(
        ifsc_code='BNKE0000002',
        defaults={
            'branch_name': 'Noida Sector 62 IT Hub',
            'address_line': 'Plot C-20, Sector 62',
            'city': 'Noida',
            'state': 'Uttar Pradesh',
            'pincode': '201309',
            'contact_phone': '+91-1202405002'
        }
    )
    b3, _ = Branch.objects.get_or_create(
        ifsc_code='BNKE0000003',
        defaults={
            'branch_name': 'Ghaziabad Crossing Republik',
            'address_line': 'NH-24, Dundahera, Crossing Republik',
            'city': 'Ghaziabad',
            'state': 'Uttar Pradesh',
            'pincode': '201009',
            'contact_phone': '+91-1202845003'
        }
    )
    print("Branches verified.")

    # 3. USERS
    # Main Demo Customer: aarav.sharma@example.com / Secure@123
    u_aarav = User.objects.filter(email='aarav.sharma@example.com').first()
    if not u_aarav:
        u_aarav = User.objects.filter(username='aarav_gupta').first()
    if not u_aarav:
        u_aarav = User.objects.create(
            username='aarav_gupta',
            email='aarav.sharma@example.com',
            full_name='Aarav Sharma',
            phone_number='+91-9811122001',
            role=roles_map['CUSTOMER'],
            home_branch=b2,
            kyc_status='VERIFIED',
            city='Noida',
            state='Uttar Pradesh',
            pincode='201301',
            is_active=True,
            is_locked=False,
        )
    else:
        u_aarav.email = 'aarav.sharma@example.com'
        u_aarav.role = roles_map['CUSTOMER']
        u_aarav.home_branch = b2
        u_aarav.is_active = True
        u_aarav.is_locked = False
    u_aarav.set_password('Secure@123')
    u_aarav.failed_login_attempts = 0
    u_aarav.save()

    # Demo Bank Officer: vikram.officer@bankease.com / Officer@123
    u_officer = User.objects.filter(email='vikram.officer@bankease.com').first()
    if not u_officer:
        u_officer = User.objects.filter(username='officer_priya').first()
    if not u_officer:
        u_officer = User.objects.create(
            username='officer_priya',
            email='vikram.officer@bankease.com',
            full_name='Vikram Malhotra (Officer)',
            phone_number='+91-9810010002',
            role=roles_map['BANK_OFFICER'],
            home_branch=b2,
            kyc_status='VERIFIED',
            city='Noida',
            state='Uttar Pradesh',
            pincode='201304',
            is_active=True,
            is_locked=False,
        )
    else:
        u_officer.email = 'vikram.officer@bankease.com'
        u_officer.role = roles_map['BANK_OFFICER']
        u_officer.home_branch = b2
        u_officer.is_active = True
        u_officer.is_locked = False
    u_officer.set_password('Officer@123')
    u_officer.failed_login_attempts = 0
    u_officer.save()

    # Demo Admin: admin@bankease.com / Admin@123
    u_admin = User.objects.filter(email='admin@bankease.com').first()
    if not u_admin:
        u_admin = User.objects.filter(username='admin_rajesh').first()
    if not u_admin:
        u_admin = User.objects.create(
            username='admin_rajesh',
            email='admin@bankease.com',
            full_name='Rajesh Verma (Admin)',
            phone_number='+91-9810010001',
            role=roles_map['ADMIN'],
            home_branch=b1,
            kyc_status='VERIFIED',
            is_active=True,
            is_locked=False,
            is_staff=True,
            is_superuser=True,
        )
    else:
        u_admin.email = 'admin@bankease.com'
        u_admin.role = roles_map['ADMIN']
        u_admin.home_branch = b1
        u_admin.is_active = True
        u_admin.is_locked = False
    u_admin.set_password('Admin@123')
    u_admin.failed_login_attempts = 0
    u_admin.save()

    # Demo Locked User: locked.user@example.com / WrongPassword
    u_locked = User.objects.filter(email='locked.user@example.com').first()
    if not u_locked:
        u_locked = User.objects.create(
            username='locked_user',
            email='locked.user@example.com',
            full_name='Suresh Sawant (Locked User)',
            phone_number='+91-9900099005',
            role=roles_map['CUSTOMER'],
            home_branch=b1,
            kyc_status='REJECTED',
            is_active=False,
            is_locked=True,
            failed_login_attempts=5,
        )
    else:
        u_locked.is_locked = True
        u_locked.is_active = False
        u_locked.failed_login_attempts = 5
    u_locked.set_password('Secure@123')
    u_locked.save()

    # Personal user accounts (akanurag and anurag)
    for uname in ['akanurag', 'anurag']:
        u = User.objects.filter(username=uname).first()
        if u:
            u.set_password('Secure@123')
            u.is_active = True
            u.is_locked = False
            u.failed_login_attempts = 0
            u.save()
            print(f"Personal account ready: {uname} / Secure@123")

    print("Users initialized successfully.")

    # 4. BANK ACCOUNTS
    acc1 = BankAccount.objects.filter(account_number='180002000001').first()
    if not acc1:
        acc1 = BankAccount.objects.create(
            user=u_aarav,
            branch=b2,
            account_number='180002000001',
            account_type='SAVINGS',
            currency='INR',
            balance=Decimal('125000.00'),
            minimum_balance=Decimal('5000.00'),
            daily_transfer_limit=Decimal('500000.00'),
            interest_rate=Decimal('3.50'),
            account_status='ACTIVE',
            nominee_name='Meena Sharma',
            nominee_relation='Mother',
            opened_at=date(2024, 2, 12),
        )
    else:
        acc1.user = u_aarav
        acc1.balance = Decimal('125000.00')
        acc1.account_status = 'ACTIVE'
        acc1.save()

    acc2 = BankAccount.objects.filter(account_number='180002000002').first()
    if not acc2:
        acc2 = BankAccount.objects.create(
            user=u_aarav,
            branch=b2,
            account_number='180002000002',
            account_type='CURRENT',
            currency='INR',
            balance=Decimal('450000.00'),
            minimum_balance=Decimal('25000.00'),
            daily_transfer_limit=Decimal('1000000.00'),
            interest_rate=Decimal('0.00'),
            account_status='ACTIVE',
            nominee_name='Siddharth Sharma',
            nominee_relation='Father',
            opened_at=date(2024, 6, 1),
        )
    else:
        acc2.user = u_aarav
        acc2.balance = Decimal('450000.00')
        acc2.save()

    # Also make sure personal account exists
    for uname in ['akanurag', 'anurag']:
        u = User.objects.filter(username=uname).first()
        if u and not BankAccount.objects.filter(user=u).exists():
            BankAccount.objects.create(
                user=u,
                branch=b3,
                account_number='180003000001' if uname == 'akanurag' else '180003000002',
                account_type='SAVINGS',
                currency='INR',
                balance=Decimal('250000.00'),
                minimum_balance=Decimal('5000.00'),
                daily_transfer_limit=Decimal('500000.00'),
                account_status='ACTIVE',
                opened_at=date(2024, 2, 12),
            )

    print("Bank Accounts initialized.")

    # 5. BENEFICIARIES
    ben1 = Beneficiary.objects.filter(user=u_aarav, account_number='180003000003').first()
    if not ben1:
        ben1 = Beneficiary.objects.create(
            user=u_aarav,
            account_number='180003000003',
            nickname='Ananya Sister',
            beneficiary_name='Ananya Pratap Singh',
            bank_name='BankEase Ltd',
            ifsc_code='BNKE0000003',
            transfer_type='INTRABANK',
            daily_limit=Decimal('200000.00'),
            cooling_ends_at=timezone.now() - timedelta(days=5),
            is_verified=True,
            status='ACTIVE',
        )

    ben2 = Beneficiary.objects.filter(user=u_aarav, account_number='004501552310').first()
    if not ben2:
        ben2 = Beneficiary.objects.create(
            user=u_aarav,
            account_number='004501552310',
            nickname='Ramesh Landlord',
            beneficiary_name='Ramesh Chandra Agarwal',
            bank_name='State Bank of India',
            ifsc_code='SBIN0001234',
            transfer_type='INTERBANK',
            daily_limit=Decimal('100000.00'),
            cooling_ends_at=timezone.now() - timedelta(days=10),
            is_verified=True,
            status='ACTIVE',
        )
    print("Beneficiaries verified.")

    # 6. TRANSACTIONS
    if not Transaction.objects.filter(account=acc1).exists():
        Transaction.objects.create(
            account=acc1,
            reference_utr='TXN202611019001',
            transaction_type='CREDIT',
            channel='NEFT',
            amount=Decimal('85000.00'),
            balance_after=Decimal('125000.00'),
            currency='INR',
            description='Monthly Salary Credit from TechCorp India',
            status='SUCCESS',
        )
        Transaction.objects.create(
            account=acc1,
            reference_utr='TXN202611108821',
            transaction_type='DEBIT',
            channel='UPI',
            amount=Decimal('2450.00'),
            balance_after=Decimal('122550.00'),
            currency='INR',
            description='Electricity Bill Payment - Torrent Power',
            status='SUCCESS',
        )
        Transaction.objects.create(
            account=acc1,
            reference_utr='TXN202611157743',
            transaction_type='DEBIT',
            channel='IMPS',
            amount=Decimal('15000.00'),
            balance_after=Decimal('107550.00'),
            currency='INR',
            description='Rent Transfer to Ramesh Landlord',
            status='SUCCESS',
        )
    print("Transactions initialized.")

    # 7. BILLERS
    b1_dir, _ = BillerDirectory.objects.get_or_create(
        biller_code='BILL00000001',
        defaults={
            'biller_name': 'Torrent Power Ltd - Agra & NCR',
            'category': 'ELECTRICITY',
            'coverage_state': 'PAN_INDIA',
            'is_active': True,
        }
    )
    b2_dir, _ = BillerDirectory.objects.get_or_create(
        biller_code='BILL00000002',
        defaults={
            'biller_name': 'Indraprastha Gas Limited (IGL)',
            'category': 'PIPED_GAS',
            'coverage_state': 'Delhi NCR',
            'is_active': True,
        }
    )
    b3_dir, _ = BillerDirectory.objects.get_or_create(
        biller_code='BILL00000003',
        defaults={
            'biller_name': 'Airtel Broadband Fiber',
            'category': 'BROADBAND',
            'coverage_state': 'PAN_INDIA',
            'is_active': True,
        }
    )

    cb = CustomerBiller.objects.filter(user=u_aarav, biller=b1_dir).first()
    if not cb:
        CustomerBiller.objects.create(
            user=u_aarav,
            biller=b1_dir,
            consumer_number='1099238471',
            short_name='Home Electricity',
            autopay_enabled=True,
            autopay_max_limit=Decimal('5000.00'),
            preferred_account=acc1,
            status='ACTIVE',
        )
    print("Billers verified.")

    # 8. LOANS
    lp1, _ = LoanProduct.objects.get_or_create(
        product_code='HL-STD-01',
        defaults={
            'product_name': 'Dream Home Loan',
            'loan_category': 'HOME',
            'base_interest_rate': Decimal('8.50'),
            'min_amount': Decimal('500000.00'),
            'max_amount': Decimal('10000000.00'),
            'min_tenure_months': 12,
            'max_tenure_months': 240,
            'processing_fee_pct': Decimal('0.50'),
            'is_active': True,
        }
    )
    lp2, _ = LoanProduct.objects.get_or_create(
        product_code='PL-FLEXI-02',
        defaults={
            'product_name': 'Instant Personal Loan',
            'loan_category': 'PERSONAL',
            'base_interest_rate': Decimal('11.50'),
            'min_amount': Decimal('50000.00'),
            'max_amount': Decimal('1500000.00'),
            'min_tenure_months': 6,
            'max_tenure_months': 60,
            'processing_fee_pct': Decimal('1.00'),
            'is_active': True,
        }
    )

    la = LoanApplication.objects.filter(user=u_aarav).first()
    if not la:
        LoanApplication.objects.create(
            application_number='LN2026110001',
            user=u_aarav,
            disbursement_account=acc1,
            loan_product=lp2,
            requested_amount=Decimal('200000.00'),
            sanctioned_amount=Decimal('200000.00'),
            interest_rate=Decimal('11.50'),
            tenure_months=24,
            emi_amount=Decimal('9368.52'),
            outstanding_principal=Decimal('185000.00'),
            applicant_annual_income=Decimal('950000.00'),
            cibil_score=780,
            purpose_description='Home renovation & electronics',
            loan_status='DISBURSED',
            disbursed_at=timezone.now() - timedelta(days=30),
        )
    print("Loans verified.")

    # 9. INVESTMENTS
    inv_plan, _ = InvestmentPlan.objects.get_or_create(
        plan_code='FD-CUM-01',
        defaults={
            'plan_name': 'BankEase Fixed Deposit Special',
            'investment_type': 'FIXED_DEPOSIT',
            'expected_return_rate': Decimal('7.25'),
            'min_investment': Decimal('10000.00'),
            'lock_in_months': 12,
            'premature_penalty_pct': Decimal('1.00'),
            'risk_level': 'LOW',
            'is_active': True,
        }
    )

    inv = Investment.objects.filter(user=u_aarav).first()
    if not inv:
        Investment.objects.create(
            certificate_number='FD2026110001',
            user=u_aarav,
            funding_account=acc1,
            plan=inv_plan,
            principal_amount=Decimal('50000.00'),
            interest_rate=Decimal('7.25'),
            tenure_months=12,
            projected_maturity_amount=Decimal('53724.80'),
            start_date=date(2024, 3, 1),
            maturity_date=date(2025, 3, 1),
            investment_status='ACTIVE',
        )
    print("Investments verified.")

    # 10. SUPPORT TICKET
    st = SupportTicket.objects.filter(user=u_aarav).first()
    if not st:
        SupportTicket.objects.create(
            ticket_number='TKT-202611-001',
            user=u_aarav,
            category='DISPUTED_TRANSACTION',
            priority='MEDIUM',
            subject='Inquiry on International Debit Card Activation',
            description='Kindly assist with enabling international e-commerce on my Platinum debit card.',
            ticket_status='OPEN',
        )
    print("Support tickets verified.")

    # 11. NOTIFICATIONS
    Notification.objects.get_or_create(
        user=u_aarav,
        title='Welcome to BankEase NextGen Net Banking',
        defaults={
            'message': 'Your BankEase profile is verified and active. Explore transfers, bills, and investments.',
            'notification_type': 'SECURITY',
            'is_read': False,
        }
    )
    Notification.objects.get_or_create(
        user=u_aarav,
        title='Salary Credited: ₹85,000.00',
        defaults={
            'message': 'Your account 180002000001 has been credited with ₹85,000.00 from TechCorp India via NEFT.',
            'notification_type': 'TRANSACTION',
            'is_read': True,
        }
    )

    print("\n=======================================================")
    print("✅ SEEDING COMPLETE! ALL DEMO ACCOUNTS FULLY OPERATIONAL")
    print("=======================================================")

if __name__ == '__main__':
    run_seed()
