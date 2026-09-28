import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { Navigation, Footer, ScrollToTop } from './components'
import { Home, Portfolio } from './pages'
import { useCopyClean } from './hooks/useCopyClean'

function App() {
  useCopyClean()

  return (
    <BrowserRouter basename={import.meta.env.BASE_URL}>
      <ScrollToTop />
      <div className="min-h-screen bg-white">
        <Navigation />

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/demos" element={<Portfolio />} />
          <Route path="/proyectos" element={<Navigate to="/demos" replace />} />
        </Routes>

        <Footer />
      </div>
    </BrowserRouter>
  )
}

export default App
