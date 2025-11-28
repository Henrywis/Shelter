import { useEffect, useMemo, useState } from 'react'
import { useAuth } from '../auth/AuthContext.jsx'
import { listIntakes, searchIntakes, updateIntakeStatus, exportCsv } from '../api/intake'
import StatusBadge from '../components/StatusBadge.jsx'
import { format } from 'date-fns'

const PAGE_SIZE_DEFAULT = 10
const PAGE_SIZE_OPTIONS = [5, 10, 20, 50]

export default function AdminPortal() {
  const { user, logout } = useAuth()
  const [loading, setLoading] = useState(false)
  const [items, setItems] = useState([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [pageSize, setPageSize] = useState(PAGE_SIZE_DEFAULT)
  const [status, setStatus] = useState('')   // '' = all
  const [fromDt, setFromDt] = useState('')
  const [toDt, setToDt] = useState('')

  const fetchData = async () => {
    setLoading(true)
    try {
      const params = {
        page,
        page_size: pageSize,
        status: status || undefined,
        from_dt: fromDt || undefined,
        to_dt: toDt || undefined,
      }
      const data = await searchIntakes(params)
      setItems(data.items || [])
      setTotal(data.total || (data.length ?? 0))
    } catch (e) {
      console.error(e)
      alert('Failed to fetch intakes')
    } finally {
      setLoading(false)
    }
  }

  // initial + pagination
  useEffect(() => { fetchData() }, [page, pageSize]) // eslint-disable-line

  // filters reset page + refetch
  useEffect(() => {
    setPage(1)
    fetchData()
  }, [status, fromDt, toDt]) // eslint-disable-line

  const onChangeStatus = async (row, newStatus) => {
    try {
      const updated = await updateIntakeStatus(row.id, newStatus)
      setItems(prev => prev.map(it => it.id === row.id ? updated : it))
    } catch (e) {
      console.error(e)
      alert('Failed to update status')
    }
  }

  const pages = useMemo(
    () => Math.max(1, Math.ceil((total || 0) / pageSize)),
    [total, pageSize]
  )

  return (
    <section className="admin-page">
      {/* Top bar: title + user + sign out */}
      <div className="admin-topbar">
        <div>
          <h2 className="page-title">Admin Portal</h2>
          <p className="page-subtitle">
            Signed in as <strong>{user?.email}</strong> ({user?.role})
          </p>
        </div>
        <button className="btn-outline" onClick={logout}>
          Sign out
        </button>
      </div>

      {/* Filters card */}
      <div className="card admin-filters-card">
        <div className="filters-grid">
          <div className="form-field">
            <label htmlFor="status" className="form-label">Status</label>
            <select
              id="status"
              className="input"
              value={status}
              onChange={e => setStatus(e.target.value)}
            >
              <option value="">All</option>
              <option value="pending">Pending</option>
              <option value="fulfilled">Fulfilled</option>
              <option value="cancelled">Cancelled</option>
            </select>
          </div>

          <div className="form-field">
            <label htmlFor="fromDt" className="form-label">From (UTC)</label>
            <input
              id="fromDt"
              type="datetime-local"
              className="input"
              value={fromDt}
              onChange={e => setFromDt(e.target.value)}
            />
          </div>

          <div className="form-field">
            <label htmlFor="toDt" className="form-label">To (UTC)</label>
            <input
              id="toDt"
              type="datetime-local"
              className="input"
              value={toDt}
              onChange={e => setToDt(e.target.value)}
            />
          </div>

          <div className="form-field">
            <label htmlFor="pageSize" className="form-label">Page size</label>
            <select
              id="pageSize"
              className="input"
              value={pageSize}
              onChange={e => setPageSize(Number(e.target.value))}
            >
              {PAGE_SIZE_OPTIONS.map(n => (
                <option key={n} value={n}>{n}</option>
              ))}
            </select>
          </div>

          <div className="form-field admin-export-cell">
            <button
              className="btn-outline w-full"
              onClick={() => exportCsv({ status: status || undefined })}
            >
              Export CSV (current filter)
            </button>
          </div>
        </div>
      </div>

      {/* Table card */}
      <div className="card admin-table-card">
        <div className="table-scroll">
          <table className="admin-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Shelter</th>
                <th>Name</th>
                <th>Reason</th>
                <th>ETA</th>
                <th>Created</th>
                <th>Status</th>
                <th>Change</th>
              </tr>
            </thead>
            <tbody>
              {loading && (
                <tr>
                  <td colSpan="8" className="table-empty">
                    Loading intakes…
                  </td>
                </tr>
              )}
              {!loading && items.length === 0 && (
                <tr>
                  <td colSpan="8" className="table-empty">
                    No intakes found
                  </td>
                </tr>
              )}
              {!loading && items.map(row => (
                <tr key={row.id}>
                  <td>{row.id}</td>
                  <td>
                    <div className="table-shelter">
                      <div className="table-shelter-name">
                        {row.shelter?.name}
                      </div>
                      <div className="table-shelter-address">
                        {row.shelter?.address}
                      </div>
                    </div>
                  </td>
                  <td>{row.name || '—'}</td>
                  <td className="table-reason">{row.reason || '—'}</td>
                  <td>
                    {row.eta
                      ? format(new Date(row.eta), 'yyyy-MM-dd HH:mm')
                      : '—'}
                  </td>
                  <td>
                    {format(new Date(row.created_at), 'yyyy-MM-dd HH:mm')}
                  </td>
                  <td>
                    <StatusBadge value={row.status} />
                  </td>
                  <td>
                    <select
                      className="input input-compact"
                      value={row.status}
                      onChange={e => onChangeStatus(row, e.target.value)}
                    >
                      <option value="pending">Pending</option>
                      <option value="fulfilled">Fulfilled</option>
                      <option value="cancelled">Cancelled</option>
                    </select>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        <div className="admin-table-footer">
          <div className="table-page-info">
            Page {page} of {pages}
          </div>
          <div className="table-pager">
            <button
              className="btn-outline btn-sm"
              disabled={page <= 1}
              onClick={() => setPage(p => Math.max(1, p - 1))}
            >
              Prev
            </button>
            <button
              className="btn-outline btn-sm"
              disabled={page >= pages}
              onClick={() => setPage(p => Math.min(pages, p + 1))}
            >
              Next
            </button>
          </div>
        </div>
      </div>
    </section>
  )
}
