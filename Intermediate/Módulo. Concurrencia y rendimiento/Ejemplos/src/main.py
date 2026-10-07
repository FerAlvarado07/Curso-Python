# Módulo. Concurrencia y rendimiento

import asyncio
import cProfile
import multiprocessing
import threading
import timeit
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

# 1. Concurrencia

# La **concurrencia** consiste en gestionar varias tareas durante un mismo periodo de tiempo.

# Una ejecución secuencial sería:

# Tarea A ──────────►
#                    Tarea B ──────────►
#                                       Tarea C ──────────►
# ```

# Una ejecución concurrente puede aprovechar los tiempos de espera:

# Tarea A ─────────────────►
# Tarea B ───────►
# Tarea C ───────────────►


# La concurrencia no implica necesariamente que las tareas se ejecuten exactamente al mismo tiempo.


# 2. Paralelismo

# El **paralelismo** consiste en ejecutar varias tareas simultáneamente, normalmente utilizando diferentes núcleos del procesador.


# CPU 1: █████████████
# CPU 2: █████████████
# CPU 3: █████████████
# CPU 4: █████████████


# ## Diferencia

# - **Concurrencia:** gestionar varias tareas.
# - **Paralelismo:** ejecutar varias tareas al mismo tiempo.

# 3. CPU-bound e I/O-bound

# Antes de elegir una estrategia de concurrencia debemos identificar el tipo de trabajo.

## CPU-bound

# Una tarea es CPU-bound cuando el principal cuello de botella es el procesador.

# Ejemplos:

# - Cálculos matemáticos.
# - Procesamiento de imágenes.
# - Compresión.
# - Criptografía.
# - Machine Learning.
# - Procesamiento de grandes cantidades de datos.

# Ejemplo:


def calcular():
    total = 0

    for numero in range(10_000_000):
        total += numero * numero

    return total


# La mayor parte del tiempo se utiliza CPU.


## I/O-bound

# Una tarea es I/O-bound cuando pasa mucho tiempo esperando una operación externa.

# Ejemplos:

# - Peticiones HTTP.
# - Bases de datos.
# - Archivos.
# - APIs.
# - Sockets.
# - Servicios externos.

# Ejemplo:

# import time


# def consultar_api():
#     time.sleep(2)
#     return "Respuesta"


# Los dos segundos representan una espera, no un cálculo intensivo.


# 4. GIL

# GIL significa **Global Interpreter Lock**.

# En CPython, el GIL ha sido históricamente un mecanismo que limita la ejecución simultánea de código Python por múltiples threads dentro de un mismo proceso. Por ello, crear múltiples threads no convierte automáticamente un trabajo CPU-bound en código paralelo aprovechando todos los núcleos.

# Esto no significa que `threading` sea inútil. Es muy útil para I/O-bound.


# Thread 1 → esperando una API
# Thread 2 → esperando una base de datos
# Thread 3 → leyendo un archivo
# Thread 4 → procesando una respuesta

# Mientras una tarea espera I/O, otra puede avanzar.

# > **Nota:** el comportamiento exacto del GIL depende de la implementación y configuración de Python. Aquí nos enfocamos en el comportamiento tradicional de CPython.


# 5. threading

# El módulo `threading` permite trabajar con múltiples threads.

# import threading
# import time


# def tarea(nombre):
#     print(f"Iniciando {nombre}")

#     time.sleep(2)

#     print(f"Finalizando {nombre}")


# thread1 = threading.Thread(
#     target=tarea,
#     args=("Tarea 1",),
# )

# thread2 = threading.Thread(
#     target=tarea,
#     args=("Tarea 2",),
# )

# thread1.start()
# thread2.start()

# thread1.join()
# thread2.join()

# print("Todas las tareas terminaron")


# #Si cada tarea espera aproximadamente dos segundos, ejecutarlas concurrentemente puede reducir el tiempo total de aproximadamente cuatro a aproximadamente dos segundos.


# # 6. start() y join()

# `start()` inicia el thread:

# ```python
# thread.start()
# ```

# `join()` espera a que termine:

# ```python
# thread.join()
# ```

# Ejemplo:

