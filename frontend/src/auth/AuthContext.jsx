import { createContext, useContext, useEffect, useState } from 'react'
import { login as apiLogin, me as apiMe, logout as apiLogout } from '../api/auth'

const AuthCtx = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) return setLoading(false)
    apiMe().then(setUser).catch(() => apiLogout()).finally(() => setLoading(false))
  }, [])

  const login = async (email, password) => {
    const { access_token } = await apiLogin(email, password)
    localStorage.setItem('token', access_token)
    const u = await apiMe()
    setUser(u)
    return u
  }
  const logout = () => {
    apiLogout()
    setUser(null)
  }

  return (
    <AuthCtx.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthCtx.Provider>
  )
}

export function useAuth() {
  return useContext(AuthCtx)
}
