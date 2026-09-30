from datetime import datetime
from src.main import get_mexico_time


def test_get_mexico_time():
    result = get_mexico_time()

    assert isinstance(result, datetime)
    assert result.tzinfo is not None
