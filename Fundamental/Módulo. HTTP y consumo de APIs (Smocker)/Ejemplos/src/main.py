# Módulo. HTTP y consumo de APIs (Smocker)

import asyncio
import logging
import time

import aiohttp
import httpx
import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


# 1. HTTP básico


def http_conceptos() -> None:
    """
    HTTP permite la comunicación entre un cliente y un servidor.

    Una petición HTTP normalmente contiene:

        Método
        URL
        Headers
        Body

    Una respuesta HTTP contiene:

        Status Code
        Headers
        Body

    Métodos HTTP comunes:

        GET     → Obtener información
        POST    → Crear información
        PUT     → Reemplazar información
        PATCH   → Modificar información
        DELETE  → Eliminar información

    Códigos HTTP comunes:

        2xx → Éxito
        3xx → Redirección
        4xx → Error del cliente
        5xx → Error del servidor
    """

    logger.info("HTTP permite la comunicación entre clientes y servidores")


def get_user(user_id: int) -> dict:
    response = requests.get(
        f"https://jsonplaceholder.typicode.com/users/{user_id}",
        timeout=5,
    )

    response.raise_for_status()

    return response.json()


# 2. requests - GET


def requests_get() -> None:
    """
    requests es una librería sencilla y ampliamente utilizada
    para consumir APIs HTTP de forma síncrona.
    """

    response = requests.get(
        "https://jsonplaceholder.typicode.com/users",
        timeout=5,
    )

    print("Status:", response.status_code)
    print("Contenido:")
    print(response.json())


# 3. requests - parámetros


def requests_params() -> None:
    """
    Los parámetros se pueden enviar utilizando params.
    """

    response = requests.get(
        "https://jsonplaceholder.typicode.com/users",
        params={
            "id": 1,
        },
        timeout=5,
    )

    print("URL:", response.url)
    print("Respuesta:", response.json())


# 4. requests - headers


def requests_headers() -> None:
    """
    Los headers permiten enviar información adicional.

    Algunos ejemplos:

        Accept
        Content-Type
        Authorization
    """

    response = requests.get(
        "https://jsonplaceholder.typicode.com/users",
        headers={
            "Accept": "application/json",
        },
        timeout=5,
    )

    print(response.status_code)


# 5. requests - POST


def requests_post() -> None:
    user = {
        "name": "Fernando",
        "email": "fernando@example.com",
    }

    try:
        response = requests.post(
            "https://jsonplaceholder.typicode.com/users",
            json=user,
            timeout=5,
        )

        response.raise_for_status()

        print("Usuario creado correctamente")
        print("Status:", response.status_code)

        if response.content:
            print("Respuesta:", response.json())

    except requests.HTTPError as error:
        logger.error(
            "Error HTTP: %s",
            error,
        )

    except requests.Timeout:
        logger.error(
            "La petición tardó demasiado",
        )

    except requests.RequestException as error:
        logger.error(
            "Error de conexión: %s",
            error,
        )


# 6. requests - manejo de errores


def requests_error_handling() -> None:
    """
    raise_for_status() genera una excepción cuando la respuesta
    representa un error HTTP.
    """

    try:
        response = requests.get(
            "https://jsonplaceholder.typicode.com/users/999999",
            timeout=5,
        )

        response.raise_for_status()

        print(response.json())

    except requests.HTTPError as error:
        logger.error("Error HTTP: %s", error)

    except requests.Timeout:
        logger.error("La petición tardó demasiado")

    except requests.RequestException as error:
        logger.error("Error de conexión: %s", error)


# 7. Timeouts


def requests_timeout() -> None:
    """
    Siempre debemos establecer un timeout.

    Sin timeout, una aplicación podría quedarse esperando
    indefinidamente una respuesta.

    También podemos separar:

        timeout de conexión
        timeout de lectura
    """

    try:
        response = requests.get(
            "https://jsonplaceholder.typicode.com/users",
            timeout=(
                3,
                10,
            ),
        )

        print(response.status_code)

    except requests.Timeout:
        logger.error("Se agotó el tiempo de espera")


# 8. httpx - petición síncrona


def httpx_get() -> None:
    """
    httpx es una alternativa moderna a requests.

    Soporta:

        HTTP/1.1
        HTTP/2
        API síncrona
        API asíncrona
    """

    response = httpx.get(
        "https://jsonplaceholder.typicode.com/users",
        timeout=5,
    )

    print("Status:", response.status_code)
    print("Respuesta:", response.json())


