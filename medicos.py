from dataclasses import dataclass


@dataclass
class Medico:
    id_medico: str
    nombre: str
    especialidad: str


class GestorMedicos:
    def __init__(self):
        self.medicos: dict[str, Medico] = {}

    def crear_medico(self, id_medico: str, nombre: str, especialidad: str) -> bool:
        if id_medico in self.medicos:
            return False
        self.medicos[id_medico] = Medico(id_medico, nombre, especialidad)
        return True

    def listar_medicos(self) -> list[Medico]:
        return list(self.medicos.values())

    def obtener_medico(self, id_medico: str) -> Medico | None:
        return self.medicos.get(id_medico)

    def actualizar_medico(self, id_medico: str, nombre: str, especialidad: str) -> bool:
        medico = self.obtener_medico(id_medico)
        if not medico:
            return False
        medico.nombre = nombre
        medico.especialidad = especialidad
        return True

    def eliminar_medico(self, id_medico: str) -> bool:
        if id_medico not in self.medicos:
            return False
        del self.medicos[id_medico]
        return True
