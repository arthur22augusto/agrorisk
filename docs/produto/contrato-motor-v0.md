# Contrato do motor v0 (provisório)

- Data: 2026-10-29 · Status: **provisório** · Sessão 06b. Itens marcados ⚠️ **dependem da sessão 06** (Y e unidade finais) e podem mudar.
- O contrato é genérico: vale para operação de crédito (frente A) e fornecedor (frente B). Em vez de nomes presos a crédito, usa `unidade_id` + `tipo_unidade`, e o Y é identificado por `evento` + `horizonte_meses`.
- Implementação de referência: **stub** em `src/agrorisk/motor/` (números de mentira, mesmo formato). Dados de teste: `tests/fixtures/sinteticos/` (gerados por `agrorisk.sinteticos`, tudo fictício).
- Dono dos dados: a estatística entrega os **indicadores** de dados públicos; o dev entrega **unidades** e **operações** do cliente. O motor não lê dado bruto.

## 1. O que o motor lê

Nomes de tabela no banco: `motor_indicadores`, `motor_unidades`, `motor_operacoes` (opcional). Em diretório: `indicadores|unidades|operacoes` `.parquet` ou `.csv`. Chaves lógicas: `unidade_id`; `(unidade_id, data_corte)`.

### 1.1 `indicadores` — uma linha por unidade × data de corte
| coluna | tipo | unidade | nulo | exemplo |
|---|---|---|---|---|
| `unidade_id` | texto | — | não | `GLB0007-2` |
| `data_corte` | data | — | não | `2023-01-01` |
| `pct_veg_nativa` | float | % (0–100) | não | `34.2` |
| `supressao_viz_ha_3a` | float ≥0 | ha, vizinhança, últimos 3 anos | não | `5.1` |
| `dist_urbano_km` | float ≥0 | km | não | `4.3` |
| `dist_mineracao_km` | float ≥0 | km | não | `9.8` |
| `sobreposicao_uc_pct` | float | % da área em UC (0–100) | não | `0.0` |
| `chuva_anual_mm` | float | mm, ano de referência | não | `1385` |

⚠️ O conjunto de colunas é o do stub; o motor real pode exigir outras (definidas após o Y). Colunas extras são ignoradas. Cada fator tem **defasagem de publicação** declarada no código (`motor/fatores.py`): o motor deriva `data_referencia` e `data_publicacao` do último ano cuja publicação é ≤ `data_corte`, e falha com `ErroVazamentoTemporal` se isso for impossível. O responsável pelo pipeline garante que o valor entregue em `indicadores` foi calculado só com dados publicados até a `data_corte`.

### 1.2 `unidades` — uma linha por unidade
| coluna | tipo | unidade | nulo | exemplo |
|---|---|---|---|---|
| `unidade_id` | texto, único | — | não | `GLB0007-2` |
| `tipo_unidade` | `gleba` \| `imovel` \| `fornecedor` | — | não | `gleba` |
| `nivel_espacial` | `gleba` \| `imovel_inteiro` | — | não | `imovel_inteiro` |
| `car_codigo` | texto | `MG-<IBGE7>-<32 hex>` | sim | `MG-3106200-00000000…` |
| `municipio_ibge` | texto (7 díg.) | — | sim | `3106200` |
| `area_ha` | float | ha | sim | `42.5` |
| `geometria_wkt` | texto WKT, EPSG:4674 | — | sim | `POLYGON((…))` |
| `valor_exposto` | float | R$ | sim | `150000.00` |

`valor_exposto` é o saldo/valor em risco **na data de corte** (snapshot). Se ausente, o motor o calcula com `exposicao_na_data(operacoes, data_corte)` quando há `operacoes` (CLI faz isso); sem operações, `exposicao_esperada` sai nula.

