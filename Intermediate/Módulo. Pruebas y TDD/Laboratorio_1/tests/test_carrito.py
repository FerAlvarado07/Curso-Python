import pytest

from src.carrito import calcular_total


from hypothesis import given
from hypothesis import strategies as st


def test_carrito_vacio():
    assert calcular_total([]) == 0


def test_carrito_con_un_producto():
    assert calcular_total([100]) == 100


def test_carrito_con_varios_productos():
    assert calcular_total([100, 50, 25]) == 175


def test_precio_negativo():
    with pytest.raises(
        ValueError,
        match="Los precios no pueden ser negativos",
    ):
        calcular_total([100, -50])


@given(st.lists(st.floats(min_value=0, allow_nan=False, allow_infinity=False)))
def test_total_siempre_es_mayor_o_igual_a_cero(precios):
    total = calcular_total(precios)

    assert total >= 0


@given(
    st.lists(
        st.floats(
            min_value=0,
            allow_nan=False,
            allow_infinity=False,
        )
    ),
    st.floats(
        min_value=0,
        allow_nan=False,
        allow_infinity=False,
    ),
)
def test_agregar_producto_aumenta_el_total(precios, nuevo_precio):
    total_original = calcular_total(precios)
    total_nuevo = calcular_total(precios + [nuevo_precio])

    assert total_nuevo == total_original + nuevo_precio


@given(
    st.lists(
        st.floats(
            min_value=0,
            allow_nan=False,
            allow_infinity=False,
        )
    )
)
def test_el_orden_no_afecta_el_total(precios):
    precios_invertidos = list(reversed(precios))

    assert calcular_total(precios) == calcular_total(precios_invertidos)
