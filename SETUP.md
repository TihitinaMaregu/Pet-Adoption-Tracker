# Setup Guide

## Prerequisites

- **Python 3.11+**
- **Node.js 18+**
- **Docker & Docker Compose** (for databases)
- **Git**

## Quick Start

### 1. Clone and Setup Environment

```bash
cd Pet-Adoption-Tracker
cp .env.example .env
```

Edit `.env` if you want to change default credentials.

### 2. Start Databases

```bash
docker-compose up -d
```

This starts:
- PostgreSQL on port 5432
- MongoDB on port 27017
- Neo4j on ports 7474 (HTTP) and 7687 (Bolt)

Verify all containers are running:
```bash
docker-compose ps
```

### 3. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Start the backend server:
```bash
uvicorn main:app --reload
```

The API will be available at http://localhost:8000

### 4. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at http://localhost:5173

## Database Access

### PostgreSQL
```bash
docker exec -it pet_adoption_postgres psql -U postgres -d pet_adoption
```

### MongoDB
```bash
docker exec -it pet_adoption_mongo mongosh -u mongo -p mongo
```

### Neo4j Browser
Open http://localhost:7474 in your browser
- Username: `neo4j`
- Password: `neo4jpassword`

## Sample Data

### Create a User

```bash
curl -X POST http://localhost:8000/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "username": "john_doe",
    "password": "secure_password",
    "full_name": "John Doe",
    "role": "adopter"
  }'
```

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
    "description": "Friendly and energetic dog looking for an active family",
    "tags": ["friendly", "energetic", "good-with-kids"]
  }'
```

### Add Health Record

```bash
curl -X POST http://localhost:8000/api/health/records \
  -H "Content-Type: application/json" \
  -d '{
    "pet_id": 1,
    "record_type": "vaccination",
    "date": "2024-01-15T10:00:00",
    "veterinarian": "Dr. Smith",
    "medications": ["Rabies", "DHPP"],
    "notes": "Annual vaccination completed"
  }'
```

### Create Adoption Application

```bash
curl -X POST http://localhost:8000/api/adoptions \
  -H "Content-Type: application/json" \
  -d '{
    "pet_id": 1,
    "adopter_id": 1,
    "notes": "I have a large backyard and love active dogs",
    "adoption_fee": 150
  }'
```

### Get Recommendations

```bash
curl -X POST http://localhost:8000/api/recommendations \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "preferences": {
      "species": "dog",
      "size": "large"
    },
    "limit": 10
  }'
```

## Testing the System

### 1. Create Test Data Script

Create `backend/seed_data.py`:

```python
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models.postgres_models import User, Pet
from passlib.context import CryptContext
import os
from dotenv import load_dotenv

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def seed_data():
    DATABASE_URL = f"postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
    engine = create_async_engine(DATABASE_URL)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        # Create users
        users = [
            User(email="alice@example.com", username="alice", hashed_password=pwd_context.hash("password"), full_name="Alice Johnson", role="adopter"),
            User(email="bob@example.com", username="bob", hashed_password=pwd_context.hash("password"), full_name="Bob Smith", role="adopter"),
            User(email="staff@shelter.com", username="staff", hashed_password=pwd_context.hash("password"), full_name="Shelter Staff", role="shelter_staff"),
        ]
        session.add_all(users)
        
        # Create pets
        pets = [
            Pet(name="Max", species="dog", breed="Golden Retriever", age_years=3, gender="male", size="large", weight=65, description="Friendly and energetic"),
            Pet(name="Luna", species="cat", breed="Siamese", age_years=2, gender="female", size="small", weight=8, description="Calm and affectionate"),
            Pet(name="Charlie", species="dog", breed="Beagle", age_years=1, age_months=6, gender="male", size="medium", weight=25, description="Playful puppy"),
            Pet(name="Bella", species="cat", breed="Persian", age_years=4, gender="female", size="medium", weight=10, description="Loves to cuddle"),
            Pet(name="Rocky", species="dog", breed="German Shepherd", age_years=5, gender="male", size="large", weight=75, description="Loyal and protective"),
        ]
        session.add_all(pets)
        
        await session.commit()
        print("✅ Seed data created successfully!")

if __name__ == "__main__":
    asyncio.run(seed_data())
```

Run it:
```bash
cd backend
python seed_data.py
```

### 2. Verify Data

- **API Docs:** http://localhost:8000/docs
- **Frontend:** http://localhost:5173
- **Neo4j Browser:** http://localhost:7474

## Troubleshooting

### Database Connection Issues

Check if containers are running:
```bash
docker-compose ps
```

View logs:
```bash
docker-compose logs postgres
docker-compose logs mongodb
docker-compose logs neo4j
```

### Backend Issues

Check Python version:
```bash
python --version  # Should be 3.11+
```

Reinstall dependencies:
```bash
pip install --upgrade -r requirements.txt
```

### Frontend Issues

Clear node modules and reinstall:
```bash
rm -rf node_modules package-lock.json
npm install
```

## Stopping the Application

```bash
# Stop backend (Ctrl+C in terminal)
# Stop frontend (Ctrl+C in terminal)

# Stop databases
docker-compose down

# Stop and remove volumes (WARNING: deletes all data)
docker-compose down -v
```

## Production Deployment

For production deployment, consider:

1. **Environment Variables:** Use secure secrets management
2. **Database:** Use managed database services (AWS RDS, MongoDB Atlas, Neo4j Aura)
3. **Backend:** Deploy with Gunicorn/Uvicorn workers
4. **Frontend:** Build and serve with Nginx
5. **SSL/TLS:** Enable HTTPS
6. **Monitoring:** Add logging and metrics
7. **Backups:** Regular database backups
