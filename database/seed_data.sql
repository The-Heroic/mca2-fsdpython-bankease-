-- ============================================================================
-- Project: P18 | BankEase - NextGen Net Banking Application
-- File:    database/seed_data.sql
-- Purpose: Realistic Indian-context sample data (2024-2026, INR amounts)
--          Master tables: 10-15 rows | Transaction tables: 55-75 rows
--          Includes Admin, Bank Officer, Customer & Auditor roles with
--          hashed placeholder passwords, plus 5 validation edge-case records.
-- ============================================================================

USE bankease_db;
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------------------------------------------------------
-- Table: roles (4 rows)
-- ----------------------------------------------------------------------------
INSERT INTO roles (role_id, role_code, role_name, description, created_at) VALUES
  (1, 'ADMIN', 'System Administrator', 'Full system configuration, user role management, and compliance oversight', '2024-01-01 09:00:00'),
  (2, 'BANK_OFFICER', 'Bank Officer', 'Branch operations, KYC verification, loan sanctioning, and ticket resolution', '2024-01-01 09:05:00'),
  (3, 'CUSTOMER', 'Retail / Corporate Customer', 'Standard net banking access for accounts, transfers, bills, loans, and investments', '2024-01-01 09:10:00'),
  (4, 'AUDITOR', 'Compliance & Risk Auditor', 'Read-only access to security audit trails, flagged transactions, and regulatory reports', '2024-01-01 09:15:00');

-- ----------------------------------------------------------------------------
-- Table: branches (12 rows)
-- ----------------------------------------------------------------------------
INSERT INTO branches (branch_id, ifsc_code, branch_name, address_line, city, state, pincode, contact_phone, created_at) VALUES
  (1, 'BNKE0000001', 'Connaught Place Main Branch', 'Block A, Inner Circle, Connaught Place', 'New Delhi', 'Delhi', '110001', '+91-1123415001', '2024-01-02 10:00:00'),
  (2, 'BNKE0000002', 'Noida Sector 62 IT Hub', 'Plot C-20, Sector 62', 'Noida', 'Uttar Pradesh', '201309', '+91-1202405002', '2024-01-02 10:05:00'),
  (3, 'BNKE0000003', 'Ghaziabad Crossing Republik', 'NH-24, Dundahera, Crossing Republik', 'Ghaziabad', 'Uttar Pradesh', '201009', '+91-1202845003', '2024-01-02 10:10:00'),
  (4, 'BNKE0000004', 'Mumbai Nariman Point Corporate', 'Maker Chambers IV, Nariman Point', 'Mumbai', 'Maharashtra', '400021', '+91-2222845004', '2024-01-02 10:15:00'),
  (5, 'BNKE0000005', 'Bengaluru Indiranagar 100Ft Rd', '742, 100 Feet Road, Indiranagar', 'Bengaluru', 'Karnataka', '560038', '+91-8025215005', '2024-01-02 10:20:00'),
  (6, 'BNKE0000006', 'Hyderabad HITEC City Cyberabad', 'Madhapur Main Road, HITEC City', 'Hyderabad', 'Telangana', '500081', '+91-4023115006', '2024-01-02 10:25:00'),
  (7, 'BNKE0000007', 'Chennai Anna Salai Mount Rd', '148, Anna Salai, Teynampet', 'Chennai', 'Tamil Nadu', '600018', '+91-4424345007', '2024-01-02 10:30:00'),
  (8, 'BNKE0000008', 'Pune Hinjewadi Rajiv Gandhi Park', 'Phase 1, Hinjewadi IT Park', 'Pune', 'Maharashtra', '411057', '+91-2022935008', '2024-01-02 10:35:00'),
  (9, 'BNKE0000009', 'Kolkata Park Street Metro', '55, Park Street, Taltala', 'Kolkata', 'West Bengal', '700016', '+91-3322295009', '2024-01-02 10:40:00'),
  (10, 'BNKE0000010', 'Jaipur Malviya Nagar Plaza', 'D-Block, Malviya Nagar', 'Jaipur', 'Rajasthan', '302017', '+91-1412525010', '2024-01-02 10:45:00'),
  (11, 'BNKE0000011', 'Lucknow Gomti Nagar Vibhuti Khand', 'TC-14, Vibhuti Khand, Gomti Nagar', 'Lucknow', 'Uttar Pradesh', '226010', '+91-5222725011', '2024-01-02 10:50:00'),
  (12, 'BNKE0000012', 'Ahmedabad SG Highway Prahladnagar', 'Corporate Road, Prahladnagar', 'Ahmedabad', 'Gujarat', '380015', '+91-7926935012', '2024-01-02 10:55:00');

-- ----------------------------------------------------------------------------
-- Table: users (15 rows)
-- ----------------------------------------------------------------------------
INSERT INTO users (user_id, role_id, home_branch_id, username, email, phone_number, password_hash, full_name, date_of_birth, pan_number, aadhaar_last4, address_line, city, state, pincode, kyc_status, is_active, is_locked, failed_login_attempts, last_login_at, created_at, updated_at) VALUES
  (1, 1, 1, 'admin_rajesh', 'rajesh.verma@bankease.in', '+91-9810010001', 'pbkdf2_sha256$600000$bankeaseSalt2026$placeholderHashedPasswordNotReal9988776655=', 'Rajesh Kumar Verma', '1982-04-15', 'AAAPV1234A', '4411', '12, Hailey Road, Connaught Place', 'New Delhi', 'Delhi', '110001', 'VERIFIED', 1, 0, 0, '2026-10-15 09:30:00', '2024-01-05 10:00:00', '2026-10-15 09:30:00'),
  (2, 2, 2, 'officer_priya', 'priya.nair@bankease.in', '+91-9810010002', 'pbkdf2_sha256$600000$bankeaseSalt2026$placeholderHashedPasswordNotReal9988776655=', 'Priya Krishnan Nair', '1988-08-22', 'ABCPN2345B', '8822', 'B-104, Lotus Boulevard, Sector 100', 'Noida', 'Uttar Pradesh', '201304', 'VERIFIED', 1, 0, 0, '2026-10-18 10:15:00', '2024-01-06 10:00:00', '2026-10-18 10:15:00'),
  (3, 2, 3, 'officer_amit', 'amit.tiwari@bankease.in', '+91-9810010003', 'pbkdf2_sha256$600000$bankeaseSalt2026$placeholderHashedPasswordNotReal9988776655=', 'Amitabh Shankar Tiwari', '1985-11-10', 'ACDPT3456C', '5533', 'Tower 5, Panchsheel Wellington, Crossing Republik', 'Ghaziabad', 'Uttar Pradesh', '201009', 'VERIFIED', 1, 0, 0, '2026-10-19 11:00:00', '2024-01-06 11:00:00', '2026-10-19 11:00:00'),
  (4, 4, 4, 'auditor_meera', 'meera.deshmukh@bankease.in', '+91-9820010004', 'pbkdf2_sha256$600000$bankeaseSalt2026$placeholderHashedPasswordNotReal9988776655=', 'Meera Sanjay Deshmukh', '1984-02-19', 'ADEPD4567D', '9944', '401, Sea View Apartments, Worli', 'Mumbai', 'Maharashtra', '400018', 'VERIFIED', 1, 0, 0, '2026-10-12 16:00:00', '2024-01-07 09:30:00', '2026-10-12 16:00:00'),
  (5, 3, 2, 'aarav_gupta', 'aarav.gupta@gmail.com', '+91-9811122001', 'pbkdf2_sha256$600000$bankeaseSalt2026$placeholderHashedPasswordNotReal9988776655=', 'Aarav Siddharth Gupta', '1996-05-14', 'AEFPG5678E', '1122', 'C-88, Sector 50', 'Noida', 'Uttar Pradesh', '201301', 'VERIFIED', 1, 0, 0, '2026-10-20 14:20:00', '2024-02-10 11:15:00', '2026-10-20 14:20:00'),
  (6, 3, 3, 'ananya_singh', 'ananya.singh@outlook.com', '+91-9811122002', 'pbkdf2_sha256$600000$bankeaseSalt2026$placeholderHashedPasswordNotReal9988776655=', 'Ananya Pratap Singh', '1998-09-03', 'AFGPS6789F', '2233', '78, Kavi Nagar, Block C', 'Ghaziabad', 'Uttar Pradesh', '201002', 'VERIFIED', 1, 0, 0, '2026-10-21 08:45:00', '2024-02-15 12:30:00', '2026-10-21 08:45:00'),
  (7, 3, 5, 'karthik_reddy', 'karthik.reddy@yahoo.co.in', '+91-9845033003', 'pbkdf2_sha256$600000$bankeaseSalt2026$placeholderHashedPasswordNotReal9988776655=', 'Karthik Venkat Reddy', '1993-12-28', 'AGHPR7890G', '3344', '22, 12th Main, HAL 2nd Stage, Indiranagar', 'Bengaluru', 'Karnataka', '560008', 'VERIFIED', 1, 0, 0, '2026-10-18 19:10:00', '2024-03-01 15:00:00', '2026-10-18 19:10:00'),
  (8, 3, 4, 'sneha_kulkarni', 'sneha.kulkarni@gmail.com', '+91-9822044004', 'pbkdf2_sha256$600000$bankeaseSalt2026$placeholderHashedPasswordNotReal9988776655=', 'Sneha Mandar Kulkarni', '1995-07-09', 'AHIPK8901H', '4455', '15, Prabhat Road, Deccan Gymkhana', 'Pune', 'Maharashtra', '411004', 'VERIFIED', 1, 0, 0, '2026-10-17 17:40:00', '2024-03-12 10:20:00', '2026-10-17 17:40:00'),
  (9, 3, 6, 'vikram_choudhary', 'vikram.choudhary@gmail.com', '+91-9829055005', 'pbkdf2_sha256$600000$bankeaseSalt2026$placeholderHashedPasswordNotReal9988776655=', 'Vikramaditya Singh Choudhary', '1990-01-25', 'AIJPC9012J', '5566', 'Plot 45, Vaishali Nagar', 'Jaipur', 'Rajasthan', '302021', 'VERIFIED', 1, 0, 0, '2026-10-16 12:05:00', '2024-04-05 14:10:00', '2026-10-16 12:05:00'),
  (10, 3, 11, 'zoya_khan', 'zoya.khan@gmail.com', '+91-9839066006', 'pbkdf2_sha256$600000$bankeaseSalt2026$placeholderHashedPasswordNotReal9988776655=', 'Zoya Tariq Khan', '1997-03-30', 'AJKPK0123K', '6677', '4/112, Vishal Khand, Gomti Nagar', 'Lucknow', 'Uttar Pradesh', '226010', 'VERIFIED', 1, 0, 0, '2026-10-19 20:55:00', '2024-04-18 16:45:00', '2026-10-19 20:55:00'),
  (11, 3, NULL, 'edge_null_optional', 'null.optional@testbankease.in', '+91-9900099001', 'pbkdf2_sha256$600000$bankeaseSalt2026$placeholderHashedPasswordNotReal9988776655=', 'Niharika Minimal Profile', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'PENDING', 1, 0, 0, NULL, '2025-01-10 10:00:00', '2025-01-10 10:00:00'),
  (12, 3, 5, 'edge_maxlen_text', 'maxlen.user@testbankease.in', '+91-9900099002', 'pbkdf2_sha256$600000$bankeaseSalt2026$placeholderHashedPasswordNotReal9988776655=', 'Sri Venkata Subrahmanya Rajeshwara Rao Parameshwaran IyerKrishnamurthy Balasubramanian Venkateshwaran Chidambaram Pillai', '1991-06-18', 'AMXLN9999M', '7788', 'Flat No 402-B, Tower 19, Shriram Suhana Greenfield Ultra Luxury Integrated Township, Near Yelahanka Airforce Station Bypass Road, Avalahalli Main Cross, Doddaballapur Highway, North Bengaluru Urban District, Karnataka State, Bharat PinCode 560064 Landmark', 'Bengaluru', 'Karnataka', '560064', 'VERIFIED', 1, 0, 0, '2026-09-01 11:11:11', '2025-02-01 09:00:00', '2026-09-01 11:11:11'),
  (13, 3, 1, 'rohit_sharma_del', 'rohit.sharma.del@testbankease.in', '+91-9900099003', 'pbkdf2_sha256$600000$bankeaseSalt2026$placeholderHashedPasswordNotReal9988776655=', 'Rohit Kumar Sharma', '1994-11-05', 'AROHS1111R', '1212', 'H-12, Lajpat Nagar IV', 'New Delhi', 'Delhi', '110024', 'VERIFIED', 1, 0, 0, '2026-10-05 15:30:00', '2025-03-15 10:30:00', '2026-10-05 15:30:00'),
  (14, 3, 1, 'rohit_sharma_ncr', 'rohit.sharma.ncr@testbankease.in', '+91-9900099004', 'pbkdf2_sha256$600000$bankeaseSalt2026$placeholderHashedPasswordNotReal9988776655=', 'Rohit Kumar  Sharma', '1994-11-05', 'AROHS1112R', '1213', 'H-12A, Lajpat Nagar IV', 'New Delhi', 'Delhi', '110024', 'VERIFIED', 1, 0, 0, '2026-10-06 16:30:00', '2025-03-16 11:30:00', '2026-10-06 16:30:00'),
  (15, 3, 4, 'edge_locked_user', 'locked.fraudtest@testbankease.in', '+91-9900099005', 'pbkdf2_sha256$600000$bankeaseSalt2026$placeholderHashedPasswordNotReal9988776655=', 'Suresh Chintamani Sawant', '1989-08-12', 'ALOCK5555Z', '9090', 'Room 14, Chawl 3, Dadar East', 'Mumbai', 'Maharashtra', '400014', 'REJECTED', 0, 1, 5, '2026-08-20 23:59:59', '2025-05-20 08:00:00', '2026-08-20 23:59:59');

-- ----------------------------------------------------------------------------
-- Table: bank_accounts (15 rows)
-- ----------------------------------------------------------------------------
INSERT INTO bank_accounts (account_id, user_id, branch_id, account_number, account_type, currency, balance, minimum_balance, daily_transfer_limit, interest_rate, account_status, nominee_name, nominee_relation, opened_at, closed_at, created_at, updated_at) VALUES
  (1, 5, 2, '180002000001', 'SAVINGS', 'INR', '245800.50', '10000.00', '500000.00', '3.50', 'ACTIVE', 'Meena Gupta', 'Mother', '2024-02-12', NULL, '2024-02-12 10:00:00', '2026-10-20 14:20:00'),
  (2, 5, 2, '180002000002', 'CURRENT', 'INR', '890500.00', '25000.00', '1000000.00', '0.00', 'ACTIVE', 'Siddharth Gupta', 'Father', '2024-06-01', NULL, '2024-06-01 11:00:00', '2026-10-18 11:00:00'),
  (3, 6, 3, '180003000003', 'SAVINGS', 'INR', '128450.75', '5000.00', '200000.00', '3.50', 'ACTIVE', 'Pratap Singh', 'Father', '2024-02-16', NULL, '2024-02-16 09:30:00', '2026-10-21 08:45:00'),
  (4, 6, 3, '180003000004', 'SALARY', 'INR', '76200.00', '0.00', '200000.00', '3.50', 'ACTIVE', NULL, NULL, '2025-01-10', NULL, '2025-01-10 12:00:00', '2026-10-01 10:00:00'),
  (5, 7, 5, '180005000005', 'SAVINGS', 'INR', '540200.00', '10000.00', '500000.00', '3.75', 'ACTIVE', 'Lakshmi Reddy', 'Spouse', '2024-03-02', NULL, '2024-03-02 14:00:00', '2026-10-18 19:10:00'),
  (6, 7, 5, '180005000006', 'SALARY', 'INR', '195300.25', '0.00', '300000.00', '3.50', 'ACTIVE', 'Lakshmi Reddy', 'Spouse', '2024-09-15', NULL, '2024-09-15 10:30:00', '2026-10-15 09:00:00'),
  (7, 8, 8, '180008000007', 'SAVINGS', 'INR', '312000.00', '5000.00', '250000.00', '3.50', 'ACTIVE', 'Mandar Kulkarni', 'Spouse', '2024-03-14', NULL, '2024-03-14 11:45:00', '2026-10-17 17:40:00'),
  (8, 9, 10, '180010000008', 'CURRENT', 'INR', '1450000.00', '25000.00', '2000000.00', '0.00', 'ACTIVE', 'Rajeshwari Choudhary', 'Spouse', '2024-04-06', NULL, '2024-04-06 15:20:00', '2026-10-16 12:05:00'),
  (9, 9, 10, '180010000009', 'SAVINGS', 'INR', '88900.50', '5000.00', '200000.00', '3.50', 'ACTIVE', 'Rajeshwari Choudhary', 'Spouse', '2024-08-20', NULL, '2024-08-20 13:10:00', '2026-10-10 10:00:00'),
  (10, 10, 11, '180011000010', 'SAVINGS', 'INR', '164500.00', '5000.00', '200000.00', '3.50', 'ACTIVE', 'Tariq Khan', 'Father', '2024-04-20', NULL, '2024-04-20 16:00:00', '2026-10-19 20:55:00'),
  (11, 11, 1, '180001000011', 'SAVINGS', 'INR', '0.00', '1000.00', '50000.00', '3.50', 'PENDING_KYC', NULL, NULL, '2025-01-10', NULL, '2025-01-10 10:05:00', '2025-01-10 10:05:00'),
  (12, 12, 5, '180005000012', 'SAVINGS', 'INR', '675000.00', '10000.00', '500000.00', '3.75', 'ACTIVE', 'Sri Venkata Subrahmanya Rajeshwara Rao Parameshwaran IyerKrishnamurthy Balasubra', 'Brother', '2025-02-02', NULL, '2025-02-02 10:00:00', '2026-09-01 11:11:11'),
  (13, 13, 1, '180001000013', 'SAVINGS', 'INR', '92400.00', '5000.00', '200000.00', '3.50', 'ACTIVE', 'Kavita Sharma', 'Spouse', '2025-03-16', NULL, '2025-03-16 10:00:00', '2026-10-05 15:30:00'),
  (14, 14, 1, '180001000014', 'SAVINGS', 'INR', '94200.00', '5000.00', '200000.00', '3.50', 'ACTIVE', 'Kavita R. Sharma', 'Spouse', '2025-03-17', NULL, '2025-03-17 10:00:00', '2026-10-06 16:30:00'),
  (15, 15, 4, '180004000015', 'SAVINGS', 'INR', '1250.00', '5000.00', '50000.00', '3.50', 'FROZEN', NULL, NULL, '2025-05-21', NULL, '2025-05-21 09:00:00', '2026-08-20 23:59:59');

