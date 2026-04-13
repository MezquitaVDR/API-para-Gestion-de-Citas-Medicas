from pacientes import GestorPacientes
from medicos import GestorMedicos
from citas import GestorCitas
from utils import pedir_entero, pedir_fecha, pedir_hora, pedir_opcion, pedir_texto


class SistemaCitasMedicas:
    def __init__(self):
        self.gestor_pacientes = GestorPacientes()
        self.gestor_medicos = GestorMedicos()
        self.gestor_citas = GestorCitas(self.gestor_pacientes, self.gestor_medicos)
        self._cargar_datos_demo()

    def _cargar_datos_demo(self):
        self.gestor_pacientes.crear_paciente("P1", "María López", 28, "7777-1234")
        self.gestor_pacientes.crear_paciente("P2", "Carlos Gómez", 35, "7888-5678")
        self.gestor_medicos.crear_medico("M1", "Dra. Hernández", "Pediatría")
        self.gestor_medicos.crear_medico("M2", "Dr. Martínez", "Dermatología")
        self.gestor_citas.crear_cita("C1", "P1", "M2", "2025-04-10", "09:55")

    def ejecutar(self):
        while True:
            try:
                print("\n=== API para Gestión de Citas Médicas ===")
                print("1. Módulo de Pacientes")
                print("2. Módulo de Médicos")
                print("3. Módulo de Citas")
                print("4. Salir")
                opcion = pedir_opcion("Seleccione una opción: ", ["1", "2", "3", "4"])

                if opcion == "1":
                    self.menu_pacientes()
                elif opcion == "2":
                    self.menu_medicos()
                elif opcion == "3":
                    self.menu_citas()
                elif opcion == "4":
                    print("Saliendo del sistema...")
                    break
            except KeyboardInterrupt:
                print("\nOperación cancelada por el usuario.")
            except Exception as e:
                print(f"Ocurrió un error inesperado: {e}")

    def menu_pacientes(self):
        while True:
            print("\n--- Módulo de Pacientes ---")
            print("1. Crear paciente")
            print("2. Listar pacientes")
            print("3. Actualizar paciente")
            print("4. Eliminar paciente")
            print("5. Volver")
            opcion = pedir_opcion("Seleccione una opción: ", ["1", "2", "3", "4", "5"])

            if opcion == "1":
                self.crear_paciente()
            elif opcion == "2":
                self.listar_pacientes()
            elif opcion == "3":
                self.actualizar_paciente()
            elif opcion == "4":
                self.eliminar_paciente()
            else:
                break

    def menu_medicos(self):
        while True:
            print("\n--- Módulo de Médicos ---")
            print("1. Crear médico")
            print("2. Listar médicos")
            print("3. Actualizar médico")
            print("4. Eliminar médico")
            print("5. Volver")
            opcion = pedir_opcion("Seleccione una opción: ", ["1", "2", "3", "4", "5"])

            if opcion == "1":
                self.crear_medico()
            elif opcion == "2":
                self.listar_medicos()
            elif opcion == "3":
                self.actualizar_medico()
            elif opcion == "4":
                self.eliminar_medico()
            else:
                break

    def menu_citas(self):
        while True:
            print("\n--- Módulo de Citas ---")
            print("1. Crear cita")
            print("2. Listar citas")
            print("3. Actualizar cita")
            print("4. Eliminar cita")
            print("5. Volver")
            opcion = pedir_opcion("Seleccione una opción: ", ["1", "2", "3", "4", "5"])

            if opcion == "1":
                self.crear_cita()
            elif opcion == "2":
                self.listar_citas()
            elif opcion == "3":
                self.actualizar_cita()
            elif opcion == "4":
                self.eliminar_cita()
            else:
                break

    def crear_paciente(self):
        print("\nCrear paciente")
        id_paciente = pedir_texto("ID: ")
        nombre = pedir_texto("Nombre: ")
        edad = pedir_entero("Edad: ")
        telefono = pedir_texto("Teléfono: ")

        if self.gestor_pacientes.crear_paciente(id_paciente, nombre, edad, telefono):
            print("Paciente creado correctamente.")
        else:
            print("Error: ya existe un paciente con ese ID.")

    def listar_pacientes(self):
        pacientes = self.gestor_pacientes.listar_pacientes()
        if not pacientes:
            print("No hay pacientes registrados.")
            return

        print("\nLista de pacientes:")
        for paciente in pacientes:
            print(f"ID: {paciente.id_paciente} | Nombre: {paciente.nombre} | Edad: {paciente.edad} | Tel: {paciente.telefono}")

    def actualizar_paciente(self):
        print("\nActualizar paciente")
        id_paciente = pedir_texto("Ingrese el ID del paciente a actualizar: ")
        paciente = self.gestor_pacientes.obtener_paciente(id_paciente)
        if not paciente:
            print("Error: el paciente no existe.")
            return

        nombre = pedir_texto(f"Nuevo nombre ({paciente.nombre}): ")
        edad = pedir_entero(f"Nueva edad ({paciente.edad}): ")
        telefono = pedir_texto(f"Nuevo teléfono ({paciente.telefono}): ")

        if self.gestor_pacientes.actualizar_paciente(id_paciente, nombre, edad, telefono):
            print("Paciente actualizado correctamente.")
        else:
            print("No se pudo actualizar el paciente.")

    def eliminar_paciente(self):
        print("\nEliminar paciente")
        id_paciente = pedir_texto("Ingrese el ID del paciente a eliminar: ")
        if self.gestor_pacientes.eliminar_paciente(id_paciente):
            self.gestor_citas.eliminar_citas_por_paciente(id_paciente)
            print("Paciente eliminado correctamente. Sus citas asociadas también fueron eliminadas.")
        else:
            print("Error: el paciente no existe.")

    def crear_medico(self):
        print("\nCrear médico")
        id_medico = pedir_texto("ID: ")
        nombre = pedir_texto("Nombre: ")
        especialidad = pedir_texto("Especialidad: ")

        if self.gestor_medicos.crear_medico(id_medico, nombre, especialidad):
            print("Médico creado correctamente.")
        else:
            print("Error: ya existe un médico con ese ID.")

    def listar_medicos(self):
        medicos = self.gestor_medicos.listar_medicos()
        if not medicos:
            print("No hay médicos registrados.")
            return

        print("\nLista de médicos:")
        for medico in medicos:
            print(f"ID: {medico.id_medico} | Nombre: {medico.nombre} | Especialidad: {medico.especialidad}")

    def actualizar_medico(self):
        print("\nActualizar médico")
        id_medico = pedir_texto("Ingrese el ID del médico a actualizar: ")
        medico = self.gestor_medicos.obtener_medico(id_medico)
        if not medico:
            print("Error: el médico no existe.")
            return

        nombre = pedir_texto(f"Nuevo nombre ({medico.nombre}): ")
        especialidad = pedir_texto(f"Nueva especialidad ({medico.especialidad}): ")

        if self.gestor_medicos.actualizar_medico(id_medico, nombre, especialidad):
            print("Médico actualizado correctamente.")
        else:
            print("No se pudo actualizar el médico.")

    def eliminar_medico(self):
        print("\nEliminar médico")
        id_medico = pedir_texto("Ingrese el ID del médico a eliminar: ")
        if self.gestor_medicos.eliminar_medico(id_medico):
            self.gestor_citas.eliminar_citas_por_medico(id_medico)
            print("Médico eliminado correctamente. Sus citas asociadas también fueron eliminadas.")
        else:
            print("Error: el médico no existe.")

    def crear_cita(self):
        print("\nCrear cita")
        id_cita = pedir_texto("ID de la cita: ")
        id_paciente = pedir_texto("ID del paciente: ")
        id_medico = pedir_texto("ID del médico: ")
        fecha = pedir_fecha("Fecha (YYYY-MM-DD): ")
        hora = pedir_hora("Hora (HH:MM): ")

        exito, mensaje = self.gestor_citas.crear_cita(id_cita, id_paciente, id_medico, fecha, hora)
        print(mensaje)

    def listar_citas(self):
        citas = self.gestor_citas.listar_citas()
        if not citas:
            print("No hay citas registradas.")
            return

        print("\nLista de citas:")
        for cita in citas:
            paciente = self.gestor_pacientes.obtener_paciente(cita.id_paciente)
            medico = self.gestor_medicos.obtener_medico(cita.id_medico)
            nombre_paciente = paciente.nombre if paciente else "Desconocido"
            nombre_medico = medico.nombre if medico else "Desconocido"
            print(
                f"ID: {cita.id_cita} | Paciente: {nombre_paciente} ({cita.id_paciente}) | "
                f"Médico: {nombre_medico} ({cita.id_medico}) | Fecha: {cita.fecha} | Hora: {cita.hora}"
            )

    def actualizar_cita(self):
        print("\nActualizar cita")
        id_cita = pedir_texto("Ingrese el ID de la cita a actualizar: ")
        cita = self.gestor_citas.obtener_cita(id_cita)
        if not cita:
            print("Error: la cita no existe.")
            return

        id_paciente = pedir_texto(f"Nuevo ID de paciente ({cita.id_paciente}): ")
        id_medico = pedir_texto(f"Nuevo ID de médico ({cita.id_medico}): ")
        fecha = pedir_fecha(f"Nueva fecha ({cita.fecha}) [formato YYYY-MM-DD]: ")
        hora = pedir_hora(f"Nueva hora ({cita.hora}) [formato HH:MM]: ")

        exito, mensaje = self.gestor_citas.actualizar_cita(id_cita, id_paciente, id_medico, fecha, hora)
        print(mensaje)

    def eliminar_cita(self):
        print("\nEliminar cita")
        id_cita = pedir_texto("Ingrese el ID de la cita a eliminar: ")
        if self.gestor_citas.eliminar_cita(id_cita):
            print("Cita eliminada correctamente.")
        else:
            print("Error: la cita no existe.")


if __name__ == "__main__":
    sistema = SistemaCitasMedicas()
    sistema.ejecutar()
