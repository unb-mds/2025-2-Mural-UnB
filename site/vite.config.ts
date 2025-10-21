import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    tailwindcss()
  ],
  base: 'https://unb-mds.github.io/2025-2-Mural-UnB/',
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'), // com isso basta importar com @/'pasta dentro do src'/'item'
    },
  }
})
