export default function UserRow({ user, onApprove }) {
  return (
    <tr>
      <td style={styles.td}>{user.name}</td>
      <td style={styles.td}>{user.email}</td>
      <td style={styles.td}>
        <span style={user.is_approved ? styles.approved : styles.pending}>
          {user.is_approved ? '승인됨' : '대기'}
        </span>
      </td>
      <td style={styles.td}>
        {user.is_approved ? (
          <button onClick={() => onApprove(user.id, false)} style={styles.blockBtn}>
            차단
          </button>
        ) : (
          <button onClick={() => onApprove(user.id, true)} style={styles.approveBtn}>
            승인
          </button>
        )}
      </td>
    </tr>
  )
}

const styles = {
  td: { padding: '10px 12px', borderBottom: '1px solid #f0f0f0' },
  approved: { color: '#27ae60', fontWeight: 500 },
  pending: { color: '#e67e22', fontWeight: 500 },
  approveBtn: {
    padding: '4px 12px', background: '#27ae60', color: '#fff',
    border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '0.85rem',
  },
  blockBtn: {
    padding: '4px 12px', background: '#e74c3c', color: '#fff',
    border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '0.85rem',
  },
}
