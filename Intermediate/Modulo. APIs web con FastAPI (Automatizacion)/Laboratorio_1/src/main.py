from fastapi import (
    FastAPI,
    HTTPException,
    Request,
    status,
)
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.routers import auth, orders, users

app = FastAPI(
    title="Laboratorio FastAPI",
    version="1.0.0",
)


@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request,
    exc: HTTPException,
):
    error_map = {
        400: "SYS_400",
        401: "AUTH_001",
        403: "AUTH_002",
        404: "SYS_404",
        409: "SYS_409",
        422: "SYS_422",
    }

    error_code = error_map.get(
        exc.status_code,
        "SYS_001",
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "errorCode": error_code,
            "errorMessage": str(exc.detail),
            "userError": get_user_error_message(
                exc.status_code,
            ),
            "info": "http://help.com",
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "errorCode": "SYS_422",
            "errorMessage": "Validation error",
            "userError": "Los datos enviados no son válidos",
            "info": "http://help.com",
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(
    request: Request,
    exc: Exception,
):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "errorCode": "SYS_001",
            "errorMessage": str(exc),
            "userError": (
                "Se presentó un error interno del sistema, intente nuevamente"
            ),
            "info": "http://help.com",
        },
    )


def get_user_error_message(
    status_code: int,
) -> str:
    messages = {
        400: "La solicitud enviada no es válida",
        401: "No está autorizado para realizar esta operación",
        403: "No tiene permisos para realizar esta operación",
        404: "No se encontró el recurso solicitado",
        409: "La información enviada entra en conflicto con datos existentes",
        422: "Los datos enviados no son válidos",
    }

    return messages.get(
        status_code,
        "Se presentó un error al procesar la solicitud",
    )


@app.get("/")
def root():
    return {
        "message": "API funcionando correctamente",
    }


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(orders.router)
