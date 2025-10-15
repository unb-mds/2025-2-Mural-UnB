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