# 9. httpx - Client


def httpx_client() -> None:
    """
    Cuando realizamos múltiples peticiones podemos reutilizar
    un mismo cliente.

    Esto permite reutilizar conexiones.
    """

    with httpx.Client(
        timeout=5,
    ) as client:
        response_users = client.get(
            "https://jsonplaceholder.typicode.com/users",
        )

        response_posts = client.get(
            "https://jsonplaceholder.typicode.com/posts",
        )

        print("Usuarios:", response_users.status_code)
        print("Posts:", response_posts.status_code)


# 10. httpx - headers


def httpx_headers() -> None:
    """
    Los headers también pueden configurarse en el cliente.
    """

    with httpx.Client(
        headers={
            "Accept": "application/json",
        },
        timeout=5,
    ) as client:
        response = client.get(
            "https://jsonplaceholder.typicode.com/users",
        )

        print(response.json())


# 11. httpx - POST


def httpx_post() -> None:
    """
    Enviar información utilizando JSON.
    """

    user = {
        "name": "Fernando",
        "email": "fernando@example.com",
    }

    try:
        with httpx.Client(
            timeout=5,
        ) as client:
            response = client.post(
                "https://jsonplaceholder.typicode.com/users",
                json=user,
            )

            print("Status:", response.status_code)

            response.raise_for_status()

            if response.content:
                print("Respuesta:", response.json())

    except httpx.HTTPStatusError as error:
        logger.error(
            "Error HTTP: %s",
            error,
        )

    except httpx.TimeoutException:
        logger.error(
            "La petición tardó demasiado",
        )

    except httpx.RequestError as error:
        logger.error(
            "Error de conexión: %s",
            error,
        )


# 12. httpx - HTTP/2


def httpx_http2() -> None:
    """
    httpx permite utilizar HTTP/2.

    Es necesario instalar:

        poetry add "httpx[http2]"

    HTTP/2 permite características como:

        Multiplexación
        Compresión de headers
        Uso más eficiente de conexiones
    """

    with httpx.Client(
        http2=True,
        timeout=5,
    ) as client:
        response = client.get(
            "https://httpbin.org/get",
        )

        print("HTTP version:", response.http_version)
        print("Status:", response.status_code)


# 13. httpx - manejo de errores


def httpx_error_handling() -> None:
    """
    httpx proporciona excepciones específicas para distintos
    problemas durante una petición.
    """

    try:
        response = httpx.get(
            "https://jsonplaceholder.typicode.com/users/999999",
            timeout=5,
        )

        response.raise_for_status()

        print(response.json())

    except httpx.HTTPStatusError as error:
        logger.error(
            "Error HTTP: %s",
            error,
        )

    except httpx.TimeoutException:
        logger.error(
            "Timeout en la petición",
        )

    except httpx.RequestError as error:
        logger.error(
            "Error de conexión: %s",
            error,
        )


# 14. Reintentos


def retry_example(
    url: str,
    retries: int = 3,
) -> dict:
    """
    Realiza varios intentos cuando ocurre un error temporal.

    Utilizamos exponential backoff:

        Intento 1 → 1 segundo
        Intento 2 → 2 segundos
        Intento 3 → 4 segundos

    No todos los errores deberían reintentarse.

    Normalmente podemos considerar:

        500
        502
        503
        504
        429
    """

    for attempt in range(1, retries + 1):
        try:
            logger.info(
                "Intento %d de %d",
                attempt,
                retries,
            )

            response = httpx.get(
                url,
                timeout=5,
            )

            response.raise_for_status()

            return response.json()

        except (
            httpx.TimeoutException,
            httpx.HTTPStatusError,
        ) as error:
            logger.warning(
                "Error en intento %d: %s",
                attempt,
                error,
            )

            if attempt == retries:
                raise

            wait_time = 2 ** (attempt - 1)

            logger.info(
                "Esperando %d segundos antes de reintentar",
                wait_time,
            )

            time.sleep(wait_time)

    raise RuntimeError("No se pudo obtener la información")


# 15. aiohttp - petición asíncrona


async def aiohttp_get() -> None:
    """
    aiohttp permite realizar peticiones HTTP utilizando asyncio.

    Es útil cuando necesitamos realizar múltiples operaciones
    de I/O concurrentemente.
    """

    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://jsonplaceholder.typicode.com/users",
        ) as response:
            response.raise_for_status()

            data = await response.json()

            print(data)


# 16. aiohttp - timeout


