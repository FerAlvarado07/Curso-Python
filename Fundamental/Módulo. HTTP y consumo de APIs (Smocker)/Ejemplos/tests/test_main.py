from unittest.mock import Mock, patch

from src.main import get_user


@patch("src.main.requests.get")
def test_get_user(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {
        "id": 1,
        "name": "Fernando",
        "email": "fernando@example.com",
    }

    mock_get.return_value = mock_response

    result = get_user(1)

    assert result["id"] == 1
    assert result["name"] == "Fernando"
    assert result["email"] == "fernando@example.com"

    mock_get.assert_called_once_with(
        "https://jsonplaceholder.typicode.com/users/1",
        timeout=5,
    )
