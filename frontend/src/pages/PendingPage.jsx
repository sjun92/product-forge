import api from '../api/client'
import { useNavigate } from 'react-router-dom'

export default function PendingPage() {
  const navigate = useNavigate()

  async function handleLogout() {
    await api.post('/auth/logout')
    navigate('/login')
  }

  return (
    <div style={styles.container}>
      <h2>승인 대기 중입니다</h2>
      <p style={styles.desc}>
        관리자가 계정을 승인하면 서비스를 이용할 수 있습니다.<br />
        승인 후 다시 로그인해 주세요.
      </p>
      <button onClick={handleLogout} style={styles.btn}>로그아웃</button>
    </div>
  )
}

const styles = {
  container: {
    display: 'flex', flexDirection: 'column', alignItems: 'center',
    justifyContent: 'center', height: '100vh', gap: '12px',
    fontFamily: 'sans-serif',
  },
  desc: { color: '#666', textAlign: 'center', lineHeight: '1.6' },
  btn: {
    padding: '8px 20px', background: '#ddd', border: 'none',
    borderRadius: '6px', cursor: 'pointer',
  },
}
