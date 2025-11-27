import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext.jsx'

export default function Login() {
  const nav = useNavigate()
  const { user, login } = useAuth()
  const [email, setEmail] = useState('admin@example.com')
  const [password, setPassword] = useState('SuperStrong1!')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  // If already logged in, bounce to /admin
  useEffect(() => {
    if (user) {
      nav('/admin')
    }
  }, [user, nav])

  const onSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      await login(email, password)
      nav('/admin')
    } catch (err) {
      console.error('Login error:', err)
      setError('Invalid credentials. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-page">
      <div className="card login-card">
        <h1 className="login-title">Admin Sign In</h1>
        <p className="login-subtitle">
          Sign in to manage shelter intake requests and capacity updates.
        </p>

        <form onSubmit={onSubmit} className="form-grid">
          <div className="form-field">
            <label htmlFor="email" className="form-label">Email</label>
            <input
              id="email"
              className="input"
              type="email"
              placeholder="admin@example.com"
              value={email}
              onChange={e => setEmail(e.target.value)}
              required
              disabled={loading}
            />
          </div>

          <div className="form-field">
            <label htmlFor="password" className="form-label">Password</label>
            <input
              id="password"
              className="input"
              type="password"
              placeholder="Enter your password"
              value={password}
              onChange={e => setPassword(e.target.value)}
              required
              disabled={loading}
            />
          </div>

          {error && (
            <div className="alert-error">
              {error}
            </div>
          )}

          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? 'Signing in…' : 'Sign in'}
          </button>
        </form>

        <div className="login-creds">
          <p>Test credentials (local dev):</p>
          <p>
            <code>admin@example.com</code><br />
            <code>SuperStrong1!</code>
          </p>
        </div>
      </div>
    </div>
  )
}
