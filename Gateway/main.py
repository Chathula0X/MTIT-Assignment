from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import httpx

# ── Pydantic schemas (mirrors each microservice) ─────────────────────────────

class UserOut(BaseModel):
    id: int
    name: str
    email: str
    password: str

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


class FoodOut(BaseModel):
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


class OrderItem(BaseModel):
    food_id: int
    quantity: int

class OrderOut(BaseModel):
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


class PaymentOut(BaseModel):
    id: int
    order_id: int
    amount: float
    status: str

class PaymentCreate(BaseModel):
    order_id: int
    amount: float

class PaymentUpdate(BaseModel):
    status: Optional[str] = None


# ── App setup ─────────────────────────────────────────────────────────────────

openapi_tags = [
    {"name": "users",    "description": "User management"},
    {"name": "foods",    "description": "Food catalogue"},
    {"name": "orders",   "description": "Order management"},
    {"name": "payments", "description": "Payment management"},
]

app = FastAPI(
    title="API Gateway",
    version="1.0.0",
    openapi_tags=openapi_tags,
    swagger_ui_parameters={"operationsSorter": "method"},
)

SERVICE = {
    "users":    "http://127.0.0.1:8001",
    "foods":    "http://127.0.0.1:8002",
    "orders":   "http://127.0.0.1:8003",
    "payments": "http://127.0.0.1:8004",
}

TIMEOUT = 10.0


async def _get(url: str) -> dict | list:
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        try:
            r = await client.get(url)
        except httpx.RequestError:
            raise HTTPException(502, "Upstream service unavailable")
    if r.status_code >= 400:
        raise HTTPException(r.status_code, r.json().get("detail", r.text))
    return r.json()


async def _post(url: str, body: dict) -> dict:
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        try:
            r = await client.post(url, json=body)
        except httpx.RequestError:
            raise HTTPException(502, "Upstream service unavailable")
    if r.status_code >= 400:
        raise HTTPException(r.status_code, r.json().get("detail", r.text))
    return r.json()


async def _put(url: str, body: dict) -> dict:
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        try:
            r = await client.put(url, json=body)
        except httpx.RequestError:
            raise HTTPException(502, "Upstream service unavailable")
    if r.status_code >= 400:
        raise HTTPException(r.status_code, r.json().get("detail", r.text))
    return r.json()


async def _delete(url: str) -> dict:
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        try:
            r = await client.delete(url)
        except httpx.RequestError:
            raise HTTPException(502, "Upstream service unavailable")
    if r.status_code >= 400:
        raise HTTPException(r.status_code, r.json().get("detail", r.text))
    return r.json()


async def _patch(url: str, body: dict) -> dict:
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        try:
            r = await client.patch(url, json=body)
        except httpx.RequestError:
            raise HTTPException(502, "Upstream service unavailable")
    if r.status_code >= 400:
        raise HTTPException(r.status_code, r.json().get("detail", r.text))
    return r.json()


# ── USER endpoints ────────────────────────────────────────────────────────────

@app.get("/api/users", response_model=List[UserOut], tags=["users"])
async def get_users():
    """Get all users."""
    data = await _get(f"{SERVICE['users']}/api/users")
    return JSONResponse(data)


@app.get("/api/users/{user_id}", response_model=UserOut, tags=["users"])
async def get_user(user_id: int):
    """Get a single user by ID."""
    data = await _get(f"{SERVICE['users']}/api/users/{user_id}")
    return JSONResponse(data)


@app.post("/api/users/register", response_model=UserOut, tags=["users"], status_code=201)
async def register_user(user: UserCreate):
    """Register a new user."""
    data = await _post(f"{SERVICE['users']}/api/users/register", user.model_dump())
    return JSONResponse(data, status_code=201)


@app.post("/api/users/login", tags=["users"])
async def login_user(
    email: str = Query(..., description="User email"),
    password: str = Query(..., description="User password"),
):
    """Login with email and password."""
    data = await _get(
        f"{SERVICE['users']}/api/users/login?email={email}&password={password}"
    )
    return JSONResponse(data)


@app.put("/api/users/{user_id}", response_model=UserOut, tags=["users"])
async def update_user(user_id: int, user: UserUpdate):
    """Update user details."""
    data = await _put(
        f"{SERVICE['users']}/api/users/{user_id}",
        user.model_dump(exclude_none=True),
    )
    return JSONResponse(data)


@app.delete("/api/users/{user_id}", tags=["users"])
async def delete_user(user_id: int):
    """Delete a user."""
    data = await _delete(f"{SERVICE['users']}/api/users/{user_id}")
    return JSONResponse(data)


