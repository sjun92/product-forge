import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../api/client'
import SearchResult from '../components/SearchResult'

export default function SearchPage() {
  const navigate = useNavigate()
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [errors, setErrors] = useState([])
  const [addedIds, setAddedIds] = useState(new Set())

  async function handleSearch(e) {
    e.preventDefault()
    if (!query.trim()) return
    setLoading(true)
    try {
      const res = await api.get('/search/stations', { params: { q: query } })
      setResults(res.data.results)
      setErrors(res.data.errors)
    } catch {
      setErrors(['검색 중 오류가 발생했습니다'])
    } finally {
      setLoading(false)
    }
  }

  async function handleAdd(station) {
    await api.post('/favorites', {
      station_id: station.station_id,
      station_name: station.station_name,
      city: station.city,
    })
    setAddedIds(prev => new Set([...prev, station.station_id]))
  }

  return (
    <div style={styles.page}>
      <header style={styles.header}>
        <button onClick={() => navigate('/')} style={styles.back}>← 돌아가기</button>
        <h2 style={styles.title}>정류장 검색</h2>
      </header>

      <form onSubmit={handleSearch} style={styles.form}>
        <input
          value={query}
          onChange={e => setQuery(e.target.value)}
          placeholder="정류장 이름을 입력하세요"
          style={styles.input}
        />
        <button type="submit" style={styles.searchBtn} disabled={loading}>
          {loading ? '검색 중...' : '검색'}
        </button>
      </form>

      {errors.length > 0 && (
        <p style={styles.error}>{errors.join(' / ')}</p>
      )}

      <div>
        {results.length === 0 && !loading && query && (
          <p style={styles.empty}>검색 결과가 없습니다</p>
        )}
        {results.map(station => (
          <SearchResult
            key={`${station.city}:${station.station_id}`}
            station={station}
            onAdd={handleAdd}
            added={addedIds.has(station.station_id)}
          />
        ))}
      </div>
    </div>
  )
}

const styles = {
  page: { fontFamily: 'sans-serif', padding: '0 24px 24px', maxWidth: '600px', margin: '0 auto' },
  header: { display: 'flex', alignItems: 'center', gap: '12px', padding: '16px 0',
             borderBottom: '1px solid #eee', marginBottom: '16px' },
  back: { background: 'none', border: 'none', cursor: 'pointer', color: '#4285F4', fontSize: '0.95rem' },
  title: { margin: 0, fontSize: '1.1rem' },
  form: { display: 'flex', gap: '8px', marginBottom: '16px' },
  input: {
    flex: 1, padding: '10px', border: '1px solid #ddd',
    borderRadius: '8px', fontSize: '1rem', outline: 'none',
  },
  searchBtn: {
    padding: '10px 20px', background: '#4285F4', color: '#fff',
    border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: 'bold',
  },
  error: { color: '#e74c3c', fontSize: '0.85rem' },
  empty: { color: '#999', textAlign: 'center', marginTop: '24px' },
}
