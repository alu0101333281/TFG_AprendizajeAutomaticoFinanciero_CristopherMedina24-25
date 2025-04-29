import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  root: path.resolve(__dirname, 'frontend/vite-project'), // especifica la raíz del frontend
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'frontend/vite-project/src'),
    },
  },
})
