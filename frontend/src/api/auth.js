import api from './client'

export async function login(email, password) {
  const { data } = await api.post('/auth/login', { email, password })
  return data   // { access_token, token_type }
}
export async function me() {
  const { data } = await api.get('/auth/me')
  return data
}
export function logout() {
  localStorage.removeItem('token')
}
