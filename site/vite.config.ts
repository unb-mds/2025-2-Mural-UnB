import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';
import path from 'path';

// O nome do repositório. O GH Pages serve o site neste subdiretório.
const REPO_NAME = '2025-2-Mural-UnB'; 

export default defineConfig({
  plugins: [
    react(),
    tailwindcss()
  ],
  server: {
    open: false,
  },
  base: `/${REPO_NAME}/`, 
  resolve: {
    alias: {
      components: path.resolve(__dirname, "src/components"),
      assets: path.resolve(__dirname, "src/assets"),
      data: path.resolve(__dirname, "src/data")
    },
  },
})
