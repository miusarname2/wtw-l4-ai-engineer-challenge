# Política de despliegues

## Cambios estándar

Todo cambio de código debe pasar por pull request, revisión de al menos una persona distinta al autor y validaciones automatizadas aplicables. El artefacto promovido a producción debe corresponder al mismo commit probado en el ambiente previo.

Antes de producción se debe validar en staging o en un ambiente equivalente. El plan debe incluir alcance, riesgo, ventana, owner, criterios de éxito y señales para detener el cambio.

## Rollback

Todo despliegue de producción debe tener un procedimiento de rollback documentado antes de comenzar. El procedimiento debe indicar quién puede activarlo, qué artefacto o versión restaura, cómo se valida la recuperación y qué datos podrían requerir reconciliación.

Cuando un cambio aumenta errores, latencia o impacto al cliente por encima de los límites acordados, se debe priorizar estabilización y rollback sobre continuar experimentando.

## Cambios urgentes

Un cambio de emergencia puede reducir pasos administrativos, pero no elimina revisión, trazabilidad ni capacidad de rollback. Debe asociarse con un incidente, registrar las aprobaciones disponibles y completar retrospectivamente la documentación que no pudo realizarse antes.

## Cierre

Después del despliegue se verifican métricas técnicas y de negocio. La persona responsable documenta el resultado, incidentes relacionados y cualquier acción de seguimiento.
