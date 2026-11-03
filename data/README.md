# data/

Nada aqui é versionado, exceto este README e os `.gitkeep`.

| Pasta | Conteúdo | Regra |
|---|---|---|
| `raw/` | arquivos como baixados, organizados por `fonte/AAAA-MM-DD/` | imutável; nunca editar à mão |
| `interim/` | dados limpos e padronizados (GeoParquet, EPSG:4674) | reconstruível a partir de `raw/` |
| `processed/` | tabelas de modelagem (CAR × data de corte × variáveis × Y) | reconstruível a partir de `interim/` |

Cada base baixada precisa de uma linha em `docs/pesquisa/licencas.md` antes de ser usada.

## Download manual quando a nuvem bloqueia (sessão 07)
- **MapBiomas Cobertura/Transição Col. 11** (`storage.googleapis.com/mapbiomas-public` retorna 403 no proxy da nuvem): baixar localmente o recorte do bbox
  do snapshot de treino (`data/raw/snapshots/<data>/treino/manifest.json`, campo `bbox_sisema`) a partir do STAC
  `https://storage.googleapis.com/mapbiomas-public/stac/catalog.json` e colocar em `data/raw/mapbiomas/AAAA-MM-DD/` com o `manifest.json` (URL, data, sha256).
- **PRODES do treino** (TerraBrasilis, bbox grande; o `curl` falha com erro TLS 35 de forma intermitente): `python -m agrorisk.fontes.prodes --bbox "<bbox>" --data <data>-treino`.
