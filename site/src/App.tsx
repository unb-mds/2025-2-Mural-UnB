import { Routes, Route, Navigate } from "react-router-dom"
import Navbar from "./components/NavBar"
import Home from "./pages/Home/Home"
import Academicos from "./pages/Academicos/Academicos"
import Profissionais from "./pages/Profissionais/Profissionais"
import './assets/styles/App.css'

export default function App() {
  return (
    <div data-theme="mural" className="min-h-screen w-screen bg-base-200 text-base-content font-gowun">
      <Navbar />
      <Routes>
        <Route path="/" element={<Navigate to="/home" replace />} />
        <Route path="/home" element={<Home />} />
        <Route path='/Academicos' element = {<Academicos />} />
        <Route path='/Profissionais' element = {<Profissionais />} />
      </Routes>
    </div>
  );
}

