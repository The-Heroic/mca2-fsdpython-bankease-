import React, { useState } from 'react'
import apiClient from '../api/client'
import AccountsSection from './AccountsSection'
import TransfersSection from './TransfersSection'
import ProfileSecuritySection from './ProfileSecuritySection'

const MODULES = [
  { id: 1, name: 'User Authentication', sprint: 'Sprint 0 / 1', status: 'Active' },
  { id: 2, name: 'Account Management', sprint: 'Sprint 1', status: 'Active' },
  { id: 3, name: 'Funds Transfer', sprint: 'Sprint 1', status: 'Active' },
  { id: 4, name: 'Bill Payment', sprint: 'Sprint 2', status: 'Planned' },
  { id: 5, name: 'Loan Management', sprint: 'Sprint 2', status: 'Planned' },
  { id: 6, name: 'Investment Services', sprint: 'Sprint 2', status: 'Planned' },
  { id: 7, name: 'Customer Support', sprint: 'Sprint 3', status: 'Planned' },
  { id: 8, name: 'Security & Compliance', sprint: 'Sprint 3', status: 'Planned' },
  { id: 9, name: 'Notification & Alerts', sprint: 'Sprint 3', status: 'Planned' },
  { id: 10, name: 'Dashboard & Reporting', sprint: 'Sprint 3', status: 'Planned' },
]

export default function DashboardShell({ user, onLogout }) {
  const [activeTab, setActiveTab] = useState('accounts')

  const handleLogout = async () => {
    const refresh = localStorage.getItem('bankease_refresh_token')
    try {
      if (refresh) {
        await apiClient.post('/auth/logout/', { refresh })
      }
    } catch {
      // Clear local session regardless of network error
    } finally {
      localStorage.removeItem('bankease_access_token')
      localStorage.removeItem('bankease_refresh_token')
      localStorage.removeItem('bankease_user')
      onLogout()
    }
  }

  return (
    <div className="min-vh-100 d-flex flex-column">
      <nav className="navbar navbar-expand-lg navbar-dark bankease-hero shadow-sm">
        <div className="container">
          <span className="navbar-brand fw-bold">BankEase</span>
          <div className="d-flex align-items-center gap-3">
            <span className="badge bg-light text-primary">{user.role_code}</span>
            <span className="text-white small d-none d-sm-inline">
              {user.full_name} ({user.username})
            </span>
            <button onClick={handleLogout} className="btn btn-outline-light btn-sm">
              Logout
            </button>
          </div>
        </div>
      </nav>

      <div className="bg-white border-bottom">
        <div className="container">
          <ul className="nav nav-pills py-2 gap-2">
            <li className="nav-item">
              <button
                className={`nav-link btn-sm ${activeTab === 'accounts' ? 'active' : ''}`}
                onClick={() => setActiveTab('accounts')}
              >
                Accounts &amp; Statements
              </button>
            </li>
            <li className="nav-item">
              <button
                className={`nav-link btn-sm ${activeTab === 'transfers' ? 'active' : ''}`}
                onClick={() => setActiveTab('transfers')}
              >
                Funds Transfer
              </button>
            </li>
            <li className="nav-item">
              <button
                className={`nav-link btn-sm ${activeTab === 'profile' ? 'active' : ''}`}
                onClick={() => setActiveTab('profile')}
              >
                Profile &amp; Security
              </button>
            </li>
            <li className="nav-item">
              <button
                className={`nav-link btn-sm ${activeTab === 'roadmap' ? 'active' : ''}`}
                onClick={() => setActiveTab('roadmap')}
              >
                Module Roadmap
              </button>
            </li>
          </ul>
        </div>
      </div>

      <main className="container py-4 flex-grow-1">
        {activeTab === 'accounts' && <AccountsSection user={user} />}
        {activeTab === 'transfers' && <TransfersSection />}
        {activeTab === 'profile' && <ProfileSecuritySection user={user} />}
        {activeTab === 'roadmap' && (
          <div className="row g-3">
            {MODULES.map((mod) => (
              <div className="col-md-6 col-lg-4" key={mod.id}>
                <div className="card h-100 border-0 shadow-sm rounded-3 module-card">
                  <div className="card-body">
                    <div className="d-flex justify-content-between align-items-start mb-2">
                      <span className="badge bg-primary-subtle text-primary">
                        Module {mod.id}
                      </span>
                      <span
                        className={`badge ${
                          mod.status === 'Active'
                            ? 'bg-success'
                            : 'bg-secondary-subtle text-secondary'
                        }`}
                      >
                        {mod.status}
                      </span>
                    </div>
                    <h6 className="fw-bold mb-1">{mod.name}</h6>
                    <div className="text-muted small">Scheduled: {mod.sprint}</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  )
}
