# Gestión de incidentes

## Definición

Un incidente es una interrupción o degradación no planificada que afecta la disponibilidad, seguridad, integridad o desempeño de un servicio. La severidad se determina por impacto al cliente, alcance, duración esperada y riesgo operativo.

## Severidades

- **SEV-1:** impacto crítico y generalizado, pérdida de una función esencial o riesgo significativo de seguridad.
- **SEV-2:** impacto alto pero parcial, degradación importante o afectación a un conjunto relevante de clientes.
- **SEV-3:** impacto limitado, workaround disponible o degradación menor.

La cadencia mínima de comunicación es obligatoria: SEV-1 requiere una actualización cada 15 minutos. SEV-2 requiere una actualización cada 30 minutos. SEV-3 requiere una actualización cada 60 minutos.

## Respuesta inicial

La primera persona que confirma el problema debe abrir o actualizar el registro del incidente, identificar el servicio afectado, recopilar evidencia inicial y contactar al equipo owner. Para SEV-1 y SEV-2 debe designarse un Incident Commander responsable de coordinación, decisiones y comunicación.

Los especialistas técnicos investigan y ejecutan acciones; el Incident Commander mantiene la visión global y evita que todos trabajen sobre la misma hipótesis sin coordinación.

## Comunicación y cierre

Las actualizaciones deben incluir estado, impacto, acciones realizadas, siguiente paso y hora estimada de la próxima actualización. No deben incluir credenciales, datos personales innecesarios ni información que incremente el riesgo de seguridad.

Después de resolver un SEV-1 o SEV-2 debe realizarse un postmortem sin culpa que documente causa, detección, respuesta, acciones correctivas y owners.
