import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext.jsx'

export default function Login() {
  const nav = useNavigate()
  const { login } = useAuth()
  const [email, setEmail] = useState('admin@example.com')
  const [password, setPassword] = useState('SuperStrong1!')
  const [error, setError] = useState('')

  const onSubmit = async (e) => {
    e.preventDefault()
    setError('')
    try {
      await login(email, password)
      nav('/admin')
    } catch (err) {
      setError('Login failed')
      console.error(err)
    }
  }

  return (
    <section style={{ maxWidth: 420 }}>
      <h2>Admin Sign-in</h2>
      <form onSubmit={onSubmit} style={{ display: 'grid', gap: 12 }}>
        <label>Email
          <input value={email} onChange={e => setEmail(e.target.value)} type="email" required style={{ width: '100%' }}/>
        </label>
        <label>Password
          <input value={password} onChange={e => setPassword(e.target.value)} type="password" required style={{ width: '100%' }}/>
        </label>
        {error && <div style={{ color: 'crimson' }}>{error}</div>}
        <button type="submit">Sign in</button>
      </form>
    </section>
  )
}
