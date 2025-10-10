# API Examples

Complete examples for testing the Pet Adoption Tracker API.

## Base URL

```
http://localhost:8000
```

## Users API

### Create a User

```bash
curl -X POST http://localhost:8000/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "username": "john_doe",
    "password": "secure_password",
    "full_name": "John Doe",
    "phone": "555-1234",
    "city": "San Francisco",
    "state": "CA",
    "role": "adopter"
  }'
```

### Get User by ID

```bash
curl http://localhost:8000/api/users/1
```

### List All Users

```bash
curl http://localhost:8000/api/users
```

## Pets API

### Create a Pet

```bash
curl -X POST http://localhost:8000/api/pets \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Max",
    "species": "dog",
    "breed": "Golden Retriever",
    "age_years": 3,
    "gender": "male",
    "size": "large",
    "weight": 65,
    "color": "golden",
    "description": "Friendly and energetic dog",
    "tags": ["friendly", "energetic", "good-with-kids", "house-trained"]
  }'
```

### Get Pet by ID

```bash
curl http://localhost:8000/api/pets/1
```

### List Pets with Filters

```bash
# All pets
curl http://localhost:8000/api/pets

# Only dogs
curl http://localhost:8000/api/pets?species=dog

# Only available pets
curl http://localhost:8000/api/pets?status=available

# Available dogs
curl "http://localhost:8000/api/pets?species=dog&status=available"
```

### Update Pet

```bash
curl -X PATCH http://localhost:8000/api/pets/1 \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Updated description - very friendly!",
    "weight": 67
  }'
```

### Delete Pet

```bash
curl -X DELETE http://localhost:8000/api/pets/1
```

## Adoptions API

### Create Adoption Application

```bash
curl -X POST http://localhost:8000/api/adoptions \
  -H "Content-Type: application/json" \
  -d '{
    "pet_id": 1,
    "adopter_id": 1,
    "notes": "I have a large backyard and love active dogs. I work from home so can give lots of attention.",
    "adoption_fee": 150
  }'
```

### Get Adoption by ID

```bash
curl http://localhost:8000/api/adoptions/1
```

### List All Adoptions

```bash
# All adoptions
curl http://localhost:8000/api/adoptions

# Adoptions by specific user
curl http://localhost:8000/api/adoptions?adopter_id=1

# Adoptions for specific pet
curl http://localhost:8000/api/adoptions?pet_id=1
```

### Update Adoption Status

```bash
# Approve adoption
curl -X PATCH http://localhost:8000/api/adoptions/1 \
  -H "Content-Type: application/json" \
  -d '{
    "status": "approved",
    "approval_date": "2024-01-20T10:00:00"
  }'

# Complete adoption
curl -X PATCH http://localhost:8000/api/adoptions/1 \
  -H "Content-Type: application/json" \
  -d '{
    "status": "completed",
    "adoption_date": "2024-01-25T14:00:00"
  }'
```

## Health Records API (MongoDB)

### Create Health Record

```bash
curl -X POST http://localhost:8000/api/health/records \
  -H "Content-Type: application/json" \
  -d '{
    "pet_id": 1,
    "record_type": "vaccination",
    "date": "2024-01-15T10:00:00",
    "veterinarian": "Dr. Sarah Smith",
    "medications": ["Rabies", "DHPP", "Bordetella"],
    "notes": "Annual vaccination completed. No adverse reactions observed.",
    "next_appointment": "2025-01-15T10:00:00"
  }'
```

### Create Surgery Record

```bash
curl -X POST http://localhost:8000/api/health/records \
  -H "Content-Type: application/json" \
  -d '{
    "pet_id": 1,
    "record_type": "surgery",
    "date": "2023-12-10T09:00:00",
    "veterinarian": "Dr. Michael Johnson",
    "diagnosis": "Dental cleaning required",
    "treatment": "Professional dental cleaning and tooth extraction",
    "medications": ["Pain medication", "Antibiotics"],
    "notes": "Recovery went well. Follow-up in 2 weeks."
  }'
```

### Get Health Records for Pet

```bash
curl http://localhost:8000/api/health/records/pet/1
```

### Get Specific Health Record

```bash
curl http://localhost:8000/api/health/records/507f1f77bcf86cd799439011
```

## Behavior Logs API (MongoDB)

### Create Behavior Log

```bash
curl -X POST http://localhost:8000/api/health/behavior \
  -H "Content-Type: application/json" \
  -d '{
    "pet_id": 1,
    "timestamp": "2024-01-20T14:30:00",
    "behavior_type": "friendly",
    "description": "Greeted new visitor with tail wagging and gentle approach",
    "severity": 1,
    "context": "Shelter visit day",
    "observed_by": "Staff Member Jane"
  }'
```

