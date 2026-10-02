import { useEffect, useState } from 'react'
import api from '../api/client'

export default function ArrivalList({ stationId, city }) {
  const [arrivals, setArrivals] = useState([])
  const [stale, setStale] = useState(false)
  const [error, setError] = useState(null)

  async function fetchArrivals() {
    try {
      const res = await api.get('/arrivals', { params: { station_id: stationId, city } })
      setArrivals(res.data.arrivals)
      setStale(res.data.stale)
      setError(null)
    } catch {
      setError('정보 갱신 실패')
    }
  }

  useEffect(() => {
    fetchArrivals()
    const timer = setInterval(fetchArrivals, 30_000)
    return () => clearInterval(timer)
  }, [stationId, city])

  if (error) return <p style={{ color: 'red', fontSize: '0.8rem' }}>{error}</p>
  if (!arrivals.length) return <p style={{ color: '#999', fontSize: '0.8rem' }}>도착 정보 없음</p>

  return (
    <ul style={styles.list}>
      {stale && <li style={styles.stale}>⚠ 이전 정보 표시 중</li>}
      {arrivals.map((a, i) => (
        <li key={i} style={styles.item}>
          <span style={styles.route}>{a.route_name}</span>
          <span style={styles.msg}>{a.arrival_msg}</span>
        </li>
      ))}
    </ul>
  )
}

const styles = {
  list: { listStyle: 'none', padding: 0, margin: 0 },
  stale: { color: '#e67e22', fontSize: '0.75rem', marginBottom: '4px' },
  item: { display: 'flex', justifyContent: 'space-between', padding: '4px 0',
          borderBottom: '1px solid #f0f0f0', fontSize: '0.9rem' },
  route: { fontWeight: 'bold', color: '#333' },
  msg: { color: '#555' },
}
