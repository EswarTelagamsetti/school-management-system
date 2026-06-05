# School Management System

## Roles

### Teacher
- Login
- View Students
- Mark Attendance
- Add Marks
- Post Assignments
- Send Announcements

### Student
- Login
- View Attendance
- View Marks
- View Assignments
- View Announcements

### Parent
- Login
- View Child Attendance
- View Child Marks
- View Assignments
- View Announcements

## Technology

Frontend:
- HTML
- CSS
- JavaScript

Backend:
- FastAPI

Database:
- MySQL

Version Control:
- Git
- GitHub


## Parent-Student Relationship

The system will follow a realistic school model.

- One parent account can be linked to multiple students.
- These linked students are called wards.
- Parents can view only their own wards' attendance, marks, assignments, and related academic details.
- Parents cannot view other students' private information.
- General announcements can be visible to all users.


A separate parent_student relationship table will be used to connect parents and students.


## Database Tables

### users
- id
- name
- email
- password
- role

### students
- id
- user_id
- roll_number
- class_name

### parents
- id
- user_id
- phone

### parent_student
- id
- parent_id
- student_id

### attendance
- id
- student_id
- date
- status

### marks
- id
- student_id
- subject
- marks

### assignments
- id
- title
- description
- due_date

### announcements
- id
- title
- description
- created_at