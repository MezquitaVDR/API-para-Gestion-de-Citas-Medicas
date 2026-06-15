# Pruebas Unitarias — APLICACION para Gestión de Citas Médicas

Esta carpeta contiene la suite de **pruebas unitarias** del proyecto. Cubre la capa de negocio (`src/core`) y las
funciones de validación (`src/utils/utils.py`).

## 📁 Archivos incluidos

Estos archivos deben colocarse en la **raíz del proyecto**, junto a la carpeta `src/`:

```text
API-para-Gestion-de-Citas-Medicas/
├── conftest.py                # Configuración global de pytest
├── pytest.ini                 # Configuración de ejecución de pytest
├── requirements-test.txt      # Dependencias necesarias para correr las pruebas
├── src/
│   └── ...
└── tests/
    ├── test_pacientes.py      # Pruebas de GestorPacientes
    ├── test_medicos.py        # Pruebas de GestorMedicos
    ├── test_citas.py          # Pruebas de GestorCitas
    └── test_utils.py          # Pruebas de las validaciones de src/utils/utils.py
```

## ⚙️ Instalación

```bash
pip install -r requirements-test.txt
```

> **Nota:** El proyecto usa `tkinter` para la interfaz gráfica. El archivo
> `conftest.py` incluye un "stub" (simulación) automática de `tkinter` para que
> las pruebas de `src/utils/utils.py` puedan ejecutarse incluso en entornos
> sin interfaz gráfica (servidores, CI/CD, contenedores). Si tu entorno **sí**
> tiene `tkinter` instalado, la simulación no se activa y las pruebas usan el
> módulo real.

## ▶️ Cómo ejecutar las pruebas

Desde la raíz del proyecto:

```bash
# Ejecutar toda la suite
python -m pytest

# Ejecutar un archivo específico
python -m pytest tests/test_citas.py

# Ejecutar una clase o caso de prueba específico
python -m pytest tests/test_citas.py::TestCrearCita
python -m pytest tests/test_citas.py::TestCrearCita::test_crear_cita_exitosa

# Ver el detalle de cobertura por nombre de prueba (modo verboso, ya activado por defecto)
python -m pytest -v

# Generar un reporte de cobertura (requiere pytest-cov)
pip install pytest-cov
python -m pytest --cov=src --cov-report=term-missing
```

## 🧪 ¿Qué se prueba?

### `tests/test_pacientes.py` — `GestorPacientes`
- Carga inicial: archivo inexistente → diccionario vacío; archivo existente → datos cargados correctamente.
- `crear_paciente`: creación exitosa, rechazo de IDs duplicados, persistencia en `pacientes.json`.
- `listar_pacientes` y `obtener_paciente` (caso existente e inexistente).
- `actualizar_paciente`: actualización exitosa, caso inexistente, persistencia de cambios.
- `eliminar_paciente`: eliminación exitosa, caso inexistente, persistencia.

### `tests/test_medicos.py` — `GestorMedicos`
- Misma cobertura que `GestorPacientes`, adaptada a médicos (`nombre`, `especialidad`).

### `tests/test_citas.py` — `GestorCitas`
- Carga inicial de citas desde archivo.
- `crear_cita`:
  - Creación exitosa.
  - Rechazo por ID de cita duplicado.
  - Rechazo si el paciente no existe.
  - Rechazo si el médico no existe.
  - Rechazo por **conflicto de horario** (mismo médico, misma fecha y hora).
  - Aceptación si dos médicos distintos comparten fecha/hora.
- `existe_conflicto_horario`: detección de conflictos, exclusión por `excluir_id`.
- `actualizar_cita`:
  - Actualización exitosa.
  - Validaciones de cita/paciente/médico inexistentes.
  - Conflictos de horario al reprogramar.
  - Caso especial: actualizar una cita sin cambiar su propio horario (no debe marcarse como conflicto consigo misma).
- `eliminar_cita`: eliminación exitosa y caso inexistente.
- **Eliminación en cascada**: `eliminar_citas_por_paciente` y `eliminar_citas_por_medico` eliminan únicamente las citas asociadas, dejando intactas las demás.
- Persistencia en `citas.json` para todas las operaciones de escritura.

### `tests/test_utils.py` — `src/utils/utils.py`
- `validar_entero_positivo`: enteros positivos, cero, negativos, texto no numérico, decimales, `None`.
- `validar_id_no_vacio`: cadenas válidas, vacías, solo espacios, valores no string.
- `validar_fecha`: formato `YYYY-MM-DD`, fechas inválidas (mes/día fuera de rango), formatos incorrectos.
- `validar_hora`: formato `HH:MM` (24 horas), horas fuera de rango, formatos incorrectos.
- `obtener_texto_no_vacio`, `obtener_entero_positivo`, `obtener_fecha`, `obtener_hora`:
  simulan un `tk.Entry` mediante una clase auxiliar (`EntradaFalsa`) y verifican
  tanto el valor retornado como la invocación de `messagebox.showerror` ante
  entradas inválidas.

## 🔒 Aislamiento de datos

Todas las pruebas que ejercitan `GestorPacientes`, `GestorMedicos` y `GestorCitas`
usan la fixture `tmp_path` de pytest para crear archivos `.json` **temporales**
en cada ejecución. Esto garantiza que las pruebas:

- No modifiquen ni dependan de `pacientes.json`, `medicos.json` o `citas.json` del proyecto real.
- Sean completamente independientes entre sí (no comparten estado).
- Puedan ejecutarse en cualquier orden sin efectos colaterales.

## ✅ Resultado esperado

Al ejecutar `python -m pytest` desde la raíz del proyecto, deberías ver una
salida similar a:

```text
======================== 104 passed in 0.2s ========================
```
