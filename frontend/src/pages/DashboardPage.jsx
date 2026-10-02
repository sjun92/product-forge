import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  DndContext, closestCenter, PointerSensor, useSensor, useSensors,
} from '@dnd-kit/core'
import {
  SortableContext, arrayMove, horizontalListSortingStrategy,
} from '@dnd-kit/sortable'
import api from '../api/client'
import { useAuth } from '../contexts/AuthContext'
import StationCard from '../components/StationCard'

export default function DashboardPage() {
  const { user } = useAuth()
  const navigate = useNavigate()
  const [favorites, setFavorites] = useState([])

  useEffect(() => {
    api.get('/favorites').then(res => setFavorites(res.data))
  }, [])

  const sensors = useSensors(useSensor(PointerSensor))

  async function handleDragEnd(event) {
    const { active, over } = event
    if (!over || active.id === over.id) return

    const oldIndex = favorites.findIndex(f => f.id === active.id)
    const newIndex = favorites.findIndex(f => f.id === over.id)
    const newOrder = arrayMove(favorites, oldIndex, newIndex)
    setFavorites(newOrder)
    await api.patch('/favorites/reorder', { order: newOrder.map(f => f.id) })
  }

  async function handleDelete(id) {
    await api.delete(`/favorites/${id}`)
    setFavorites(prev => prev.filter(f => f.id !== id))
  }

  return (
    <div style={styles.page}>
      <header style={styles.header}>
        <span>🚌 버스 도착 알리미</span>
        <div style={styles.headerRight}>
          {user?.is_admin && (
            <button onClick={() => navigate('/admin')} style={styles.adminBtn}>
              관리자
            </button>
          )}
          <span style={styles.userName}>{user?.name}</span>
        </div>
      </header>

      <div style={styles.toolbar}>
        <button onClick={() => navigate('/search')} style={styles.addBtn}>
          + 정류장 추가
        </button>
      </div>

      {favorites.length === 0 ? (
        <p style={styles.empty}>즐겨찾기 정류장이 없습니다. 정류장을 추가해 보세요.</p>
      ) : (
        <DndContext sensors={sensors} collisionDetection={closestCenter} onDragEnd={handleDragEnd}>
          <SortableContext items={favorites.map(f => f.id)} strategy={horizontalListSortingStrategy}>
            <div style={styles.grid}>
              {favorites.map(fav => (
                <StationCard key={fav.id} favorite={fav} onDelete={handleDelete} />
              ))}
            </div>
          </SortableContext>
        </DndContext>
      )}
    </div>
  )
}

const styles = {
  page: { fontFamily: 'sans-serif', padding: '0 24px 24px' },
  header: {
    display: 'flex', justifyContent: 'space-between', alignItems: 'center',
    padding: '16px 0', borderBottom: '1px solid #eee', marginBottom: '16px',
    fontWeight: 'bold', fontSize: '1.1rem',
  },
  headerRight: { display: 'flex', alignItems: 'center', gap: '12px' },
  userName: { fontSize: '0.9rem', color: '#666' },
  adminBtn: {
    padding: '4px 12px', background: '#f0f0f0', border: '1px solid #ddd',
    borderRadius: '6px', cursor: 'pointer', fontSize: '0.85rem',
  },
  toolbar: { marginBottom: '16px' },
  addBtn: {
    padding: '8px 16px', background: '#4285F4', color: '#fff',
    border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: 'bold',
  },
  empty: { color: '#999', marginTop: '40px', textAlign: 'center' },
  grid: { display: 'flex', gap: '16px', flexWrap: 'wrap' },
}
