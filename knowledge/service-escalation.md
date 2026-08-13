# Procedimiento de escalamiento de servicios

## Identificación

Antes de escalar, identifica el servicio afectado y recopila los síntomas observados, severidad estimada, hora de inicio, alcance e identificador del incidente. La información dinámica del owner debe consultarse en el catálogo de servicios y no asumirse a partir de este documento.

## Contacto inicial

Consulta el catálogo de servicios para obtener el equipo owner, el alias on-call y el canal de soporte. Contacta primero al canal o alias recomendado y proporciona contexto suficiente para que el equipo pueda responder sin pedir los datos básicos nuevamente.

Para una afectación activa, registra cuándo se envió el contacto y si hubo acknowledgement. Evita notificar múltiples canales simultáneamente sin coordinación porque puede generar respuestas duplicadas.

## Escalamiento

Para incidentes SEV-1 y SEV-2 sin respuesta del equipo owner durante 10 minutos, se debe escalar al Incident Commander. Si todavía no existe Incident Commander, solicita su asignación conforme a la política de gestión de incidentes.

En un SEV-3, utiliza el canal de soporte del servicio y sigue la cadencia normal, salvo que el impacto aumente. Si el owner confirma que el problema pertenece a otro servicio, actualiza el registro y repite la consulta del catálogo para el nuevo servicio.

## Información mínima

El mensaje de escalamiento debe incluir: incidente, servicio, severidad, impacto, acciones realizadas, evidencia relevante, contacto previo y ayuda requerida. No incluyas secretos ni datos personales que no sean necesarios.
