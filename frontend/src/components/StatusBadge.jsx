export default function StatusBadge({ value }) {
    const v = (value || '').toLowerCase()
    const styles = {
      base: {
        display: 'inline-block',
        padding: '2px 8px',
        borderRadius: 999,
        fontSize: 12,
        fontWeight: 600,
        border: '1px solid transparent'
      },
      pending: { background: '#f3f4f6', color: '#111827', borderColor: '#e5e7eb' },     // gray
      fulfilled: { background: '#ecfdf5', color: '#065f46', borderColor: '#a7f3d0' },   // green
      cancelled: { background: '#fef2f2', color: '#991b1b', borderColor: '#fecaca' }    // red
    }
    const style = { ...styles.base, ...(styles[v] || styles.pending) }
    return <span style={style}>{v}</span>
  }
  