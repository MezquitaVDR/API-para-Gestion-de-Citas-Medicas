from dataclasses import dataclass

from pacientes import GestorPacientes
from medicos import GestorMedicos


@dataclass
class Cita:
    id_cita: str
    id_paciente: str
    id_medico: str
    fecha: str
    hora: str


class GestorCitas:
    def __init__(self, gestor_pacientes: GestorPacientes, gestor_medicos: GestorMedicos):
        self.citas: dict[str, Cita] = {}
        self.gestor_pacientes = gestor_pacientes
        self.gestor_medicos = gestor_medicos

    def existe_conflicto_horario(self, id_medico: str, fecha: str, hora: str, excluir_id: str | None = None) -> bool:
        for cita in self.citas.values():
            if excluir_id and cita.id_cita == excluir_id:
                continue
            if cita.id_medico == id_medico and cita.fecha == fecha and cita.hora == hora:
                return True
        return False

    def crear_cita(self, id_cita: str, id_paciente: str, id_medico: str, fecha: str, hora: str) -> tuple[bool, str]:
        if id_cita in self.citas:
            return False, "Ya existe una cita con ese ID."
        if not self.gestor_pacientes.obtener_paciente(id_paciente):
            return False, "El paciente no existe."
        if not self.gestor_medicos.obtener_medico(id_medico):
            return False, "El médico no existe."
        if self.existe_conflicto_horario(id_medico, fecha, hora):
            return False, "El médico ya tiene una cita asignada en esa fecha y hora."

        self.citas[id_cita] = Cita(id_cita, id_paciente, id_medico, fecha, hora)
        return True, "Cita creada correctamente."

    def listar_citas(self) -> list[Cita]:
        return list(self.citas.values())

    def obtener_cita(self, id_cita: str) -> Cita | None:
        return self.citas.get(id_cita)

    def actualizar_cita(self, id_cita: str, id_paciente: str, id_medico: str, fecha: str, hora: str) -> tuple[bool, str]:
        cita = self.obtener_cita(id_cita)
        if not cita:
            return False, "La cita no existe."
        if not self.gestor_pacientes.obtener_paciente(id_paciente):
            return False, "El paciente no existe."
        if not self.gestor_medicos.obtener_medico(id_medico):
            return False, "El médico no existe."
        if self.existe_conflicto_horario(id_medico, fecha, hora, excluir_id=id_cita):
            return False, "El médico ya tiene una cita asignada en esa fecha y hora."

        cita.id_paciente = id_paciente
        cita.id_medico = id_medico
        cita.fecha = fecha
        cita.hora = hora
        return True, "Cita actualizada correctamente."

    def eliminar_cita(self, id_cita: str) -> bool:
        if id_cita not in self.citas:
            return False
        del self.citas[id_cita]
        return True

    def eliminar_citas_por_paciente(self, id_paciente: str):
        ids = [cita.id_cita for cita in self.citas.values() if cita.id_paciente == id_paciente]
        for id_cita in ids:
            del self.citas[id_cita]

    def eliminar_citas_por_medico(self, id_medico: str):
        ids = [cita.id_cita for cita in self.citas.values() if cita.id_medico == id_medico]
        for id_cita in ids:
            del self.citas[id_cita]
