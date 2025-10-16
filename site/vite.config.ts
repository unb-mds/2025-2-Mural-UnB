import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
<<<<<<< HEAD
import path from 'path'
=======
>>>>>>> 17e311137a9a8bc594ce68d30aa61eb31bdaee8b

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    tailwindcss()
  ],
<<<<<<< HEAD
  base: 'https://unb-mds.github.io/2025-2-Mural-UnB/',
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'), // com isso basta importar com @/'pasta dentro do src'/'item'
    },
  },
=======
  base: '/2025-2-Mural-UnB/',
>>>>>>> 17e311137a9a8bc594ce68d30aa61eb31bdaee8b
})
