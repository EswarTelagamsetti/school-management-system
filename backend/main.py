from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.models import Base, User
from backend.database import engine, get_db
from backend.schemas import UserCreate, UserLogin, Token
from backend.auth import hash_password, verify_password, create_access_token

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


@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user with hashed password
    new_user = User(
        name=user.name,
        email=user.email,
        password_hash=hash_password(user.password),
        role=user.role
    )
    
    # Save to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {
        "message": "User registered successfully",
        "user_id": new_user.id,
        "email": new_user.email,
        "role": new_user.role
    }


@app.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    """Authenticate a user and return a JWT access token."""
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token_data = {
        "user_id": db_user.id,
        "email": db_user.email,
        "role": db_user.role
    }
    access_token = create_access_token(data=token_data)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

