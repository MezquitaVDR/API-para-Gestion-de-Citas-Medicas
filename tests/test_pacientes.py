"""
Pruebas unitarias para src.core.pacientes (GestorPacientes y Paciente).
"""

import json

import pytest

from src.core.pacientes import GestorPacientes, Paciente


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def archivo_pacientes(tmp_path):
    """Ruta a un archivo JSON temporal y aislado para cada prueba."""
    return str(tmp_path / "pacientes.json")


@pytest.fixture
def gestor(archivo_pacientes):
    """Gestor de pacientes vacío, sin datos previos."""
    return GestorPacientes(archivo_datos=archivo_pacientes)


@pytest.fixture
def gestor_con_datos(gestor):
    """Gestor de pacientes con dos pacientes precargados."""
    gestor.crear_paciente("P1", "Ana Gómez", 30, "7000-1111")
    gestor.crear_paciente("P2", "Luis Pérez", 45, "7000-2222")
    return gestor


# ---------------------------------------------------------------------------
# Inicialización / carga de datos
# ---------------------------------------------------------------------------

class TestCargaInicial:
    def test_inicia_vacio_si_no_existe_archivo(self, archivo_pacientes):
        gestor = GestorPacientes(archivo_datos=archivo_pacientes)
        assert gestor.pacientes == {}
        assert gestor.listar_pacientes() == []

    def test_carga_datos_existentes_del_archivo(self, archivo_pacientes):
        datos = {
            "P1": {"id_paciente": "P1", "nombre": "Ana", "edad": 30, "telefono": "111"}
        }
        with open(archivo_pacientes, "w", encoding="utf-8") as f:
            json.dump(datos, f)

        gestor = GestorPacientes(archivo_datos=archivo_pacientes)

        assert "P1" in gestor.pacientes
        assert gestor.pacientes["P1"] == Paciente("P1", "Ana", 30, "111")


# ---------------------------------------------------------------------------
# crear_paciente
# ---------------------------------------------------------------------------

class TestCrearPaciente:
    def test_crear_paciente_exitoso(self, gestor):
        resultado = gestor.crear_paciente("P1", "Ana Gómez", 30, "7000-1111")

        assert resultado is True
        assert gestor.obtener_paciente("P1") == Paciente("P1", "Ana Gómez", 30, "7000-1111")

    def test_crear_paciente_con_id_duplicado_falla(self, gestor_con_datos):
        resultado = gestor_con_datos.crear_paciente("P1", "Otro Nombre", 50, "7000-9999")

        assert resultado is False
        # Los datos originales no deben modificarse
        paciente = gestor_con_datos.obtener_paciente("P1")
        assert paciente.nombre == "Ana Gómez"
        assert paciente.edad == 30

    def test_crear_paciente_persiste_en_archivo(self, archivo_pacientes):
        gestor = GestorPacientes(archivo_datos=archivo_pacientes)
        gestor.crear_paciente("P1", "Ana Gómez", 30, "7000-1111")

        with open(archivo_pacientes, "r", encoding="utf-8") as f:
            datos_guardados = json.load(f)

        assert datos_guardados["P1"]["nombre"] == "Ana Gómez"
        assert datos_guardados["P1"]["edad"] == 30


# ---------------------------------------------------------------------------
# listar_pacientes
# ---------------------------------------------------------------------------

class TestListarPacientes:
    def test_listar_pacientes_vacio(self, gestor):
        assert gestor.listar_pacientes() == []

    def test_listar_pacientes_con_datos(self, gestor_con_datos):
        pacientes = gestor_con_datos.listar_pacientes()

        assert len(pacientes) == 2
        ids = {p.id_paciente for p in pacientes}
        assert ids == {"P1", "P2"}


# ---------------------------------------------------------------------------
# obtener_paciente
# ---------------------------------------------------------------------------

class TestObtenerPaciente:
    def test_obtener_paciente_existente(self, gestor_con_datos):
        paciente = gestor_con_datos.obtener_paciente("P1")

        assert paciente is not None
        assert paciente.nombre == "Ana Gómez"

    def test_obtener_paciente_inexistente_retorna_none(self, gestor_con_datos):
        assert gestor_con_datos.obtener_paciente("NO_EXISTE") is None


# ---------------------------------------------------------------------------
# actualizar_paciente
# ---------------------------------------------------------------------------

class TestActualizarPaciente:
    def test_actualizar_paciente_existente(self, gestor_con_datos):
        resultado = gestor_con_datos.actualizar_paciente("P1", "Ana M. Gómez", 31, "7000-3333")

        assert resultado is True
        paciente = gestor_con_datos.obtener_paciente("P1")
        assert paciente.nombre == "Ana M. Gómez"
        assert paciente.edad == 31
        assert paciente.telefono == "7000-3333"

    def test_actualizar_paciente_inexistente_falla(self, gestor_con_datos):
        resultado = gestor_con_datos.actualizar_paciente("NO_EXISTE", "X", 1, "0")

        assert resultado is False

    def test_actualizar_paciente_persiste_cambios(self, archivo_pacientes):
        gestor = GestorPacientes(archivo_datos=archivo_pacientes)
        gestor.crear_paciente("P1", "Ana Gómez", 30, "7000-1111")

        gestor.actualizar_paciente("P1", "Ana Actualizada", 31, "7000-0000")

        with open(archivo_pacientes, "r", encoding="utf-8") as f:
            datos_guardados = json.load(f)

        assert datos_guardados["P1"]["nombre"] == "Ana Actualizada"
        assert datos_guardados["P1"]["edad"] == 31


# ---------------------------------------------------------------------------
# eliminar_paciente
# ---------------------------------------------------------------------------

class TestEliminarPaciente:
    def test_eliminar_paciente_existente(self, gestor_con_datos):
        resultado = gestor_con_datos.eliminar_paciente("P1")

        assert resultado is True
        assert gestor_con_datos.obtener_paciente("P1") is None
        assert len(gestor_con_datos.listar_pacientes()) == 1

    def test_eliminar_paciente_inexistente_falla(self, gestor_con_datos):
        resultado = gestor_con_datos.eliminar_paciente("NO_EXISTE")

        assert resultado is False
        # El total de pacientes no cambia
        assert len(gestor_con_datos.listar_pacientes()) == 2

    def test_eliminar_paciente_persiste_en_archivo(self, archivo_pacientes):
        gestor = GestorPacientes(archivo_datos=archivo_pacientes)
        gestor.crear_paciente("P1", "Ana Gómez", 30, "7000-1111")

        gestor.eliminar_paciente("P1")

        with open(archivo_pacientes, "r", encoding="utf-8") as f:
            datos_guardados = json.load(f)

        assert "P1" not in datos_guardados
