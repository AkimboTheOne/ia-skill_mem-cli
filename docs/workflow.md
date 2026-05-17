# Flujo de Trabajo

Flujo de uso recomendado:

1. Inicializa una bóveda.
2. Agrega archivos o carpetas al flujo de inbox/captura.
3. Indexa la bóveda para normalizar y catalogar el contenido.
4. Genera conexiones heurísticas a partir del contenido indexado.
5. Produce un brief para un tema cuando se necesite síntesis.
6. Revisa el estado para confirmar que la bóveda está sana.

## Ejemplo

```bash
$mem-cli init --vault ./mem-cli-vault
$mem-cli add ./src ./docs
$mem-cli index --vault ./mem-cli-vault
$mem-cli connect --vault ./mem-cli-vault --days 7
$mem-cli brief --vault ./mem-cli-vault --topic "refactor patterns"
$mem-cli status --vault ./mem-cli-vault
```