# ```python
# thread1.start()
# thread2.start()

# thread1.join()
# thread2.join()

# print("Terminó todo")
# ```

# ---

# # 7. Condiciones de carrera

# Cuando varios threads acceden o modifican los mismos datos pueden aparecer **condiciones de carrera**.

# ```python
# contador = 0
# ```

# Conceptualmente puede ocurrir:

# ```text
# Thread 1 → lee contador
# Thread 2 → lee contador
# Thread 1 → incrementa
# Thread 2 → incrementa
# ```

# El resultado puede no ser el esperado si el acceso al estado compartido no está correctamente sincronizado.

# ---

# # 8. Lock

# `threading.Lock` permite proteger una sección crítica.

# ```python
# import threading


# contador = 0
# lock = threading.Lock()


# def incrementar():
#     global contador

#     for _ in range(100_000):
#         with lock:
#             contador += 1


# thread1 = threading.Thread(target=incrementar)
# thread2 = threading.Thread(target=incrementar)

# thread1.start()
# thread2.start()

# thread1.join()
# thread2.join()

# print(f"Contador: {contador}")
# ```

# La instrucción:

# ```python
# with lock:
# ```

# protege el acceso a la sección crítica.

# ---

# # 9. concurrent.futures

# `concurrent.futures` proporciona una API de alto nivel para ejecutar tareas concurrentemente.

# Las clases principales son:

# ```python
# ThreadPoolExecutor
# ProcessPoolExecutor
# ```

# ---

# # 10. ThreadPoolExecutor

# `ThreadPoolExecutor` administra un conjunto de threads.

# Es especialmente útil para tareas I/O-bound.

# ```python
# from concurrent.futures import ThreadPoolExecutor
# import time


# def descargar_archivo(numero):
#     print(f"Descargando archivo {numero}")
#     time.sleep(2)
#     return f"Archivo {numero} descargado"


# with ThreadPoolExecutor(max_workers=3) as executor:
#     resultados = executor.map(
#         descargar_archivo,
#         range(1, 4),
#     )

# for resultado in resultados:
#     print(resultado)
# ```

# El executor se encarga de crear y administrar los threads.

# ---

# # 11. submit()

# `submit()` envía una tarea al executor y devuelve un `Future`.

# ```python
# from concurrent.futures import ThreadPoolExecutor


# def sumar(a, b):
#     return a + b


# with ThreadPoolExecutor(max_workers=3) as executor:
#     future = executor.submit(sumar, 10, 20)
#     resultado = future.result()

# print(f"Resultado: {resultado}")
# ```

# ---

# # 12. Future

# Un `Future` representa una operación cuyo resultado estará disponible posteriormente.

# ```python
# future = executor.submit(sumar, 10, 20)
# ```

# Podemos comprobar si terminó:

# ```python
# future.done()
# ```

# Y obtener el resultado:

# ```python
# resultado = future.result()
# ```

# ---

# # 13. Varios Future

# ```python
# from concurrent.futures import ThreadPoolExecutor


# def cuadrado(numero):
#     return numero * numero


# with ThreadPoolExecutor(max_workers=3) as executor:
#     futures = [
#         executor.submit(cuadrado, numero)
#         for numero in range(1, 6)
#     ]

#     for future in futures:
#         print(f"Resultado: {future.result()}")
# ```

# ---

# # 14. asyncio

# `asyncio` permite implementar concurrencia asíncrona y es especialmente útil para aplicaciones I/O-bound con muchas operaciones concurrentes.

# Conceptos principales:

# - Event loop.
# - Coroutines.
# - `async`.
# - `await`.
# - Tasks.

# ---

# # 15. Event loop

# El **event loop** administra las tareas asíncronas.

# ```text
#              Event Loop
#                   │
#        ┌──────────┼──────────┐
#        ▼          ▼          ▼
#     Tarea A    Tarea B    Tarea C
#        │          │          │
#     esperando  ejecutando  esperando
#        │          │          │
#        └──────────┼──────────┘
#                   │
#              continuar
# ```

# Cuando una coroutine llega a una operación que debe esperar y utiliza `await`, el event loop puede continuar con otra tarea.

