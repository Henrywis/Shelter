import { Link, useLocation } from 'react-router-dom'

export default function Header() {
  const loc = useLocation()
  return (
    <header style={{
      display: 'flex', alignItems: 'center', justifyContent: 'space-between',
      padding: 16, borderBottom: '1px solid #eee'
    }}>
      <Link to="/" style={{ textDecoration: 'none' }}>
        <h1 style={{ margin: 0, fontSize: 18 }}>Shelter Capacity</h1>
      </Link>
      <nav style={{ display: 'flex', gap: 12 }}>
        <Link to="/" style={{ fontWeight: loc.pathname === '/' ? 700 : 400 }}>Map</Link>
        <Link to="/admin" style={{ fontWeight: loc.pathname === '/admin' ? 700 : 400 }}>Admin</Link>
      </nav>
    </header>
  )
}