### 1.3 `operacoes` (opcional; crédito e fornecimento)
`operacao_id` (texto), `unidade_id`, `tipo_operacao` (`custeio`\|`investimento`\|`fornecimento`), `produto_cultura`, `safra` (`2021/22`), `valor_rs` (R$), `data_inicio`, `data_fim` (datas; vigente em `[inicio, fim)`). ⚠️ O dev define o schema definitivo (ver `perguntas-dev-v0.md` §1: a ligação operação ↔ CAR/gleba vem da cooperativa, não do SICOR público).

## 2. O que o motor grava

### 2.1 `motor_resultados` — chave única `(unidade_id, data_corte, evento, versao_modelo)`
| coluna | tipo | nulo | descrição |
|---|---|---|---|
| `unidade_id`, `tipo_unidade` | texto | não | copiados de `unidades` |
| `data_corte` | data | não | |
| `evento` | texto | não | identifica o Y. Stub: `supressao_vegetacao` ⚠️ |
| `horizonte_meses` | int | não | Stub: 12 ⚠️ |
| `versao_modelo` | texto | não | `semver[-stub]+<hash git>`, ex. `0.1.0-stub+4baa920c1d2e` |
| `p` | float [0,1] | não | P(evento em `horizonte_meses` após `data_corte`) |
| `score` | int [0,1000] | não | `round(1000·(1−p))`, meio para cima |
| `faixa` | `A`–`E` | não | ver §3 |
| `taxa_base` | float | não | taxa-base usada nas faixas. Stub: 0,02 ⚠️ |
| `valor_exposto` | float R$ | sim | |
| `exposicao_esperada` | float R$ | sim | `p × valor_exposto`. **Exposição, não perda** |
| `nivel_espacial` | texto | não | cópia da entrada |
| `aviso` | texto | sim | preenchido se `imovel_inteiro` (§5) |
| `versoes_dados` | JSON texto | não | `{"fonte": "versão ou data de publicação"}` |
| `calculado_em` | timestamp ISO | não | informativo; **não** faz parte da chave |

### 2.2 `motor_resultados_detalhes` — uma linha por fator, chave `(unidade_id, data_corte, evento, versao_modelo, fator)`
Colunas: as da chave + `ordem` (1 = maior |contribuição|) + `valor`, `unidade`, `contribuicao`, `direcao`, `fonte`, `data_referencia`, `data_publicacao`, `texto`. Para a tela, o dev monta a lista `detalhes` (um objeto por linha, ordenado por `ordem`, só com os 9 campos) e ela deve validar em [`schemas/detalhes.schema.json`](schemas/detalhes.schema.json):

```json
[{"fator": "supressao_vizinhanca", "valor": 12.4, "unidade": "ha", "contribuicao": 1.31,
  "direcao": "aumenta_risco", "fonte": "MapBiomas Desmatamento (sintético)",
  "data_referencia": "2021-12-31", "data_publicacao": "2022-09-27",
  "texto": "Supressão recente na vizinhança do imóvel acima do típico."}]
```
`contribuicao` está em log-odds (positivo aumenta o risco). `data_publicacao` ≤ `data_corte`, sempre.

## 3. Fórmulas
- `p` ∈ [0,1], float. Stub: logística com ruído determinístico, intercepto calibrado para média = taxa-base no lote (p não é calibrado de verdade). ⚠️ O motor real será calibrado e validado por backtest temporal.
- `score = round(1000·(1−p))`. Score alto = risco baixo.
- `faixa` pela razão `p / taxa_base`: **A** ≤0,5× · **B** ≤1× · **C** ≤2× · **D** ≤4× · **E** >4× (limites superiores inclusivos). ⚠️ A taxa-base depende do Y e do recorte.
- `exposicao_esperada = p × valor_exposto` (R$).

