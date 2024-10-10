from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.database.schemas import User
from app.database.database import db
from app import oauth2
from bson import ObjectId
from app import utils


# All endpoints here will have a /admin prefix
router = APIRouter(
    prefix = "/admin",
    tags = ['Admins'],
)

# POST /register - Register a new admin
# The incoming data should match the schema 'User' in database/schemas.py
@router.post("/register")
async def register_admin(user: User):

    # Check if user with this username already exists if so send back 400
    if db.users.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already registered")

    # Set is_admin property to True
    user.is_admin = True

    # Hash the password before saving
    user.password = utils.hash(user.password)

    # Add admin details to database
    db.users.insert_one(user.model_dump())
    return {"message": "Admin registered successfully"}


# POST /login - Admin login
@router.post("/login")
async def login_admin(user_credentials: OAuth2PasswordRequestForm = Depends()):

    # Check if this user exists in the database
    user = db.users.find_one({"username": user_credentials.username})
    
    # If the user doesn't exist or wrong password is given, return 401 Invalid Credentials
    if not user or \
       not utils.verify(user_credentials.password, user['password']):
        raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials",)
    
    # If the user isn't an admin, return 403 Forbidden
    if not user['is_admin']:
        raise HTTPException( status_code=status.HTTP_403_FORBIDDEN, detail="Not an admin",)
    
    # Else create a JWT token with the user's ID as the payload
    user_id = str(user['_id'])
    access_token = oauth2.create_access_token(data={"user_id": user_id})

    # Return the access token
    return {"access_token": access_token, "token_type": "bearer"}


# GET /assignments - View assignments tagged to the admin
# Protected route, dependency injection - verifies if the JWT token is valid, then only access is provided
@router.get("/assignments")
async def get_assignments(current_user: int = Depends(oauth2.get_current_user)):

    # If the user isn't an admin, return 403 Forbidden
    if not current_user['is_admin']:
        raise HTTPException( status_code=status.HTTP_403_FORBIDDEN, detail="Not an admin",)
    
    # Get all the assignments which have the logged in admin's ID
    admin_id = str(current_user['_id'])
    assignments = db.assignments.find({"admin": admin_id})

    # Converting the MongoDB _id to string as its not serialized
    assignments_list = []
    for assignment in assignments:
        assignment['_id'] = str(assignment['_id'])
        assignments_list.append(assignment)

    # Return the list of assignments
    return assignments_list


# POST /assignments/:id/accept - Accept an assignment
# Protected route, dependency injection - verifies if the JWT token is valid, then only access is provided
@router.post("/assignments/{id}/accept")
async def accept_assignment(id: str, current_user: int = Depends(oauth2.get_current_user)):

    # If the user isn't an admin, return 403 Forbidden
    if not current_user['is_admin']:
        raise HTTPException( status_code=status.HTTP_403_FORBIDDEN, detail="Not an admin",)
    
    # Update the assignment to have status: accepted
    result = db.assignments.update_one({"_id": ObjectId(id)}, {"$set": {"status": "accepted"}})

    # If the assignment with given ID doesnt exist, return 404 not found
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    return JSONResponse(content={"message": "Assignment accepted"}, status_code=200)


# POST /assignments/:id/reject - Reject an assignment.
# Protected route, dependency injection - verifies if the JWT token is valid, then only access is provided
@router.post("/assignments/{id}/reject")
async def reject_assignment(id: str, current_user: int = Depends(oauth2.get_current_user)):
    
    # If the user isn't an admin, return 403 Forbidden
    if not current_user['is_admin']:
        raise HTTPException( status_code=status.HTTP_403_FORBIDDEN, detail="Not an admin",)
    
    # Update the assignment to have status: rejected
    result = db.assignments.update_one({"_id": ObjectId(id)}, {"$set": {"status": "rejected"}})

    # If the assignment with given ID doesnt exist, return 404 not found
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    return JSONResponse(content={"message": "Assignment rejected"}, status_code=200)