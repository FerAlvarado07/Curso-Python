from functools import wraps
import time


def retry(max_retries=3, delay=1):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            attempts = 0

            while attempts < max_retries:
                try:
                    return function(*args, **kwargs)

                except Exception as error:
                    attempts += 1

                    if attempts >= max_retries:
                        raise error

                    wait_time = delay * (2 ** (attempts - 1))

                    print(f"Intento {attempts} falló: {error}")
                    print(f"Reintentando en {wait_time} segundos...")

                    time.sleep(wait_time)

        return wrapper

    return decorator


# Contador de intentos de la operación
operation_attempts = 0


@retry(max_retries=4, delay=1)
def unstable_operation():
    global operation_attempts

    operation_attempts += 1

    print(f"Ejecutando operación: intento {operation_attempts}")

    if operation_attempts < 3:
        raise ConnectionError("El servicio no está disponible")

    return "Operación exitosa"


result = unstable_operation()

print(result)
