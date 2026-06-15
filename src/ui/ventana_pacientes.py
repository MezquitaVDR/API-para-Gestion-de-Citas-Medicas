import tkinter as tk
from tkinter import ttk, messagebox

from src.core.pacientes import GestorPacientes
from src.core.medicos import GestorMedicos
from src.core.citas import GestorCitas
from src.utils.utils import obtener_texto_no_vacio, obtener_entero_positivo

class VentanaPacientes:
    def __init__(self, root: tk.Tk, gestor_pacientes: GestorPacientes,
                 gestor_medicos: GestorMedicos, gestor_citas: GestorCitas):
        self.root = root
        self.gestor_pacientes = gestor_pacientes
        self.gestor_medicos = gestor_medicos
        self.gestor_citas = gestor_citas

        self.ventana = tk.Toplevel(self.root)
        self.ventana.title("Gestión de Pacientes")
        self.ventana.geometry("850x500")
        self.ventana.minsize(600, 400)

        # Contenedor principal con padding
        main_frame = ttk.Frame(self.ventana, padding="20 20 20 20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        lbl_titulo = ttk.Label(main_frame, text="Directorio de Pacientes", font=("Helvetica", 16, "bold"))
        lbl_titulo.pack(anchor=tk.W, pady=(0, 15))

        # Tabla de pacientes (Treeview) en lugar de Listbox
        columnas = ("id", "nombre", "edad", "telefono")
        self.tree = ttk.Treeview(main_frame, columns=columnas, show="headings", height=15)
        
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("edad", text="Edad")
        self.tree.heading("telefono", text="Teléfono")

        self.tree.column("id", width=80, anchor=tk.CENTER)
        self.tree.column("nombre", width=300)
        self.tree.column("edad", width=80, anchor=tk.CENTER)
        self.tree.column("telefono", width=150, anchor=tk.CENTER)

        # Scrollbar para la tabla
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Panel de Botones
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(15, 0))

        ttk.Button(btn_frame, text="➕ Agregar Paciente", command=self._agregar_paciente).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="✏️ Editar", command=self._editar_paciente).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="❌ Eliminar", command=self._eliminar_paciente).pack(side=tk.LEFT)

        self._actualizar_lista()

    def _actualizar_lista(self):
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Llenar tabla
        for paciente in self.gestor_pacientes.listar_pacientes():
            self.tree.insert("", tk.END, values=(
                paciente.id_paciente, 
                paciente.nombre, 
                paciente.edad, 
                paciente.telefono
            ))

    def _agregar_paciente(self):
        formulario = tk.Toplevel(self.ventana)
        formulario.title("Agregar Nuevo Paciente")
        formulario.geometry("350x300")
        formulario.resizable(False, False)
        
        frame = ttk.Frame(formulario, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="ID del Paciente:").pack(anchor=tk.W, pady=(0, 5))
        entry_id = ttk.Entry(frame, width=40)
        entry_id.pack(pady=(0, 10))

        ttk.Label(frame, text="Nombre Completo:").pack(anchor=tk.W, pady=(0, 5))
        entry_nombre = ttk.Entry(frame, width=40)
        entry_nombre.pack(pady=(0, 10))

        ttk.Label(frame, text="Edad:").pack(anchor=tk.W, pady=(0, 5))
        entry_edad = ttk.Entry(frame, width=40)
        entry_edad.pack(pady=(0, 10))

        ttk.Label(frame, text="Teléfono:").pack(anchor=tk.W, pady=(0, 5))
        entry_telefono = ttk.Entry(frame, width=40)
        entry_telefono.pack(pady=(0, 15))

        def guardar():
            id_paciente = obtener_texto_no_vacio(entry_id)
            nombre = obtener_texto_no_vacio(entry_nombre)
            edad = obtener_entero_positivo(entry_edad)
            telefono = obtener_texto_no_vacio(entry_telefono)

            if not all([id_paciente, nombre, edad, telefono]):
                return

            if self.gestor_pacientes.crear_paciente(id_paciente, nombre, edad, telefono):
                messagebox.showinfo("Éxito", "Paciente agregado correctamente.", parent=formulario)
                self._actualizar_lista()
                formulario.destroy()
            else:
                messagebox.showerror("Error", "Ya existe un paciente con ese ID.", parent=formulario)

        ttk.Button(frame, text="Guardar Paciente", command=guardar).pack(fill=tk.X)

    def _editar_paciente(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un paciente de la tabla para editar.", parent=self.ventana)
            return

        # Obtener valores de la fila seleccionada
        item = self.tree.item(seleccion[0])
        id_paciente = str(item['values'][0])
        paciente = self.gestor_pacientes.obtener_paciente(id_paciente)

        formulario = tk.Toplevel(self.ventana)
        formulario.title(f"Editar Paciente: {paciente.nombre}")
        formulario.geometry("350x250")
        formulario.resizable(False, False)
        
        frame = ttk.Frame(formulario, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Nombre Completo:").pack(anchor=tk.W, pady=(0, 5))
        entry_nombre = ttk.Entry(frame, width=40)
        entry_nombre.insert(0, paciente.nombre)
        entry_nombre.pack(pady=(0, 10))

        ttk.Label(frame, text="Edad:").pack(anchor=tk.W, pady=(0, 5))
        entry_edad = ttk.Entry(frame, width=40)
        entry_edad.insert(0, str(paciente.edad))
        entry_edad.pack(pady=(0, 10))

        ttk.Label(frame, text="Teléfono:").pack(anchor=tk.W, pady=(0, 5))
        entry_telefono = ttk.Entry(frame, width=40)
        entry_telefono.insert(0, paciente.telefono)
        entry_telefono.pack(pady=(0, 15))

        def guardar():
            nombre = obtener_texto_no_vacio(entry_nombre)
            edad = obtener_entero_positivo(entry_edad)
            telefono = obtener_texto_no_vacio(entry_telefono)

            if not all([nombre, edad, telefono]):
                return

            if self.gestor_pacientes.actualizar_paciente(id_paciente, nombre, edad, telefono):
                messagebox.showinfo("Éxito", "Paciente actualizado correctamente.", parent=formulario)
                self._actualizar_lista()
                formulario.destroy()
            else:
                messagebox.showerror("Error", "No se pudo actualizar el paciente.", parent=formulario)

        ttk.Button(frame, text="Guardar Cambios", command=guardar).pack(fill=tk.X)

    def _eliminar_paciente(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un paciente de la tabla para eliminar.", parent=self.ventana)
            return

        item = self.tree.item(seleccion[0])
        id_paciente = str(item['values'][0])
        nombre_paciente = item['values'][1]

        if messagebox.askyesno("Confirmar Eliminación", f"¿Seguro que desea eliminar al paciente '{nombre_paciente}' y todas sus citas?", parent=self.ventana):
            self.gestor_pacientes.eliminar_paciente(id_paciente)
            self.gestor_citas.eliminar_citas_por_paciente(id_paciente)
            messagebox.showinfo("Éxito", "Paciente eliminado correctamente.", parent=self.ventana)
            self._actualizar_lista()