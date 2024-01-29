from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import SessionLocal, engine, Base
from schemas.user import UserCreate, UserUpdate

from model.user import User
import bcrypt

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def hash_password(password: str):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

@router.post("/users/", response_model=UserCreate)  
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter((User.username == user.username) | (User.email == user.email)).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username or Email already registered")
    
    hashed_password = hash_password(user.password)

    new_user = User(
        username=user.username, 
        email=user.email, 
        hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/users/")  
async def read_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@router.patch("/users/{user_id}", response_model=UserUpdate)
async def update_user(user_id: str, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_user.username = user.username
    db_user.email = user.email
    db.commit()
    db.refresh(db_user)

    return db_user

@router.delete('/users/{user_id}')
async def delete_user(user_id: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return {"message": "User successfully deleted", "user_id": user_id}