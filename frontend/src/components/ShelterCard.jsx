export default function ShelterCard({ shelter }) {
    return (
      <div style={{ border: '1px solid #eee', borderRadius: 8, padding: 12, marginBottom: 8 }}>
        <h3 style={{ marginTop: 0 }}>{shelter.name}</h3>
        <div style={{ fontSize: 14, opacity: 0.8 }}>{shelter.address}</div>
        <div style={{ marginTop: 6 }}>Beds available: <strong>{shelter.beds_available}</strong></div>
      </div>
    )
  }
  