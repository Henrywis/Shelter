import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'
import { useEffect, useState } from 'react'
import api from '../api/client'
import ShelterCard from '../components/ShelterCard.jsx'

export default function MapView() {
  const [shelters, setShelters] = useState([])
  const [healthy, setHealthy] = useState(null)

  useEffect(() => {
    // Health check (ensures backend reachable)
    api.get('/health').then(res => setHealthy(res.data?.status)).catch(() => setHealthy('down'))
    // Shelters endpoint will exist at Marker 4; placeholder now:
    setShelters([])
  }, [])

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
      <div>
        <h2>Nearby Shelters</h2>
        <p style={{ fontSize: 12, opacity: 0.7 }}>Backend health: {healthy ?? '...'}</p>
        {shelters.length === 0 && <p>No data yet. (Comes online at Marker 4)</p>}
        {shelters.map(s => <ShelterCard key={s.id} shelter={s} />)}
      </div>
      <div>
        <MapContainer style={{ height: 500 }} center={[36.1627, -86.7816]} zoom={12}>
          <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
          {shelters.map(s => (
            <Marker key={s.id} position={[s.geo_lat, s.geo_lng]}>
              <Popup>
                <strong>{s.name}</strong><br/>
                Beds available: {s.beds_available}
              </Popup>
            </Marker>
          ))}
        </MapContainer>
      </div>
    </div>
  )
}
