from fastapi import FastAPI, HTTPException
from typing import List
from models import User, UserCreate, UserUpdate
from service import UserService

app = FastAPI(title="User Service")

service = UserService()

@app.get("/api/users", response_model=List[User])
def get_users():
    return service.get_all()

@app.get("/api/users/{user_id}", response_model=User)
def get_user(user_id: int):
    user = service.get_by_id(user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return user

@app.post("/api/users/register")
def register(user: UserCreate):
    try:
        return service.register(user)
    except Exception as e:
        raise HTTPException(400, str(e))

@app.post("/api/users/login")
def login(email: str, password: str):
    user = service.login(email, password)
    if not user:
        raise HTTPException(401, "Invalid credentials")
    return user

@app.put("/api/users/{user_id}")
def update(user_id: int, user: UserUpdate):
    updated = service.update(user_id, user)
    if not updated:
        raise HTTPException(404, "User not found")
    return updated

@app.delete("/api/users/{user_id}")
def delete(user_id: int):
    if not service.delete(user_id):
        raise HTTPException(404, "User not found")
    return {"message": "Deleted"}