-- ----------------------------------------------------------------------------
-- Table: beneficiaries (14 rows)
-- ----------------------------------------------------------------------------
INSERT INTO beneficiaries (beneficiary_id, user_id, nickname, beneficiary_name, account_number, bank_name, ifsc_code, transfer_type, daily_limit, cooling_ends_at, is_verified, status, created_at) VALUES
  (1, 5, 'Ananya Sister', 'Ananya Pratap Singh', '180003000003', 'BankEase Ltd', 'BNKE0000003', 'INTRABANK', '200000.00', '2024-02-15 10:00:00', 1, 'ACTIVE', '2024-02-14 10:00:00'),
  (2, 5, 'Ramesh Landlord', 'Ramesh Chandra Agarwal', '004501552310', 'State Bank of India', 'SBIN0001234', 'INTERBANK', '100000.00', '2024-03-01 12:00:00', 1, 'ACTIVE', '2024-02-28 12:00:00'),
  (3, 5, 'CA Office Vendor', 'Mehta & Associates LLP', '50200044112288', 'HDFC Bank', 'HDFC0000240', 'INTERBANK', '500000.00', '2024-06-10 09:00:00', 1, 'ACTIVE', '2024-06-09 09:00:00'),
  (4, 6, 'Aarav Brother', 'Aarav Siddharth Gupta', '180002000001', 'BankEase Ltd', 'BNKE0000002', 'INTRABANK', '150000.00', '2024-02-20 15:00:00', 1, 'ACTIVE', '2024-02-19 15:00:00'),
  (5, 6, 'Mom Savings', 'Sunita Devi Singh', '339802010045112', 'Union Bank of India', 'UBIN0533980', 'INTERBANK', '100000.00', '2024-04-02 10:00:00', 1, 'ACTIVE', '2024-04-01 10:00:00'),
  (6, 7, 'Sneha Pune', 'Sneha Mandar Kulkarni', '180008000007', 'BankEase Ltd', 'BNKE0000008', 'INTRABANK', '250000.00', '2024-03-20 18:00:00', 1, 'ACTIVE', '2024-03-19 18:00:00'),
  (7, 7, 'Prestige Maintenance', 'Prestige Estates Welfare Assoc', '000905028877', 'ICICI Bank', 'ICIC0000009', 'INTERBANK', '100000.00', '2024-05-05 11:00:00', 1, 'ACTIVE', '2024-05-04 11:00:00'),
  (8, 8, 'Vikram Supplier', 'Vikramaditya Singh Choudhary', '180010000008', 'BankEase Ltd', 'BNKE0000010', 'INTRABANK', '250000.00', '2024-05-15 14:00:00', 1, 'ACTIVE', '2024-05-14 14:00:00'),
  (9, 8, 'Mandar Joint', 'Mandar Vasant Kulkarni', '918010045672319', 'Axis Bank', 'UTIB0000037', 'INTERBANK', '200000.00', '2024-07-02 09:00:00', 1, 'ACTIVE', '2024-07-01 09:00:00'),
  (10, 9, 'Jaipur Marble Co', 'Aravali Stones & Marbles Pvt Ltd', '67120500001234', 'Bank of Baroda', 'BARB0JAIPUR', 'INTERBANK', '1000000.00', '2024-06-15 16:00:00', 1, 'ACTIVE', '2024-06-14 16:00:00'),
  (11, 10, 'Zoya Boutique Vendor', 'Awadh Chikankari Crafts', '4125002100098765', 'Punjab National Bank', 'PUNB0412500', 'INTERBANK', '150000.00', '2024-08-10 12:00:00', 1, 'ACTIVE', '2024-08-09 12:00:00'),
  (12, 12, 'Bengaluru Tech Park', 'Manyata Promoters Pvt Ltd', '50200088997766', 'HDFC Bank', 'HDFC0001206', 'INTERBANK', '300000.00', '2025-03-01 10:00:00', 1, 'ACTIVE', '2025-02-28 10:00:00'),
  (13, 13, 'Rohit Twin Test', 'Rohit Kumar  Sharma', '180001000014', 'BankEase Ltd', 'BNKE0000001', 'INTRABANK', '50000.00', '2026-11-18 18:00:00', 0, 'COOLING', '2026-11-18 10:00:00'),
  (14, 15, 'Suspicious Offshore', 'Unknown Shell Traders', '999888777666', 'Yes Bank', 'YESB0000001', 'INTERBANK', '50000.00', '2025-06-01 10:00:00', 0, 'BLOCKED', '2025-05-31 10:00:00');

-- ----------------------------------------------------------------------------
-- Table: biller_directory (12 rows)
-- ----------------------------------------------------------------------------
INSERT INTO biller_directory (biller_id, biller_code, biller_name, category, coverage_state, is_active, created_at) VALUES
  (1, 'UPPCL_NR', 'Uttar Pradesh Power Corporation Ltd (UPPCL)', 'ELECTRICITY', 'Uttar Pradesh', 1, '2024-01-03 10:00:00'),
  (2, 'BSES_RAJ', 'BSES Rajdhani Power Ltd', 'ELECTRICITY', 'Delhi', 1, '2024-01-03 10:05:00'),
  (3, 'BESCOM_KA', 'Bangalore Electricity Supply Company (BESCOM)', 'ELECTRICITY', 'Karnataka', 1, '2024-01-03 10:10:00'),
  (4, 'MAHADISCOM', 'Mahavitaran - Maharashtra State Electricity (MSEDCL)', 'ELECTRICITY', 'Maharashtra', 1, '2024-01-03 10:15:00'),
  (5, 'DJB_WATER', 'Delhi Jal Board (DJB)', 'WATER', 'Delhi', 1, '2024-01-03 10:20:00'),
  (6, 'BWSSB_WATER', 'Bangalore Water Supply and Sewerage Board', 'WATER', 'Karnataka', 1, '2024-01-03 10:25:00'),
  (7, 'IGL_PNG', 'Indraprastha Gas Limited (IGL PNG)', 'PIPED_GAS', 'Delhi NCR', 1, '2024-01-03 10:30:00'),
  (8, 'JIO_FIBER', 'JioFiber Postpaid Broadband', 'BROADBAND', 'PAN_INDIA', 1, '2024-01-03 10:35:00'),
  (9, 'AIRTEL_BB', 'Airtel Xstream Fiber Broadband', 'BROADBAND', 'PAN_INDIA', 1, '2024-01-03 10:40:00'),
  (10, 'TATA_PLAY', 'Tata Play DTH Recharge', 'DTH', 'PAN_INDIA', 1, '2024-01-03 10:45:00'),
  (11, 'SBI_CARD', 'SBI Card Bill Payment', 'CREDIT_CARD', 'PAN_INDIA', 1, '2024-01-03 10:50:00'),
  (12, 'LIC_INDIA', 'Life Insurance Corporation of India (LIC)', 'INSURANCE', 'PAN_INDIA', 1, '2024-01-03 10:55:00');

-- ----------------------------------------------------------------------------
-- Table: customer_billers (14 rows)
-- ----------------------------------------------------------------------------
INSERT INTO customer_billers (customer_biller_id, user_id, biller_id, consumer_number, short_name, autopay_enabled, autopay_max_limit, preferred_account_id, status, created_at) VALUES
  (1, 5, 1, '4012889011', 'Noida Home Electricity', 1, '8000.00', 1, 'ACTIVE', '2024-03-01 10:00:00'),
  (2, 5, 7, '7000192837', 'Noida Kitchen PNG', 1, '2500.00', 1, 'ACTIVE', '2024-03-01 10:15:00'),
  (3, 5, 8, '01204556677', 'Home JioFiber', 1, '1500.00', 1, 'ACTIVE', '2024-03-01 10:30:00'),
  (4, 6, 1, '4019881122', 'Ghaziabad Flat Power', 0, NULL, 3, 'ACTIVE', '2024-03-05 11:00:00'),
  (5, 6, 9, '01202889900', 'Airtel Broadband', 1, '1200.00', 3, 'ACTIVE', '2024-03-05 11:20:00'),
  (6, 7, 3, '8819200345', 'Indiranagar BESCOM', 1, '6000.00', 5, 'ACTIVE', '2024-04-01 09:00:00'),
  (7, 7, 6, 'BWSSB99812', 'Indiranagar Water', 0, NULL, 5, 'ACTIVE', '2024-04-01 09:15:00'),
  (8, 7, 11, '4321XXXXXXXX8899', 'Karthik SBI Elite Card', 0, NULL, 6, 'ACTIVE', '2024-04-10 14:00:00'),
  (9, 8, 4, '170029384756', 'Pune Home MSEDCL', 1, '5000.00', 7, 'ACTIVE', '2024-04-12 16:00:00'),
  (10, 8, 12, '981273645', 'LIC Jeevan Anand Policy', 1, '35000.00', 7, 'ACTIVE', '2024-04-12 16:30:00'),
  (11, 9, 10, '1009283746', 'Jaipur Home Tata Play', 1, '800.00', 9, 'ACTIVE', '2024-05-01 12:00:00'),
  (12, 10, 1, '4055667788', 'Lucknow Home Power', 0, NULL, 10, 'ACTIVE', '2024-05-10 17:00:00'),
  (13, 13, 2, '1029384756', 'Lajpat Nagar BSES', 0, NULL, 13, 'ACTIVE', '2025-04-01 10:00:00'),
  (14, 14, 5, 'DJB55443322', 'Lajpat Nagar Water', 0, NULL, 14, 'PAUSED', '2025-04-02 10:00:00');

-- ----------------------------------------------------------------------------
-- Table: loan_products (10 rows)
-- ----------------------------------------------------------------------------
INSERT INTO loan_products (loan_product_id, product_code, product_name, loan_category, min_amount, max_amount, base_interest_rate, min_tenure_months, max_tenure_months, processing_fee_pct, is_active, created_at) VALUES
  (1, 'LN_PERS_EXP', 'BankEase Express Personal Loan', 'PERSONAL', '50000.00', '2500000.00', '10.75', 12, 60, '1.50', 1, '2024-01-04 09:00:00'),
  (2, 'LN_PERS_SAL', 'Pre-Approved Salary Overdraft Loan', 'PERSONAL', '25000.00', '1000000.00', '10.25', 6, 48, '1.00', 1, '2024-01-04 09:10:00'),
  (3, 'LN_HOME_PRM', 'Griha Suvidha Prime Home Loan', 'HOME', '1000000.00', '50000000.00', '8.50', 60, 360, '0.50', 1, '2024-01-04 09:20:00'),
  (4, 'LN_HOME_TOP', 'Home Renovation & Top-Up Loan', 'HOME', '200000.00', '5000000.00', '8.90', 24, 180, '0.75', 1, '2024-01-04 09:30:00'),
  (5, 'LN_AUTO_NEW', 'BankEase Drive New Car Loan', 'VEHICLE', '300000.00', '10000000.00', '8.85', 12, 84, '0.50', 1, '2024-01-04 09:40:00'),
  (6, 'LN_AUTO_EV', 'Green Mobility Electric Vehicle Loan', 'VEHICLE', '100000.00', '5000000.00', '8.40', 12, 84, '0.25', 1, '2024-01-04 09:50:00'),
  (7, 'LN_EDU_IND', 'Vidya Shiksha Premier India Education Loan', 'EDUCATION', '100000.00', '4000000.00', '8.15', 24, 180, '0.00', 1, '2024-01-04 10:00:00'),
  (8, 'LN_EDU_ABR', 'Global Scholar Overseas Education Loan', 'EDUCATION', '1000000.00', '15000000.00', '9.25', 36, 180, '1.00', 1, '2024-01-04 10:10:00'),
  (9, 'LN_BIZ_MSME', 'Udyog MSME Working Capital Term Loan', 'BUSINESS', '500000.00', '25000000.00', '11.20', 12, 120, '1.25', 1, '2024-01-04 10:20:00'),
  (10, 'LN_GOLD_INS', 'Swarna Instant Gold Loan', 'GOLD', '25000.00', '2000000.00', '9.00', 6, 36, '0.50', 1, '2024-01-04 10:30:00');

-- ----------------------------------------------------------------------------
-- Table: loan_applications (12 rows)
-- ----------------------------------------------------------------------------
INSERT INTO loan_applications (loan_id, application_number, user_id, disbursement_account_id, loan_product_id, reviewed_by_officer_id, requested_amount, sanctioned_amount, interest_rate, tenure_months, emi_amount, outstanding_principal, applicant_annual_income, cibil_score, purpose_description, officer_remarks, loan_status, applied_at, approved_at, disbursed_at) VALUES
  (1, 'BNKLN202400001', 5, 1, 5, 2, '850000.00', '850000.00', '8.85', 60, '17583.00', '582400.00', '1850000.00', 782, 'Purchase of Hyundai Creta SX in Noida', 'CIBIL 782 verified, salary slips and ITR approved.', 'DISBURSED', '2024-05-02 11:00:00', '2024-05-05 15:00:00', '2024-05-06 10:30:00'),
  (2, 'BNKLN202400002', 6, 3, 1, 3, '300000.00', '300000.00', '10.75', 36, '9786.00', '142000.00', '960000.00', 756, 'Home interior modular kitchen work', 'Verified employment at TCS Noida.', 'DISBURSED', '2024-06-10 10:30:00', '2024-06-12 16:00:00', '2024-06-13 11:00:00'),
  (3, 'BNKLN202400003', 7, 5, 3, 2, '6500000.00', '6500000.00', '8.50', 240, '56408.00', '6120000.00', '3200000.00', 810, 'Purchase of 3BHK flat in Whitefield Bengaluru', 'Property legal opinion and valuation clear.', 'DISBURSED', '2024-07-01 09:45:00', '2024-07-08 14:30:00', '2024-07-10 10:00:00'),
  (4, 'BNKLN202400004', 8, 7, 6, 3, '1400000.00', '1400000.00', '8.40', 60, '28655.00', '1050000.00', '1600000.00', 774, 'Purchase of Tata Nexon EV Empowered', 'Green EV concession applied.', 'DISBURSED', '2024-08-12 12:15:00', '2024-08-14 17:00:00', '2024-08-15 11:00:00'),
  (5, 'BNKLN202400005', 9, 8, 9, 2, '4500000.00', '4500000.00', '11.20', 60, '98268.00', '3520000.00', '6800000.00', 765, 'CNC marble cutting machinery expansion', 'GST returns and audited balance sheet verified.', 'DISBURSED', '2024-09-05 14:00:00', '2024-09-09 16:30:00', '2024-09-10 12:00:00'),
  (6, 'BNKLN202400006', 10, 10, 7, 3, '600000.00', '600000.00', '8.15', 60, '12209.00', '465000.00', '1100000.00', 748, 'MCA tuition and hostel fees at ABES', 'Co-applicant father income verified.', 'DISBURSED', '2024-10-01 10:00:00', '2024-10-03 15:00:00', '2024-10-04 10:30:00'),
  (7, 'BNKLN202500007', 12, 12, 4, 2, '1200000.00', '1200000.00', '8.90', 60, '24852.00', '980000.00', '2900000.00', 795, 'Solar rooftop and terrace waterproofing', 'Approved under existing home customer scheme.', 'DISBURSED', '2025-03-10 11:00:00', '2025-03-12 14:00:00', '2025-03-13 09:30:00'),
  (8, 'BNKLN202500008', 5, 2, 10, 2, '200000.00', '200000.00', '9.00', 12, '17490.00', '0.00', '1850000.00', 788, 'Short-term working capital against gold ornaments', 'Closed early with zero outstanding.', 'CLOSED', '2025-01-15 10:00:00', '2025-01-15 13:00:00', '2025-01-15 15:00:00'),
  (9, 'BNKLN202600009', 13, 13, 1, 3, '450000.00', '450000.00', '10.75', 36, '14679.00', '450000.00', '1250000.00', 742, 'Family medical expenses and travel', 'Sanctioned, awaiting customer e-sign for disbursal.', 'APPROVED', '2026-10-01 11:30:00', '2026-10-04 16:00:00', NULL),
  (10, 'BNKLN202600010', 14, 14, 5, 2, '950000.00', NULL, '8.85', 60, '19651.00', '0.00', '1300000.00', 739, 'Purchase of Maruti Grand Vitara', 'Field verification of Lajpat Nagar address in progress.', 'UNDER_REVIEW', '2026-10-15 14:00:00', NULL, NULL),
  (11, 'BNKLN202600011', 6, 3, 8, NULL, '3500000.00', NULL, '9.25', 84, '56748.00', '0.00', '960000.00', 760, 'MS in Data Science overseas admission', NULL, 'APPLIED', '2026-11-10 09:30:00', NULL, NULL),
  (12, 'BNKLN202500012', 15, 15, 1, 2, '1500000.00', NULL, '10.75', 48, '38603.00', '0.00', '320000.00', 540, 'Unsecured personal cash requirement', 'Rejected due to low CIBIL (540), high FOIR, and KYC mismatch.', 'REJECTED', '2025-06-05 12:00:00', NULL, NULL);

