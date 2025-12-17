import { Routes, Route } from "react-router-dom"
import Navbar from "./components/NavBar"
import Footer from "./components/Footer"
import Home from "./pages/Home"
import Sobre from "./pages/About"
import FeedPage from "./pages/Feed"
import DetailPage from "./pages/Oportunity"
import "./assets/styles/App.css"

export default function App() {
  return (
    <div data-theme="mural" className="min-h-screen w-screen bg-base-200 text-base-content font-gowun flex flex-col">
      <Navbar />
      <main className="flex-1">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<Sobre />} />
          <Route path="/feed" element={<FeedPage />} />
          <Route path="/feed/:id" element={<DetailPage />} />
        </Routes>
      </main>
      <Footer />
    </div>
  );
}

