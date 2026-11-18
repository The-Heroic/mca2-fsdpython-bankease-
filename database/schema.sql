-- ============================================================================
-- Project: P18 | BankEase - NextGen Net Banking Application
-- Track:   FSD Python (Python 3.11+, Django 4.2, React 18, MySQL 8.0)
-- File:    database/schema.sql
-- Purpose: 3NF Normalized Relational Schema for MySQL 8.0 (InnoDB, utf8mb4)
--          covering all 10 core modules of BankEase.
-- ============================================================================

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

CREATE DATABASE IF NOT EXISTS bankease_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE bankease_db;

-- Drop existing tables in reverse dependency order for clean re-runs
DROP TABLE IF EXISTS report_exports;
DROP TABLE IF EXISTS notifications;
DROP TABLE IF EXISTS security_audit_logs;
DROP TABLE IF EXISTS kyc_documents;
DROP TABLE IF EXISTS ticket_messages;
DROP TABLE IF EXISTS support_tickets;
DROP TABLE IF EXISTS investments;
DROP TABLE IF EXISTS investment_plans;
DROP TABLE IF EXISTS loan_repayments;
DROP TABLE IF EXISTS loan_applications;
DROP TABLE IF EXISTS loan_products;
DROP TABLE IF EXISTS bill_payments;
DROP TABLE IF EXISTS customer_billers;
DROP TABLE IF EXISTS biller_Directory;
DROP TABLE IF EXISTS biller_directory;
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS beneficiaries;
DROP TABLE IF EXISTS bank_accounts;
DROP TABLE IF EXISTS branches;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS roles;

-- ============================================================================
-- MODULE 1: USER AUTHENTICATION (roles, users)
-- ============================================================================

