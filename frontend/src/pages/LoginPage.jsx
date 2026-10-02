export default function LoginPage() {
  return (
    <div style={styles.container}>
      <h1 style={styles.title}>🚌 버스 도착 알리미</h1>
      <p style={styles.subtitle}>사내 내부 툴 — 수도권 버스 도착 정보</p>
      <a href="/auth/google" style={styles.button}>
        Google 계정으로 로그인
      </a>
    </div>
  )
}

const styles = {
  container: {
    display: 'flex', flexDirection: 'column', alignItems: 'center',
    justifyContent: 'center', height: '100vh', gap: '16px',
    fontFamily: 'sans-serif',
  },
  title: { fontSize: '2rem', margin: 0 },
  subtitle: { color: '#666', margin: 0 },
  button: {
    padding: '12px 24px', backgroundColor: '#4285F4', color: '#fff',
    borderRadius: '8px', textDecoration: 'none', fontWeight: 'bold',
    fontSize: '1rem',
  },
}
