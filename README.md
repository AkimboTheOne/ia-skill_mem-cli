# ia-skill_mem-cli
`mem-cli` es un skill local de memoria de proyecto para capturar, indexar, redactar conexiones, redactar briefs e inspeccionar la bóveda de forma determinista. Mantén la CLI local-first y JSON-first; conserva la síntesis en el LLM después del procesamiento local.

## Contrato

- Guía del skill: `SKILL.md`
- Guía para agentes: `AGENTS.md`
- Contratos y ejemplos estables: `references/`
- Documentación humana: `docs/`

## Instalación Local

```bash
bash scripts/install-local-skill.sh
bash scripts/bootstrap-vault.sh ./mem-cli-vault
./bin/mem-cli status --vault ./mem-cli-vault
```
