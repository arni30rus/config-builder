import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  // <-- ДОБАВЛЯЕМ ЭТОТ БЛОК ДЛЯ ПРОКСИ -->
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000', // Адрес нашего бэкенда
        changeOrigin: true,
      }
    }
  }
})
