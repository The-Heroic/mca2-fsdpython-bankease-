import React, { useEffect, useState } from 'react'
import apiClient from '../api/client'

export default function LoansSection({ user }) {
  const [products, setProducts] = useState([])
  const [accounts, setAccounts] = useState([])
  const [applications, setApplications] = useState([])
  const [repayments, setRepayments] = useState([])
  const [selectedLoanId, setSelectedLoanId] = useState(null)
  const [emiPreview, setEmiPreview] = useState(null)
  const [appForm, setAppForm] = useState({
    disbursement_account_id: '',
    loan_product_id: '',
    requested_amount: '100000',
    tenure_months: '12',
    applicant_annual_income: '800000',
    cibil_score: '760',
    purpose_description: '',
  })
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  const isOfficer = user.role_code === 'BANK_OFFICER' || user.role_code === 'ADMIN'

  const loadAll = async () => {
    try {
      const [prodRes, accRes, appRes] = await Promise.all([
        apiClient.get('/loans/products/'),
        apiClient.get('/accounts/'),
        apiClient.get('/loans/applications/'),
      ])
      setProducts(prodRes.data)
      setAccounts(accRes.data.filter((a) => a.account_status === 'ACTIVE'))
      setApplications(appRes.data)
    } catch {
      setError('Failed to load loan data.')
    }
  }

  useEffect(() => {
    loadAll()
  }, [])

  const handleCalcEmi = async () => {
    const selectedProd = products.find((p) => p.loan_product_id === Number(appForm.loan_product_id))
    const rate = selectedProd ? selectedProd.base_interest_rate : '10.5'
    try {
      const res = await apiClient.post('/loans/calculate-emi/', {
        principal: appForm.requested_amount,
        interest_rate: rate,
        tenure_months: Number(appForm.tenure_months),
      })
      setEmiPreview(res.data)
    } catch {
      setError('Enter valid amount and tenure for EMI calculation.')
    }
  }

  const handleApplyLoan = async (e) => {
    e.preventDefault()
    setError('')
    setMessage('')
    try {
      const res = await apiClient.post('/loans/applications/', {
        ...appForm,
        disbursement_account_id: Number(appForm.disbursement_account_id),
        loan_product_id: Number(appForm.loan_product_id),
        tenure_months: Number(appForm.tenure_months),
        cibil_score: Number(appForm.cibil_score),
      })
      setMessage(`Loan application ${res.data.application_number} submitted!`)
      setAppForm({ ...appForm, purpose_description: '' })
      loadAll()
    } catch (err) {
      const data = err.response?.data
      const firstKey = data && typeof data === 'object' ? Object.keys(data)[0] : null
      setError(firstKey ? data[firstKey]?.[0] || data[firstKey] : 'Loan application failed.')
    }
  }

  const handleReview = async (loanId, decision) => {
    setError('')
    setMessage('')
    try {
      await apiClient.patch(`/loans/applications/${loanId}/review/`, { decision })
      setMessage(`Loan #${loanId} processed (${decision}).`)
      loadAll()
    } catch (err) {
      setError(err.response?.data?.detail || 'Loan review failed.')
    }
  }

  const viewRepayments = async (loanId) => {
    try {
      const res = await apiClient.get(`/loans/applications/${loanId}/repayments/`)
      setSelectedLoanId(loanId)
      setRepayments(res.data)
    } catch {
      setError('Failed to load EMI schedule.')
    }
  }

  const payEmi = async (repaymentId) => {
    setError('')
    setMessage('')
    try {
      await apiClient.post(`/loans/repayments/${repaymentId}/pay/`)
      setMessage('EMI paid successfully!')
      viewRepayments(selectedLoanId)
      loadAll()
    } catch (err) {
      setError(err.response?.data?.detail || 'EMI payment failed.')
    }
  }

  return (
    <div className="row g-4">
      {error && <div className="col-12"><div className="alert alert-danger py-2 small mb-0">{error}</div></div>}
      {message && <div className="col-12"><div className="alert alert-success py-2 small mb-0">{message}</div></div>}

      <div className="col-lg-5">
        <div className="card border-0 shadow-sm rounded-4">
          <div className="card-body p-4">
            <h5 className="fw-bold mb-3">Apply for a Loan &amp; EMI Calculator</h5>
            <form onSubmit={handleApplyLoan}>
              <div className="mb-2">
                <label className="form-label small fw-semibold">Loan Product</label>
                <select
                  className="form-select"
                  value={appForm.loan_product_id}
                  onChange={(e) => setAppForm({ ...appForm, loan_product_id: e.target.value })}
                  required
                >
                  <option value="">Select loan product...</option>
                  {products.map((p) => (
                    <option key={p.loan_product_id} value={p.loan_product_id}>
                      {p.product_name} ({p.base_interest_rate}% p.a.)
                    </option>
                  ))}
                </select>
              </div>
              <div className="mb-2">
                <label className="form-label small fw-semibold">Disbursement Account</label>
                <select
                  className="form-select"
                  value={appForm.disbursement_account_id}
                  onChange={(e) => setAppForm({ ...appForm, disbursement_account_id: e.target.value })}
                  required
                >
                  <option value="">Select active account...</option>
                  {accounts.map((a) => (
                    <option key={a.account_id} value={a.account_id}>
                      {a.account_number} ({a.account_type})
                    </option>
                  ))}
                </select>
              </div>
              <div className="row g-2 mb-2">
                <div className="col-6">
                  <label className="form-label small fw-semibold">Amount (INR)</label>
                  <input
                    type="number"
                    className="form-control"
                    value={appForm.requested_amount}
                    onChange={(e) => setAppForm({ ...appForm, requested_amount: e.target.value })}
                    required
                  />
                </div>
                <div className="col-6">
                  <label className="form-label small fw-semibold">Tenure (Months)</label>
                  <input
                    type="number"
                    className="form-control"
                    value={appForm.tenure_months}
                    onChange={(e) => setAppForm({ ...appForm, tenure_months: e.target.value })}
                    required
                  />
                </div>
              </div>
              <div className="row g-2 mb-2">
                <div className="col-6">
                  <label className="form-label small fw-semibold">Annual Income (INR)</label>
                  <input
                    type="number"
                    className="form-control"
                    value={appForm.applicant_annual_income}
                    onChange={(e) => setAppForm({ ...appForm, applicant_annual_income: e.target.value })}
                    required
                  />
                </div>
                <div className="col-6">
                  <label className="form-label small fw-semibold">CIBIL Score</label>
                  <input
                    type="number"
                    min="300"
                    max="900"
                    className="form-control"
                    value={appForm.cibil_score}
                    onChange={(e) => setAppForm({ ...appForm, cibil_score: e.target.value })}
                    required
                  />
                </div>
              </div>
              <div className="mb-3">
                <label className="form-label small fw-semibold">Purpose</label>
                <input
                  type="text"
                  className="form-control"
                  value={appForm.purpose_description}
                  onChange={(e) => setAppForm({ ...appForm, purpose_description: e.target.value })}
                  required
                />
              </div>

              <div className="d-flex gap-2">
                <button type="button" onClick={handleCalcEmi} className="btn btn-outline-secondary w-50">
                  Calculate EMI
                </button>
                <button type="submit" className="btn btn-primary w-50 fw-semibold">
                  Submit Loan
                </button>
              </div>
            </form>

            {emiPreview && (
              <div className="alert alert-info mt-3 small mb-0">
                <strong>Monthly EMI:</strong> ₹{Number(emiPreview.emi_amount).toLocaleString('en-IN')}
                <br />
                Total Interest: ₹{Number(emiPreview.total_interest).toLocaleString('en-IN')}
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="col-lg-7">
        <div className="card border-0 shadow-sm rounded-4">
          <div className="card-body p-4">
            <h5 className="fw-bold mb-3">Loan Applications</h5>
            <div className="table-responsive">
              <table className="table table-sm table-hover small align-middle">
                <thead className="table-light">
                  <tr>
                    <th>App No</th>
                    <th>Product</th>
                    <th>Amount</th>
                    <th>EMI</th>
                    <th>Status</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {applications.length === 0 ? (
                    <tr>
                      <td colSpan={6} className="text-center text-muted py-3">
                        No loan applications found.
                      </td>
                    </tr>
                  ) : (
                    applications.map((loan) => (
                      <tr key={loan.loan_id}>
                        <td className="font-monospace">{loan.application_number}</td>
                        <td>{loan.product_name}</td>
                        <td>₹{Number(loan.requested_amount).toLocaleString('en-IN')}</td>
                        <td>₹{Number(loan.emi_amount).toLocaleString('en-IN')}</td>
                        <td>
                          <span className="badge bg-secondary">{loan.loan_status}</span>
                        </td>
                        <td className="d-flex gap-1 flex-wrap">
                          {loan.loan_status === 'DISBURSED' && (
                            <button
                              className="btn btn-outline-primary btn-sm"
                              onClick={() => viewRepayments(loan.loan_id)}
                            >
                              Schedule
                            </button>
                          )}
                          {isOfficer && loan.loan_status === 'APPLIED' && (
                            <>
                              <button
                                className="btn btn-success btn-sm"
                                onClick={() => handleReview(loan.loan_id, 'APPROVE_AND_DISBURSE')}
                              >
                                Disburse
                              </button>
                              <button
                                className="btn btn-danger btn-sm"
                                onClick={() => handleReview(loan.loan_id, 'REJECT')}
                              >
                                Reject
                              </button>
                            </>
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

        {selectedLoanId && (
          <div className="card border-0 shadow-sm rounded-4 mt-4">
            <div className="card-body p-4">
              <h6 className="fw-bold mb-3">EMI Repayment Schedule (Loan #{selectedLoanId})</h6>
              <div className="table-responsive">
                <table className="table table-sm small">
                  <thead className="table-light">
                    <tr>
                      <th>#</th>
                      <th>Due Date</th>
                      <th>EMI</th>
                      <th>Status</th>
                      <th>Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    {repayments.map((rep) => (
                      <tr key={rep.repayment_id}>
                        <td>{rep.installment_number}</td>
                        <td>{rep.due_date}</td>
                        <td>₹{Number(rep.emi_amount).toLocaleString('en-IN')}</td>
                        <td>{rep.repayment_status}</td>
                        <td>
                          {rep.repayment_status === 'PENDING' && (
                            <button
                              className="btn btn-sm btn-primary"
                              onClick={() => payEmi(rep.repayment_id)}
                            >
                              Pay EMI
                            </button>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
