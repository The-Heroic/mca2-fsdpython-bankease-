import React, { useEffect, useState } from 'react'
import apiClient from '../api/client'

export default function SecurityNotificationsSection({ user, onUnreadChange }) {
  const [notifications, setNotifications] = useState([])
  const [kycDocs, setKycDocs] = useState([])
  const [auditLogs, setAuditLogs] = useState([])
  const [kycForm, setKycForm] = useState({
    document_type: 'PAN_CARD',
    document_number_masked: '',
    file_path: '/media/kyc/doc_upload.pdf',
  })
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  const isStaff = ['ADMIN', 'BANK_OFFICER', 'AUDITOR'].includes(user.role_code)

  const loadAll = async () => {
    try {
      const reqs = [
        apiClient.get('/notifications/'),
        apiClient.get('/security/kyc/'),
      ]
      if (isStaff) {
        reqs.push(apiClient.get('/security/audit-logs/'))
      }
      const results = await Promise.all(reqs)
      setNotifications(results[0].data.notifications)
      onUnreadChange?.(results[0].data.unread_count)
      setKycDocs(results[1].data)
      if (isStaff && results[2]) {
        setAuditLogs(results[2].data)
      }
    } catch {
      setError('Failed to load security & notification data.')
    }
  }

  useEffect(() => {
    loadAll()
  }, [])

  const handleMarkAllRead = async () => {
    await apiClient.post('/notifications/mark-all-read/')
    loadAll()
  }

  const handleUploadKyc = async (e) => {
    e.preventDefault()
    setError('')
    setMessage('')
    try {
      await apiClient.post('/security/kyc/', kycForm)
      setMessage('KYC document submitted for officer verification.')
      setKycForm({ ...kycForm, document_number_masked: '' })
      loadAll()
    } catch {
      setError('Could not submit KYC document.')
    }
  }

  const handleVerifyKyc = async (docId, verification_status) => {
    await apiClient.patch(`/security/kyc/${docId}/verify/`, { verification_status })
    setMessage(`KYC document #${docId} marked ${verification_status}.`)
    loadAll()
  }

  return (
    <div className="row g-4">
      {error && <div className="col-12"><div className="alert alert-danger py-2 small mb-0">{error}</div></div>}
      {message && <div className="col-12"><div className="alert alert-success py-2 small mb-0">{message}</div></div>}

      <div className="col-lg-6">
        <div className="card border-0 shadow-sm rounded-4 h-100">
          <div className="card-body p-4">
            <div className="d-flex justify-content-between align-items-center mb-3">
              <h5 className="fw-bold mb-0">Notifications &amp; Alerts</h5>
              <button className="btn btn-sm btn-outline-primary" onClick={handleMarkAllRead}>
                Mark All Read
              </button>
            </div>
            {notifications.length === 0 ? (
              <p className="text-muted small mb-0">No notifications yet.</p>
            ) : (
              <ul className="list-group list-group-flush small">
                {notifications.map((n) => (
                  <li
                    key={n.notification_id}
                    className={`list-group-item px-0 ${n.is_read ? 'opacity-75' : 'fw-semibold'}`}
                  >
                    <div className="d-flex justify-content-between">
                      <span>{n.title}</span>
                      <span className="badge bg-info text-dark">{n.notification_type}</span>
                    </div>
                    <div className="text-muted fw-normal">{n.message}</div>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
      </div>

      <div className="col-lg-6">
        <div className="card border-0 shadow-sm rounded-4 h-100">
          <div className="card-body p-4">
            <h5 className="fw-bold mb-3">KYC Compliance Documents</h5>
            <form onSubmit={handleUploadKyc} className="row g-2 mb-3">
              <div className="col-5">
                <select
                  className="form-select form-select-sm"
                  value={kycForm.document_type}
                  onChange={(e) => setKycForm({ ...kycForm, document_type: e.target.value })}
                >
                  <option value="PAN_CARD">PAN Card</option>
                  <option value="AADHAAR_CARD">Aadhaar Card</option>
                  <option value="PASSPORT">Passport</option>
                </select>
              </div>
              <div className="col-4">
                <input
                  type="text"
                  className="form-control form-control-sm"
                  placeholder="Masked ID"
                  value={kycForm.document_number_masked}
                  onChange={(e) => setKycForm({ ...kycForm, document_number_masked: e.target.value })}
                  required
                />
              </div>
              <div className="col-3">
                <button type="submit" className="btn btn-primary btn-sm w-100">
                  Submit
                </button>
              </div>
            </form>

            <div className="table-responsive">
              <table className="table table-sm small">
                <thead className="table-light">
                  <tr>
                    <th>User</th>
                    <th>Type</th>
                    <th>Doc No</th>
                    <th>Status</th>
                    {isStaff && <th>Action</th>}
                  </tr>
                </thead>
                <tbody>
                  {kycDocs.map((d) => (
                    <tr key={d.kyc_doc_id}>
                      <td>{d.username}</td>
                      <td>{d.document_type}</td>
                      <td>{d.document_number_masked}</td>
                      <td>{d.verification_status}</td>
                      {isStaff && (
                        <td>
                          {d.verification_status === 'PENDING' && (
                            <button
                              className="btn btn-success btn-sm"
                              onClick={() => handleVerifyKyc(d.kyc_doc_id, 'VERIFIED')}
                            >
                              Verify
                            </button>
                          )}
                        </td>
                      )}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      {isStaff && (
        <div className="col-12">
          <div className="card border-0 shadow-sm rounded-4">
            <div className="card-body p-4">
              <h5 className="fw-bold mb-3">Security Audit Trail</h5>
              <div className="table-responsive">
                <table className="table table-sm small">
                  <thead className="table-light">
                    <tr>
                      <th>Event</th>
                      <th>Severity</th>
                      <th>User</th>
                      <th>IP</th>
                      <th>Description</th>
                    </tr>
                  </thead>
                  <tbody>
                    {auditLogs.map((log) => (
                      <tr key={log.audit_id}>
                        <td>{log.event_category}</td>
                        <td>{log.severity}</td>
                        <td>{log.username || 'System'}</td>
                        <td>{log.ip_address}</td>
                        <td>{log.event_description}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
