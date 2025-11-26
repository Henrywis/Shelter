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

export async function exportCsv(params = {}) {
  try {
    const res = await api.get('/intake/export.csv', {
      params,
      responseType: 'blob', // important for binary/CSV
    })

    const blob = new Blob([res.data], { type: 'text/csv;charset=utf-8;' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'intakes.csv'
    document.body.appendChild(a)
    a.click()
    a.remove()
    window.URL.revokeObjectURL(url)
  } catch (err) {
    console.error(err)
    alert('CSV export failed')
  }
}
