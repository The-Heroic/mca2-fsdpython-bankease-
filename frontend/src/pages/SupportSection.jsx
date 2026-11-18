import React, { useEffect, useState } from 'react'
import apiClient from '../api/client'

export default function SupportSection({ user }) {
  const [tickets, setTickets] = useState([])
  const [selectedTicket, setSelectedTicket] = useState(null)
  const [messages, setMessages] = useState([])
  const [replyBody, setReplyBody] = useState('')
  const [form, setForm] = useState({
    category: 'ACCOUNT_ISSUE',
    priority: 'MEDIUM',
    subject: '',
    description: '',
  })
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  const isOfficer = ['ADMIN', 'BANK_OFFICER'].includes(user.role_code)

  const loadTickets = async () => {
    try {
      const res = await apiClient.get('/support/tickets/')
      setTickets(res.data)
    } catch {
      setError('Failed to load support tickets.')
    }
  }

  useEffect(() => {
    loadTickets()
  }, [])

  const handleCreateTicket = async (e) => {
    e.preventDefault()
    setError('')
    setMessage('')
    try {
      const res = await apiClient.post('/support/tickets/', form)
      setMessage(`Ticket ${res.data.ticket_number} raised successfully.`)
      setForm({ category: 'ACCOUNT_ISSUE', priority: 'MEDIUM', subject: '', description: '' })
      loadTickets()
    } catch {
      setError('Failed to submit support ticket.')
    }
  }

  const openThread = async (ticket) => {
    try {
      const res = await apiClient.get(`/support/tickets/${ticket.ticket_id}/messages/`)
      setSelectedTicket(ticket)
      setMessages(res.data)
    } catch {
      setError('Failed to load ticket messages.')
    }
  }

  const handleReply = async (e) => {
    e.preventDefault()
    if (!replyBody.trim() || !selectedTicket) return
    try {
      await apiClient.post(`/support/tickets/${selectedTicket.ticket_id}/messages/`, {
        message_body: replyBody,
      })
      setReplyBody('')
      openThread(selectedTicket)
      loadTickets()
    } catch {
      setError('Failed to post reply.')
    }
  }

  const updateStatus = async (ticketId, ticket_status) => {
    try {
      await apiClient.patch(`/support/tickets/${ticketId}/status/`, { ticket_status })
      setMessage(`Ticket updated to ${ticket_status}.`)
      loadTickets()
      if (selectedTicket?.ticket_id === ticketId) {
        setSelectedTicket({ ...selectedTicket, ticket_status })
      }
    } catch {
      setError('Failed to update ticket status.')
    }
  }

  return (
    <div className="row g-4">
      {error && <div className="col-12"><div className="alert alert-danger py-2 small mb-0">{error}</div></div>}
      {message && <div className="col-12"><div className="alert alert-success py-2 small mb-0">{message}</div></div>}

      <div className="col-lg-5">
        <div className="card border-0 shadow-sm rounded-4">
          <div className="card-body p-4">
            <h5 className="fw-bold mb-3">Raise Support Ticket</h5>
            <form onSubmit={handleCreateTicket}>
              <div className="row g-2 mb-2">
                <div className="col-7">
                  <label className="form-label small fw-semibold">Category</label>
                  <select
                    className="form-select"
                    value={form.category}
                    onChange={(e) => setForm({ ...form, category: e.target.value })}
                  >
                    <option value="ACCOUNT_ISSUE">Account Issue</option>
                    <option value="FUNDS_TRANSFER">Funds Transfer</option>
                    <option value="BILL_PAYMENT">Bill Payment</option>
                    <option value="LOAN_QUERY">Loan Query</option>
                    <option value="KYC_UPDATE">KYC Update</option>
                    <option value="DISPUTED_TRANSACTION">Disputed Transaction</option>
                    <option value="TECHNICAL_ISSUE">Technical Issue</option>
                  </select>
                </div>
                <div className="col-5">
                  <label className="form-label small fw-semibold">Priority</label>
                  <select
                    className="form-select"
                    value={form.priority}
                    onChange={(e) => setForm({ ...form, priority: e.target.value })}
                  >
                    <option value="LOW">LOW</option>
                    <option value="MEDIUM">MEDIUM</option>
                    <option value="HIGH">HIGH</option>
                    <option value="CRITICAL">CRITICAL</option>
                  </select>
                </div>
              </div>
              <div className="mb-2">
                <label className="form-label small fw-semibold">Subject</label>
                <input
                  type="text"
                  className="form-control"
                  value={form.subject}
                  onChange={(e) => setForm({ ...form, subject: e.target.value })}
                  required
                />
              </div>
              <div className="mb-3">
                <label className="form-label small fw-semibold">Description</label>
                <textarea
                  className="form-control"
                  rows={3}
                  value={form.description}
                  onChange={(e) => setForm({ ...form, description: e.target.value })}
                  required
                />
              </div>
              <button type="submit" className="btn btn-primary w-100 fw-semibold">
                Submit Ticket
              </button>
            </form>
          </div>
        </div>
      </div>

      <div className="col-lg-7">
        <div className="card border-0 shadow-sm rounded-4">
          <div className="card-body p-4">
            <h5 className="fw-bold mb-3">Support Tickets</h5>
            <div className="table-responsive">
              <table className="table table-sm table-hover small align-middle">
                <thead className="table-light">
                  <tr>
                    <th>Ticket</th>
                    <th>Subject</th>
                    <th>Priority</th>
                    <th>Status</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  {tickets.length === 0 ? (
                    <tr>
                      <td colSpan={5} className="text-center text-muted py-3">
                        No support tickets found.
                      </td>
                    </tr>
                  ) : (
                    tickets.map((t) => (
                      <tr key={t.ticket_id}>
                        <td className="font-monospace">{t.ticket_number}</td>
                        <td>{t.subject}</td>
                        <td>{t.priority}</td>
                        <td>
                          <span className="badge bg-secondary">{t.ticket_status}</span>
                        </td>
                        <td className="d-flex gap-1">
                          <button
                            className="btn btn-outline-primary btn-sm"
                            onClick={() => openThread(t)}
                          >
                            View
                          </button>
                          {isOfficer && t.ticket_status !== 'RESOLVED' && t.ticket_status !== 'CLOSED' && (
                            <button
                              className="btn btn-success btn-sm"
                              onClick={() => updateStatus(t.ticket_id, 'RESOLVED')}
                            >
                              Resolve
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

        {selectedTicket && (
          <div className="card border-0 shadow-sm rounded-4 mt-4">
            <div className="card-body p-4">
              <h6 className="fw-bold mb-3">
                Thread: {selectedTicket.ticket_number} — {selectedTicket.subject}
              </h6>
              <div className="mb-3" style={{ maxHeight: 220, overflowY: 'auto' }}>
                {messages.map((m) => (
                  <div key={m.message_id} className="border rounded-3 p-2 mb-2 bg-light small">
                    <div className="fw-bold">
                      {m.sender_name} <span className="badge bg-secondary">{m.sender_role}</span>
                    </div>
                    <div>{m.message_body}</div>
                  </div>
                ))}
              </div>
              <form onSubmit={handleReply} className="d-flex gap-2">
                <input
                  type="text"
                  className="form-control form-control-sm"
                  placeholder="Write a reply..."
                  value={replyBody}
                  onChange={(e) => setReplyBody(e.target.value)}
                />
                <button type="submit" className="btn btn-primary btn-sm">
                  Send
                </button>
              </form>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
