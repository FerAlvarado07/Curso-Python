from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.middleware.logging import log_requests
from src.routers.users import router as users_router

from src.routers.auth import router as auth_router

app = FastAPI(
    title="Curso Python API",
    description=("API de ejemplo desarrollada con FastAPI para el curso de Python."),
    version="1.0.0",
)


# CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Middleware

app.middleware("http")(log_requests)


# Routers

app.include_router(users_router)
app.include_router(auth_router)


@app.get(
    "/",
    tags=["Health"],
    summary="Comprobar API",
)
def root() -> dict:
    """
    Endpoint utilizado para comprobar que la API funciona.
    """

    return {
        "message": "API funcionando",
    }


# Query Parameters


# GET /users?limit=10

# @app.get("/users")
# def get_users(
#     limit: int = 10,
# ) -> dict:
#     return {
#         "limit": limit,
#     }


# GET /users?page=2&limit=20

# @app.get("/users")
# def get_users(
#     page: int = 1,
#     limit: int = 10,
# ) -> dict:
#     return {
#         "page": page,
#         "limit": limit,
#     }
