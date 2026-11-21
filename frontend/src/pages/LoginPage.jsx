import React, { useState } from 'react'
import apiClient from '../api/client'

export default function LoginPage({ onLoginSuccess }) {
  const [isRegister, setIsRegister] = useState(false)
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    confirm_password: '',
    email: '',
    phone_number: '',
    full_name: '',
    city: '',
    state: '',
  })
  const [error, setError] = useState('')
  const [info, setInfo] = useState('')
  const [loading, setLoading] = useState(false)

  const handleChange = (e) => {
    setFormData((prev) => ({ ...prev, [e.target.name]: e.target.value }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setInfo('')
    setLoading(true)

    try {
      if (isRegister) {
        await apiClient.post('/auth/register/', formData)
        setInfo('Registration successful! You can now sign in with your credentials.')
        setIsRegister(false)
      } else {
        const res = await apiClient.post('/auth/login/', {
          username: formData.username,
          password: formData.password,
        })
        localStorage.setItem('bankease_access_token', res.data.access)
        localStorage.setItem('bankease_refresh_token', res.data.refresh)
        localStorage.setItem('bankease_user', JSON.stringify(res.data.user))
        onLoginSuccess(res.data.user)
      }
    } catch (err) {
      const data = err.response?.data
      if (data?.detail) {
        setError(data.detail)
      } else if (data && typeof data === 'object') {
        const firstKey = Object.keys(data)[0]
        const firstVal = Array.isArray(data[firstKey]) ? data[firstKey][0] : data[firstKey]
        setError(`${firstKey}: ${firstVal}`)
      } else if (err.message) {
        setError(`Unable to connect to backend (${apiClient.defaults.baseURL}): ${err.message}`)
      } else {
        setError('Unable to reach BankEase API server. Ensure backend is running.')
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-vh-100 d-flex align-items-center py-5">
      <div className="container">
        <div className="row justify-content-center shadow-lg rounded-4 overflow-hidden bg-white">
          <div className="col-lg-5 bankease-hero p-5 d-flex flex-column justify-content-between">
            <div>
              <span className="badge bg-light text-primary fw-semibold mb-3">
                P18 • Sprint 0 (v0.1.0)
              </span>
              <h1 className="fw-bold display-6 mb-3">BankEase</h1>
              <p className="opacity-75 mb-4">
                NextGen Net Banking Application for secure account management, instant
                IMPS/NEFT/RTGS transfers, utility bill payments, loans, and investments.
              </p>
            </div>
            <div className="small opacity-75">
              <div>• 256-bit JWT Session Security</div>
              <div>• Role-Based Portals: Customer, Bank Officer &amp; Admin</div>
              <div>• MySQL 8.0 3NF Ledger &amp; Audit Trail</div>
            </div>
          </div>

          <div className="col-lg-7 p-4 p-md-5">
            <h3 className="fw-bold mb-1">
              {isRegister ? 'Open Your BankEase Profile' : 'Sign In to Net Banking'}
            </h3>
            <p className="text-muted small mb-4">
              {isRegister
                ? 'Register as a new Customer to get started.'
                : 'Enter your BankEase username and password.'}
            </p>

            {error && <div className="alert alert-danger py-2 small">{error}</div>}
            {info && <div className="alert alert-success py-2 small">{info}</div>}

            <form onSubmit={handleSubmit}>
              <div className="row g-3">
                <div className="col-12">
                  <label className="form-label small fw-semibold">Username</label>
                  <input
                    type="text"
                    name="username"
                    className="form-control"
                    placeholder="e.g., aarav_gupta"
                    value={formData.username}
                    onChange={handleChange}
                    required
                  />
                </div>

                {isRegister && (
                  <>
                    <div className="col-md-6">
                      <label className="form-label small fw-semibold">Full Name</label>
                      <input
                        type="text"
                        name="full_name"
                        className="form-control"
                        placeholder="Aarav Siddharth Gupta"
                        value={formData.full_name}
                        onChange={handleChange}
                        required
                      />
                    </div>
                    <div className="col-md-6">
                      <label className="form-label small fw-semibold">Phone Number</label>
                      <input
                        type="text"
                        name="phone_number"
                        className="form-control"
                        placeholder="+91-9811122001"
                        value={formData.phone_number}
                        onChange={handleChange}
                        required
                      />
                    </div>
                    <div className="col-12">
                      <label className="form-label small fw-semibold">Email Address</label>
                      <input
                        type="email"
                        name="email"
                        className="form-control"
                        placeholder="name@example.com"
                        value={formData.email}
                        onChange={handleChange}
                        required
                      />
                    </div>
                    <div className="col-md-6">
                      <label className="form-label small fw-semibold">City</label>
                      <input
                        type="text"
                        name="city"
                        className="form-control"
                        placeholder="Noida"
                        value={formData.city}
                        onChange={handleChange}
                      />
                    </div>
                    <div className="col-md-6">
                      <label className="form-label small fw-semibold">State</label>
                      <input
                        type="text"
                        name="state"
                        className="form-control"
                        placeholder="Uttar Pradesh"
                        value={formData.state}
                        onChange={handleChange}
                      />
                    </div>
                  </>
                )}

                <div className={isRegister ? 'col-md-6' : 'col-12'}>
                  <label className="form-label small fw-semibold">Password</label>
                  <input
                    type="password"
                    name="password"
                    className="form-control"
                    placeholder="Minimum 8 characters"
                    value={formData.password}
                    onChange={handleChange}
                    required
                  />
                </div>

                {isRegister && (
                  <div className="col-md-6">
                    <label className="form-label small fw-semibold">Confirm Password</label>
                    <input
                      type="password"
                      name="confirm_password"
                      className="form-control"
                      placeholder="Re-enter password"
                      value={formData.confirm_password}
                      onChange={handleChange}
                      required
                    />
                  </div>
                )}
              </div>

              <button
                type="submit"
                className="btn btn-primary w-100 mt-4 py-2 fw-semibold"
                disabled={loading}
              >
                {loading
                  ? 'Please wait...'
                  : isRegister
                  ? 'Create Customer Account'
                  : 'Sign In Securely'}
              </button>
            </form>

            <div className="text-center mt-4 small">
              {isRegister ? 'Already have a BankEase account? ' : 'New to BankEase? '}
              <button
                type="button"
                className="btn btn-link btn-sm p-0 fw-semibold text-decoration-none"
                onClick={() => {
                  setIsRegister(!isRegister)
                  setError('')
                  setInfo('')
                }}
              >
                {isRegister ? 'Sign In' : 'Register Now'}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
