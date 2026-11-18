# BankEase (P18) — REST API Documentation

Base URL: `http://127.0.0.1:8000/api/v1`

| Module | Endpoint | Method | Auth | Description |
| :--- | :--- | :--- | :--- | :--- |
| System | `/health/` | GET | Public | API health check |
| 1. Auth | `/auth/register/` | POST | Public | Register new customer |
| 1. Auth | `/auth/login/` | POST | Public | Obtain JWT access & refresh tokens |
| 1. Auth | `/auth/refresh/` | POST | Public | Refresh JWT access token |
| 1. Auth | `/auth/me/` | GET | JWT | Current user profile |
| 1. Auth | `/auth/change-password/` | POST | JWT | Update password |
| 1. Auth | `/auth/branches/` | GET | Public | List bank branches |
| 1. Auth | `/auth/unlock-user/<id>/` | POST | Officer/Admin | Unlock locked user |
| 1. Auth | `/auth/logout/` | POST | JWT | Blacklist refresh token |
| 2. Accounts | `/accounts/` | GET, POST | JWT | List accounts / open new account |
| 2. Accounts | `/accounts/<id>/` | GET | JWT | Account details |
| 2. Accounts | `/accounts/<id>/status/` | PATCH | Officer/Admin | Approve KYC, freeze, or close |
| 2. Accounts | `/accounts/<id>/statement/` | GET | JWT | Filtered account statement |
| 3. Transfers | `/transfers/beneficiaries/` | GET, POST | JWT | List / register beneficiaries |
| 3. Transfers | `/transfers/beneficiaries/<id>/activate/` | PATCH | JWT | Activate cooling beneficiary |
| 3. Transfers | `/transfers/execute/` | POST | JWT | Atomic IMPS/NEFT/RTGS/UPI/Internal transfer |
| 3. Transfers | `/transfers/history/` | GET | JWT | Transfer history |
| 4. Bills | `/bills/directory/` | GET | JWT | List BBPS billers |
| 4. Bills | `/bills/my-billers/` | GET, POST | JWT | List / link customer billers |
| 4. Bills | `/bills/pay/` | POST | JWT | Atomic bill payment |
| 4. Bills | `/bills/history/` | GET | JWT | Bill payment history |
| 5. Loans | `/loans/products/` | GET | JWT | List loan products |
| 5. Loans | `/loans/calculate-emi/` | POST | Public | EMI calculator |
| 5. Loans | `/loans/applications/` | GET, POST | JWT | List / apply for loan |
| 5. Loans | `/loans/applications/<id>/review/` | PATCH | Officer/Admin | Approve & disburse or reject |
| 5. Loans | `/loans/applications/<id>/repayments/` | GET | JWT | View EMI schedule |
| 5. Loans | `/loans/repayments/<id>/pay/` | POST | JWT | Pay EMI installment |
| 6. Investments | `/investments/plans/` | GET | JWT | List FD/RD/MF plans |
| 6. Investments | `/investments/` | GET, POST | JWT | List / book investment |
| 6. Investments | `/investments/<id>/close/` | POST | JWT | Maturity or premature withdrawal |
| 7. Support | `/support/tickets/` | GET, POST | JWT | List / raise support tickets |
| 7. Support | `/support/tickets/<id>/messages/` | GET, POST | JWT | View / post ticket messages |
| 7. Support | `/support/tickets/<id>/status/` | PATCH | JWT | Update ticket status |
| 8. Security | `/security/kyc/` | GET, POST | JWT | List / submit KYC documents |
| 8. Security | `/security/kyc/<id>/verify/` | PATCH | Officer/Admin | Verify or reject KYC doc |
| 8. Security | `/security/audit-logs/` | GET | Staff | View security audit trail |
| 8. Security | `/security/flagged-transactions/` | GET | Staff | View flagged transactions |
| 9. Alerts | `/notifications/` | GET, POST | JWT | List / create notifications |
| 9. Alerts | `/notifications/<id>/read/` | PATCH | JWT | Mark notification read |
| 9. Alerts | `/notifications/mark-all-read/` | POST | JWT | Mark all read |
| 10. Reports | `/reports/dashboard/` | GET | JWT | Role-based KPI analytics |
| 10. Reports | `/reports/exports/` | GET, POST | JWT | List / create report exports |
| 10. Reports | `/reports/exports/<id>/download/` | GET | JWT | Download CSV report |
