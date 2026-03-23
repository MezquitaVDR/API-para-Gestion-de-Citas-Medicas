def menu():
    while True:
        print("\n=== SISTEMA DE CITAS MÉDICAS ===")
        print("1. Pacientes")
        print("2. Médicos")
        print("3. Citas")
        print("4. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            print("Módulo pacientes")
        elif opcion == "2":
            print("Módulo médicos")
        elif opcion == "3":
            print("Módulo citas")
        elif opcion == "4":
            print("Saliendo...")
            break
        else:
            print("Opción inválida")

if __name__ == "__main__":
    menu()