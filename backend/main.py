from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from db.postgres import init_postgres, close_postgres
from db.mongodb import init_mongodb, close_mongodb
from db.neo4j_db import init_neo4j, close_neo4j
from routes import pets, users, adoptions, health, recommendations

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_postgres()
    await init_mongodb()
    await init_neo4j()
    yield
    # Shutdown
    await close_postgres()
    await close_mongodb()
    await close_neo4j()


app = FastAPI(
    title="Pet Adoption Tracker",
    description="Multi-database pet adoption management system",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Configuration
origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(pets.router, prefix="/api/pets", tags=["Pets"])
app.include_router(adoptions.router, prefix="/api/adoptions", tags=["Adoptions"])
app.include_router(health.router, prefix="/api/health", tags=["Health Records"])
app.include_router(recommendations.router, prefix="/api/recommendations", tags=["Recommendations"])


@app.get("/")
async def root():
    return {
        "message": "Pet Adoption Tracker API",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
