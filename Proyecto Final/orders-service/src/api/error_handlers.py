from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.domain.exceptions.order_exceptions import (
    InvalidOrderError,
    NotificationError,
    OrderNotFoundError,
)


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(InvalidOrderError)
    async def handle_invalid_order(
        request: Request,
        exc: InvalidOrderError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content={"detail": str(exc)},
        )

    @app.exception_handler(OrderNotFoundError)
    async def handle_order_not_found(
        request: Request,
        exc: OrderNotFoundError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=404,
            content={"detail": str(exc)},
        )

    @app.exception_handler(NotificationError)
    async def handle_notification_error(
        request: Request,
        exc: NotificationError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=502,
            content={"detail": str(exc)},
        )
