# APIs Mock Externas — Referencia para el Candidato

Este documento describe los servicios mock externos disponibles durante la entrevista práctica para el rol de AI Engineer.

Estas APIs representan sistemas empresariales externos que tu aplicación de IA o agente puede consultar en tiempo de ejecución. Se espera que las integres en tu solución cuando sea apropiado.

Las APIs ya están desplegadas. **No necesitas crear, desplegar ni modificar ningún recurso en AWS.**

---

## 1. Alcance

La API mock es **solo de lectura** para este ejercicio.

No se espera que:

- crees o actualices incidentes;
- modifiques metadatos de servicios;
- despliegues infraestructura en AWS;
- utilices el SDK de AWS;
- configures credenciales de AWS IAM;
- accedas directamente a S3;
- conozcas cómo está implementada internamente la API mock.

Tu aplicación únicamente necesita consumir los endpoints HTTPS documentados a continuación.

---

## 2. Variables de entorno

Los siguientes valores estarán disponibles en tu entorno de desarrollo:

```bash
MOCK_API_BASE_URL=https://upqupn62prlcmunoshnb6z5lxq0znfvi.lambda-url.us-east-1.on.aws
MOCK_API_KEY=<proporcionada-durante-la-entrevista>
```

Utiliza estos valores desde la configuración del entorno. No hardcodees la API key en el código fuente.

La URL base también debe tratarse como un valor configurable.

---

## 3. Autenticación

Todos los endpoints bajo `/v1/*` requieren el siguiente header HTTP:

```text
x-mock-api-key: <provided-key>
```

El endpoint de health check no requiere autenticación:

```text
GET /health
```

No se requiere autenticación de AWS, firma IAM ni credenciales de AWS para consumir estas APIs.

---

## 4. Cómo se relacionan estas APIs con el challenge

Las APIs representan sistemas empresariales externos que contienen información operacional que no debe asumirse como parte del conocimiento del modelo ni del corpus documental utilizado para RAG.

Tu agente puede exponer estas capacidades como tools. Por ejemplo, una solución podría ofrecer conceptualmente funciones similares a:

```text
get_incident_status(incident_id)
get_service_owner(service_name)
```

Estos nombres son únicamente ejemplos.

Tú decides:

- los nombres de las tools;
- las descripciones de las tools;
- los schemas de entrada;
- cómo decide el LLM cuándo necesita utilizar una tool;
- cómo se entregan al modelo los resultados devueltos por las APIs;
- cómo se representan los errores ante el agente;
- si la información obtenida mediante una tool debe combinarse con resultados de RAG.

Los contratos HTTP descritos a continuación son la fuente de verdad para las APIs externas.

---

## 5. Convenciones de respuesta

Las respuestas exitosas utilizan JSON.

```text
Content-Type: application/json
```

Las respuestas incluyen un header HTTP `x-request-id`, que puede resultar útil al diagnosticar una solicitud.

Los errores utilizan la siguiente estructura JSON:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message.",
    "request_id": "..."
  }
}
```

Tu implementación no debe asumir que todas las solicitudes devolverán HTTP `200`.

---

# 6. Endpoints

## 6.1 GET /health

Health check del servicio mock.

### Autenticación

Ninguna.

### Ejemplo de solicitud

```bash
curl -sS "${MOCK_API_BASE_URL%/}/health"
```

### Ejemplo de respuesta `200`

```json
{
  "status": "ok",
  "service": "ai-engineer-interview-mock-api",
  "version": "1.0.0"
}
```

---

## 6.2 GET /v1/incidents/{incident_id}

Devuelve información actual sobre un incidente.

### Autenticación

Requerida:

```text
x-mock-api-key: <provided-key>
```

### Parámetro de ruta

`incident_id`

Formato esperado:

```text
INC-####
```

La entrada no distingue entre mayúsculas y minúsculas.

Por ejemplo, `inc-1042` e `INC-1042` hacen referencia al mismo identificador.

### Ejemplo de solicitud

```bash
curl -sS \
  -H "x-mock-api-key: $MOCK_API_KEY" \
  "${MOCK_API_BASE_URL%/}/v1/incidents/INC-1042"