# ── FOOD endpoints ────────────────────────────────────────────────────────────

@app.get("/api/foods", response_model=List[FoodOut], tags=["foods"])
async def get_foods():
    """Get all food items."""
    data = await _get(f"{SERVICE['foods']}/api/foods")
    return JSONResponse(data)


@app.get("/api/foods/{food_id}", response_model=FoodOut, tags=["foods"])
async def get_food(food_id: int):
    """Get a single food item by ID."""
    data = await _get(f"{SERVICE['foods']}/api/foods/{food_id}")
    return JSONResponse(data)


@app.post("/api/foods", response_model=FoodOut, tags=["foods"], status_code=201)
async def create_food(food: FoodCreate):
    """Create a new food item."""
    data = await _post(f"{SERVICE['foods']}/api/foods", food.model_dump())
    return JSONResponse(data, status_code=201)


@app.put("/api/foods/{food_id}", response_model=FoodOut, tags=["foods"])
async def update_food(food_id: int, food: FoodUpdate):
    """Update a food item."""
    data = await _put(
        f"{SERVICE['foods']}/api/foods/{food_id}",
        food.model_dump(exclude_none=True),
    )
    return JSONResponse(data)


@app.delete("/api/foods/{food_id}", tags=["foods"])
async def delete_food(food_id: int):
    """Delete a food item."""
    data = await _delete(f"{SERVICE['foods']}/api/foods/{food_id}")
    return JSONResponse(data)


# ── ORDER endpoints ───────────────────────────────────────────────────────────

@app.get("/api/orders", response_model=List[OrderOut], tags=["orders"])
async def get_orders():
    """Get all orders."""
    data = await _get(f"{SERVICE['orders']}/api/orders")
    return JSONResponse(data)


@app.get("/api/orders/{order_id}", response_model=OrderOut, tags=["orders"])
async def get_order(order_id: int):
    """Get a single order by ID."""
    data = await _get(f"{SERVICE['orders']}/api/orders/{order_id}")
    return JSONResponse(data)


@app.post("/api/orders", response_model=OrderOut, tags=["orders"], status_code=201)
async def create_order(order: OrderCreate):
    """Create a new order."""
    data = await _post(f"{SERVICE['orders']}/api/orders", order.model_dump())
    return JSONResponse(data, status_code=201)


@app.put("/api/orders/{order_id}", response_model=OrderOut, tags=["orders"])
async def update_order(order_id: int, order: OrderUpdate):
    """Update an order."""
    data = await _put(
        f"{SERVICE['orders']}/api/orders/{order_id}",
        order.model_dump(exclude_none=True),
    )
    return JSONResponse(data)


@app.delete("/api/orders/{order_id}", tags=["orders"])
async def delete_order(order_id: int):
    """Delete an order."""
    data = await _delete(f"{SERVICE['orders']}/api/orders/{order_id}")
    return JSONResponse(data)


# ── PAYMENT endpoints ─────────────────────────────────────────────────────────

@app.get("/api/payments", response_model=List[PaymentOut], tags=["payments"])
async def get_payments():
    """Get all payments."""
    data = await _get(f"{SERVICE['payments']}/api/payments")
    return JSONResponse(data)


@app.get("/api/payments/{payment_id}", response_model=PaymentOut, tags=["payments"])
async def get_payment(payment_id: int):
    """Get a single payment by ID."""
    data = await _get(f"{SERVICE['payments']}/api/payments/{payment_id}")
    return JSONResponse(data)


@app.post("/api/payments", response_model=PaymentOut, tags=["payments"], status_code=201)
async def create_payment(payment: PaymentCreate):
    """Create a new payment."""
    data = await _post(f"{SERVICE['payments']}/api/payments", payment.model_dump())
    return JSONResponse(data, status_code=201)


@app.put("/api/payments/{payment_id}", response_model=PaymentOut, tags=["payments"])
async def update_payment(payment_id: int, payment: PaymentUpdate):
    """Update payment status."""
    data = await _put(
        f"{SERVICE['payments']}/api/payments/{payment_id}",
        payment.model_dump(exclude_none=True),
    )
    return JSONResponse(data)


@app.delete("/api/payments/{payment_id}", tags=["payments"])
async def delete_payment(payment_id: int):
    """Delete a payment."""
    data = await _delete(f"{SERVICE['payments']}/api/payments/{payment_id}")
    return JSONResponse(data)