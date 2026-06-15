import tkinter as tk
from tkinter import ttk, messagebox

from src.core.citas import GestorCitas
from src.core.medicos import GestorMedicos
from src.core.pacientes import GestorPacientes


class VentanaPrincipal:
    def __init__(self, root, gestor_pacientes, gestor_medicos, gestor_citas):
        self.root = root
        self.gestor_pacientes = gestor_pacientes
        self.gestor_medicos = gestor_medicos
        self.gestor_citas = gestor_citas

        self.root.title("Doctor Citas - Sistema de Gestión de Citas Médicas")
        self.root.geometry("850x650")
        self.root.minsize(700, 500)
        self.root.configure(bg="#F8F9FA")  # Un gris muy claro, más moderno que el blanco puro

        self._configurar_estilos()
        self.construir_ui()

    def _configurar_estilos(self):
        """Define los estilos visuales para los componentes ttk"""
        estilo = ttk.Style()
        estilo.theme_use("clam")  # Un tema base más limpio y plano
        
        # Estilo para los botones principales del menú
        estilo.configure(
            "Menu.TButton",
            font=("Segoe UI", 12, "bold"),
            padding=15,
            width=25,
            background="#FFFFFF",
            foreground="#1E3A8A"
        )
        # Efecto al pasar el mouse por encima (hover)
        estilo.map("Menu.TButton", background=[("active", "#E2E8F0")])
        
        # Estilo para el botón de salir
        estilo.configure(
            "Salir.TButton",
            font=("Segoe UI", 11, "bold"),
            padding=10,
            width=25,
            background="#FEE2E2",
            foreground="#991B1B"
        )
        estilo.map("Salir.TButton", background=[("active", "#FECACA")])

    def construir_ui(self):
        # Intentar cargar el logo
        try:
            import requests
            from io import BytesIO
            from PIL import Image, ImageTk

            url_logo = "https://raw.githubusercontent.com/MezquitaVDR/API-para-Gestion-de-Citas-Medicas/master/Diseno%20UXIU/Logotipo.png"
            respuesta = requests.get(url_logo, timeout=5)
            respuesta.raise_for_status()
            img_data = Image.open(BytesIO(respuesta.content))
            img_data = img_data.resize((250, 125), Image.LANCZOS)
            logo_img = ImageTk.PhotoImage(img_data)
            
            label_logo = tk.Label(self.root, image=logo_img, bg="#F8F9FA")
            label_logo.image = logo_img
            label_logo.pack(pady=(40, 10))

        except Exception as e:
            print(f"No se pudo cargar el logo: {e}")
            # Fallback en caso de que no haya internet
            tk.Label(self.root, text="🏥", font=("Arial", 50), bg="#F8F9FA", fg="#1E3A8A").pack(pady=(40, 0))

        # Contenedor central
        frame = tk.Frame(self.root, bg="#F8F9FA")
        frame.pack(expand=True)

        tk.Label(frame, text="Bienvenido al Panel de Control",
                 font=("Segoe UI", 16, "bold"), fg="#1E3A8A", bg="#F8F9FA").pack(pady=(0, 25))

        # Botones con Íconos (Unicode) y Estilo
        ttk.Button(frame, text="👥  Gestión de Pacientes", style="Menu.TButton",
                   command=self.abrir_ventana_pacientes).pack(pady=10)
                   
        ttk.Button(frame, text="🩺  Personal Médico", style="Menu.TButton",
                   command=self.abrir_ventana_medicos).pack(pady=10)
                   
        ttk.Button(frame, text="📅  Agenda de Citas", style="Menu.TButton",
                   command=self.abrir_ventana_citas).pack(pady=10)
                   
        # Separador visual antes de salir
        ttk.Separator(frame, orient="horizontal").pack(fill=tk.X, pady=20)
        
        ttk.Button(frame, text="🚪  Salir del Sistema", style="Salir.TButton",
                   command=self.salir).pack(pady=10)

    def abrir_ventana_pacientes(self):
        from src.ui.ventana_pacientes import VentanaPacientes
        VentanaPacientes(self.root, self.gestor_pacientes, self.gestor_medicos, self.gestor_citas)

    def abrir_ventana_medicos(self):
        from src.ui.ventana_medicos import VentanaMedicos
        VentanaMedicos(self.root, self.gestor_pacientes, self.gestor_medicos, self.gestor_citas)

    def abrir_ventana_citas(self):
        from src.ui.ventana_citas import VentanaCitas
        VentanaCitas(self.root, self.gestor_pacientes, self.gestor_medicos, self.gestor_citas)

    def salir(self):
        if messagebox.askokcancel("Salir", "¿Estás seguro de que quieres cerrar la aplicación?"):
            self.root.destroy()