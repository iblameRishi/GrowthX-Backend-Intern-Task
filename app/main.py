from fastapi import FastAPI
from app.routers import users, admins
from app.database.database import init_db

app = FastAPI()

# MongoDB Initialization
init_db()

# Routers for each type of user endpoint - better for readability and maintenance
app.include_router(users.router)
app.include_router(admins.router)

# Test Endpoint
@app.get("/")
def test():
    return {"Hello": "World"}
