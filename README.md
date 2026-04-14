# API para Gestión de Citas Médicas

Aplicación CLI en Python para administrar pacientes, médicos y citas médicas desde consola.

## Características

- Programación orientada a objetos
- CRUD completo de pacientes
- CRUD completo de médicos
- CRUD completo de citas
- Validación de ID duplicados
- Validación de fecha y hora
- Validación de conflicto de horarios para médicos
- Manejo de errores con try/except
- Estructura modular por archivos
- Simulación de base de datos en memoria usando diccionarios

## Estructura del proyecto

- main.py: menú principal y navegación
- pacientes.py: entidad y gestor de pacientes
- medicos.py: entidad y gestor de médicos
- citas.py: entidad y gestor de citas
- utils.py: validaciones y funciones auxiliares
- pruebas.py: pruebas básicas del sistema

## Cómo ejecutarlo

1. Abre una terminal en la carpeta del proyecto
2. Ejecuta:

bash
python main.py


## Cómo ejecutar las pruebas

bash
python pruebas.py


## Ejemplos de uso

### Crear un paciente
- ID: P3
- Nombre: Luis Torres
- Edad: 40
- Teléfono: 7999-0000

### Crear un médico
- ID: M3
- Nombre: Dra. Rivera
- Especialidad: Medicina General

### Crear una cita
- ID de cita: C1
- ID del paciente: P3
- ID del médico: M3
- Fecha: 2026-03-30
- Hora: 08:30

## Reglas de negocio aplicadas

- No permite IDs duplicados
- No permite citas con pacientes inexistentes
- No permite citas con médicos inexistentes
- No permite agendar dos citas con el mismo médico en la misma fecha y hora
- Elimina automáticamente las citas asociadas cuando se elimina un paciente o médico

## Nota

El almacenamiento es en memoria, por lo tanto los datos se pierden al cerrar el programa.