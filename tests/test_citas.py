"""
Pruebas unitarias para src.core.citas (GestorCitas y Cita).

Estas pruebas validan las reglas de negocio principales:
- No permitir IDs de cita duplicados.
- No permitir citas con pacientes o médicos inexistentes.
- No permitir conflictos de horario para un mismo médico.
- Eliminación en cascada de citas por paciente o médico.
"""

import json

import pytest

from src.core.citas import GestorCitas, Cita
from src.core.medicos import GestorMedicos
from src.core.pacientes import GestorPacientes


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def gestor_pacientes(tmp_path):
    gestor = GestorPacientes(archivo_datos=str(tmp_path / "pacientes.json"))
    gestor.crear_paciente("P1", "Ana Gómez", 30, "7000-1111")
    gestor.crear_paciente("P2", "Luis Pérez", 45, "7000-2222")
    return gestor


@pytest.fixture
def gestor_medicos(tmp_path):
    gestor = GestorMedicos(archivo_datos=str(tmp_path / "medicos.json"))
    gestor.crear_medico("M1", "Dr. Pérez", "Cardiología")
    gestor.crear_medico("M2", "Dra. López", "Pediatría")
    return gestor


@pytest.fixture
def archivo_citas(tmp_path):
    return str(tmp_path / "citas.json")


@pytest.fixture
def gestor_citas(gestor_pacientes, gestor_medicos, archivo_citas):
    return GestorCitas(gestor_pacientes, gestor_medicos, archivo_datos=archivo_citas)


@pytest.fixture
def gestor_citas_con_datos(gestor_citas):
    gestor_citas.crear_cita("C1", "P1", "M1", "2026-03-30", "08:30")
    gestor_citas.crear_cita("C2", "P2", "M2", "2026-03-31", "09:00")
    return gestor_citas


# ---------------------------------------------------------------------------
# Inicialización / carga de datos
# ---------------------------------------------------------------------------

class TestCargaInicial:
    def test_inicia_vacio_si_no_existe_archivo(self, gestor_citas):
        assert gestor_citas.citas == {}
        assert gestor_citas.listar_citas() == []

    def test_carga_datos_existentes_del_archivo(
        self, gestor_pacientes, gestor_medicos, archivo_citas
    ):
        datos = {
            "C1": {
                "id_cita": "C1",
                "id_paciente": "P1",
                "id_medico": "M1",
                "fecha": "2026-03-30",
                "hora": "08:30",
            }
        }
        with open(archivo_citas, "w", encoding="utf-8") as f:
            json.dump(datos, f)

        gestor = GestorCitas(gestor_pacientes, gestor_medicos, archivo_datos=archivo_citas)

        assert "C1" in gestor.citas
        assert gestor.citas["C1"] == Cita("C1", "P1", "M1", "2026-03-30", "08:30")


# ---------------------------------------------------------------------------
# crear_cita
# ---------------------------------------------------------------------------

class TestCrearCita:
    def test_crear_cita_exitosa(self, gestor_citas):
        ok, mensaje = gestor_citas.crear_cita("C1", "P1", "M1", "2026-03-30", "08:30")

        assert ok is True
        assert mensaje == "Cita creada correctamente."
        assert gestor_citas.obtener_cita("C1") == Cita("C1", "P1", "M1", "2026-03-30", "08:30")

    def test_crear_cita_id_duplicado_falla(self, gestor_citas_con_datos):
        ok, mensaje = gestor_citas_con_datos.crear_cita("C1", "P2", "M2", "2026-04-01", "10:00")

        assert ok is False
        assert mensaje == "Ya existe una cita con ese ID."
        # La cita original no debe modificarse
        cita = gestor_citas_con_datos.obtener_cita("C1")
        assert cita.id_paciente == "P1"

    def test_crear_cita_paciente_inexistente_falla(self, gestor_citas):
        ok, mensaje = gestor_citas.crear_cita("C1", "NO_EXISTE", "M1", "2026-03-30", "08:30")

        assert ok is False
        assert mensaje == "El paciente no existe."
        assert gestor_citas.obtener_cita("C1") is None

    def test_crear_cita_medico_inexistente_falla(self, gestor_citas):
        ok, mensaje = gestor_citas.crear_cita("C1", "P1", "NO_EXISTE", "2026-03-30", "08:30")

        assert ok is False
        assert mensaje == "El médico no existe."
        assert gestor_citas.obtener_cita("C1") is None

    def test_crear_cita_con_conflicto_de_horario_falla(self, gestor_citas_con_datos):
        # M1 ya tiene cita el 2026-03-30 a las 08:30 (C1)
        ok, mensaje = gestor_citas_con_datos.crear_cita("C3", "P2", "M1", "2026-03-30", "08:30")

        assert ok is False
        assert mensaje == "El médico ya tiene una cita asignada en esa fecha y hora."
        assert gestor_citas_con_datos.obtener_cita("C3") is None

    def test_crear_cita_mismo_horario_distinto_medico_es_valida(self, gestor_citas_con_datos):
        # M2 está libre el 2026-03-30 a las 08:30 aunque M1 tenga cita a esa hora
        ok, mensaje = gestor_citas_con_datos.crear_cita("C3", "P1", "M2", "2026-03-30", "08:30")

        assert ok is True
        assert mensaje == "Cita creada correctamente."

    def test_crear_cita_persiste_en_archivo(self, gestor_citas, archivo_citas):
        gestor_citas.crear_cita("C1", "P1", "M1", "2026-03-30", "08:30")

        with open(archivo_citas, "r", encoding="utf-8") as f:
            datos_guardados = json.load(f)

        assert datos_guardados["C1"]["id_paciente"] == "P1"
        assert datos_guardados["C1"]["id_medico"] == "M1"


