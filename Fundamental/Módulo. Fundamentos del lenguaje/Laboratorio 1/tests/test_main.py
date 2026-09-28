from src.main import (
    calculate_average_score,
    calculate_total_score,
    filter_users,
)


def test_filter_users():
    users = [
        {"name": "Fernando", "age": 27, "score": 85},
        {"name": "Ana", "age": 17, "score": 90},
        {"name": "Luis", "age": 30, "score": 75},
    ]

    result = filter_users(users)

    assert len(result) == 2
    assert result[0]["name"] == "Fernando"
    assert result[1]["name"] == "Luis"


def test_calculate_total_score():
    users = [
        {"name": "Fernando", "age": 27, "score": 85},
        {"name": "Ana", "age": 17, "score": 90},
        {"name": "Luis", "age": 30, "score": 75},
    ]

    result = calculate_total_score(users)

    assert result == 250


def test_calculate_average_score():
    users = [
        {"name": "Fernando", "age": 27, "score": 85},
        {"name": "Ana", "age": 17, "score": 90},
        {"name": "Luis", "age": 30, "score": 75},
    ]

    result = calculate_average_score(users)

    assert result == 250 / 3


def test_calculate_average_score_empty():
    result = calculate_average_score([])

    assert result == 0
