from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.database import schemas
from fastapi import Depends, status, HTTPException
from app.database.database import db
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os
from bson.objectid import ObjectId


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

load_dotenv()

# Get the necessary data for the creation of JWT from the .env file
SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES'))


# Function to create the access token
def create_access_token(data: dict):
    to_encode = data.copy()

    # Set the time after which the token will expire
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # Encode and return back the JWT
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


# Function to verify the access token
def verify_access_token(token: str, credentials_exception):
    try:
        # Decode and get the payload data
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")

        # If there's no user ID in the payload: invalid return 401 unauthorized
        if not id:
            raise credentials_exception
        
        token_data = schemas.TokenData(id=str(id))
    
    # If any error: cannot be decoded - invalid return 401 unauthorized
    except JWTError:
        raise credentials_exception
    
    return token_data
    

# Function which is called as a dependency injection to check if the token is valid
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)

    user = db.users.find_one({"_id": ObjectId(token.id)})

    return user