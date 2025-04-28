from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from typing import List, Optional
from datetime import datetime, timedelta
import os
import jwt
from passlib.context import CryptContext
from models import UserCreate, User, FinancialRecord, AnomalyAlert, UserInDB
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(title="RobinHood AI Backend", 
              description="API for transparent and fair taxation monitoring")

# Setup CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect to MongoDB
try:
    client = MongoClient(os.getenv("MONGODB_URL", "mongodb://localhost:27017/"))
    db = client[os.getenv("MONGODB_DB", "robinhood")]
    logger.info("Connected to MongoDB")
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {e}")
    raise

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-for-development-only")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Helper functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(username: str):
    user = db.users.find_one({"username": username})
    if user:
        return UserInDB(**user)
    return None

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    user = get_user(username)
    if user is None:
        raise credentials_exception
    return user

# Routes
@app.post("/token", response_model=dict)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=User)
async def create_user(user: UserCreate):
    db_user = get_user(user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = get_password_hash(user.password)
    user_dict = user.dict(exclude={"password"})
    user_dict["hashed_password"] = hashed_password
    user_dict["created_at"] = datetime.utcnow()
    
    db.users.insert_one(user_dict)
    return User(**user_dict)

@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@app.post("/financial-records/", response_model=FinancialRecord)
async def create_financial_record(
    record: FinancialRecord, 
    current_user: User = Depends(get_current_user)
):
    record_dict = record.dict()
    record_dict["user_id"] = str(current_user.id)
    record_dict["created_at"] = datetime.utcnow()
    
    result = db.financial_records.insert_one(record_dict)
    record_dict["id"] = str(result.inserted_id)
    
    # Trigger anomaly detection (placeholder)
    # In a real system, you might want to do this asynchronously
    detect_anomalies(current_user.id)
    
    return FinancialRecord(**record_dict)

@app.get("/financial-records/", response_model=List[FinancialRecord])
async def read_financial_records(current_user: User = Depends(get_current_user)):
    records = db.financial_records.find({"user_id": str(current_user.id)})
    return [FinancialRecord(**record) for record in records]

@app.get("/anomalies/", response_model=List[AnomalyAlert])
async def read_anomalies(current_user: User = Depends(get_current_user)):
    alerts = db.anomaly_alerts.find({"user_id": str(current_user.id)})
    return [AnomalyAlert(**alert) for alert in alerts]

# Placeholder for anomaly detection
def detect_anomalies(user_id: str):
    # In a real implementation, this would connect to your AI model
    # For now, it's just a placeholder function
    logger.info(f"Anomaly detection triggered for user {user_id}")
    # You would query the financial records, run them through the model,
    # and store any detected anomalies in the database
    return

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)