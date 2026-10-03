import time

from fastapi import Request


async def log_requests(
    request: Request,
    call_next,
):
    """
    Registra información básica de cada petición HTTP.
    """

    start = time.perf_counter()

    response = await call_next(request)

    duration = time.perf_counter() - start

    print(
        f"{request.method} "
        f"{request.url.path} "
        f"-> {response.status_code} "
        f"({duration:.4f}s)"
    )

    return response
