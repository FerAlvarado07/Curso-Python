import asyncio
import math
import time
from concurrent.futures import ProcessPoolExecutor

import httpx

URLS = [
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/1",
]


def fetch_sync(
    client: httpx.Client,
    url: str,
) -> int:
    response = client.get(url)

    response.raise_for_status()

    return response.status_code


def fetch_all_sync(
    urls: list[str],
) -> list[int]:
    with httpx.Client(timeout=10) as client:
        results = []

        for url in urls:
            status_code = fetch_sync(
                client,
                url,
            )

            results.append(status_code)

        return results


async def fetch_async(
    client: httpx.AsyncClient,
    url: str,
    semaphore: asyncio.Semaphore,
) -> int:
    async with semaphore:
        response = await client.get(url)

        response.raise_for_status()

        return response.status_code


async def fetch_all_async(
    urls: list[str],
    max_concurrent: int = 2,
) -> list[int]:
    semaphore = asyncio.Semaphore(max_concurrent)

    async with httpx.AsyncClient(timeout=10) as client:
        tasks = [
            fetch_async(
                client,
                url,
                semaphore,
            )
            for url in urls
        ]

        return await asyncio.gather(*tasks)


def calculate_cpu(
    number: int,
) -> float:
    result = 0.0

    for value in range(1, 5_000_000):
        result += math.sqrt(value * number)

    return result


def execute_cpu_parallel(
    numbers: list[int],
) -> list[float]:
    with ProcessPoolExecutor() as executor:
        results = list(
            executor.map(
                calculate_cpu,
                numbers,
            )
        )

    return results


def compare_sync(
    urls: list[str],
) -> float:
    print("\n--- Fetcher síncrono ---")

    start_time = time.perf_counter()

    results = fetch_all_sync(urls)

    elapsed_time = time.perf_counter() - start_time

    print(f"Resultados: {results}")
    print(f"Tiempo: {elapsed_time:.2f} segundos")

    return elapsed_time


async def compare_async(
    urls: list[str],
) -> float:
    print("\n--- Fetcher asíncrono ---")

    start_time = time.perf_counter()

    results = await fetch_all_async(
        urls,
        max_concurrent=2,
    )

    elapsed_time = time.perf_counter() - start_time

    print(f"Resultados: {results}")
    print(f"Tiempo: {elapsed_time:.2f} segundos")

    return elapsed_time


def compare_cpu() -> None:
    print("\n--- CPU-bound con ProcessPoolExecutor ---")

    numbers = [1, 2, 3, 4]

    start_time = time.perf_counter()

    results = execute_cpu_parallel(numbers)

    elapsed_time = time.perf_counter() - start_time

    print("Resultados:")

    for number, result in zip(
        numbers,
        results,
    ):
        print(f"{number}: {result:.2f}")

    print(f"Tiempo: {elapsed_time:.2f} segundos")


async def main() -> None:
    sync_time = compare_sync(URLS)

    async_time = await compare_async(URLS)

    compare_cpu()

    print("\n--- Comparación final ---")

    print(f"Síncrono: {sync_time:.2f} segundos")

    print(f"Asíncrono: {async_time:.2f} segundos")

    if async_time < sync_time:
        improvement = sync_time / async_time

        print(f"Async fue aproximadamente {improvement:.2f}x más rápido")


if __name__ == "__main__":
    asyncio.run(main())
