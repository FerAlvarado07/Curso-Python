from fastapi import FastAPI

from src.api.routes.orders import router as orders_router

app = FastAPI(
    title="Ejemplo de Arquitectura Hexagonal",
    version="1.0.0",
)

app.include_router(orders_router)
