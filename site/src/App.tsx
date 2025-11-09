import { Routes, Route } from "react-router-dom"
import Navbar from "./components/NavBar"
import Footer from "./components/feed/Footer"
import Home from "./pages/Home/Home"
import FeedPage from "./pages/Oportunidades/FeedPage"
import DetailPage from "./pages/Oportunidades/DetailPage"
import './assets/styles/App.css'

export default function App() {
  return (
    <div data-theme="mural" className="min-h-screen w-screen bg-base-200 text-base-content font-gowun flex flex-col">
      <Navbar />
      <main className="flex-1">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path='/Oportunidades' element={<FeedPage />} />
          <Route path='/Oportunidades/:id' element={<DetailPage />} />s
        </Routes>
      </main>
      <Footer />
    </div>
  );
}

