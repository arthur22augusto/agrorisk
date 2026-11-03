# Dicionário de dados — `data/processed/painel_car_t0.parquet`

Uma linha por **CAR × data de corte** (chave `(cod_imovel, data_corte)`). Gerado por `python -m agrorisk.pipeline --etapa todas --recorte vitrine` (código: `src/agrorisk/painel.py`).
`t0 = data_corte = 31/jul/(y−1)`; `ano_prodes = y` (ciclo ago/(y−1)–jul/y); horizonte h = 12 meses. Inclusão: CAR inscrito há ≥ 6 meses em t0; cancelados permanecem.
**Limitações declaradas:** (1) geometria e `m_fiscal` do CAR são os **vigentes** (snapshot 2026-11-03; sem versões antigas) → retrospectivo exploratório; (2) o filtro "≥ 1 ha de vegetação nativa em t0" **não foi aplicado** (MapBiomas bloqueado na nuvem; ver `docs/pesquisa/07-gate-do-y.md`); (3) declividade, clima e % nativa/tendência não entraram.
Convenção anti-vazamento: preditores PRODES usam anos ≤ y−2 (o ciclo y−1 termina em t0 e só é publicado ~3–4 meses depois; data real de publicação dos polígonos **não verificada**).

| Variável | Definição | Fonte | Defasagem / data de referência | Como evita vazamento |
|---|---|---|---|---|
| `cod_imovel` | Código do CAR (SICAR) | SICAR WFS `sicar_imoveis_mg` | snapshot 2026-11-03 | identificador; sem CPF/nome |
| `data_corte` | t0 (31/jul) | convenção | — | — |
| `ano_prodes` | Ano-PRODES do rótulo (y) | convenção | — | rótulo, não preditor |
| `cod_municipio_ibge` | Município (7 dígitos) | SICAR | vigente | estático |
| `porte_modulos_fiscais` | `m_fiscal` do SICAR (módulos fiscais) | SICAR | **vigente** | valor atual; aceito como proxy do porte (exploratório) |
| `classe_porte` | ≤4MF / 4-15MF / >15MF | derivada | idem | idem |
| `area_ha` | Área do polígono do CAR (EPSG:31983) | SICAR | **vigente** | geometria atual; retificações posteriores a t0 podem alterá-la (93% dos positivos têm `data_atualizacao` > t0) |
| `status_imovel` | AT/PE/SU/CA | SICAR | **vigente** | cancelados mantidos; status atual (limite) |
| `idade_car_meses` | Meses entre `dat_criacao` e t0 | SICAR | criação ≤ t0−6 meses | só passado |
| `hist_imovel_ha_12m` | Área (ha) de supressão PRODES dentro do imóvel no ano y−2 | PRODES | publicação ≥ 4 meses após 31/jul/(y−2) | só ano ≤ y−2 |
| `hist_imovel_ha_36m` | Idem, anos y−4 a y−2 | PRODES | idem | idem |
| `hist_imovel_n_anos_36m` | Nº de anos com supressão no imóvel (y−4..y−2) | PRODES | idem | idem |
| `viz_{1,3,5}km_ha_{12m,36m}` | Soma da área (ha) dos polígonos PRODES que tocam o anel de 1/3/5 km do imóvel, **excluindo** os que tocam o próprio imóvel (área total do polígono, não recortada) | PRODES | idem | só anos ≤ y−2 |
| `dist_evento_36m_m` | Distância (m) ao polígono PRODES mais próximo de y−4..y−2 (0 = dentro/encostado) | PRODES | idem | idem; efeito de borda do recorte (eventos fora do bbox) |
| `taxa_municipio_36m` | Eventos ≥1 ha (CAR×ano) no município em y−4..y−2 ÷ CARs elegíveis do município em t0 | PRODES + CAR | idem | só anos ≤ y−2; numerador usa a geometria atual do CAR |
| `embargo_sisema_ate_t0` | CAR toca área embargada Sisema com data do ato ≤ t0 (**sem cobertura: a camada só tem atos de 2025–26 → constante 0 em todos os t0 do painel; reservada para o futuro**) | IDE-Sisema `ide_2304` | data do ato (`data_fisca`); **data de publicação não verificada** | filtra por data do ato ≤ t0; risco de embargos inseridos/retificados depois (limite) |
| `embargo_data_min` | Menor data de ato de embargo ≤ t0 | idem | idem | idem |
| `prodes_ano_max_usado` | Último ano-PRODES usado nos preditores (= y−2) | — | — | usado pelo teste de não-vazamento |
| `vig_uc_frac` | Fração do CAR dentro de UC (est./fed./mun.) | IDE-Sisema | **vigente (2026-11-03)** | **NÃO é preditor limpo** (sem data de criação das UCs); fora de `PREDITORES_DATADOS` |
| `Y_total` | 1 se há ≥ 1 ha **contíguo** de supressão PRODES no CAR no ciclo y | PRODES | — | rótulo (futuro de t0) |
| `Y_agro` | `Y_total` ∧ destino não minerário/urbano (< 50% do evento em SIGMINE lavra/licenciamento ou IBGE urbanizada 2022) | PRODES + SIGMINE (atual) + IBGE | fotos atuais | rótulo; subestima não-agro dos anos iniciais |
| `Y_ilegal` | `Y_total` ∧ **sem autorização identificada** (IEF datada ±12 meses do ciclo, ou FEAM sem data; interseção ≥ 10% do evento) | IDE-Sisema | IEF só cobre 2021–26 | rótulo; **≈ `Y_total` por falta de cobertura**; não é "ilegal" |
| `diag_geom_atualizada_pos_t0` | `data_atualizacao` do CAR > t0 | SICAR | — | **diagnóstico** (usa informação posterior); não usar como preditor |

Conjunto de preditores sem vazamento conhecido: `agrorisk.painel.PREDITORES_DATADOS`. Colunas `vig_*` e `diag_*` não entram.
