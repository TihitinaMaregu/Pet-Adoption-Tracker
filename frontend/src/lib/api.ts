import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Pets
export const getPets = (params?: { species?: string; status?: string }) => 
  api.get('/api/pets', { params })

export const getPet = (id: number) => 
  api.get(`/api/pets/${id}`)

export const createPet = (data: any) => 
  api.post('/api/pets', data)

export const updatePet = (id: number, data: any) => 
  api.patch(`/api/pets/${id}`, data)

export const deletePet = (id: number) => 
  api.delete(`/api/pets/${id}`)

// Users
export const getUsers = () => 
  api.get('/api/users')

export const getUser = (id: number) => 
  api.get(`/api/users/${id}`)

export const createUser = (data: any) => 
  api.post('/api/users', data)

// Adoptions
export const getAdoptions = (params?: { adopter_id?: number; pet_id?: number }) => 
  api.get('/api/adoptions', { params })

export const getAdoption = (id: number) => 
  api.get(`/api/adoptions/${id}`)

export const createAdoption = (data: any) => 
  api.post('/api/adoptions', data)

export const updateAdoption = (id: number, data: any) => 
  api.patch(`/api/adoptions/${id}`, data)

// Health Records
export const getHealthRecords = (petId: number) => 
  api.get(`/api/health/records/pet/${petId}`)

export const createHealthRecord = (data: any) => 
  api.post('/api/health/records', data)

export const getBehaviorLogs = (petId: number) => 
  api.get(`/api/health/behavior/pet/${petId}`)

export const createBehaviorLog = (data: any) => 
  api.post('/api/health/behavior', data)

export const getBehaviorSummary = (petId: number) => 
  api.get(`/api/health/behavior/summary/${petId}`)

// Recommendations
export const getRecommendations = (userId: number, preferences?: any) => 
  api.post('/api/recommendations', { user_id: userId, preferences, limit: 10 })

export const addUserTagPreferences = (userId: number, tags: string[]) => 
  api.post(`/api/recommendations/user/${userId}/preferences/tags`, tags)

export const addFriendConnection = (userId: number, friendId: number) => 
  api.post(`/api/recommendations/user/${userId}/friends/${friendId}`)

export const getSimilarPets = (petId: number) => 
  api.get(`/api/recommendations/similar/${petId}`)
