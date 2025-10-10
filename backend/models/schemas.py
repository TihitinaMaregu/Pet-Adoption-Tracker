from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum


# Enums
class AdoptionStatus(str, Enum):
    AVAILABLE = "available"
    PENDING = "pending"
    ADOPTED = "adopted"
    FOSTERED = "fostered"
    UNAVAILABLE = "unavailable"


class UserRole(str, Enum):
    ADOPTER = "adopter"
    SHELTER_STAFF = "shelter_staff"
    ADMIN = "admin"


# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    role: UserRole = UserRole.ADOPTER


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Pet Schemas
class PetBase(BaseModel):
    name: str
    species: str
    breed: Optional[str] = None
    age_years: Optional[int] = None
    age_months: Optional[int] = None
    gender: Optional[str] = None
    color: Optional[str] = None
    size: Optional[str] = None
    weight: Optional[float] = None
    description: Optional[str] = None
    shelter_id: Optional[int] = None


class PetCreate(PetBase):
    tags: Optional[List[str]] = []


class PetUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[AdoptionStatus] = None
    description: Optional[str] = None
    weight: Optional[float] = None


class PetResponse(PetBase):
    id: int
    status: AdoptionStatus
    intake_date: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True


# Adoption Schemas
class AdoptionBase(BaseModel):
    pet_id: int
    adopter_id: int
    notes: Optional[str] = None
    adoption_fee: Optional[float] = None


class AdoptionCreate(AdoptionBase):
    pass


class AdoptionUpdate(BaseModel):
    status: Optional[str] = None
    notes: Optional[str] = None
    approval_date: Optional[datetime] = None
    adoption_date: Optional[datetime] = None


class AdoptionResponse(AdoptionBase):
    id: int
    application_date: datetime
    approval_date: Optional[datetime] = None
    adoption_date: Optional[datetime] = None
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# Health Record Schemas (MongoDB)
class HealthRecordBase(BaseModel):
    pet_id: int
    record_type: str  # vaccination, checkup, surgery, medication, etc.
    date: datetime
    veterinarian: Optional[str] = None
    diagnosis: Optional[str] = None
    treatment: Optional[str] = None
    medications: Optional[List[str]] = []
    notes: Optional[str] = None
    next_appointment: Optional[datetime] = None


class HealthRecordCreate(HealthRecordBase):
    pass


class HealthRecordResponse(HealthRecordBase):
    id: str = Field(alias="_id")
    created_at: datetime
    
    class Config:
        populate_by_name = True


# Behavior Log Schemas (MongoDB)
class BehaviorLogBase(BaseModel):
    pet_id: int
    timestamp: datetime
    behavior_type: str  # friendly, aggressive, anxious, playful, etc.
    description: str
    severity: Optional[int] = Field(None, ge=1, le=5)  # 1-5 scale
    context: Optional[str] = None
    observed_by: Optional[str] = None


class BehaviorLogCreate(BehaviorLogBase):
    pass


class BehaviorLogResponse(BehaviorLogBase):
    id: str = Field(alias="_id")
    
    class Config:
        populate_by_name = True


# Recommendation Schemas
class RecommendationRequest(BaseModel):
    user_id: int
    preferences: Optional[dict] = {}
    limit: int = 10


class RecommendationResponse(BaseModel):
    pet_id: int
    score: float
    reasons: List[str]
    pet_details: Optional[PetResponse] = None
