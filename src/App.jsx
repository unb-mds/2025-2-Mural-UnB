import { HashRouter as Router, Routes, Route } from "react-router-dom"
import Navbar from "./components/Navbar"
import FeedPage from "./pages/FeedPage"
import DetailPage from "./pages/DetailPage"
import Footer from "./components/Footer"
import "./App.css"

function App() {
  return (
    <Router>
      <div className="flex flex-col min-h-screen">
        <Navbar />
        <main className="flex-grow">
          <Routes>
            <Route path="/" element={<FeedPage />} />
            <Route path="/oportunidade/:id" element={<DetailPage />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  )
}

export default App
