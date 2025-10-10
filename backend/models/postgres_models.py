from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text, Float
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from db.postgres import Base


class AdoptionStatus(str, enum.Enum):
    AVAILABLE = "available"
    PENDING = "pending"
    ADOPTED = "adopted"
    FOSTERED = "fostered"
    UNAVAILABLE = "unavailable"


class UserRole(str, enum.Enum):
    ADOPTER = "adopter"
    SHELTER_STAFF = "shelter_staff"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    phone = Column(String)
    address = Column(Text)
    city = Column(String)
    state = Column(String)
    zip_code = Column(String)
    role = Column(Enum(UserRole), default=UserRole.ADOPTER)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    adoptions = relationship("Adoption", back_populates="adopter")


class Pet(Base):
    __tablename__ = "pets"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    species = Column(String, nullable=False)  # dog, cat, rabbit, etc.
    breed = Column(String)
    age_years = Column(Integer)
    age_months = Column(Integer)
    gender = Column(String)
    color = Column(String)
    size = Column(String)  # small, medium, large
    weight = Column(Float)
    description = Column(Text)
    status = Column(Enum(AdoptionStatus), default=AdoptionStatus.AVAILABLE)
    intake_date = Column(DateTime, default=datetime.utcnow)
    shelter_id = Column(Integer)  # Reference to shelter
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    adoptions = relationship("Adoption", back_populates="pet")


class Adoption(Base):
    __tablename__ = "adoptions"
    
    id = Column(Integer, primary_key=True, index=True)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)
    adopter_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    application_date = Column(DateTime, default=datetime.utcnow)
    approval_date = Column(DateTime, nullable=True)
    adoption_date = Column(DateTime, nullable=True)
    status = Column(String, default="pending")  # pending, approved, completed, rejected
    notes = Column(Text)
    adoption_fee = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    pet = relationship("Pet", back_populates="adoptions")
    adopter = relationship("User", back_populates="adoptions")


class FollowUp(Base):
    __tablename__ = "follow_ups"
    
    id = Column(Integer, primary_key=True, index=True)
    adoption_id = Column(Integer, ForeignKey("adoptions.id"), nullable=False)
    scheduled_date = Column(DateTime, nullable=False)
    completed_date = Column(DateTime, nullable=True)
    contact_method = Column(String)  # phone, email, visit
    notes = Column(Text)
    status = Column(String, default="scheduled")  # scheduled, completed, cancelled
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
