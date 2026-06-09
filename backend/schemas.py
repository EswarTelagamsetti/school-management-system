from pydantic import BaseModel, EmailStr
from datetime import date


class UserCreate(BaseModel):
    """Schema for creating a new user."""
    name: str
    email: EmailStr
    password: str
    role: str


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str


class Token(BaseModel):
    """Schema for JWT authentication token."""
    access_token: str
    token_type: str


class AssignmentCreate(BaseModel):
    class_id: int
    subject_id: int
    title: str
    description: str
    due_date: date


class SubjectCreate(BaseModel):
    class_id: int
    subject_name: str


class TeacherCreate(BaseModel):
    employee_id: str
    department: str
    qualification: str


class ClassCreate(BaseModel):
    class_name: str
    section: str

