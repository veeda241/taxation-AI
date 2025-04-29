from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from . import crud, models, database

router = APIRouter()

@router.post("/register", response_model=models.UserOut)
def register_user(user: models.UserCreate, db: Session = Depends(database.get_db)):
    return crud.create_user(db=db, user=user)
