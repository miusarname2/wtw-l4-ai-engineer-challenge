# Challenge técnico — Staging Agent Review

## Misión

Recibiste un agente empresarial existente que pasa sus happy paths. Debes revisarlo como candidato a producción.

Tu trabajo es:

1. entender el flujo;
2. identificar riesgos con evidencia en el código;
3. priorizar los problemas más importantes;
4. mejorar una parte razonable dentro del timebox;
5. responder a cambios o fallos introducidos por el entrevistador;
6. defender la arquitectura.

## Regla inicial

No modifiques código hasta que el entrevistador te lo indique.

Durante la revisión inicial explica:

- cómo funciona `/api/ask`;
- dónde ocurre retrieval;
- dónde se ejecutan tools;
- cómo se construyen `sources` y `tools_used`;
- cuáles son tus tres riesgos principales;
- qué arreglarías primero.

## Resultado esperado

No existe una única solución correcta. No se espera que arregles todo.

Se valoran más:

- diagnóstico;
- decisiones;
- pruebas dirigidas a riesgos;
- seguridad y resiliencia;
- comprensión de AI/agent/RAG;
- uso crítico de Copilot;

que la cantidad de archivos modificados.

## GitHub Copilot

Está permitido y esperado. Puedes pedirle que analice, genere, pruebe y refactorice. Toda propuesta debe ser revisada y explicada por ti.

## Restricciones

- no hardcodees respuestas;
- no modifiques los datos de las APIs para forzar los tests;
- no elimines trazabilidad para ocultar errores;
- no sustituyas el agente por routing basado únicamente en keywords;
- no expongas secretos en código o logs;
- no dependas de una suscripción Azure.
