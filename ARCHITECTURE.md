# Architecture Documentation

## Overview

The Pet Adoption Tracker uses a **polyglot persistence** architecture with three specialized databases, each optimized for different data access patterns and use cases.

## Database Architecture

### 1. PostgreSQL - Structured Transactional Data

**Purpose:** Reliable storage for structured adoption records and user accounts

**Schema:**
- `users` - User accounts (adopters, shelter staff, admins)
- `pets` - Core pet information
- `adoptions` - Adoption applications and status
- `follow_ups` - Post-adoption check-ins

**Why PostgreSQL?**
- ACID compliance for critical adoption transactions
- Strong referential integrity with foreign keys
- Excellent for structured queries and reports
- Mature ecosystem with SQLAlchemy ORM

**Example Queries:**
```sql
-- Find all available pets
SELECT * FROM pets WHERE status = 'available';

-- Get adoption history for a user
SELECT a.*, p.name FROM adoptions a 
JOIN pets p ON a.pet_id = p.id 
WHERE a.adopter_id = 123;
```

### 2. MongoDB - Flexible Document Storage

**Purpose:** Dynamic health records and behavior tracking

**Collections:**
- `health_records` - Medical history, vaccinations, treatments
- `behavior_logs` - Behavioral observations and notes

**Why MongoDB?**
- Flexible schema for varying health record types
- Easy to add new fields without migrations
- Excellent for time-series behavior data
- Fast writes for logging systems
- Aggregation pipeline for behavior analytics

**Example Documents:**
```json
{
  "pet_id": 42,
  "record_type": "vaccination",
  "date": "2024-01-15",
  "medications": ["Rabies", "DHPP"],
  "veterinarian": "Dr. Smith",
  "next_appointment": "2025-01-15",
  "notes": "No adverse reactions"
}
```

**Aggregation Example:**
```javascript
// Behavior summary by type
db.behavior_logs.aggregate([
  { $match: { pet_id: 42 } },
  { $group: {
      _id: "$behavior_type",
      count: { $sum: 1 },
      avg_severity: { $avg: "$severity" }
  }}
])
```

### 3. Neo4j - Graph Relationships

**Purpose:** Intelligent recommendations based on relationships

**Graph Model:**
```
(User)-[:INTERESTED_IN]->(Tag)
(Pet)-[:HAS_TAG]->(Tag)
(User)-[:FRIENDS_WITH]-(User)
(User)-[:ADOPTED]->(Pet)
(User)-[:APPLIED_FOR]->(Pet)
```

**Why Neo4j?**
- Natural representation of social connections
- Efficient traversal of relationship networks
- Pattern matching with Cypher queries
- Real-time recommendation engine
- Discovers indirect connections (friends-of-friends)

**Example Cypher Queries:**
```cypher
// Find pets matching user preferences
MATCH (u:User {id: 123})
MATCH (p:Pet)
WHERE NOT (u)-[:ADOPTED|APPLIED_FOR]->(p)
WITH u, p,
  CASE WHEN p.species = u.preferred_species THEN 2.0 ELSE 0.0 END +
  size((p)-[:HAS_TAG]->(:Tag)<-[:INTERESTED_IN]-(u)) * 1.0 +
  size((u)-[:FRIENDS_WITH]->(:User)-[:ADOPTED]->(:Pet)-[:HAS_TAG]->(:Tag)<-[:HAS_TAG]-(p)) * 0.5
  AS score
WHERE score > 0
RETURN p.id, score
ORDER BY score DESC
LIMIT 10

// Find similar pets based on tags
MATCH (p1:Pet {id: 42})-[:HAS_TAG]->(t:Tag)<-[:HAS_TAG]-(p2:Pet)
WHERE p1.id <> p2.id
WITH p2, count(t) AS common_tags
RETURN p2.id, common_tags
ORDER BY common_tags DESC
```

## Data Flow

### Creating a Pet
1. **PostgreSQL:** Insert pet record with core attributes
2. **Neo4j:** Create Pet node and tag relationships
3. **MongoDB:** Ready to receive health records

### Adoption Application
1. **PostgreSQL:** Create adoption record, update pet status
2. **Neo4j:** Create APPLIED_FOR relationship
3. On approval: Update relationship to ADOPTED

### Getting Recommendations
1. **Neo4j:** Run graph traversal algorithm
2. **PostgreSQL:** Fetch detailed pet information
3. Return combined results with scores and reasons

### Health Tracking
1. **MongoDB:** Store flexible health records
2. **PostgreSQL:** Reference pet_id for joins
3. Aggregation for behavior summaries

## API Architecture

### FastAPI Backend
- **Async/await:** Non-blocking database operations
- **Dependency Injection:** Database session management
- **Pydantic:** Request/response validation
- **CORS:** Frontend integration

### Route Organization
```
/api/users          - User management (PostgreSQL)
/api/pets           - Pet CRUD (PostgreSQL + Neo4j)
/api/adoptions      - Adoption workflow (PostgreSQL + Neo4j)
/api/health         - Health records (MongoDB)
/api/recommendations - Graph-based matching (Neo4j + PostgreSQL)
```

## Frontend Architecture

### React + TypeScript
- **React Router:** Client-side routing
- **Axios:** API communication
- **TailwindCSS:** Utility-first styling
- **Lucide Icons:** Modern icon library

### Key Features
- Real-time pet availability
- Interactive recommendation engine
- Health record timeline
- Adoption status tracking

## Scalability Considerations

### PostgreSQL
- Connection pooling with SQLAlchemy
- Indexes on foreign keys and status fields
- Potential read replicas for reporting

### MongoDB
- Indexed on pet_id and date fields
- Sharding by pet_id for horizontal scaling
- TTL indexes for old behavior logs

### Neo4j
- Constraints on unique IDs
- Indexes on frequently queried properties
- APOC procedures for advanced operations

## Security

- Password hashing with bcrypt
- Environment-based configuration
- CORS restrictions
- Input validation with Pydantic
- Prepared statements (SQL injection prevention)

## Monitoring & Observability

Recommended additions:
- Database connection health checks
- Query performance monitoring
- Error tracking (Sentry)
- Metrics collection (Prometheus)
- Logging aggregation (ELK stack)