-- ----------------------------------------------------------------------------
-- Table: investment_plans (10 rows)
-- ----------------------------------------------------------------------------
INSERT INTO investment_plans (plan_id, plan_code, plan_name, investment_type, min_investment, expected_return_rate, lock_in_months, premature_penalty_pct, risk_level, is_active, created_at) VALUES
  (1, 'FD_REG_1YR', 'BankEase Regular Fixed Deposit - 1 Year', 'FIXED_DEPOSIT', '10000.00', '6.80', 12, '1.00', 'LOW', 1, '2024-01-04 11:00:00'),
  (2, 'FD_MAX_3YR', 'BankEase WealthMax Fixed Deposit - 3 Years', 'FIXED_DEPOSIT', '25000.00', '7.25', 36, '1.00', 'LOW', 1, '2024-01-04 11:05:00'),
  (3, 'FD_TAX_5YR', 'Section 80C Tax Saver Fixed Deposit - 5 Years', 'FIXED_DEPOSIT', '10000.00', '7.10', 60, '0.00', 'LOW', 1, '2024-01-04 11:10:00'),
  (4, 'FD_SNR_2YR', 'Senior Citizen Samman FD - 2 Years', 'FIXED_DEPOSIT', '10000.00', '7.75', 24, '0.50', 'LOW', 1, '2024-01-04 11:15:00'),
  (5, 'RD_FLEX_1YR', 'Smart Goal Recurring Deposit - 12 Months', 'RECURRING_DEPOSIT', '1000.00', '6.70', 12, '1.00', 'LOW', 1, '2024-01-04 11:20:00'),
  (6, 'RD_PLUS_3YR', 'Sankalp Systematic Recurring Deposit - 36 Months', 'RECURRING_DEPOSIT', '2000.00', '7.00', 36, '1.00', 'LOW', 1, '2024-01-04 11:25:00'),
  (7, 'MF_NIFTY_50', 'BankEase Nifty 50 Index Direct Growth Fund', 'MUTUAL_FUND', '5000.00', '12.40', 0, '0.00', 'HIGH', 1, '2024-01-04 11:30:00'),
  (8, 'MF_BAL_ADV', 'BankEase Balanced Advantage Hybrid Fund', 'MUTUAL_FUND', '5000.00', '10.50', 12, '1.00', 'MODERATE', 1, '2024-01-04 11:35:00'),
  (9, 'SGB_2024_I', 'RBI Sovereign Gold Bond Series', 'SOVEREIGN_GOLD_BOND', '6000.00', '2.50', 96, '0.00', 'MODERATE', 1, '2024-01-04 11:40:00'),
  (10, 'PPF_GOV_15Y', 'Public Provident Fund (PPF) Scheme', 'PPF', '500.00', '7.10', 180, '1.00', 'LOW', 1, '2024-01-04 11:45:00');

-- ----------------------------------------------------------------------------
-- Table: investments (14 rows)
-- ----------------------------------------------------------------------------
INSERT INTO investments (investment_id, certificate_number, user_id, funding_account_id, plan_id, principal_amount, monthly_installment, interest_rate, tenure_months, projected_maturity_amount, start_date, maturity_date, auto_renew, investment_status, created_at) VALUES
  (1, 'BNKFD2024001', 5, 1, 2, '250000.00', NULL, '7.25', 36, '309850.00', '2024-04-01', '2027-04-01', 1, 'ACTIVE', '2024-04-01 10:30:00'),
  (2, 'BNKFD2024002', 5, 1, 3, '150000.00', NULL, '7.10', 60, '213200.00', '2024-07-15', '2029-07-15', 0, 'ACTIVE', '2024-07-15 11:00:00'),
  (3, 'BNKRD2024003', 6, 3, 5, '60000.00', '5000.00', '6.70', 12, '62190.00', '2024-05-01', '2025-05-01', 0, 'MATURED', '2024-05-01 09:30:00'),
  (4, 'BNKMF2024004', 6, 4, 7, '100000.00', NULL, '12.40', 36, '142000.00', '2025-02-10', '2028-02-10', 0, 'ACTIVE', '2025-02-10 14:00:00'),
  (5, 'BNKFD2024005', 7, 5, 2, '500000.00', NULL, '7.25', 36, '619700.00', '2024-06-01', '2027-06-01', 1, 'ACTIVE', '2024-06-01 12:00:00'),
  (6, 'BNKSGB202406', 7, 5, 9, '120000.00', NULL, '2.50', 96, '146000.00', '2024-08-01', '2032-08-01', 0, 'ACTIVE', '2024-08-01 15:00:00'),
  (7, 'BNKFD2024007', 8, 7, 1, '200000.00', NULL, '6.80', 12, '213950.00', '2024-05-10', '2025-05-10', 0, 'MATURED', '2024-05-10 10:15:00'),
  (8, 'BNKRD2025008', 8, 7, 6, '360000.00', '10000.00', '7.00', 36, '401250.00', '2025-01-05', '2028-01-05', 1, 'ACTIVE', '2025-01-05 11:20:00'),
  (9, 'BNKFD2024009', 9, 8, 2, '1000000.00', NULL, '7.25', 36, '1239400.00', '2024-09-01', '2027-09-01', 1, 'ACTIVE', '2024-09-01 16:00:00'),
  (10, 'BNKPPF202410', 10, 10, 10, '150000.00', NULL, '7.10', 180, '406820.00', '2024-06-20', '2039-06-20', 0, 'ACTIVE', '2024-06-20 13:45:00'),
  (11, 'BNKMF2025011', 10, 10, 8, '75000.00', NULL, '10.50', 24, '91800.00', '2025-04-10', '2027-04-10', 0, 'ACTIVE', '2025-04-10 10:00:00'),
  (12, 'BNKFD2025012', 12, 12, 4, '400000.00', NULL, '7.75', 24, '466100.00', '2025-03-01', '2027-03-01', 1, 'ACTIVE', '2025-03-01 12:30:00'),
  (13, 'BNKFD2025013', 13, 13, 1, '100000.00', NULL, '6.80', 12, '103200.00', '2025-05-01', '2026-05-01', 0, 'PREMATURE_CLOSED', '2025-05-01 10:00:00'),
  (14, 'BNKRD2025014', 14, 14, 5, '36000.00', '3000.00', '6.70', 12, '37314.00', '2025-11-01', '2026-11-01', 1, 'ACTIVE', '2025-11-01 09:00:00');

