import asyncio
from unittest.mock import patch

import httpx

from src.main import (
    calculate_cpu,
    execute_cpu_parallel,
    fetch_all_async,
    fetch_all_sync,
)


def test_calculate_cpu():
    result = calculate_cpu(1)

    assert isinstance(result, float)
    assert result > 0


def test_execute_cpu_parallel():
    numbers = [1, 2, 3, 4]

    results = execute_cpu_parallel(numbers)

    assert len(results) == 4

    for result in results:
        assert isinstance(result, float)
        assert result > 0


def test_fetch_all_sync():
    def handler(
        request: httpx.Request,
    ) -> httpx.Response:
        return httpx.Response(
            status_code=200,
            request=request,
        )

    transport = httpx.MockTransport(handler)

    with patch(
        "src.main.httpx.Client",
        return_value=httpx.Client(transport=transport),
    ):
        urls = [
            "https://example.com/1",
            "https://example.com/2",
            "https://example.com/3",
        ]

        results = fetch_all_sync(urls)

    assert results == [
        200,
        200,
        200,
    ]


def test_fetch_all_async():
    async def run_test():
        def handler(
            request: httpx.Request,
        ) -> httpx.Response:
            return httpx.Response(
                status_code=200,
                request=request,
            )

        transport = httpx.MockTransport(handler)

        with patch(
            "src.main.httpx.AsyncClient",
            return_value=httpx.AsyncClient(transport=transport),
        ):
            urls = [
                "https://example.com/1",
                "https://example.com/2",
                "https://example.com/3",
            ]

            return await fetch_all_async(
                urls,
                max_concurrent=2,
            )

    results = asyncio.run(run_test())

    assert results == [
        200,
        200,
        200,
    ]


def test_fetch_all_sync_error():
    def handler(
        request: httpx.Request,
    ) -> httpx.Response:
        return httpx.Response(
            status_code=500,
            request=request,
        )

    transport = httpx.MockTransport(handler)

    with patch(
        "src.main.httpx.Client",
        return_value=httpx.Client(transport=transport),
    ):
        urls = [
            "https://example.com",
        ]

        try:
            fetch_all_sync(urls)
        except httpx.HTTPStatusError as error:
            assert error.response.status_code == 500
        else:
            raise AssertionError("Expected HTTPStatusError")


def test_fetch_all_async_respects_semaphore():
    async def run_test():
        active_requests = 0
        max_concurrency = 0

        async def handler(
            request: httpx.Request,
        ) -> httpx.Response:
            nonlocal active_requests
            nonlocal max_concurrency

            active_requests += 1

            max_concurrency = max(
                max_concurrency,
                active_requests,
            )

            await asyncio.sleep(0.01)

            active_requests -= 1

            return httpx.Response(
                status_code=200,
                request=request,
            )

        semaphore = asyncio.Semaphore(2)

        async def execute_request(
            client: httpx.AsyncClient,
            url: str,
        ) -> httpx.Response:
            async with semaphore:
                return await client.get(url)

        transport = httpx.MockTransport(handler)

        async with httpx.AsyncClient(transport=transport) as client:
            urls = [
                "https://example.com/1",
                "https://example.com/2",
                "https://example.com/3",
                "https://example.com/4",
                "https://example.com/5",
            ]

            tasks = [
                execute_request(
                    client,
                    url,
                )
                for url in urls
            ]

            responses = await asyncio.gather(*tasks)

        return (
            responses,
            max_concurrency,
        )

    responses, max_concurrency = asyncio.run(run_test())

    assert len(responses) == 5

    assert all(response.status_code == 200 for response in responses)

    assert max_concurrency <= 2
