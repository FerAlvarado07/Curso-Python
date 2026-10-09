from dotenv import load_dotenv

from fastapi import FastAPI

from src.api.error_handlers import register_error_handlers
from src.api.routes.orders import order_router, orders_router
from src.api.schemas.order_schema import PingResponse
from src.api.routes.auth import auth_router

load_dotenv()

app = FastAPI(
    title="Orders Service",
    description="API de órdenes implementada con arquitectura hexagonal.",
    version="1.0.0",
)

register_error_handlers(app)
app.include_router(order_router)
app.include_router(orders_router)
app.include_router(auth_router)


@app.get(
    "/ping",
    response_model=PingResponse,
    tags=["Ping"],
)
def ping_check() -> PingResponse:
    return PingResponse(status="pong")