# ---

# # 16. async

# Una función asíncrona se declara con `async def`.

# ```python
# async def obtener_datos():
#     return "Datos"
# ```

# La llamada produce una coroutine que debe ejecutarse mediante un event loop.

# ---

# # 17. await

# `await` permite esperar una operación asíncrona sin bloquear el event loop.

# ```python
# import asyncio


# async def tarea():
#     print("Iniciando")
#     await asyncio.sleep(2)
#     print("Finalizando")
# ```

# En código asíncrono debemos preferir operaciones asíncronas. Por ejemplo:

# ```python
# await asyncio.sleep(2)
# ```

# en lugar de:

# ```python
# time.sleep(2)
# ```

# `time.sleep()` bloquea el thread; `asyncio.sleep()` permite que el event loop atienda otras tareas.

# ---

# # 18. asyncio.run()

# Para ejecutar la coroutine principal:

# ```python
# import asyncio


# async def main():
#     print("Hola desde asyncio")


# asyncio.run(main())
# ```

# ---

# # 19. asyncio.gather()

# `asyncio.gather()` permite esperar varias operaciones asíncronas.

# ```python
# import asyncio


# async def tarea(nombre):
#     print(f"Iniciando {nombre}")
#     await asyncio.sleep(2)
#     print(f"Terminando {nombre}")
#     return nombre


# async def main():
#     resultados = await asyncio.gather(
#         tarea("Tarea 1"),
#         tarea("Tarea 2"),
#         tarea("Tarea 3"),
#     )

#     print(f"Resultados: {resultados}")


# asyncio.run(main())
# ```

# ---

# # 20. asyncio.create_task()

# También podemos crear tareas explícitamente.

# ```python
# import asyncio


# async def tarea(numero):
#     await asyncio.sleep(1)
#     return numero * 2


# async def main():
#     task1 = asyncio.create_task(tarea(1))
#     task2 = asyncio.create_task(tarea(2))
#     task3 = asyncio.create_task(tarea(3))

#     resultado1 = await task1
#     resultado2 = await task2
#     resultado3 = await task3

#     print(resultado1)
#     print(resultado2)
#     print(resultado3)


# asyncio.run(main())
# ```

# ---

# # 21. threading vs asyncio

# | Característica | threading | asyncio |
# |---|---|---|
# | Modelo | Threads | Coroutines |
# | I/O-bound | Excelente | Excelente |
# | CPU-bound | No es ideal | No es ideal |
# | Gestión | Threads | Event loop |
# | Sintaxis | `Thread` | `async/await` |
# | Escenario típico | I/O con librerías síncronas | Muchas operaciones I/O asíncronas |

# Regla práctica:

# - Librerías síncronas y tareas I/O-bound → `threading`.
# - Stack asíncrono y muchas operaciones I/O → `asyncio`.

# ---

# # 22. multiprocessing

# `multiprocessing` permite ejecutar tareas utilizando diferentes procesos.

# Es especialmente útil para tareas CPU-bound.

# ```python
# from multiprocessing import Process


# def calcular():
#     total = 0

#     for numero in range(10_000_000):
#         total += numero * numero

#     print(total)


# if __name__ == "__main__":
#     proceso1 = Process(target=calcular)
#     proceso2 = Process(target=calcular)

#     proceso1.start()
#     proceso2.start()

#     proceso1.join()
#     proceso2.join()
# ```

# Los procesos tienen espacios de memoria independientes y pueden ejecutarse en diferentes núcleos.

# ---

# # 23. Por qué multiprocessing para CPU-bound

# Con threads, el GIL puede limitar el paralelismo de código Python CPU-bound en el CPython tradicional.

# Con procesos:

# ```text
# Proceso 1 → CPU 1
# Proceso 2 → CPU 2
# Proceso 3 → CPU 3
# ```

# Cada proceso tiene su propio intérprete y espacio de memoria.

# ---

# # 24. ProcessPoolExecutor

# `ProcessPoolExecutor` proporciona una API de alto nivel para trabajar con procesos.

# ```python
# from concurrent.futures import ProcessPoolExecutor


# def calcular(numero):
#     return numero * numero


