from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from db.postgres import get_db
from db.neo4j_db import get_neo4j
from models.postgres_models import Pet
from models.schemas import PetCreate, PetResponse, PetUpdate, AdoptionStatus

router = APIRouter()


@router.post("/", response_model=PetResponse, status_code=status.HTTP_201_CREATED)
async def create_pet(pet: PetCreate, db: AsyncSession = Depends(get_db)):
    """Create a new pet record"""
    db_pet = Pet(
        name=pet.name,
        species=pet.species,
        breed=pet.breed,
        age_years=pet.age_years,
        age_months=pet.age_months,
        gender=pet.gender,
        color=pet.color,
        size=pet.size,
        weight=pet.weight,
        description=pet.description,
        shelter_id=pet.shelter_id
    )
    db.add(db_pet)
    await db.commit()
    await db.refresh(db_pet)
    
    # Add to Neo4j graph
    driver = get_neo4j()
    async with driver.session() as session:
        await session.run(
            """
            CREATE (p:Pet {
                id: $id,
                name: $name,
                species: $species,
                breed: $breed,
                size: $size,
                age_years: $age_years
            })
            """,
            id=db_pet.id,
            name=db_pet.name,
            species=db_pet.species,
            breed=db_pet.breed,
            size=db_pet.size,
            age_years=db_pet.age_years
        )
        
        # Add tags to Neo4j
        if pet.tags:
            for tag in pet.tags:
                await session.run(
                    """
                    MATCH (p:Pet {id: $pet_id})
                    MERGE (t:Tag {name: $tag})
                    MERGE (p)-[:HAS_TAG]->(t)
                    """,
                    pet_id=db_pet.id,
                    tag=tag.lower()
                )
    
    return db_pet


@router.get("/{pet_id}", response_model=PetResponse)
async def get_pet(pet_id: int, db: AsyncSession = Depends(get_db)):
    """Get pet by ID"""
    result = await db.execute(select(Pet).where(Pet.id == pet_id))
    pet = result.scalar_one_or_none()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pet


@router.get("/", response_model=List[PetResponse])
async def list_pets(
    skip: int = 0,
    limit: int = 100,
    species: str = None,
    status: AdoptionStatus = None,
    db: AsyncSession = Depends(get_db)
):
    """List all pets with optional filters"""
    query = select(Pet)
    
    if species:
        query = query.where(Pet.species == species)
    if status:
        query = query.where(Pet.status == status)
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    pets = result.scalars().all()
    return pets


@router.patch("/{pet_id}", response_model=PetResponse)
async def update_pet(pet_id: int, pet_update: PetUpdate, db: AsyncSession = Depends(get_db)):
    """Update pet information"""
    result = await db.execute(select(Pet).where(Pet.id == pet_id))
    pet = result.scalar_one_or_none()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    
    update_data = pet_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(pet, field, value)
    
    await db.commit()
    await db.refresh(pet)
    return pet


@router.delete("/{pet_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pet(pet_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a pet record"""
    result = await db.execute(select(Pet).where(Pet.id == pet_id))
    pet = result.scalar_one_or_none()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    
    await db.delete(pet)
    await db.commit()
    
    # Remove from Neo4j
    driver = get_neo4j()
    async with driver.session() as session:
        await session.run("MATCH (p:Pet {id: $id}) DETACH DELETE p", id=pet_id)
    
    return None
