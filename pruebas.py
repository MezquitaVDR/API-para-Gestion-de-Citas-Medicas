from pacientes import GestorPacientes
from medicos import GestorMedicos
from citas import GestorCitas



def ejecutar_pruebas_basicas() -> None:
    pacientes = GestorPacientes()
    medicos = GestorMedicos()
    citas = GestorCitas(pacientes, medicos)

    assert pacientes.crear_paciente("P1", "Ana López", 30, "7777-1111") is True
    assert pacientes.crear_paciente("P1", "Ana López", 30, "7777-1111") is False

    assert medicos.crear_medico("M1", "Dr. Pérez", "Cardiología") is True
    assert medicos.crear_medico("M1", "Dr. Pérez", "Cardiología") is False

    exito, _ = citas.crear_cita("C1", "P1", "M1", "2026-03-25", "09:00")
    assert exito is True

    exito, mensaje = citas.crear_cita("C2", "P1", "M1", "2026-03-25", "09:00")
    assert exito is False
    assert "ya tiene una cita" in mensaje.lower()

    exito, _ = citas.actualizar_cita("C1", "P1", "M1", "2026-03-25", "10:00")
    assert exito is True

    assert citas.eliminar_cita("C1") is True
    assert citas.eliminar_cita("C1") is False

    print("Todas las pruebas básicas pasaron correctamente.")


if __name__ == "__main__":
    ejecutar_pruebas_basicas()
