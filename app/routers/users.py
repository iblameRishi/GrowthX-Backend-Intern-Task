from fastapi import APIRouter, HTTPException, status, Depends
from app.database.models import User, Assignment, AdminOut
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.database.database import db
from app import oauth2
from typing import List
# from bson import ObjectId

router = APIRouter(
    prefix = "/user",
    tags = ['Users'],
)

@router.post("/register")
async def register_user(user: User):

    if db.users.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already registered")
    db.users.insert_one(user.model_dump())
    return {"message": "User registered successfully"}


@router.post("/login")
async def login_user(user_credentials: OAuth2PasswordRequestForm = Depends()):

    user = db.users.find_one({"username": user_credentials.username})
    if not user or user['password'] != user_credentials.password:
        raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials",)
    
    user_id = str(user['_id'])
    access_token = oauth2.create_access_token(data={"user_id": user_id})

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/upload")
async def upload_assignment(assignment: Assignment, current_user: int = Depends(oauth2.get_current_user)):

    user_id = str(current_user['_id'])
    new_assignment = Assignment(user_id=user_id, **assignment.model_dump())

    db.assignments.insert_one(new_assignment.model_dump())

    return {"message": "Assignment uploaded successfully"}


@router.get("/admins", response_model=List[AdminOut])
async def get_admins(current_user: int = Depends(oauth2.get_current_user)):

    admins = db.users.find({"is_admin": True})
    admins_list = []

    for admin in admins:
        admin['_id'] = str(admin['_id']) 
        admins_list.append(AdminOut(admin_id=admin['_id'], username=admin['username'])) 

    return admins_list