from fastapi import HTTPException, status
from app.database.database import db

def authenticate_user(username: str, password: str):
    user = db.users.find_one({"username": username})
    if not user or user['password'] != password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    return user