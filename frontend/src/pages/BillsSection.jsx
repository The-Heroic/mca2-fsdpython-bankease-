import React, { useEffect, useState } from 'react'
import apiClient from '../api/client'

export default function BillsSection() {
  const [directory, setDirectory] = useState([])
  const [myBillers, setMyBillers] = useState([])
  const [accounts, setAccounts] = useState([])
  const [history, setHistory] = useState([])
  const [linkForm, setLinkForm] = useState({
    biller: '',
    consumer_number: '',
    short_name: '',
    autopay_enabled: false,
  })
  const [payForm, setPayForm] = useState({
    customer_biller_id: '',
    account_id: '',
    bill_amount: '',
    bill_period: 'Nov-2026',
    payment_mode: 'MANUAL',
  })
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  const loadAll = async () => {
    try {
      const [dirRes, myRes, accRes, histRes] = await Promise.all([
        apiClient.get('/bills/directory/'),
        apiClient.get('/bills/my-billers/'),
        apiClient.get('/accounts/'),
        apiClient.get('/bills/history/'),
      ])
      setDirectory(dirRes.data)
      setMyBillers(myRes.data)
      setAccounts(accRes.data.filter((a) => a.account_status === 'ACTIVE'))
      setHistory(histRes.data)
    } catch {
      setError('Failed to load bill payment data.')
    }
  }

  useEffect(() => {
    loadAll()
  }, [])

  const handleLinkBiller = async (e) => {
    e.preventDefault()
    setError('')
    setMessage('')
    try {
      await apiClient.post('/bills/my-billers/', {
        ...linkForm,
        biller: Number(linkForm.biller),
      })
      setMessage('Biller linked successfully.')
      setLinkForm({ biller: '', consumer_number: '', short_name: '', autopay_enabled: false })
      loadAll()
    } catch (err) {
      setError(err.response?.data?.detail || 'Could not link biller.')
    }
  }

  const handlePayBill = async (e) => {
    e.preventDefault()
    setError('')
    setMessage('')
    try {
      const res = await apiClient.post('/bills/pay/', {
        ...payForm,
        customer_biller_id: Number(payForm.customer_biller_id),
        account_id: Number(payForm.account_id),
      })
      setMessage(`Bill paid! BBPS Ref: ${res.data.payment.bbps_ref_no}`)
      setPayForm({ ...payForm, bill_amount: '' })
      loadAll()
    } catch (err) {
      const data = err.response?.data
      const firstKey = data && typeof data === 'object' ? Object.keys(data)[0] : null
      setError(firstKey ? data[firstKey]?.[0] || data[firstKey] : 'Bill payment failed.')
    }
  }

  return (
    <div className="row g-4">
      {error && <div className="col-12"><div className="alert alert-danger py-2 small mb-0">{error}</div></div>}
      {message && <div className="col-12"><div className="alert alert-success py-2 small mb-0">{message}</div></div>}

      <div className="col-lg-6">
        <div className="card border-0 shadow-sm rounded-4 h-100">
          <div className="card-body p-4">
            <h5 className="fw-bold mb-3">Pay Utility Bill</h5>
            <form onSubmit={handlePayBill}>
              <div className="mb-3">
                <label className="form-label small fw-semibold">Registered Biller</label>
                <select
                  className="form-select"
                  value={payForm.customer_biller_id}
                  onChange={(e) => setPayForm({ ...payForm, customer_biller_id: e.target.value })}
                  required
                >
                  <option value="">Select linked biller...</option>
                  {myBillers.map((b) => (
                    <option key={b.customer_biller_id} value={b.customer_biller_id}>
                      {b.short_name || b.biller_name} ({b.consumer_number})
                    </option>
                  ))}
                </select>
              </div>
              <div className="mb-3">
                <label className="form-label small fw-semibold">Source Account</label>
                <select
                  className="form-select"
                  value={payForm.account_id}
                  onChange={(e) => setPayForm({ ...payForm, account_id: e.target.value })}
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
                <div className="col-md-4">
                  <label className="form-label small fw-semibold">Amount (INR)</label>
                  <input
                    type="number"
                    step="0.01"
                    min="1"
                    className="form-control"
                    value={payForm.bill_amount}
                    onChange={(e) => setPayForm({ ...payForm, bill_amount: e.target.value })}
                    required
                  />
                </div>
                <div className="col-md-4">
                  <label className="form-label small fw-semibold">Bill Period</label>
                  <input
                    type="text"
                    className="form-control"
                    value={payForm.bill_period}
                    onChange={(e) => setPayForm({ ...payForm, bill_period: e.target.value })}
                    required
                  />
                </div>
                <div className="col-md-4">
                  <label className="form-label small fw-semibold">Mode</label>
                  <select
                    className="form-select"
                    value={payForm.payment_mode}
                    onChange={(e) => setPayForm({ ...payForm, payment_mode: e.target.value })}
                  >
                    <option value="MANUAL">MANUAL</option>
                    <option value="AUTOPAY">AUTOPAY</option>
                  </select>
                </div>
              </div>
              <button type="submit" className="btn btn-primary w-100 fw-semibold">
                Pay Bill Now
              </button>
            </form>
          </div>
        </div>
      </div>

      <div className="col-lg-6">
        <div className="card border-0 shadow-sm rounded-4 h-100">
          <div className="card-body p-4">
            <h5 className="fw-bold mb-3">Link New Biller</h5>
            <form onSubmit={handleLinkBiller}>
              <div className="mb-3">
                <label className="form-label small fw-semibold">Select Biller</label>
                <select
                  className="form-select"
                  value={linkForm.biller}
                  onChange={(e) => setLinkForm({ ...linkForm, biller: e.target.value })}
                  required
                >
                  <option value="">Choose from BBPS directory...</option>
                  {directory.map((d) => (
                    <option key={d.biller_id} value={d.biller_id}>
                      {d.biller_name} [{d.category}]
                    </option>
                  ))}
                </select>
              </div>
              <div className="row g-2 mb-3">
                <div className="col-md-6">
                  <label className="form-label small fw-semibold">Consumer Number</label>
                  <input
                    type="text"
                    className="form-control"
                    value={linkForm.consumer_number}
                    onChange={(e) => setLinkForm({ ...linkForm, consumer_number: e.target.value })}
                    required
                  />
                </div>
                <div className="col-md-6">
                  <label className="form-label small fw-semibold">Nickname</label>
                  <input
                    type="text"
                    className="form-control"
                    value={linkForm.short_name}
                    onChange={(e) => setLinkForm({ ...linkForm, short_name: e.target.value })}
                  />
                </div>
              </div>
              <div className="form-check mb-3">
                <input
                  className="form-check-input"
                  type="checkbox"
                  checked={linkForm.autopay_enabled}
                  onChange={(e) => setLinkForm({ ...linkForm, autopay_enabled: e.target.checked })}
                  id="autopayCheck"
                />
                <label className="form-check-label small" htmlFor="autopayCheck">
                  Enable Auto-Pay (Zero convenience fee)
                </label>
              </div>
              <button type="submit" className="btn btn-outline-primary w-100 fw-semibold">
                Save Biller
              </button>
            </form>
          </div>
        </div>
      </div>

      <div className="col-12">
        <div className="card border-0 shadow-sm rounded-4">
          <div className="card-body p-4">
            <h5 className="fw-bold mb-3">Bill Payment History</h5>
            <div className="table-responsive">
              <table className="table table-sm table-hover small">
                <thead className="table-light">
                  <tr>
                    <th>BBPS Ref</th>
                    <th>Biller</th>
                    <th>Consumer No</th>
                    <th>Period</th>
                    <th>Total Paid</th>
                    <th>Mode</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {history.length === 0 ? (
                    <tr>
                      <td colSpan={7} className="text-center text-muted py-3">
                        No bill payments recorded yet.
                      </td>
                    </tr>
                  ) : (
                    history.map((bp) => (
                      <tr key={bp.bill_payment_id}>
                        <td className="font-monospace">{bp.bbps_ref_no}</td>
                        <td>{bp.biller_name}</td>
                        <td>{bp.consumer_number}</td>
                        <td>{bp.bill_period}</td>
                        <td className="fw-semibold">₹{Number(bp.total_paid).toLocaleString('en-IN')}</td>
                        <td>{bp.payment_mode}</td>
                        <td>
                          <span className="badge bg-success">{bp.payment_status}</span>
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
