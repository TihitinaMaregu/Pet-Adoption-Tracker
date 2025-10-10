import { Link } from 'react-router-dom'
import { Calendar, MapPin } from 'lucide-react'
import { formatDate, getStatusColor } from '@/lib/utils'

interface PetCardProps {
  pet: {
    id: number
    name: string
    species: string
    breed?: string
    age_years?: number
    age_months?: number
    gender?: string
    size?: string
    status: string
    intake_date: string
    description?: string
  }
}

export default function PetCard({ pet }: PetCardProps) {
  const age = pet.age_years 
    ? `${pet.age_years} year${pet.age_years > 1 ? 's' : ''}${pet.age_months ? ` ${pet.age_months} months` : ''}`
    : pet.age_months 
    ? `${pet.age_months} month${pet.age_months > 1 ? 's' : ''}`
    : 'Age unknown'

  return (
    <Link to={`/pets/${pet.id}`}>
      <div className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow overflow-hidden">
        <div className="h-48 bg-gradient-to-br from-blue-100 to-purple-100 flex items-center justify-center">
          <span className="text-6xl">
            {pet.species === 'dog' ? '🐕' : pet.species === 'cat' ? '🐈' : '🐾'}
          </span>
        </div>
        <div className="p-4">
          <div className="flex justify-between items-start mb-2">
            <h3 className="text-xl font-bold text-gray-900">{pet.name}</h3>
            <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(pet.status)}`}>
              {pet.status}
            </span>
          </div>
          <p className="text-gray-600 text-sm mb-2">
            {pet.breed || pet.species} • {age} • {pet.gender || 'Unknown'}
          </p>
          {pet.size && (
            <p className="text-gray-500 text-sm mb-2">
              Size: <span className="font-medium capitalize">{pet.size}</span>
            </p>
          )}
          {pet.description && (
            <p className="text-gray-600 text-sm mb-3 line-clamp-2">
              {pet.description}
            </p>
          )}
          <div className="flex items-center text-gray-500 text-xs">
            <Calendar className="h-3 w-3 mr-1" />
            <span>Intake: {formatDate(pet.intake_date)}</span>
          </div>
        </div>
      </div>
    </Link>
  )
}
