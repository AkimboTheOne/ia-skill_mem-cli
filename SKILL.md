---
name: mem-cli
description: Usa este skill para operar mem-cli y capturar, indexar, conectar, resumir o inspeccionar una bóveda de proyecto con flujos deterministas, JSON-first y compatibles con Markdown.
---

# mem-cli

Usa `mem-cli` como un skill local de memoria de proyecto. Mantén la CLI determinista, local-first y JSON-first. Trata al LLM como la capa de síntesis y juicio solo después del procesamiento local.

## Leer Primero

Antes de usar o cambiar el skill, lee:
- `AGENTS.md`
- `references/command-contract.md`
- `references/behavior-contract.md`
- `references/output-schemas.md`
- `README.md`

Si una solicitud entra en conflicto con esas fuentes, sigue el contrato del repositorio.

## Qué Hace el Skill

Usa `mem-cli` para:
- inicializar una bóveda
- agregar archivos o carpetas al flujo de la bóveda
- indexar capturas normalizadas
- derivar conexiones heurísticas
- generar un brief temático
- reportar el estado de la bóveda

No expandas la superficie de comandos salvo que el contrato se actualice en el mismo cambio.

## Reglas de Operación

- Mantén las escrituras dentro de la bóveda solicitada y de las rutas de entrada explícitas.
- Mantén `.tmp/` como algo efímero.
- Conserva el frontmatter de Markdown como YAML con los campos definidos en el contrato.
- Mantén `schema_version: 1` salvo que se apruebe explícitamente una migración.
- Prefiere scripts directos y comportamiento explícito sobre lógica oculta de framework.
- Trata las conexiones y briefs generados como borradores hasta que se revisen.

## Layout de la Bóveda

Usa este layout canónico:
- `00-INBOX/`
- `01-CAPTURES/`
- `02-CONNECTIONS/`
- `03-BRIEFS/`
- `docs/`
- `.tmp/`

## Superficie de Comandos

Los comandos soportados son:
- `init`
- `add`
- `index`
- `connect`
- `brief`
- `status`

La salida por defecto es JSON. La salida TTY, cuando esté soportada, debe reflejar los mismos datos subyacentes.

## Frontmatter

El Markdown capturado debe conservar frontmatter YAML con los campos del contrato. Normaliza campos faltantes, pero no inventes nuevos campos persistentes sin actualizar las referencias.

## Condiciones de Parada

Detente antes de editar si la solicitud:
- cambia la superficie pública de comandos
- cambia los campos del esquema o `schema_version`
- introduce una nueva carpeta de primer nivel o un artefacto persistente
- escribe fuera de la bóveda solicitada o de las rutas de entrada explícitas
- rompe el comportamiento determinista o JSON-first
