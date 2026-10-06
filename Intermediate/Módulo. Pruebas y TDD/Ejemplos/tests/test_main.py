import sys
from datetime import datetime
from unittest.mock import Mock, patch

import pytest
from hypothesis import given
from hypothesis import strategies as st

# 1. Parametrización con pytest


def sumar(a: int, b: int) -> int:
    return a + b


@pytest.mark.parametrize(
    "a, b, esperado",
    [
        (1, 2, 3),
        (5, 5, 10),
        (10, 20, 30),
        (-1, 1, 0),
    ],
)
def test_sumar_parametrize(a, b, esperado):
    assert sumar(a, b) == esperado


@pytest.mark.parametrize(
    "nombre, esperado",
    [
        ("Fernando", True),
        ("Juan", True),
        ("", False),
        ("   ", False),
    ],
)
def test_nombre_valido(nombre, esperado):
    resultado = bool(nombre.strip())

    assert resultado is esperado


# 2. pytest.param


@pytest.mark.parametrize(
    "a, b, esperado",
    [
        pytest.param(2, 3, 5, id="suma-positivos"),
        pytest.param(-2, 3, 1, id="suma-negativo"),
        pytest.param(0, 0, 0, id="suma-ceros"),
    ],
)
def test_sumar_con_ids(a, b, esperado):
    assert sumar(a, b) == esperado


@pytest.mark.parametrize(
    "numero, esperado",
    [
        pytest.param(2, True, id="par"),
        pytest.param(3, False, id="impar"),
        pytest.param(0, True, id="cero"),
    ],
)
def test_es_par_con_ids(numero, esperado):
    assert (numero % 2 == 0) is esperado


@pytest.mark.parametrize(
    "numero, esperado",
    [
        (2, True),
        pytest.param(
            3,
            False,
            marks=pytest.mark.slow,
            id="caso-lento",
        ),
    ],
)
def test_es_par_con_marker(numero, esperado):
    assert (numero % 2 == 0) is esperado


# 3. Markers personalizados


@pytest.mark.unit
def test_suma_unit():
    assert 2 + 2 == 4


@pytest.mark.integration
def test_api_integration():
    assert True


@pytest.mark.slow
def test_proceso_lento():
    assert True


# Ejecutar markers:
#
# poetry run pytest -m unit
# poetry run pytest -m integration
# poetry run pytest -m slow
# poetry run pytest -m "not slow"
# poetry run pytest -m "unit and not slow"


# 4. Combinar markers y parametrización


@pytest.mark.unit
@pytest.mark.parametrize(
    "numero, esperado",
    [
        (2, True),
        (4, True),
        (6, True),
        (3, False),
        (5, False),
    ],
)
def test_es_par_unit(numero, esperado):
    assert (numero % 2 == 0) is esperado


# 5. pytest.raises


