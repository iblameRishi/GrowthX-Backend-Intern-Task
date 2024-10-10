from passlib.context import CryptContext

# Initialise Hash manager with bcrypt scheme
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to hash the password
def hash(password: str):
    return pwd_context.hash(password)

# Function to verify given password with stored hashed passwrod
def verify(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)