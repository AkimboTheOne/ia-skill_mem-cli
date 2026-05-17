# Esquemas de Salida

`schema_version: 1` es obligatorio en todo payload JSON emitido por `mem-cli`.

## Regla de idioma

Escribe en español el texto humano de esta documentación. Conserva en inglés solo los identificadores técnicos que formen parte del contrato.

## Campos Comunes

- `schema_version`: versión entera del esquema.
- `command`: nombre del comando.
- `vault`: ruta de bóveda resuelta cuando el comando opera sobre una bóveda.

## Campos Específicos por Comando

- `init`: `created`
- `add`: `requested`, `added`, `missing`, `count`
- `index`: `files_indexed`, `captures_indexed`, `captures`
- `connect`: `days`, `connections`, `connections_count`, `status`
- `brief`: `topic`, `one_thing`, `proof`, `reader_transformation`, `three_hooks`, `three_closers`, `status`
- `status`: `exists`, `layout`, `artifacts`

## Regla de Contrato

No agregues ni elimines campos sin actualizar en el mismo cambio el contrato de comandos, el contrato de comportamiento y los ejemplos canónicos.