# if __name__ == "__main__":
#     numeros = range(1, 10)

#     with ProcessPoolExecutor() as executor:
#         resultados = executor.map(
#             calcular,
#             numeros,
#         )

#     print(f"Resultados: {list(resultados)}")
# ```

# ---

# # 25. Importante en Windows

# Cuando utilizamos `multiprocessing` o `ProcessPoolExecutor`, debemos proteger el punto de entrada:

# ```python
# if __name__ == "__main__":
#     ...
# ```

# Ejemplo:

# ```python
# from multiprocessing import Process


# def tarea():
#     print("Ejecutando proceso")


# if __name__ == "__main__":
#     proceso = Process(target=tarea)
#     proceso.start()
#     proceso.join()
# ```

# ---

# # 26. Comunicación entre procesos

# Los procesos no comparten normalmente las variables globales como lo hacen los threads.

# Algunos mecanismos de comunicación son:

# - `Queue`
# - `Pipe`
# - `Value`
# - `Array`
# - `Manager`

# Ejemplo con `Queue`:

# ```python
# from multiprocessing import Process, Queue


# def productor(queue):
#     queue.put("Datos procesados")


# if __name__ == "__main__":
#     queue = Queue()

#     proceso = Process(
#         target=productor,
#         args=(queue,),
#     )

#     proceso.start()

#     resultado = queue.get()

#     proceso.join()

#     print(f"Resultado: {resultado}")
# ```

# ---

# # 27. ¿Qué utilizar?

# ```text
#                     ¿Qué hace la tarea?
#                            │
#              ┌─────────────┴─────────────┐
#              │                           │
#           I/O-bound                  CPU-bound
#              │                           │
#        ┌─────┴─────┐                     │
#        │           │                     │
#    threading    asyncio            multiprocessing
#        │           │                     │
#        ▼           ▼                     ▼
#    APIs/files   async APIs          cálculos
#    DB/sockets   conexiones          procesamiento
# ```

# | Problema | Solución habitual |
# |---|---|
# | Esperar APIs | `asyncio` |
# | Muchas conexiones | `asyncio` |
# | I/O con librerías síncronas | `threading` |
# | Cálculos intensivos | `multiprocessing` |
# | CPU-bound paralelo | `ProcessPoolExecutor` |

# La elección real también depende de las librerías utilizadas, cantidad de tareas, memoria, overhead y arquitectura de la aplicación.

# ---

# # 28. Medición del rendimiento

# No debemos asumir que una implementación es más rápida. Hay que medir.

# Las herramientas principales son:

# ```text
# timeit
# cProfile
# ```

# ---

# # 29. timeit

# `timeit` permite medir el tiempo de ejecución de pequeños fragmentos.

# ```python
# import timeit


# resultado = timeit.timeit(
#     "sum(range(1000))",
#     number=10_000,
# )

# print(f"Tiempo: {resultado:.4f} segundos")
# ```

# `number` indica cuántas veces se ejecuta el código.

# ---

# # 30. Comparar implementaciones con timeit

# ```python
# import timeit


# tiempo_sum = timeit.timeit(
#     "sum(range(1000))",
#     number=10_000,
# )

# tiempo_loop = timeit.timeit(
#     """
# total = 0

# for numero in range(1000):
#     total += numero
# """,
#     number=10_000,
# )

# print(f"sum(): {tiempo_sum:.4f} segundos")
# print(f"loop: {tiempo_loop:.4f} segundos")
# ```

# ---

# # 31. timeit con funciones

# ```python
# import timeit


# def sumar():
#     return sum(range(1000))


# tiempo = timeit.timeit(
#     sumar,
#     number=10_000,
# )

# print(f"Tiempo: {tiempo:.4f} segundos")
# ```

# ---

# # 32. cProfile

# `cProfile` permite analizar el rendimiento de un programa completo.

# ```python
# def funcion_a():
#     return sum(range(1_000_000))


# def funcion_b():
#     total = 0

#     for numero in range(1_000_000):
#         total += numero

#     return total


# def main():
#     funcion_a()
#     funcion_b()


# if __name__ == "__main__":
#     main()
# ```

