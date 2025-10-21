import { Routes, Route } from "react-router-dom"
import Navbar from "./components/NavBar"
import Home from "./pages/Home/Home"
import Academicos from "./pages/Academicos/Academicos"
import Profissionais from "./pages/Profissionais/Profissionais"
import './assets/styles/App.css'

export default function App() {
  return (
    <div className="min-h-screen bg-base-100 text-base-content font-gowunR">
      <Navbar />
      <Routes>
        <Route path='/' element = {<Home />} />
        <Route path='/Academicos' element = {<Academicos />} />
        <Route path='/Profissionais' element = {<Profissionais />} />
      </Routes>
    </div>
  );
}
import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  )
}

export default App
