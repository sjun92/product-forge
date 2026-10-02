import axios from 'axios'

const api = axios.create({
  baseURL: '/',
  withCredentials: true,   // httpOnly cookie 자동 전송
})

// 401 응답 → 로그인 페이지로 이동
api.interceptors.response.use(
  res => res,
  err => {
    if (err.response?.status === 401) {
      window.location.href = '/login'
    }
    return Promise.reject(err)
  }
)

export default api
