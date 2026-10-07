# HU  - Como usuario, quiero calcular el total de una lista de productos para conocer cuánto debo pagar.

# Criterios de aceptación:
# El total de una lista vacía debe ser 0.
# El total debe ser la suma de los precios.
# Los precios deben ser mayores o iguales a 0.
# El resultado debe ser un número.
# El cálculo debe funcionar independientemente del número de productos.


# green test

# def calcular_total(precios: list[float]) -> float:
#     return sum(precios)


# Refactorización:
def calcular_total(precios: list[float]) -> float:
    if any(precio < 0 for precio in precios):
        raise ValueError("Los precios no pueden ser negativos")

    return sum(precios)
