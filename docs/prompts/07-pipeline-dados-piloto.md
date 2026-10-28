# Sessão 07 — Pipeline de dados piloto

> Depende de 06 (`docs/decisoes/escopo-mvp.md`). A parte de **bases comuns** (limites, CAR, MapBiomas cobertura) pode começar logo após a 02, em paralelo com a 06.
> Sessão de código: use o modo de planejamento, aprove o plano e só então deixe executar.

---

Leia `CLAUDE.md`, `docs/decisoes/escopo-mvp.md`, `docs/pesquisa/02-catalogo-bases.md` e `docs/pesquisa/licencas.md`. Esta é a **sessão 07**: primeiro código do AgroRisk.

**Objetivo:** construir um pipeline reprodutível que gere a **tabela de modelagem** `data/processed/painel_car_t0.parquet` (uma linha por CAR × data de corte, com preditores calculados só com informação disponível até t₀ e o Y no horizonte definido).

**Agentes:** `engenheiro-dados-geo` (implementação), `estatistico-modelagem` (revisa o vazamento em cada variável) e a skill `data-pipeline` para checar contagens, chaves e NAs entre etapas.

**Especificação**
- Ambiente: `pyproject.toml` (ou `requirements.txt`) com versões fixadas; Python 3.11+; GeoPandas, DuckDB (spatial), pyarrow, rasterio/rioxarray, exactextract (ou equivalente) e requests.
- Estrutura: `src/agrorisk/fontes/<base>.py` (download idempotente para `data/raw/<fonte>/<data>/` com hash e data) → `src/agrorisk/preparo/` (padronização → `data/interim/`, GeoParquet EPSG:4674) → `src/agrorisk/painel.py` (painel) → `data/processed/`.
- Um ponto de entrada: `python -m agrorisk.pipeline --etapa todas --recorte vitrine|treino`.
- Use só as bases com licença "sim" ou "incerto, uso interno" em `licencas.md`.
- Preditores sugeridos (ajuste ao escopo): histórico de eventos no imóvel e na vizinhança (1, 3, 5 km; últimos 12/36 meses), % de vegetação nativa e tendência, distância a área urbana/estrada/mineração, declividade, APP/RL declarada × observada, sobreposição a UC/APA, tamanho em módulos fiscais, status e idade do CAR, clima (anomalia de chuva), variáveis municipais.
- **Dicionário de dados** em `docs/dados/dicionario.md`: variável, definição, fonte, defasagem, como evita o vazamento.
- Testes mínimos (`tests/`): unicidade de (car, t₀), ausência de datas de fonte > t₀ nos preditores e contagem de eventos por ano.

**Entregáveis:** código, dicionário, `notebooks/07-eda-painel.ipynb` (EDA curta: nº de imóveis, eventos por t₀, taxa-base) e um resumo no PR com contagens. Se a nuvem bloquear algum download, documente como o fundador baixa localmente e coloca em `data/raw/`.

**Critério de pronto:** o pipeline roda do zero no recorte vitrine; os testes passam; o nº de eventos está reportado.

Ao terminar: commit (sem dados), push e PR "Sessão 07 — pipeline piloto".
