from datetime import datetime
from tkinter import messagebox
import tkinter as tk


def validar_entero_positivo(valor: str) -> bool:
    try:
        return int(valor) > 0
    except (TypeError, ValueError):
        return False

def validar_id_no_vacio(valor: str) -> bool:
    return isinstance(valor, str) and valor.strip() != ""


def validar_fecha(fecha: str) -> bool:
    try:
        datetime.strptime(fecha, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validar_hora(hora: str) -> bool:
    try:
        datetime.strptime(hora, "%H:%M")
        return True
    except ValueError:
        return False

def obtener_texto_no_vacio(entry: tk.Entry) -> str | None:
    valor = entry.get().strip()
    if validar_id_no_vacio(valor):
        return valor
    messagebox.showerror("Error", "La entrada no puede estar vacía.")
    return None

def obtener_entero_positivo(entry: tk.Entry) -> int | None:
    valor = entry.get().strip()
    if validar_entero_positivo(valor):
        return int(valor)
    messagebox.showerror("Error", "La entrada debe ser un número entero positivo.")
    return None

def obtener_fecha(entry: tk.Entry) -> str | None:
    valor = entry.get().strip()
    if validar_fecha(valor):
        return valor
    messagebox.showerror("Error", "La fecha debe tener el formato YYYY-MM-DD.")
    return None

def obtener_hora(entry: tk.Entry) -> str | None:
    valor = entry.get().strip()
    if validar_hora(valor):
        return valor
    messagebox.showerror("Error", "La hora debe tener el formato HH:MM en 24 horas.")
    return None