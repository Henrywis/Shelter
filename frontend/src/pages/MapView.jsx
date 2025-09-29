import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'
import { useEffect, useState } from 'react'
import { listShelters } from '../api/shelters'
import ShelterCard from '../components/ShelterCard.jsx'

export default function MapView() {
  const [shelters, setShelters] = useState([])
  const [healthy, setHealthy] = useState(null)

  useEffect(() => {
    // health ping
    fetch(`${import.meta.env.VITE_API_BASE || 'http://localhost:8000'}/health`)
      .then(r => r.json()).then(d => setHealthy(d?.status || 'ok'))
      .catch(() => setHealthy('down'))

    // load shelters (Marker 4+ live)
    listShelters().then(setShelters).catch(() => setShelters([]))
  }, [])

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
      <div>
        <h2>Nearby Shelters</h2>
        <p style={{ fontSize: 12, opacity: 0.7 }}>Backend health: {healthy ?? '...'}</p>
        {shelters.length === 0 && <p>No shelters found.</p>}
        {shelters.map(s => <ShelterCard key={s.id} shelter={s} />)}
      </div>
      <div>
        <MapContainer style={{ height: 500 }} center={[36.1627, -86.7816]} zoom={12}>
          <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
          {shelters.map(s => (
            <Marker key={s.id} position={[s.geo_lat, s.geo_lng]}>
              <Popup>
                <strong>{s.name}</strong><br/>
                {s.address}<br/>
                Beds available: {s.beds_available ?? '—'}
              </Popup>
            </Marker>
          ))}
        </MapContainer>
      </div>
    </div>
  )
}