async def aiohttp_timeout() -> None:
    """
    Podemos configurar un timeout para el ClientSession.
    """

    timeout = aiohttp.ClientTimeout(
        total=10,
        connect=5,
        sock_read=5,
    )

    async with aiohttp.ClientSession(
        timeout=timeout,
    ) as session:
        async with session.get(
            "https://jsonplaceholder.typicode.com/users",
        ) as response:
            response.raise_for_status()

            data = await response.json()

            print(data)


# 17. aiohttp - múltiples peticiones concurrentes


async def aiohttp_multiple_requests() -> None:
    """
    asyncio.gather permite ejecutar varias peticiones
    concurrentemente.

    Ejemplo:

        API A → 2 segundos
        API B → 3 segundos
        API C → 2 segundos

    Secuencial:

        2 + 3 + 2 = 7 segundos

    Concurrente:

        aproximadamente 3 segundos
    """

    urls = [
        "https://jsonplaceholder.typicode.com/users",
        "https://jsonplaceholder.typicode.com/posts",
        "https://jsonplaceholder.typicode.com/comments",
    ]

    async def get_data(
        session: aiohttp.ClientSession,
        url: str,
    ) -> dict | list:
        async with session.get(url) as response:
            response.raise_for_status()

            return await response.json()

    async with aiohttp.ClientSession() as session:
        results = await asyncio.gather(
            *(get_data(session, url) for url in urls),
        )

    for result in results:
        print(type(result))
        print(len(result))


# 18. Streaming con httpx


def httpx_streaming() -> None:
    """
    Streaming permite procesar una respuesta por partes.

    Esto es especialmente importante cuando descargamos
    archivos grandes.

    En lugar de cargar todo:

        response.content

    podemos procesar pequeños bloques:

        response.iter_bytes()
    """

    url = "https://httpbin.org/bytes/1024"

    with httpx.stream(
        "GET",
        url,
        timeout=10,
    ) as response:
        response.raise_for_status()

        total_bytes = 0

        for chunk in response.iter_bytes():
            total_bytes += len(chunk)

            logger.info(
                "Recibidos %d bytes",
                len(chunk),
            )

        print(
            "Total recibido:",
            total_bytes,
        )


# 19. Streaming para guardar archivos


def download_file(
    url: str,
    output_file: str,
) -> None:
    """
    Descarga un archivo utilizando streaming.

    Esto evita cargar todo el archivo en memoria.
    """

    with httpx.stream(
        "GET",
        url,
        timeout=30,
    ) as response:
        response.raise_for_status()

        with open(
            output_file,
            "wb",
        ) as file:
            for chunk in response.iter_bytes(
                chunk_size=8192,
            ):
                file.write(chunk)

    logger.info(
        "Archivo descargado: %s",
        output_file,
    )


# 20. Streaming con aiohttp


async def aiohttp_streaming() -> None:
    """
    aiohttp también permite procesar una respuesta
    por pequeños bloques.
    """

    url = "https://httpbin.org/bytes/1024"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()

            total_bytes = 0

            async for chunk in response.content.iter_chunked(
                8192,
            ):
                total_bytes += len(chunk)

                logger.info(
                    "Recibidos %d bytes",
                    len(chunk),
                )

            print(
                "Total recibido:",
                total_bytes,
            )


# 21. Uso eficiente de memoria


def memory_efficient_processing() -> None:
    """
    Una mala práctica para archivos grandes sería:

        response = httpx.get(url)
        data = response.content

    Esto carga todo el contenido en memoria.

    Una alternativa es utilizar streaming:

        with httpx.stream(...) as response:
            for chunk in response.iter_bytes():
                process(chunk)

    De esta forma procesamos pequeños bloques.
    """

    url = "https://httpbin.org/bytes/1024"

    with httpx.stream(
        "GET",
        url,
    ) as response:
        response.raise_for_status()

        for chunk in response.iter_bytes(
            chunk_size=1024,
        ):
            logger.debug(
                "Procesando chunk de %d bytes",
                len(chunk),
            )


# 22. Cliente HTTP reutilizable


class UserClient:
    """
    Cliente HTTP sencillo para consultar usuarios.

    Centralizar las llamadas HTTP permite mantener
    una separación entre la lógica de negocio y
    la comunicación con la API.
    """

    def __init__(
        self,
        base_url: str,
    ) -> None:
        self.client = httpx.Client(
            base_url=base_url,
            timeout=5,
        )

    def get_user(
        self,
        user_id: int,
    ) -> dict:
        response = self.client.get(
            f"/users/{user_id}",
        )

        response.raise_for_status()

        return response.json()

    def close(self) -> None:
        self.client.close()


