from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import Response
import httpx

openapi_tags = [
    {"name": "user", "description": "User proxy endpoints"},
    {"name": "foods", "description": "Food proxy endpoints"},
    {"name": "orders", "description": "Order proxy endpoints"},
    {"name": "payment", "description": "Payment proxy endpoints"},
]

app = FastAPI(
    title="API Gateway",
    openapi_tags=openapi_tags,
    swagger_ui_parameters={
        "operationsSorter": "method",
    },
)

SERVICE_MAP = {
    "users": "http://127.0.0.1:8001",
    "foods": "http://127.0.0.1:8002",
    "orders": "http://127.0.0.1:8003",
    "payments": "http://127.0.0.1:8004",
}

async def forward(request: Request, service_base: str) -> Response:
    target_url = f"{service_base}{request.url.path}"
    if request.url.query:
        target_url += f"?{request.url.query}"

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            upstream = await client.request(
                method=request.method,
                url=target_url,
                content=await request.body(),
                headers={k: v for k, v in request.headers.items() if k.lower() != "host"},
            )
    except httpx.RequestError:
        raise HTTPException(status_code=502, detail="Upstream service unavailable")

    excluded = {"content-encoding", "transfer-encoding", "connection"}
    headers = {k: v for k, v in upstream.headers.items() if k.lower() not in excluded}
    return Response(content=upstream.content, status_code=upstream.status_code, headers=headers)

@app.get("/api/users", tags=["user"])
@app.get("/api/users/{path:path}", tags=["user"], include_in_schema=False)
async def users_get(path: str = "", request: Request = None):
    return await forward(request, SERVICE_MAP["users"])

@app.post("/api/users", tags=["user"])
@app.post("/api/users/{path:path}", tags=["user"], include_in_schema=False)
async def users_post(path: str = "", request: Request = None):
    return await forward(request, SERVICE_MAP["users"])


@app.put("/api/users", tags=["user"])
@app.put("/api/users/{path:path}", tags=["user"], include_in_schema=False)
async def users_put(path: str = "", request: Request = None):
    return await forward(request, SERVICE_MAP["users"])


@app.delete("/api/users", tags=["user"])
@app.delete("/api/users/{path:path}", tags=["user"], include_in_schema=False)
async def users_delete(path: str = "", request: Request = None):
    return await forward(request, SERVICE_MAP["users"])


@app.patch("/api/users", tags=["user"])
@app.patch("/api/users/{path:path}", tags=["user"], include_in_schema=False)
async def users_patch(path: str = "", request: Request = None):
    return await forward(request, SERVICE_MAP["users"])


@app.get("/api/foods", tags=["foods"])
@app.get("/api/foods/{path:path}", tags=["foods"], include_in_schema=False)
async def foods_get(path: str = "", request: Request = None):
    return await forward(request, SERVICE_MAP["foods"])


@app.post("/api/foods", tags=["foods"])
@app.post("/api/foods/{path:path}", tags=["foods"], include_in_schema=False)
async def foods_post(path: str = "", request: Request = None):
    return await forward(request, SERVICE_MAP["foods"])


@app.put("/api/foods", tags=["foods"])
@app.put("/api/foods/{path:path}", tags=["foods"], include_in_schema=False)
async def foods_put(path: str = "", request: Request = None):
    return await forward(request, SERVICE_MAP["foods"])


@app.delete("/api/foods", tags=["foods"])
@app.delete("/api/foods/{path:path}", tags=["foods"], include_in_schema=False)
async def foods_delete(path: str = "", request: Request = None):
    return await forward(request, SERVICE_MAP["foods"])


@app.patch("/api/foods", tags=["foods"])
@app.patch("/api/foods/{path:path}", tags=["foods"], include_in_schema=False)
async def foods_patch(path: str = "", request: Request = None):
    return await forward(request, SERVICE_MAP["foods"])


@app.get("/api/orders", tags=["orders"])
@app.get("/api/orders/{path:path}", tags=["orders"], include_in_schema=False)
async def orders_get(path: str = "", request: Request = None):
    return await forward(request, SERVICE_MAP["orders"])


@app.post("/api/orders", tags=["orders"])
@app.post("/api/orders/{path:path}", tags=["orders"], include_in_schema=False)
async def orders_post(path: str = "", request: Request = None):
    return await forward(request, SERVICE_MAP["orders"])


@app.put("/api/orders", tags=["orders"])
@app.put("/api/orders/{path:path}", tags=["orders"], include_in_schema=False)
async def orders_put(path: str = "", request: Request = None):
    return await forward(request, SERVICE_MAP["orders"])


@app.delete("/api/orders", tags=["orders"])
@app.delete("/api/orders/{path:path}", tags=["orders"], include_in_schema=False)
async def orders_delete(path: str = "", request: Request = None):
    return await forward(request, SERVICE_MAP["orders"])


@app.patch("/api/orders", tags=["orders"])
@app.patch("/api/orders/{path:path}", tags=["orders"], include_in_schema=False)
async def orders_patch(path: str = "", request: Request = None):
    return await forward(request, SERVICE_MAP["orders"])


@app.get("/api/payments", tags=["payment"])
@app.get("/api/payments/{path:path}", tags=["payment"], include_in_schema=False)
async def payments_get(path: str = "", request: Request = None):
    return await forward(request, SERVICE_MAP["payments"])


@app.post("/api/payments", tags=["payment"])
@app.post("/api/payments/{path:path}", tags=["payment"], include_in_schema=False)
async def payments_post(path: str = "", request: Request = None):
    return await forward(request, SERVICE_MAP["payments"])


@app.put("/api/payments", tags=["payment"])
@app.put("/api/payments/{path:path}", tags=["payment"], include_in_schema=False)
async def payments_put(path: str = "", request: Request = None):
    return await forward(request, SERVICE_MAP["payments"])


@app.delete("/api/payments", tags=["payment"])
@app.delete("/api/payments/{path:path}", tags=["payment"], include_in_schema=False)
async def payments_delete(path: str = "", request: Request = None):
    return await forward(request, SERVICE_MAP["payments"])


@app.patch("/api/payments", tags=["payment"])
@app.patch("/api/payments/{path:path}", tags=["payment"], include_in_schema=False)
async def payments_patch(path: str = "", request: Request = None):
    return await forward(request, SERVICE_MAP["payments"])