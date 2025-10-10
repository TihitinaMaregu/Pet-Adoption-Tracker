from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from datetime import datetime
from bson import ObjectId

from db.mongodb import get_mongodb
from models.schemas import HealthRecordCreate, HealthRecordResponse, BehaviorLogCreate, BehaviorLogResponse

router = APIRouter()


@router.post("/records", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_health_record(record: HealthRecordCreate):
    """Create a new health record in MongoDB"""
    db = get_mongodb()
    
    record_dict = record.model_dump()
    record_dict["created_at"] = datetime.utcnow()
    
    result = await db.health_records.insert_one(record_dict)
    record_dict["_id"] = str(result.inserted_id)
    
    return {"id": str(result.inserted_id), "message": "Health record created successfully"}


@router.get("/records/pet/{pet_id}", response_model=List[dict])
async def get_pet_health_records(pet_id: int):
    """Get all health records for a specific pet"""
    db = get_mongodb()
    
    cursor = db.health_records.find({"pet_id": pet_id}).sort("date", -1)
    records = await cursor.to_list(length=100)
    
    # Convert ObjectId to string
    for record in records:
        record["_id"] = str(record["_id"])
    
    return records


@router.get("/records/{record_id}", response_model=dict)
async def get_health_record(record_id: str):
    """Get a specific health record"""
    db = get_mongodb()
    
    try:
        record = await db.health_records.find_one({"_id": ObjectId(record_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid record ID")
    
    if not record:
        raise HTTPException(status_code=404, detail="Health record not found")
    
    record["_id"] = str(record["_id"])
    return record


@router.post("/behavior", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_behavior_log(log: BehaviorLogCreate):
    """Create a new behavior log in MongoDB"""
    db = get_mongodb()
    
    log_dict = log.model_dump()
    
    result = await db.behavior_logs.insert_one(log_dict)
    log_dict["_id"] = str(result.inserted_id)
    
    return {"id": str(result.inserted_id), "message": "Behavior log created successfully"}


@router.get("/behavior/pet/{pet_id}", response_model=List[dict])
async def get_pet_behavior_logs(pet_id: int, limit: int = 50):
    """Get behavior logs for a specific pet"""
    db = get_mongodb()
    
    cursor = db.behavior_logs.find({"pet_id": pet_id}).sort("timestamp", -1).limit(limit)
    logs = await cursor.to_list(length=limit)
    
    # Convert ObjectId to string
    for log in logs:
        log["_id"] = str(log["_id"])
    
    return logs


@router.get("/behavior/summary/{pet_id}", response_model=dict)
async def get_behavior_summary(pet_id: int):
    """Get behavior summary statistics for a pet"""
    db = get_mongodb()
    
    pipeline = [
        {"$match": {"pet_id": pet_id}},
        {"$group": {
            "_id": "$behavior_type",
            "count": {"$sum": 1},
            "avg_severity": {"$avg": "$severity"}
        }}
    ]
    
    cursor = db.behavior_logs.aggregate(pipeline)
    summary = await cursor.to_list(length=100)
    
    return {
        "pet_id": pet_id,
        "behavior_summary": summary
    }