# ---------------------------------------------------------------------------
# listar_citas / obtener_cita
# ---------------------------------------------------------------------------

class TestListarYObtenerCitas:
    def test_listar_citas_vacio(self, gestor_citas):
        assert gestor_citas.listar_citas() == []

    def test_listar_citas_con_datos(self, gestor_citas_con_datos):
        citas = gestor_citas_con_datos.listar_citas()

        assert len(citas) == 2
        ids = {c.id_cita for c in citas}
        assert ids == {"C1", "C2"}

    def test_obtener_cita_existente(self, gestor_citas_con_datos):
        cita = gestor_citas_con_datos.obtener_cita("C1")

        assert cita is not None
        assert cita.id_paciente == "P1"
        assert cita.id_medico == "M1"

    def test_obtener_cita_inexistente_retorna_none(self, gestor_citas_con_datos):
        assert gestor_citas_con_datos.obtener_cita("NO_EXISTE") is None


# ---------------------------------------------------------------------------
# existe_conflicto_horario
# ---------------------------------------------------------------------------

class TestExisteConflictoHorario:
    def test_detecta_conflicto_para_mismo_medico_fecha_y_hora(self, gestor_citas_con_datos):
        assert gestor_citas_con_datos.existe_conflicto_horario("M1", "2026-03-30", "08:30") is True

    def test_no_detecta_conflicto_para_otra_hora(self, gestor_citas_con_datos):
        assert gestor_citas_con_datos.existe_conflicto_horario("M1", "2026-03-30", "09:00") is False

    def test_no_detecta_conflicto_para_otro_medico(self, gestor_citas_con_datos):
        assert gestor_citas_con_datos.existe_conflicto_horario("M2", "2026-03-30", "08:30") is False

    def test_excluir_id_permite_ignorar_la_propia_cita(self, gestor_citas_con_datos):
        # C1 ocupa M1 el 2026-03-30 a las 08:30; al excluirla, no debe haber conflicto
        assert gestor_citas_con_datos.existe_conflicto_horario(
            "M1", "2026-03-30", "08:30", excluir_id="C1"
        ) is False


# ---------------------------------------------------------------------------
# actualizar_cita
# ---------------------------------------------------------------------------

class TestActualizarCita:
    def test_actualizar_cita_exitosa(self, gestor_citas_con_datos):
        ok, mensaje = gestor_citas_con_datos.actualizar_cita("C1", "P2", "M2", "2026-04-05", "11:00")

        assert ok is True
        assert mensaje == "Cita actualizada correctamente."
        cita = gestor_citas_con_datos.obtener_cita("C1")
        assert cita.id_paciente == "P2"
        assert cita.id_medico == "M2"
        assert cita.fecha == "2026-04-05"
        assert cita.hora == "11:00"

    def test_actualizar_cita_inexistente_falla(self, gestor_citas_con_datos):
        ok, mensaje = gestor_citas_con_datos.actualizar_cita(
            "NO_EXISTE", "P1", "M1", "2026-03-30", "08:30"
        )

        assert ok is False
        assert mensaje == "La cita no existe."

    def test_actualizar_cita_paciente_inexistente_falla(self, gestor_citas_con_datos):
        ok, mensaje = gestor_citas_con_datos.actualizar_cita(
            "C1", "NO_EXISTE", "M1", "2026-03-30", "08:30"
        )

        assert ok is False
        assert mensaje == "El paciente no existe."

    def test_actualizar_cita_medico_inexistente_falla(self, gestor_citas_con_datos):
        ok, mensaje = gestor_citas_con_datos.actualizar_cita(
            "C1", "P1", "NO_EXISTE", "2026-03-30", "08:30"
        )

        assert ok is False
        assert mensaje == "El médico no existe."

    def test_actualizar_cita_sin_cambiar_su_propio_horario_es_valida(self, gestor_citas_con_datos):
        # C1 ya tiene M1, 2026-03-30, 08:30: actualizar manteniendo el mismo
        # horario no debe disparar un falso conflicto (excluir_id en acción).
        ok, mensaje = gestor_citas_con_datos.actualizar_cita("C1", "P2", "M1", "2026-03-30", "08:30")

        assert ok is True
        assert mensaje == "Cita actualizada correctamente."
        cita = gestor_citas_con_datos.obtener_cita("C1")
        assert cita.id_paciente == "P2"

    def test_actualizar_cita_con_conflicto_de_horario_falla(self, gestor_citas_con_datos):
        # Mover C2 al horario que ya ocupa C1 (M1, 2026-03-30, 08:30) debe fallar
        ok, mensaje = gestor_citas_con_datos.actualizar_cita("C2", "P2", "M1", "2026-03-30", "08:30")

        assert ok is False
        assert mensaje == "El médico ya tiene una cita asignada en esa fecha y hora."
        # C2 conserva sus datos originales
        cita = gestor_citas_con_datos.obtener_cita("C2")
        assert cita.id_medico == "M2"
        assert cita.fecha == "2026-03-31"

    def test_actualizar_cita_persiste_cambios(self, gestor_citas_con_datos, archivo_citas):
        gestor_citas_con_datos.actualizar_cita("C1", "P2", "M2", "2026-04-05", "11:00")

        with open(archivo_citas, "r", encoding="utf-8") as f:
            datos_guardados = json.load(f)

        assert datos_guardados["C1"]["id_paciente"] == "P2"
        assert datos_guardados["C1"]["hora"] == "11:00"