def dividir(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("No se puede dividir entre cero")

    return a / b


def test_dividir():
    assert dividir(10, 2) == 5


def test_dividir_cero():
    with pytest.raises(ValueError):
        dividir(10, 0)


def test_dividir_cero_mensaje():
    with pytest.raises(
        ValueError,
        match="No se puede dividir",
    ):
        dividir(10, 0)


# 6. Fixtures


@pytest.fixture
def usuario_fixture():
    return {
        "nombre": "Fernando",
        "email": "fernando@example.com",
    }


def test_nombre_usuario(usuario_fixture):
    assert usuario_fixture["nombre"] == "Fernando"


def test_email_usuario(usuario_fixture):
    assert usuario_fixture["email"] == "fernando@example.com"


# 7. Fixture con yield


@pytest.fixture
def archivo_fixture():
    print("Preparando archivo")

    archivo = "datos.txt"

    yield archivo

    print("Eliminando archivo")


def test_archivo_fixture(archivo_fixture):
    assert archivo_fixture == "datos.txt"


# 8. Fixture con scope function


@pytest.fixture(scope="function")
def usuario_function():
    return {
        "nombre": "Fernando",
    }


def test_usuario_function(usuario_function):
    assert usuario_function["nombre"] == "Fernando"


# 9. Fixture con scope class


@pytest.fixture(scope="class")
def usuario_class():
    return {
        "nombre": "Fernando",
    }


class TestUsuarios:
    def test_nombre(self, usuario_class):
        assert usuario_class["nombre"] == "Fernando"

    def test_usuario_existe(self, usuario_class):
        assert usuario_class is not None


# 10. Fixture con scope module


@pytest.fixture(scope="module")
def configuracion_module():
    return {
        "host": "localhost",
        "port": 8000,
    }


def test_configuracion_host(configuracion_module):
    assert configuracion_module["host"] == "localhost"


# 11. Fixture con scope session


@pytest.fixture(scope="session")
def configuracion_session():
    return {
        "environment": "test",
    }


def test_configuracion_environment(configuracion_session):
    assert configuracion_session["environment"] == "test"


# 12. Fixture que depende de otra fixture


@pytest.fixture
def usuario_base():
    return {
        "nombre": "Fernando",
        "email": "fernando@example.com",
    }


@pytest.fixture
def usuario_autenticado(usuario_base):
    usuario_base["token"] = "abc123"

    return usuario_base


def test_usuario_autenticado(usuario_autenticado):
    assert usuario_autenticado["token"] == "abc123"


# 13. Fixture con autouse


@pytest.fixture(autouse=True)
def preparar_test():
    print("Antes del test")


def test_autouse_uno():
    assert True


def test_autouse_dos():
    assert True


# 14. Skip


@pytest.mark.skip(reason="Funcionalidad todavía no implementada")
def test_funcionalidad_no_implementada():
    assert True


# 15. Skipif


@pytest.mark.skipif(
    sys.platform == "win32",
    reason="No funciona en Windows",
)
def test_linux():
    assert True


# 16. XFail


@pytest.mark.xfail(reason="Bug conocido")
def test_funcionalidad_esperada_fallida():
    assert 1 == 2


# 17. XFail estricto


@pytest.mark.xfail(
    reason="Bug conocido",
    strict=True,
)
def test_funcionalidad_xfail_estricto():
    assert 1 == 2


# 18. Mock


def enviar_correo(email: str) -> str:
    return f"Correo enviado a {email}"


def test_enviar_correo_mock():
    servicio = Mock()

    servicio.enviar.return_value = "OK"

    resultado = servicio.enviar("fernando@example.com")

    assert resultado == "OK"


# 19. Comprobar llamadas con Mock


def test_mock():
    servicio = Mock()

    servicio.enviar("fernando@example.com")

    servicio.enviar.assert_called_once_with("fernando@example.com")


def test_mock_called():
    servicio = Mock()

    servicio.enviar()

    servicio.enviar.assert_called()


def test_mock_not_called():
    servicio = Mock()

    servicio.enviar.assert_not_called()


# 20. Mock con return_value


servicio_usuario = Mock()

servicio_usuario.obtener_usuario.return_value = {
    "id": 1,
    "nombre": "Fernando",
}


def test_mock_return_value():
    usuario = servicio_usuario.obtener_usuario()

    assert usuario["id"] == 1
    assert usuario["nombre"] == "Fernando"


# 21. Mock con side_effect


servicio_error = Mock()

servicio_error.obtener_usuario.side_effect = ValueError("Usuario no encontrado")


def test_mock_side_effect():
    with pytest.raises(ValueError, match="Usuario no encontrado"):
        servicio_error.obtener_usuario()


# 22. Mock con diferentes resultados usando side_effect


servicio_resultados = Mock()

servicio_resultados.obtener.side_effect = [
    "primero",
    "segundo",
    "tercero",
]


def test_mock_side_effect_lista():
    assert servicio_resultados.obtener() == "primero"
    assert servicio_resultados.obtener() == "segundo"
    assert servicio_resultados.obtener() == "tercero"


# 23. Patch


def obtener_fecha() -> datetime:
    return datetime.now()


def test_obtener_fecha():
    with patch("tests.test_main.datetime") as mock_datetime:
        mock_datetime.now.return_value = "2026-01-01"

        resultado = obtener_fecha()

        assert resultado == "2026-01-01"


# 24. Patch como decorador


@patch("tests.test_main.datetime")
def test_obtener_fecha_decorador(mock_datetime):
    mock_datetime.now.return_value = "2026-01-01"

    resultado = obtener_fecha()

    assert resultado == "2026-01-01"


# 25. patch.object


def test_patch_object():
    servicio = Mock()

    with patch.object(
        servicio,
        "obtener",
        return_value="Fernando",
    ):
        resultado = servicio.obtener()

        assert resultado == "Fernando"


# 26. Hypothesis con enteros


@given(st.integers())
def test_doble(numero):
    resultado = numero * 2

    assert resultado % 2 == 0


# 27. Hypothesis con strings


@given(st.text())
def test_string(texto):
    assert isinstance(texto, str)


# 28. Hypothesis con booleanos


@given(st.booleans())
def test_booleano(valor):
    assert valor is True or valor is False


# 29. Hypothesis con listas


@given(st.lists(st.integers()))
def test_lista(numeros):
    assert isinstance(numeros, list)


# 30. Hypothesis con diccionarios


@given(
    st.dictionaries(
        keys=st.text(),
        values=st.integers(),
    )
)
def test_diccionario(datos):
    assert isinstance(datos, dict)


# 31. Hypothesis con rangos


@given(
    st.integers(
        min_value=1,
        max_value=100,
    )
)
def test_numero_positivo(numero):
    assert 1 <= numero <= 100


# 32. Hypothesis combinando estrategias


@given(
    nombre=st.text(min_size=1),
    edad=st.integers(
        min_value=18,
        max_value=100,
    ),
)
def test_usuario_hypothesis(nombre, edad):
    assert len(nombre) >= 1
    assert edad >= 18


# 33. tmp_path


def test_archivo_tmp_path(tmp_path):
    archivo = tmp_path / "datos.txt"

    archivo.write_text(
        "Hola Fernando",
        encoding="utf-8",
    )

    contenido = archivo.read_text(
        encoding="utf-8",
    )

    assert contenido == "Hola Fernando"
