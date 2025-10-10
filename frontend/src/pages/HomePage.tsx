import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { Heart, TrendingUp, Users, Database } from 'lucide-react'
import { getPets, getAdoptions } from '@/lib/api'

export default function HomePage() {
  const [stats, setStats] = useState({
    totalPets: 0,
    availablePets: 0,
    adoptions: 0,
  })

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const [petsRes, adoptionsRes] = await Promise.all([
          getPets(),
          getAdoptions(),
        ])
        
        const pets = petsRes.data
        const availablePets = pets.filter((p: any) => p.status === 'available')
        
        setStats({
          totalPets: pets.length,
          availablePets: availablePets.length,
          adoptions: adoptionsRes.data.length,
        })
      } catch (error) {
        console.error('Error fetching stats:', error)
      }
    }

    fetchStats()
  }, [])

  return (
    <div>
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Welcome to Pet Adoption Tracker
        </h1>
        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
          A comprehensive multi-database system helping shelters manage adoptions,
          track pet health, and connect families with their perfect companions.
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm font-medium">Total Pets</p>
              <p className="text-3xl font-bold text-gray-900">{stats.totalPets}</p>
            </div>
            <Heart className="h-12 w-12 text-blue-500" />
          </div>
        </div>
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm font-medium">Available</p>
              <p className="text-3xl font-bold text-green-600">{stats.availablePets}</p>
            </div>
            <TrendingUp className="h-12 w-12 text-green-500" />
          </div>
        </div>
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm font-medium">Adoptions</p>
              <p className="text-3xl font-bold text-purple-600">{stats.adoptions}</p>
            </div>
            <Users className="h-12 w-12 text-purple-500" />
          </div>
        </div>
      </div>

      {/* Architecture Overview */}
      <div className="bg-white rounded-lg shadow-md p-8 mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
          <Database className="h-6 w-6 mr-2 text-primary" />
          Multi-Database Architecture
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="border-l-4 border-blue-500 pl-4">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">PostgreSQL</h3>
            <p className="text-gray-600 text-sm">
              Structured adoption records, user accounts, and transactional data
              for reliable record-keeping.
            </p>
          </div>
          <div className="border-l-4 border-green-500 pl-4">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">MongoDB</h3>
            <p className="text-gray-600 text-sm">
              Flexible health records, behavior tracking, and medical history
              with dynamic schemas.
            </p>
          </div>
          <div className="border-l-4 border-purple-500 pl-4">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Neo4j</h3>
            <p className="text-gray-600 text-sm">
              Graph-based relationship modeling for intelligent pet recommendations
              using preferences and social connections.
            </p>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Link
          to="/pets"
          className="bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow"
        >
          <h3 className="text-xl font-bold mb-2">Browse Available Pets</h3>
          <p className="text-blue-100">
            View all pets available for adoption and find your perfect match.
          </p>
        </Link>
        <Link
          to="/recommendations"
          className="bg-gradient-to-r from-purple-500 to-purple-600 text-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow"
        >
          <h3 className="text-xl font-bold mb-2">Get Recommendations</h3>
          <p className="text-purple-100">
            Discover personalized pet recommendations based on your preferences.
          </p>
        </Link>
      </div>
    </div>
  )
}
