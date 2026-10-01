import time
from pathlib import Path

import httpx


def httpx_client_with_retry(
    url: str,
    retries: int = 3,
    timeout: float = 5,
) -> dict:
    for attempt in range(1, retries + 1):
        try:
            with httpx.Client(timeout=timeout) as client:
                response = client.get(url)

                response.raise_for_status()

                return response.json()

        except httpx.TimeoutException:
            print(
                f"Timeout en el intento {attempt} de {retries}",
            )

        except httpx.HTTPStatusError as error:
            print(
                f"Error HTTP: {error.response.status_code}",
            )

            if error.response.status_code < 500:
                raise

        except httpx.RequestError as error:
            print(
                f"Error de conexión en el intento {attempt}: {error}",
            )

        if attempt < retries:
            wait_time = attempt
            print(
                f"Reintentando en {wait_time} segundo(s)...",
            )
            time.sleep(wait_time)

    raise RuntimeError(
        f"No fue posible realizar la petición después de {retries} intentos",
    )


def download_file(
    url: str,
    destination: str,
    timeout: float = 30,
) -> None:
    destination_path = Path(destination)

    try:
        with httpx.Client(timeout=timeout) as client:
            with client.stream("GET", url) as response:
                response.raise_for_status()

                with destination_path.open("wb") as file:
                    for chunk in response.iter_bytes(
                        chunk_size=8192,
                    ):
                        file.write(chunk)

        print(
            f"Archivo descargado correctamente: {destination_path}",
        )

    except httpx.TimeoutException:
        print("La descarga superó el tiempo máximo permitido.")

    except httpx.HTTPStatusError as error:
        print(
            f"Error HTTP durante la descarga: {error.response.status_code}",
        )

    except httpx.RequestError as error:
        print(
            f"Error de conexión durante la descarga: {error}",
        )


def main() -> None:
    print("Cliente HTTPX con reintentos")

    try:
        user = httpx_client_with_retry(
            "https://jsonplaceholder.typicode.com/users/1",
            retries=3,
            timeout=5,
        )

        print("Usuario:")
        print(user)

    except (httpx.HTTPStatusError, RuntimeError) as error:
        print(f"No fue posible obtener el usuario: {error}")

    print("\nDescarga por streaming")

    download_file(
        "https://httpbin.org/image/jpeg",
        "imagen.jpg",
    )


if __name__ == "__main__":
    main()