-- ----------------------------------------------------------------------------
-- Table: transactions (75 rows)
-- ----------------------------------------------------------------------------
INSERT INTO transactions (transaction_id, account_id, counterparty_account_id, beneficiary_id, reference_utr, transaction_type, channel, amount, balance_after, currency, description, remarks, status, is_flagged, initiated_ip, transaction_date) VALUES
  (1, 1, NULL, NULL, 'BNKUTR2024000001', 'CREDIT', 'NEFT', '350000.00', '350000.00', 'INR', 'Initial Salary & Savings Deposit from Infosys Ltd', 'March Payroll', 'SUCCESS', 0, '103.21.58.11', '2024-03-07 10:30:00'),
  (2, 3, NULL, NULL, 'BNKUTR2024000002', 'CREDIT', 'NEFT', '180000.00', '180000.00', 'INR', 'Initial Account Funding via NEFT', 'Self Transfer', 'SUCCESS', 0, '103.21.58.12', '2024-03-13 11:30:00'),
  (3, 5, NULL, NULL, 'BNKUTR2024000003', 'CREDIT', 'RTGS', '650000.00', '650000.00', 'INR', 'RTGS Inward Credit from Zerodha Broking', 'Payout', 'SUCCESS', 0, '103.21.58.13', '2024-03-19 12:30:00'),
  (4, 7, NULL, NULL, 'BNKUTR2024000004', 'CREDIT', 'NEFT', '400000.00', '400000.00', 'INR', 'Consultancy Retainer Credit', 'Invoice 101', 'SUCCESS', 0, '103.21.58.14', '2024-03-25 13:30:00'),
  (5, 8, NULL, NULL, 'BNKUTR2024000005', 'CREDIT', 'RTGS', '1800000.00', '1800000.00', 'INR', 'Business Export Realization Credit', 'Marble Shipment', 'SUCCESS', 0, '103.21.58.15', '2024-03-31 14:30:00'),
  (6, 10, NULL, NULL, 'BNKUTR2024000006', 'CREDIT', 'IMPS', '220000.00', '220000.00', 'INR', 'Family Remittance Credit', 'Gift from Father', 'SUCCESS', 0, '103.21.58.16', '2024-04-06 15:30:00'),
  (7, 1, 3, 1, 'BNKUTR2024000007', 'DEBIT', 'INTERNAL', '25000.00', '325000.00', 'INR', 'Internal Transfer to Ananya Sister', 'Rakhi Gift', 'SUCCESS', 0, '103.21.58.17', '2024-04-12 16:30:00'),
  (8, 3, 1, NULL, 'BNKUTR2024000008', 'CREDIT', 'INTERNAL', '25000.00', '205000.00', 'INR', 'Internal Credit from Aarav Gupta', 'Rakhi Gift', 'SUCCESS', 0, '103.21.58.18', '2024-04-18 09:30:00'),
  (9, 1, NULL, 2, 'BNKUTR2024000009', 'DEBIT', 'IMPS', '28000.00', '297000.00', 'INR', 'IMPS Transfer to Ramesh Landlord', 'April House Rent', 'SUCCESS', 0, '103.21.58.19', '2024-04-24 10:30:00'),
  (10, 5, 7, 6, 'BNKUTR2024000010', 'DEBIT', 'INTERNAL', '45000.00', '605000.00', 'INR', 'Internal Transfer to Sneha Pune', 'Project Design Fee', 'SUCCESS', 0, '103.21.58.20', '2024-04-30 11:30:00'),
  (11, 7, 5, NULL, 'BNKUTR2024000011', 'CREDIT', 'INTERNAL', '45000.00', '445000.00', 'INR', 'Internal Credit from Karthik Reddy', 'Project Design Fee', 'SUCCESS', 0, '103.21.58.21', '2024-05-06 12:30:00'),
  (12, 1, NULL, NULL, 'BNKUTR2024000012', 'DEBIT', 'INVESTMENT', '250000.00', '247000.00', 'INR', 'Fixed Deposit Booking BNKFD2024001', '3Yr FD', 'SUCCESS', 0, '103.21.58.22', '2024-05-12 13:30:00'),
  (13, 1, NULL, NULL, 'BNKUTR2024000013', 'CREDIT', 'LOAN_DISBURSAL', '850000.00', '1097000.00', 'INR', 'Vehicle Loan Disbursal BNKLN202400001', 'Hyundai Creta', 'SUCCESS', 0, '103.21.58.23', '2024-05-18 14:30:00'),
  (14, 1, NULL, 3, 'BNKUTR2024000014', 'DEBIT', 'RTGS', '840000.00', '257000.00', 'INR', 'RTGS Payment to Samara Hyundai Showroom', 'Car Invoice', 'SUCCESS', 0, '103.21.58.24', '2024-05-24 15:30:00'),
  (15, 3, NULL, NULL, 'BNKUTR2024000015', 'CREDIT', 'LOAN_DISBURSAL', '300000.00', '505000.00', 'INR', 'Personal Loan Disbursal BNKLN202400002', 'Home Interior', 'SUCCESS', 0, '103.21.58.25', '2024-05-30 16:30:00'),
  (16, 5, NULL, NULL, 'BNKUTR2024000016', 'DEBIT', 'INVESTMENT', '500000.00', '605000.00', 'INR', 'Fixed Deposit Booking BNKFD2024005', 'WealthMax FD', 'SUCCESS', 0, '103.21.58.26', '2024-06-05 09:30:00'),
  (17, 8, NULL, 10, 'BNKUTR2024000017', 'DEBIT', 'RTGS', '650000.00', '1150000.00', 'INR', 'RTGS Payment to Aravali Stones & Marbles', 'Raw Material', 'SUCCESS', 0, '103.21.58.27', '2024-06-11 10:30:00'),
  (18, 8, NULL, NULL, 'BNKUTR2024000018', 'CREDIT', 'RTGS', '950000.00', '2100000.00', 'INR', 'Dealer Advance Receipt from DLF Infra', 'Order 882', 'SUCCESS', 0, '103.21.58.28', '2024-06-17 11:30:00'),
  (19, 12, NULL, 12, 'BNKUTR2024000019', 'DEBIT', 'NEFT', '125000.00', '675000.00', 'INR', 'NEFT Office Lease Payment Manyata Park', 'Q1 Rent', 'SUCCESS', 0, '103.21.58.29', '2024-06-23 12:30:00'),
  (20, 15, NULL, 14, 'BNKUTR2024000020', 'DEBIT', 'IMPS', '49999.00', '1250.00', 'INR', 'Rapid High-Risk Transfer Attempt to Unknown Shell Traders', 'Flagged by AML Rule Engine', 'FLAGGED', 1, '103.21.58.30', '2024-06-29 13:30:00'),
  (21, 1, NULL, NULL, 'BNKBBPS202500021', 'DEBIT', 'BILL_PAY', '1065.50', '121450.00', 'INR', 'BBPS Utility Bill Payment - Noida Home Electricity', 'Consumer 4012889011', 'SUCCESS', 0, '49.36.128.21', '2024-06-16 11:00:00'),
  (22, 1, NULL, NULL, 'BNKBBPS202500022', 'DEBIT', 'BILL_PAY', '1281.00', '122900.00', 'INR', 'BBPS Utility Bill Payment - Noida Kitchen PNG', 'Consumer 7000192837', 'SUCCESS', 0, '49.36.128.22', '2024-07-01 12:00:00'),
  (23, 1, NULL, NULL, 'BNKBBPS202500023', 'DEBIT', 'BILL_PAY', '1496.50', '124350.00', 'INR', 'BBPS Utility Bill Payment - Home JioFiber', 'Consumer 01204556677', 'SUCCESS', 0, '49.36.128.23', '2024-07-16 13:00:00'),
  (24, 3, NULL, NULL, 'BNKBBPS202500024', 'DEBIT', 'BILL_PAY', '1712.00', '125800.00', 'INR', 'BBPS Utility Bill Payment - Ghaziabad Flat Power', 'Consumer 4019881122', 'SUCCESS', 0, '49.36.128.24', '2024-07-31 14:00:00'),
  (25, 3, NULL, NULL, 'BNKBBPS202500025', 'DEBIT', 'BILL_PAY', '1927.50', '127250.00', 'INR', 'BBPS Utility Bill Payment - Airtel Broadband', 'Consumer 01202889900', 'SUCCESS', 0, '49.36.128.25', '2024-08-15 15:00:00'),
  (26, 5, NULL, NULL, 'BNKBBPS202500026', 'DEBIT', 'BILL_PAY', '2143.00', '128700.00', 'INR', 'BBPS Utility Bill Payment - Indiranagar BESCOM', 'Consumer 8819200345', 'SUCCESS', 0, '49.36.128.26', '2024-08-30 10:00:00'),
  (27, 5, NULL, NULL, 'BNKBBPS202500027', 'DEBIT', 'BILL_PAY', '2358.50', '130150.00', 'INR', 'BBPS Utility Bill Payment - Indiranagar Water', 'Consumer BWSSB99812', 'SUCCESS', 0, '49.36.128.27', '2024-09-14 11:00:00'),
  (28, 6, NULL, NULL, 'BNKBBPS202500028', 'DEBIT', 'BILL_PAY', '2574.00', '131600.00', 'INR', 'BBPS Utility Bill Payment - Karthik SBI Elite Card', 'Consumer 4321XXXXXXXX8899', 'SUCCESS', 0, '49.36.128.28', '2024-09-29 12:00:00'),
  (29, 7, NULL, NULL, 'BNKBBPS202500029', 'DEBIT', 'BILL_PAY', '2789.50', '133050.00', 'INR', 'BBPS Utility Bill Payment - Pune Home MSEDCL', 'Consumer 170029384756', 'SUCCESS', 0, '49.36.128.29', '2024-10-14 13:00:00'),
  (30, 7, NULL, NULL, 'BNKBBPS202500030', 'DEBIT', 'BILL_PAY', '3005.00', '134500.00', 'INR', 'BBPS Utility Bill Payment - LIC Jeevan Anand Policy', 'Consumer 981273645', 'SUCCESS', 0, '49.36.128.30', '2024-10-29 14:00:00'),
  (31, 9, NULL, NULL, 'BNKBBPS202500031', 'DEBIT', 'BILL_PAY', '3220.50', '135950.00', 'INR', 'BBPS Utility Bill Payment - Jaipur Home Tata Play', 'Consumer 1009283746', 'SUCCESS', 0, '49.36.128.31', '2024-11-13 15:00:00'),
  (32, 10, NULL, NULL, 'BNKBBPS202500032', 'DEBIT', 'BILL_PAY', '3436.00', '137400.00', 'INR', 'BBPS Utility Bill Payment - Lucknow Home Power', 'Consumer 4055667788', 'SUCCESS', 0, '49.36.128.32', '2024-11-28 10:00:00'),
  (33, 13, NULL, NULL, 'BNKBBPS202500033', 'DEBIT', 'BILL_PAY', '3651.50', '138850.00', 'INR', 'BBPS Utility Bill Payment - Lajpat Nagar BSES', 'Consumer 1029384756', 'SUCCESS', 0, '49.36.128.33', '2024-12-13 11:00:00'),
  (34, 14, NULL, NULL, 'BNKBBPS202500034', 'DEBIT', 'BILL_PAY', '3867.00', '140300.00', 'INR', 'BBPS Utility Bill Payment - Lajpat Nagar Water', 'Consumer DJB55443322', 'SUCCESS', 0, '49.36.128.34', '2024-12-28 12:00:00'),
  (35, 1, NULL, NULL, 'BNKBBPS202500035', 'DEBIT', 'BILL_PAY', '4082.50', '141750.00', 'INR', 'BBPS Utility Bill Payment - Noida Home Electricity', 'Consumer 4012889011', 'SUCCESS', 0, '49.36.128.35', '2025-01-12 13:00:00'),
  (36, 1, NULL, NULL, 'BNKBBPS202500036', 'DEBIT', 'BILL_PAY', '4298.00', '143200.00', 'INR', 'BBPS Utility Bill Payment - Noida Kitchen PNG', 'Consumer 7000192837', 'SUCCESS', 0, '49.36.128.36', '2025-01-27 14:00:00'),
  (37, 1, NULL, NULL, 'BNKBBPS202500037', 'DEBIT', 'BILL_PAY', '4513.50', '144650.00', 'INR', 'BBPS Utility Bill Payment - Home JioFiber', 'Consumer 01204556677', 'SUCCESS', 0, '49.36.128.37', '2025-02-11 15:00:00'),
  (38, 3, NULL, NULL, 'BNKBBPS202500038', 'DEBIT', 'BILL_PAY', '4729.00', '146100.00', 'INR', 'BBPS Utility Bill Payment - Ghaziabad Flat Power', 'Consumer 4019881122', 'SUCCESS', 0, '49.36.128.38', '2025-02-26 10:00:00'),
  (39, 3, NULL, NULL, 'BNKBBPS202500039', 'DEBIT', 'BILL_PAY', '4944.50', '147550.00', 'INR', 'BBPS Utility Bill Payment - Airtel Broadband', 'Consumer 01202889900', 'FAILED', 0, '49.36.128.39', '2025-03-13 11:00:00'),
  (40, 5, NULL, NULL, 'BNKBBPS202500040', 'DEBIT', 'BILL_PAY', '5160.00', '149000.00', 'INR', 'BBPS Utility Bill Payment - Indiranagar BESCOM', 'Consumer 8819200345', 'SUCCESS', 0, '49.36.128.40', '2025-03-28 12:00:00'),
  (41, 5, NULL, NULL, 'BNKBBPS202500041', 'DEBIT', 'BILL_PAY', '5375.50', '150450.00', 'INR', 'BBPS Utility Bill Payment - Indiranagar Water', 'Consumer BWSSB99812', 'SUCCESS', 0, '49.36.128.41', '2025-04-12 13:00:00'),
  (42, 6, NULL, NULL, 'BNKBBPS202500042', 'DEBIT', 'BILL_PAY', '5591.00', '151900.00', 'INR', 'BBPS Utility Bill Payment - Karthik SBI Elite Card', 'Consumer 4321XXXXXXXX8899', 'SUCCESS', 0, '49.36.128.42', '2025-04-27 14:00:00'),
  (43, 7, NULL, NULL, 'BNKBBPS202500043', 'DEBIT', 'BILL_PAY', '5806.50', '153350.00', 'INR', 'BBPS Utility Bill Payment - Pune Home MSEDCL', 'Consumer 170029384756', 'SUCCESS', 0, '49.36.128.43', '2025-05-12 15:00:00'),
  (44, 7, NULL, NULL, 'BNKBBPS202500044', 'DEBIT', 'BILL_PAY', '6022.00', '154800.00', 'INR', 'BBPS Utility Bill Payment - LIC Jeevan Anand Policy', 'Consumer 981273645', 'SUCCESS', 0, '49.36.128.44', '2025-05-27 10:00:00'),
  (45, 9, NULL, NULL, 'BNKBBPS202500045', 'DEBIT', 'BILL_PAY', '6237.50', '156250.00', 'INR', 'BBPS Utility Bill Payment - Jaipur Home Tata Play', 'Consumer 1009283746', 'SUCCESS', 0, '49.36.128.45', '2025-06-11 11:00:00'),
  (46, 1, NULL, NULL, 'BNKEMI2025000046', 'DEBIT', 'LOAN_EMI', '17583.00', '215400.00', 'INR', 'Auto-Debit Loan EMI for BNKLN202400001', 'Installment #1', 'SUCCESS', 0, '122.161.44.11', '2025-01-23 10:15:00'),
  (47, 3, NULL, NULL, 'BNKEMI2025000047', 'DEBIT', 'LOAN_EMI', '9786.00', '215400.00', 'INR', 'Auto-Debit Loan EMI for BNKLN202400002', 'Installment #1', 'SUCCESS', 0, '122.161.44.12', '2025-02-10 11:15:00'),
  (48, 5, NULL, NULL, 'BNKEMI2025000048', 'DEBIT', 'LOAN_EMI', '56408.00', '215400.00', 'INR', 'Auto-Debit Loan EMI for BNKLN202400003', 'Installment #1', 'SUCCESS', 0, '122.161.44.13', '2025-02-28 12:15:00'),
  (49, 7, NULL, NULL, 'BNKEMI2025000049', 'DEBIT', 'LOAN_EMI', '28655.00', '215400.00', 'INR', 'Auto-Debit Loan EMI for BNKLN202400004', 'Installment #1', 'SUCCESS', 0, '122.161.44.14', '2025-03-18 13:15:00'),
  (50, 8, NULL, NULL, 'BNKEMI2025000050', 'DEBIT', 'LOAN_EMI', '98268.00', '215400.00', 'INR', 'Auto-Debit Loan EMI for BNKLN202400005', 'Installment #1', 'SUCCESS', 0, '122.161.44.15', '2025-04-05 14:15:00'),
  (51, 10, NULL, NULL, 'BNKEMI2025000051', 'DEBIT', 'LOAN_EMI', '12209.00', '215400.00', 'INR', 'Auto-Debit Loan EMI for BNKLN202400006', 'Installment #1', 'SUCCESS', 0, '122.161.44.16', '2025-04-23 15:15:00'),
  (52, 12, NULL, NULL, 'BNKEMI2025000052', 'DEBIT', 'LOAN_EMI', '24852.00', '215400.00', 'INR', 'Auto-Debit Loan EMI for BNKLN202500007', 'Installment #1', 'SUCCESS', 0, '122.161.44.17', '2025-05-11 16:15:00'),
  (53, 1, NULL, NULL, 'BNKEMI2025000053', 'DEBIT', 'LOAN_EMI', '17583.00', '215400.00', 'INR', 'Auto-Debit Loan EMI for BNKLN202400001', 'Installment #2', 'SUCCESS', 0, '122.161.44.18', '2025-05-29 17:15:00'),
  (54, 3, NULL, NULL, 'BNKEMI2025000054', 'DEBIT', 'LOAN_EMI', '9786.00', '215400.00', 'INR', 'Auto-Debit Loan EMI for BNKLN202400002', 'Installment #2', 'SUCCESS', 0, '122.161.44.19', '2025-06-16 09:15:00'),
  (55, 5, NULL, NULL, 'BNKEMI2025000055', 'DEBIT', 'LOAN_EMI', '56408.00', '215400.00', 'INR', 'Auto-Debit Loan EMI for BNKLN202400003', 'Installment #2', 'SUCCESS', 0, '122.161.44.20', '2025-07-04 10:15:00'),
  (56, 7, NULL, NULL, 'BNKEMI2025000056', 'DEBIT', 'LOAN_EMI', '28655.00', '215400.00', 'INR', 'Auto-Debit Loan EMI for BNKLN202400004', 'Installment #2', 'SUCCESS', 0, '122.161.44.21', '2025-07-22 11:15:00'),
  (57, 8, NULL, NULL, 'BNKEMI2025000057', 'DEBIT', 'LOAN_EMI', '98268.00', '215400.00', 'INR', 'Auto-Debit Loan EMI for BNKLN202400005', 'Installment #2', 'SUCCESS', 0, '122.161.44.22', '2025-08-09 12:15:00'),
  (58, 10, NULL, NULL, 'BNKEMI2025000058', 'DEBIT', 'LOAN_EMI', '12209.00', '215400.00', 'INR', 'Auto-Debit Loan EMI for BNKLN202400006', 'Installment #2', 'SUCCESS', 0, '122.161.44.23', '2025-08-27 13:15:00'),
  (59, 12, NULL, NULL, 'BNKEMI2025000059', 'DEBIT', 'LOAN_EMI', '24852.00', '215400.00', 'INR', 'Auto-Debit Loan EMI for BNKLN202500007', 'Installment #2', 'SUCCESS', 0, '122.161.44.24', '2025-09-14 14:15:00'),
  (60, 1, NULL, NULL, 'BNKEMI2025000060', 'DEBIT', 'LOAN_EMI', '17583.00', '215400.00', 'INR', 'Auto-Debit Loan EMI for BNKLN202400001', 'Installment #3', 'SUCCESS', 0, '122.161.44.25', '2025-10-02 15:15:00'),
  (61, 3, NULL, NULL, 'BNKEMI2025000061', 'DEBIT', 'LOAN_EMI', '9786.00', '215400.00', 'INR', 'Auto-Debit Loan EMI for BNKLN202400002', 'Installment #3', 'SUCCESS', 0, '122.161.44.26', '2025-10-20 16:15:00'),
  (62, 5, NULL, NULL, 'BNKEMI2025000062', 'DEBIT', 'LOAN_EMI', '56408.00', '215400.00', 'INR', 'Auto-Debit Loan EMI for BNKLN202400003', 'Installment #3', 'SUCCESS', 0, '122.161.44.27', '2025-11-07 17:15:00'),
  (63, 7, NULL, NULL, 'BNKEMI2025000063', 'DEBIT', 'LOAN_EMI', '28655.00', '215400.00', 'INR', 'Auto-Debit Loan EMI for BNKLN202400004', 'Installment #3', 'SUCCESS', 0, '122.161.44.28', '2025-11-25 09:15:00'),
  (64, 8, NULL, NULL, 'BNKEMI2025000064', 'DEBIT', 'LOAN_EMI', '98268.00', '215400.00', 'INR', 'Auto-Debit Loan EMI for BNKLN202400005', 'Installment #3', 'SUCCESS', 0, '122.161.44.29', '2025-12-13 10:15:00'),
  (65, 10, NULL, NULL, 'BNKEMI2025000065', 'DEBIT', 'LOAN_EMI', '12209.00', '215400.00', 'INR', 'Auto-Debit Loan EMI for BNKLN202400006', 'Installment #3', 'SUCCESS', 0, '122.161.44.30', '2025-12-31 11:15:00'),
  (66, 1, NULL, NULL, 'BNKTXN2026000066', 'DEBIT', 'IMPS', '8220.00', '184200.00', 'INR', 'IMPS Merchant / Peer Transfer #21', 'Everyday Banking', 'SUCCESS', 0, '157.42.99.21', '2026-01-18 12:15:00'),
  (67, 2, NULL, NULL, 'BNKTXN2026000067', 'DEBIT', 'UPI', '8540.00', '184200.00', 'INR', 'UPI Merchant / Peer Transfer #22', 'Everyday Banking', 'SUCCESS', 0, '157.42.99.22', '2026-02-05 13:15:00'),
  (68, 3, NULL, NULL, 'BNKTXN2026000068', 'DEBIT', 'IMPS', '8860.00', '184200.00', 'INR', 'IMPS Merchant / Peer Transfer #23', 'Everyday Banking', 'SUCCESS', 0, '157.42.99.23', '2026-02-23 14:15:00'),
  (69, 4, NULL, NULL, 'BNKTXN2026000069', 'DEBIT', 'UPI', '9180.00', '184200.00', 'INR', 'UPI Merchant / Peer Transfer #24', 'Everyday Banking', 'SUCCESS', 0, '157.42.99.24', '2026-03-13 15:15:00'),
  (70, 5, NULL, NULL, 'BNKTXN2026000070', 'DEBIT', 'IMPS', '9500.00', '184200.00', 'INR', 'IMPS Merchant / Peer Transfer #25', 'Everyday Banking', 'SUCCESS', 0, '157.42.99.25', '2026-03-31 16:15:00'),
  (71, 6, NULL, NULL, 'BNKTXN2026000071', 'DEBIT', 'UPI', '9820.00', '184200.00', 'INR', 'UPI Merchant / Peer Transfer #26', 'Everyday Banking', 'SUCCESS', 0, '157.42.99.26', '2026-04-18 17:15:00'),
  (72, 7, NULL, NULL, 'BNKTXN2026000072', 'DEBIT', 'IMPS', '10140.00', '184200.00', 'INR', 'IMPS Merchant / Peer Transfer #27', 'Everyday Banking', 'SUCCESS', 0, '157.42.99.27', '2026-05-06 09:15:00'),
  (73, 8, NULL, 2, 'BNKTXN2026000073', 'DEBIT', 'RTGS', '985000.00', '184200.00', 'INR', 'High-Value RTGS Outward Remittance Requiring Compliance Review', 'Automated Audit Check', 'FLAGGED', 1, '157.42.99.28', '2026-05-24 10:15:00'),
  (74, 9, NULL, NULL, 'BNKTXN2026000074', 'DEBIT', 'IMPS', '10780.00', '184200.00', 'INR', 'IMPS Merchant / Peer Transfer #29', 'Everyday Banking', 'SUCCESS', 0, '157.42.99.29', '2026-06-11 11:15:00'),
  (75, 10, NULL, 2, 'BNKTXN2026000075', 'DEBIT', 'RTGS', '985000.00', '184200.00', 'INR', 'High-Value RTGS Outward Remittance Requiring Compliance Review', 'Automated Audit Check', 'FLAGGED', 1, '157.42.99.30', '2026-06-29 12:15:00');

