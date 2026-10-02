import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './contexts/AuthContext'
import LoginPage from './pages/LoginPage'
import PendingPage from './pages/PendingPage'
import DashboardPage from './pages/DashboardPage'
import SearchPage from './pages/SearchPage'
import AdminPage from './pages/AdminPage'

function ProtectedRoute({ children, requireAdmin = false }) {
  const { user } = useAuth()
  if (user === undefined) return <div>로딩 중...</div>
  if (!user) return <Navigate to="/login" replace />
  if (!user.is_approved) return <Navigate to="/pending" replace />
  if (requireAdmin && !user.is_admin) return <Navigate to="/" replace />
  return children
}

function AuthRoute({ children }) {
  const { user } = useAuth()
  if (user === undefined) return <div>로딩 중...</div>
  if (user) return <Navigate to="/" replace />
  return children
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<AuthRoute><LoginPage /></AuthRoute>} />
          <Route path="/pending" element={<PendingPage />} />
          <Route path="/" element={<ProtectedRoute><DashboardPage /></ProtectedRoute>} />
          <Route path="/search" element={<ProtectedRoute><SearchPage /></ProtectedRoute>} />
          <Route path="/admin" element={<ProtectedRoute requireAdmin><AdminPage /></ProtectedRoute>} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  )
}