## 4. Contrato de execução
- **Conexão:** o motor abre a **própria** conexão, pela variável `AGRORISK_DB_URL` (URL SQLAlchemy, ex. `postgresql+psycopg://usuario:senha@host/db`); não depende do Django nem do ORM dele. Ele cria as tabelas `motor_resultados*` se não existirem (com índice único da chave); o dev pode criá-las antes via migration, desde que mantenha nomes, colunas e a chave.
- **Chamada em Python:** `pontuar(indicadores, unidades, data_corte, *, evento, horizonte_meses, taxa_base, versoes_dados) -> (resultados, detalhes)` (DataFrames pandas, sem efeitos colaterais). **CLI:** `python -m agrorisk.motor --entrada <dir|db> --saida <dir|db> [--data-corte AAAA-MM-DD]`; `db` lê `AGRORISK_DB_URL`; uma URL SQLAlchemy também vale.
- **Exceções** (`agrorisk.motor`) e **códigos de saída:** `ErroEntrada` → 2 (tabela/coluna ausente, duplicata, valor inválido, nenhum dado na data de corte) · `ErroConexao` → 3 · `ErroVazamentoTemporal` → 4 · `ErroModelo` → 5 (modelo ausente; o stub não usa) · qualquer outra falha → 1 · sucesso → 0. Mensagem em stderr; em erro de entrada nada é gravado; no banco cada tabela é gravada em uma transação (resultados e detalhes em transações separadas — ⚠️ unificar na versão real).
- **Idempotência:** upsert por `(unidade_id, data_corte, evento, versao_modelo)`; rodar 2× não duplica. Versão de modelo nova gera linhas novas (o histórico é preservado).
- **`versao_modelo`:** semver + hash do git (`AGRORISK_GIT_HASH` > `direct_url.json` da instalação via git > `git rev-parse` > `desconhecido`).
- **`versoes_dados`:** JSON `{fonte: versão/data de publicação}` ⚠️ o stub grava só `{"origem": "cli"}`; o pipeline real preenche com as versões congeladas de cada base.
- **Determinismo:** semente fixa (20261029); mesma entrada → mesma saída.

## 5. `nivel_espacial`
`gleba` = indicadores calculados na gleba financiada/fornecedora; `imovel_inteiro` = fallback quando a gleba não foi informada. O motor calcula igual, **não reduz p artificialmente**, grava `nivel_espacial` e preenche `aviso` ("Indicadores calculados sobre o imóvel inteiro…") para a tela exibir. O backtest mede o desempenho dos dois níveis separadamente.

## 6. Empacotamento e instalação
- Python ≥3.11. `uv add git+https://github.com/arthur22augusto/agrorisk` (ou `@<tag|commit>` para travar a versão).
- **Núcleo leve:** pandas, numpy, pyarrow, sqlalchemy (pyarrow para Parquet; SQLAlchemy para o banco). Driver do Postgres (`psycopg[binary]`) é do dev.
- **Extras:** `[modelo]` = lightgbm (motor real) · `[pipeline]` = geopandas, shapely, duckdb, rasterio (geoprocessamento; **o dev não precisa**) · `[dev]` = pytest, jsonschema, psycopg.
- **Modelos treinados** ficam fora do git, em `AGRORISK_MODELO_DIR` (⚠️ formato e nomes de arquivo a definir quando houver modelo; o stub ignora a variável).

## 7. Lista do que depende da sessão 06 ⚠️
1. `evento` e `horizonte_meses` (Y) e `taxa_base` — hoje `supressao_vegetacao`, 12, 2%.
2. Conjunto, nomes e unidades dos indicadores e dos fatores (hoje 6 fatores sintéticos).
3. `tipo_unidade` e granularidade final (gleba, imóvel, fornecedor, operação).
4. Schema de `operacoes` e o cálculo de `valor_exposto` (depende do cliente/frente).
5. Formato dos modelos em `AGRORISK_MODELO_DIR`; conteúdo de `versoes_dados`.
6. Calibração: no stub, `p` não é probabilidade calibrada; os números só servem para testar integração.

## 8. O que NÃO muda (alvo de estabilidade)
Nomes das tabelas de saída e da chave de upsert, fórmulas de `score`/`faixa`/`exposicao_esperada`, os 9 campos de `detalhes`, a variável `AGRORISK_DB_URL`, códigos de saída e a assinatura de `pontuar`.
