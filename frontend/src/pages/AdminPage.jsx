import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../api/client'
import UserRow from '../components/UserRow'

export default function AdminPage() {
  const navigate = useNavigate()
  const [users, setUsers] = useState([])
  const [tab, setTab] = useState('pending')
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState(null)
  const [loadingId, setLoadingId] = useState(null)

  useEffect(() => {
    api.get('/admin/users')
      .then(res => setUsers(res.data))
      .catch(() => setError('사용자 목록을 불러오지 못했습니다'))
      .finally(() => setIsLoading(false))
  }, [])

  async function handleApprove(userId, isApproved) {
    if (loadingId !== null) return
    const snapshot = users
    setLoadingId(userId)
    setUsers(prev => prev.map(u => u.id === userId ? { ...u, is_approved: isApproved } : u))
    try {
      await api.patch(`/admin/users/${userId}/approve`, { is_approved: isApproved })
    } catch {
      setUsers(snapshot)
      setError('상태 변경 중 오류가 발생했습니다')
    } finally {
      setLoadingId(null)
    }
  }

  const displayed = tab === 'pending'
    ? users.filter(u => !u.is_approved)
    : users

  return (
    <div style={styles.page}>
      <header style={styles.header}>
        <button onClick={() => navigate('/')} style={styles.back}>← 대시보드</button>
        <h2 style={styles.title}>관리자 — 사용자 관리</h2>
      </header>

      {error && <p style={styles.error}>{error}</p>}

      <div style={styles.tabs}>
        <button
          onClick={() => setTab('pending')}
          style={tab === 'pending' ? styles.activeTab : styles.tab}
        >
          승인 대기 ({users.filter(u => !u.is_approved).length})
        </button>
        <button
          onClick={() => setTab('all')}
          style={tab === 'all' ? styles.activeTab : styles.tab}
        >
          전체 ({users.length})
        </button>
      </div>

      <table style={styles.table}>
        <thead>
          <tr>
            {['이름', '이메일', '상태', '액션'].map(h => (
              <th key={h} style={styles.th}>{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {isLoading ? (
            <tr><td colSpan={4} style={styles.empty}>불러오는 중...</td></tr>
          ) : displayed.length === 0 ? (
            <tr><td colSpan={4} style={styles.empty}>해당 사용자 없음</td></tr>
          ) : (
            displayed.map(u => (
              <UserRow
                key={u.id}
                user={u}
                onApprove={handleApprove}
                disabled={loadingId !== null}
              />
            ))
          )}
        </tbody>
      </table>
    </div>
  )
}

const styles = {
  page: { fontFamily: 'sans-serif', padding: '0 24px 24px', maxWidth: '700px', margin: '0 auto' },
  header: { display: 'flex', alignItems: 'center', gap: '12px', padding: '16px 0',
             borderBottom: '1px solid #eee', marginBottom: '16px' },
  back: { background: 'none', border: 'none', cursor: 'pointer', color: '#4285F4', fontSize: '0.95rem' },
  title: { margin: 0, fontSize: '1.1rem' },
  tabs: { display: 'flex', gap: '8px', marginBottom: '16px' },
  tab: {
    padding: '6px 16px', background: '#f5f5f5', border: '1px solid #ddd',
    borderRadius: '6px', cursor: 'pointer', fontSize: '0.9rem',
  },
  activeTab: {
    padding: '6px 16px', background: '#4285F4', color: '#fff',
    border: '1px solid #4285F4', borderRadius: '6px', cursor: 'pointer', fontSize: '0.9rem',
  },
  table: { width: '100%', borderCollapse: 'collapse' },
  th: { padding: '10px 12px', background: '#f8f8f8', textAlign: 'left',
        fontSize: '0.85rem', color: '#666', fontWeight: 600 },
  empty: { padding: '24px', textAlign: 'center', color: '#999' },
  error: { color: '#e74c3c', fontSize: '0.85rem', marginBottom: '12px' },
}
