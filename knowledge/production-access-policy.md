# Política de acceso a producción

## Objetivo

El acceso a entornos de producción se concede únicamente cuando existe una necesidad operativa o de soporte justificada. Los permisos deben seguir el principio de mínimo privilegio y limitarse al servicio, ambiente y periodo requeridos.

## Solicitud estándar

Toda solicitud debe registrarse en el sistema corporativo de accesos. Debe incluir el servicio afectado, la justificación de negocio, las actividades que se realizarán, el nivel de privilegio solicitado y la fecha de expiración. La solicitud requiere aprobación del manager de la persona solicitante y del owner del servicio.

Antes de activar el permiso, la persona debe tener MFA habilitado y haber completado la capacitación de seguridad correspondiente. No se permiten cuentas compartidas, credenciales genéricas ni transferencia de tokens entre personas.

## Acceso privilegiado temporal

Los permisos administrativos deben ser temporales. El acceso privilegiado de emergencia expira después de 4 horas. Si el trabajo continúa después de ese periodo, debe generarse una nueva solicitud y una nueva aprobación.

Durante una emergencia se debe asociar el acceso con el incidente correspondiente y registrar las acciones relevantes sin incluir secretos en logs. El acceso no debe utilizarse para tareas distintas de las aprobadas.

## Revisión y revocación

Los accesos permanentes deben revisarse trimestralmente. Los permisos deben revocarse cuando una persona cambia de equipo, deja de participar en el servicio o ya no requiere el privilegio. El owner del servicio es responsable de validar la lista de acceso durante cada revisión.
