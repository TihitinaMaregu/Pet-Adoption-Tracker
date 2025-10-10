from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from datetime import datetime

from db.postgres import get_db
from db.neo4j_db import get_neo4j
from models.postgres_models import Adoption, Pet, User
from models.schemas import AdoptionCreate, AdoptionResponse, AdoptionUpdate

router = APIRouter()


@router.post("/", response_model=AdoptionResponse, status_code=status.HTTP_201_CREATED)
async def create_adoption(adoption: AdoptionCreate, db: AsyncSession = Depends(get_db)):
    """Create a new adoption application"""
    # Verify pet exists and is available
    result = await db.execute(select(Pet).where(Pet.id == adoption.pet_id))
    pet = result.scalar_one_or_none()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    if pet.status != "available":
        raise HTTPException(status_code=400, detail="Pet is not available for adoption")
    
    # Verify user exists
    result = await db.execute(select(User).where(User.id == adoption.adopter_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Create adoption record
    db_adoption = Adoption(
        pet_id=adoption.pet_id,
        adopter_id=adoption.adopter_id,
        notes=adoption.notes,
        adoption_fee=adoption.adoption_fee
    )
    db.add(db_adoption)
    
    # Update pet status
    pet.status = "pending"
    
    await db.commit()
    await db.refresh(db_adoption)
    
    # Add relationship to Neo4j
    driver = get_neo4j()
    async with driver.session() as session:
        await session.run(
            """
            MATCH (u:User {id: $user_id})
            MATCH (p:Pet {id: $pet_id})
            MERGE (u)-[:APPLIED_FOR {
                adoption_id: $adoption_id,
                date: datetime($date),
                status: $status
            }]->(p)
            """,
            user_id=adoption.adopter_id,
            pet_id=adoption.pet_id,
            adoption_id=db_adoption.id,
            date=db_adoption.application_date.isoformat(),
            status="pending"
        )
    
    return db_adoption


@router.get("/{adoption_id}", response_model=AdoptionResponse)
async def get_adoption(adoption_id: int, db: AsyncSession = Depends(get_db)):
    """Get adoption by ID"""
    result = await db.execute(select(Adoption).where(Adoption.id == adoption_id))
    adoption = result.scalar_one_or_none()
    if not adoption:
        raise HTTPException(status_code=404, detail="Adoption not found")
    return adoption


@router.get("/", response_model=List[AdoptionResponse])
async def list_adoptions(
    skip: int = 0,
    limit: int = 100,
    adopter_id: int = None,
    pet_id: int = None,
    db: AsyncSession = Depends(get_db)
):
    """List all adoptions with optional filters"""
    query = select(Adoption)
    
    if adopter_id:
        query = query.where(Adoption.adopter_id == adopter_id)
    if pet_id:
        query = query.where(Adoption.pet_id == pet_id)
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    adoptions = result.scalars().all()
    return adoptions


@router.patch("/{adoption_id}", response_model=AdoptionResponse)
async def update_adoption(
    adoption_id: int,
    adoption_update: AdoptionUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update adoption status"""
    result = await db.execute(select(Adoption).where(Adoption.id == adoption_id))
    adoption = result.scalar_one_or_none()
    if not adoption:
        raise HTTPException(status_code=404, detail="Adoption not found")
    
    update_data = adoption_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(adoption, field, value)
    
    # Update pet status if adoption is completed
    if adoption_update.status == "completed":
        result = await db.execute(select(Pet).where(Pet.id == adoption.pet_id))
        pet = result.scalar_one_or_none()
        if pet:
            pet.status = "adopted"
        
        # Update Neo4j relationship
        driver = get_neo4j()
        async with driver.session() as session:
            await session.run(
                """
                MATCH (u:User {id: $user_id})-[r:APPLIED_FOR]->(p:Pet {id: $pet_id})
                WHERE r.adoption_id = $adoption_id
                DELETE r
                CREATE (u)-[:ADOPTED {
                    adoption_id: $adoption_id,
                    date: datetime($date)
                }]->(p)
                """,
                user_id=adoption.adopter_id,
                pet_id=adoption.pet_id,
                adoption_id=adoption.id,
                date=datetime.utcnow().isoformat()
            )
    
    await db.commit()
    await db.refresh(adoption)
    return adoption
