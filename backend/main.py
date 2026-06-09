from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import engine, get_db
from backend.models import Base, User, Teacher, Class, Subject, Assignment
from backend.schemas import (
    UserCreate, UserLogin, Token,
    TeacherCreate, ClassCreate, SubjectCreate, AssignmentCreate
)
from backend.auth import (
    hash_password, verify_password, create_access_token,
    get_current_user, get_current_teacher
)


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

@app.get("/profile")
def profile(current_user = Depends(get_current_user)):
    return {
        "message": "Welcome",
        "user": current_user
    }



@app.get("/teacher-dashboard")
def teacher_dashboard(
    current_user = Depends(get_current_teacher)
):
    return {
        "message": "Welcome Teacher",
        "user": current_user
    }


@app.post("/teachers/create-profile")
def create_teacher_profile(
    teacher_data: TeacherCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_teacher)
):
    """Create a teacher profile for the logged in teacher."""
    existing_profile = db.query(Teacher).filter(Teacher.user_id == current_user["user_id"]).first()
    if existing_profile:
        raise HTTPException(status_code=400, detail="Teacher profile already exists")

    new_teacher = Teacher(
        user_id=current_user["user_id"],
        employee_id=teacher_data.employee_id,
        department=teacher_data.department,
        qualification=teacher_data.qualification,
        is_admin=True
    )

    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)

    return {
        "message": "Teacher profile created successfully",
        "teacher": {
            "id": new_teacher.id,
            "user_id": new_teacher.user_id,
            "employee_id": new_teacher.employee_id,
            "department": new_teacher.department,
            "qualification": new_teacher.qualification,
            "is_admin": new_teacher.is_admin
        }
    }


@app.post("/classes/create")
def create_class(
    class_data: ClassCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_teacher)
):
    teacher = db.query(Teacher).filter(
        Teacher.user_id == current_user["user_id"]
    ).first()

    if not teacher:
        raise HTTPException(status_code=400, detail="Create teacher profile first")

    new_class = Class(
        class_name=class_data.class_name,
        section=class_data.section,
        class_teacher_id=teacher.id
    )

    db.add(new_class)
    db.commit()
    db.refresh(new_class)

    return {
        "message": "Class created successfully",
        "class": {
            "id": new_class.id,
            "class_name": new_class.class_name,
            "section": new_class.section,
            "class_teacher_id": new_class.class_teacher_id
        }
    }

@app.post("/subjects/create")
def create_subject(
    subject_data: SubjectCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_teacher)
):
    teacher = db.query(Teacher).filter(
        Teacher.user_id == current_user["user_id"]
    ).first()

    if not teacher:
        raise HTTPException(status_code=400, detail="Create teacher profile first")

    class_obj = db.query(Class).filter(Class.id == subject_data.class_id).first()
    if not class_obj:
        raise HTTPException(status_code=400, detail="Class not found. Create class first.")

    new_subject = Subject(
        subject_name=subject_data.subject_name,
        class_id=subject_data.class_id,
        teacher_id=teacher.id
    )

    db.add(new_subject)
    db.commit()
    db.refresh(new_subject)

    return {
        "message": "Subject created successfully",
        "subject": {
            "id": new_subject.id,
            "subject_name": new_subject.subject_name,
            "class_id": new_subject.class_id,
            "teacher_id": new_subject.teacher_id
        }
    }

@app.post("/assignments/create")
def create_assignment(
    assignment: AssignmentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_teacher)
):
    teacher = db.query(Teacher).filter(
        Teacher.user_id == current_user["user_id"]
    ).first()

    if not teacher:
        raise HTTPException(status_code=400, detail="Create teacher profile first")

    class_obj = db.query(Class).filter(Class.id == assignment.class_id).first()
    if not class_obj:
        raise HTTPException(status_code=400, detail="Class not found. Create class first.")

    subject_obj = db.query(Subject).filter(Subject.id == assignment.subject_id).first()
    if not subject_obj:
        raise HTTPException(status_code=400, detail="Subject not found. Create subject first.")

    new_assignment = Assignment(
        class_id=assignment.class_id,
        subject_id=assignment.subject_id,
        teacher_id=teacher.id,
        title=assignment.title,
        description=assignment.description,
        due_date=assignment.due_date
    )

    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)

    return {
        "message": "Assignment created successfully",
        "assignment": {
            "id": new_assignment.id,
            "class_id": new_assignment.class_id,
            "subject_id": new_assignment.subject_id,
            "teacher_id": new_assignment.teacher_id,
            "title": new_assignment.title,
            "description": new_assignment.description,
            "due_date": new_assignment.due_date
        }
    }

@app.get("/assignments")
def get_assignments(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    assignments = db.query(Assignment).all()

    return {
        "message": "Assignments fetched successfully",
        "assignments": assignments
    }