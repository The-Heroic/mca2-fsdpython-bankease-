import React, { useEffect, useState } from 'react'
import apiClient from '../api/client'

export default function TransfersSection() {
  const [accounts, setAccounts] = useState([])
  const [beneficiaries, setBeneficiaries] = useState([])
  const [history, setHistory] = useState([])
  const [benForm, setBenForm] = useState({
    nickname: '',
    beneficiary_name: '',
    account_number: '',
    bank_name: 'BankEase Ltd',
    ifsc_code: 'BNKE0000001',
  })
  const [txForm, setTxForm] = useState({
    source_account_id: '',
    beneficiary_id: '',
    channel: 'IMPS',
    amount: '',
    remarks: '',
  })
  const [receipt, setReceipt] = useState(null)
  const [error, setError] = useState('')
  const [message, setMessage] = useState('')

  const loadAll = async () => {
    try {
      const [accRes, benRes, histRes] = await Promise.all([
        apiClient.get('/accounts/'),
        apiClient.get('/transfers/beneficiaries/'),
        apiClient.get('/transfers/history/'),
      ])
      setAccounts(accRes.data.filter((a) => a.account_status === 'ACTIVE'))
      setBeneficiaries(benRes.data)
      setHistory(histRes.data)
    } catch {
      setError('Failed to load transfer data.')
    }
  }

  useEffect(() => {
    loadAll()
  }, [])

  const handleAddBeneficiary = async (e) => {
    e.preventDefault()
    setError('')
    setMessage('')
    try {
      await apiClient.post('/transfers/beneficiaries/', benForm)
      setMessage('Beneficiary registered successfully.')
      setBenForm({
        nickname: '',
        beneficiary_name: '',
        account_number: '',
        bank_name: 'BankEase Ltd',
        ifsc_code: 'BNKE0000001',
      })
      loadAll()
    } catch (err) {
      const data = err.response?.data
      setError(data?.ifsc_code?.[0] || data?.detail || 'Could not add beneficiary.')
    }
  }

  const handleTransfer = async (e) => {
    e.preventDefault()
    setError('')
    setMessage('')
    setReceipt(null)
    try {
      const res = await apiClient.post('/transfers/execute/', {
        ...txForm,
        source_account_id: Number(txForm.source_account_id),
        beneficiary_id: Number(txForm.beneficiary_id),
      })
      setReceipt(res.data.transaction)
      setMessage('Transfer executed successfully!')
      setTxForm({ ...txForm, amount: '', remarks: '' })
      loadAll()
    } catch (err) {
      const data = err.response?.data
      const firstKey = data && typeof data === 'object' ? Object.keys(data)[0] : null
      const msg = firstKey
        ? Array.isArray(data[firstKey])
          ? data[firstKey][0]
          : data[firstKey]
        : 'Transfer failed.'
      setError(msg)
    }
  }

  return (
    <div className="row g-4">
      {error && <div className="col-12"><div className="alert alert-danger py-2 small mb-0">{error}</div></div>}
      {message && <div className="col-12"><div className="alert alert-success py-2 small mb-0">{message}</div></div>}

      <div className="col-lg-6">
        <div className="card border-0 shadow-sm rounded-4 h-100">
          <div className="card-body p-4">
            <h5 className="fw-bold mb-3">Execute Funds Transfer</h5>
            <form onSubmit={handleTransfer}>
              <div className="mb-3">
                <label className="form-label small fw-semibold">Source Account</label>
                <select
                  className="form-select"
                  value={txForm.source_account_id}
                  onChange={(e) => setTxForm({ ...txForm, source_account_id: e.target.value })}
                  required
                >
                  <option value="">Select active account...</option>
                  {accounts.map((a) => (
                    <option key={a.account_id} value={a.account_id}>
                      {a.account_number} ({a.account_type}) — ₹{Number(a.balance).toLocaleString('en-IN')}
                    </option>
                  ))}
                </select>
              </div>
              <div className="mb-3">
                <label className="form-label small fw-semibold">Beneficiary</label>
                <select
                  className="form-select"
                  value={txForm.beneficiary_id}
                  onChange={(e) => setTxForm({ ...txForm, beneficiary_id: e.target.value })}
                  required
                >
                  <option value="">Select beneficiary...</option>
                  {beneficiaries.map((b) => (
                    <option key={b.beneficiary_id} value={b.beneficiary_id}>
                      {b.beneficiary_name} ({b.ifsc_code}) [{b.status}]
                    </option>
                  ))}
                </select>
              </div>
              <div className="row g-2 mb-3">
                <div className="col-md-5">
                  <label className="form-label small fw-semibold">Channel</label>
                  <select
                    className="form-select"
                    value={txForm.channel}
                    onChange={(e) => setTxForm({ ...txForm, channel: e.target.value })}
                  >
                    <option value="IMPS">IMPS</option>
                    <option value="NEFT">NEFT</option>
                    <option value="RTGS">RTGS</option>
                    <option value="UPI">UPI</option>
                    <option value="INTERNAL">INTERNAL</option>
                  </select>
                </div>
                <div className="col-md-7">
                  <label className="form-label small fw-semibold">Amount (INR)</label>
                  <input
                    type="number"
                    step="0.01"
                    min="1"
                    className="form-control"
                    value={txForm.amount}
                    onChange={(e) => setTxForm({ ...txForm, amount: e.target.value })}
                    required
                  />
                </div>
              </div>
              <div className="mb-3">
                <label className="form-label small fw-semibold">Remarks</label>
                <input
                  type="text"
                  className="form-control"
                  placeholder="Optional payment note"
                  value={txForm.remarks}
                  onChange={(e) => setTxForm({ ...txForm, remarks: e.target.value })}
                />
              </div>
              <button type="submit" className="btn btn-primary w-100 fw-semibold">
                Send Money Securely
              </button>
            </form>

            {receipt && (
              <div className="alert alert-info mt-3 small mb-0">
                <strong>UTR Receipt:</strong> <span className="font-monospace">{receipt.reference_utr}</span>
                <br />
                Amount: ₹{Number(receipt.amount).toLocaleString('en-IN')} | New Balance: ₹
                {Number(receipt.balance_after).toLocaleString('en-IN')}
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="col-lg-6">
        <div className="card border-0 shadow-sm rounded-4 h-100">
          <div className="card-body p-4">
            <h5 className="fw-bold mb-3">Add Beneficiary</h5>
            <form onSubmit={handleAddBeneficiary}>
              <div className="row g-2 mb-2">
                <div className="col-md-6">
                  <label className="form-label small fw-semibold">Beneficiary Name</label>
                  <input
                    type="text"
                    className="form-control"
                    value={benForm.beneficiary_name}
                    onChange={(e) => setBenForm({ ...benForm, beneficiary_name: e.target.value })}
                    required
                  />
                </div>
                <div className="col-md-6">
                  <label className="form-label small fw-semibold">Nickname</label>
                  <input
                    type="text"
                    className="form-control"
                    value={benForm.nickname}
                    onChange={(e) => setBenForm({ ...benForm, nickname: e.target.value })}
                  />
                </div>
              </div>
              <div className="mb-2">
                <label className="form-label small fw-semibold">Account Number</label>
                <input
                  type="text"
                  className="form-control"
                  value={benForm.account_number}
                  onChange={(e) => setBenForm({ ...benForm, account_number: e.target.value })}
                  required
                />
              </div>
              <div className="row g-2 mb-3">
                <div className="col-md-6">
                  <label className="form-label small fw-semibold">Bank Name</label>
                  <input
                    type="text"
                    className="form-control"
                    value={benForm.bank_name}
                    onChange={(e) => setBenForm({ ...benForm, bank_name: e.target.value })}
                    required
                  />
                </div>
                <div className="col-md-6">
                  <label className="form-label small fw-semibold">IFSC Code</label>
                  <input
                    type="text"
                    className="form-control text-uppercase"
                    maxLength={11}
                    value={benForm.ifsc_code}
                    onChange={(e) => setBenForm({ ...benForm, ifsc_code: e.target.value })}
                    required
                  />
                </div>
              </div>
              <button type="submit" className="btn btn-outline-primary w-100 fw-semibold">
                Register Beneficiary
              </button>
            </form>
          </div>
        </div>
      </div>

      <div className="col-12">
        <div className="card border-0 shadow-sm rounded-4">
          <div className="card-body p-4">
            <h5 className="fw-bold mb-3">Recent Transfer History</h5>
            <div className="table-responsive">
              <table className="table table-hover table-sm small">
                <thead className="table-light">
                  <tr>
                    <th>UTR</th>
                    <th>Account</th>
                    <th>Type</th>
                    <th>Channel</th>
                    <th>Amount</th>
                    <th>Status</th>
                    <th>Description</th>
                  </tr>
                </thead>
                <tbody>
                  {history.length === 0 ? (
                    <tr>
                      <td colSpan={7} className="text-center text-muted py-3">
                        No transfers executed yet.
                      </td>
                    </tr>
                  ) : (
                    history.map((tx) => (
                      <tr key={tx.transaction_id}>
                        <td className="font-monospace">{tx.reference_utr}</td>
                        <td>{tx.account_number}</td>
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
                        <td>{tx.description}</td>
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
