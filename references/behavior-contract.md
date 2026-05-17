# Contrato de Comportamiento

Este repositorio usa `schema_version: 1` para todas las salidas legibles por máquina.

## Regla de idioma

Escribe en español el texto humano de esta documentación. Conserva en inglés solo los identificadores técnicos que formen parte del contrato.

## Reglas Globales

- La salida es JSON por defecto.
- `--format tty` produce texto estable y legible por humanos.
- Los comandos son deterministas para las mismas entradas.
- Las escrituras en la bóveda se limitan a la bóveda solicitada y a sus subdirectorios administrados.
- La ingesta de Markdown normaliza el frontmatter pero preserva los campos semánticos explícitos cuando están presentes.

## Reglas de Ingesta

- Los archivos Markdown van a `01-CAPTURES/`.
- Los archivos que no son Markdown van a `00-INBOX/`.
- Las rutas faltantes se reportan y no impiden procesar las entradas válidas.
- Las ingestas idénticas se deduplican por hash de contenido en el destino.
- Las claves existentes de frontmatter fuera del conjunto permitido se reportan como advertencias.

## Reglas de Indexación

- `index` lee capturas normalizadas desde `01-CAPTURES/`.
- Las capturas duplicadas se reportan cuando comparten la misma huella semántica.
- Los resultados de indexación se guardan en `.tmp/index.json`.

## Reglas de Brief

- `brief` escribe su artefacto en `03-BRIEFS/` y `.tmp/brief.json`.
- El nombre del archivo se deriva del slug del tema.
- El payload debe incluir el tema y los campos canónicos del brief.
- Los artefactos generados de conexiones y briefs son borradores hasta que los revise un humano o el LLM.
