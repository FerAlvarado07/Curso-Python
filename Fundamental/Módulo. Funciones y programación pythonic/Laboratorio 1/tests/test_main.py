import pytest

from src.main import retry


def test_retry_success():
    attempts = 0

    @retry(max_retries=4, delay=0)
    def operation():
        nonlocal attempts

        attempts += 1

        if attempts < 3:
            raise ConnectionError("Error temporal")

        return "Operación exitosa"

    result = operation()

    assert result == "Operación exitosa"
    assert attempts == 3


def test_retry_max_retries():
    attempts = 0

    @retry(max_retries=3, delay=0)
    def operation():
        nonlocal attempts

        attempts += 1

        raise ConnectionError("Error temporal")

    with pytest.raises(ConnectionError, match="Error temporal"):
        operation()

    assert attempts == 3
