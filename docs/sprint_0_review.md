# Sprint 0 Review Note (`v0.1.0`)

**Project:** P18 | BankEase - NextGen Net Banking Application  
**Sprint:** Sprint 0 (6 Hours)  
**Tag:** `v0.1.0`  

## Completed Deliverables
1. **Repository & Workflow Setup:**
   - Initialized `main` and `develop` branches with `.gitignore`, `.env.example`, and `README.md`.
   - Organized `backend/`, `frontend/`, `database/`, and `docs/` directories.
2. **3NF MySQL 8.0 Database Design & Seed Data:**
   - Created `database/schema.sql` with 20 normalized (3NF) tables covering all 10 BankEase modules.
   - Created `database/seed_data.sql` and 20 `.csv` files in `database/csv/` with Indian-context data, role accounts, and 5 validation edge-case records.
   - Documented ER cardinalities and Mermaid ER diagram in `database/er_diagram.md`.
3. **Backend & Frontend Skeleton + Login (P18-US01):**
   - Scaffolded Django 4.2 LTS + DRF + SimpleJWT in `backend/` with `accounts_auth` models (`Role`, `Branch`, `User`) and REST endpoints (`/api/v1/health/`, `/api/v1/auth/register/`, `/api/v1/auth/login/`, `/api/v1/auth/me/`, `/api/v1/auth/logout/`).
   - Verified with 3 passing `pytest` tests (`test_health_check`, `test_customer_registration_and_login_flow`, `test_account_locks_after_three_failed_attempts`).
   - Scaffolded React 18 (Vite) + Bootstrap 5 in `frontend/` with `LoginPage` and `DashboardShell`.