```

### Ejemplo de respuesta `200`

```json
{
  "incident_id": "INC-1042",
  "service": "payments",
  "title": "Elevated payment authorization failures",
  "status": "investigating",
  "severity": "SEV-2",
  "customer_impact": "Some customers cannot complete card payments.",
  "started_at": "2026-08-12T13:55:00Z",
  "updated_at": "2026-08-12T14:20:00Z",
  "assigned_team": "Payments Platform"
}
```

> Nota: los valores del JSON de ejemplo se muestran tal como los devuelve actualmente el servicio mock. No deben traducirse ni asumirse como valores constantes dentro de tu implementación.

### Errores comunes

| HTTP status | Código de error | Significado |
|---|---|---|
| `400` | `INVALID_INCIDENT_ID` | El parámetro de ruta no tiene un formato válido de ID de incidente. |
| `401` | `UNAUTHORIZED` | La API key no está presente o no es válida. |
| `404` | `INCIDENT_NOT_FOUND` | No existe un incidente para el ID proporcionado. |

### Ejemplos de preguntas que este endpoint puede ayudar a responder

```text
¿Cuál es el estado de INC-1042?
```

```text
¿Qué servicio está afectado por INC-1042?
```

```text
¿Cuál es la severidad y el impacto al cliente de INC-1042?
```

Los ejemplos demuestran el contrato de la API. Tu implementación no debe estar acoplada a un único ID de incidente.

---

## 6.3 GET /v1/services/{service_name}

Devuelve metadatos sobre un servicio interno.

### Autenticación

Requerida:

```text
x-mock-api-key: <provided-key>
```

### Parámetro de ruta

`service_name`

Los nombres de servicio son slugs como:

```text
payments
```

La entrada no distingue entre mayúsculas y minúsculas y es normalizada por la API.

### Ejemplo de solicitud

```bash
curl -sS \
  -H "x-mock-api-key: $MOCK_API_KEY" \
  "${MOCK_API_BASE_URL%/}/v1/services/payments"
```

### Ejemplo de respuesta `200`

```json
{
  "service": "payments",
  "display_name": "Payments",
  "owner_team": "Payments Platform",
  "on_call": "payments-oncall",
  "criticality": "high",
  "tier": "tier-1",
  "support_channel": "#payments-support",
  "repository": "platform/payments-service",
  "active": true,
  "updated_at": "2026-08-10T16:30:00Z"
}
```

> Nota: los valores del JSON de ejemplo se muestran tal como los devuelve actualmente el servicio mock. Tu implementación debe tratar estos valores como datos externos, no como constantes del código.

### Errores comunes

| HTTP status | Código de error | Significado |
|---|---|---|
| `400` | `INVALID_SERVICE_NAME` | El nombre del servicio no es válido. |
| `401` | `UNAUTHORIZED` | La API key no está presente o no es válida. |
| `404` | `SERVICE_NOT_FOUND` | No existe un servicio para el nombre proporcionado. |

### Ejemplos de preguntas que este endpoint puede ayudar a responder

```text
¿Quién es responsable del servicio payments?
```

```text
¿Cuál es el grupo on-call de payments?
```

```text
¿Qué tan crítico es el servicio payments?
```

Los ejemplos demuestran el contrato de la API. Tu implementación no debe estar acoplada a un único nombre de servicio.

---

# 7. Combinación de APIs externas con RAG

Algunas preguntas pueden responderse utilizando una sola fuente de información. Otras pueden requerir combinar múltiples fuentes.

Por ejemplo:

```text
Payments está caído. ¿Quién es responsable del servicio y cómo debo escalar el incidente?
```

Una solución razonable puede necesitar combinar:

```text
Metadatos externos del servicio
        +
Documentación interna recuperada mediante RAG
        ↓
