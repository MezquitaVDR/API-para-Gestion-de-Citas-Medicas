import json
import os
from dataclasses import dataclass, asdict

@dataclass
class Paciente:
    id_paciente: str
    nombre: str
    edad: int
    telefono: str


class GestorPacientes:
    def __init__(self, archivo_datos="pacientes.json"):
        self.archivo_datos = archivo_datos
        self.pacientes: dict[str, Paciente] = self._cargar_datos()

    def _cargar_datos(self) -> dict[str, Paciente]:
        if not os.path.exists(self.archivo_datos):
            return {}
        with open(self.archivo_datos, "r", encoding="utf-8") as archivo:
            datos_json = json.load(archivo)
            # Reconstruimos los objetos Paciente desempacando el diccionario con **
            return {id_paciente: Paciente(**info) for id_paciente, info in datos_json.items()}

    def _guardar_datos(self):
        with open(self.archivo_datos, "w", encoding="utf-8") as archivo:
            # asdict() convierte automáticamente el dataclass a diccionario
            datos_a_guardar = {id_pac: asdict(paciente) for id_pac, paciente in self.pacientes.items()}
            json.dump(datos_a_guardar, archivo, indent=4, ensure_ascii=False)

    def crear_paciente(self, id_paciente: str, nombre: str, edad: int, telefono: str) -> bool:
        if id_paciente in self.pacientes:
            return False
        self.pacientes[id_paciente] = Paciente(id_paciente, nombre, edad, telefono)
        self._guardar_datos()
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
        self._guardar_datos()
        return True

    def eliminar_paciente(self, id_paciente: str) -> bool:
        if id_paciente not in self.pacientes:
            return False
        del self.pacientes[id_paciente]
        self._guardar_datos()
        return True