# ---------------------------------------------------------------------------
# eliminar_cita
# ---------------------------------------------------------------------------

class TestEliminarCita:
    def test_eliminar_cita_existente(self, gestor_citas_con_datos):
        resultado = gestor_citas_con_datos.eliminar_cita("C1")

        assert resultado is True
        assert gestor_citas_con_datos.obtener_cita("C1") is None
        assert len(gestor_citas_con_datos.listar_citas()) == 1

    def test_eliminar_cita_inexistente_falla(self, gestor_citas_con_datos):
        resultado = gestor_citas_con_datos.eliminar_cita("NO_EXISTE")

        assert resultado is False
        assert len(gestor_citas_con_datos.listar_citas()) == 2

    def test_eliminar_cita_persiste_en_archivo(self, gestor_citas_con_datos, archivo_citas):
        gestor_citas_con_datos.eliminar_cita("C1")

        with open(archivo_citas, "r", encoding="utf-8") as f:
            datos_guardados = json.load(f)

        assert "C1" not in datos_guardados


# ---------------------------------------------------------------------------
# eliminar_citas_por_paciente / eliminar_citas_por_medico (eliminación en cascada)
# ---------------------------------------------------------------------------

class TestEliminacionEnCascada:
    def test_eliminar_citas_por_paciente(self, gestor_citas):
        gestor_citas.crear_cita("C1", "P1", "M1", "2026-03-30", "08:30")
        gestor_citas.crear_cita("C2", "P1", "M2", "2026-03-31", "09:00")
        gestor_citas.crear_cita("C3", "P2", "M1", "2026-04-01", "10:00")

        gestor_citas.eliminar_citas_por_paciente("P1")

        ids_restantes = {c.id_cita for c in gestor_citas.listar_citas()}
        assert ids_restantes == {"C3"}

    def test_eliminar_citas_por_paciente_sin_citas_no_falla(self, gestor_citas_con_datos):
        # P1 tiene la cita C1; un paciente sin citas no debe causar error
        gestor_citas_con_datos.eliminar_citas_por_paciente("P_SIN_CITAS")

        assert len(gestor_citas_con_datos.listar_citas()) == 2

    def test_eliminar_citas_por_medico(self, gestor_citas):
        gestor_citas.crear_cita("C1", "P1", "M1", "2026-03-30", "08:30")
        gestor_citas.crear_cita("C2", "P2", "M1", "2026-03-31", "09:00")
        gestor_citas.crear_cita("C3", "P1", "M2", "2026-04-01", "10:00")

        gestor_citas.eliminar_citas_por_medico("M1")

        ids_restantes = {c.id_cita for c in gestor_citas.listar_citas()}
        assert ids_restantes == {"C3"}

    def test_eliminar_citas_por_medico_persiste_en_archivo(self, gestor_citas, archivo_citas):
        gestor_citas.crear_cita("C1", "P1", "M1", "2026-03-30", "08:30")
        gestor_citas.crear_cita("C2", "P1", "M2", "2026-03-31", "09:00")

        gestor_citas.eliminar_citas_por_medico("M1")

        with open(archivo_citas, "r", encoding="utf-8") as f:
            datos_guardados = json.load(f)

        assert "C1" not in datos_guardados
        assert "C2" in datos_guardados
