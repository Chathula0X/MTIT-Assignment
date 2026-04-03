from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional


class OrderItemCreate(BaseModel):
    quantity: int
    price: float


class OrderCreate(BaseModel):
    customerId: str
    name: str
    phone: str
    menuId: str
    items: List[OrderItemCreate]
    totalPrice: float


class OrderItemOut(BaseModel):
    """Response items: no per-line ids (stored `_id` ignored)."""

    model_config = ConfigDict(extra="ignore")
    quantity: int
    price: float


class Order(BaseModel):
    """Public API: `order_id` (int) only; mongo `_id`s hidden from items/order."""

    model_config = ConfigDict(populate_by_name=True)
    order_id: int
    id: str = Field(alias="_id", serialization_alias="_id", exclude=True)
    customerId: str
    name: str
    phone: str
    menuId: str
    items: List[OrderItemOut]
    totalPrice: float
    status: str
    createdAt: str
    version: int = Field(0, alias="__v", serialization_alias="__v")


class OrderUpdate(BaseModel):
    customerId: Optional[str] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    menuId: Optional[str] = None
    items: Optional[List[OrderItemCreate]] = None
    totalPrice: Optional[float] = None
    status: Optional[str] = None


class OrderUpdateResponse(BaseModel):
    message: str
    order: Order
