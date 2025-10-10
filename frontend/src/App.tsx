import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import HomePage from './pages/HomePage'
import PetsPage from './pages/PetsPage'
import PetDetailPage from './pages/PetDetailPage'
import AdoptionsPage from './pages/AdoptionsPage'
import RecommendationsPage from './pages/RecommendationsPage'

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/pets" element={<PetsPage />} />
          <Route path="/pets/:id" element={<PetDetailPage />} />
          <Route path="/adoptions" element={<AdoptionsPage />} />
          <Route path="/recommendations" element={<RecommendationsPage />} />
        </Routes>
      </Layout>
    </Router>
  )
}

export default App