### Create Multiple Behavior Types

```bash
# Playful behavior
curl -X POST http://localhost:8000/api/health/behavior \
  -H "Content-Type: application/json" \
  -d '{
    "pet_id": 1,
    "timestamp": "2024-01-21T10:00:00",
    "behavior_type": "playful",
    "description": "Engaged in play with other dogs in the yard",
    "severity": 1,
    "observed_by": "Volunteer Tom"
  }'

# Anxious behavior
curl -X POST http://localhost:8000/api/health/behavior \
  -H "Content-Type: application/json" \
  -d '{
    "pet_id": 2,
    "timestamp": "2024-01-21T11:00:00",
    "behavior_type": "anxious",
    "description": "Showed signs of stress during thunderstorm",
    "severity": 3,
    "context": "Weather event",
    "observed_by": "Staff Member Sarah"
  }'
```

### Get Behavior Logs for Pet

```bash
curl http://localhost:8000/api/health/behavior/pet/1
```

### Get Behavior Summary

```bash
curl http://localhost:8000/api/health/behavior/summary/1
```

## Recommendations API (Neo4j)

### Add User Tag Preferences

```bash
curl -X POST http://localhost:8000/api/recommendations/user/1/preferences/tags \
  -H "Content-Type: application/json" \
  -d '["friendly", "energetic", "good-with-kids", "house-trained"]'
```

### Add Friend Connection

```bash
curl -X POST http://localhost:8000/api/recommendations/user/1/friends/2
```

### Get Personalized Recommendations

```bash
# Basic recommendations
curl -X POST http://localhost:8000/api/recommendations \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "limit": 10
  }'

# With preferences
curl -X POST http://localhost:8000/api/recommendations \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "preferences": {
      "species": "dog",
      "size": "large"
    },
    "limit": 5
  }'
```

### Get Similar Pets

```bash
curl http://localhost:8000/api/recommendations/similar/1
```

## Complete Workflow Example

### 1. Setup Users and Pets

```bash
# Create adopter
curl -X POST http://localhost:8000/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "email": "adopter@example.com",
    "username": "pet_lover",
    "password": "password123",
    "full_name": "Pet Lover",
    "city": "San Francisco",
    "role": "adopter"
  }'

# Create pet
curl -X POST http://localhost:8000/api/pets \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Buddy",
    "species": "dog",
    "breed": "Labrador",
    "age_years": 2,
    "gender": "male",
    "size": "large",
    "description": "Friendly lab",
    "tags": ["friendly", "active", "good-with-kids"]
  }'
```

### 2. Add Health Records

```bash
curl -X POST http://localhost:8000/api/health/records \
  -H "Content-Type: application/json" \
  -d '{
    "pet_id": 1,
    "record_type": "checkup",
    "date": "2024-01-10T10:00:00",
    "veterinarian": "Dr. Smith",
    "notes": "Healthy and ready for adoption"
  }'
```

### 3. Set User Preferences

```bash
curl -X POST http://localhost:8000/api/recommendations/user/1/preferences/tags \
  -H "Content-Type: application/json" \
  -d '["friendly", "active", "good-with-kids"]'
```

### 4. Get Recommendations

```bash
curl -X POST http://localhost:8000/api/recommendations \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "preferences": {"species": "dog", "size": "large"},
    "limit": 10
  }'
```

### 5. Apply for Adoption

```bash
curl -X POST http://localhost:8000/api/adoptions \
  -H "Content-Type: application/json" \
  -d '{
    "pet_id": 1,
    "adopter_id": 1,
    "notes": "Perfect match for my family!",
    "adoption_fee": 150
  }'
```

### 6. Approve and Complete

```bash
# Approve
curl -X PATCH http://localhost:8000/api/adoptions/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "approved"}'

# Complete
curl -X PATCH http://localhost:8000/api/adoptions/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}'
```

## Testing with Python

```python
import requests

BASE_URL = "http://localhost:8000"

# Create user
response = requests.post(f"{BASE_URL}/api/users", json={
    "email": "test@example.com",
    "username": "testuser",
    "password": "password123",
    "full_name": "Test User",
    "role": "adopter"
})
user = response.json()
print(f"Created user: {user['id']}")

# Get recommendations
response = requests.post(f"{BASE_URL}/api/recommendations", json={
    "user_id": user['id'],
    "preferences": {"species": "dog"},
    "limit": 5
})
recommendations = response.json()
print(f"Found {len(recommendations)} recommendations")
```

## Interactive API Documentation

Visit http://localhost:8000/docs for interactive Swagger UI documentation where you can test all endpoints directly in your browser.
