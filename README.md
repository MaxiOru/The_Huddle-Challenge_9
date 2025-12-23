# Sistema de Chat Multicliente con Testing Completo

## ¿Qué es?

Sistema de **chat en tiempo real** que permite la comunicación simultánea entre múltiples clientes conectados a un servidor central. Implementado en Python con arquitectura cliente-servidor utilizando sockets TCP/IP y threading para manejar múltiples conexiones concurrentes.

El proyecto está diseñado con **enfoque en testing**, siguiendo metodologías de desarrollo profesional como **TDD (Test-Driven Development)** y pruebas exhaustivas que garantizan la calidad, estabilidad y robustez del sistema.

---

## ¿Para qué sirve?

### Funcionalidades del Sistema

- ✅ **Conexión múltiple:** Soporta varios clientes conectados simultáneamente
- ✅ **Broadcast de mensajes:** Los mensajes se distribuyen a todos los clientes conectados
- ✅ **Validación de mensajes:** Rechaza mensajes vacíos o inválidos
- ✅ **Manejo de desconexiones:** Detecta y gestiona desconexiones inesperadas sin afectar a otros usuarios
- ✅ **Comunicación bidireccional:** Envío y recepción de mensajes en tiempo real
- ✅ **Gestión de clientes:** Añade y remueve clientes automáticamente

### Objetivo de Testing

El propósito principal de este proyecto es **demostrar la implementación de pruebas exhaustivas** en sistemas de red concurrentes, cubriendo:

- Pruebas unitarias con aislamiento completo
- Desarrollo guiado por pruebas (TDD)
- Pruebas de integración con componentes reales
- Pruebas de resiliencia ante fallos

---

## Tecnologías y Herramientas

### Core del Sistema

| Tecnología         | Versión | Propósito                                 |
| ------------------- | -------- | ------------------------------------------ |
| **Python**    | 3.10+    | Lenguaje de programación principal        |
| **socket**    | stdlib   | Comunicación TCP/IP cliente-servidor      |
| **threading** | stdlib   | Manejo de múltiples clientes concurrentes |

### Framework de Testing

| Herramienta             | Versión | Propósito                           |
| ----------------------- | -------- | ------------------------------------ |
| **pytest**        | 7.4+     | Framework principal de testing       |
| **unittest.mock** | stdlib   | Aislamiento de componentes con Mocks |

---

## Implementación de Testing con pytest

### ¿Por qué pytest?

**pytest** es el framework de testing más utilizado en Python por:

- Sintaxis simple y legible
- Autodescubrimiento de tests
- Salida detallada de errores
- Soporte para fixtures y parametrización
- Ecosistema extenso de plugins

### Tipos de Pruebas Implementadas

#### 1️⃣ **Pruebas Unitarias** ([test_unitarios.py](test_unitarios.py))

**Propósito:** Validar métodos individuales de forma aislada

**Tecnología clave:** `unittest.mock.Mock`

- Simula clientes sin necesidad de conexiones reales
- Aísla la lógica de negocio del sistema de red
- Pruebas rápidas y deterministas

**Métodos probados:**

- `validar_mensaje()` - Validación de entrada
- `agregar_cliente()` - Gestión de lista de clientes
- `remover_cliente()` - Limpieza de conexiones
- `broadcast()` - Distribución de mensajes

```bash
pytest test_unitarios.py -v
```

---

#### 2️⃣ **Test-Driven Development** ([test_tdd.py](test_tdd.py))

**Propósito:** Desarrollar funcionalidad siguiendo ciclo RED-GREEN-REFACTOR

**Metodología TDD:**

1. 🔴 **RED:** Escribir test que falla (método no existe)
2. 🟢 **GREEN:** Implementar código mínimo que pasa el test
3. 🔵 **REFACTOR:** Optimizar sin romper el test

**Funcionalidad desarrollada:** `validar_mensaje()`

- Demuestra cómo TDD guía el diseño del código
- Prueba como especificación ejecutable
- Refactoring seguro respaldado por tests

```bash
pytest test_tdd.py -v
```

---

#### 3️⃣ **Pruebas de Integración** ([test_integracion.py](test_integracion.py))

**Propósito:** Validar interacción entre componentes reales

**Tecnologías integradas:**

- Sockets TCP/IP reales (puerto 55125)
- Threading concurrente (múltiples hilos simultáneos)
- Callbacks para comunicación asíncrona

**Escenarios probados:**

- Conexión de 3 clientes simultáneos
- Broadcast a múltiples receptores
- Comunicación bidireccional
- Sincronización de threads

```bash
pytest test_integracion.py -v -s
```

---

#### 4️⃣ **Pruebas de Desconexión** ([test_desconexion.py](test_desconexion.py))

**Propósito:** Verificar resiliencia ante fallos de red

**Técnica:** `Mock.side_effect` para simular excepciones

- Simula `BrokenPipeError` (cliente desconectado)
- Verifica que el servidor NO crashea
- Valida que otros clientes no se afectan

**Casos de uso reales:**

- Usuario cierra aplicación abruptamente
- Pérdida de conexión de red
- Timeout de socket

```bash
pytest test_desconexion.py -v
```

---

## 📁 Estructura del Proyecto

```
noveno reto/
│
├── server.py                    # Servidor de chat (ServidorChat)
├── cliente.py                   # Cliente de chat (ClienteChat)
│
├── test_unitarios.py           # 5 pruebas unitarias con Mocks
├── test_tdd.py                 # 1 prueba TDD (RED-GREEN-REFACTOR)
├── test_integracion.py         # 1 prueba de integración (sockets reales)
├── test_desconexion.py         # 1 prueba de resiliencia
│
└── README.md                   # Este archivo
```

**Total:** 8 pruebas automatizadas con pytest

---

## ▶️ Cómo Ejecutar

### Ejecutar el Sistema

**1. Iniciar el servidor:**

```bash
python server.py
```

**2. Conectar clientes (en terminales separadas):**

```bash
python cliente.py
```

### Ejecutar las Pruebas

**Todas las pruebas:**

```bash
pytest -v
```

**Por tipo de prueba:**

```bash
pytest test_unitarios.py -v      # Pruebas unitarias
pytest test_tdd.py -v             # TDD
pytest test_integracion.py -v    # Integración
pytest test_desconexion.py -v    # Desconexión
```

**Con cobertura:**

```bash
pytest --cov=server --cov=cliente --cov-report=html
```

**Modo detallado (con prints):**

```bash
pytest -v -s
```
