import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { ArrowLeft, Calendar, Heart, Activity, FileText } from 'lucide-react'
import { getPet, getHealthRecords, getBehaviorLogs, getSimilarPets } from '@/lib/api'
import { formatDate, getStatusColor } from '@/lib/utils'

export default function PetDetailPage() {
  const { id } = useParams<{ id: string }>()
  const [pet, setPet] = useState<any>(null)
  const [healthRecords, setHealthRecords] = useState<any[]>([])
  const [behaviorLogs, setBehaviorLogs] = useState<any[]>([])
  const [similarPets, setSimilarPets] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('details')

  useEffect(() => {
    const fetchPetData = async () => {
      if (!id) return
      
      try {
        setLoading(true)
        const [petRes, healthRes, behaviorRes, similarRes] = await Promise.all([
          getPet(parseInt(id)),
          getHealthRecords(parseInt(id)).catch(() => ({ data: [] })),
          getBehaviorLogs(parseInt(id)).catch(() => ({ data: [] })),
          getSimilarPets(parseInt(id)).catch(() => ({ data: [] })),
        ])
        
        setPet(petRes.data)
        setHealthRecords(healthRes.data)
        setBehaviorLogs(behaviorRes.data)
        setSimilarPets(similarRes.data)
      } catch (error) {
        console.error('Error fetching pet data:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchPetData()
  }, [id])

  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    )
  }

  if (!pet) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-600">Pet not found</p>
      </div>
    )
  }

  const age = pet.age_years 
    ? `${pet.age_years} year${pet.age_years > 1 ? 's' : ''}${pet.age_months ? ` ${pet.age_months} months` : ''}`
    : pet.age_months 
    ? `${pet.age_months} month${pet.age_months > 1 ? 's' : ''}`
    : 'Age unknown'

  return (
    <div>
      <Link to="/pets" className="inline-flex items-center text-primary hover:text-primary/80 mb-6">
        <ArrowLeft className="h-4 w-4 mr-2" />
        Back to Pets
      </Link>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Info */}
        <div className="lg:col-span-2">
          <div className="bg-white rounded-lg shadow-md overflow-hidden">
            <div className="h-64 bg-gradient-to-br from-blue-100 to-purple-100 flex items-center justify-center">
              <span className="text-9xl">
                {pet.species === 'dog' ? '🐕' : pet.species === 'cat' ? '🐈' : '🐾'}
              </span>
            </div>
            <div className="p-6">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h1 className="text-3xl font-bold text-gray-900 mb-2">{pet.name}</h1>
                  <p className="text-xl text-gray-600">
                    {pet.breed || pet.species} • {age} • {pet.gender || 'Unknown'}
                  </p>
                </div>
                <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(pet.status)}`}>
                  {pet.status}
                </span>
              </div>

              {pet.description && (
                <div className="mb-6">
                  <h2 className="text-lg font-semibold text-gray-900 mb-2">About {pet.name}</h2>
                  <p className="text-gray-600">{pet.description}</p>
                </div>
              )}

              <div className="grid grid-cols-2 gap-4 mb-6">
                {pet.size && (
                  <div>
                    <p className="text-sm text-gray-500">Size</p>
                    <p className="font-medium capitalize">{pet.size}</p>
                  </div>
                )}
                {pet.weight && (
                  <div>
                    <p className="text-sm text-gray-500">Weight</p>
                    <p className="font-medium">{pet.weight} lbs</p>
                  </div>
                )}
                {pet.color && (
                  <div>
                    <p className="text-sm text-gray-500">Color</p>
                    <p className="font-medium capitalize">{pet.color}</p>
                  </div>
                )}
                <div>
                  <p className="text-sm text-gray-500">Intake Date</p>
                  <p className="font-medium">{formatDate(pet.intake_date)}</p>
                </div>
              </div>

              {pet.status === 'available' && (
                <button className="w-full bg-primary text-white py-3 rounded-lg font-semibold hover:bg-primary/90 transition-colors flex items-center justify-center">
                  <Heart className="h-5 w-5 mr-2" />
                  Apply for Adoption
                </button>
              )}
            </div>
          </div>

          {/* Tabs */}
          <div className="mt-6 bg-white rounded-lg shadow-md">
            <div className="border-b border-gray-200">
              <nav className="flex -mb-px">
                <button
                  onClick={() => setActiveTab('health')}
                  className={`px-6 py-3 border-b-2 font-medium text-sm ${
                    activeTab === 'health'
                      ? 'border-primary text-primary'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <Activity className="h-4 w-4 inline mr-2" />
                  Health Records
                </button>
                <button
                  onClick={() => setActiveTab('behavior')}
                  className={`px-6 py-3 border-b-2 font-medium text-sm ${
                    activeTab === 'behavior'
                      ? 'border-primary text-primary'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <FileText className="h-4 w-4 inline mr-2" />
                  Behavior Logs
                </button>
              </nav>
            </div>

            <div className="p-6">
              {activeTab === 'health' && (
                <div>
                  {healthRecords.length === 0 ? (
                    <p className="text-gray-500 text-center py-8">No health records yet</p>
                  ) : (
                    <div className="space-y-4">
                      {healthRecords.map((record: any) => (
                        <div key={record._id} className="border-l-4 border-blue-500 pl-4 py-2">
                          <div className="flex justify-between items-start mb-1">
                            <h3 className="font-semibold capitalize">{record.record_type}</h3>
                            <span className="text-sm text-gray-500">{formatDate(record.date)}</span>
                          </div>
                          {record.diagnosis && <p className="text-sm text-gray-600">Diagnosis: {record.diagnosis}</p>}
                          {record.treatment && <p className="text-sm text-gray-600">Treatment: {record.treatment}</p>}
                          {record.notes && <p className="text-sm text-gray-500 mt-1">{record.notes}</p>}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}

              {activeTab === 'behavior' && (
                <div>
                  {behaviorLogs.length === 0 ? (
                    <p className="text-gray-500 text-center py-8">No behavior logs yet</p>
                  ) : (
                    <div className="space-y-4">
                      {behaviorLogs.map((log: any) => (
                        <div key={log._id} className="border-l-4 border-green-500 pl-4 py-2">
                          <div className="flex justify-between items-start mb-1">
                            <h3 className="font-semibold capitalize">{log.behavior_type}</h3>
                            <span className="text-sm text-gray-500">
                              {new Date(log.timestamp).toLocaleString()}
                            </span>
                          </div>
                          <p className="text-sm text-gray-600">{log.description}</p>
                          {log.severity && (
                            <p className="text-sm text-gray-500 mt-1">Severity: {log.severity}/5</p>
                          )}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Sidebar */}
        <div className="lg:col-span-1">
          {similarPets.length > 0 && (
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Similar Pets</h2>
              <div className="space-y-4">
                {similarPets.map((similar: any) => (
                  <Link
                    key={similar.pet_id}
                    to={`/pets/${similar.pet_id}`}
                    className="block border rounded-lg p-3 hover:bg-gray-50 transition-colors"
                  >
                    <h3 className="font-medium text-gray-900">{similar.pet_details.name}</h3>
                    <p className="text-sm text-gray-600">
                      {similar.pet_details.breed || similar.pet_details.species}
                    </p>
                    <p className="text-xs text-gray-500 mt-1">
                      {similar.common_tags} common tag{similar.common_tags > 1 ? 's' : ''}
                    </p>
                  </Link>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
