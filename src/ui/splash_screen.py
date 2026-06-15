import tkinter as tk
from tkinter import ttk
from io import BytesIO
import requests
from PIL import Image, ImageTk


def crear_splash_screen(ventana):
    ancho_ventana = 800
    alto_ventana = 600
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()
    x = (ancho_pantalla // 2) - (ancho_ventana // 2)
    y = (alto_pantalla // 2) - (alto_ventana // 2)

    ventana.title("Cargando Doctor Citas...")
    ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")
    ventana.overrideredirect(True)  # Oculta los bordes de la ventana
    ventana.configure(bg="white")

    # --- CONFIGURACIÓN DE ESTILOS PARA LA BARRA ---
    estilo = ttk.Style()
    estilo.theme_use('clam')
    estilo.configure(
        "Estetica.Horizontal.TProgressbar",
        troughcolor='#F3F4F6',  # Color de fondo de la barra (gris muy claro)
        background='#1E3A8A',   # Color de la barra de progreso (azul oscuro institucional)
        bordercolor='white',
        lightcolor='#1E3A8A',
        darkcolor='#1E3A8A',
        thickness=6             # Grosor de la barra (fina y elegante)
    )

    # Frame centrado en la ventana
    frame = tk.Frame(ventana, bg="white")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    url_logo = "https://raw.githubusercontent.com/MezquitaVDR/API-para-Gestion-de-Citas-Medicas/master/Diseno%20UXIU/Logotipo.png"

    try:
        respuesta = requests.get(url_logo, timeout=5)
        respuesta.raise_for_status()
        img_data = Image.open(BytesIO(respuesta.content))
        img_data = img_data.resize((280, 140), Image.LANCZOS)
        logo_img = ImageTk.PhotoImage(img_data)
        label_logo = tk.Label(frame, image=logo_img, bg="white")
        label_logo.image = logo_img
        label_logo.pack(pady=(30, 10))

    except Exception as e:
        print(f"Error detectado al cargar la imagen: {e}")
        tk.Label(frame, text="DOCTOR CITAS", fg="#0F4C81", bg="white",
                 font=("Arial", 28, "bold")).pack(pady=(50, 10))

    tk.Label(frame, text="Sistema de Gestión de Citas Médicas",
             font=("Arial", 14, "bold"), fg="#1E3A8A", bg="white").pack(pady=10)

    # Etiqueta dinámica de estado
    label_estado = tk.Label(frame, text="Iniciando sistema...",
                            font=("Arial", 10, "italic"), fg="#6B7280", bg="white")
    label_estado.pack(pady=(15, 5))

    # Barra de progreso estética
    barra_progreso = ttk.Progressbar(
        frame, 
        style="Estetica.Horizontal.TProgressbar", 
        orient="horizontal", 
        length=400, 
        mode="determinate"
    )
    barra_progreso.pack(pady=(0, 20))

    # El pie va directo a ventana, no al frame, para que quede abajo del todo
    tk.Label(ventana, text="© Elaborado para proyecto de Lógica de Programación - Doctor Citas 2026 - Todos los derechos reservados",
             font=("Arial", 8), fg="#9CA3AF", bg="white").pack(side="bottom", pady=15)

    # --- LÓGICA DE ANIMACIÓN Y CARGA ---
    def animar_carga(progreso=0):
        if progreso <= 100:
            barra_progreso['value'] = progreso
            
            # Cambiar el texto según el progreso para dar sensación de carga real
            if progreso == 15:
                label_estado.config(text="Cargando módulos principales...")
            elif progreso == 45:
                label_estado.config(text="Conectando con la base de datos local (JSON)...")
            elif progreso == 75:
                label_estado.config(text="Renderizando interfaz de usuario...")
            elif progreso == 95:
                label_estado.config(text="¡Todo listo para iniciar!")

            # Llama a esta misma función 30 milisegundos después incrementando el progreso
            ventana.after(30, animar_carga, progreso + 1)
        else:
            # Cuando llega al 100%, se destruye el Splash Screen (aquí tu main.py debería abrir la ventana principal)
            ventana.destroy()

    # Iniciar la animación
    animar_carga()