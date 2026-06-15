import tkinter as tk
from tkinter import ttk, messagebox

from src.core.pacientes import GestorPacientes
from src.core.medicos import GestorMedicos
from src.core.citas import GestorCitas
from src.utils.utils import obtener_texto_no_vacio


class VentanaMedicos:
    # Lista de especialidades médicas predefinidas para los desplegables
    ESPECIALIDADES = [
        "Medicina General",
        "Pediatría",
        "Cardiología",
        "Dermatología",
        "Ginecología",
        "Traumatología",
        "Neurología",
        "Oftalmología"
    ]

    def __init__(self, root: tk.Tk, gestor_pacientes: GestorPacientes,
                 gestor_medicos: GestorMedicos, gestor_citas: GestorCitas):
        self.gestor_pacientes = gestor_pacientes
        self.gestor_medicos = gestor_medicos
        self.gestor_citas = gestor_citas

        self.ventana = tk.Toplevel(root)
        self.ventana.title("Gestión de Médicos")
        self.ventana.geometry("850x500")
        self.ventana.minsize(600, 400)

        # Contenedor principal con espaciado
        main_frame = ttk.Frame(self.ventana, padding="20 20 20 20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título de la sección
        lbl_titulo = ttk.Label(main_frame, text="Personal Médico", font=("Helvetica", 16, "bold"))
        lbl_titulo.pack(anchor=tk.W, pady=(0, 15))

        # Tabla de médicos (Treeview) para sustituir el Listbox antiguo
        columnas = ("id", "nombre", "especialidad")
        self.tree = ttk.Treeview(main_frame, columns=columnas, show="headings", height=15)
        
        self.tree.heading("id", text="ID Médico")
        self.tree.heading("nombre", text="Nombre del Médico")
        self.tree.heading("especialidad", text="Especialidad")

        self.tree.column("id", width=100, anchor=tk.CENTER)
        self.tree.column("nombre", width=350)
        self.tree.column("especialidad", width=250)

        # Barra de desplazamiento para la tabla
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Panel de Botones Inferior
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(15, 0))

        ttk.Button(btn_frame, text="➕ Agregar Médico", command=self._agregar_medico).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="✏️ Editar", command=self._editar_medico).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="❌ Eliminar", command=self._eliminar_medico).pack(side=tk.LEFT)

        self._actualizar_lista()

    def _actualizar_lista(self):
        # Limpiar filas existentes en la tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Insertar los registros actualizados
        for medico in self.gestor_medicos.listar_medicos():
            self.tree.insert("", tk.END, values=(
                medico.id_medico,
                medico.nombre,
                medico.especialidad
            ))

    def _agregar_medico(self):
        formulario = tk.Toplevel(self.ventana)
        formulario.title("Agregar Nuevo Médico")
        formulario.geometry("350x270")
        formulario.resizable(False, False)
        
        frame = ttk.Frame(formulario, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="ID del Médico:").pack(anchor=tk.W, pady=(0, 5))
        entry_id = ttk.Entry(frame, width=40)
        entry_id.pack(pady=(0, 10))

        ttk.Label(frame, text="Nombre Completo:").pack(anchor=tk.W, pady=(0, 5))
        entry_nombre = ttk.Entry(frame, width=40)
        entry_nombre.pack(pady=(0, 10))

        ttk.Label(frame, text="Especialidad:").pack(anchor=tk.W, pady=(0, 5))
        # Uso de Combobox en vez de Entry, en modo 'readonly' para que solo elijan opciones válidas
        combo_especialidad = ttk.Combobox(frame, values=self.ESPECIALIDADES, width=37, state="readonly")
        combo_especialidad.pack(pady=(0, 20))
        combo_especialidad.set("Seleccione una opción...")  # Texto inicial descriptivo

        def guardar():
            id_medico = obtener_texto_no_vacio(entry_id)
            nombre = obtener_texto_no_vacio(entry_nombre)
            especialidad = combo_especialidad.get()

            # Validación extra para asegurar que no dejen el texto por defecto del combobox
            if especialidad == "Seleccione una opción..." or not especialidad:
                messagebox.showwarning("Advertencia", "Por favor, seleccione una especialidad válida.", parent=formulario)
                return

            if not all([id_medico, nombre]):
                return

            if self.gestor_medicos.crear_medico(id_medico, nombre, especialidad):
                messagebox.showinfo("Éxito", "Médico agregado correctamente.", parent=formulario)
                self._actualizar_lista()
                formulario.destroy()
            else:
                messagebox.showerror("Error", "Ya existe un médico con ese ID.", parent=formulario)

        ttk.Button(frame, text="Guardar Médico", command=guardar).pack(fill=tk.X)

    def _editar_medico(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un médico de la tabla para editar.", parent=self.ventana)
            return

        # Recuperar información del médico seleccionado
        item = self.tree.item(seleccion[0])
        id_medico = str(item['values'][0])
        medico = self.gestor_medicos.obtener_medico(id_medico)

        formulario = tk.Toplevel(self.ventana)
        formulario.title(f"Editar Médico: {medico.nombre}")
        formulario.geometry("350x220")
        formulario.resizable(False, False)
        
        frame = ttk.Frame(formulario, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Nombre Completo:").pack(anchor=tk.W, pady=(0, 5))
        entry_nombre = ttk.Entry(frame, width=40)
        entry_nombre.insert(0, medico.nombre)
        entry_nombre.pack(pady=(0, 10))

        ttk.Label(frame, text="Especialidad:").pack(anchor=tk.W, pady=(0, 5))
        combo_especialidad = ttk.Combobox(frame, values=self.ESPECIALIDADES, width=37, state="readonly")
        combo_especialidad.pack(pady=(0, 20))
        
        # Asignar la especialidad que el médico ya tenía registrada
        if medico.especialidad in self.ESPECIALIDADES:
            combo_especialidad.set(medico.especialidad)
        else:
            combo_especialidad.set(medico.especialidad)  # Caso de que sea una personalizada previa

        def guardar():
            nombre = obtener_texto_no_vacio(entry_nombre)
            especialidad = combo_especialidad.get()

            if not all([nombre, ...]) or not especialidad:
                return

            if self.gestor_medicos.actualizar_medico(id_medico, nombre, especialidad):
                messagebox.showinfo("Éxito", "Médico actualizado correctamente.", parent=formulario)
                self._actualizar_lista()
                formulario.destroy()
            else:
                messagebox.showerror("Error", "No se pudo actualizar el médico.", parent=formulario)

        ttk.Button(frame, text="Guardar Cambios", command=guardar).pack(fill=tk.X)

    def _eliminar_medico(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un médico de la tabla para eliminar.", parent=self.ventana)
            return

        item = self.tree.item(seleccion[0])
        id_medico = str(item['values'][0])
        nombre_medico = item['values'][1]

        if messagebox.askyesno("Confirmar Eliminación", f"¿Seguro que desea eliminar al Dr(a). '{nombre_medico}' y cancelar todas sus citas?", parent=self.ventana):
            self.gestor_medicos.eliminar_medico(id_medico)
            self.gestor_citas.eliminar_citas_por_medico(id_medico)
            messagebox.showinfo("Éxito", "Médico eliminado correctamente.", parent=self.ventana)
            self._actualizar_lista()