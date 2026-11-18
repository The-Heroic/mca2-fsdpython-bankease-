import React, { useState } from 'react'
import apiClient from '../api/client'
import DashboardOverviewSection from './DashboardOverviewSection'
import AccountsSection from './AccountsSection'
import TransfersSection from './TransfersSection'
import BillsSection from './BillsSection'
import LoansSection from './LoansSection'
import InvestmentsSection from './InvestmentsSection'
import SupportSection from './SupportSection'
import SecurityNotificationsSection from './SecurityNotificationsSection'
import ProfileSecuritySection from './ProfileSecuritySection'

const MODULES = [
  { id: 1, name: 'User Authentication', sprint: 'Sprint 0 / 1', status: 'Active' },
  { id: 2, name: 'Account Management', sprint: 'Sprint 1', status: 'Active' },
  { id: 3, name: 'Funds Transfer', sprint: 'Sprint 1', status: 'Active' },
  { id: 4, name: 'Bill Payment', sprint: 'Sprint 2', status: 'Active' },
  { id: 5, name: 'Loan Management', sprint: 'Sprint 2', status: 'Active' },
  { id: 6, name: 'Investment Services', sprint: 'Sprint 2', status: 'Active' },
  { id: 7, name: 'Customer Support', sprint: 'Sprint 3', status: 'Active' },
  { id: 8, name: 'Security & Compliance', sprint: 'Sprint 3', status: 'Active' },
  { id: 9, name: 'Notification & Alerts', sprint: 'Sprint 3', status: 'Active' },
  { id: 10, name: 'Dashboard & Reporting', sprint: 'Sprint 3', status: 'Active' },
]

export default function DashboardShell({ user, onLogout }) {
  const [activeTab, setActiveTab] = useState('dashboard')
  const [unreadCount, setUnreadCount] = useState(0)

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
          <ul className="nav nav-pills py-2 gap-2 flex-wrap">
            <li className="nav-item">
              <button
                className={`nav-link btn-sm ${activeTab === 'dashboard' ? 'active' : ''}`}
                onClick={() => setActiveTab('dashboard')}
              >
                Dashboard
              </button>
            </li>
            <li className="nav-item">
              <button
                className={`nav-link btn-sm ${activeTab === 'accounts' ? 'active' : ''}`}
                onClick={() => setActiveTab('accounts')}
              >
                Accounts
              </button>
            </li>
            <li className="nav-item">
              <button
                className={`nav-link btn-sm ${activeTab === 'transfers' ? 'active' : ''}`}
                onClick={() => setActiveTab('transfers')}
              >
                Transfers
              </button>
            </li>
            <li className="nav-item">
              <button
                className={`nav-link btn-sm ${activeTab === 'bills' ? 'active' : ''}`}
                onClick={() => setActiveTab('bills')}
              >
                Bill Pay
              </button>
            </li>
            <li className="nav-item">
              <button
                className={`nav-link btn-sm ${activeTab === 'loans' ? 'active' : ''}`}
                onClick={() => setActiveTab('loans')}
              >
                Loans
              </button>
            </li>
            <li className="nav-item">
              <button
                className={`nav-link btn-sm ${activeTab === 'investments' ? 'active' : ''}`}
                onClick={() => setActiveTab('investments')}
              >
                Investments
              </button>
            </li>
            <li className="nav-item">
              <button
                className={`nav-link btn-sm ${activeTab === 'support' ? 'active' : ''}`}
                onClick={() => setActiveTab('support')}
              >
                Support
              </button>
            </li>
            <li className="nav-item">
              <button
                className={`nav-link btn-sm ${activeTab === 'security' ? 'active' : ''}`}
                onClick={() => setActiveTab('security')}
              >
                Alerts &amp; KYC {unreadCount > 0 && <span className="badge bg-danger ms-1">{unreadCount}</span>}
              </button>
            </li>
            <li className="nav-item">
              <button
                className={`nav-link btn-sm ${activeTab === 'profile' ? 'active' : ''}`}
                onClick={() => setActiveTab('profile')}
              >
                Profile
              </button>
            </li>
            <li className="nav-item">
              <button
                className={`nav-link btn-sm ${activeTab === 'roadmap' ? 'active' : ''}`}
                onClick={() => setActiveTab('roadmap')}
              >
                Modules
              </button>
            </li>
          </ul>
        </div>
      </div>

      <main className="container py-4 flex-grow-1">
        {activeTab === 'dashboard' && <DashboardOverviewSection user={user} />}
        {activeTab === 'accounts' && <AccountsSection user={user} />}
        {activeTab === 'transfers' && <TransfersSection />}
        {activeTab === 'bills' && <BillsSection />}
        {activeTab === 'loans' && <LoansSection user={user} />}
        {activeTab === 'investments' && <InvestmentsSection />}
        {activeTab === 'support' && <SupportSection user={user} />}
        {activeTab === 'security' && (
          <SecurityNotificationsSection user={user} onUnreadChange={setUnreadCount} />
        )}
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
                      <span className="badge bg-success">{mod.status}</span>
                    </div>
                    <h6 className="fw-bold mb-1">{mod.name}</h6>
                    <div className="text-muted small">Delivered: {mod.sprint}</div>
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
