import { Routes, Route } from 'react-router-dom'
import MapView from './pages/MapView.jsx'
import AdminPortal from './pages/AdminPortal.jsx'
import Login from './pages/Login.jsx'
import Header from './components/Header.jsx'
import { useAuth } from './auth/AuthContext.jsx'

export default function App() {
  const { loading } = useAuth()
  if (loading) return <div style={{ padding: 16 }}>Loading…</div>

  return (
    <div className="app-shell">
      <Header />
      <main className="app-main">
        <Routes>
          <Route path="/" element={<MapView />} />
          <Route path="/login" element={<Login />} />
          <Route path="/admin" element={<AdminPortal />} />
        </Routes>
      </main>
      <footer className="app-footer">
        Shelter Capacity &bull; v0.1.0
      </footer>
    </div>
  )
}
