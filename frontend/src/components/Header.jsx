import { Link, useLocation } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext.jsx'
import { Building2 } from 'lucide-react'

export default function Header() {
  const loc = useLocation()
  const { user, logout } = useAuth()

  const isActive = (path) => loc.pathname === path

  return (
    <header className="app-header">
      <Link to="/" className="app-header-title-link">
        <h1 className="app-header-title">
          <Building2 size={20} className="app-header-icon" />
          Shelter Capacity
        </h1> 
      </Link>

      <nav className="app-nav">
        <Link
          to="/"
          className={`app-nav-link ${isActive('/') ? 'app-nav-active' : ''}`}
        >
          Map
        </Link>

        <Link
          to="/admin"
          className={`app-nav-link ${isActive('/admin') ? 'app-nav-active' : ''}`}
        >
          Admin
        </Link>

        {!user && (
          <Link
            to="/login"
            className={`app-nav-link ${isActive('/login') ? 'app-nav-active' : ''}`}
          >
            Sign in
          </Link>
        )}

        {user && (
          <>
            <span className="app-header-user">
              {user.email}
            </span>
            <button
              type="button"
              className="app-header-logout"
              onClick={logout}
            >
              Logout
            </button>
          </>
        )}
      </nav>
    </header>
  )
}
