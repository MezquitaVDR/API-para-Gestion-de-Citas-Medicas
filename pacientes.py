from dataclasses import dataclass


@dataclass
class Paciente:
    id_paciente: str
    nombre: str
    edad: int
    telefono: str


class GestorPacientes:
    def __init__(self):
        self.pacientes: dict[str, Paciente] = {}

    def crear_paciente(self, id_paciente: str, nombre: str, edad: int, telefono: str) -> bool:
        if id_paciente in self.pacientes:
            return False
        self.pacientes[id_paciente] = Paciente(id_paciente, nombre, edad, telefono)
        return True

    def listar_pacientes(self) -> list[Paciente]:
        return list(self.pacientes.values())

    def obtener_paciente(self, id_paciente: str) -> Paciente | None:
        return self.pacientes.get(id_paciente)

    def actualizar_paciente(self, id_paciente: str, nombre: str, edad: int, telefono: str) -> bool:
        paciente = self.obtener_paciente(id_paciente)
        if not paciente:
            return False
        paciente.nombre = nombre
        paciente.edad = edad
        paciente.telefono = telefono
        return True

    def eliminar_paciente(self, id_paciente: str) -> bool:
        if id_paciente not in self.pacientes:
            return False
        del self.pacientes[id_paciente]
        return True
