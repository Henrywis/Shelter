import api from './client'

// flexible list (role-aware), supports ?status, ?shelter_id, ?page, ?page_size
export async function listIntakes(params = {}) {
  const { data } = await api.get('/intake/', { params })
  return data   // array when using /intake/; object when using /intake/search
}

// search endpoint with pagination + date range
export async function searchIntakes(params) {
  const { data } = await api.get('/intake/search', { params })
  return data   // { items, total, page, page_size }
}

export async function updateIntakeStatus(intakeId, status) {
  const { data } = await api.patch(`/intake/${intakeId}/status`, { status })
  return data
}

export function exportCsv(params = {}) {
  // force a file download via browser
  const url = new URL(`${api.defaults.baseURL}/intake/export.csv`)
  Object.entries(params).forEach(([k, v]) => {
    if (v !== undefined && v !== null && v !== '') url.searchParams.set(k, v)
  })
  window.location.href = url.toString()
}
