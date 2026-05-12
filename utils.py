from datetime import datetime


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



def pedir_texto(mensaje: str, permitir_vacio: bool = False) -> str:
    while True:
        valor = input(mensaje).strip()
        if valor or permitir_vacio:
            return valor
        print("Entrada inválida. No puede estar vacía.")



def pedir_entero(mensaje: str, minimo: int = 1) -> int:
    while True:
        valor = input(mensaje).strip()
        if validar_entero_positivo(valor):
            numero = int(valor)
            if numero >= minimo:
                return numero
        print(f"Entrada inválida. Debe ser un número entero mayor o igual a {minimo}.")



def pedir_opcion(mensaje: str, opciones_validas: list[str]) -> str:
    while True:
        valor = input(mensaje).strip()
        if valor in opciones_validas:
            return valor
        print("Opción inválida. Intente nuevamente.")
        print("\n=== API para Gestión de Citas Médicas ===")
        print("1. Módulo de Pacientes")
        print("2. Módulo de Médicos")
        print("3. Módulo de Citas")
        print("4. Salir")



def pedir_fecha(mensaje: str) -> str:
    while True:
        fecha = input(mensaje).strip()
        if validar_fecha(fecha):
            return fecha
        print("Fecha inválida. Use el formato YYYY-MM-DD.")



def pedir_hora(mensaje: str) -> str:
    while True:
        hora = input(mensaje).strip()
        if validar_hora(hora):
            return hora
        print("Hora inválida. Use el formato HH:MM en 24 horas.")
