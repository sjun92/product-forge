export default function SearchResult({ station, onAdd, added }) {
  return (
    <div style={styles.row}>
      <div>
        <span style={styles.name}>{station.station_name}</span>
        <span style={styles.city}>{station.city === 'seoul' ? '서울' : '경기'}</span>
      </div>
      <button
        onClick={() => onAdd(station)}
        disabled={added}
        style={added ? styles.addedBtn : styles.addBtn}
      >
        {added ? '추가됨' : '+ 추가'}
      </button>
    </div>
  )
}

const styles = {
  row: {
    display: 'flex', justifyContent: 'space-between', alignItems: 'center',
    padding: '12px', borderBottom: '1px solid #f0f0f0',
  },
  name: { fontWeight: 500 },
  city: {
    marginLeft: '8px', fontSize: '0.75rem', color: '#888',
    background: '#f5f5f5', padding: '2px 6px', borderRadius: '4px',
  },
  addBtn: {
    padding: '6px 14px', background: '#4285F4', color: '#fff',
    border: 'none', borderRadius: '6px', cursor: 'pointer', fontSize: '0.85rem',
  },
  addedBtn: {
    padding: '6px 14px', background: '#e0e0e0', color: '#999',
    border: 'none', borderRadius: '6px', cursor: 'default', fontSize: '0.85rem',
  },
}
