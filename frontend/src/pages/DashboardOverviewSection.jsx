import React, { useEffect, useState } from 'react'
import apiClient from '../api/client'

export default function DashboardOverviewSection({ user }) {
  const [dashboard, setDashboard] = useState(null)
  const [exportsList, setExportsList] = useState([])
  const [reportForm, setReportForm] = useState({
    report_type: 'ACCOUNT_STATEMENT',
    file_format: 'CSV',
    period_start: '2026-01-01',
    period_end: '2026-12-31',
  })
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  const loadAll = async () => {
    try {
      const [dashRes, expRes] = await Promise.all([
        apiClient.get('/reports/dashboard/'),
        apiClient.get('/reports/exports/'),
      ])
      setDashboard(dashRes.data)
      setExportsList(expRes.data)
    } catch {
      setError('Failed to load dashboard analytics.')
    }
  }

  useEffect(() => {
    loadAll()
  }, [])

  const handleGenerateReport = async (e) => {
    e.preventDefault()
    setError('')
    setMessage('')
    try {
      await apiClient.post('/reports/exports/', reportForm)
      setMessage('Report generated successfully!')
      loadAll()
    } catch {
      setError('Could not generate report.')
    }
  }

  if (!dashboard) {
    return <div className="text-muted small">Loading analytics...</div>
  }

  const kpis = dashboard.kpis
  const isStaff = ['ADMIN', 'BANK_OFFICER', 'AUDITOR'].includes(dashboard.role)

  return (
    <div className="row g-4">
      {error && <div className="col-12"><div className="alert alert-danger py-2 small mb-0">{error}</div></div>}
      {message && <div className="col-12"><div className="alert alert-success py-2 small mb-0">{message}</div></div>}

      <div className="col-12">
        <div className="row g-3">
          {isStaff ? (
            <>
              <div className="col-md-3">
                <div className="card border-0 shadow-sm rounded-4 p-3">
                  <div className="text-muted small">Total Bank Deposits</div>
                  <div className="fs-4 fw-bold text-primary">
                    ₹{Number(kpis.total_bank_deposits).toLocaleString('en-IN')}
                  </div>
                </div>
              </div>
              <div className="col-md-3">
                <div className="card border-0 shadow-sm rounded-4 p-3">
                  <div className="text-muted small">Pending KYC Accounts</div>
                  <div className="fs-4 fw-bold text-warning">{kpis.pending_kyc_accounts}</div>
                </div>
              </div>
              <div className="col-md-3">
                <div className="card border-0 shadow-sm rounded-4 p-3">
                  <div className="text-muted small">Pending Loan Apps</div>
                  <div className="fs-4 fw-bold text-info">{kpis.pending_loan_applications}</div>
                </div>
              </div>
              <div className="col-md-3">
                <div className="card border-0 shadow-sm rounded-4 p-3">
                  <div className="text-muted small">Flagged Transactions</div>
                  <div className="fs-4 fw-bold text-danger">{kpis.flagged_transactions}</div>
                </div>
              </div>
            </>
          ) : (
            <>
              <div className="col-md-3">
                <div className="card border-0 shadow-sm rounded-4 p-3">
                  <div className="text-muted small">Total Balance</div>
                  <div className="fs-4 fw-bold text-primary">
                    ₹{Number(kpis.total_balance).toLocaleString('en-IN')}
                  </div>
                </div>
              </div>
              <div className="col-md-3">
                <div className="card border-0 shadow-sm rounded-4 p-3">
                  <div className="text-muted small">Active Investments</div>
                  <div className="fs-4 fw-bold text-success">
                    ₹{Number(kpis.total_investments).toLocaleString('en-IN')}
                  </div>
                </div>
              </div>
              <div className="col-md-3">
                <div className="card border-0 shadow-sm rounded-4 p-3">
                  <div className="text-muted small">Total Credits</div>
                  <div className="fs-4 fw-bold text-info">
                    ₹{Number(kpis.total_credits).toLocaleString('en-IN')}
                  </div>
                </div>
              </div>
              <div className="col-md-3">
                <div className="card border-0 shadow-sm rounded-4 p-3">
                  <div className="text-muted small">Total Debits</div>
                  <div className="fs-4 fw-bold text-danger">
                    ₹{Number(kpis.total_debits).toLocaleString('en-IN')}
                  </div>
                </div>
              </div>
            </>
          )}
        </div>
      </div>

      <div className="col-lg-7">
        <div className="card border-0 shadow-sm rounded-4 h-100">
          <div className="card-body p-4">
            <h5 className="fw-bold mb-3">Recent Ledger Activity</h5>
            <div className="table-responsive">
              <table className="table table-sm table-hover small">
                <thead className="table-light">
                  <tr>
                    <th>UTR</th>
                    <th>Type</th>
                    <th>Channel</th>
                    <th>Amount</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {dashboard.recent_transactions.length === 0 ? (
                    <tr>
                      <td colSpan={5} className="text-center text-muted py-3">
                        No transactions recorded yet.
                      </td>
                    </tr>
                  ) : (
                    dashboard.recent_transactions.map((tx) => (
                      <tr key={tx.transaction_id}>
                        <td className="font-monospace">{tx.reference_utr}</td>
                        <td>
                          <span
                            className={`badge ${
                              tx.transaction_type === 'CREDIT' ? 'bg-success' : 'bg-danger'
                            }`}
                          >
                            {tx.transaction_type}
                          </span>
                        </td>
                        <td>{tx.channel}</td>
                        <td className="fw-semibold">₹{Number(tx.amount).toLocaleString('en-IN')}</td>
                        <td>{tx.status}</td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <div className="col-lg-5">
        <div className="card border-0 shadow-sm rounded-4 h-100">
          <div className="card-body p-4">
            <h5 className="fw-bold mb-3">Generate Financial Report</h5>
            <form onSubmit={handleGenerateReport}>
              <div className="mb-2">
                <label className="form-label small fw-semibold">Report Type</label>
                <select
                  className="form-select"
                  value={reportForm.report_type}
                  onChange={(e) => setReportForm({ ...reportForm, report_type: e.target.value })}
                >
                  <option value="ACCOUNT_STATEMENT">Account Statement</option>
                  <option value="TAX_CERTIFICATE">Tax Certificate</option>
                  <option value="PORTFOLIO_SUMMARY">Portfolio Summary</option>
                  <option value="COMPLIANCE_AUDIT">Compliance Audit</option>
                </select>
              </div>
              <div className="row g-2 mb-3">
                <div className="col-6">
                  <label className="form-label small fw-semibold">From</label>
                  <input
                    type="date"
                    className="form-control"
                    value={reportForm.period_start}
                    onChange={(e) => setReportForm({ ...reportForm, period_start: e.target.value })}
                    required
                  />
                </div>
                <div className="col-6">
                  <label className="form-label small fw-semibold">To</label>
                  <input
                    type="date"
                    className="form-control"
                    value={reportForm.period_end}
                    onChange={(e) => setReportForm({ ...reportForm, period_end: e.target.value })}
                    required
                  />
                </div>
              </div>
              <button type="submit" className="btn btn-primary w-100 fw-semibold">
                Export CSV Report
              </button>
            </form>

            {exportsList.length > 0 && (
              <div className="mt-3">
                <div className="small fw-bold text-muted mb-1">Recent Exports</div>
                <ul className="list-group list-group-flush small">
                  {exportsList.slice(0, 4).map((rep) => (
                    <li
                      key={rep.report_id}
                      className="list-group-item px-0 d-flex justify-content-between align-items-center"
                    >
                      <span>{rep.report_type}</span>
                      <span className="badge bg-light text-dark">{rep.file_format}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
