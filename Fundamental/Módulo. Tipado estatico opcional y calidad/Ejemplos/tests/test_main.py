from src.main import addNumbers


def test_addNumbers():
    assert addNumbers(2, 3) == 5
    assert addNumbers(-1, 1) == 0
