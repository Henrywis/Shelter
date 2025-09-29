import api from './client'

export async function listShelters() {
  const { data } = await api.get('/shelters')
  return data
}
