# Contratos

Este archivo es un resumen corto para humanos. El contrato autoritativo vive en `SKILL.md` y `references/`.

## Comandos

- `init`: crea el layout de directorios de la bóveda.
- `add`: captura archivos o carpetas dentro del flujo de la bóveda.
- `index`: indexa archivos o un árbol de bóveda.
- `connect`: deriva enlaces heurísticos a partir del contenido capturado.
- `brief`: genera un resumen temático a partir del contenido preparado.
- `status`: reporta la salud e inventario de la bóveda.

## Política de Salida

- La salida principal legible por máquina debe ser JSON.
- La salida TTY para humanos puede ser texto legible, pero debe reflejar los mismos datos subyacentes.
- Los fallos deben ser explícitos y estructurados cuando sea posible.

## Frontmatter

Los archivos Markdown capturados deben preservar un bloque de frontmatter YAML con campos como:

```yaml
---
created: 2026-05-17T12:00:00Z
type: source
status: new
source: local
tags: [tag1, tag2]
source_file: path/to/file
---
```

Consulta `references/frontmatter-example.md` para la forma canónica.
