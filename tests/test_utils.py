"""
Pruebas unitarias para src.utils.utils.

Incluye las funciones puras de validación (validar_*) y las funciones
que dependen de la GUI (obtener_*), las cuales se prueban simulando
un widget `tk.Entry` con una clase auxiliar `EntradaFalsa` y reemplazando
`messagebox.showerror` por un "mock".
"""

import pytest

from src.utils import utils


# ---------------------------------------------------------------------------
# Auxiliares
# ---------------------------------------------------------------------------

class EntradaFalsa:
    """Simula un widget tk.Entry exponiendo únicamente el método get()."""

    def __init__(self, valor: str):
        self._valor = valor

    def get(self) -> str:
        return self._valor


# ---------------------------------------------------------------------------
# validar_entero_positivo
# ---------------------------------------------------------------------------

class TestValidarEnteroPositivo:
    @pytest.mark.parametrize(
        "valor, esperado",
        [
            ("1", True),
            ("10", True),
            ("999999", True),
            ("0", False),
            ("-5", False),
            ("3.5", False),
            ("abc", False),
            ("", False),
            (" ", False),
            ("  7  ", True),  # int() ignora espacios al inicio/fin
            (None, False),
        ],
    )
    def test_validar_entero_positivo(self, valor, esperado):
        assert utils.validar_entero_positivo(valor) is esperado


# ---------------------------------------------------------------------------
# validar_id_no_vacio
# ---------------------------------------------------------------------------

class TestValidarIdNoVacio:
    @pytest.mark.parametrize(
        "valor, esperado",
        [
            ("P1", True),
            ("  P1  ", True),
            ("", False),
            ("   ", False),
            (None, False),
            (123, False),
        ],
    )
    def test_validar_id_no_vacio(self, valor, esperado):
        assert utils.validar_id_no_vacio(valor) is esperado


# ---------------------------------------------------------------------------
# validar_fecha
# ---------------------------------------------------------------------------

class TestValidarFecha:
    @pytest.mark.parametrize(
        "fecha, esperado",
        [
            ("2026-03-30", True),
            ("2026-01-01", True),
            ("2026-12-31", True),
            ("2026-13-01", False),   # mes inválido
            ("2026-02-30", False),  # día inválido para febrero
            ("30-03-2026", False),  # formato incorrecto
            ("2026/03/30", False),  # separador incorrecto
            ("", False),
            ("no es una fecha", False),
        ],
    )
    def test_validar_fecha(self, fecha, esperado):
        assert utils.validar_fecha(fecha) is esperado


# ---------------------------------------------------------------------------
# validar_hora
# ---------------------------------------------------------------------------

class TestValidarHora:
    @pytest.mark.parametrize(
        "hora, esperado",
        [
            ("08:30", True),
            ("00:00", True),
            ("23:59", True),
            ("24:00", False),  # hora fuera de rango
            ("8:30", True),    # strptime acepta horas sin cero a la izquierda
            ("08-30", False),  # separador incorrecto
            ("", False),
            ("hh:mm", False),
        ],
    )
    def test_validar_hora(self, hora, esperado):
        assert utils.validar_hora(hora) is esperado


# ---------------------------------------------------------------------------
# obtener_texto_no_vacio
# ---------------------------------------------------------------------------

class TestObtenerTextoNoVacio:
    def test_retorna_texto_sin_espacios_cuando_es_valido(self, monkeypatch):
        mock_showerror = utils.messagebox.showerror
        monkeypatch.setattr(utils.messagebox, "showerror", lambda *a, **k: None)

        entrada = EntradaFalsa("  Ana Gómez  ")
        resultado = utils.obtener_texto_no_vacio(entrada)

        assert resultado == "Ana Gómez"
        monkeypatch.setattr(utils.messagebox, "showerror", mock_showerror)

    def test_retorna_none_y_muestra_error_si_esta_vacio(self, monkeypatch):
        llamadas = []
        monkeypatch.setattr(
            utils.messagebox, "showerror", lambda *a, **k: llamadas.append((a, k))
        )

        entrada = EntradaFalsa("   ")
        resultado = utils.obtener_texto_no_vacio(entrada)

        assert resultado is None
        assert len(llamadas) == 1


# ---------------------------------------------------------------------------
# obtener_entero_positivo
# ---------------------------------------------------------------------------

class TestObtenerEnteroPositivo:
    def test_retorna_entero_cuando_es_valido(self, monkeypatch):
        monkeypatch.setattr(utils.messagebox, "showerror", lambda *a, **k: None)

        entrada = EntradaFalsa(" 25 ")
        resultado = utils.obtener_entero_positivo(entrada)

        assert resultado == 25
        assert isinstance(resultado, int)

    def test_retorna_none_y_muestra_error_si_no_es_entero(self, monkeypatch):
        llamadas = []
        monkeypatch.setattr(
            utils.messagebox, "showerror", lambda *a, **k: llamadas.append((a, k))
        )

        entrada = EntradaFalsa("abc")
        resultado = utils.obtener_entero_positivo(entrada)

        assert resultado is None
        assert len(llamadas) == 1

    def test_retorna_none_si_es_cero_o_negativo(self, monkeypatch):
        monkeypatch.setattr(utils.messagebox, "showerror", lambda *a, **k: None)

        assert utils.obtener_entero_positivo(EntradaFalsa("0")) is None
        assert utils.obtener_entero_positivo(EntradaFalsa("-3")) is None


# ---------------------------------------------------------------------------
# obtener_fecha
# ---------------------------------------------------------------------------

class TestObtenerFecha:
    def test_retorna_fecha_cuando_es_valida(self, monkeypatch):
        monkeypatch.setattr(utils.messagebox, "showerror", lambda *a, **k: None)

        entrada = EntradaFalsa(" 2026-03-30 ")
        resultado = utils.obtener_fecha(entrada)

        assert resultado == "2026-03-30"

    def test_retorna_none_y_muestra_error_si_formato_invalido(self, monkeypatch):
        llamadas = []
        monkeypatch.setattr(
            utils.messagebox, "showerror", lambda *a, **k: llamadas.append((a, k))
        )

        entrada = EntradaFalsa("30/03/2026")
        resultado = utils.obtener_fecha(entrada)

        assert resultado is None
        assert len(llamadas) == 1


# ---------------------------------------------------------------------------
# obtener_hora
# ---------------------------------------------------------------------------

class TestObtenerHora:
    def test_retorna_hora_cuando_es_valida(self, monkeypatch):
        monkeypatch.setattr(utils.messagebox, "showerror", lambda *a, **k: None)

        entrada = EntradaFalsa(" 08:30 ")
        resultado = utils.obtener_hora(entrada)

        assert resultado == "08:30"

    def test_retorna_none_y_muestra_error_si_formato_invalido(self, monkeypatch):
        llamadas = []
        monkeypatch.setattr(
            utils.messagebox, "showerror", lambda *a, **k: llamadas.append((a, k))
        )

        entrada = EntradaFalsa("8:30 pm")
        resultado = utils.obtener_hora(entrada)

        assert resultado is None
        assert len(llamadas) == 1