# Guarda el código como `programa.py` y ejecuta:

# ```powershell
# poetry run python -m cProfile programa.py
# ```

# ---

# # 33. Columnas importantes de cProfile

# El resultado incluye información similar a:

# ```text
# ncalls  tottime  percall  cumtime  percall filename
# ```

# ## ncalls

# Número de llamadas a la función.

# ## tottime

# Tiempo empleado directamente dentro de la función.

# ## percall

# Tiempo promedio por llamada según la columna asociada.

# ## cumtime

# Tiempo acumulado incluyendo funciones llamadas desde esa función.

# Estas métricas ayudan a localizar cuellos de botella.

# ---

# # 34. Guardar un perfil

# Podemos guardar el resultado en un archivo:

# ```powershell
# poetry run python -m cProfile -o profile.prof programa.py
# ```

# Después podemos analizarlo con `pstats`:

# ```python
# import pstats


# stats = pstats.Stats("profile.prof")
# stats.sort_stats("cumulative")
# stats.print_stats(10)
# ```

# Esto muestra las funciones con mayor tiempo acumulado.

# ---

# # 35. Ejemplo completo: secuencial vs concurrente

# Este ejemplo simula una tarea I/O-bound.

# ```python
# import time
# from concurrent.futures import ThreadPoolExecutor


# def tarea(numero):
#     print(f"Iniciando tarea {numero}")
#     time.sleep(1)
#     return numero * 2


# def ejecutar_secuencial():
#     inicio = time.perf_counter()

#     resultados = [
#         tarea(numero)
#         for numero in range(1, 4)
#     ]

#     tiempo = time.perf_counter() - inicio

#     print(f"Resultados secuenciales: {resultados}")
#     print(f"Tiempo secuencial: {tiempo:.2f} segundos")


# def ejecutar_concurrente():
#     inicio = time.perf_counter()

#     with ThreadPoolExecutor(max_workers=3) as executor:
#         resultados = list(
#             executor.map(
#                 tarea,
#                 range(1, 4),
#             )
#         )

#     tiempo = time.perf_counter() - inicio

#     print(f"Resultados concurrentes: {resultados}")
#     print(f"Tiempo concurrente: {tiempo:.2f} segundos")


# if __name__ == "__main__":
#     ejecutar_secuencial()
#     ejecutar_concurrente()
# ```

# Como cada tarea espera aproximadamente un segundo, la versión concurrente puede reducir considerablemente el tiempo total.

# ---

# # 36. Ejemplo completo con asyncio

# ```python
# import asyncio
# import time


# async def tarea(numero):
#     print(f"Iniciando tarea {numero}")
#     await asyncio.sleep(1)
#     return numero * 2


# async def main():
#     inicio = time.perf_counter()

#     resultados = await asyncio.gather(
#         tarea(1),
#         tarea(2),
#         tarea(3),
#     )

#     tiempo = time.perf_counter() - inicio

#     print(f"Resultados: {resultados}")
#     print(f"Tiempo total: {tiempo:.2f} segundos")


# asyncio.run(main())
# ```

# ---

# # 37. Ejemplo CPU-bound con ProcessPoolExecutor

# ```python
# from concurrent.futures import ProcessPoolExecutor


# def calcular(numero):
#     total = 0

#     for valor in range(1_000_000):
#         total += valor * numero

#     return total


# if __name__ == "__main__":
#     numeros = [1, 2, 3, 4]

#     with ProcessPoolExecutor() as executor:
#         resultados = list(
#             executor.map(
#                 calcular,
#                 numeros,
#             )
#         )

#     print(f"Resultados: {resultados}")
# ```

# Este ejemplo puede beneficiarse de procesos cuando el trabajo es suficientemente costoso como para compensar el overhead de crear y coordinar procesos.

# ---

# # 38. Errores comunes

# ## Usar threads para cualquier problema

# No debemos asumir:

# ```text
# "Necesito que sea más rápido → creo 20 threads"
# ```

# Primero hay que determinar si el problema es CPU-bound o I/O-bound.

# ## Usar time.sleep() dentro de asyncio

# Evita:

# ```python
# async def tarea():
#     time.sleep(5)
# ```

