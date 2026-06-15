"""
Pruebas unitarias para src.core.medicos (GestorMedicos y Medico).
"""

import json

import pytest

from src.core.medicos import GestorMedicos, Medico


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def archivo_medicos(tmp_path):
    """Ruta a un archivo JSON temporal y aislado para cada prueba."""
    return str(tmp_path / "medicos.json")


@pytest.fixture
def gestor(archivo_medicos):
    """Gestor de médicos vacío, sin datos previos."""
    return GestorMedicos(archivo_datos=archivo_medicos)


@pytest.fixture
def gestor_con_datos(gestor):
    """Gestor de médicos con dos médicos precargados."""
    gestor.crear_medico("M1", "Dr. Pérez", "Cardiología")
    gestor.crear_medico("M2", "Dra. López", "Pediatría")
    return gestor


# ---------------------------------------------------------------------------
# Inicialización / carga de datos
# ---------------------------------------------------------------------------

class TestCargaInicial:
    def test_inicia_vacio_si_no_existe_archivo(self, archivo_medicos):
        gestor = GestorMedicos(archivo_datos=archivo_medicos)
        assert gestor.medicos == {}
        assert gestor.listar_medicos() == []

    def test_carga_datos_existentes_del_archivo(self, archivo_medicos):
        datos = {
            "M1": {"id_medico": "M1", "nombre": "Dr. Pérez", "especialidad": "Cardiología"}
        }
        with open(archivo_medicos, "w", encoding="utf-8") as f:
            json.dump(datos, f)

        gestor = GestorMedicos(archivo_datos=archivo_medicos)

        assert "M1" in gestor.medicos
        assert gestor.medicos["M1"] == Medico("M1", "Dr. Pérez", "Cardiología")


# ---------------------------------------------------------------------------
# crear_medico
# ---------------------------------------------------------------------------

class TestCrearMedico:
    def test_crear_medico_exitoso(self, gestor):
        resultado = gestor.crear_medico("M1", "Dr. Pérez", "Cardiología")

        assert resultado is True
        assert gestor.obtener_medico("M1") == Medico("M1", "Dr. Pérez", "Cardiología")

    def test_crear_medico_con_id_duplicado_falla(self, gestor_con_datos):
        resultado = gestor_con_datos.crear_medico("M1", "Otro Doctor", "Dermatología")

        assert resultado is False
        medico = gestor_con_datos.obtener_medico("M1")
        assert medico.nombre == "Dr. Pérez"
        assert medico.especialidad == "Cardiología"

    def test_crear_medico_persiste_en_archivo(self, archivo_medicos):
        gestor = GestorMedicos(archivo_datos=archivo_medicos)
        gestor.crear_medico("M1", "Dr. Pérez", "Cardiología")

        with open(archivo_medicos, "r", encoding="utf-8") as f:
            datos_guardados = json.load(f)

        assert datos_guardados["M1"]["nombre"] == "Dr. Pérez"
        assert datos_guardados["M1"]["especialidad"] == "Cardiología"


# ---------------------------------------------------------------------------
# listar_medicos
# ---------------------------------------------------------------------------

class TestListarMedicos:
    def test_listar_medicos_vacio(self, gestor):
        assert gestor.listar_medicos() == []

    def test_listar_medicos_con_datos(self, gestor_con_datos):
        medicos = gestor_con_datos.listar_medicos()

        assert len(medicos) == 2
        ids = {m.id_medico for m in medicos}
        assert ids == {"M1", "M2"}


# ---------------------------------------------------------------------------
# obtener_medico
# ---------------------------------------------------------------------------

class TestObtenerMedico:
    def test_obtener_medico_existente(self, gestor_con_datos):
        medico = gestor_con_datos.obtener_medico("M2")

        assert medico is not None
        assert medico.nombre == "Dra. López"
        assert medico.especialidad == "Pediatría"

    def test_obtener_medico_inexistente_retorna_none(self, gestor_con_datos):
        assert gestor_con_datos.obtener_medico("NO_EXISTE") is None


# ---------------------------------------------------------------------------
# actualizar_medico
# ---------------------------------------------------------------------------

class TestActualizarMedico:
    def test_actualizar_medico_existente(self, gestor_con_datos):
        resultado = gestor_con_datos.actualizar_medico("M1", "Dr. Juan Pérez", "Neurología")

        assert resultado is True
        medico = gestor_con_datos.obtener_medico("M1")
        assert medico.nombre == "Dr. Juan Pérez"
        assert medico.especialidad == "Neurología"

    def test_actualizar_medico_inexistente_falla(self, gestor_con_datos):
        resultado = gestor_con_datos.actualizar_medico("NO_EXISTE", "X", "Y")

        assert resultado is False

    def test_actualizar_medico_persiste_cambios(self, archivo_medicos):
        gestor = GestorMedicos(archivo_datos=archivo_medicos)
        gestor.crear_medico("M1", "Dr. Pérez", "Cardiología")

        gestor.actualizar_medico("M1", "Dr. Pérez Actualizado", "Neurología")

        with open(archivo_medicos, "r", encoding="utf-8") as f:
            datos_guardados = json.load(f)

        assert datos_guardados["M1"]["nombre"] == "Dr. Pérez Actualizado"
        assert datos_guardados["M1"]["especialidad"] == "Neurología"


# ---------------------------------------------------------------------------
# eliminar_medico
# ---------------------------------------------------------------------------

class TestEliminarMedico:
    def test_eliminar_medico_existente(self, gestor_con_datos):
        resultado = gestor_con_datos.eliminar_medico("M1")

        assert resultado is True
        assert gestor_con_datos.obtener_medico("M1") is None
        assert len(gestor_con_datos.listar_medicos()) == 1

    def test_eliminar_medico_inexistente_falla(self, gestor_con_datos):
        resultado = gestor_con_datos.eliminar_medico("NO_EXISTE")

        assert resultado is False
        assert len(gestor_con_datos.listar_medicos()) == 2

    def test_eliminar_medico_persiste_en_archivo(self, archivo_medicos):
        gestor = GestorMedicos(archivo_datos=archivo_medicos)
        gestor.crear_medico("M1", "Dr. Pérez", "Cardiología")

        gestor.eliminar_medico("M1")

        with open(archivo_medicos, "r", encoding="utf-8") as f:
            datos_guardados = json.load(f)

        assert "M1" not in datos_guardados
