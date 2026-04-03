from fastapi import FastAPI, HTTPException
from typing import List
from models import Payment, PaymentCreate, PaymentUpdate
from service import PaymentService

app = FastAPI(title="Payment Service")

service = PaymentService()

@app.get("/api/payments", response_model=List[Payment])
def get_all():
    return service.get_all()

@app.get("/api/payments/{payment_id}", response_model=Payment)
def get_one(payment_id: int):
    payment = service.get_by_id(payment_id)
    if not payment:
        raise HTTPException(404, "Payment not found")
    return payment

@app.post("/api/payments")
def create(payment: PaymentCreate):
    return service.create(payment)

@app.put("/api/payments/{payment_id}")
def update(payment_id: int, payment: PaymentUpdate):
    updated = service.update(payment_id, payment)
    if not updated:
        raise HTTPException(404, "Payment not found")
    return updated

@app.delete("/api/payments/{payment_id}")
def delete(payment_id: int):
    if not service.delete(payment_id):
        raise HTTPException(404, "Payment not found")
    return {"message": "Payment deleted successfully"}