# 23. Uso del cliente HTTP


def user_client_example() -> None:
    """
    Ejemplo de utilización de UserClient.
    """

    client = UserClient(
        "https://jsonplaceholder.typicode.com",
    )

    try:
        user = client.get_user(1)

        print(user)

    finally:
        client.close()


# 24. Smocker


def smocker_documentation() -> None:
    """
    Smocker permite simular APIs HTTP para pruebas.

    Arquitectura normal:

        Aplicación
             |
             v
        API real


    Durante pruebas:

        Aplicación
             |
             v
          Smocker
             |
             v
        Respuesta simulada


    Podemos simular:

        200 OK
        201 Created
        400 Bad Request
        401 Unauthorized
        403 Forbidden
        404 Not Found
        429 Too Many Requests
        500 Internal Server Error
        503 Service Unavailable
        Timeouts
        Respuestas lentas
    """

    logger.info(
        "Smocker permite simular servicios HTTP para pruebas",
    )


# 25. Logging


def logging_examples() -> None:
    """
    Los niveles principales de logging son:

        DEBUG
        INFO
        WARNING
        ERROR
        CRITICAL
    """

    logger.debug(
        "Información detallada para debugging",
    )

    logger.info(
        "La operación se ejecutó correctamente",
    )

    logger.warning(
        "Se detectó una situación inesperada",
    )

    logger.error(
        "Ocurrió un error",
    )

    logger.critical(
        "Error crítico",
    )


# 26. Comparación de librerías


def library_comparison() -> None:
    """
    requests:

        - Síncrono
        - API sencilla
        - Muy utilizado
        - Excelente para aplicaciones tradicionales


    httpx:

        - Síncrono
        - Asíncrono
        - HTTP/1.1
        - HTTP/2
        - Cliente moderno


    aiohttp:

        - Asíncrono
        - Integración con asyncio
        - Muy útil para aplicaciones con muchas operaciones
          concurrentes de I/O
    """

    print(
        """
requests
    HTTP síncrono y sencillo

httpx
    HTTP síncrono + asíncrono + HTTP/2

aiohttp
    HTTP asíncrono + asyncio
        """,
    )


def main() -> None:
    print("Módulo. HTTP y consumo de APIs")
    print()

    print("1. HTTP")
    http_conceptos()

    print()
    print("2. requests - GET")
    requests_get()

    print()
    print("3. requests - parámetros")
    requests_params()

    print()
    print("4. requests - headers")
    requests_headers()

    print()
    print("5. requests - POST")
    requests_post()

    print()
    print("6. requests - errores")
    requests_error_handling()

    print()
    print("7. requests - timeout")
    requests_timeout()

    print()
    print("8. httpx - GET")
    httpx_get()

    print()
    print("9. httpx - Client")
    httpx_client()

    print()
    print("10. httpx - headers")
    httpx_headers()

    print()
    print("11. httpx - POST")
    httpx_post()

    print()
    print("12. httpx - HTTP/2")
    httpx_http2()

    print()
    print("13. httpx - errores")
    httpx_error_handling()

    print()
    print("14. Reintentos")

    try:
        retry_example(
            "https://jsonplaceholder.typicode.com/users/1",
        )
    except Exception as error:
        logger.error(
            "No se pudo completar la petición: %s",
            error,
        )

    print()
    print("15. aiohttp - GET")
    asyncio.run(
        aiohttp_get(),
    )

    print()
    print("16. aiohttp - timeout")
    asyncio.run(
        aiohttp_timeout(),
    )

    print()
    print("17. aiohttp - peticiones concurrentes")
    asyncio.run(
        aiohttp_multiple_requests(),
    )

    print()
    print("18. httpx - streaming")
    httpx_streaming()

    print()
    print("19. Descarga mediante streaming")

    download_file(
        "https://httpbin.org/bytes/1024",
        "download.bin",
    )

    print()
    print("20. aiohttp - streaming")
    asyncio.run(
        aiohttp_streaming(),
    )

    print()
    print("21. Uso eficiente de memoria")
    memory_efficient_processing()

    print()
    print("22. Cliente HTTP")
    user_client_example()

    print()
    print("23. Smocker")
    smocker_documentation()

    print()
    print("24. Logging")
    logging_examples()

    print()
    print("25. Comparación")
    library_comparison()


if __name__ == "__main__":
    main()
