# ia-skill_mem-cli
`$mem-cli` es un skill local diseñado para operar una memoria local de proyecto, capturando archivos, indexando relaciones, generando conexiones y briefs. La inteligencia permanece delegada al LLM.

## Baseline

This repo now includes the baseline contract and supporting docs for the skill.

- Skill spec: `20260517_mem-cli_SKILL.md`
- Future agent guidance: `AGENTS.md`
- Installation helper: `scripts/install-local-skill.sh`
- Vault bootstrap helper: `scripts/bootstrap-vault.sh`
- CLI executable: `bin/mem-cli`
- Docs: `docs/`
- Stable examples and contracts: `references/`
- Contract docs: `references/output-schemas.md` and `references/behavior-contract.md`

## Local Setup

```bash
bash scripts/install-local-skill.sh
bash scripts/bootstrap-vault.sh ./mem-cli-vault
./bin/mem-cli status --vault ./mem-cli-vault
```