Una única respuesta fundamentada
```

El enfoque de orquestación queda intencionalmente a tu criterio.

No asumas que la información operacional devuelta por estas APIs también estará disponible dentro de la colección documental utilizada para RAG.

---

# 8. Ejemplo mínimo en Python

El siguiente fragmento demuestra únicamente el patrón de integración HTTP. No busca prescribir la arquitectura de tu agente ni la implementación de tus tools.

```python
import os

import requests

base_url = os.environ["MOCK_API_BASE_URL"].rstrip("/")
api_key = os.environ["MOCK_API_KEY"]

response = requests.get(
    f"{base_url}/v1/incidents/INC-1042",
    headers={"x-mock-api-key": api_key},
    timeout=5,
)

response.raise_for_status()
incident = response.json()

print(incident)
```

Puedes utilizar otro cliente HTTP o un estilo de implementación diferente si lo prefieres.

---

# 9. Pruebas rápidas de conectividad

Antes de integrar las APIs con el agente, puedes verificar la conectividad de forma independiente.

### Health

```bash
curl -i "${MOCK_API_BASE_URL%/}/health"
```

### Incident API

```bash
curl -i \
  -H "x-mock-api-key: $MOCK_API_KEY" \
  "${MOCK_API_BASE_URL%/}/v1/incidents/INC-1042"
```

### Service API

```bash
curl -i \
  -H "x-mock-api-key: $MOCK_API_KEY" \
  "${MOCK_API_BASE_URL%/}/v1/services/payments"
```

Si estos comandos funcionan pero tu agente no, considera el problema como parte de la integración de la aplicación y no como un problema de despliegue en AWS.

---

# 10. Datos de demostración conocidos

Los ejemplos de este documento exponen intencionalmente únicamente los datos necesarios para verificar tu integración.

Puedes utilizar los siguientes registros durante el desarrollo:

```text
Incident: INC-1042
Service:  payments
```

Pueden existir otros registros válidos dentro del servicio mock.

Por lo tanto, tu solución debe tratar los IDs de incidente y los nombres de servicio como inputs dinámicos de las tools, y no como valores hardcodeados.

---

# 11. Aspectos intencionalmente no especificados

Esta referencia de API intencionalmente **no** prescribe:

- el framework de agentes que debes utilizar;
- la abstracción de proveedor de LLM;
- tu estrategia de orquestación de RAG;
- la arquitectura de tool calling;
- tu estrategia de retries;
- el diseño de observabilidad;
- la estructura interna de la aplicación;
- la arquitectura de despliegue;
- caching;
- el diseño de autenticación para un entorno productivo;
- cuántos pasos puede ejecutar el agente;
- cómo prevenir llamadas innecesarias a tools.

Estas son decisiones de ingeniería que puedes tomar y explicar durante el ejercicio.

---

# 12. Checklist de integración

Antes de considerar completa la integración con los sistemas externos, como mínimo deberías poder demostrar que tu aplicación puede:

- leer la URL base y la API key desde configuración;
- llamar exitosamente al endpoint de incidentes utilizando un ID dinámico;
- llamar exitosamente al endpoint de servicios utilizando un nombre de servicio dinámico;
- interpretar respuestas JSON exitosas;
- distinguir una respuesta exitosa de un error de la API;
- poner la información externa a disposición del agente;
- responder una pregunta que requiera información obtenida desde una de las APIs externas.

La forma de implementar estas capacidades queda a tu criterio.

---

# 13. Resumen

Durante el ejercicio están disponibles dos capacidades externas de solo lectura:

```text
Información de incidentes
GET /v1/incidents/{incident_id}

Metadatos de servicios
GET /v1/services/{service_name}
```

Ambas utilizan:

```text
x-mock-api-key: $MOCK_API_KEY
```

Las APIs deben tratarse como sistemas empresariales externos que tu agente de IA puede consultar cuando la pregunta del usuario requiera información operacional.

Los registros de ejemplo `INC-1042` y `payments` se proporcionan únicamente para realizar pruebas de conectividad. Tu implementación debe permanecer genérica y aceptar otros valores válidos.
