# Jetoil - Adaptaciones y Correcciones para Cheques (Argentina)

Este módulo implementa correcciones críticas sobre la localización argentina (`odoo-argentina` de ADHOC) específicamente para el flujo de **Rechazo de Cheques de Terceros**.

## 📋 Resumen

El módulo soluciona tres bloqueos principales que impedían rechazar un cheque entregado/depositado:
1.  **Error de Singleton:** Conflicto cuando el Diario de Banco tiene múltiples métodos de pago de salida.
2.  **Restricción de Grupos de Pago:** Bloqueo de ADHOC que impide crear pagos sueltos (necesarios para el ajuste contable del rechazo).
3.  **Crash por Datos Corruptos:** Error `AttributeError: 'NoneType'` debido a líneas de historial sin documento de origen.

---

## 🛠 Detalles Técnicos y Métodos Afectados

El módulo utiliza herencia para interceptar y corregir el flujo en tres puntos clave:

### 1. Wizard de Acción de Cheques (`account.check.action.wizard`)
**Archivo:** `models/extended_check_wizard.py`
**Método afectado:** `action_confirm()`

* **Función de Reparación:** Antes de procesar, analiza el historial (`operation_ids`) del cheque. Si encuentra operaciones corruptas (donde `origin` es `None` o vacío), las repara asignando el propio cheque como origen. Esto evita que Odoo borre el historial y pase el cheque a "Borrador".
* **Inyección de Contexto (Pase VIP):** Agrega la clave `'force_account_payment_create': True` al contexto antes de llamar al método original. Esto sirve de "llave maestra" para los pasos siguientes.

### 2. Modelo de Cheques (`account.check`)
**Archivo:** `models/extended_account_check.py`
**Método afectado:** `get_payment_values(journal)`

* **Corrección Singleton:** Si el diario seleccionado devuelve múltiples métodos de pago (ej. Manual y Cheques), se fuerza la selección del primero (índice 0) para evitar el error `ValueError: Expected singleton`.
* **Corrección de Base de Datos:** Se inyecta explícitamente `'payment_type': 'outbound'`. Esto es necesario porque al rechazar un depósito, el dinero "sale" del banco, y PostgreSQL requiere este campo obligatorio que no siempre se calculaba automáticamente en este flujo.

### 3. Modelo de Pagos (`account.payment`)
**Archivo:** `models/extended_account_payment.py`
**Método afectado:** `check_payment_group()` (@api.constrains)

* **Bypass de Validación:** Intercepta la validación nativa de ADHOC que obliga a usar Grupos de Pago.
* **Lógica:** Verifica si en el contexto viene la llave `force_account_payment_create`. Si es `True`, omite la validación y permite crear el pago de ajuste suelto. Si es `False`, ejecuta la validación original.

---

## 📂 Estructura de Archivos

```text
jetoil/
├── models/
│   ├── __init__.py
│   ├── extended_check_wizard.py    # Lógica del Wizard (Reparación + Contexto)
│   ├── extended_account_check.py   # Lógica del Cheque (Valores Default)
│   └── extended_account_payment.py # Lógica del Pago (Permisos)
├── __init__.py
├── __manifest__.py
└── README.md