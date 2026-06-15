import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

from src.core.pacientes import GestorPacientes
from src.core.medicos import GestorMedicos
from src.core.citas import GestorCitas
# Eliminamos obtener_fecha y obtener_hora porque los nuevos widgets ya garantizan el formato correcto
from src.utils.utils import obtener_texto_no_vacio


class VentanaCitas:
    def __init__(self, root: tk.Tk, gestor_pacientes: GestorPacientes,
                 gestor_medicos: GestorMedicos, gestor_citas: GestorCitas):
        self.gestor_pacientes = gestor_pacientes
        self.gestor_medicos = gestor_medicos
        self.gestor_citas = gestor_citas

        self.ventana = tk.Toplevel(root)
        self.ventana.title("Gestión de Citas")
        self.ventana.geometry("900x550")
        self.ventana.minsize(700, 450)

        main_frame = ttk.Frame(self.ventana, padding="20 20 20 20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        lbl_titulo = ttk.Label(main_frame, text="Agenda de Citas Médicas", font=("Helvetica", 16, "bold"))
        lbl_titulo.pack(anchor=tk.W, pady=(0, 15))

        columnas = ("id_cita", "paciente", "medico", "fecha", "hora")
        self.tree = ttk.Treeview(main_frame, columns=columnas, show="headings", height=15)
        
        self.tree.heading("id_cita", text="ID Cita")
        self.tree.heading("paciente", text="Paciente")
        self.tree.heading("medico", text="Médico")
        self.tree.heading("fecha", text="Fecha")
        self.tree.heading("hora", text="Hora")

        self.tree.column("id_cita", width=80, anchor=tk.CENTER)
        self.tree.column("paciente", width=250)
        self.tree.column("medico", width=250)
        self.tree.column("fecha", width=120, anchor=tk.CENTER)
        self.tree.column("hora", width=100, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)

        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(15, 0))

        ttk.Button(btn_frame, text="➕ Agendar Cita", command=self._agregar_cita).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="✏️ Reprogramar", command=self._editar_cita).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="❌ Cancelar Cita", command=self._eliminar_cita).pack(side=tk.LEFT)

        self._actualizar_lista()

    def _actualizar_lista(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        for cita in self.gestor_citas.listar_citas():
            paciente = self.gestor_pacientes.obtener_paciente(cita.id_paciente)
            medico = self.gestor_medicos.obtener_medico(cita.id_medico)
            
            nombre_paciente = paciente.nombre if paciente else f"ID: {cita.id_paciente}"
            nombre_medico = medico.nombre if medico else f"ID: {cita.id_medico}"
            
            self.tree.insert("", tk.END, values=(
                cita.id_cita,
                nombre_paciente,
                nombre_medico,
                cita.fecha,
                cita.hora
            ))

    def _crear_selectores_tiempo(self, parent):
        frame_tiempo = ttk.Frame(parent)
        horas = [f"{i:02d}" for i in range(8, 20)]
        minutos = ["00", "15", "30", "45"]
        
        combo_hora = ttk.Combobox(frame_tiempo, values=horas, width=5, state="readonly")
        combo_hora.set("08")
        combo_hora.pack(side=tk.LEFT)
        
        ttk.Label(frame_tiempo, text=":").pack(side=tk.LEFT, padx=2)
        
        combo_minuto = ttk.Combobox(frame_tiempo, values=minutos, width=5, state="readonly")
        combo_minuto.set("00")
        combo_minuto.pack(side=tk.LEFT)
        
        return frame_tiempo, combo_hora, combo_minuto

    def _agregar_cita(self):
        # 1. Obtener las listas de pacientes y médicos para el Combobox
        pacientes_opciones = [f"{p.id_paciente} - {p.nombre}" for p in self.gestor_pacientes.listar_pacientes()]
        medicos_opciones = [f"{m.id_medico} - {m.nombre}" for m in self.gestor_medicos.listar_medicos()]

        if not pacientes_opciones or not medicos_opciones:
            messagebox.showwarning("Advertencia", "Debe registrar al menos un paciente y un médico antes de agendar citas.", parent=self.ventana)
            return

        formulario = tk.Toplevel(self.ventana)
        formulario.title("Agendar Nueva Cita")
        formulario.geometry("350x380")
        formulario.resizable(False, False)
        
        frame = ttk.Frame(formulario, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="ID de la Cita:").pack(anchor=tk.W, pady=(0, 2))
        entry_id = ttk.Entry(frame, width=40)
        entry_id.pack(pady=(0, 10))

        # 2. Selector de Pacientes
        ttk.Label(frame, text="Seleccione Paciente:").pack(anchor=tk.W, pady=(0, 2))
        combo_paciente = ttk.Combobox(frame, values=pacientes_opciones, width=37, state="readonly")
        combo_paciente.pack(pady=(0, 10))
        combo_paciente.set("Seleccione un paciente...")

        # 3. Selector de Médicos
        ttk.Label(frame, text="Seleccione Médico:").pack(anchor=tk.W, pady=(0, 2))
        combo_medico = ttk.Combobox(frame, values=medicos_opciones, width=37, state="readonly")
        combo_medico.pack(pady=(0, 10))
        combo_medico.set("Seleccione un médico...")

        ttk.Label(frame, text="Fecha de la Cita:").pack(anchor=tk.W, pady=(0, 2))
        cal_fecha = DateEntry(frame, width=37, background='darkblue', 
                              foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        cal_fecha.pack(pady=(0, 10))

        ttk.Label(frame, text="Hora:").pack(anchor=tk.W, pady=(0, 2))
        frame_tiempo, combo_hora, combo_minuto = self._crear_selectores_tiempo(frame)
        frame_tiempo.pack(anchor=tk.W, pady=(0, 15))

        def guardar():
            id_cita = obtener_texto_no_vacio(entry_id)
            paciente_sel = combo_paciente.get()
            medico_sel = combo_medico.get()
            
            # Validación de los Combobox
            if paciente_sel.startswith("Seleccione") or medico_sel.startswith("Seleccione"):
                messagebox.showwarning("Campos vacíos", "Por favor seleccione un paciente y un médico.", parent=formulario)
                return

            # Extraemos el ID separando el texto por " - "
            id_paciente = paciente_sel.split(" - ")[0]
            id_medico = medico_sel.split(" - ")[0]
            
            # Extraemos directamente los valores del calendario y los comboboxes de tiempo
            fecha = cal_fecha.get()
            hora = f"{combo_hora.get()}:{combo_minuto.get()}"

            if not all([id_cita, id_paciente, id_medico, fecha, hora]):
                messagebox.showwarning("Campos vacíos", "Por favor complete todos los campos.", parent=formulario)
                return

            exito, mensaje = self.gestor_citas.crear_cita(id_cita, id_paciente, id_medico, fecha, hora)
            if exito:
                messagebox.showinfo("Éxito", mensaje, parent=formulario)
                self._actualizar_lista()
                formulario.destroy()
            else:
                messagebox.showerror("Error", mensaje, parent=formulario)

        ttk.Button(frame, text="Agendar Cita", command=guardar).pack(fill=tk.X)

    def _editar_cita(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una cita de la tabla para editar.", parent=self.ventana)
            return

        item = self.tree.item(seleccion[0])
        id_cita = str(item['values'][0])
        cita = self.gestor_citas.obtener_cita(id_cita)

        pacientes_opciones = [f"{p.id_paciente} - {p.nombre}" for p in self.gestor_pacientes.listar_pacientes()]
        medicos_opciones = [f"{m.id_medico} - {m.nombre}" for m in self.gestor_medicos.listar_medicos()]

        formulario = tk.Toplevel(self.ventana)
        formulario.title(f"Reprogramar Cita: {id_cita}")
        formulario.geometry("350x320")
        formulario.resizable(False, False)
        
        frame = ttk.Frame(formulario, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Paciente:").pack(anchor=tk.W, pady=(0, 2))
        combo_paciente = ttk.Combobox(frame, values=pacientes_opciones, width=37, state="readonly")
        combo_paciente.pack(pady=(0, 10))
        # Autoseleccionar el paciente actual
        for op in pacientes_opciones:
            if op.startswith(f"{cita.id_paciente} -"):
                combo_paciente.set(op)
                break

        ttk.Label(frame, text="Médico:").pack(anchor=tk.W, pady=(0, 2))
        combo_medico = ttk.Combobox(frame, values=medicos_opciones, width=37, state="readonly")
        combo_medico.pack(pady=(0, 10))
        # Autoseleccionar el médico actual
        for op in medicos_opciones:
            if op.startswith(f"{cita.id_medico} -"):
                combo_medico.set(op)
                break

        ttk.Label(frame, text="Nueva Fecha:").pack(anchor=tk.W, pady=(0, 2))
        cal_fecha = DateEntry(frame, width=37, background='darkblue', 
                              foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        cal_fecha.set_date(cita.fecha)
        cal_fecha.pack(pady=(0, 10))

        ttk.Label(frame, text="Nueva Hora:").pack(anchor=tk.W, pady=(0, 2))
        frame_tiempo, combo_hora, combo_minuto = self._crear_selectores_tiempo(frame)
        try:
            h, m = cita.hora.split(":")
            combo_hora.set(h)
            combo_minuto.set(m)
        except ValueError:
            pass
        frame_tiempo.pack(anchor=tk.W, pady=(0, 15))

        def guardar():
            paciente_sel = combo_paciente.get()
            medico_sel = combo_medico.get()

            if paciente_sel.startswith("Seleccione") or medico_sel.startswith("Seleccione"):
                messagebox.showwarning("Campos vacíos", "Por favor seleccione un paciente y un médico.", parent=formulario)
                return

            id_paciente = paciente_sel.split(" - ")[0]
            id_medico = medico_sel.split(" - ")[0]
            
            fecha = cal_fecha.get()
            hora = f"{combo_hora.get()}:{combo_minuto.get()}"

            if not all([id_paciente, id_medico, fecha, hora]):
                messagebox.showwarning("Campos vacíos", "Por favor complete todos los campos.", parent=formulario)
                return

            exito, mensaje = self.gestor_citas.actualizar_cita(id_cita, id_paciente, id_medico, fecha, hora)
            if exito:
                messagebox.showinfo("Éxito", mensaje, parent=formulario)
                self._actualizar_lista()
                formulario.destroy()
            else:
                messagebox.showerror("Error", mensaje, parent=formulario)

        ttk.Button(frame, text="Guardar Cambios", command=guardar).pack(fill=tk.X)

    def _eliminar_cita(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una cita de la tabla para cancelar.", parent=self.ventana)
            return

        item = self.tree.item(seleccion[0])
        id_cita = str(item['values'][0])
        info_cita = f"{item['values'][3]} a las {item['values'][4]}"

        if messagebox.askyesno("Confirmar Cancelación", f"¿Seguro que desea cancelar la cita del {info_cita}?", parent=self.ventana):
            self.gestor_citas.eliminar_cita(id_cita)
            messagebox.showinfo("Éxito", "Cita cancelada correctamente.", parent=self.ventana)
            self._actualizar_lista()