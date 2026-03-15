# Pet Adoption Tracker

A comprehensive pet adoption management system using a multi-database architecture to handle different aspects of the adoption workflow.

## Features

- 📋 **Adoption Management**: Track pets, adopters, and adoption status
- 🏥 **Health Tracking**: Flexible medical records and behavior logs
- 🤝 **Smart Recommendations**: Graph-based matching using preferences, tags, and social connections
- 📊 **Post-Adoption Follow-up**: Stay connected with families after adoption

## Tech Stack

### Backend
- Python 3.11+
- FastAPI
- SQLAlchemy (PostgreSQL ORM)
- Motor (MongoDB async driver)
- Neo4j Python Driver

### Frontend
- React 18
- TypeScript
- TailwindCSS
- shadcn/ui components
- Lucide React icons

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose (for databases)

### 1. Start Databases

```bash
docker-compose up -d
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start the server
uvicorn main:app --reload
```

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The app will be available at:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Database Configuration

Default credentials are in `.env.example`. Copy to `.env` and update as needed:

```bash
cp .env.example .env
```

## Project Structure

```
├── backend/
│   ├── models/          # Database models
│   ├── routes/          # API endpoints
│   ├── services/        # Business logic
│   ├── db/              # Database connections
│   └── main.py          # FastAPI app
├── frontend/
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── pages/       # Page components
│   │   ├── hooks/       # Custom hooks
│   │   └── lib/         # Utilities
└── docker-compose.yml   # Database services
```

## API Documentation

Once the backend is running, visit http://localhost:8000/docs for interactive API documentation.

## License

MIT
