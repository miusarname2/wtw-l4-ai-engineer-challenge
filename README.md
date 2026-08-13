# AI Engineer Semi Senior L4 — Diagnóstico de un agente empresarial

Este repositorio contiene un sistema de IA que ya funciona en los casos básicos de staging. La entrevista no consiste en construirlo desde cero.

Tu objetivo es **entenderlo, diagnosticar sus riesgos, priorizar mejoras y aplicar cambios concretos con ayuda de GitHub Copilot**.

La entrevista completa dura **60 minutos** y se realiza localmente. No necesitas una suscripción de Azure ni desplegar infraestructura.

---

## 1. Escenario

El equipo de Plataforma desarrolló un asistente interno que:

- responde preguntas con documentación local mediante RAG;
- consulta incidentes y servicios mediante APIs externas;
- combina contexto documental y tools;
- se expone como una Azure Function HTTP local;
- devuelve `answer`, `sources` y `tools_used`.

El prototipo pasa pruebas básicas, pero aún no ha sido aprobado para producción. Tu tarea es revisar el sistema como si hubiera llegado a tu equipo desde otro proyecto.

**No asumas que una implementación existente o un test que pasa implica que el diseño es correcto.**

---

## 2. Qué se espera durante la entrevista

### Fase 1 — Revisión sin modificar código

Durante los primeros minutos:

1. inspecciona el repositorio;
2. explica el flujo completo de una solicitud;
3. identifica los riesgos técnicos más importantes;
4. prioriza qué cambiarías primero y por qué.

El entrevistador te indicará cuándo puedes comenzar a editar.

### Fase 2 — Mejoras

Selecciona un número razonable de problemas y mejora la implementación. No se espera corregir todo.

Se evalúa especialmente:

- calidad del diagnóstico;
- priorización;
- grounding y trazabilidad;
- diseño de tools y agente;
- seguridad;
- resiliencia;
- observabilidad;
- criterio Azure/cloud;
- capacidad para dirigir y validar a GitHub Copilot.

### Fase 3 — Cambio de requisitos y fallos

El entrevistador presentará uno o más escenarios adicionales que no aparecen necesariamente en este README. Tendrás que explicar o modificar la solución de forma incremental.

### Fase 4 — Defensa técnica

Al final deberás explicar:

- qué cambiaste;
- qué dejaste pendiente;
- qué decisiones tomó Copilot y cuáles tomaste tú;
- cómo llevarías el sistema a producción.

---

## 3. GitHub Copilot

El uso de **GitHub Copilot está permitido y esperado**.

Puedes utilizar:

- Chat;
- Agent Mode;
- Edit Mode;
- autocomplete;
- generación de tests;
- refactoring;
- debugging;
- revisión de código.

No se evalúa cuánto código escribes manualmente. Sí se evalúa que:

- comprendas el código que conservas;
- verifiques las sugerencias;
- detectes decisiones incorrectas;
- puedas rechazar o modificar una propuesta de Copilot;
- expliques tus trade-offs.

Si alcanzas un límite de tu plan de Copilot, informa al entrevistador. El límite del producto no se evalúa negativamente.

---

## 4. Arquitectura actual

```text
Cliente
   │
   ▼
Azure Function local
POST /api/ask
   │
   ▼
Agent orchestration
   │
   ├──────────────► Retrieval local ─────► knowledge/*.md
   │
   ├──────────────► Incident tool ───────► API externa
   │
   └──────────────► Service tool ────────► API externa
   │
   ▼
LLM compatible con Chat Completions + tool calling
```

La arquitectura mostrada describe el sistema actual, no necesariamente la arquitectura que debes conservar.

---

## 5. APIs externas

Los contratos de las APIs se encuentran en:

```text
docs/API_REFERENCE.md
```

Ese documento es la fuente de verdad para:

- URL;
- autenticación;
- endpoints;
- parámetros;
- payloads;
- errores.

No necesitas crear recursos en AWS ni conocer la implementación interna de los mocks.

---

## 6. Ejecución local con Azure Functions

La aplicación usa Azure Functions Python v2 y se ejecuta con Azure Functions Core Tools.

No se requiere cuenta Azure.

### Prerrequisitos

- Python 3.11 o 3.12;
- Azure Functions Core Tools v4;
- Git;
- VS Code recomendado;
- GitHub Copilot autenticado;
- acceso a las variables entregadas por el entrevistador.

### Preparación

```bash
python -m venv .venv
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Instala dependencias:

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

Copia la configuración:

```bash
cp local.settings.example.json local.settings.json
```

Completa los valores proporcionados para LLM y API mock.

### Iniciar

```bash
func start
```

Endpoints:

```text
GET  http://localhost:7071/api/health
POST http://localhost:7071/api/ask
```

---

## 7. Requests básicos

Health:

```bash
curl -sS http://localhost:7071/api/health
```

RAG:

```bash
curl -sS \
  -H 'Content-Type: application/json' \
  -d '{"question":"¿Cuánto dura el acceso privilegiado de emergencia?"}' \
  http://localhost:7071/api/ask
```

Tool:

```bash
curl -sS \
  -H 'Content-Type: application/json' \
  -d '{"question":"¿Cuál es el estado de INC-1042?"}' \
  http://localhost:7071/api/ask
```

Composición:

```bash
curl -sS \
  -H 'Content-Type: application/json' \
  -d '{"question":"Payments está caído. ¿Quién es responsable y cómo debo escalarlo?"}' \
  http://localhost:7071/api/ask
```

También puedes usar `requests.http`.

---

## 8. Tests

```bash
pytest
```

Los tests públicos demuestran que el starter funciona en escenarios básicos. **No constituyen una especificación completa de calidad ni de producción.**

---

## 9. Estructura

```text
.
├── README.md
├── CHALLENGE.md
├── function_app.py
├── host.json
├── local.settings.example.json
├── requests.http
├── requirements.txt
├── requirements-dev.txt
│
├── src/
│   ├── agent.py
│   ├── config.py
│   ├── knowledge.py
│   ├── llm.py
│   ├── models.py
│   └── tools.py
│
├── knowledge/
├── docs/
│   └── API_REFERENCE.md
│
├── tests/
└── .github/
    └── copilot-instructions.md
```

---

## 10. Alcance

No se exige durante la entrevista:

- desplegar en Azure;
- implementar infraestructura como código;
- crear Azure AI Search;
- crear una interfaz gráfica;
- completar una solución production-ready;
- corregir todos los defectos existentes.

Se espera que puedas reconocer las limitaciones del timebox y defender lo que priorizaste.
