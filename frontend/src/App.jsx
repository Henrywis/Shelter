import { Routes, Route, Link } from 'react-router-dom'
import MapView from './pages/MapView.jsx'
import AdminPortal from './pages/AdminPortal.jsx'
import Header from './components/Header.jsx'

export default function App() {
  return (
    <>
      <Header />
      <main style={{ padding: 16 }}>
        <Routes>
          <Route path="/" element={<MapView />} />
          <Route path="/admin" element={<AdminPortal />} />
        </Routes>
      </main>
      <footer style={{ padding: 16, fontSize: 12, opacity: 0.7 }}>
        Shelter Capacity &bull; v0.1.0
      </footer>
    </>
  )
}
