import { useSortable } from '@dnd-kit/sortable'
import { CSS } from '@dnd-kit/utilities'
import ArrivalList from './ArrivalList'

export default function StationCard({ favorite, onDelete }) {
  const { attributes, listeners, setNodeRef, transform, transition, isDragging } =
    useSortable({ id: favorite.id })

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.5 : 1,
  }

  return (
    <div ref={setNodeRef} style={{ ...styles.card, ...style }}>
      <div style={styles.header}>
        <span {...attributes} {...listeners} style={styles.drag}>⠿</span>
        <span style={styles.name}>{favorite.station_name}</span>
        <span style={styles.city}>{favorite.city === 'seoul' ? '서울' : '경기'}</span>
        <button onClick={() => onDelete(favorite.id)} style={styles.del}>삭제</button>
      </div>
      <ArrivalList stationId={favorite.station_id} city={favorite.city} />
    </div>
  )
}

const styles = {
  card: {
    background: '#fff', border: '1px solid #e0e0e0', borderRadius: '12px',
    padding: '16px', minWidth: '240px', boxShadow: '0 2px 4px rgba(0,0,0,0.06)',
  },
  header: { display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px' },
  drag: { cursor: 'grab', color: '#bbb', fontSize: '1.2rem', userSelect: 'none' },
  name: { fontWeight: 'bold', flex: 1, fontSize: '1rem' },
  city: { fontSize: '0.75rem', color: '#888', background: '#f5f5f5',
          padding: '2px 6px', borderRadius: '4px' },
  del: { border: 'none', background: 'none', color: '#e74c3c', cursor: 'pointer',
         fontSize: '0.85rem' },
}