-- ----------------------------------------------------------------------------
-- Table: bill_payments (55 rows)
-- ----------------------------------------------------------------------------
INSERT INTO bill_payments (bill_payment_id, customer_biller_id, account_id, transaction_id, bbps_ref_no, bill_period, bill_amount, convenience_fee, total_paid, due_date, payment_mode, payment_status, paid_at, created_at) VALUES
  (1, 1, 1, 21, 'BBPSIN202500000001', 'Apr-2024', '887.25', '0.00', '887.25', '2024-05-24', 'AUTOPAY', 'PAID', '2024-05-22 14:20:00', '2024-05-17 14:20:00'),
  (2, 2, 1, 22, 'BBPSIN202500000002', 'May-2024', '1024.50', '0.00', '1024.50', '2024-06-07', 'AUTOPAY', 'PAID', '2024-06-05 14:20:00', '2024-05-31 14:20:00'),
  (3, 3, 1, 23, 'BBPSIN202500000003', 'Jun-2024', '1161.75', '0.00', '1161.75', '2024-06-21', 'AUTOPAY', 'PAID', '2024-06-19 14:20:00', '2024-06-14 14:20:00'),
  (4, 4, 3, 24, 'BBPSIN202500000004', 'Jul-2024', '1299.00', '15.00', '1314.00', '2024-07-05', 'MANUAL', 'PAID', '2024-07-03 14:20:00', '2024-06-28 14:20:00'),
  (5, 5, 3, 25, 'BBPSIN202500000005', 'Aug-2024', '1436.25', '0.00', '1436.25', '2024-07-19', 'AUTOPAY', 'PAID', '2024-07-17 14:20:00', '2024-07-12 14:20:00'),
  (6, 6, 5, 26, 'BBPSIN202500000006', 'Sep-2024', '1573.50', '0.00', '1573.50', '2024-08-02', 'AUTOPAY', 'PAID', '2024-07-31 14:20:00', '2024-07-26 14:20:00'),
  (7, 7, 5, 27, 'BBPSIN202500000007', 'Oct-2024', '1710.75', '15.00', '1725.75', '2024-08-16', 'MANUAL', 'PAID', '2024-08-14 14:20:00', '2024-08-09 14:20:00'),
  (8, 8, 6, 28, 'BBPSIN202500000008', 'Nov-2024', '1848.00', '15.00', '1863.00', '2024-08-30', 'MANUAL', 'PAID', '2024-08-28 14:20:00', '2024-08-23 14:20:00'),
  (9, 9, 7, 29, 'BBPSIN202500000009', 'Dec-2024', '1985.25', '0.00', '1985.25', '2024-09-13', 'AUTOPAY', 'PAID', '2024-09-11 14:20:00', '2024-09-06 14:20:00'),
  (10, 10, 7, 30, 'BBPSIN202500000010', 'Jan-2025', '2122.50', '0.00', '2122.50', '2024-09-27', 'AUTOPAY', 'PAID', '2024-09-25 14:20:00', '2024-09-20 14:20:00'),
  (11, 11, 9, 31, 'BBPSIN202500000011', 'Feb-2025', '2259.75', '0.00', '2259.75', '2024-10-11', 'AUTOPAY', 'PAID', '2024-10-09 14:20:00', '2024-10-04 14:20:00'),
  (12, 12, 10, 32, 'BBPSIN202500000012', 'Mar-2025', '2397.00', '15.00', '2412.00', '2024-10-25', 'MANUAL', 'PAID', '2024-10-23 14:20:00', '2024-10-18 14:20:00'),
  (13, 13, 13, 33, 'BBPSIN202500000013', 'Apr-2025', '2534.25', '15.00', '2549.25', '2024-11-08', 'MANUAL', 'PAID', '2024-11-06 14:20:00', '2024-11-01 14:20:00'),
  (14, 14, 14, 34, 'BBPSIN202500000014', 'May-2025', '2671.50', '15.00', '2686.50', '2024-11-22', 'MANUAL', 'PAID', '2024-11-20 14:20:00', '2024-11-15 14:20:00'),
  (15, 1, 1, 35, 'BBPSIN202500000015', 'Jun-2025', '2808.75', '0.00', '2808.75', '2024-12-06', 'AUTOPAY', 'PAID', '2024-12-04 14:20:00', '2024-11-29 14:20:00'),
  (16, 2, 1, 36, 'BBPSIN202500000016', 'Jul-2025', '2946.00', '0.00', '2946.00', '2024-12-20', 'AUTOPAY', 'PAID', '2024-12-18 14:20:00', '2024-12-13 14:20:00'),
  (17, 3, 1, 37, 'BBPSIN202500000017', 'Aug-2025', '3083.25', '0.00', '3083.25', '2025-01-03', 'AUTOPAY', 'PAID', '2025-01-01 14:20:00', '2024-12-27 14:20:00'),
  (18, 4, 3, 38, 'BBPSIN202500000018', 'Sep-2025', '3220.50', '15.00', '3235.50', '2025-01-17', 'MANUAL', 'PAID', '2025-01-15 14:20:00', '2025-01-10 14:20:00'),
  (19, 5, 3, 39, 'BBPSIN202500000019', 'Oct-2025', '3357.75', '0.00', '3357.75', '2025-01-31', 'AUTOPAY', 'FAILED', NULL, '2025-01-24 14:20:00'),
  (20, 6, 5, 40, 'BBPSIN202500000020', 'Nov-2025', '3495.00', '0.00', '3495.00', '2025-02-14', 'AUTOPAY', 'PAID', '2025-02-12 14:20:00', '2025-02-07 14:20:00'),
  (21, 7, 5, 41, 'BBPSIN202500000021', 'Dec-2025', '3632.25', '15.00', '3647.25', '2025-02-28', 'MANUAL', 'PAID', '2025-02-26 14:20:00', '2025-02-21 14:20:00'),
  (22, 8, 6, 42, 'BBPSIN202500000022', 'Jan-2026', '3769.50', '15.00', '3784.50', '2025-03-14', 'MANUAL', 'PAID', '2025-03-12 14:20:00', '2025-03-07 14:20:00'),
  (23, 9, 7, 43, 'BBPSIN202500000023', 'Feb-2026', '3906.75', '0.00', '3906.75', '2025-03-28', 'AUTOPAY', 'PAID', '2025-03-26 14:20:00', '2025-03-21 14:20:00'),
  (24, 10, 7, 44, 'BBPSIN202500000024', 'Mar-2026', '4044.00', '0.00', '4044.00', '2025-04-11', 'AUTOPAY', 'PAID', '2025-04-09 14:20:00', '2025-04-04 14:20:00'),
  (25, 11, 9, 45, 'BBPSIN202500000025', 'Apr-2026', '4181.25', '0.00', '4181.25', '2025-04-25', 'AUTOPAY', 'PAID', '2025-04-23 14:20:00', '2025-04-18 14:20:00'),
  (26, 12, 10, NULL, 'BBPSIN202500000026', 'May-2026', '4318.50', '15.00', '4333.50', '2025-05-09', 'MANUAL', 'PAID', '2025-05-07 14:20:00', '2025-05-02 14:20:00'),
  (27, 13, 13, NULL, 'BBPSIN202500000027', 'Jun-2026', '4455.75', '15.00', '4470.75', '2025-05-23', 'MANUAL', 'PAID', '2025-05-21 14:20:00', '2025-05-16 14:20:00'),
  (28, 14, 14, NULL, 'BBPSIN202500000028', 'Jul-2026', '4593.00', '15.00', '4608.00', '2025-06-06', 'MANUAL', 'PAID', '2025-06-04 14:20:00', '2025-05-30 14:20:00'),
  (29, 1, 1, NULL, 'BBPSIN202500000029', 'Aug-2026', '4730.25', '0.00', '4730.25', '2025-06-20', 'AUTOPAY', 'PAID', '2025-06-18 14:20:00', '2025-06-13 14:20:00'),
  (30, 2, 1, NULL, 'BBPSIN202500000030', 'Sep-2026', '4867.50', '0.00', '4867.50', '2025-07-04', 'AUTOPAY', 'PAID', '2025-07-02 14:20:00', '2025-06-27 14:20:00'),
  (31, 3, 1, NULL, 'BBPSIN202500000031', 'Oct-2026', '5004.75', '0.00', '5004.75', '2025-07-18', 'AUTOPAY', 'PAID', '2025-07-16 14:20:00', '2025-07-11 14:20:00'),
  (32, 4, 3, NULL, 'BBPSIN202500000032', 'Apr-2024', '5142.00', '15.00', '5157.00', '2025-08-01', 'MANUAL', 'PAID', '2025-07-30 14:20:00', '2025-07-25 14:20:00'),
  (33, 5, 3, NULL, 'BBPSIN202500000033', 'May-2024', '779.25', '0.00', '779.25', '2025-08-15', 'AUTOPAY', 'PAID', '2025-08-13 14:20:00', '2025-08-08 14:20:00'),
  (34, 6, 5, NULL, 'BBPSIN202500000034', 'Jun-2024', '916.50', '0.00', '916.50', '2025-08-29', 'AUTOPAY', 'PAID', '2025-08-27 14:20:00', '2025-08-22 14:20:00'),
  (35, 7, 5, NULL, 'BBPSIN202500000035', 'Jul-2024', '1053.75', '15.00', '1068.75', '2025-09-12', 'MANUAL', 'PAID', '2025-09-10 14:20:00', '2025-09-05 14:20:00'),
  (36, 8, 6, NULL, 'BBPSIN202500000036', 'Aug-2024', '1191.00', '15.00', '1206.00', '2025-09-26', 'MANUAL', 'PAID', '2025-09-24 14:20:00', '2025-09-19 14:20:00'),
  (37, 9, 7, NULL, 'BBPSIN202500000037', 'Sep-2024', '1328.25', '0.00', '1328.25', '2025-10-10', 'AUTOPAY', 'PAID', '2025-10-08 14:20:00', '2025-10-03 14:20:00'),
  (38, 10, 7, NULL, 'BBPSIN202500000038', 'Oct-2024', '1465.50', '0.00', '1465.50', '2025-10-24', 'AUTOPAY', 'PAID', '2025-10-22 14:20:00', '2025-10-17 14:20:00'),
  (39, 11, 9, NULL, 'BBPSIN202500000039', 'Nov-2024', '1602.75', '0.00', '1602.75', '2025-11-07', 'AUTOPAY', 'PAID', '2025-11-05 14:20:00', '2025-10-31 14:20:00'),
  (40, 12, 10, NULL, 'BBPSIN202500000040', 'Dec-2024', '1740.00', '15.00', '1755.00', '2025-11-21', 'MANUAL', 'PAID', '2025-11-19 14:20:00', '2025-11-14 14:20:00'),
  (41, 13, 13, NULL, 'BBPSIN202500000041', 'Jan-2025', '1877.25', '15.00', '1892.25', '2025-12-05', 'MANUAL', 'PAID', '2025-12-03 14:20:00', '2025-11-28 14:20:00'),
  (42, 14, 14, NULL, 'BBPSIN202500000042', 'Feb-2025', '2014.50', '15.00', '2029.50', '2025-12-19', 'MANUAL', 'PAID', '2025-12-17 14:20:00', '2025-12-12 14:20:00'),
  (43, 1, 1, NULL, 'BBPSIN202500000043', 'Mar-2025', '2151.75', '0.00', '2151.75', '2026-01-02', 'AUTOPAY', 'PAID', '2025-12-31 14:20:00', '2025-12-26 14:20:00'),
  (44, 2, 1, NULL, 'BBPSIN202500000044', 'Apr-2025', '2289.00', '0.00', '2289.00', '2026-01-16', 'AUTOPAY', 'PAID', '2026-01-14 14:20:00', '2026-01-09 14:20:00'),
  (45, 3, 1, NULL, 'BBPSIN202500000045', 'May-2025', '2426.25', '0.00', '2426.25', '2026-01-30', 'AUTOPAY', 'PAID', '2026-01-28 14:20:00', '2026-01-23 14:20:00'),
  (46, 4, 3, NULL, 'BBPSIN202500000046', 'Jun-2025', '2563.50', '15.00', '2578.50', '2026-02-13', 'MANUAL', 'PAID', '2026-02-11 14:20:00', '2026-02-06 14:20:00'),
  (47, 5, 3, NULL, 'BBPSIN202500000047', 'Jul-2025', '2700.75', '0.00', '2700.75', '2026-02-27', 'AUTOPAY', 'PAID', '2026-02-25 14:20:00', '2026-02-20 14:20:00'),
  (48, 6, 5, NULL, 'BBPSIN202500000048', 'Aug-2025', '2838.00', '0.00', '2838.00', '2026-03-13', 'AUTOPAY', 'PAID', '2026-03-11 14:20:00', '2026-03-06 14:20:00'),
  (49, 7, 5, NULL, 'BBPSIN202500000049', 'Sep-2025', '2975.25', '15.00', '2990.25', '2026-03-27', 'MANUAL', 'PAID', '2026-03-25 14:20:00', '2026-03-20 14:20:00'),
  (50, 8, 6, NULL, 'BBPSIN202500000050', 'Oct-2025', '3112.50', '15.00', '3127.50', '2026-04-10', 'MANUAL', 'PAID', '2026-04-08 14:20:00', '2026-04-03 14:20:00'),
  (51, 9, 7, NULL, 'BBPSIN202500000051', 'Nov-2025', '3249.75', '0.00', '3249.75', '2026-04-24', 'AUTOPAY', 'PAID', '2026-04-22 14:20:00', '2026-04-17 14:20:00'),
  (52, 10, 7, NULL, 'BBPSIN202500000052', 'Dec-2025', '3387.00', '0.00', '3387.00', '2026-05-08', 'AUTOPAY', 'PENDING', NULL, '2026-05-01 14:20:00'),
  (53, 11, 9, NULL, 'BBPSIN202500000053', 'Jan-2026', '3524.25', '0.00', '3524.25', '2026-05-22', 'AUTOPAY', 'PENDING', NULL, '2026-05-15 14:20:00'),
  (54, 12, 10, NULL, 'BBPSIN202500000054', 'Feb-2026', '3661.50', '15.00', '3676.50', '2026-06-05', 'MANUAL', 'OVERDUE', NULL, '2026-05-29 14:20:00'),
  (55, 13, 13, NULL, 'BBPSIN202500000055', 'Mar-2026', '3798.75', '15.00', '3813.75', '2026-06-19', 'MANUAL', 'OVERDUE', NULL, '2026-06-12 14:20:00');

-- ----------------------------------------------------------------------------
-- Table: loan_repayments (60 rows)
-- ----------------------------------------------------------------------------
INSERT INTO loan_repayments (repayment_id, loan_id, transaction_id, installment_number, due_date, emi_amount, principal_component, interest_component, penalty_amount, repayment_status, paid_at) VALUES
  (1, 1, 46, 1, '2024-08-04', '17583.00', '10901.46', '6681.54', '0.00', 'PAID', '2024-08-04 10:15:00'),
  (2, 1, 47, 2, '2024-09-03', '17583.00', '10901.46', '6681.54', '0.00', 'PAID', '2024-09-03 10:15:00'),
  (3, 1, 48, 3, '2024-10-03', '17583.00', '10901.46', '6681.54', '0.00', 'PAID', '2024-10-03 10:15:00'),
  (4, 1, 49, 4, '2024-11-02', '17583.00', '10901.46', '6681.54', '0.00', 'PAID', '2024-11-02 10:15:00'),
  (5, 1, 50, 5, '2024-12-02', '17583.00', '10901.46', '6681.54', '0.00', 'PAID', '2024-12-02 10:15:00'),
  (6, 1, 51, 6, '2025-01-01', '17583.00', '10901.46', '6681.54', '0.00', 'PAID', '2025-01-01 10:15:00'),
  (7, 1, 52, 7, '2025-01-31', '17583.00', '10901.46', '6681.54', '0.00', 'PAID', '2025-01-31 10:15:00'),
  (8, 1, 53, 8, '2025-03-02', '17583.00', '10901.46', '6681.54', '0.00', 'PAID', '2025-03-02 10:15:00'),
  (9, 2, 54, 1, '2024-08-09', '9786.00', '6067.32', '3718.68', '0.00', 'PAID', '2024-08-09 10:15:00'),
  (10, 2, 55, 2, '2024-09-08', '9786.00', '6067.32', '3718.68', '0.00', 'PAID', '2024-09-08 10:15:00'),
  (11, 2, 56, 3, '2024-10-08', '9786.00', '6067.32', '3718.68', '0.00', 'PAID', '2024-10-08 10:15:00'),
  (12, 2, 57, 4, '2024-11-07', '9786.00', '6067.32', '3718.68', '0.00', 'PAID', '2024-11-07 10:15:00'),
  (13, 2, 58, 5, '2024-12-07', '9786.00', '6067.32', '3718.68', '0.00', 'PAID', '2024-12-07 10:15:00'),
  (14, 2, 59, 6, '2025-01-06', '9786.00', '6067.32', '3718.68', '0.00', 'PAID', '2025-01-06 10:15:00'),
  (15, 2, 60, 7, '2025-02-05', '9786.00', '6067.32', '3718.68', '0.00', 'PAID', '2025-02-05 10:15:00'),
  (16, 2, 61, 8, '2025-03-07', '9786.00', '6067.32', '3718.68', '0.00', 'PENDING', NULL),
  (17, 3, 62, 1, '2024-08-14', '56408.00', '34972.96', '21435.04', '0.00', 'PAID', '2024-08-14 10:15:00'),
  (18, 3, 63, 2, '2024-09-13', '56408.00', '34972.96', '21435.04', '0.00', 'PAID', '2024-09-13 10:15:00'),
  (19, 3, 64, 3, '2024-10-13', '56408.00', '34972.96', '21435.04', '0.00', 'PAID', '2024-10-13 10:15:00'),
  (20, 3, 65, 4, '2024-11-12', '56408.00', '34972.96', '21435.04', '0.00', 'PAID', '2024-11-12 10:15:00'),
  (21, 3, NULL, 5, '2024-12-12', '56408.00', '34972.96', '21435.04', '0.00', 'PAID', '2024-12-12 10:15:00'),
  (22, 3, NULL, 6, '2025-01-11', '56408.00', '34972.96', '21435.04', '0.00', 'PAID', '2025-01-11 10:15:00'),
  (23, 3, NULL, 7, '2025-02-10', '56408.00', '34972.96', '21435.04', '0.00', 'PAID', '2025-02-10 10:15:00'),
  (24, 3, NULL, 8, '2025-03-12', '56408.00', '34972.96', '21435.04', '0.00', 'PAID', '2025-03-12 10:15:00'),
  (25, 4, NULL, 1, '2024-08-19', '28655.00', '17766.10', '10888.90', '0.00', 'PAID', '2024-08-19 10:15:00'),
  (26, 4, NULL, 2, '2024-09-18', '28655.00', '17766.10', '10888.90', '0.00', 'PAID', '2024-09-18 10:15:00'),
  (27, 4, NULL, 3, '2024-10-18', '28655.00', '17766.10', '10888.90', '0.00', 'PAID', '2024-10-18 10:15:00'),
  (28, 4, NULL, 4, '2024-11-17', '28655.00', '17766.10', '10888.90', '0.00', 'PAID', '2024-11-17 10:15:00'),
  (29, 4, NULL, 5, '2024-12-17', '28655.00', '17766.10', '10888.90', '0.00', 'PAID', '2024-12-17 10:15:00'),
  (30, 4, NULL, 6, '2025-01-16', '28655.00', '17766.10', '10888.90', '0.00', 'PAID', '2025-01-16 10:15:00'),
  (31, 4, NULL, 7, '2025-02-15', '28655.00', '17766.10', '10888.90', '0.00', 'PAID', '2025-02-15 10:15:00'),
  (32, 4, NULL, 8, '2025-03-17', '28655.00', '17766.10', '10888.90', '0.00', 'PENDING', NULL),
  (33, 5, NULL, 1, '2024-08-24', '98268.00', '60926.16', '37341.84', '0.00', 'PAID', '2024-08-24 10:15:00'),
  (34, 5, NULL, 2, '2024-09-23', '98268.00', '60926.16', '37341.84', '0.00', 'PAID', '2024-09-23 10:15:00'),
  (35, 5, NULL, 3, '2024-10-23', '98268.00', '60926.16', '37341.84', '0.00', 'PAID', '2024-10-23 10:15:00'),
  (36, 5, NULL, 4, '2024-11-22', '98268.00', '60926.16', '37341.84', '0.00', 'PAID', '2024-11-22 10:15:00'),
  (37, 5, NULL, 5, '2024-12-22', '98268.00', '60926.16', '37341.84', '0.00', 'PAID', '2024-12-22 10:15:00'),
  (38, 5, NULL, 6, '2025-01-21', '98268.00', '60926.16', '37341.84', '500.00', 'OVERDUE', NULL),
  (39, 5, NULL, 7, '2025-02-20', '98268.00', '60926.16', '37341.84', '0.00', 'PAID', '2025-02-20 10:15:00'),
  (40, 6, NULL, 1, '2024-08-29', '12209.00', '7569.58', '4639.42', '0.00', 'PAID', '2024-08-29 10:15:00'),
  (41, 6, NULL, 2, '2024-09-28', '12209.00', '7569.58', '4639.42', '0.00', 'PAID', '2024-09-28 10:15:00'),
  (42, 6, NULL, 3, '2024-10-28', '12209.00', '7569.58', '4639.42', '0.00', 'PAID', '2024-10-28 10:15:00'),
  (43, 6, NULL, 4, '2024-11-27', '12209.00', '7569.58', '4639.42', '0.00', 'PAID', '2024-11-27 10:15:00'),
  (44, 6, NULL, 5, '2024-12-27', '12209.00', '7569.58', '4639.42', '0.00', 'PAID', '2024-12-27 10:15:00'),
  (45, 6, NULL, 6, '2025-01-26', '12209.00', '7569.58', '4639.42', '0.00', 'PAID', '2025-01-26 10:15:00'),
  (46, 6, NULL, 7, '2025-02-25', '12209.00', '7569.58', '4639.42', '0.00', 'PAID', '2025-02-25 10:15:00'),
  (47, 7, NULL, 1, '2024-09-03', '24852.00', '15408.24', '9443.76', '0.00', 'PAID', '2024-09-03 10:15:00'),
  (48, 7, NULL, 2, '2024-10-03', '24852.00', '15408.24', '9443.76', '0.00', 'PAID', '2024-10-03 10:15:00'),
  (49, 7, NULL, 3, '2024-11-02', '24852.00', '15408.24', '9443.76', '0.00', 'PAID', '2024-11-02 10:15:00'),
  (50, 7, NULL, 4, '2024-12-02', '24852.00', '15408.24', '9443.76', '0.00', 'PAID', '2024-12-02 10:15:00'),
  (51, 7, NULL, 5, '2025-01-01', '24852.00', '15408.24', '9443.76', '0.00', 'PAID', '2025-01-01 10:15:00'),
  (52, 7, NULL, 6, '2025-01-31', '24852.00', '15408.24', '9443.76', '0.00', 'PAID', '2025-01-31 10:15:00'),
  (53, 7, NULL, 7, '2025-03-02', '24852.00', '15408.24', '9443.76', '0.00', 'PAID', '2025-03-02 10:15:00'),
  (54, 8, NULL, 1, '2024-09-08', '17490.00', '10843.80', '6646.20', '0.00', 'PAID', '2024-09-08 10:15:00'),
  (55, 8, NULL, 2, '2024-10-08', '17490.00', '10843.80', '6646.20', '0.00', 'PAID', '2024-10-08 10:15:00'),
  (56, 8, NULL, 3, '2024-11-07', '17490.00', '10843.80', '6646.20', '0.00', 'PAID', '2024-11-07 10:15:00'),
  (57, 8, NULL, 4, '2024-12-07', '17490.00', '10843.80', '6646.20', '0.00', 'PAID', '2024-12-07 10:15:00'),
  (58, 8, NULL, 5, '2025-01-06', '17490.00', '10843.80', '6646.20', '0.00', 'PAID', '2025-01-06 10:15:00'),
  (59, 8, NULL, 6, '2025-02-05', '17490.00', '10843.80', '6646.20', '0.00', 'PAID', '2025-02-05 10:15:00'),
  (60, 8, NULL, 7, '2025-03-07', '17490.00', '10843.80', '6646.20', '0.00', 'PAID', '2025-03-07 10:15:00');