# Preferible:

# ```python
# async def tarea():
#     await asyncio.sleep(5)
# ```

# ## Olvidar await

# Si una función es async, su llamada produce una coroutine:

# ```python
# resultado = tarea()
# ```

# Dentro de otra coroutine normalmente debemos hacer:

# ```python
# resultado = await tarea()
# ```

# ## Olvidar __main__ con multiprocessing

# En Windows utiliza:

# ```python
# if __name__ == "__main__":
#     ...
# ```

# ## Crear demasiados threads

# Más threads no significa automáticamente mayor rendimiento. Demasiados threads pueden generar mayor consumo de memoria, overhead, cambios de contexto y contención.

# ---

# # 39. Buenas prácticas

# ### 1. Identifica el tipo de tarea

# Pregunta si estás esperando I/O o consumiendo CPU.

# ### 2. Mide antes de optimizar

# Utiliza `timeit` y `cProfile`.

# ### 3. Mantén las tareas independientes cuando sea posible

# Las tareas independientes son más fáciles de ejecutar concurrentemente.

# ### 4. Evita compartir estado innecesariamente

# Compartir datos entre threads puede requerir locks. Compartir datos entre procesos requiere mecanismos de comunicación.

# ### 5. No bloquees el event loop

# En `asyncio`, evita llamadas bloqueantes dentro de coroutines.

# ### 6. No confundas concurrencia con paralelismo

# Una aplicación concurrente no necesariamente utiliza varios núcleos simultáneamente.

# ---

# # 40. Resumen

# | Concepto | Idea principal |
# |---|---|
# | Concurrencia | Gestionar varias tareas |
# | Paralelismo | Ejecutar tareas simultáneamente |
# | CPU-bound | El CPU es el cuello de botella |
# | I/O-bound | El programa pasa tiempo esperando I/O |
# | GIL | Limita el paralelismo de threads para código Python en CPython tradicional |
# | `threading` | Concurrencia mediante threads |
# | `Lock` | Protege secciones críticas |
# | `ThreadPoolExecutor` | Pool administrado de threads |
# | `Future` | Representa un resultado futuro |
# | `asyncio` | Concurrencia asíncrona |
# | Event loop | Administra coroutines |
# | `async` | Declara una función asíncrona |
# | `await` | Espera una operación asíncrona |
# | `multiprocessing` | Paralelismo mediante procesos |
# | `ProcessPoolExecutor` | Pool administrado de procesos |
# | `timeit` | Medición de pequeños fragmentos |
# | `cProfile` | Análisis del rendimiento de un programa |

# ---

# # 41. Regla rápida para elegir herramienta

# ```text
#                     TIPO DE TAREA
#                          │
#              ┌───────────┴───────────┐
#              │                       │
#           I/O-bound              CPU-bound
#              │                       │
#        ┌─────┴─────┐                 │
#        │           │                 │
#    threading    asyncio        multiprocessing
#        │           │                 │
#        ▼           ▼                 ▼
#   I/O síncrono  I/O async       CPU intensivo
# ```

# Para medir:

# ```text
# ¿Quiero saber cuánto tarda?
#         │
#         ▼
#       timeit

# ¿Quiero saber dónde está el cuello de botella?
#         │
#         ▼
#      cProfile
# ```

# ---

# # 42. Ejercicio práctico

# Implementa un programa que procese una lista de tareas simulando consultas a servicios externos.

# Requisitos:

# 1. Crear una función que reciba un identificador.
# 2. Simular una espera de 1 segundo.
# 3. Ejecutar primero las tareas de forma secuencial.
# 4. Ejecutarlas después utilizando `ThreadPoolExecutor`.
# 5. Medir ambos tiempos.
# 6. Crear una versión con `asyncio`.
# 7. Comparar los resultados.
# 8. Ejecutar `cProfile` sobre el programa.
# 9. Explicar por qué `threading` y `asyncio` funcionan bien para este escenario.
# 10. Explicar por qué `multiprocessing` no sería la primera opción.

# Salida aproximada:

# ```text
# Ejecutando de forma secuencial...

