import { Link, useLocation } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext.jsx'

export default function Header() {
  const loc = useLocation()
  const { user, logout } = useAuth()
  const at = (p) => ({ fontWeight: loc.pathname === p ? 700 : 400 })

  return (
    <header style={{
      display: 'flex', alignItems: 'center', justifyContent: 'space-between',
      padding: 16, borderBottom: '1px solid #eee'
    }}>
      <Link to="/" style={{ textDecoration: 'none' }}>
        <h1 style={{ margin: 0, fontSize: 18 }}>Shelter Capacity</h1>
      </Link>
      <nav style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
        <Link to="/" style={at('/')}>Map</Link>
        <Link to="/admin" style={at('/admin')}>Admin</Link>
        {!user && <Link to="/login" style={at('/login')}>Sign in</Link>}
        {user && (
          <>
            <span style={{ fontSize: 12, opacity: 0.7 }}>{user.email}</span>
            <button onClick={logout}>Logout</button>
          </>
        )}
      </nav>
    </header>
  )
}
