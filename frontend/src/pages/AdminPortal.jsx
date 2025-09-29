import { useEffect, useMemo, useState } from 'react'
import { useAuth } from '../auth/AuthContext.jsx'
import { listIntakes, searchIntakes, updateIntakeStatus, exportCsv } from '../api/intake'
import StatusBadge from '../components/StatusBadge.jsx'
import { format } from 'date-fns'

const PAGE_SIZE_DEFAULT = 10

export default function AdminPortal() {
  const { user } = useAuth()
  const [loading, setLoading] = useState(false)
  const [items, setItems] = useState([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [pageSize, setPageSize] = useState(PAGE_SIZE_DEFAULT)
  const [status, setStatus] = useState('')
  const [fromDt, setFromDt] = useState('')
  const [toDt, setToDt] = useState('')

  const isAdmin = user?.role === 'admin'

  const fetchData = async () => {
    setLoading(true)
    try {
      // use search endpoint when any filter/pagination present
      const params = {
        page, page_size: pageSize,
        status: status || undefined,
        from_dt: fromDt || undefined,
        to_dt: toDt || undefined,
        // admins can filter by shelter_id later from a dropdown; leave undefined for now
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

  useEffect(() => { fetchData() }, [page, pageSize]) // eslint-disable-line
  // refetch when filters change
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

  const pages = useMemo(() => Math.max(1, Math.ceil((total || 0) / pageSize)), [total, pageSize])

  return (
    <section>
      <h2>Admin Portal</h2>
      <p style={{ fontSize: 12, opacity: 0.7 }}>
        Signed in as <strong>{user?.email}</strong> ({user?.role})
      </p>

      {/* Filters */}
      <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap', alignItems: 'end', margin: '12px 0' }}>
        <label>Status<br/>
          <select value={status} onChange={e => setStatus(e.target.value)} style={{ minWidth: 160 }}>
            <option value="">All</option>
            <option value="pending">Pending</option>
            <option value="fulfilled">Fulfilled</option>
            <option value="cancelled">Cancelled</option>
          </select>
        </label>
        <label>From (UTC)<br/>
          <input type="datetime-local" value={fromDt} onChange={e => setFromDt(e.target.value)} />
        </label>
        <label>To (UTC)<br/>
          <input type="datetime-local" value={toDt} onChange={e => setToDt(e.target.value)} />
        </label>
        <label>Page size<br/>
          <select value={pageSize} onChange={e => setPageSize(Number(e.target.value))}>
            {[5,10,20,50].map(n => <option key={n} value={n}>{n}</option>)}
          </select>
        </label>
        <button onClick={() => exportCsv({ status: status || undefined })}>
          Export CSV (current filter)
        </button>
      </div>

      {/* Table */}
      <div style={{ overflowX: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ textAlign: 'left', borderBottom: '1px solid #eee' }}>
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
              <tr><td colSpan="8" style={{ padding: 12 }}>Loading…</td></tr>
            )}
            {!loading && items.length === 0 && (
              <tr><td colSpan="8" style={{ padding: 12 }}>No results</td></tr>
            )}
            {!loading && items.map(row => (
              <tr key={row.id} style={{ borderBottom: '1px solid #f2f2f2' }}>
                <td style={{ padding: 8 }}>{row.id}</td>
                <td style={{ padding: 8 }}>
                  <div style={{ fontWeight: 600 }}>{row.shelter?.name}</div>
                  <div style={{ fontSize: 12, opacity: 0.7 }}>{row.shelter?.address}</div>
                </td>
                <td style={{ padding: 8 }}>{row.name || '—'}</td>
                <td style={{ padding: 8, maxWidth: 260 }}>{row.reason || '—'}</td>
                <td style={{ padding: 8 }}>{row.eta ? format(new Date(row.eta), 'yyyy-MM-dd HH:mm') : '—'}</td>
                <td style={{ padding: 8 }}>{format(new Date(row.created_at), 'yyyy-MM-dd HH:mm')}</td>
                <td style={{ padding: 8 }}><StatusBadge value={row.status} /></td>
                <td style={{ padding: 8 }}>
                  <select value={row.status} onChange={e => onChangeStatus(row, e.target.value)}>
                    <option value="pending">pending</option>
                    <option value="fulfilled">fulfilled</option>
                    <option value="cancelled">cancelled</option>
                  </select>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      <div style={{ display: 'flex', gap: 8, alignItems: 'center', marginTop: 12 }}>
        <button disabled={page <= 1} onClick={() => setPage(p => Math.max(1, p - 1))}>Prev</button>
        <span>Page {page} / {pages}</span>
        <button disabled={page >= pages} onClick={() => setPage(p => Math.min(pages, p + 1))}>Next</button>
      </div>
    </section>
  )
}