# Tarea 1 completada
# Tarea 2 completada
# Tarea 3 completada

# Tiempo secuencial: 3.00 segundos

# Ejecutando con ThreadPoolExecutor...

# Tarea 1 completada
# Tarea 2 completada
# Tarea 3 completada

# Tiempo concurrente: 1.00 segundos

# Ejecutando con asyncio...

# Tarea 1 completada
# Tarea 2 completada
# Tarea 3 completada

# Tiempo asyncio: 1.00 segundos
# ```

# Los tiempos son aproximados y dependen del equipo.

# ---

# # 43. Comandos útiles con Poetry

# Ejecutar un programa:

# ```powershell
# poetry run python programa.py
# ```

# Ejecutar un programa con cProfile:

# ```powershell
# poetry run python -m cProfile programa.py
# ```

# Guardar perfil:

# ```powershell
# poetry run python -m cProfile -o profile.prof programa.py
# ```

# Ejecutar pruebas:

# ```powershell
# poetry run python -m pytest
# ```


# # 44. Concepto final

# La concurrencia no consiste simplemente en hacer varias cosas al mismo tiempo. El objetivo es utilizar los recursos disponibles de manera eficiente.

# La estrategia depende del problema:

# I/O-bound
#     ↓
# threading / asyncio

# CPU-bound
#     ↓
# multiprocessing / ProcessPoolExecutor

# Medición
#     ↓
# timeit / cProfile

# La mejor práctica es:

# Identificar el problema
#         ↓
# Elegir la estrategia
#         ↓
# Implementar
#         ↓
# Medir
#         ↓
# Encontrar cuellos de botella
#         ↓
# Optimizar
#         ↓
# Volver a medir


# ============================================================
# EJEMPLOS EJECUTABLES
# ============================================================

# ------------------------------------------------------------
# 1. threading
# ------------------------------------------------------------


def ejemplo_thread(nombre):
    print(f"Iniciando {nombre}")
    time.sleep(1)
    print(f"Finalizando {nombre}")


def ejemplo_threading():
    print("\n--- threading ---")

    thread1 = threading.Thread(
        target=ejemplo_thread,
        args=("Tarea 1",),
    )

    thread2 = threading.Thread(
        target=ejemplo_thread,
        args=("Tarea 2",),
    )

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    print("Todas las tareas terminaron")


# ------------------------------------------------------------
# 2. threading + Lock
# ------------------------------------------------------------


def ejemplo_lock():
    print("\n--- Lock ---")

    contador = 0
    lock = threading.Lock()

    def incrementar():
        nonlocal contador

        for _ in range(100_000):
            with lock:
                contador += 1

    thread1 = threading.Thread(target=incrementar)
    thread2 = threading.Thread(target=incrementar)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    print(f"Contador final: {contador}")


# ------------------------------------------------------------
# 3. ThreadPoolExecutor
# ------------------------------------------------------------


def tarea_thread(numero):
    print(f"ThreadPool: tarea {numero}")

    time.sleep(1)

    return numero * 2


def ejemplo_thread_pool():
    print("\n--- ThreadPoolExecutor ---")

    with ThreadPoolExecutor(max_workers=3) as executor:
        resultados = list(
            executor.map(
                tarea_thread,
                range(1, 4),
            )
        )

    print(f"Resultados: {resultados}")


# ------------------------------------------------------------
# 4. Future + submit
# ------------------------------------------------------------


def ejemplo_future():
    print("\n--- Future ---")

    with ThreadPoolExecutor(max_workers=2) as executor:
        future = executor.submit(lambda: 10 + 20)

        print(f"¿Terminó?: {future.done()}")

        resultado = future.result()

    print(f"Resultado: {resultado}")


# ------------------------------------------------------------
# 5. asyncio
# ------------------------------------------------------------


async def tarea_async(numero):
    print(f"Async: iniciando tarea {numero}")

    await asyncio.sleep(1)

    print(f"Async: terminando tarea {numero}")

    return numero * 2


async def ejemplo_asyncio():
    print("\n--- asyncio ---")

    resultados = await asyncio.gather(
        tarea_async(1),
        tarea_async(2),
        tarea_async(3),
    )

    print(f"Resultados: {resultados}")


