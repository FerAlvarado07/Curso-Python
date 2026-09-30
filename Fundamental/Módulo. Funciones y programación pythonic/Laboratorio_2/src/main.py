import time
from contextlib import contextmanager


def batch_generator(items, batch_size):
    for index in range(0, len(items), batch_size):
        yield items[index : index + batch_size]


@contextmanager
def timer():
    start_time = time.perf_counter()

    try:
        yield
    finally:
        elapsed_time = time.perf_counter() - start_time

        print(f"Tiempo de ejecución: {elapsed_time:.4f} segundos")


if __name__ == "__main__":
    numbers = list(range(1, 11))

    print("Procesando números por lotes:")

    with timer():
        for batch in batch_generator(numbers, 3):
            print(f"Procesando lote: {batch}")

            time.sleep(0.5)
