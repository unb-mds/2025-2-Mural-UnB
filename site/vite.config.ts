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
  server: {
    open: '/2025-2-Mural-UnB/home'
  },
  base: process.env.NODE_ENV === 'production' 
    ? 'https://unb-mds.github.io/2025-2-Mural-UnB/' 
    : '/2025-2-Mural-UnB/',
  resolve: {
    alias: {
      components: path.resolve(__dirname, "src/components"),
      assets: path.resolve(__dirname, "src/assets"),
    },
  },
})
