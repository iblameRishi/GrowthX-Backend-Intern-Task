from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.database.models import User
from app.database.database import db
from app.auth import authenticate_user
from app import oauth2
from bson import ObjectId

router = APIRouter(
    prefix = "/admin",
    tags = ['Admins'],
)

@router.post("/register")
async def register_admin(user: User):

    user.is_admin = True
    if db.users.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already registered")
    
    db.users.insert_one(user.model_dump())
    return {"message": "Admin registered successfully"}


@router.post("/login")
async def login_admin(user_credentials: OAuth2PasswordRequestForm = Depends()):

    user = db.users.find_one({"username": user_credentials.username})
    if not user or user['password'] != user_credentials.password:
        raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials",)
    
    if not user['is_admin']:
        raise HTTPException( status_code=status.HTTP_403_FORBIDDEN, detail="Not an admin",)
    
    user_id = str(user['_id'])
    access_token = oauth2.create_access_token(data={"user_id": user_id})

    return {"access_token": access_token, "token_type": "bearer"}



@router.get("/assignments")
async def get_assignments(current_user: int = Depends(oauth2.get_current_user)):

    if not current_user['is_admin']:
        raise HTTPException( status_code=status.HTTP_403_FORBIDDEN, detail="Not an admin",)
    
    admin_id = str(current_user['_id'])
    assignments = db.assignments.find({"admin": admin_id})

    assignments_list = []
    for assignment in assignments:
        assignment['_id'] = str(assignment['_id'])
        assignments_list.append(assignment)

    return assignments_list



@router.post("/assignments/{id}/accept")
async def accept_assignment(id: str, current_user: int = Depends(oauth2.get_current_user)):

    if not current_user['is_admin']:
        raise HTTPException( status_code=status.HTTP_403_FORBIDDEN, detail="Not an admin",)
    
    result = db.assignments.update_one({"_id": ObjectId(id)}, {"$set": {"status": "accepted"}})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    return JSONResponse(content={"message": "Assignment accepted"}, status_code=200)


@router.post("/assignments/{id}/reject")
async def reject_assignment(id: str, current_user: int = Depends(oauth2.get_current_user)):
    
    if not current_user['is_admin']:
        raise HTTPException( status_code=status.HTTP_403_FORBIDDEN, detail="Not an admin",)
    
    result = db.assignments.update_one({"_id": ObjectId(id)}, {"$set": {"status": "rejected"}})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    return JSONResponse(content={"message": "Assignment rejected"}, status_code=200)