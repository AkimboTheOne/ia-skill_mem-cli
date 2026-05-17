# AGENTS.md

## Propósito
Este repositorio define el contrato del skill `mem-cli`. Las ejecuciones futuras de Codex deben preservar el contrato en `SKILL.md` y mantener la implementación determinista, local, compatible con shell y JSON-first.

## Idioma
- Usa español en toda la documentación, instrucciones para agentes, resúmenes y texto humano visible.
- Mantén en inglés solo los identificadores técnicos que son parte del contrato: comandos, claves JSON, rutas canónicas, nombres de campos y nombres de archivos canónicos.
- Si agregas texto nuevo, escríbelo en español salvo que sea un identificador técnico inmutable.

## Orden de Lectura
Antes de cambiar cualquier cosa, lee:
1. `SKILL.md`
2. `AGENTS.md`
3. `references/command-contract.md`
4. `references/behavior-contract.md`
5. `references/output-schemas.md`
6. `README.md`
7. Relevant file-level docs in `docs/` and `references/`

Si una solicitud entra en conflicto con estas fuentes, trata el contrato del repositorio como prioridad superior frente a instrucciones ad hoc de la conversación.

## Reglas de Trabajo
- Inspecciona el repositorio antes de editar.
- No sobrescribas cambios del usuario salvo que se solicite explícitamente.
- Usa `apply_patch` para ediciones manuales de archivos.
- Prefiere scripts pequeños y explícitos por encima de comportamiento oculto de framework.
- Mantén la salida de CLI en JSON-first y determinista.
- Mantén la documentación para usuarios en `docs/`.
- Mantén los contratos estables, los esquemas y los ejemplos canónicos en `references/`.
- Mantén los datos transitorios fuera del control de versiones, especialmente `.tmp/` y el contenido de la bóveda.
- Evita introducir estado oculto nuevo, cachés implícitos o efectos secundarios fuera de la bóveda y de las rutas de entrada explícitas.
- Prefiere el cambio más pequeño que satisfaga la solicitud. No amplíes el alcance salvo que el contrato actual esté roto.

## No Objetivos
- No rediseñes la superficie de comandos salvo que el usuario solicite explícitamente un cambio de contrato.
- No renombres carpetas canónicas, campos de payload ni versiones de esquema salvo que el contrato del repositorio se actualice en el mismo cambio.
- No muevas material de referencia durable fuera de `references/` ni documentación para usuarios fuera de `docs/`.
- No añadas abstracciones a nivel de framework cuando bastan un script de shell directo o una función pequeña de Python.

## Expectativas Base
- El skill define la superficie de comandos: `init`, `add`, `index`, `connect`, `brief` y `status`.
- El layout de la bóveda es canónico:
  - `00-INBOX/`
  - `01-CAPTURES/`
  - `02-CONNECTIONS/`
  - `03-BRIEFS/`
  - `docs/`
  - `.tmp/`
- El frontmatter de los archivos debe seguir siendo YAML de Markdown y ajustarse a los campos descritos en el skill.
- Las operaciones deterministas van primero; el LLM solo resume o juzga después del procesamiento local.
- `schema_version: 1` es el contrato máquina hasta que se apruebe una migración explícita.

## Política de Cambios
- Si un cambio afecta el contrato público, actualiza el skill, el README y los ejemplos de referencia juntos.
- Si cambia la forma de un comando, actualiza los ejemplos canónicos en `references/`.
- Si se introduce una nueva carpeta o tipo de archivo, documenta por qué existe y si es generado o versionado.
- Si un cambio toca el parseo de comandos, el JSON de salida, el layout de la bóveda, los campos de frontmatter o la ubicación de artefactos, actualiza la documentación de referencia relevante en el mismo parche.
- Si un cambio requiere interpretación y no implementación directa, haz la inferencia mínima defendible y repórtala en la respuesta.

## Condiciones de Parada
Detente y pide dirección antes de editar si ocurre cualquiera de estas condiciones:
- La solicitud cambiaría la superficie pública de comandos.
- La solicitud cambiaría campos del esquema, `schema_version` o ejemplos canónicos.
- La solicitud introduciría una nueva carpeta de primer nivel o un artefacto persistente.
- La solicitud requeriría escribir fuera de la bóveda solicitada o de las rutas de entrada explícitas.
- La solicitud entra en conflicto con la determinación, la salida JSON-first o el procesamiento local-first.
- La solicitud forzaría la eliminación o sobrescritura de contenido del usuario que no está explícitamente dentro del alcance.

## Verificación
- Prefiere verificaciones rápidas y reproducibles:
  - comprobaciones de sintaxis de shell para scripts
  - smoke tests para directorios generados y salida de ayuda
  - validación de forma JSON para ejemplos de salida cuando se agreguen ejemplos
- Si la verificación no es posible en el entorno actual, indícalo claramente en la entrega final.
- Antes de cerrar un cambio, verifica solo la superficie tocada. No ejecutes reconstrucciones amplias salvo que sea necesario para demostrar corrección.
