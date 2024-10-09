from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client.assignment_portal

def init_db():
    # Initialize collections
    db.users.create_index("username", unique=True)
    db.assignments.create_index("userId")