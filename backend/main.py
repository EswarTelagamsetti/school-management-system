from fastapi import FastAPI
from backend.models import Base
from backend.database import engine

app = FastAPI()

# Create all database tables automatically when the application starts
Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "School Management System API Running"}


@app.get("/about")
def about():
    return {
        "project": "School Management System",
        "roles": ["Teacher", "Student", "Parent"]
    }

