import React, { useState } from 'react'
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import LoginPage from './pages/LoginPage'
import DashboardShell from './pages/DashboardShell'

export default function App() {
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem('bankease_user')
    return saved ? JSON.parse(saved) : null
  })

  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/login"
          element={
            user ? (
              <Navigate to="/" replace />
            ) : (
              <LoginPage onLoginSuccess={(u) => setUser(u)} />
            )
          }
        />
        <Route
          path="/"
          element={
            user ? (
              <DashboardShell user={user} onLogout={() => setUser(null)} />
            ) : (
              <Navigate to="/login" replace />
            )
          }
        />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}
