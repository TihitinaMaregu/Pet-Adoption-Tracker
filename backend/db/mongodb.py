from motor.motor_asyncio import AsyncIOMotorClient
import os

mongodb_client = None
database = None


async def init_mongodb():
    global mongodb_client, database
    mongodb_url = f"mongodb://{os.getenv('MONGODB_USER')}:{os.getenv('MONGODB_PASSWORD')}@{os.getenv('MONGODB_HOST')}:{os.getenv('MONGODB_PORT')}"
    mongodb_client = AsyncIOMotorClient(mongodb_url)
    database = mongodb_client[os.getenv('MONGODB_DB')]
    
    # Create indexes
    await database.health_records.create_index("pet_id")
    await database.health_records.create_index("date")
    await database.behavior_logs.create_index("pet_id")
    await database.behavior_logs.create_index("timestamp")


async def close_mongodb():
    global mongodb_client
    if mongodb_client:
        mongodb_client.close()


def get_mongodb():
    return database
