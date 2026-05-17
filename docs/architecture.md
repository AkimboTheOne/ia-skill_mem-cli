# Arquitectura

`mem-cli` es una CLI local de memoria con una frontera estricta:

- La CLI maneja operaciones del sistema de archivos, captura, indexación y contabilidad determinista.
- El LLM maneja la síntesis, el resumen y el juicio después de que los datos locales se hayan preparado.

## Principios Básicos

- Primero local: la bóveda es la fuente de verdad.
- Determinista primero: los comandos deben producir salida estable para las mismas entradas.
- JSON-first: la salida estructurada debe ser fácil de consumir por agentes.
- Amigable con Markdown: los archivos capturados permanecen legibles y portables.

## Responsabilidades de la Bóveda

- `00-INBOX/`: material entrante en bruto que espera procesamiento.
- `01-CAPTURES/`: capturas normalizadas con frontmatter.
- `02-CONNECTIONS/`: notas de relación y heurísticas.
- `03-BRIEFS/`: briefs temáticos y resúmenes sintetizados.
- `docs/`: documentación local del repositorio asociada con la bóveda.
- `.tmp/`: estado de trabajo transitorio, no fuente de verdad.

El contrato detallado de comandos vive en `references/` y `SKILL.md`.
