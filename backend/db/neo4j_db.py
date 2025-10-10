from neo4j import AsyncGraphDatabase
import os

neo4j_driver = None


async def init_neo4j():
    global neo4j_driver
    uri = os.getenv('NEO4J_URI')
    user = os.getenv('NEO4J_USER')
    password = os.getenv('NEO4J_PASSWORD')
    neo4j_driver = AsyncGraphDatabase.driver(uri, auth=(user, password))
    
    # Verify connectivity
    await neo4j_driver.verify_connectivity()
    
    # Create constraints and indexes
    async with neo4j_driver.session() as session:
        # Constraints
        await session.run("CREATE CONSTRAINT pet_id IF NOT EXISTS FOR (p:Pet) REQUIRE p.id IS UNIQUE")
        await session.run("CREATE CONSTRAINT user_id IF NOT EXISTS FOR (u:User) REQUIRE u.id IS UNIQUE")
        await session.run("CREATE CONSTRAINT tag_name IF NOT EXISTS FOR (t:Tag) REQUIRE t.name IS UNIQUE")
        
        # Indexes
        await session.run("CREATE INDEX pet_species IF NOT EXISTS FOR (p:Pet) ON (p.species)")
        await session.run("CREATE INDEX user_location IF NOT EXISTS FOR (u:User) ON (u.location)")


async def close_neo4j():
    global neo4j_driver
    if neo4j_driver:
        await neo4j_driver.close()


def get_neo4j():
    return neo4j_driver
