import React, { useEffect, useState } from 'react'
import apiClient from '../api/client'

export default function AccountsSection({ user }) {
  const [accounts, setAccounts] = useState([])
  const [branches, setBranches] = useState([])
  const [selectedStatement, setSelectedStatement] = useState(null)
  const [txFilter, setTxFilter] = useState('')
  const [form, setForm] = useState({
    branch_id: '',
    account_type: 'SAVINGS',
    initial_deposit: '5000.00',
    nominee_name: '',
    nominee_relation: '',
  })
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  const isOfficer = user.role_code === 'BANK_OFFICER' || user.role_code === 'ADMIN'

  const loadData = async () => {
    try {
      const [accRes, brRes] = await Promise.all([
        apiClient.get('/accounts/'),
        apiClient.get('/auth/branches/'),
      ])
      setAccounts(accRes.data)
      setBranches(brRes.data)
    } catch {
      setError('Failed to load accounts.')
    }
  }

  useEffect(() => {
    loadData()
  }, [])

  const handleOpenAccount = async (e) => {
    e.preventDefault()
    setError('')
    setMessage('')
    try {
      await apiClient.post('/accounts/', {
        ...form,
        branch_id: form.branch_id ? Number(form.branch_id) : undefined,
      })
      setMessage('Account application submitted successfully!')
      setForm({ ...form, nominee_name: '', nominee_relation: '' })
      loadData()
    } catch (err) {
      setError(err.response?.data?.detail || 'Could not create account.')
    }
  }

  const handleStatusChange = async (accountId, newStatus) => {
    setError('')
    setMessage('')
    try {
      await apiClient.patch(`/accounts/${accountId}/status/`, { account_status: newStatus })
      setMessage(`Account #${accountId} updated to ${newStatus}.`)
      loadData()
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to update account status.')
    }
  }

  const viewStatement = async (accountId, type = txFilter) => {
    try {
      const query = type ? `?type=${type}` : ''
      const res = await apiClient.get(`/accounts/${accountId}/statement/${query}`)
      setSelectedStatement(res.data)
    } catch {
      setError('Failed to load account statement.')
    }
  }

  return (
    <div className="row g-4">
      {error && <div className="col-12"><div className="alert alert-danger py-2 small mb-0">{error}</div></div>}
      {message && <div className="col-12"><div className="alert alert-success py-2 small mb-0">{message}</div></div>}

      <div className="col-lg-8">
        <div className="card border-0 shadow-sm rounded-4">
          <div className="card-body p-4">
            <h5 className="fw-bold mb-3">
              {isOfficer ? 'All Customer Bank Accounts' : 'My Bank Accounts'}
            </h5>
            <div className="table-responsive">
              <table className="table table-hover align-middle small">
                <thead className="table-light">
                  <tr>
                    <th>Account No.</th>
                    <th>Type</th>
                    {isOfficer && <th>Owner</th>}
                    <th>Balance (INR)</th>
                    <th>Status</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {accounts.length === 0 ? (
                    <tr>
                      <td colSpan={isOfficer ? 6 : 5} className="text-center text-muted py-4">
                        No bank accounts found. Open a new account on the right.
                      </td>
                    </tr>
                  ) : (
                    accounts.map((acc) => (
                      <tr key={acc.account_id}>
                        <td className="fw-semibold">{acc.account_number}</td>
                        <td>{acc.account_type}</td>
                        {isOfficer && <td>{acc.owner_name}</td>}
                        <td className="fw-bold text-primary">₹{Number(acc.balance).toLocaleString('en-IN')}</td>
                        <td>
                          <span
                            className={`badge ${
                              acc.account_status === 'ACTIVE'
                                ? 'bg-success'
                                : acc.account_status === 'FROZEN'
                                ? 'bg-danger'
                                : 'bg-warning text-dark'
                            }`}
                          >
                            {acc.account_status}
                          </span>
                        </td>
                        <td className="d-flex gap-1 flex-wrap">
                          <button
                            className="btn btn-outline-primary btn-sm"
                            onClick={() => viewStatement(acc.account_id)}
                          >
                            Statement
                          </button>
                          {isOfficer && acc.account_status !== 'ACTIVE' && (
                            <button
                              className="btn btn-success btn-sm"
                              onClick={() => handleStatusChange(acc.account_id, 'ACTIVE')}
                            >
                              Approve
                            </button>
                          )}
                          {isOfficer && acc.account_status === 'ACTIVE' && (
                            <button
                              className="btn btn-outline-danger btn-sm"
                              onClick={() => handleStatusChange(acc.account_id, 'FROZEN')}
                            >
                              Freeze
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

        {selectedStatement && (
          <div className="card border-0 shadow-sm rounded-4 mt-4">
            <div className="card-body p-4">
              <div className="d-flex justify-content-between align-items-center mb-3 flex-wrap gap-2">
                <h6 className="fw-bold mb-0">
                  Statement: {selectedStatement.account.account_number}
                </h6>
                <div className="d-flex gap-2">
                  <select
                    className="form-select form-select-sm"
                    value={txFilter}
                    onChange={(e) => {
                      setTxFilter(e.target.value)
                      viewStatement(selectedStatement.account.account_id, e.target.value)
                    }}
                  >
                    <option value="">All Types</option>
                    <option value="DEBIT">Debit Only</option>
                    <option value="CREDIT">Credit Only</option>
                  </select>
                  <button
                    className="btn btn-sm btn-outline-secondary"
                    onClick={() => setSelectedStatement(null)}
                  >
                    Close
                  </button>
                </div>
              </div>
              <div className="table-responsive">
                <table className="table table-sm small">
                  <thead className="table-light">
                    <tr>
                      <th>UTR</th>
                      <th>Type</th>
                      <th>Channel</th>
                      <th>Amount</th>
                      <th>Balance After</th>
                      <th>Description</th>
                    </tr>
                  </thead>
                  <tbody>
                    {selectedStatement.transactions.length === 0 ? (
                      <tr>
                        <td colSpan={6} className="text-center text-muted py-3">
                          No transactions recorded yet.
                        </td>
                      </tr>
                    ) : (
                      selectedStatement.transactions.map((tx) => (
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
                          <td>₹{Number(tx.amount).toLocaleString('en-IN')}</td>
                          <td>₹{Number(tx.balance_after).toLocaleString('en-IN')}</td>
                          <td>{tx.description}</td>
                        </tr>
                      ))
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="col-lg-4">
        <div className="card border-0 shadow-sm rounded-4">
          <div className="card-body p-4">
            <h5 className="fw-bold mb-3">Open New Account</h5>
            <form onSubmit={handleOpenAccount}>
              <div className="mb-3">
                <label className="form-label small fw-semibold">Account Type</label>
                <select
                  className="form-select"
                  value={form.account_type}
                  onChange={(e) => setForm({ ...form, account_type: e.target.value })}
                >
                  <option value="SAVINGS">Savings Account</option>
                  <option value="CURRENT">Current Account</option>
                  <option value="SALARY">Salary Account</option>
                </select>
              </div>
              {branches.length > 0 && (
                <div className="mb-3">
                  <label className="form-label small fw-semibold">Branch</label>
                  <select
                    className="form-select"
                    value={form.branch_id}
                    onChange={(e) => setForm({ ...form, branch_id: e.target.value })}
                  >
                    <option value="">Default Branch</option>
                    {branches.map((b) => (
                      <option key={b.branch_id} value={b.branch_id}>
                        {b.branch_name} ({b.ifsc_code})
                      </option>
                    ))}
                  </select>
                </div>
              )}
              <div className="mb-3">
                <label className="form-label small fw-semibold">Initial Deposit (INR)</label>
                <input
                  type="number"
                  step="0.01"
                  min="0"
                  className="form-control"
                  value={form.initial_deposit}
                  onChange={(e) => setForm({ ...form, initial_deposit: e.target.value })}
                  required
                />
              </div>
              <div className="mb-3">
                <label className="form-label small fw-semibold">Nominee Name</label>
                <input
                  type="text"
                  className="form-control"
                  value={form.nominee_name}
                  onChange={(e) => setForm({ ...form, nominee_name: e.target.value })}
                />
              </div>
              <div className="mb-3">
                <label className="form-label small fw-semibold">Nominee Relation</label>
                <input
                  type="text"
                  className="form-control"
                  value={form.nominee_relation}
                  onChange={(e) => setForm({ ...form, nominee_relation: e.target.value })}
                />
              </div>
              <button type="submit" className="btn btn-primary w-100 fw-semibold">
                Submit Account Application
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  )
}
