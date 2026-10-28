# Scripts da sessão 01 (diagnóstico territorial)

Scripts de consulta usados para gerar os números de `docs/pesquisa/01-diagnostico-territorial.md`.
**Não há dados aqui** (regra 4 do `CLAUDE.md`). Execução em 2026-10-28.

- Cada script espera ser executado dentro de uma pasta de trabalho com `municipios.csv` (gerado por `s01_municipios.py`)
  e `raw/` (downloads). Nada disso é versionado; use `data/raw` e `data/interim` ao reaproveitar.
- Ordem: `s01` (municípios) → `s02` (MapBiomas) → `s03_*` (PRODES, focos, fogo, IBAMA, IDE-Sisema) → `s04` (CAR)
  → `s05` (sumário de Y) → `s08` (eventos PRODES por imóvel CAR) → `s09` (figuras).
- Requer GeoPandas, pandas, openpyxl e `curl` (o SICAR falha no handshake TLS com `urllib`).
- Os caminhos dentro dos scripts são relativos à pasta de trabalho e podem precisar de ajuste.
- Os scripts são exploratórios (sessão de pesquisa); a versão reutilizável vai para `src/agrorisk/` na sessão 07.
