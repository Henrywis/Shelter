export default function StatusBadge({ value }) {
  const v = (value || '').toLowerCase()

  const cls =
    v === 'fulfilled'
      ? 'status-badge status-badge-fulfilled'
      : v === 'cancelled'
      ? 'status-badge status-badge-cancelled'
      : 'status-badge status-badge-pending'

  return <span className={cls}>{v || 'pending'}</span>
}