-- ----------------------------------------------------------------------------
-- Table: support_tickets (14 rows)
-- ----------------------------------------------------------------------------
INSERT INTO support_tickets (ticket_id, ticket_number, user_id, assigned_officer_id, related_transaction_id, category, priority, subject, description, ticket_status, resolution_notes, created_at, resolved_at) VALUES
  (1, 'TKT20240001', 5, 2, 9, 'FUNDS_TRANSFER', 'HIGH', 'IMPS rent transfer delayed acknowledgement', 'Transferred INR 28,000 via IMPS to landlord Ramesh Agarwal but receipt took 10 minutes to reflect.', 'CLOSED', 'Verified IMPS switch settlement; UTR confirmed credited to beneficiary bank.', '2024-04-20 11:00:00', '2024-04-20 16:30:00'),
  (2, 'TKT20240002', 6, 3, 39, 'BILL_PAYMENT', 'HIGH', 'Electricity bill debited but utility portal shows unpaid', 'Paid Ghaziabad electricity bill of INR 4,944.50, amount debited failed at biller end.', 'RESOLVED', 'Auto-reversal initiated and credited back to savings account.', '2025-03-10 14:20:00', '2025-03-11 11:00:00'),
  (3, 'TKT20240003', 7, 2, NULL, 'LOAN_QUERY', 'MEDIUM', 'Request for Home Loan Provisional Interest Certificate FY 2024-25', 'Need provisional home loan interest and principal certificate for Section 24 and 80C tax filing.', 'CLOSED', 'Generated and shared provisional tax certificate in Reports module.', '2025-01-18 09:45:00', '2025-01-18 15:10:00'),
  (4, 'TKT20250004', 8, 3, NULL, 'INVESTMENT_QUERY', 'LOW', 'Enable auto-renewal on matured Fixed Deposit BNKFD2024007', 'Please confirm maturity payout credit for FD BNKFD2024007.', 'CLOSED', 'Maturity proceeds credited to Pune savings account.', '2025-05-11 10:00:00', '2025-05-11 17:00:00'),
  (5, 'TKT20250005', 9, 2, 17, 'FUNDS_TRANSFER', 'MEDIUM', 'Bulk RTGS limit enhancement for current account', 'Requesting daily RTGS limit increase from 20 Lakhs to 50 Lakhs for marble export settlements.', 'RESOLVED', 'Enhanced limit approved after verifying trade turnover.', '2025-06-14 12:30:00', '2025-06-16 14:00:00'),
  (6, 'TKT20250006', 10, 3, NULL, 'LOAN_QUERY', 'LOW', 'Moratorium period query for Education Loan BNKLN202400006', 'Clarification requested on simple interest subsidy during MCA course period.', 'CLOSED', 'Explained repayment schedule and CSIS interest breakdown.', '2025-07-02 15:00:00', '2025-07-03 11:30:00'),
  (7, 'TKT20250007', 11, 2, NULL, 'KYC_UPDATE', 'MEDIUM', 'Unable to upload PAN card PDF from mobile browser', 'My account is in PENDING_KYC state and I want to complete video KYC.', 'IN_PROGRESS', NULL, '2026-09-12 10:15:00', NULL),
  (8, 'TKT20250008', 12, 2, NULL, 'ACCOUNT_ISSUE', 'LOW', 'Name truncation on printed passbook header', 'My full legal name is 120 characters long and gets clipped on PDF export.', 'RESOLVED', 'Updated PDF statement template to wrap long multi-line customer names.', '2026-09-15 11:00:00', '2026-09-16 16:00:00'),
  (9, 'TKT20260009', 13, 3, NULL, 'FUNDS_TRANSFER', 'MEDIUM', 'Beneficiary cooling period waiver request', 'Added my cousin Rohit Sharma as beneficiary, need urgent medical transfer.', 'IN_PROGRESS', NULL, '2026-10-08 09:30:00', NULL),
  (10, 'TKT20260010', 14, 3, NULL, 'ACCOUNT_ISSUE', 'MEDIUM', 'Duplicate profile confusion at Connaught Place branch', 'Branch desk confused my account with another Rohit Kumar Sharma in Lajpat Nagar.', 'RESOLVED', 'Added distinct customer ID & PAN verification note on branch profile.', '2026-10-09 13:00:00', '2026-10-10 10:30:00'),
  (11, 'TKT20260011', 15, 2, 20, 'DISPUTED_TRANSACTION', 'CRITICAL', 'Account frozen after outbound IMPS transfer attempt', 'My account 180004000015 was frozen when transferring INR 49,999.', 'OPEN', NULL, '2026-08-21 09:00:00', NULL),
  (12, 'TKT20260012', 5, 2, 73, 'DISPUTED_TRANSACTION', 'HIGH', 'High-value RTGS transaction held for compliance verification', 'My RTGS transfer of INR 9,85,000 is showing FLAGGED status.', 'IN_PROGRESS', NULL, '2026-10-18 16:00:00', NULL),
  (13, 'TKT20260013', 6, NULL, NULL, 'TECHNICAL_ISSUE', 'LOW', 'Dark mode chart labels on Analytics Dashboard', 'Expense pie chart tooltips overlap on small 1366x768 screens.', 'OPEN', NULL, '2026-11-12 18:00:00', NULL),
  (14, 'TKT20260014', 7, 3, NULL, 'BILL_PAYMENT', 'MEDIUM', 'SBI Credit Card biller auto-pay limit update', 'Want to enable auto-pay up to INR 50,000 for my SBI Elite card.', 'RESOLVED', 'Updated customer biller configuration.', '2026-10-25 11:20:00', '2026-10-25 17:45:00');

-- ----------------------------------------------------------------------------
-- Table: ticket_messages (28 rows)
-- ----------------------------------------------------------------------------
INSERT INTO ticket_messages (message_id, ticket_id, sender_user_id, message_body, is_internal_note, created_at) VALUES
  (1, 1, 5, 'Customer Inquiry (TKT20240001): Transferred INR 28,000 via IMPS to landlord Ramesh Agarwal but receipt took 10 minutes to reflect.', 0, '2024-04-20 11:00:00'),
  (2, 1, 2, 'Bank Officer Response: Verified IMPS switch settlement; UTR confirmed credited to beneficiary bank.', 0, '2024-04-20 13:00:00'),
  (3, 2, 6, 'Customer Inquiry (TKT20240002): Paid Ghaziabad electricity bill of INR 4,944.50, amount debited failed at biller end.', 0, '2025-03-10 14:20:00'),
  (4, 2, 3, 'Bank Officer Response: Auto-reversal initiated and credited back to savings account.', 0, '2025-03-10 16:20:00'),
  (5, 3, 7, 'Customer Inquiry (TKT20240003): Need provisional home loan interest and principal certificate for Section 24 and 80C tax filing.', 0, '2025-01-18 09:45:00'),
  (6, 3, 2, 'Bank Officer Response: Generated and shared provisional tax certificate in Reports module.', 0, '2025-01-18 11:45:00'),
  (7, 4, 8, 'Customer Inquiry (TKT20250004): Please confirm maturity payout credit for FD BNKFD2024007.', 0, '2025-05-11 10:00:00'),
  (8, 4, 3, 'Bank Officer Response: Maturity proceeds credited to Pune savings account.', 0, '2025-05-11 12:00:00'),
  (9, 5, 9, 'Customer Inquiry (TKT20250005): Requesting daily RTGS limit increase from 20 Lakhs to 50 Lakhs for marble export settlements.', 0, '2025-06-14 12:30:00'),
  (10, 5, 2, 'Bank Officer Response: Enhanced limit approved after verifying trade turnover.', 0, '2025-06-14 14:30:00'),
  (11, 6, 10, 'Customer Inquiry (TKT20250006): Clarification requested on simple interest subsidy during MCA course period.', 0, '2025-07-02 15:00:00'),
  (12, 6, 3, 'Bank Officer Response: Explained repayment schedule and CSIS interest breakdown.', 0, '2025-07-02 17:00:00'),
  (13, 7, 11, 'Customer Inquiry (TKT20250007): My account is in PENDING_KYC state and I want to complete video KYC.', 0, '2026-09-12 10:15:00'),
  (14, 7, 2, 'Bank Officer Response: Thank you for contacting BankEase Support. A Bank Officer is reviewing your request and verifying the ledger records.', 0, '2026-09-12 12:15:00'),
  (15, 8, 12, 'Customer Inquiry (TKT20250008): My full legal name is 120 characters long and gets clipped on PDF export.', 0, '2026-09-15 11:00:00'),
  (16, 8, 2, 'Bank Officer Response: Updated PDF statement template to wrap long multi-line customer names.', 0, '2026-09-15 13:00:00'),
  (17, 9, 13, 'Customer Inquiry (TKT20260009): Added my cousin Rohit Sharma as beneficiary, need urgent medical transfer.', 0, '2026-10-08 09:30:00'),
  (18, 9, 3, 'Bank Officer Response: Thank you for contacting BankEase Support. A Bank Officer is reviewing your request and verifying the ledger records.', 0, '2026-10-08 11:30:00'),
  (19, 10, 14, 'Customer Inquiry (TKT20260010): Branch desk confused my account with another Rohit Kumar Sharma in Lajpat Nagar.', 0, '2026-10-09 13:00:00'),
  (20, 10, 3, 'Bank Officer Response: Added distinct customer ID & PAN verification note on branch profile.', 0, '2026-10-09 15:00:00'),
  (21, 11, 15, 'Customer Inquiry (TKT20260011): My account 180004000015 was frozen when transferring INR 49,999.', 0, '2026-08-21 09:00:00'),
  (22, 11, 2, 'Bank Officer Response: Thank you for contacting BankEase Support. A Bank Officer is reviewing your request and verifying the ledger records.', 0, '2026-08-21 11:00:00'),
  (23, 12, 5, 'Customer Inquiry (TKT20260012): My RTGS transfer of INR 9,85,000 is showing FLAGGED status.', 0, '2026-10-18 16:00:00'),
  (24, 12, 2, 'Bank Officer Response: Thank you for contacting BankEase Support. A Bank Officer is reviewing your request and verifying the ledger records.', 0, '2026-10-18 18:00:00'),
  (25, 13, 6, 'Customer Inquiry (TKT20260013): Expense pie chart tooltips overlap on small 1366x768 screens.', 0, '2026-11-12 18:00:00'),
  (26, 13, 2, 'Bank Officer Response: Thank you for contacting BankEase Support. A Bank Officer is reviewing your request and verifying the ledger records.', 0, '2026-11-12 20:00:00'),
  (27, 14, 7, 'Customer Inquiry (TKT20260014): Want to enable auto-pay up to INR 50,000 for my SBI Elite card.', 0, '2026-10-25 11:20:00'),
  (28, 14, 3, 'Bank Officer Response: Updated customer biller configuration.', 0, '2026-10-25 13:20:00');

-- ----------------------------------------------------------------------------
-- Table: kyc_documents (15 rows)
-- ----------------------------------------------------------------------------
INSERT INTO kyc_documents (kyc_doc_id, user_id, verified_by_officer_id, document_type, document_number_masked, file_path, verification_status, rejection_reason, uploaded_at, verified_at) VALUES
  (1, 5, 2, 'PAN_CARD', 'AEFPG5678E', '/media/kyc/user_5_pan.pdf', 'VERIFIED', NULL, '2024-02-10 11:20:00', '2024-02-11 10:00:00'),
  (2, 5, 2, 'AADHAAR_CARD', 'XXXX-XXXX-1122', '/media/kyc/user_5_aadhaar.pdf', 'VERIFIED', NULL, '2024-02-10 11:22:00', '2024-02-11 10:05:00'),
  (3, 6, 3, 'PAN_CARD', 'AFGPS6789F', '/media/kyc/user_6_pan.pdf', 'VERIFIED', NULL, '2024-02-15 12:35:00', '2024-02-16 09:00:00'),
  (4, 6, 3, 'AADHAAR_CARD', 'XXXX-XXXX-2233', '/media/kyc/user_6_aadhaar.pdf', 'VERIFIED', NULL, '2024-02-15 12:36:00', '2024-02-16 09:05:00'),
  (5, 7, 2, 'PAN_CARD', 'AGHPR7890G', '/media/kyc/user_7_pan.pdf', 'VERIFIED', NULL, '2024-03-01 15:10:00', '2024-03-02 11:00:00'),
  (6, 7, 2, 'PASSPORT', 'Z4455667', '/media/kyc/user_7_passport.pdf', 'VERIFIED', NULL, '2024-03-01 15:12:00', '2024-03-02 11:10:00'),
  (7, 8, 3, 'PAN_CARD', 'AHIPK8901H', '/media/kyc/user_8_pan.pdf', 'VERIFIED', NULL, '2024-03-12 10:30:00', '2024-03-13 14:00:00'),
  (8, 8, 3, 'AADHAAR_CARD', 'XXXX-XXXX-4455', '/media/kyc/user_8_aadhaar.pdf', 'VERIFIED', NULL, '2024-03-12 10:32:00', '2024-03-13 14:05:00'),
  (9, 9, 2, 'PAN_CARD', 'AIJPC9012J', '/media/kyc/user_9_pan.pdf', 'VERIFIED', NULL, '2024-04-05 14:20:00', '2024-04-06 10:30:00'),
  (10, 10, 3, 'PAN_CARD', 'AJKPK0123K', '/media/kyc/user_10_pan.pdf', 'VERIFIED', NULL, '2024-04-18 17:00:00', '2024-04-19 11:15:00'),
  (11, 11, NULL, 'VOTER_ID', 'DL/01/099/112233', '/media/kyc/user_11_voter.pdf', 'PENDING', NULL, '2025-01-10 10:15:00', NULL),
  (12, 12, 2, 'PAN_CARD', 'AMXLN9999M', '/media/kyc/user_12_pan.pdf', 'VERIFIED', NULL, '2025-02-01 09:30:00', '2025-02-01 16:00:00'),
  (13, 13, 3, 'PAN_CARD', 'AROHS1111R', '/media/kyc/user_13_pan.pdf', 'VERIFIED', NULL, '2025-03-15 10:45:00', '2025-03-15 17:00:00'),
  (14, 14, 3, 'PAN_CARD', 'AROHS1112R', '/media/kyc/user_14_pan.pdf', 'VERIFIED', NULL, '2025-03-16 11:45:00', '2025-03-16 18:00:00'),
  (15, 15, 2, 'PAN_CARD', 'ALOCK5555Z', '/media/kyc/user_15_pan_blurred.pdf', 'REJECTED', 'Document image tampered and name mismatch with NSDL database.', '2025-05-20 08:30:00', '2025-05-21 12:00:00');