CREATE TABLE roles (
    role_id INT AUTO_INCREMENT PRIMARY KEY,
    role_code VARCHAR(30) NOT NULL UNIQUE,
    role_name VARCHAR(60) NOT NULL UNIQUE,
    description VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE branches (
    branch_id INT AUTO_INCREMENT PRIMARY KEY,
    ifsc_code CHAR(11) NOT NULL UNIQUE,
    branch_name VARCHAR(100) NOT NULL,
    address_line VARCHAR(255) NOT NULL,
    city VARCHAR(60) NOT NULL,
    state VARCHAR(60) NOT NULL,
    pincode CHAR(6) NOT NULL,
    contact_phone VARCHAR(15) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_branches_city (city)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    role_id INT NOT NULL,
    home_branch_id INT NULL,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    phone_number VARCHAR(15) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(120) NOT NULL,
    date_of_birth DATE NULL,
    pan_number CHAR(10) NULL UNIQUE,
    aadhaar_last4 CHAR(4) NULL,
    address_line VARCHAR(255) NULL,
    city VARCHAR(60) NULL,
    state VARCHAR(60) NULL,
    pincode CHAR(6) NULL,
    kyc_status ENUM('PENDING', 'SUBMITTED', 'VERIFIED', 'REJECTED') NOT NULL DEFAULT 'PENDING',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_locked BOOLEAN NOT NULL DEFAULT FALSE,
    failed_login_attempts INT NOT NULL DEFAULT 0,
    last_login_at DATETIME NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_users_role FOREIGN KEY (role_id) REFERENCES roles(role_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_users_branch FOREIGN KEY (home_branch_id) REFERENCES branches(branch_id) ON DELETE SET NULL ON UPDATE CASCADE,
    INDEX idx_users_role (role_id),
    INDEX idx_users_branch (home_branch_id),
    INDEX idx_users_kyc_status (kyc_status),
    INDEX idx_users_full_name (full_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- MODULE 2: ACCOUNT MANAGEMENT (bank_accounts)
-- ============================================================================

CREATE TABLE bank_accounts (
    account_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    branch_id INT NOT NULL,
    account_number CHAR(12) NOT NULL UNIQUE,
    account_type ENUM('SAVINGS', 'CURRENT', 'SALARY') NOT NULL DEFAULT 'SAVINGS',
    currency CHAR(3) NOT NULL DEFAULT 'INR',
    balance DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
    minimum_balance DECIMAL(10, 2) NOT NULL DEFAULT 1000.00,
    daily_transfer_limit DECIMAL(12, 2) NOT NULL DEFAULT 200000.00,
    interest_rate DECIMAL(5, 2) NOT NULL DEFAULT 3.50,
    account_status ENUM('PENDING_KYC', 'ACTIVE', 'FROZEN', 'DORMANT', 'CLOSED') NOT NULL DEFAULT 'ACTIVE',
    nominee_name VARCHAR(120) NULL,
    nominee_relation VARCHAR(50) NULL,
    opened_at DATE NOT NULL,
    closed_at DATE NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_accounts_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_accounts_branch FOREIGN KEY (branch_id) REFERENCES branches(branch_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    INDEX idx_accounts_user (user_id),
    INDEX idx_accounts_branch (branch_id),
    INDEX idx_accounts_status (account_status),
    INDEX idx_accounts_type (account_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- MODULE 3: FUNDS TRANSFER (beneficiaries, transactions)
-- ============================================================================

CREATE TABLE beneficiaries (
    beneficiary_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    nickname VARCHAR(60) NULL,
    beneficiary_name VARCHAR(120) NOT NULL,
    account_number VARCHAR(20) NOT NULL,
    bank_name VARCHAR(100) NOT NULL,
    ifsc_code CHAR(11) NOT NULL,
    transfer_type ENUM('INTRABANK', 'INTERBANK') NOT NULL DEFAULT 'INTERBANK',
    daily_limit DECIMAL(12, 2) NOT NULL DEFAULT 100000.00,
    cooling_ends_at DATETIME NOT NULL,
    is_verified BOOLEAN NOT NULL DEFAULT TRUE,
    status ENUM('COOLING', 'ACTIVE', 'BLOCKED') NOT NULL DEFAULT 'ACTIVE',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_beneficiaries_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT uq_user_beneficiary_account UNIQUE (user_id, account_number, ifsc_code),
    INDEX idx_beneficiaries_user (user_id),
    INDEX idx_beneficiaries_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE transactions (
    transaction_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    account_id INT NOT NULL,
    counterparty_account_id INT NULL,
    beneficiary_id INT NULL,
    reference_utr VARCHAR(30) NOT NULL UNIQUE,
    transaction_type ENUM('DEBIT', 'CREDIT') NOT NULL,
    channel ENUM('IMPS', 'NEFT', 'RTGS', 'UPI', 'INTERNAL', 'BILL_PAY', 'LOAN_DISBURSAL', 'LOAN_EMI', 'INVESTMENT') NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    balance_after DECIMAL(15, 2) NOT NULL,
    currency CHAR(3) NOT NULL DEFAULT 'INR',
    description VARCHAR(255) NOT NULL,
    remarks VARCHAR(255) NULL,
    status ENUM('PENDING', 'SUCCESS', 'FAILED', 'REVERSED', 'FLAGGED') NOT NULL DEFAULT 'SUCCESS',
    is_flagged BOOLEAN NOT NULL DEFAULT FALSE,
    initiated_ip VARCHAR(45) NULL,
    transaction_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_tx_account FOREIGN KEY (account_id) REFERENCES bank_accounts(account_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_tx_counterparty FOREIGN KEY (counterparty_account_id) REFERENCES bank_accounts(account_id) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_tx_beneficiary FOREIGN KEY (beneficiary_id) REFERENCES beneficiaries(beneficiary_id) ON DELETE SET NULL ON UPDATE CASCADE,
    INDEX idx_tx_account_date (account_id, transaction_date),
    INDEX idx_tx_counterparty (counterparty_account_id),
    INDEX idx_tx_beneficiary (beneficiary_id),
    INDEX idx_tx_channel_status (channel, status),
    INDEX idx_tx_flagged (is_flagged)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- MODULE 4: BILL PAYMENT (biller_directory, customer_billers, bill_payments)
-- ============================================================================

CREATE TABLE biller_directory (
    biller_id INT AUTO_INCREMENT PRIMARY KEY,
    biller_code VARCHAR(30) NOT NULL UNIQUE,
    biller_name VARCHAR(120) NOT NULL UNIQUE,
    category ENUM('ELECTRICITY', 'WATER', 'PIPED_GAS', 'BROADBAND', 'DTH', 'MOBILE_POSTPAID', 'CREDIT_CARD', 'INSURANCE') NOT NULL,
    coverage_state VARCHAR(60) NOT NULL DEFAULT 'PAN_INDIA',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_biller_category (category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE customer_billers (
    customer_biller_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    biller_id INT NOT NULL,
    consumer_number VARCHAR(50) NOT NULL,
    short_name VARCHAR(60) NULL,
    autopay_enabled BOOLEAN NOT NULL DEFAULT FALSE,
    autopay_max_limit DECIMAL(10, 2) NULL,
    preferred_account_id INT NULL,
    status ENUM('ACTIVE', 'PAUSED', 'REMOVED') NOT NULL DEFAULT 'ACTIVE',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_custbiller_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_custbiller_biller FOREIGN KEY (biller_id) REFERENCES biller_directory(biller_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_custbiller_account FOREIGN KEY (preferred_account_id) REFERENCES bank_accounts(account_id) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT uq_user_biller_consumer UNIQUE (user_id, biller_id, consumer_number),
    INDEX idx_custbiller_user (user_id),
    INDEX idx_custbiller_biller (biller_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE bill_payments (
    bill_payment_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_biller_id INT NOT NULL,
    account_id INT NOT NULL,
    transaction_id BIGINT NULL,
    bbps_ref_no VARCHAR(35) NOT NULL UNIQUE,
    bill_period VARCHAR(30) NOT NULL,
    bill_amount DECIMAL(12, 2) NOT NULL,
    convenience_fee DECIMAL(8, 2) NOT NULL DEFAULT 0.00,
    total_paid DECIMAL(12, 2) NOT NULL,
    due_date DATE NOT NULL,
    payment_mode ENUM('MANUAL', 'AUTOPAY') NOT NULL DEFAULT 'MANUAL',
    payment_status ENUM('PENDING', 'PAID', 'FAILED', 'OVERDUE') NOT NULL DEFAULT 'PAID',
    paid_at DATETIME NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_billpay_custbiller FOREIGN KEY (customer_biller_id) REFERENCES customer_billers(customer_biller_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_billpay_account FOREIGN KEY (account_id) REFERENCES bank_accounts(account_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_billpay_tx FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id) ON DELETE SET NULL ON UPDATE CASCADE,
    INDEX idx_billpay_custbiller (customer_biller_id),
    INDEX idx_billpay_account (account_id),
    INDEX idx_billpay_status_due (payment_status, due_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- MODULE 5: LOAN MANAGEMENT (loan_products, loan_applications, loan_repayments)
-- ============================================================================

CREATE TABLE loan_products (
    loan_product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_code VARCHAR(30) NOT NULL UNIQUE,
    product_name VARCHAR(100) NOT NULL UNIQUE,
    loan_category ENUM('PERSONAL', 'HOME', 'VEHICLE', 'EDUCATION', 'BUSINESS', 'GOLD') NOT NULL,
    min_amount DECIMAL(15, 2) NOT NULL,
    max_amount DECIMAL(15, 2) NOT NULL,
    base_interest_rate DECIMAL(5, 2) NOT NULL,
    min_tenure_months INT NOT NULL,
    max_tenure_months INT NOT NULL,
    processing_fee_pct DECIMAL(4, 2) NOT NULL DEFAULT 1.00,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE loan_applications (
    loan_id INT AUTO_INCREMENT PRIMARY KEY,
    application_number VARCHAR(25) NOT NULL UNIQUE,
    user_id INT NOT NULL,
    disbursement_account_id INT NOT NULL,
    loan_product_id INT NOT NULL,
    reviewed_by_officer_id INT NULL,
    requested_amount DECIMAL(15, 2) NOT NULL,
    sanctioned_amount DECIMAL(15, 2) NULL,
    interest_rate DECIMAL(5, 2) NOT NULL,
    tenure_months INT NOT NULL,
    emi_amount DECIMAL(12, 2) NOT NULL,
    outstanding_principal DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
    applicant_annual_income DECIMAL(15, 2) NOT NULL,
    cibil_score INT NOT NULL,
    purpose_description VARCHAR(255) NOT NULL,
    officer_remarks VARCHAR(255) NULL,
    loan_status ENUM('APPLIED', 'UNDER_REVIEW', 'APPROVED', 'DISBURSED', 'REJECTED', 'CLOSED', 'DEFAULTED') NOT NULL DEFAULT 'APPLIED',
    applied_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    approved_at DATETIME NULL,
    disbursed_at DATETIME NULL,
    CONSTRAINT fk_loan_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_loan_account FOREIGN KEY (disbursement_account_id) REFERENCES bank_accounts(account_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_loan_product FOREIGN KEY (loan_product_id) REFERENCES loan_products(loan_product_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_loan_officer FOREIGN KEY (reviewed_by_officer_id) REFERENCES users(user_id) ON DELETE SET NULL ON UPDATE CASCADE,
    INDEX idx_loan_user (user_id),
    INDEX idx_loan_officer (reviewed_by_officer_id),
    INDEX idx_loan_status (loan_status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE loan_repayments (
    repayment_id INT AUTO_INCREMENT PRIMARY KEY,
    loan_id INT NOT NULL,
    transaction_id BIGINT NULL,
    installment_number INT NOT NULL,
    due_date DATE NOT NULL,
    emi_amount DECIMAL(12, 2) NOT NULL,
    principal_component DECIMAL(12, 2) NOT NULL,
    interest_component DECIMAL(12, 2) NOT NULL,
    penalty_amount DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    repayment_status ENUM('PENDING', 'PAID', 'OVERDUE', 'WAIVED') NOT NULL DEFAULT 'PENDING',
    paid_at DATETIME NULL,
    CONSTRAINT fk_repay_loan FOREIGN KEY (loan_id) REFERENCES loan_applications(loan_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_repay_tx FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT uq_loan_installment UNIQUE (loan_id, installment_number),
    INDEX idx_repay_loan_status (loan_id, repayment_status),
    INDEX idx_repay_due_date (due_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- MODULE 6: INVESTMENT SERVICES (investment_plans, investments)
-- ============================================================================

CREATE TABLE investment_plans (
    plan_id INT AUTO_INCREMENT PRIMARY KEY,
    plan_code VARCHAR(30) NOT NULL UNIQUE,
    plan_name VARCHAR(100) NOT NULL UNIQUE,
    investment_type ENUM('FIXED_DEPOSIT', 'RECURRING_DEPOSIT', 'MUTUAL_FUND', 'SOVEREIGN_GOLD_BOND', 'PPF') NOT NULL,
    min_investment DECIMAL(12, 2) NOT NULL,
    expected_return_rate DECIMAL(5, 2) NOT NULL,
    lock_in_months INT NOT NULL,
    premature_penalty_pct DECIMAL(4, 2) NOT NULL DEFAULT 1.00,
    risk_level ENUM('LOW', 'MODERATE', 'HIGH') NOT NULL DEFAULT 'LOW',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE investments (
    investment_id INT AUTO_INCREMENT PRIMARY KEY,
    certificate_number VARCHAR(30) NOT NULL UNIQUE,
    user_id INT NOT NULL,
    funding_account_id INT NOT NULL,
    plan_id INT NOT NULL,
    principal_amount DECIMAL(15, 2) NOT NULL,
    monthly_installment DECIMAL(12, 2) NULL,
    interest_rate DECIMAL(5, 2) NOT NULL,
    tenure_months INT NOT NULL,
    projected_maturity_amount DECIMAL(15, 2) NOT NULL,
    start_date DATE NOT NULL,
    maturity_date DATE NOT NULL,
    auto_renew BOOLEAN NOT NULL DEFAULT FALSE,
    investment_status ENUM('ACTIVE', 'MATURED', 'PREMATURE_CLOSED', 'CANCELLED') NOT NULL DEFAULT 'ACTIVE',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_inv_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_inv_account FOREIGN KEY (funding_account_id) REFERENCES bank_accounts(account_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_inv_plan FOREIGN KEY (plan_id) REFERENCES investment_plans(plan_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    INDEX idx_inv_user (user_id),
    INDEX idx_inv_account (funding_account_id),
    INDEX idx_inv_status_maturity (investment_status, maturity_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- MODULE 7: CUSTOMER SUPPORT (support_tickets, ticket_messages)
-- ============================================================================

CREATE TABLE support_tickets (
    ticket_id INT AUTO_INCREMENT PRIMARY KEY,
    ticket_number VARCHAR(25) NOT NULL UNIQUE,
    user_id INT NOT NULL,
    assigned_officer_id INT NULL,
    related_transaction_id BIGINT NULL,
    category ENUM('DISPUTED_TRANSACTION', 'ACCOUNT_ISSUE', 'FUNDS_TRANSFER', 'BILL_PAYMENT', 'LOAN_QUERY', 'INVESTMENT_QUERY', 'KYC_UPDATE', 'TECHNICAL_ISSUE') NOT NULL,
    priority ENUM('LOW', 'MEDIUM', 'HIGH', 'CRITICAL') NOT NULL DEFAULT 'MEDIUM',
    subject VARCHAR(160) NOT NULL,
    description TEXT NOT NULL,
    ticket_status ENUM('OPEN', 'IN_PROGRESS', 'RESOLVED', 'CLOSED') NOT NULL DEFAULT 'OPEN',
    resolution_notes VARCHAR(255) NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    resolved_at DATETIME NULL,
    CONSTRAINT fk_ticket_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_ticket_officer FOREIGN KEY (assigned_officer_id) REFERENCES users(user_id) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_ticket_tx FOREIGN KEY (related_transaction_id) REFERENCES transactions(transaction_id) ON DELETE SET NULL ON UPDATE CASCADE,
    INDEX idx_ticket_user (user_id),
    INDEX idx_ticket_officer (assigned_officer_id),
    INDEX idx_ticket_status_priority (ticket_status, priority)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE ticket_messages (
    message_id INT AUTO_INCREMENT PRIMARY KEY,
    ticket_id INT NOT NULL,
    sender_user_id INT NOT NULL,
    message_body TEXT NOT NULL,
    is_internal_note BOOLEAN NOT NULL DEFAULT FALSE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_msg_ticket FOREIGN KEY (ticket_id) REFERENCES support_tickets(ticket_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_msg_sender FOREIGN KEY (sender_user_id) REFERENCES users(user_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    INDEX idx_msg_ticket (ticket_id),
    INDEX idx_msg_sender (sender_user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- MODULE 8: SECURITY AND COMPLIANCE (kyc_documents, security_audit_logs)
-- ============================================================================

CREATE TABLE kyc_documents (
    kyc_doc_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    verified_by_officer_id INT NULL,
    document_type ENUM('PAN_CARD', 'AADHAAR_CARD', 'PASSPORT', 'DRIVING_LICENSE', 'VOTER_ID', 'SALARY_SLIP') NOT NULL,
    document_number_masked VARCHAR(30) NOT NULL,
    file_path VARCHAR(255) NOT NULL,
    verification_status ENUM('PENDING', 'VERIFIED', 'REJECTED') NOT NULL DEFAULT 'PENDING',
    rejection_reason VARCHAR(255) NULL,
    uploaded_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    verified_at DATETIME NULL,
    CONSTRAINT fk_kyc_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_kyc_officer FOREIGN KEY (verified_by_officer_id) REFERENCES users(user_id) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT uq_user_doctype UNIQUE (user_id, document_type),
    INDEX idx_kyc_user (user_id),
    INDEX idx_kyc_status (verification_status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE security_audit_logs (
    audit_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NULL,
    event_category ENUM('AUTH_LOGIN', 'AUTH_FAILED', 'ACCOUNT_LOCK', 'PASSWORD_CHANGE', 'HIGH_VALUE_TX', 'KYC_REVIEW', 'ACCOUNT_STATUS_CHANGE', 'ROLE_CHANGE', 'DATA_EXPORT') NOT NULL,
    severity ENUM('INFO', 'WARNING', 'CRITICAL') NOT NULL DEFAULT 'INFO',
    ip_address VARCHAR(45) NOT NULL,
    user_agent VARCHAR(255) NOT NULL,
    resource_target VARCHAR(100) NULL,
    event_description VARCHAR(255) NOT NULL,
    is_suspicious BOOLEAN NOT NULL DEFAULT FALSE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_audit_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL ON UPDATE CASCADE,
    INDEX idx_audit_user (user_id),
    INDEX idx_audit_category_severity (event_category, severity),
    INDEX idx_audit_suspicious_date (is_suspicious, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- MODULE 9: NOTIFICATION AND ALERTS (notifications)
-- ============================================================================

CREATE TABLE notifications (
    notification_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    notification_type ENUM('TRANSACTION', 'SECURITY', 'BILL_REMINDER', 'LOAN_ALERT', 'INVESTMENT_UPDATE', 'SUPPORT_UPDATE') NOT NULL,
    priority ENUM('NORMAL', 'HIGH', 'CRITICAL') NOT NULL DEFAULT 'NORMAL',
    title VARCHAR(140) NOT NULL,
    message VARCHAR(255) NOT NULL,
    channel ENUM('IN_APP', 'EMAIL', 'SMS') NOT NULL DEFAULT 'IN_APP',
    is_read BOOLEAN NOT NULL DEFAULT FALSE,
    read_at DATETIME NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_notif_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX idx_notif_user_read (user_id, is_read),
    INDEX idx_notif_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- MODULE 10: DASHBOARD AND REPORTING (report_exports)
-- ============================================================================

CREATE TABLE report_exports (
    report_id INT AUTO_INCREMENT PRIMARY KEY,
    generated_by_user_id INT NOT NULL,
    report_type ENUM('ACCOUNT_STATEMENT', 'TAX_CERTIFICATE', 'LOAN_AMORTIZATION', 'BRANCH_LIQUIDITY', 'COMPLIANCE_AUDIT', 'PORTFOLIO_SUMMARY') NOT NULL,
    file_format ENUM('PDF', 'CSV', 'XLSX') NOT NULL DEFAULT 'PDF',
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    filter_summary VARCHAR(255) NULL,
    file_path VARCHAR(255) NOT NULL,
    generated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_report_user FOREIGN KEY (generated_by_user_id) REFERENCES users(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX idx_report_user_date (generated_by_user_id, generated_at),
    INDEX idx_report_type (report_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

SET FOREIGN_KEY_CHECKS = 1;
