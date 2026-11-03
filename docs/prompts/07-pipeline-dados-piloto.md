# Sessão 07 — Pipeline de dados piloto

> Depende de 06 (`docs/decisoes/escopo-mvp.md`, aceita em 2026-10-29: frente A-reformulada; Y = supressão PRODES ≥ 1 ha por CAR, h = 12, t₀ = 31/jul; **Y provisório até o gate abaixo**). A parte de **bases comuns** (limites, CAR, MapBiomas cobertura) pode começar logo após a 02, em paralelo com a 06.
> Sessão de código: use o modo de planejamento, aprove o plano e só então deixe executar.

---

Leia `CLAUDE.md`, `docs/decisoes/escopo-mvp.md`, `docs/pesquisa/02-catalogo-bases.md` e `docs/pesquisa/licencas.md`. Esta é a **sessão 07**: primeiro código do AgroRisk.

**Objetivo:** construir um pipeline reprodutível que gere a **tabela de modelagem** `data/processed/painel_car_t0.parquet` (uma linha por CAR × data de corte, com preditores calculados só com informação disponível até t₀ e o Y no horizonte definido).

**Agentes:** `engenheiro-dados-geo` (implementação), `estatistico-modelagem` (revisa o vazamento em cada variável) e a skill `data-pipeline` para checar contagens, chaves e NAs entre etapas.

**Etapa 0 — Gate do Y (fazer ANTES do painel, ~5–8 h; ver `escopo-mvp.md` §3).** Com os dados da 01 recarregados em `data/raw/`: (a) fração dos eventos PRODES ≥ 1 ha em imóveis ≤ 4 MF (campo `mod_fiscal`); (b) fração em mineração/urbano (SIGMINE e MapBiomas / matriz de transição); (c) fração com autorização IEF/FEAM (janela ±12 meses); (d) estabilidade da geometria do CAR (`dat_criaca`/`dat_atuali` × eventos); (e) fração dos flags de t+12 que já estavam em evento prévio ou vizinhança em t₀; (f) leitura do MCR 2-9 (UC, embargo estadual); (g) nº de eventos no recorte ampliado (Metropolitana + Central Mineira); (h) data de publicação do PRODES por ciclo. Registre em `docs/pesquisa/07-gate-do-y.md`. **Regra:** se < ~30% dos positivos sobrarem como Y_agro sem autorização identificada em ≤ 4 MF, ou se (e) mostrar que o histórico explica quase tudo, **pare e reabra o escopo** (nova decisão). Escolha o Y primário (Y_total ou derivado) e congele o protocolo (commit/hash) antes da sessão 08. Crie também o script de **snapshots mensais com hash** do CAR e da IDE-Sisema (ver `escopo-mvp.md` §4).

**Especificação**
- Ambiente: `pyproject.toml` (ou `requirements.txt`) com versões fixadas; Python 3.11+; GeoPandas, DuckDB (spatial), pyarrow, rasterio/rioxarray, exactextract (ou equivalente) e requests.
- Estrutura: `src/agrorisk/fontes/<base>.py` (download idempotente para `data/raw/<fonte>/<data>/` com hash e data) → `src/agrorisk/preparo/` (padronização → `data/interim/`, GeoParquet EPSG:4674) → `src/agrorisk/painel.py` (painel) → `data/processed/`.
- Um ponto de entrada: `python -m agrorisk.pipeline --etapa todas --recorte vitrine|treino`.
- Use só as bases com licença "sim" ou "incerto, uso interno" em `licencas.md`.
- Unidade e janelas (decisão 06): CAR × t₀ com t₀ = 31/jul; h = 12 meses (24 só descritivo); inscrito há ≥ 6 meses, ≥ 1 ha de nativa em t₀; cancelados no denominador; `porte_modulos_fiscais` no painel; colunas `Y_total`, `Y_ilegal` (sem autorização identificada), `Y_agro`. Camada de **vedações determinísticas** (supressão × autorização, embargo, UC) separada das variáveis de risco.
- Preditores sugeridos (ajuste ao escopo): histórico de eventos no imóvel e na vizinhança (1, 3, 5 km; últimos 12/36 meses), % de vegetação nativa e tendência, distância a área urbana/estrada/mineração, declividade, APP/RL declarada × observada, sobreposição a UC/APA, tamanho em módulos fiscais, status e idade do CAR, clima (anomalia de chuva), variáveis municipais.
- **Dicionário de dados** em `docs/dados/dicionario.md`: variável, definição, fonte, defasagem, como evita o vazamento.
- Testes mínimos (`tests/`): unicidade de (car, t₀), ausência de datas de fonte > t₀ nos preditores e contagem de eventos por ano.

**Entregáveis:** código, dicionário, `notebooks/07-eda-painel.ipynb` (EDA curta: nº de imóveis, eventos por t₀, taxa-base) e um resumo no PR com contagens. Se a nuvem bloquear algum download, documente como o fundador baixa localmente e coloca em `data/raw/`.

**Critério de pronto:** o pipeline roda do zero no recorte vitrine; os testes passam; o nº de eventos está reportado.

Ao terminar: commit (sem dados), push e PR "Sessão 07 — pipeline piloto".
