from fastapi import FastAPI
from app.routers import users, admins
from app.database.database import init_db

app = FastAPI()

# Initialize the database
init_db()

# Include routers
app.include_router(users.router)
app.include_router(admins.router)

@app.get("/")
def test():
    return {"Hello": "World"}
