import time
from src.main import batch_generator, timer


def test_batch_generator():
    numbers = list(range(1, 11))

    result = list(batch_generator(numbers, 3))

    assert result == [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
        [10],
    ]


def test_batch_generator_exact_batches():
    numbers = list(range(1, 7))

    result = list(batch_generator(numbers, 3))

    assert result == [
        [1, 2, 3],
        [4, 5, 6],
    ]


def test_batch_generator_different_size():
    numbers = list(range(1, 11))

    result = list(batch_generator(numbers, 4))

    assert result == [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10],
    ]


def test_batch_generator_empty():
    result = list(batch_generator([], 3))

    assert result == []


def test_timer():
    with timer():
        time.sleep(0.01)
