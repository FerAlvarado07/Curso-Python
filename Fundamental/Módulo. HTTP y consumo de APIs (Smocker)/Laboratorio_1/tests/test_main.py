from unittest.mock import Mock, patch

import httpx
import pytest

from src.main import download_file, httpx_client_with_retry


@patch("src.main.httpx.Client")
def test_httpx_client_with_retry_success(mock_client):
    mock_response = Mock()
    mock_response.json.return_value = {
        "id": 1,
        "name": "Fernando",
    }

    mock_client_instance = mock_client.return_value.__enter__.return_value
    mock_client_instance.get.return_value = mock_response

    result = httpx_client_with_retry(
        "https://example.com/users/1",
    )

    assert result == {
        "id": 1,
        "name": "Fernando",
    }

    mock_client_instance.get.assert_called_once_with(
        "https://example.com/users/1",
    )


@patch("src.main.time.sleep")
@patch("src.main.httpx.Client")
def test_httpx_client_with_retry(mock_client, mock_sleep):
    mock_response = Mock()
    mock_response.json.return_value = {
        "id": 1,
    }

    mock_client_instance = mock_client.return_value.__enter__.return_value

    mock_client_instance.get.side_effect = [
        httpx.RequestError("Error de conexión"),
        httpx.RequestError("Error de conexión"),
        mock_response,
    ]

    result = httpx_client_with_retry(
        "https://example.com/users/1",
        retries=3,
    )

    assert result == {
        "id": 1,
    }

    assert mock_client_instance.get.call_count == 3

    mock_sleep.assert_any_call(1)
    mock_sleep.assert_any_call(2)


@patch("src.main.time.sleep")
@patch("src.main.httpx.Client")
def test_httpx_client_with_retry_max_retries(
    mock_client,
    mock_sleep,
):
    mock_client_instance = mock_client.return_value.__enter__.return_value

    mock_client_instance.get.side_effect = httpx.RequestError(
        "Error de conexión",
    )

    with pytest.raises(RuntimeError):
        httpx_client_with_retry(
            "https://example.com/users/1",
            retries=3,
        )

    assert mock_client_instance.get.call_count == 3

    mock_sleep.assert_any_call(1)
    mock_sleep.assert_any_call(2)


@patch("src.main.time.sleep")
@patch("src.main.httpx.Client")
def test_httpx_client_with_retry_http_error(
    mock_client,
    mock_sleep,
):
    mock_response = Mock()
    mock_response.status_code = 404

    error = httpx.HTTPStatusError(
        "404 Not Found",
        request=Mock(),
        response=mock_response,
    )

    mock_client_instance = mock_client.return_value.__enter__.return_value
    mock_client_instance.get.return_value.raise_for_status.side_effect = error

    with pytest.raises(httpx.HTTPStatusError):
        httpx_client_with_retry(
            "https://example.com/users/999",
            retries=3,
        )

    mock_client_instance.get.assert_called_once()

    mock_sleep.assert_not_called()


@patch("src.main.httpx.Client")
def test_download_file(mock_client, tmp_path):
    mock_response = Mock()

    mock_response.iter_bytes.return_value = [
        b"Hola ",
        b"mundo",
    ]

    mock_client_instance = mock_client.return_value.__enter__.return_value

    mock_stream = mock_client_instance.stream.return_value
    mock_stream.__enter__.return_value = mock_response

    destination = tmp_path / "archivo.txt"

    download_file(
        "https://example.com/archivo.txt",
        str(destination),
    )

    assert destination.exists()
    assert destination.read_bytes() == b"Hola mundo"


@patch("src.main.httpx.Client")
def test_download_file_http_error(mock_client, tmp_path):
    mock_response = Mock()

    error = httpx.HTTPStatusError(
        "404 Not Found",
        request=Mock(),
        response=mock_response,
    )

    mock_response.raise_for_status.side_effect = error

    mock_client_instance = mock_client.return_value.__enter__.return_value

    mock_stream = mock_client_instance.stream.return_value
    mock_stream.__enter__.return_value = mock_response

    destination = tmp_path / "archivo.txt"

    download_file(
        "https://example.com/archivo.txt",
        str(destination),
    )

    assert not destination.exists()
