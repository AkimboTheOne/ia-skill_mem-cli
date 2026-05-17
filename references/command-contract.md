# Contrato de Comandos

Superficie canónica de comandos:

```text
mem-cli init --vault <path>
mem-cli add <path...>
mem-cli index --vault <path>
mem-cli connect --vault <path> --days <n>
mem-cli brief --vault <path> --topic <text>
mem-cli status --vault <path>
```

## Comportamientos Requeridos

- Los comandos deben ser deterministas para las mismas entradas.
- Los comandos deben emitir JSON por defecto.
- Los comandos no deben mutar fuera de la bóveda o de las rutas de entrada explícitas.
- Los comandos deben mantener `.tmp/` como efímero.
