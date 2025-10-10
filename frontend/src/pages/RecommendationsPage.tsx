import { useState } from 'react'
import { Sparkles, Search } from 'lucide-react'
import PetCard from '@/components/PetCard'
import { getRecommendations } from '@/lib/api'

export default function RecommendationsPage() {
  const [userId, setUserId] = useState('')
  const [preferences, setPreferences] = useState({
    species: '',
    size: '',
  })
  const [recommendations, setRecommendations] = useState([])
  const [loading, setLoading] = useState(false)
  const [searched, setSearched] = useState(false)

  const handleGetRecommendations = async () => {
    if (!userId) {
      alert('Please enter a user ID')
      return
    }

    try {
      setLoading(true)
      const prefs = Object.fromEntries(
        Object.entries(preferences).filter(([_, v]) => v !== '')
      )
      const response = await getRecommendations(parseInt(userId), prefs)
      setRecommendations(response.data)
      setSearched(true)
    } catch (error) {
      console.error('Error fetching recommendations:', error)
      alert('Error fetching recommendations. Make sure the user ID exists.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2 flex items-center">
          <Sparkles className="h-8 w-8 mr-3 text-purple-500" />
          Pet Recommendations
        </h1>
        <p className="text-gray-600">
          Get personalized pet recommendations powered by Neo4j graph database
        </p>
      </div>

      {/* Search Form */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              User ID *
            </label>
            <input
              type="number"
              value={userId}
              onChange={(e) => setUserId(e.target.value)}
              placeholder="Enter user ID"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Preferred Species
            </label>
            <select
              value={preferences.species}
              onChange={(e) => setPreferences({ ...preferences, species: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
            >
              <option value="">Any</option>
              <option value="dog">Dog</option>
              <option value="cat">Cat</option>
              <option value="rabbit">Rabbit</option>
              <option value="bird">Bird</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Preferred Size
            </label>
            <select
              value={preferences.size}
              onChange={(e) => setPreferences({ ...preferences, size: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
            >
              <option value="">Any</option>
              <option value="small">Small</option>
              <option value="medium">Medium</option>
              <option value="large">Large</option>
            </select>
          </div>
        </div>
        <button
          onClick={handleGetRecommendations}
          disabled={loading}
          className="w-full bg-gradient-to-r from-purple-500 to-purple-600 text-white py-3 rounded-lg font-semibold hover:from-purple-600 hover:to-purple-700 transition-colors flex items-center justify-center disabled:opacity-50"
        >
          <Search className="h-5 w-5 mr-2" />
          {loading ? 'Finding Recommendations...' : 'Get Recommendations'}
        </button>
      </div>

      {/* How It Works */}
      <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-lg p-6 mb-8">
        <h2 className="text-lg font-semibold text-gray-900 mb-3">How Recommendations Work</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-gray-700">
          <div className="flex items-start">
            <div className="bg-purple-500 text-white rounded-full w-6 h-6 flex items-center justify-center mr-2 mt-0.5 flex-shrink-0">
              1
            </div>
            <p>
              <strong>Preference Matching:</strong> Pets matching your species and size preferences get higher scores
            </p>
          </div>
          <div className="flex items-start">
            <div className="bg-purple-500 text-white rounded-full w-6 h-6 flex items-center justify-center mr-2 mt-0.5 flex-shrink-0">
              2
            </div>
            <p>
              <strong>Tag Similarity:</strong> Pets with tags you're interested in are prioritized
            </p>
          </div>
          <div className="flex items-start">
            <div className="bg-purple-500 text-white rounded-full w-6 h-6 flex items-center justify-center mr-2 mt-0.5 flex-shrink-0">
              3
            </div>
            <p>
              <strong>Social Connections:</strong> Pets similar to those adopted by your friends are recommended
            </p>
          </div>
        </div>
      </div>

      {/* Results */}
      {loading ? (
        <div className="text-center py-12">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-purple-500"></div>
          <p className="mt-4 text-gray-600">Finding your perfect match...</p>
        </div>
      ) : searched && recommendations.length === 0 ? (
        <div className="text-center py-12 bg-white rounded-lg shadow-md">
          <Sparkles className="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-600">No recommendations found. Try adjusting your preferences.</p>
        </div>
      ) : recommendations.length > 0 ? (
        <div>
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            Recommended for You ({recommendations.length})
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {recommendations.map((rec: any) => (
              <div key={rec.pet_id} className="relative">
                <div className="absolute top-2 right-2 z-10 bg-purple-500 text-white px-3 py-1 rounded-full text-sm font-medium shadow-lg">
                  Score: {rec.score.toFixed(1)}
                </div>
                {rec.pet_details && <PetCard pet={rec.pet_details} />}
                {rec.reasons && rec.reasons.length > 0 && (
                  <div className="mt-2 bg-purple-50 rounded-lg p-3">
                    <p className="text-xs font-medium text-purple-900 mb-1">Why recommended:</p>
                    <ul className="text-xs text-purple-700 space-y-1">
                      {rec.reasons.map((reason: string, idx: number) => (
                        <li key={idx}>• {reason}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      ) : null}
    </div>
  )
}
