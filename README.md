# AgroRisk

Inteligência de risco socioambiental para o mercado rural: **transformar sustentabilidade em valor
econômico mensurável**, com estatística, geoprocessamento e otimização sobre dados públicos.

**Status:** fase de pesquisa e definição do MVP (out/2026). Ainda não há código de análise.

## Foco atual
- **Região vitrine:** Minas Gerais — RMBH + Colar Metropolitano + Sete Lagoas (Cerrado / Mata Atlântica).
- **Hipótese de MVP:** priorização de carteira de CARs — prever P(evento socioambiental relevante em
  12–24 meses), ranquear, explicar, validar por backtest temporal e prescrever onde agir sob orçamento.
- **Cliente-alvo provisório:** crédito rural para pequenos e médios produtores (cooperativas e bancos).

## Por onde começar
| Você quer… | Leia |
|---|---|
| Entender o negócio | [`docs/AgroRisk_proposta_v2.pdf`](docs/AgroRisk_proposta_v2.pdf) |
| Regras do projeto (também lidas pelo Claude) | [`CLAUDE.md`](CLAUDE.md) |
| Aprender a usar o Claude Code na nuvem | [`docs/GUIA.md`](docs/GUIA.md) |
| Rodar a próxima sessão | [`docs/prompts/README.md`](docs/prompts/README.md) |
| Ver decisões tomadas | [`docs/decisoes/`](docs/decisoes/) |
| Ver pesquisas e licenças | [`docs/pesquisa/`](docs/pesquisa/) |

## Estrutura
```
.claude/agents/   subagentes especialistas (mercado, dados, academia, crédito, estatística, comprador, crítico)
.claude/skills/   procedimentos reutilizáveis (pipeline, revisão de código, pptx, postgresql…)
data/             dados locais — fora do git (raw → interim → processed)
docs/             proposta, guia, decisões, pesquisa, prompts
notebooks/        exploração numerada (NN-descricao.ipynb)
reports/          entregáveis (Excel, relatórios, mapas, figuras leves)
src/agrorisk/     código Python do pipeline, modelos e relatórios
```

## Stack
Python 3.11+ · GeoPandas · DuckDB (spatial) · GeoParquet · scikit-learn/LightGBM · (futuro) PostgreSQL/PostGIS.

## Licença
Ver [`LICENSE`](LICENSE). As bases de dados de terceiros têm licenças próprias, registradas em
[`docs/pesquisa/licencas.md`](docs/pesquisa/licencas.md).
