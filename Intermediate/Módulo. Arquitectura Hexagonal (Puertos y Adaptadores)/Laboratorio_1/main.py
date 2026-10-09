from fastapi import FastAPI

from src.api.routes.orders import router as orders_router

app = FastAPI(
    title="Orders API",
    version="1.0.0",
)

app.include_router(orders_router)


@app.get("/ping")
def ping_pong() -> dict[str, str]:
    return {"response": "pong!"}