# ------------------------------------------------------------
# 6. asyncio.create_task
# ------------------------------------------------------------


async def ejemplo_create_task():
    print("\n--- asyncio.create_task ---")

    task1 = asyncio.create_task(tarea_async(1))
    task2 = asyncio.create_task(tarea_async(2))
    task3 = asyncio.create_task(tarea_async(3))

    resultados = await asyncio.gather(
        task1,
        task2,
        task3,
    )

    print(f"Resultados: {resultados}")


# ------------------------------------------------------------
# 7. multiprocessing
# ------------------------------------------------------------


def tarea_proceso(numero):
    total = 0

    for valor in range(500_000):
        total += valor * numero

    return total


def ejemplo_multiprocessing():
    print("\n--- multiprocessing ---")

    procesos = [
        multiprocessing.Process(
            target=tarea_proceso,
            args=(numero,),
        )
        for numero in range(1, 3)
    ]

    for proceso in procesos:
        proceso.start()

    for proceso in procesos:
        proceso.join()

    print("Los procesos terminaron")


# ------------------------------------------------------------
# 8. ProcessPoolExecutor
# ------------------------------------------------------------


def ejemplo_process_pool():
    print("\n--- ProcessPoolExecutor ---")

    numeros = [1, 2, 3, 4]

    with ProcessPoolExecutor() as executor:
        resultados = list(
            executor.map(
                tarea_proceso,
                numeros,
            )
        )

    print(f"Resultados: {resultados}")


# ------------------------------------------------------------
# 9. timeit
# ------------------------------------------------------------


def ejemplo_timeit():
    print("\n--- timeit ---")

    tiempo_sum = timeit.timeit(
        "sum(range(1000))",
        number=10_000,
    )

    tiempo_loop = timeit.timeit(
        """
total = 0

for numero in range(1000):
    total += numero
""",
        number=10_000,
    )

    print(f"sum(): {tiempo_sum:.4f} segundos")
    print(f"loop: {tiempo_loop:.4f} segundos")


# ------------------------------------------------------------
# 10. cProfile
# ------------------------------------------------------------


def funcion_a():
    return sum(range(1_000_000))


def funcion_b():
    total = 0

    for numero in range(1_000_000):
        total += numero

    return total


def funcion_para_profile():
    funcion_a()
    funcion_b()


def ejemplo_cprofile():
    print("\n--- cProfile ---")

    profiler = cProfile.Profile()

    profiler.enable()

    funcion_para_profile()

    profiler.disable()

    profiler.print_stats(sort="cumulative")


# ------------------------------------------------------------
# 11. Comparación secuencial vs concurrente
# ------------------------------------------------------------


def tarea_comparacion(numero):
    time.sleep(1)
    return numero * 2


def ejecutar_secuencial():
    inicio = time.perf_counter()

    resultados = [tarea_comparacion(numero) for numero in range(1, 4)]

    tiempo_total = time.perf_counter() - inicio

    print(f"Secuencial: {resultados}")
    print(f"Tiempo secuencial: {tiempo_total:.2f} segundos")


def ejecutar_concurrente():
    inicio = time.perf_counter()

    with ThreadPoolExecutor(max_workers=3) as executor:
        resultados = list(
            executor.map(
                tarea_comparacion,
                range(1, 4),
            )
        )

    tiempo_total = time.perf_counter() - inicio

    print(f"Concurrente: {resultados}")
    print(f"Tiempo concurrente: {tiempo_total:.2f} segundos")


# ------------------------------------------------------------
# 12. Ejecutar todos los ejemplos
# ------------------------------------------------------------


def main():
    ejemplo_threading()
    ejemplo_lock()
    ejemplo_thread_pool()
    ejemplo_future()

    asyncio.run(ejemplo_asyncio())

    asyncio.run(ejemplo_create_task())

    ejemplo_multiprocessing()
    ejemplo_process_pool()

    ejemplo_timeit()
    ejemplo_cprofile()

    print("\n--- Comparación ---")
    ejecutar_secuencial()
    ejecutar_concurrente()


if __name__ == "__main__":
    main()
