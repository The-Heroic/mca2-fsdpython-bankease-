import React, { useEffect, useState } from 'react'
import apiClient from '../api/client'

export default function InvestmentsSection() {
  const [plans, setPlans] = useState([])
  const [accounts, setAccounts] = useState([])
  const [investments, setInvestments] = useState([])
  const [form, setForm] = useState({
    funding_account_id: '',
    plan_id: '',
    principal_amount: '25000',
    tenure_months: '12',
    auto_renew: false,
  })
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  const loadAll = async () => {
    try {
      const [planRes, accRes, invRes] = await Promise.all([
        apiClient.get('/investments/plans/'),
        apiClient.get('/accounts/'),
        apiClient.get('/investments/'),
      ])
      setPlans(planRes.data)
      setAccounts(accRes.data.filter((a) => a.account_status === 'ACTIVE'))
      setInvestments(invRes.data)
    } catch {
      setError('Failed to load investment services.')
    }
  }

  useEffect(() => {
    loadAll()
  }, [])

  const handleBook = async (e) => {
    e.preventDefault()
    setError('')
    setMessage('')
    try {
      const res = await apiClient.post('/investments/', {
        ...form,
        funding_account_id: Number(form.funding_account_id),
        plan_id: Number(form.plan_id),
        tenure_months: Number(form.tenure_months),
      })
      setMessage(`Investment booked! Certificate: ${res.data.certificate_number}`)
      loadAll()
    } catch (err) {
      const data = err.response?.data
      const firstKey = data && typeof data === 'object' ? Object.keys(data)[0] : null
      setError(firstKey ? data[firstKey]?.[0] || data[firstKey] : 'Investment booking failed.')
    }
  }

  const handleClose = async (investmentId) => {
    setError('')
    setMessage('')
    try {
      const res = await apiClient.post(`/investments/${investmentId}/close/`)
      setMessage(res.data.message)
      loadAll()
    } catch (err) {
      setError(err.response?.data?.detail || 'Could not close investment.')
    }
  }

  return (
    <div className="row g-4">
      {error && <div className="col-12"><div className="alert alert-danger py-2 small mb-0">{error}</div></div>}
      {message && <div className="col-12"><div className="alert alert-success py-2 small mb-0">{message}</div></div>}

      <div className="col-lg-5">
        <div className="card border-0 shadow-sm rounded-4">
          <div className="card-body p-4">
            <h5 className="fw-bold mb-3">Open FD / RD / Investment</h5>
            <form onSubmit={handleBook}>
              <div className="mb-3">
                <label className="form-label small fw-semibold">Investment Plan</label>
                <select
                  className="form-select"
                  value={form.plan_id}
                  onChange={(e) => setForm({ ...form, plan_id: e.target.value })}
                  required
                >
                  <option value="">Select plan...</option>
                  {plans.map((p) => (
                    <option key={p.plan_id} value={p.plan_id}>
                      {p.plan_name} ({p.expected_return_rate}% | Risk: {p.risk_level})
                    </option>
                  ))}
                </select>
              </div>
              <div className="mb-3">
                <label className="form-label small fw-semibold">Funding Account</label>
                <select
                  className="form-select"
                  value={form.funding_account_id}
                  onChange={(e) => setForm({ ...form, funding_account_id: e.target.value })}
                  required
                >
                  <option value="">Select active account...</option>
                  {accounts.map((a) => (
                    <option key={a.account_id} value={a.account_id}>
                      {a.account_number} — ₹{Number(a.balance).toLocaleString('en-IN')}
                    </option>
                  ))}
                </select>
              </div>
              <div className="row g-2 mb-3">
                <div className="col-6">
                  <label className="form-label small fw-semibold">Principal (INR)</label>
                  <input
                    type="number"
                    className="form-control"
                    value={form.principal_amount}
                    onChange={(e) => setForm({ ...form, principal_amount: e.target.value })}
                    required
                  />
                </div>
                <div className="col-6">
                  <label className="form-label small fw-semibold">Tenure (Months)</label>
                  <input
                    type="number"
                    className="form-control"
                    value={form.tenure_months}
                    onChange={(e) => setForm({ ...form, tenure_months: e.target.value })}
                    required
                  />
                </div>
              </div>
              <button type="submit" className="btn btn-primary w-100 fw-semibold">
                Book Investment
              </button>
            </form>
          </div>
        </div>
      </div>

      <div className="col-lg-7">
        <div className="card border-0 shadow-sm rounded-4">
          <div className="card-body p-4">
            <h5 className="fw-bold mb-3">My Investment Portfolio</h5>
            <div className="table-responsive">
              <table className="table table-sm table-hover small align-middle">
                <thead className="table-light">
                  <tr>
                    <th>Certificate</th>
                    <th>Plan</th>
                    <th>Principal</th>
                    <th>Projected</th>
                    <th>Status</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  {investments.length === 0 ? (
                    <tr>
                      <td colSpan={6} className="text-center text-muted py-3">
                        No investments found.
                      </td>
                    </tr>
                  ) : (
                    investments.map((inv) => (
                      <tr key={inv.investment_id}>
                        <td className="font-monospace">{inv.certificate_number}</td>
                        <td>{inv.plan_name}</td>
                        <td>₹{Number(inv.principal_amount).toLocaleString('en-IN')}</td>
                        <td className="fw-semibold text-success">
                          ₹{Number(inv.projected_maturity_amount).toLocaleString('en-IN')}
                        </td>
                        <td>
                          <span className="badge bg-info text-dark">{inv.investment_status}</span>
                        </td>
                        <td>
                          {inv.investment_status === 'ACTIVE' && (
                            <button
                              className="btn btn-outline-danger btn-sm"
                              onClick={() => handleClose(inv.investment_id)}
                            >
                              Withdraw
                            </button>
                          )}
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
