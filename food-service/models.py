from pydantic import BaseModel
from typing import Optional

class Food(BaseModel):
    id: int
    name: str
    price: float
    description: str

class FoodCreate(BaseModel):
    name: str
    price: float
    description: str

class FoodUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None