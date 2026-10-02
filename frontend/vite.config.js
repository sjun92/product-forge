import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/auth': 'http://localhost:8000',
      '/favorites': 'http://localhost:8000',
      '/arrivals': 'http://localhost:8000',
      '/search': 'http://localhost:8000',
      '/admin': 'http://localhost:8000',
    }
  }
})
