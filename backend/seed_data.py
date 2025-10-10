"""
Seed script to populate the database with sample data for testing
"""
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
        print("🌱 Seeding database with sample data...")
        
        # Create users
        users = [
            User(
                email="alice@example.com",
                username="alice",
                hashed_password=pwd_context.hash("password123"),
                full_name="Alice Johnson",
                phone="555-0101",
                city="San Francisco",
                state="CA",
                role="adopter"
            ),
            User(
                email="bob@example.com",
                username="bob",
                hashed_password=pwd_context.hash("password123"),
                full_name="Bob Smith",
                phone="555-0102",
                city="Los Angeles",
                state="CA",
                role="adopter"
            ),
            User(
                email="staff@shelter.com",
                username="staff",
                hashed_password=pwd_context.hash("password123"),
                full_name="Shelter Staff",
                role="shelter_staff"
            ),
        ]
        session.add_all(users)
        await session.flush()
        print(f"✅ Created {len(users)} users")
        
        # Create pets
        pets = [
            Pet(
                name="Max",
                species="dog",
                breed="Golden Retriever",
                age_years=3,
                gender="male",
                size="large",
                weight=65,
                color="golden",
                description="Friendly and energetic dog who loves to play fetch. Great with kids and other dogs. Max is house-trained and knows basic commands.",
                status="available"
            ),
            Pet(
                name="Luna",
                species="cat",
                breed="Siamese",
                age_years=2,
                gender="female",
                size="small",
                weight=8,
                color="cream",
                description="Calm and affectionate cat who enjoys quiet environments. Luna is perfect for apartment living and loves to cuddle.",
                status="available"
            ),
            Pet(
                name="Charlie",
                species="dog",
                breed="Beagle",
                age_years=1,
                age_months=6,
                gender="male",
                size="medium",
                weight=25,
                color="tricolor",
                description="Playful puppy with lots of energy. Charlie is still learning but is very food-motivated and eager to please.",
                status="available"
            ),
            Pet(
                name="Bella",
                species="cat",
                breed="Persian",
                age_years=4,
                gender="female",
                size="medium",
                weight=10,
                color="white",
                description="Gentle and loving cat who enjoys being pampered. Bella requires regular grooming but is worth the extra care.",
                status="available"
            ),
            Pet(
                name="Rocky",
                species="dog",
                breed="German Shepherd",
                age_years=5,
                gender="male",
                size="large",
                weight=75,
                color="black and tan",
                description="Loyal and protective dog with training experience. Rocky would do best in a home with a yard and an active owner.",
                status="available"
            ),
            Pet(
                name="Whiskers",
                species="cat",
                breed="Tabby",
                age_years=1,
                gender="male",
                size="small",
                weight=7,
                color="orange",
                description="Curious and playful young cat. Whiskers loves to explore and would enjoy a home with cat trees and toys.",
                status="available"
            ),
            Pet(
                name="Daisy",
                species="dog",
                breed="Labrador Retriever",
                age_years=2,
                gender="female",
                size="large",
                weight=60,
                color="yellow",
                description="Sweet and gentle dog who loves water and swimming. Daisy is great with children and very patient.",
                status="available"
            ),
            Pet(
                name="Mittens",
                species="cat",
                breed="Domestic Shorthair",
                age_years=3,
                gender="female",
                size="small",
                weight=9,
                color="gray",
                description="Independent but affectionate cat. Mittens enjoys her alone time but also loves attention on her terms.",
                status="available"
            ),
        ]
        session.add_all(pets)
        await session.commit()
        print(f"✅ Created {len(pets)} pets")
        
        print("\n🎉 Database seeded successfully!")
        print("\nSample credentials:")
        print("  Email: alice@example.com | Password: password123")
        print("  Email: bob@example.com | Password: password123")
        print("  Email: staff@shelter.com | Password: password123")
        print("\nUser IDs: 1 (Alice), 2 (Bob), 3 (Staff)")


if __name__ == "__main__":
    asyncio.run(seed_data())
