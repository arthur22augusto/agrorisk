# data/

Nada aqui é versionado, exceto este README e os `.gitkeep`.

| Pasta | Conteúdo | Regra |
|---|---|---|
| `raw/` | arquivos como baixados, organizados por `fonte/AAAA-MM-DD/` | imutável; nunca editar à mão |
| `interim/` | dados limpos e padronizados (GeoParquet, EPSG:4674) | reconstruível a partir de `raw/` |
| `processed/` | tabelas de modelagem (CAR × data de corte × variáveis × Y) | reconstruível a partir de `interim/` |

Cada base baixada precisa de uma linha em `docs/pesquisa/licencas.md` antes de ser usada.
