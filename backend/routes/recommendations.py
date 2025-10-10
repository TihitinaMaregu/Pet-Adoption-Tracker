from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from db.postgres import get_db
from db.neo4j_db import get_neo4j
from models.postgres_models import Pet, User
from models.schemas import RecommendationRequest, RecommendationResponse, PetResponse

router = APIRouter()


@router.post("/", response_model=List[RecommendationResponse])
async def get_recommendations(
    request: RecommendationRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Get personalized pet recommendations using Neo4j graph relationships.
    
    Recommendation algorithm considers:
    - User preferences (species, size, age)
    - Tags and characteristics
    - Social connections (friends who adopted similar pets)
    - Previous interactions
    """
    driver = get_neo4j()
    
    # First, ensure user exists in Neo4j
    async with driver.session() as session:
        await session.run(
            """
            MERGE (u:User {id: $user_id})
            ON CREATE SET u.created_at = datetime()
            """,
            user_id=request.user_id
        )
        
        # Add user preferences to graph
        if request.preferences:
            if "species" in request.preferences:
                await session.run(
                    """
                    MATCH (u:User {id: $user_id})
                    SET u.preferred_species = $species
                    """,
                    user_id=request.user_id,
                    species=request.preferences["species"]
                )
            if "size" in request.preferences:
                await session.run(
                    """
                    MATCH (u:User {id: $user_id})
                    SET u.preferred_size = $size
                    """,
                    user_id=request.user_id,
                    size=request.preferences["size"]
                )
        
        # Run recommendation query
        result = await session.run(
            """
            MATCH (u:User {id: $user_id})
            MATCH (p:Pet)
            WHERE NOT (u)-[:ADOPTED|APPLIED_FOR]->(p)
            
            // Calculate score based on multiple factors
            WITH u, p,
                // Preference matching
                CASE 
                    WHEN u.preferred_species IS NOT NULL AND p.species = u.preferred_species THEN 2.0
                    ELSE 0.0
                END +
                CASE 
                    WHEN u.preferred_size IS NOT NULL AND p.size = u.preferred_size THEN 1.5
                    ELSE 0.0
                END +
                // Tag similarity
                size((p)-[:HAS_TAG]->(:Tag)<-[:INTERESTED_IN]-(u)) * 1.0 +
                // Social recommendations (friends who adopted similar pets)
                size((u)-[:FRIENDS_WITH]->(:User)-[:ADOPTED]->(:Pet)-[:HAS_TAG]->(:Tag)<-[:HAS_TAG]-(p)) * 0.5
                AS score
            
            WHERE score > 0
            
            RETURN p.id AS pet_id, score
            ORDER BY score DESC
            LIMIT $limit
            """,
            user_id=request.user_id,
            limit=request.limit
        )
        
        recommendations = []
        async for record in result:
            pet_id = record["pet_id"]
            score = record["score"]
            
            # Get reasons for recommendation
            reasons = []
            if request.preferences.get("species"):
                reasons.append(f"Matches your preferred species")
            if request.preferences.get("size"):
                reasons.append(f"Matches your preferred size")
            
            # Fetch pet details from PostgreSQL
            pet_result = await db.execute(select(Pet).where(Pet.id == pet_id))
            pet = pet_result.scalar_one_or_none()
            
            if pet and pet.status == "available":
                recommendations.append(
                    RecommendationResponse(
                        pet_id=pet_id,
                        score=score,
                        reasons=reasons if reasons else ["Based on your profile"],
                        pet_details=PetResponse.model_validate(pet)
                    )
                )
        
        return recommendations


@router.post("/user/{user_id}/preferences/tags")
async def add_user_tag_preference(user_id: int, tags: List[str]):
    """Add tag preferences for a user in Neo4j"""
    driver = get_neo4j()
    
    async with driver.session() as session:
        # Ensure user exists
        await session.run(
            """
            MERGE (u:User {id: $user_id})
            """,
            user_id=user_id
        )
        
        # Add tag preferences
        for tag in tags:
            await session.run(
                """
                MATCH (u:User {id: $user_id})
                MERGE (t:Tag {name: $tag})
                MERGE (u)-[:INTERESTED_IN]->(t)
                """,
                user_id=user_id,
                tag=tag.lower()
            )
    
    return {"message": f"Added {len(tags)} tag preferences for user {user_id}"}


@router.post("/user/{user_id}/friends/{friend_id}")
async def add_friend_connection(user_id: int, friend_id: int):
    """Create a friendship connection in Neo4j for social recommendations"""
    driver = get_neo4j()
    
    async with driver.session() as session:
        await session.run(
            """
            MERGE (u1:User {id: $user_id})
            MERGE (u2:User {id: $friend_id})
            MERGE (u1)-[:FRIENDS_WITH]-(u2)
            """,
            user_id=user_id,
            friend_id=friend_id
        )
    
    return {"message": f"Friend connection created between user {user_id} and {friend_id}"}


@router.get("/similar/{pet_id}", response_model=List[dict])
async def get_similar_pets(pet_id: int, limit: int = 5, db: AsyncSession = Depends(get_db)):
    """Find similar pets based on tags and characteristics"""
    driver = get_neo4j()
    
    async with driver.session() as session:
        result = await session.run(
            """
            MATCH (p1:Pet {id: $pet_id})-[:HAS_TAG]->(t:Tag)<-[:HAS_TAG]-(p2:Pet)
            WHERE p1.id <> p2.id
            WITH p2, count(t) AS common_tags
            RETURN p2.id AS pet_id, common_tags
            ORDER BY common_tags DESC
            LIMIT $limit
            """,
            pet_id=pet_id,
            limit=limit
        )
        
        similar_pets = []
        async for record in result:
            similar_pet_id = record["pet_id"]
            common_tags = record["common_tags"]
            
            # Fetch pet details
            pet_result = await db.execute(select(Pet).where(Pet.id == similar_pet_id))
            pet = pet_result.scalar_one_or_none()
            
            if pet:
                similar_pets.append({
                    "pet_id": similar_pet_id,
                    "common_tags": common_tags,
                    "pet_details": PetResponse.model_validate(pet)
                })
        
        return similar_pets