-- ----------------------------------------------------------------------------
-- Table: security_audit_logs (60 rows)
-- ----------------------------------------------------------------------------
INSERT INTO security_audit_logs (audit_id, user_id, event_category, severity, ip_address, user_agent, resource_target, event_description, is_suspicious, created_at) VALUES
  (1, 1, 'AUTH_LOGIN', 'INFO', '103.48.21.11', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-2/resource/1', 'Successful JWT login session established via OTP verification', 0, '2024-04-15 09:00:00'),
  (2, 2, 'KYC_REVIEW', 'INFO', '103.48.22.12', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-3/resource/2', 'Bank Officer verified customer KYC document against NSDL/UIDAI', 0, '2024-04-29 10:00:00'),
  (3, 3, 'PASSWORD_CHANGE', 'INFO', '103.48.23.13', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-4/resource/3', 'User rotated net banking login password and invalidated old refresh tokens', 0, '2024-05-13 11:00:00'),
  (4, 4, 'DATA_EXPORT', 'INFO', '103.48.24.14', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-5/resource/4', 'User downloaded encrypted PDF financial statement', 0, '2024-05-27 12:00:00'),
  (5, 5, 'AUTH_FAILED', 'WARNING', '103.48.25.15', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-6/resource/5', 'Invalid password or expired OTP entered during login flow', 0, '2024-06-10 13:00:00'),
  (6, 6, 'HIGH_VALUE_TX', 'CRITICAL', '103.48.26.16', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-7/resource/6', 'Transaction exceeded AML threshold and was flagged for compliance review', 1, '2024-06-24 14:00:00'),
  (7, 7, 'ACCOUNT_LOCK', 'CRITICAL', '103.48.27.17', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-8/resource/7', 'Account locked automatically after consecutive failed authentication attempts', 1, '2024-07-08 15:00:00'),
  (8, 8, 'ACCOUNT_STATUS_CHANGE', 'WARNING', '103.48.28.18', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-9/resource/8', 'Bank Officer updated account operational status to FROZEN/ACTIVE', 0, '2024-07-22 16:00:00'),
  (9, 9, 'AUTH_LOGIN', 'INFO', '103.48.29.19', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-10/resource/9', 'Successful JWT login session established via OTP verification', 0, '2024-08-05 17:00:00'),
  (10, 10, 'KYC_REVIEW', 'INFO', '103.48.30.20', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-1/resource/10', 'Bank Officer verified customer KYC document against NSDL/UIDAI', 0, '2024-08-19 18:00:00'),
  (11, 11, 'PASSWORD_CHANGE', 'INFO', '103.48.31.21', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-2/resource/11', 'User rotated net banking login password and invalidated old refresh tokens', 0, '2024-09-02 19:00:00'),
  (12, 12, 'DATA_EXPORT', 'INFO', '103.48.32.22', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-3/resource/12', 'User downloaded encrypted PDF financial statement', 0, '2024-09-16 08:00:00'),
  (13, 13, 'AUTH_FAILED', 'WARNING', '103.48.33.23', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-4/resource/13', 'Invalid password or expired OTP entered during login flow', 0, '2024-09-30 09:00:00'),
  (14, 14, 'HIGH_VALUE_TX', 'CRITICAL', '103.48.34.24', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-5/resource/14', 'Transaction exceeded AML threshold and was flagged for compliance review', 1, '2024-10-14 10:00:00'),
  (15, 15, 'AUTH_FAILED', 'CRITICAL', '103.48.35.25', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-6/resource/15', 'Brute-force login attempt detected from untrusted IP on locked account', 1, '2024-10-28 11:00:00'),
  (16, 1, 'ACCOUNT_STATUS_CHANGE', 'WARNING', '103.48.36.26', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-7/resource/16', 'Bank Officer updated account operational status to FROZEN/ACTIVE', 0, '2024-11-11 12:00:00'),
  (17, 2, 'AUTH_LOGIN', 'INFO', '103.48.37.27', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-8/resource/17', 'Successful JWT login session established via OTP verification', 0, '2024-11-25 13:00:00'),
  (18, 3, 'KYC_REVIEW', 'INFO', '103.48.38.28', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-9/resource/18', 'Bank Officer verified customer KYC document against NSDL/UIDAI', 0, '2024-12-09 14:00:00'),
  (19, 4, 'PASSWORD_CHANGE', 'INFO', '103.48.39.29', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-10/resource/19', 'User rotated net banking login password and invalidated old refresh tokens', 0, '2024-12-23 15:00:00'),
  (20, 5, 'DATA_EXPORT', 'INFO', '103.48.40.30', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-1/resource/20', 'User downloaded encrypted PDF financial statement', 0, '2025-01-06 16:00:00'),
  (21, 6, 'AUTH_FAILED', 'WARNING', '103.48.41.31', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-2/resource/21', 'Invalid password or expired OTP entered during login flow', 0, '2025-01-20 17:00:00'),
  (22, 7, 'HIGH_VALUE_TX', 'CRITICAL', '103.48.42.32', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-3/resource/22', 'Transaction exceeded AML threshold and was flagged for compliance review', 1, '2025-02-03 18:00:00'),
  (23, 8, 'ACCOUNT_LOCK', 'CRITICAL', '103.48.43.33', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-4/resource/23', 'Account locked automatically after consecutive failed authentication attempts', 1, '2025-02-17 19:00:00'),
  (24, 9, 'ACCOUNT_STATUS_CHANGE', 'WARNING', '103.48.44.34', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-5/resource/24', 'Bank Officer updated account operational status to FROZEN/ACTIVE', 0, '2025-03-03 08:00:00'),
  (25, 10, 'AUTH_LOGIN', 'INFO', '103.48.45.35', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-6/resource/25', 'Successful JWT login session established via OTP verification', 0, '2025-03-17 09:00:00'),
  (26, 11, 'KYC_REVIEW', 'INFO', '103.48.46.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-7/resource/26', 'Bank Officer verified customer KYC document against NSDL/UIDAI', 0, '2025-03-31 10:00:00'),
  (27, 12, 'PASSWORD_CHANGE', 'INFO', '103.48.47.37', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-8/resource/27', 'User rotated net banking login password and invalidated old refresh tokens', 0, '2025-04-14 11:00:00'),
  (28, 13, 'DATA_EXPORT', 'INFO', '103.48.48.38', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-9/resource/28', 'User downloaded encrypted PDF financial statement', 0, '2025-04-28 12:00:00'),
  (29, 14, 'AUTH_FAILED', 'WARNING', '103.48.49.39', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-10/resource/29', 'Invalid password or expired OTP entered during login flow', 0, '2025-05-12 13:00:00'),
  (30, 15, 'AUTH_FAILED', 'CRITICAL', '103.48.50.40', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-1/resource/30', 'Brute-force login attempt detected from untrusted IP on locked account', 1, '2025-05-26 14:00:00'),
  (31, 1, 'ACCOUNT_LOCK', 'CRITICAL', '103.48.51.41', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-2/resource/31', 'Account locked automatically after consecutive failed authentication attempts', 1, '2025-06-09 15:00:00'),
  (32, 2, 'ACCOUNT_STATUS_CHANGE', 'WARNING', '103.48.52.42', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-3/resource/32', 'Bank Officer updated account operational status to FROZEN/ACTIVE', 0, '2025-06-23 16:00:00'),
  (33, 3, 'AUTH_LOGIN', 'INFO', '103.48.53.43', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-4/resource/33', 'Successful JWT login session established via OTP verification', 0, '2025-07-07 17:00:00'),
  (34, 4, 'KYC_REVIEW', 'INFO', '103.48.54.44', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-5/resource/34', 'Bank Officer verified customer KYC document against NSDL/UIDAI', 0, '2025-07-21 18:00:00'),
  (35, 5, 'PASSWORD_CHANGE', 'INFO', '103.48.55.45', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-6/resource/35', 'User rotated net banking login password and invalidated old refresh tokens', 0, '2025-08-04 19:00:00'),
  (36, 6, 'DATA_EXPORT', 'INFO', '103.48.56.46', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-7/resource/36', 'User downloaded encrypted PDF financial statement', 0, '2025-08-18 08:00:00'),
  (37, 7, 'AUTH_FAILED', 'WARNING', '103.48.57.47', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-8/resource/37', 'Invalid password or expired OTP entered during login flow', 0, '2025-09-01 09:00:00'),
  (38, 8, 'HIGH_VALUE_TX', 'CRITICAL', '103.48.58.48', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-9/resource/38', 'Transaction exceeded AML threshold and was flagged for compliance review', 1, '2025-09-15 10:00:00'),
  (39, 9, 'ACCOUNT_LOCK', 'CRITICAL', '103.48.59.49', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-10/resource/39', 'Account locked automatically after consecutive failed authentication attempts', 1, '2025-09-29 11:00:00'),
  (40, 10, 'ACCOUNT_STATUS_CHANGE', 'WARNING', '103.48.60.50', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-1/resource/40', 'Bank Officer updated account operational status to FROZEN/ACTIVE', 0, '2025-10-13 12:00:00'),
  (41, 11, 'AUTH_LOGIN', 'INFO', '103.48.61.51', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-2/resource/41', 'Successful JWT login session established via OTP verification', 0, '2025-10-27 13:00:00'),
  (42, 12, 'KYC_REVIEW', 'INFO', '103.48.62.52', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-3/resource/42', 'Bank Officer verified customer KYC document against NSDL/UIDAI', 0, '2025-11-10 14:00:00'),
  (43, 13, 'PASSWORD_CHANGE', 'INFO', '103.48.63.53', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-4/resource/43', 'User rotated net banking login password and invalidated old refresh tokens', 0, '2025-11-24 15:00:00'),
  (44, 14, 'DATA_EXPORT', 'INFO', '103.48.64.54', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-5/resource/44', 'User downloaded encrypted PDF financial statement', 0, '2025-12-08 16:00:00'),
  (45, 15, 'AUTH_FAILED', 'CRITICAL', '103.48.65.55', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-6/resource/45', 'Brute-force login attempt detected from untrusted IP on locked account', 1, '2025-12-22 17:00:00'),
  (46, 1, 'HIGH_VALUE_TX', 'CRITICAL', '103.48.66.56', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-7/resource/46', 'Transaction exceeded AML threshold and was flagged for compliance review', 1, '2026-01-05 18:00:00'),
  (47, 2, 'ACCOUNT_LOCK', 'CRITICAL', '103.48.67.57', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-8/resource/47', 'Account locked automatically after consecutive failed authentication attempts', 1, '2026-01-19 19:00:00'),
  (48, 3, 'ACCOUNT_STATUS_CHANGE', 'WARNING', '103.48.68.58', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-9/resource/48', 'Bank Officer updated account operational status to FROZEN/ACTIVE', 0, '2026-02-02 08:00:00'),
  (49, 4, 'AUTH_LOGIN', 'INFO', '103.48.69.59', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-10/resource/49', 'Successful JWT login session established via OTP verification', 0, '2026-02-16 09:00:00'),
  (50, 5, 'KYC_REVIEW', 'INFO', '103.48.20.60', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-1/resource/50', 'Bank Officer verified customer KYC document against NSDL/UIDAI', 0, '2026-03-02 10:00:00'),
  (51, 6, 'PASSWORD_CHANGE', 'INFO', '103.48.21.61', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-2/resource/51', 'User rotated net banking login password and invalidated old refresh tokens', 0, '2026-03-16 11:00:00'),
  (52, 7, 'DATA_EXPORT', 'INFO', '103.48.22.62', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-3/resource/52', 'User downloaded encrypted PDF financial statement', 0, '2026-03-30 12:00:00'),
  (53, 8, 'AUTH_FAILED', 'WARNING', '103.48.23.63', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-4/resource/53', 'Invalid password or expired OTP entered during login flow', 0, '2026-04-13 13:00:00'),
  (54, 9, 'HIGH_VALUE_TX', 'CRITICAL', '103.48.24.64', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-5/resource/54', 'Transaction exceeded AML threshold and was flagged for compliance review', 1, '2026-04-27 14:00:00'),
  (55, 10, 'ACCOUNT_LOCK', 'CRITICAL', '103.48.25.65', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-6/resource/55', 'Account locked automatically after consecutive failed authentication attempts', 1, '2026-05-11 15:00:00'),
  (56, 11, 'ACCOUNT_STATUS_CHANGE', 'WARNING', '103.48.26.66', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-7/resource/56', 'Bank Officer updated account operational status to FROZEN/ACTIVE', 0, '2026-05-25 16:00:00'),
  (57, 12, 'AUTH_LOGIN', 'INFO', '103.48.27.67', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-8/resource/57', 'Successful JWT login session established via OTP verification', 0, '2026-06-08 17:00:00'),
  (58, 13, 'KYC_REVIEW', 'INFO', '103.48.28.68', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-9/resource/58', 'Bank Officer verified customer KYC document against NSDL/UIDAI', 0, '2026-06-22 18:00:00'),
  (59, 14, 'PASSWORD_CHANGE', 'INFO', '103.48.29.69', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-10/resource/59', 'User rotated net banking login password and invalidated old refresh tokens', 0, '2026-07-06 19:00:00'),
  (60, 15, 'AUTH_FAILED', 'CRITICAL', '103.48.30.70', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36', '/api/v1/module-1/resource/60', 'Brute-force login attempt detected from untrusted IP on locked account', 1, '2026-07-20 08:00:00');

-- ----------------------------------------------------------------------------
-- Table: notifications (60 rows)
-- ----------------------------------------------------------------------------
INSERT INTO notifications (notification_id, user_id, notification_type, priority, title, message, channel, is_read, read_at, created_at) VALUES
  (1, 5, 'TRANSACTION', 'HIGH', 'Account Debited via IMPS/NEFT (#1)', 'Your BankEase account was debited for an outward fund transfer. Check statement for UTR details.', 'IN_APP', 1, '2024-05-14 14:00:00', '2024-05-14 10:00:00'),
  (2, 6, 'TRANSACTION', 'NORMAL', 'Inward Credit Received (#2)', 'Funds have been credited to your BankEase account via NEFT/RTGS.', 'EMAIL', 1, '2024-05-27 15:00:00', '2024-05-27 11:00:00'),
  (3, 7, 'BILL_REMINDER', 'NORMAL', 'Upcoming Utility Bill Due in 3 Days (#3)', 'Your registered utility biller has an upcoming due date. Ensure sufficient balance for Auto-Pay.', 'IN_APP', 1, '2024-06-09 16:00:00', '2024-06-09 12:00:00'),
  (4, 8, 'LOAN_ALERT', 'HIGH', 'Monthly Loan EMI Auto-Debit Confirmation (#4)', 'Your monthly loan EMI installment has been processed successfully towards your active loan.', 'SMS', 1, '2024-06-22 17:00:00', '2024-06-22 13:00:00'),
  (5, 9, 'INVESTMENT_UPDATE', 'NORMAL', 'Quarterly FD Interest Credited (#5)', 'Quarterly compounded interest has been accrued on your active Fixed Deposit portfolio.', 'IN_APP', 1, '2024-07-05 18:00:00', '2024-07-05 14:00:00'),
  (6, 10, 'SECURITY', 'CRITICAL', 'New Device Login Detected (#6)', 'Your BankEase profile was accessed from a new browser session. Contact support if unrecognized.', 'EMAIL', 1, '2024-07-18 19:00:00', '2024-07-18 15:00:00'),
  (7, 11, 'SUPPORT_UPDATE', 'NORMAL', 'Bank Officer Replied to Your Support Ticket (#7)', 'An update has been posted on your support ticket in the Customer Support portal.', 'IN_APP', 1, '2024-07-31 20:00:00', '2024-07-31 16:00:00'),
  (8, 12, 'TRANSACTION', 'HIGH', 'Account Debited via IMPS/NEFT (#8)', 'Your BankEase account was debited for an outward fund transfer. Check statement for UTR details.', 'IN_APP', 1, '2024-08-13 21:00:00', '2024-08-13 17:00:00'),
  (9, 13, 'TRANSACTION', 'NORMAL', 'Inward Credit Received (#9)', 'Funds have been credited to your BankEase account via NEFT/RTGS.', 'EMAIL', 1, '2024-08-26 22:00:00', '2024-08-26 18:00:00'),
  (10, 14, 'BILL_REMINDER', 'NORMAL', 'Upcoming Utility Bill Due in 3 Days (#10)', 'Your registered utility biller has an upcoming due date. Ensure sufficient balance for Auto-Pay.', 'IN_APP', 1, '2024-09-08 13:00:00', '2024-09-08 09:00:00'),
  (11, 15, 'LOAN_ALERT', 'HIGH', 'Monthly Loan EMI Auto-Debit Confirmation (#11)', 'Your monthly loan EMI installment has been processed successfully towards your active loan.', 'SMS', 1, '2024-09-21 14:00:00', '2024-09-21 10:00:00'),
  (12, 5, 'INVESTMENT_UPDATE', 'NORMAL', 'Quarterly FD Interest Credited (#12)', 'Quarterly compounded interest has been accrued on your active Fixed Deposit portfolio.', 'IN_APP', 1, '2024-10-04 15:00:00', '2024-10-04 11:00:00'),
  (13, 6, 'SECURITY', 'CRITICAL', 'New Device Login Detected (#13)', 'Your BankEase profile was accessed from a new browser session. Contact support if unrecognized.', 'EMAIL', 1, '2024-10-17 16:00:00', '2024-10-17 12:00:00'),
  (14, 7, 'SUPPORT_UPDATE', 'NORMAL', 'Bank Officer Replied to Your Support Ticket (#14)', 'An update has been posted on your support ticket in the Customer Support portal.', 'IN_APP', 1, '2024-10-30 17:00:00', '2024-10-30 13:00:00'),
  (15, 8, 'TRANSACTION', 'HIGH', 'Account Debited via IMPS/NEFT (#15)', 'Your BankEase account was debited for an outward fund transfer. Check statement for UTR details.', 'IN_APP', 1, '2024-11-12 18:00:00', '2024-11-12 14:00:00'),
  (16, 9, 'TRANSACTION', 'NORMAL', 'Inward Credit Received (#16)', 'Funds have been credited to your BankEase account via NEFT/RTGS.', 'EMAIL', 1, '2024-11-25 19:00:00', '2024-11-25 15:00:00'),
  (17, 10, 'BILL_REMINDER', 'NORMAL', 'Upcoming Utility Bill Due in 3 Days (#17)', 'Your registered utility biller has an upcoming due date. Ensure sufficient balance for Auto-Pay.', 'IN_APP', 1, '2024-12-08 20:00:00', '2024-12-08 16:00:00'),
  (18, 11, 'LOAN_ALERT', 'HIGH', 'Monthly Loan EMI Auto-Debit Confirmation (#18)', 'Your monthly loan EMI installment has been processed successfully towards your active loan.', 'SMS', 1, '2024-12-21 21:00:00', '2024-12-21 17:00:00'),
  (19, 12, 'INVESTMENT_UPDATE', 'NORMAL', 'Quarterly FD Interest Credited (#19)', 'Quarterly compounded interest has been accrued on your active Fixed Deposit portfolio.', 'IN_APP', 1, '2025-01-03 22:00:00', '2025-01-03 18:00:00'),
  (20, 13, 'SECURITY', 'CRITICAL', 'New Device Login Detected (#20)', 'Your BankEase profile was accessed from a new browser session. Contact support if unrecognized.', 'EMAIL', 1, '2025-01-16 13:00:00', '2025-01-16 09:00:00'),
  (21, 14, 'SUPPORT_UPDATE', 'NORMAL', 'Bank Officer Replied to Your Support Ticket (#21)', 'An update has been posted on your support ticket in the Customer Support portal.', 'IN_APP', 1, '2025-01-29 14:00:00', '2025-01-29 10:00:00'),
  (22, 15, 'TRANSACTION', 'HIGH', 'Account Debited via IMPS/NEFT (#22)', 'Your BankEase account was debited for an outward fund transfer. Check statement for UTR details.', 'IN_APP', 1, '2025-02-11 15:00:00', '2025-02-11 11:00:00'),
  (23, 5, 'TRANSACTION', 'NORMAL', 'Inward Credit Received (#23)', 'Funds have been credited to your BankEase account via NEFT/RTGS.', 'EMAIL', 1, '2025-02-24 16:00:00', '2025-02-24 12:00:00'),
  (24, 6, 'BILL_REMINDER', 'NORMAL', 'Upcoming Utility Bill Due in 3 Days (#24)', 'Your registered utility biller has an upcoming due date. Ensure sufficient balance for Auto-Pay.', 'IN_APP', 1, '2025-03-09 17:00:00', '2025-03-09 13:00:00'),
  (25, 7, 'LOAN_ALERT', 'HIGH', 'Monthly Loan EMI Auto-Debit Confirmation (#25)', 'Your monthly loan EMI installment has been processed successfully towards your active loan.', 'SMS', 1, '2025-03-22 18:00:00', '2025-03-22 14:00:00'),
  (26, 8, 'INVESTMENT_UPDATE', 'NORMAL', 'Quarterly FD Interest Credited (#26)', 'Quarterly compounded interest has been accrued on your active Fixed Deposit portfolio.', 'IN_APP', 1, '2025-04-04 19:00:00', '2025-04-04 15:00:00'),
  (27, 9, 'SECURITY', 'CRITICAL', 'New Device Login Detected (#27)', 'Your BankEase profile was accessed from a new browser session. Contact support if unrecognized.', 'EMAIL', 1, '2025-04-17 20:00:00', '2025-04-17 16:00:00'),
  (28, 10, 'SUPPORT_UPDATE', 'NORMAL', 'Bank Officer Replied to Your Support Ticket (#28)', 'An update has been posted on your support ticket in the Customer Support portal.', 'IN_APP', 1, '2025-04-30 21:00:00', '2025-04-30 17:00:00'),
  (29, 11, 'TRANSACTION', 'HIGH', 'Account Debited via IMPS/NEFT (#29)', 'Your BankEase account was debited for an outward fund transfer. Check statement for UTR details.', 'IN_APP', 1, '2025-05-13 22:00:00', '2025-05-13 18:00:00'),
  (30, 12, 'TRANSACTION', 'NORMAL', 'Inward Credit Received (#30)', 'Funds have been credited to your BankEase account via NEFT/RTGS.', 'EMAIL', 1, '2025-05-26 13:00:00', '2025-05-26 09:00:00'),
  (31, 13, 'BILL_REMINDER', 'NORMAL', 'Upcoming Utility Bill Due in 3 Days (#31)', 'Your registered utility biller has an upcoming due date. Ensure sufficient balance for Auto-Pay.', 'IN_APP', 1, '2025-06-08 14:00:00', '2025-06-08 10:00:00'),
  (32, 14, 'LOAN_ALERT', 'HIGH', 'Monthly Loan EMI Auto-Debit Confirmation (#32)', 'Your monthly loan EMI installment has been processed successfully towards your active loan.', 'SMS', 1, '2025-06-21 15:00:00', '2025-06-21 11:00:00'),
  (33, 15, 'INVESTMENT_UPDATE', 'NORMAL', 'Quarterly FD Interest Credited (#33)', 'Quarterly compounded interest has been accrued on your active Fixed Deposit portfolio.', 'IN_APP', 1, '2025-07-04 16:00:00', '2025-07-04 12:00:00'),
  (34, 5, 'SECURITY', 'CRITICAL', 'New Device Login Detected (#34)', 'Your BankEase profile was accessed from a new browser session. Contact support if unrecognized.', 'EMAIL', 1, '2025-07-17 17:00:00', '2025-07-17 13:00:00'),
  (35, 6, 'SUPPORT_UPDATE', 'NORMAL', 'Bank Officer Replied to Your Support Ticket (#35)', 'An update has been posted on your support ticket in the Customer Support portal.', 'IN_APP', 1, '2025-07-30 18:00:00', '2025-07-30 14:00:00'),
  (36, 7, 'TRANSACTION', 'HIGH', 'Account Debited via IMPS/NEFT (#36)', 'Your BankEase account was debited for an outward fund transfer. Check statement for UTR details.', 'IN_APP', 1, '2025-08-12 19:00:00', '2025-08-12 15:00:00'),
  (37, 8, 'TRANSACTION', 'NORMAL', 'Inward Credit Received (#37)', 'Funds have been credited to your BankEase account via NEFT/RTGS.', 'EMAIL', 1, '2025-08-25 20:00:00', '2025-08-25 16:00:00'),
  (38, 9, 'BILL_REMINDER', 'NORMAL', 'Upcoming Utility Bill Due in 3 Days (#38)', 'Your registered utility biller has an upcoming due date. Ensure sufficient balance for Auto-Pay.', 'IN_APP', 1, '2025-09-07 21:00:00', '2025-09-07 17:00:00'),
  (39, 10, 'LOAN_ALERT', 'HIGH', 'Monthly Loan EMI Auto-Debit Confirmation (#39)', 'Your monthly loan EMI installment has been processed successfully towards your active loan.', 'SMS', 1, '2025-09-20 22:00:00', '2025-09-20 18:00:00'),
  (40, 11, 'INVESTMENT_UPDATE', 'NORMAL', 'Quarterly FD Interest Credited (#40)', 'Quarterly compounded interest has been accrued on your active Fixed Deposit portfolio.', 'IN_APP', 1, '2025-10-03 13:00:00', '2025-10-03 09:00:00'),
  (41, 12, 'SECURITY', 'CRITICAL', 'New Device Login Detected (#41)', 'Your BankEase profile was accessed from a new browser session. Contact support if unrecognized.', 'EMAIL', 1, '2025-10-16 14:00:00', '2025-10-16 10:00:00'),
  (42, 13, 'SUPPORT_UPDATE', 'NORMAL', 'Bank Officer Replied to Your Support Ticket (#42)', 'An update has been posted on your support ticket in the Customer Support portal.', 'IN_APP', 1, '2025-10-29 15:00:00', '2025-10-29 11:00:00'),
  (43, 14, 'TRANSACTION', 'HIGH', 'Account Debited via IMPS/NEFT (#43)', 'Your BankEase account was debited for an outward fund transfer. Check statement for UTR details.', 'IN_APP', 0, NULL, '2025-11-11 12:00:00'),
  (44, 15, 'TRANSACTION', 'NORMAL', 'Inward Credit Received (#44)', 'Funds have been credited to your BankEase account via NEFT/RTGS.', 'EMAIL', 0, NULL, '2025-11-24 13:00:00'),
  (45, 5, 'BILL_REMINDER', 'NORMAL', 'Upcoming Utility Bill Due in 3 Days (#45)', 'Your registered utility biller has an upcoming due date. Ensure sufficient balance for Auto-Pay.', 'IN_APP', 0, NULL, '2025-12-07 14:00:00'),
  (46, 6, 'LOAN_ALERT', 'HIGH', 'Monthly Loan EMI Auto-Debit Confirmation (#46)', 'Your monthly loan EMI installment has been processed successfully towards your active loan.', 'SMS', 0, NULL, '2025-12-20 15:00:00'),
  (47, 7, 'INVESTMENT_UPDATE', 'NORMAL', 'Quarterly FD Interest Credited (#47)', 'Quarterly compounded interest has been accrued on your active Fixed Deposit portfolio.', 'IN_APP', 0, NULL, '2026-01-02 16:00:00'),
  (48, 8, 'SECURITY', 'CRITICAL', 'New Device Login Detected (#48)', 'Your BankEase profile was accessed from a new browser session. Contact support if unrecognized.', 'EMAIL', 0, NULL, '2026-01-15 17:00:00'),
  (49, 9, 'SUPPORT_UPDATE', 'NORMAL', 'Bank Officer Replied to Your Support Ticket (#49)', 'An update has been posted on your support ticket in the Customer Support portal.', 'IN_APP', 0, NULL, '2026-01-28 18:00:00'),
  (50, 10, 'TRANSACTION', 'HIGH', 'Account Debited via IMPS/NEFT (#50)', 'Your BankEase account was debited for an outward fund transfer. Check statement for UTR details.', 'IN_APP', 0, NULL, '2026-02-10 09:00:00'),
  (51, 11, 'TRANSACTION', 'NORMAL', 'Inward Credit Received (#51)', 'Funds have been credited to your BankEase account via NEFT/RTGS.', 'EMAIL', 0, NULL, '2026-02-23 10:00:00'),
  (52, 12, 'BILL_REMINDER', 'NORMAL', 'Upcoming Utility Bill Due in 3 Days (#52)', 'Your registered utility biller has an upcoming due date. Ensure sufficient balance for Auto-Pay.', 'IN_APP', 0, NULL, '2026-03-08 11:00:00'),
  (53, 13, 'LOAN_ALERT', 'HIGH', 'Monthly Loan EMI Auto-Debit Confirmation (#53)', 'Your monthly loan EMI installment has been processed successfully towards your active loan.', 'SMS', 0, NULL, '2026-03-21 12:00:00'),
  (54, 14, 'INVESTMENT_UPDATE', 'NORMAL', 'Quarterly FD Interest Credited (#54)', 'Quarterly compounded interest has been accrued on your active Fixed Deposit portfolio.', 'IN_APP', 0, NULL, '2026-04-03 13:00:00'),
  (55, 15, 'SECURITY', 'CRITICAL', 'New Device Login Detected (#55)', 'Your BankEase profile was accessed from a new browser session. Contact support if unrecognized.', 'EMAIL', 0, NULL, '2026-04-16 14:00:00'),
  (56, 5, 'SUPPORT_UPDATE', 'NORMAL', 'Bank Officer Replied to Your Support Ticket (#56)', 'An update has been posted on your support ticket in the Customer Support portal.', 'IN_APP', 0, NULL, '2026-04-29 15:00:00'),
  (57, 6, 'TRANSACTION', 'HIGH', 'Account Debited via IMPS/NEFT (#57)', 'Your BankEase account was debited for an outward fund transfer. Check statement for UTR details.', 'IN_APP', 0, NULL, '2026-05-12 16:00:00'),
  (58, 7, 'TRANSACTION', 'NORMAL', 'Inward Credit Received (#58)', 'Funds have been credited to your BankEase account via NEFT/RTGS.', 'EMAIL', 0, NULL, '2026-05-25 17:00:00'),
  (59, 8, 'BILL_REMINDER', 'NORMAL', 'Upcoming Utility Bill Due in 3 Days (#59)', 'Your registered utility biller has an upcoming due date. Ensure sufficient balance for Auto-Pay.', 'IN_APP', 0, NULL, '2026-06-07 18:00:00'),
  (60, 9, 'LOAN_ALERT', 'HIGH', 'Monthly Loan EMI Auto-Debit Confirmation (#60)', 'Your monthly loan EMI installment has been processed successfully towards your active loan.', 'SMS', 0, NULL, '2026-06-20 09:00:00');

-- ----------------------------------------------------------------------------
-- Table: report_exports (12 rows)
-- ----------------------------------------------------------------------------
INSERT INTO report_exports (report_id, generated_by_user_id, report_type, file_format, period_start, period_end, filter_summary, file_path, generated_at) VALUES
  (1, 5, 'ACCOUNT_STATEMENT', 'PDF', '2024-04-01', '2025-03-31', 'Account 180002000001 FY 2024-25 All Tx', '/exports/stmt_acc1_fy2425.pdf', '2025-04-05 10:15:00'),
  (2, 5, 'TAX_CERTIFICATE', 'PDF', '2024-04-01', '2025-03-31', 'FD TDS & Interest Certificate FY 2024-25', '/exports/tax_user5_fy2425.pdf', '2025-04-06 11:00:00'),
  (3, 6, 'ACCOUNT_STATEMENT', 'CSV', '2025-01-01', '2025-06-30', 'Account 180003000003 H1 2025', '/exports/stmt_acc3_h1_2025.csv', '2025-07-02 09:30:00'),
  (4, 7, 'LOAN_AMORTIZATION', 'PDF', '2024-07-10', '2044-07-10', 'Home Loan BNKLN202400003 240M Schedule', '/exports/loan3_amortization.pdf', '2025-01-18 15:00:00'),
  (5, 7, 'PORTFOLIO_SUMMARY', 'PDF', '2024-04-01', '2026-03-31', 'Consolidated FD & SGB Wealth Statement', '/exports/portfolio_user7_2026.pdf', '2026-04-02 18:20:00'),
  (6, 8, 'ACCOUNT_STATEMENT', 'XLSX', '2025-04-01', '2026-03-31', 'Pune Savings Account Annual Ledger', '/exports/stmt_acc7_fy2526.xlsx', '2026-04-10 14:10:00'),
  (7, 9, 'ACCOUNT_STATEMENT', 'PDF', '2025-04-01', '2026-03-31', 'Current Account 180010000008 GST Audit Ledger', '/exports/stmt_acc8_fy2526.pdf', '2026-04-15 16:45:00'),
  (8, 10, 'LOAN_AMORTIZATION', 'PDF', '2024-10-04', '2029-10-04', 'Education Loan Repayment Schedule', '/exports/loan6_schedule.pdf', '2025-07-03 11:20:00'),
  (9, 2, 'BRANCH_LIQUIDITY', 'XLSX', '2026-01-01', '2026-09-30', 'Noida Sector 62 Branch CASA & Loan Book', '/exports/branch2_liquidity_q3_2026.xlsx', '2026-10-01 17:00:00'),
  (10, 3, 'BRANCH_LIQUIDITY', 'PDF', '2026-01-01', '2026-09-30', 'Ghaziabad Crossing Republik Branch Summary', '/exports/branch3_liquidity_q3_2026.pdf', '2026-10-02 17:30:00'),
  (11, 1, 'COMPLIANCE_AUDIT', 'CSV', '2026-01-01', '2026-10-31', 'Flagged High-Value RTGS & Locked Accounts Audit', '/exports/admin_compliance_oct2026.csv', '2026-11-01 10:00:00'),
  (12, 4, 'COMPLIANCE_AUDIT', 'PDF', '2024-01-01', '2026-10-31', 'RBI Statutory Concurrent Audit Report', '/exports/auditor_statutory_2026.pdf', '2026-11-05 15:00:00');

SET FOREIGN_KEY_CHECKS = 1;
