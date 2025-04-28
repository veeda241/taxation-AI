# models.py - Pydantic Models for Data Validation

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"
    TAX_AUTHORITY = "tax_authority"

class UserBase(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None
    role: UserRole = UserRole.USER
    
class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True

class UserInDB(User):
    hashed_password: str

class RecordType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"
    ASSET = "asset"
    LIABILITY = "liability"

class FinancialRecord(BaseModel):
    id: Optional[str] = None
    user_id: Optional[str] = None
    record_type: RecordType
    amount: float
    description: str
    category: str
    date: datetime
    location: Optional[str] = None
    currency: str = "USD"
    metadata: Optional[dict] = None
    created_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True

class AnomalySeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AnomalyAlert(BaseModel):
    id: Optional[str] = None
    user_id: str
    severity: AnomalySeverity
    description: str
    related_records: List[str] = []  # IDs of related financial records
    detected_at: datetime
    resolved: bool = False
    resolution_notes: Optional[str] = None
    resolved_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True

class AuditLog(BaseModel):
    id: Optional[str] = None
    user_id: str
    action: str
    details: dict
    timestamp: datetime
    ip_address: Optional[str] = None
    
    class Config:
        orm_mode = True