from fastapi import FastAPI, HTTPException
from typing import List
from models import Food, FoodCreate, FoodUpdate
from service import FoodService

app = FastAPI(title="Food Service")

service = FoodService()

@app.get("/api/foods", response_model=List[Food])
def get_foods():
    return service.get_all()

@app.get("/api/foods/{food_id}", response_model=Food)
def get_food(food_id: int):
    food = service.get_by_id(food_id)
    if not food:
        raise HTTPException(404, "Food not found")
    return food

@app.post("/api/foods")
def create(food: FoodCreate):
    return service.create(food)

@app.put("/api/foods/{food_id}")
def update(food_id: int, food: FoodUpdate):
    updated = service.update(food_id, food)
    if not updated:
        raise HTTPException(404, "Food not found")
    return updated

@app.delete("/api/foods/{food_id}")
def delete(food_id: int):
    if not service.delete(food_id):
        raise HTTPException(404, "Food not found")
    return {"message": "Deleted"}