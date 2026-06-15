import json
import os
from dataclasses import dataclass, asdict

@dataclass
class Medico:
    id_medico: str
    nombre: str
    especialidad: str


class GestorMedicos:
    def __init__(self, archivo_datos="medicos.json"):
        self.archivo_datos = archivo_datos
        self.medicos: dict[str, Medico] = self._cargar_datos()

    def _cargar_datos(self) -> dict[str, Medico]:
        if not os.path.exists(self.archivo_datos):
            return {}
        with open(self.archivo_datos, "r", encoding="utf-8") as archivo:
            datos_json = json.load(archivo)
            return {id_medico: Medico(**info) for id_medico, info in datos_json.items()}

    def _guardar_datos(self):
        with open(self.archivo_datos, "w", encoding="utf-8") as archivo:
            datos_a_guardar = {id_med: asdict(medico) for id_med, medico in self.medicos.items()}
            json.dump(datos_a_guardar, archivo, indent=4, ensure_ascii=False)

    def crear_medico(self, id_medico: str, nombre: str, especialidad: str) -> bool:
        if id_medico in self.medicos:
            return False
        self.medicos[id_medico] = Medico(id_medico, nombre, especialidad)
        self._guardar_datos()
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
        self._guardar_datos()
        return True

    def eliminar_medico(self, id_medico: str) -> bool:
        if id_medico not in self.medicos:
            return False
        del self.medicos[id_medico]
        self._guardar_datos()
        return True