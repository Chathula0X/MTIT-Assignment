from fastapi import FastAPI, HTTPException, status
from typing import List
from models import Order, OrderCreate, OrderUpdate, OrderUpdateResponse
from service import OrderService

app = FastAPI(title="Order Microservice", version="1.0.0")

order_service = OrderService()

@app.get("/")
def read_root():
    return {"message": "Booking (Order) Microservice is running"}

@app.get("/api/orders", response_model=List[Order])
def get_all_orders():
    """Get all orders"""
    return order_service.get_all()

@app.get("/api/orders/{order_id}", response_model=Order)
def get_order(order_id: int):
    """Get order by ID"""
    order = order_service.get_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.post("/api/orders", response_model=Order, status_code=status.HTTP_201_CREATED)
def create_order(order: OrderCreate):
    """Create new order"""
    return order_service.create(order)

@app.put("/api/orders/{order_id}", response_model=OrderUpdateResponse)
def update_order(order_id: int, order: OrderUpdate):
    """Update order"""
    patch = order.model_dump(exclude_unset=True)
    if not patch:
        raise HTTPException(
            status_code=400, detail="No fields to update (send at least one field)"
        )
    updated_order = order_service.update(order_id, patch)
    if not updated_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Update successful", "order": updated_order}

@app.delete("/api/orders/{order_id}")
def delete_order(order_id: int):
    """Delete order"""
    success = order_service.delete(order_id)
    if not success:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Delete successful"}