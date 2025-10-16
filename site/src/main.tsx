import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
<<<<<<< HEAD
import { BrowserRouter } from 'react-router-dom'
import './assets/styles/index.css'
=======
import './index.css'
>>>>>>> 17e311137a9a8bc594ce68d30aa61eb31bdaee8b
import App from './App.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
<<<<<<< HEAD
    <BrowserRouter>
      <App />
    </BrowserRouter>
=======
    <App />
>>>>>>> 17e311137a9a8bc594ce68d30aa61eb31bdaee8b
  </StrictMode>,
)
