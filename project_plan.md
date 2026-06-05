# School Management System

## Project Overview

A role-based School Management System built using FastAPI, MySQL, HTML, CSS, and JavaScript.

The system supports:

* Teacher
* Student
* Parent

with JWT-based authentication and role-based access control.

---

## Roles

### Teacher (Admin)

Teachers act as administrators of the system.

Permissions:

* Login
* Add Students
* Add Parents
* Link Parents to Students
* Create Classes
* Assign Class Teachers
* Create Subjects
* Mark Attendance
* Add Marks
* Upload Assignments
* Post Announcements
* View Student Records

---

### Student

Permissions:

* Login
* View Profile
* View Attendance
* View Marks
* View Assignments
* View Announcements

---

### Parent

Permissions:

* Login
* View Ward Attendance
* View Ward Marks
* View Ward Assignments
* View Ward Announcements

Restrictions:

* Cannot view other students' data
* Can view only linked wards

---

## Technology Stack

### Frontend

* HTML
* CSS
* JavaScript

### Backend

* FastAPI

### Database

* MySQL

### Authentication

* JWT

### Version Control

* Git
* GitHub

---

## Parent-Student Relationship

The system follows a realistic school structure.

* One Parent can have multiple wards.
* One Student can be linked to one or more parents.
* Parents can access only their own ward data.
* Parents cannot access data of other students.

A separate relationship table will be used:

* parent_student

---

## Authentication Architecture

A common users table will be used for authentication.

All users:

* Teacher
* Student
* Parent

will login through the same authentication system.

JWT tokens will be generated after successful login.

---

## Database Design

### users

Stores login information.

Columns:

* id
* name
* email (unique)
* password_hash
* role
* created_at

Roles:

* teacher
* student
* parent

---

### teachers

Stores teacher-specific information.

Columns:

* id
* user_id
* employee_id
* department
* qualification
* is_admin

---

### classes

Stores class information.

Columns:

* id
* class_name
* section
* class_teacher_id

Examples:

* 10-A
* 10-B
* 9-A

---

### students

Stores student-specific information.

Columns:

* id
* user_id
* student_id
* class_id
* date_of_birth

---

### parents

Stores parent-specific information.

Columns:

* id
* user_id
* phone

---

### parent_student

Links parents and students.

Columns:

* id
* parent_id
* student_id

Example:

Parent Rahul

* Student Arjun
* Student Priya

---

### subjects

Stores subjects assigned to classes.

Columns:

* id
* subject_name
* class_id
* teacher_id

Examples:

* Mathematics
* English
* Science

---

### attendance

Stores daily attendance.

Columns:

* id
* student_id
* class_id
* teacher_id
* date
* status

Status:

* Present
* Absent

---

### marks

Stores examination marks.

Columns:

* id
* student_id
* subject_id
* teacher_id
* exam_id
* marks_obtained
* max_marks

Examples:

* Unit Test 1
* Mid Exam
* Final Exam

### exams

Columns:

- id
- exam_name
- class_id
- exam_date

---

### assignments

Stores assignments uploaded by teachers.

Columns:

* id
* class_id
* subject_id
* teacher_id
* title
* description
* due_date

---

### announcements

Stores school announcements.

Columns:

* id
* title
* description
* created_by
* target_role
* class_id

Target Roles:

* teacher
* student
* parent
* all

---

### attendance_sessions

Columns:

- id
- class_id
- teacher_id
- attendance_date

### attendance_records

Columns:

- id
- session_id
- student_id
- status

## Primary Key Strategy

All tables use:

* INT AUTO_INCREMENT

as the primary key.

---

## Future Enhancements

Possible future modules:

* Fee Management
* Online Exams
* Timetable Management
* Leave Management
* Result Generation
* Notification System
* File Uploads
* Report Cards
* Parent-Teacher Meeting Scheduler
