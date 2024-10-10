from fastapi import APIRouter, HTTPException, status, Depends
from app.database.schemas import User, Assignment, AdminOut
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.database.database import db
from app import oauth2
from typing import List
from app import utils


# All endpoints here will have a /user prefix
router = APIRouter(
    prefix = "/user",
    tags = ['Users'],
)

# POST /register - Register a new user
# The incoming data should match the schema 'User' in database/schemas.py
@router.post("/register")
async def register_user(user: User):

     # Check if user with this username already exists if so send back 400
    if db.users.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Hash the password before saving
    user.password = utils.hash(user.password)

    # Add user details to database
    db.users.insert_one(user.model_dump())

    return {"message": "User registered successfully"}


# POST /login - User login
@router.post("/login")
async def login_user(user_credentials: OAuth2PasswordRequestForm = Depends()):

    # Check if this user exists in the database
    user = db.users.find_one({"username": user_credentials.username})
    
    # If the user doesn't exist or wrong password is given, return 401 Invalid Credentials
    if not user or \
       not utils.verify(user_credentials.password, user['password']):
        raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials",)
    
    # Else create a JWT token with the user's ID as the payload
    user_id = str(user['_id'])
    access_token = oauth2.create_access_token(data={"user_id": user_id})

    # Return the access token
    return {"access_token": access_token, "token_type": "bearer"}


# POST /upload - Upload an assignment
# Protected route, dependency injection - verifies if the JWT token is valid, then only access is provided
# The incoming data should match the schema 'Assignment' in database/schemas.py
@router.post("/upload")
async def upload_assignment(assignment: Assignment, current_user: int = Depends(oauth2.get_current_user)):

    # Get the current user's ID through the JWT and make a new assignment object with 
    user_id = str(current_user['_id'])
    new_assignment = Assignment(user_id=user_id, **assignment.model_dump())

    # Add to the database
    db.assignments.insert_one(new_assignment.model_dump())

    return {"message": "Assignment uploaded successfully"}


# GET /admins- Fetch all admins
# Protected route, dependency injection - verifies if the JWT token is valid, then only access is provided
@router.get("/admins", response_model=List[AdminOut])
async def get_admins(current_user: int = Depends(oauth2.get_current_user)):

    # Get all the users who have is_admin = True
    admins = db.users.find({"is_admin": True})

    admins_list = []
    for admin in admins:
        # Convert the MongoDB _id to string as its not serialized
        admin['_id'] = str(admin['_id']) 
        
        # Add the data to the list in the schema of AdminOut
        admins_list.append(AdminOut(admin_id=admin['_id'], username=admin['username'])) 

    # Return the list of admins
    return admins_list