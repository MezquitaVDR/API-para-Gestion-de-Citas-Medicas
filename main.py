# 1. Biblioteca de Nativos de Python
import tkinter as tk

# 2. Módulos locales
from src.core.citas import GestorCitas
from src.core.medicos import GestorMedicos
from src.core.pacientes import GestorPacientes
from src.ui import splash_screen
from src.ui.ventana_principal import VentanaPrincipal


def iniciar_aplicacion():
    splash = tk.Tk()
    splash_screen.crear_splash_screen(splash)
    splash.after(3000, splash.destroy)
    splash.mainloop()

    root = tk.Tk()
    gestor_pacientes = GestorPacientes()
    gestor_medicos = GestorMedicos()
    gestor_citas = GestorCitas(gestor_pacientes, gestor_medicos)

    VentanaPrincipal(root, gestor_pacientes, gestor_medicos, gestor_citas)
    root.mainloop()


if __name__ == "__main__":
    iniciar_aplicacion()