import axios from 'axios'

const api = axios.create({
  baseURL: '/',
  withCredentials: true,
})

api.interceptors.response.use(
  res => res,
  err => {
    // /auth/me의 401은 정상적인 비로그인 상태 — AuthContext에서 처리
    const isAuthMe = err.config?.url?.includes('/auth/me')
    if (err.response?.status === 401 && !isAuthMe) {
      window.location.href = '/login'
    }
    return Promise.reject(err)
  }
)

export default api
