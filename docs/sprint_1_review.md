# Sprint 1 Review Note (`v0.2.0`)

**Project:** P18 | BankEase - NextGen Net Banking Application  
**Sprint:** Sprint 1 (28 Hours)  
**Tag:** `v0.2.0`  

## Completed Deliverables
1. **Module 1: User Authentication Enhancements (`apps/accounts_auth`)**
   - Added `/api/v1/auth/change-password/`, `/api/v1/auth/branches/`, and officer-only `/api/v1/auth/unlock-user/<user_id>/`.
2. **Module 2: Account Management (`apps/banking_accounts`)**
   - Implemented `BankAccount` model and REST APIs for opening Savings/Current/Salary accounts, viewing account summaries, officer KYC approval/freeze/closure (`/status/`), and filtered account statements (`/statement/`).
3. **Module 3: Funds Transfer (`apps/transfers`)**
   - Implemented `Beneficiary` and `Transaction` models, IFSC validation, cooling period activation, and atomic (`transaction.atomic()` + `select_for_update()`) IMPS/NEFT/RTGS/UPI/Internal transfers with automatic UTR generation and high-value flagging.
4. **Frontend UI (`frontend/src/pages/`)**
   - Built `AccountsSection.jsx`, `TransfersSection.jsx`, and `ProfileSecuritySection.jsx` inside `DashboardShell.jsx`.
5. **Automated Tests (`pytest`)**
   - Verified 5 passing tests across Module 1, Module 2, and Module 3.
