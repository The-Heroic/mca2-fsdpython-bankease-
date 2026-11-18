# P18 | BankEase - NextGen Net Banking Application

**Domain:** Finance and Banking  
**Skill Track:** Full Stack Development with Python (FSD Python)  
**Institution:** ABES Engineering College | MCA 2nd Year  
**Repository:** `mca2-fsdpython-bankease`

---

## 1. Project Overview
**BankEase** is a secure, comprehensive full-stack Net Banking platform enabling **Customers**, **Bank Officers**, and **Administrators** to manage bank accounts, execute intra/inter-bank funds transfers, pay utility bills, apply for and process loans, manage investments (FD/RD/Mutual Funds), handle customer support tickets, enforce security and compliance audit trails, receive real-time notifications, and view interactive financial analytics dashboards.

## 2. Core Modules
1. **User Authentication** — Role-based access control (`Admin`, `Bank Officer`, `Customer`), JWT session management, OTP/MFA verification, password security.
2. **Account Management** — Savings, Current, and Salary accounts, KYC verification workflow, balance inquiries, account statements, freeze/unfreeze controls.
3. **Funds Transfer** — Beneficiary management with cooling period, IMPS/NEFT/RTGS/UPI/Internal transfers, daily limits, atomic transactions.
4. **Bill Payment** — Registered billers across Electricity, Water, Gas, Broadband, DTH, Mobile, and Credit Card categories, auto-pay rules, BBPS receipts.
5. **Loan Management** — Personal, Home, Vehicle, and Education loan products, EMI calculator, officer credit appraisal, disbursement, and repayment schedule tracking.
6. **Investment Services** — Fixed Deposits (FD), Recurring Deposits (RD), Mutual Fund portfolios, maturity projections, and premature withdrawal handling.
7. **Customer Support** — Multi-category support ticketing, SLA priority routing, Bank Officer resolution threads, and status tracking.
8. **Security and Compliance** — Immutable security audit trails, IP/User-Agent tracking, suspicious/high-value transaction flagging, and KYC compliance logs.
9. **Notification and Alerts** — Real-time alerts for transactions, security events, bill reminders, and loan EMIs with read/unread states.
10. **Dashboard and Reporting** — Role-based financial analytics, income vs. expense visualisations, officer work queues, and downloadable CSV/PDF reports.

## 3. Technology Stack
* **Backend:** Python 3.11+, Django 4.2 LTS, Django REST Framework (DRF), SimpleJWT
* **Frontend:** Node.js 18 LTS, React 18 (Vite), Bootstrap 5
* **Database:** MySQL 8.0 Community Server (`InnoDB`, `utf8mb4`, 3NF Normalized Schema)
* **Testing & Tooling:** Pytest, `pytest-django`, Postman, Git 2.40+

## 4. Repository Structure
```text
mca2-fsdpython-bankease/
├── backend/                  # Django 4.2 project, modular apps, requirements.txt
├── frontend/                 # React 18 (Vite + Bootstrap) single-page application
├── database/                 # MySQL 8.0 3NF DDL, seed data & ER documentation
│   ├── schema.sql            # Complete MySQL 8.0 3NF DDL script
│   ├── seed_data.sql         # Indian-context sample data & edge-case records
│   ├── er_diagram.md         # Entity-Relationship diagram & cardinality summary
│   └── csv/                  # Seed data exported as CSV files for workbench import
├── docs/                     # Flowcharts, wireframes, API docs, sprint reviews
│   └── bankease_flowchart.drawio
├── .env.example              # Environment variable template (copy to .env)
├── .gitignore                # Git ignore rules
└── README.md                 # Project setup and documentation
```

## 5. Quick Start Instructions

### Step 1: Clone & Configure Environment
```bash
git clone <repo-url>
cd mca2-fsdpython-bankease
git checkout develop
cp .env.example .env
```

### Step 2: Initialize the MySQL 8.0 Database
Run the schema and seed scripts in MySQL Workbench or via the MySQL CLI:
```bash
mysql -u root -p < database/schema.sql
mysql -u root -p bankease_db < database/seed_data.sql
```

### Step 3: Run Backend & Frontend (Sprint 0 Skeleton)
Instructions for starting the Django API server (`backend/`) and React Vite server (`frontend/`) are maintained in their respective directories.
