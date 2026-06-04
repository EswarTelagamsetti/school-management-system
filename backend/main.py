from fastapi import FastAPI 
app=FastAPI()

@app.get("/")
def home():
    return {"message": "School Management System API Running"}


@app.get("/about")
def about():
    return {
        "project": "School Management System",
        "roles": ["Teacher", "Student", "Parent"]
    }