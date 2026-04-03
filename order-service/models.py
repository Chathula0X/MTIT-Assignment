from pydantic import BaseModel
from typing import List, Optional

class OrderItem(BaseModel):
    food_id: int
    quantity: int

class Order(BaseModel):
    id: int
    user_id: int
    items: List[OrderItem]
    total_price: float
    status: str  

class OrderCreate(BaseModel):
    user_id: int
    items: List[OrderItem]
    total_price: float

class OrderUpdate(BaseModel):
    items: Optional[List[OrderItem]] = None
    total_price: Optional[float] = None
    status: Optional[str] = None