import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    open: true,
    host: true
  },
  build: {
    outDir: 'build',
    sourcemap: false,
    minify: 'terser',
    chunkSizeWarningLimit: 1600
  }
})
