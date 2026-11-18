import React, { useState } from 'react'
import apiClient from '../api/client'

export default function ProfileSecuritySection({ user }) {
  const [form, setForm] = useState({
    current_password: '',
    new_password: '',
    confirm_new_password: '',
  })
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  const handlePasswordChange = async (e) => {
    e.preventDefault()
    setError('')
    setMessage('')
    try {
      const res = await apiClient.post('/auth/change-password/', form)
      setMessage(res.data.message)
      setForm({ current_password: '', new_password: '', confirm_new_password: '' })
    } catch (err) {
      const data = err.response?.data
      const firstKey = data && typeof data === 'object' ? Object.keys(data)[0] : null
      setError(
        firstKey
          ? Array.isArray(data[firstKey])
            ? data[firstKey][0]
            : data[firstKey]
          : 'Failed to update password.'
      )
    }
  }

  return (
    <div className="row g-4">
      <div className="col-md-6">
        <div className="card border-0 shadow-sm rounded-4 h-100">
          <div className="card-body p-4">
            <h5 className="fw-bold mb-3">Profile Details</h5>
            <dl className="row small mb-0">
              <dt className="col-sm-4 text-muted">Full Name</dt>
              <dd className="col-sm-8 fw-semibold">{user.full_name}</dd>
              <dt className="col-sm-4 text-muted">Username</dt>
              <dd className="col-sm-8">{user.username}</dd>
              <dt className="col-sm-4 text-muted">Email</dt>
              <dd className="col-sm-8">{user.email}</dd>
              <dt className="col-sm-4 text-muted">Phone</dt>
              <dd className="col-sm-8">{user.phone_number}</dd>
              <dt className="col-sm-4 text-muted">Role</dt>
              <dd className="col-sm-8">{user.role_name}</dd>
              <dt className="col-sm-4 text-muted">KYC Status</dt>
              <dd className="col-sm-8">
                <span className="badge bg-info text-dark">{user.kyc_status}</span>
              </dd>
            </dl>
          </div>
        </div>
      </div>

      <div className="col-md-6">
        <div className="card border-0 shadow-sm rounded-4 h-100">
          <div className="card-body p-4">
            <h5 className="fw-bold mb-3">Change Password</h5>
            {error && <div className="alert alert-danger py-2 small">{error}</div>}
            {message && <div className="alert alert-success py-2 small">{message}</div>}
            <form onSubmit={handlePasswordChange}>
              <div className="mb-3">
                <label className="form-label small fw-semibold">Current Password</label>
                <input
                  type="password"
                  className="form-control"
                  value={form.current_password}
                  onChange={(e) => setForm({ ...form, current_password: e.target.value })}
                  required
                />
              </div>
              <div className="mb-3">
                <label className="form-label small fw-semibold">New Password</label>
                <input
                  type="password"
                  className="form-control"
                  value={form.new_password}
                  onChange={(e) => setForm({ ...form, new_password: e.target.value })}
                  required
                />
              </div>
              <div className="mb-3">
                <label className="form-label small fw-semibold">Confirm New Password</label>
                <input
                  type="password"
                  className="form-control"
                  value={form.confirm_new_password}
                  onChange={(e) => setForm({ ...form, confirm_new_password: e.target.value })}
                  required
                />
              </div>
              <button type="submit" className="btn btn-primary w-100 fw-semibold">
                Update Password
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  )
}
