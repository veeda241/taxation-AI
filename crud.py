from sqlalchemy.orm import Session
from . import db_models, models, auth

def create_user(db: Session, user: models.UserCreate):
    """
    Create a new user after hashing the password.
    """
    # Check if the username or email already exists
    if get_user_by_username(db, user.username):
        raise ValueError(f"Username '{user.username}' is already taken.")
    if get_user_by_email(db, user.email):
        raise ValueError(f"Email '{user.email}' is already registered.")
    
    hashed_password = auth.hash_password(user.password)
    db_user = db_models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    """
    Helper function to get a user by username.
    """
    return db.query(db_models.User).filter(db_models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    """
    Helper function to get a user by email.
    """
    return db.query(db_models.User).filter(db_models.User.email == email).first()

