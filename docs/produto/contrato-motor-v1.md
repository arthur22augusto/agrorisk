# Contrato do motor v1 (provisório)

- Data: 2026-11-03 · Status: **provisório** · Sessão 06c · **Substitui** [`contrato-motor-v0.md`](contrato-motor-v0.md) (histórico).
- Base: [`docs/decisoes/escopo-mvp.md`](../decisoes/escopo-mvp.md) (aceita em 2026-10-29), seção "Impacto no contrato do motor" e respostas 6–9. **Esta sessão não altera a decisão**; o que o ADR deixa ambíguo está em §9.
- Escopo: **frente A-reformulada** (crédito rural pós-concessão). O v0 era genérico (crédito + fornecedor); o v1 não tem `fornecedor` (frente B é só discovery, sem código).
- Implementação de referência: **stub** em `src/agrorisk/motor/` (números de mentira, mesmo formato). Dados de teste: `tests/fixtures/sinteticos/` (gerados por `agrorisk.sinteticos`, tudo fictício, sem dado real).
- Dono dos dados: a estatística entrega **indicadores** e **verificações** (dados públicos); o dev entrega **unidades** e **operações** do cliente. O motor não lê dado bruto.
- Schemas (validados nos testes): [`detalhes`](schemas/detalhes.schema.json) · [`verificacoes`](schemas/verificacoes.schema.json) · [`resultado`](schemas/resultado.schema.json).

## 0. O que mudou em relação ao v0

| Tema | v0 | v1 |
|---|---|---|
| Y | `evento` livre (`supressao_vegetacao`), cortes em 01/jan | `y_definicao` = `Y_total`; `data_corte` sempre **31/jul**; `horizonte_meses` = 12 |
| Camadas | só p | **verificações determinísticas** (vedação) separadas de **risco** (p); vedação não é feature |
| Nível espacial | `gleba`\|`imovel_inteiro` | `poligono`\|`imovel_inteiro`, obrigatório; **taxa-base e faixas por nível** |
| Unidade | `unidade_id` + `tipo_unidade` (`gleba`\|`imovel`\|`fornecedor`) | CAR ou gleba (`car`\|`gleba`); comercial = **operação + CAR (+ gleba)**; `porte_modulos_fiscais`, `programa`, `data_contrato` |
| Exposição | `exposicao_esperada = p × valor_exposto` | removida; no lugar, `exposicao_bloqueavel = saldo_exposto × bloqueio_provavel` (mecânica) |
| Y2 / Y3 | fora de escopo implícito | Y2 (Proagro) **removido**; `proagro_acionado` coluna opcional; Y3 só como rótulo opcional de piloto |
| Auditoria | `versao_modelo`, `versoes_dados` (`{"origem":"cli"}`) | + `hash_snapshot`, `versoes_dados` com `data_referencia`/`data_publicacao`/hashes por fonte, verificações com fonte+hash |
| LGPD | — | nenhuma coluna de CPF/nome; o motor **rejeita** (`ErroEntrada`) |
| `pontuar` | retorna `(resultados, detalhes)` | retorna `Saida(resultados, detalhes, verificacoes)` (3 DataFrames) |

## 1. Definição do Y (declarada, não livre)

- `y_definicao` ∈ {`Y_total`}. O motor **prevê `Y_total`**: supressão de vegetação nativa **≥ 1 ha contíguo dentro do polígono do CAR**, rótulo **PRODES** (Cerrado + Mata Atlântica), no ciclo ago–jul seguinte à data de corte. `Y_ilegal` (sem autorização identificada) e `Y_agro` (fora de mineração/urbano) são **derivados reportados em relatório**, não saídas do motor; pedir outro valor dá `ErroEntrada`.
- `horizonte_meses` = 12 (único aceito; 24 meses é descritivo, fora do motor). `data_corte` = 31/jul de cada ano (qualquer outra data → `ErroEntrada`).
- ⚠️ O Y é **provisório até o gate da sessão 07**; o Y primário da avaliação pode mudar. `y_definicao` existe para isso ser explícito na chave.
- "Sem autorização identificada" **não** significa "ilegal".

## 2. O que o motor lê

Nomes de tabela no banco: `motor_indicadores`, `motor_unidades`, `motor_operacoes` (opc.), `motor_verificacoes` (opc.), `motor_rotulos_piloto` (opc.). Em diretório: `indicadores|unidades|operacoes|verificacoes|rotulos_piloto` `.parquet` ou `.csv`. Colunas extras são ignoradas, **exceto** colunas de dado pessoal (§2.6).

### 2.1 `indicadores` — uma linha por unidade × data de corte (camada de risco)
Inalterada em relação ao v0: `unidade_id`, `data_corte` (31/jul), `pct_veg_nativa` (%), `supressao_viz_ha_3a` (ha), `dist_urbano_km`, `dist_mineracao_km`, `sobreposicao_uc_pct` (%), `chuva_anual_mm`; sem nulos. ⚠️ Conjunto do stub; o real depende do gate do Y. **Vedações (embargo, UC como proibição, supressão × autorização) não entram aqui como fator**: vão em `verificacoes`. O pipeline garante que cada valor foi calculado só com dados publicados até a `data_corte`; cada fator tem defasagem declarada em `motor/fatores.py` e o motor deriva `data_referencia`/`data_publicacao`, falhando com `ErroVazamentoTemporal` se for impossível.

### 2.2 `unidades` — uma linha por unidade (CAR ou gleba)
| coluna | tipo | nulo | descrição / exemplo |
|---|---|---|---|
| `unidade_id` | texto, único | não | `CAR0000` / `GLB0001-2` |
| `tipo_unidade` | `car` \| `gleba` | não | |
| `nivel_espacial` | `poligono` \| `imovel_inteiro` | **não (obrigatório)** | `car` ⇒ `imovel_inteiro`; `gleba` ⇒ `poligono` (o motor valida a coerência) |
| `car_codigo` | texto `UF-IBGE7-32hex` | **não** | `MG-3157807-…` |
| `porte_modulos_fiscais` | float ≥ 0 | **não** | tamanho do **imóvel (CAR)** em módulos fiscais, mesmo para gleba. Reporte: `ate_4_mf` (≤ 4), `4_a_15_mf`, `acima_15_mf` (> 15) |
| `municipio_ibge`, `area_ha`, `geometria_wkt` (EPSG:4674) | | sim | informativos |

`nivel_espacial = poligono` quando há geometria do polígono financiado (gleba); `imovel_inteiro` é o fallback (a unidade é o CAR). Ver §5.

### 2.3 `operacoes` (opcional) — unidade comercial = operação + CAR (+ gleba)
| coluna | tipo | nulo | descrição |
|---|---|---|---|
| `operacao_id` | texto, único | não | **pseudonimizado** (hash com sal do cliente) |
| `unidade_id`, `car_codigo` | texto | não | a unidade (CAR ou gleba) financiada; `car_codigo` deve coincidir com o da unidade |
| `tipo_operacao` | `custeio` \| `investimento` | não | |
| `programa` | texto | não | `pronaf`, `pronamp`, `demais_programas`… (lista aberta; ⚠️ §9) |
| `data_contrato`, `data_vencimento` | data | não | vigente em `[data_contrato, data_vencimento)` |
| `valor_rs` | float R$ | não | valor contratado; **proxy** do saldo |
| `saldo_rs` | float R$ | sim | saldo na data de corte, se o cliente entregar; tem prioridade sobre `valor_rs` |
| `produto_cultura`, `safra` | texto | sim | informativos |
| `proagro_acionado` | bool | sim | **opcional; o motor valida o tipo e não o usa** (Y2 fora do MVP) |

### 2.4 `verificacoes` (opcional, mas ver aviso) — camada determinística
Entregue pelo pipeline: **uma linha por ocorrência** (regra × unidade × data de corte × fonte). O motor **não decide** consequência legal: o pipeline informa `efeito`.

| coluna | tipo | descrição |
|---|---|---|
| `unidade_id`, `data_corte` | | `data_corte` = 31/jul |
| `regra` | snake_case | ex.: `supressao_x_autorizacao`, `embargo`, `sobreposicao_uc` (lista aberta; ⚠️ §9) |
| `efeito` | `bloqueia` \| `alerta` | só `bloqueia` entra em `bloqueio_provavel` |
| `status_juridico` | `detectado` \| `autorizado` \| `sem_autorizacao_identificada` \| `indeterminado` | |
| `fonte`, `texto` | texto | |
| `data_referencia`, `data_publicacao` | data | `data_referencia ≤ data_publicacao ≤ data_corte`; senão `ErroEntrada` / **`ErroVazamentoTemporal`** |
| `hash_fonte` | SHA-256 hex (64) | hash do snapshot da fonte usado |

Chave: `(unidade_id, data_corte, regra, fonte, hash_fonte)`. ⚠️ **Sem a tabela, o motor não avalia vedação**: `verificacoes_avaliadas = false` e `bloqueio_provavel`, `n_vedacoes*`, `exposicao_bloqueavel` saem **nulos** (não "zero"). Com a tabela, unidade sem linha = sem ocorrência (ver ⚠️ de cobertura em §9).

### 2.5 `rotulos_piloto` (opcional) — Y3, só no piloto
`operacao_id`, `data_corte`, `y3_atraso_90d` (0/1; atraso > 90 dias ou renegociação em 12 meses), `data_evento` (obrigatória se 1; **posterior** ao corte), `data_registro` (≥ `data_evento`; data do registro e do evento separadas, anti-vazamento). O motor só **valida** o formato (`validar_rotulos_piloto`); **não pontua com ele**. O painel operação × mês completo do piloto (decisão, pergunta 9) tem schema próprio, ainda não entregue ao repositório.

### 2.6 LGPD
Entradas pseudonimizadas; **nenhuma coluna de CPF/nome**. O motor rejeita com `ErroEntrada` colunas chamadas `cpf`, `cnpj`, `nome`, `nome_produtor`, `razao_social`, `rg`, `email`, `telefone` (qualquer caixa) em qualquer tabela. Armazenar só o necessário. Base legal e sigilo bancário (LGPD, LC 105/2001, Res. CMN 4.893/2021): **não verificados; validar com advogado antes de receber dado real**.

## 3. O que o motor grava

### 3.1 `motor_resultados` — chave `(unidade_id, data_corte, y_definicao, versao_modelo)`
Validado por [`resultado.schema.json`](schemas/resultado.schema.json).

| coluna | tipo | nulo | descrição |
|---|---|---|---|
| `unidade_id`, `tipo_unidade`, `car_codigo` | texto | não | |
| `data_corte` | data | não | 31/jul |
| `y_definicao`, `horizonte_meses` | texto, int | não | `Y_total`, 12 |
| `versao_modelo` | texto | não | `semver[-stub]+<hash git>`, ex. `0.2.0-stub+5358cae2c9a1` |
| `p` | float [0,1] | não | **P(Y_total em 12 meses após `data_corte`)**, no `nivel_espacial` da linha |
| `score` | int [0,1000] | não | `round(1000·(1−p))`, meio para cima |
| `faixa` | `A`–`E` | não | por `p / taxa_base` **do nível** (§4) |
| `taxa_base` | float | não | taxa-base do `nivel_espacial` da linha. Stub: 0,02 (`poligono`), 0,04 (`imovel_inteiro`) ⚠️ |
| `nivel_espacial`, `aviso` | texto | aviso: só nulo se `poligono` | `aviso` = rótulo "Evento no imóvel…" para `imovel_inteiro` |
| `porte_modulos_fiscais`, `porte_classe` | float, texto | não | para reporte por porte |
| `verificacoes_avaliadas` | bool | não | §2.4 |
| `bloqueio_provavel` | float [0,1] | sim | §3.3 (mecânica, **não** probabilidade estimada) |
| `n_vedacoes`, `n_vedacoes_indeterminadas` | int | sim | contagem de verificações `bloqueia` ocorridas / indeterminadas |
| `n_operacoes`, `saldo_exposto` | int, R$ | sim | operações vigentes na data de corte (nulos se não há `operacoes`) |
| `exposicao_bloqueavel` | R$ | sim | `saldo_exposto × bloqueio_provavel`. **Não é perda esperada** |
| `hash_snapshot` | SHA-256 | não | hash do conteúdo lógico das entradas lidas no corte (`indicadores`, `unidades`, `operacoes` vigentes, `verificacoes`) |
| `versoes_dados` | JSON texto | não | `{fonte: {data_referencia, data_publicacao, hashes?}}` — fatores de risco (derivados da defasagem declarada) + fontes das verificações |
| `calculado_em` | timestamp ISO | não | informativo; fora da chave |

`exposicao_esperada` **não existe no v1**: só voltará depois de desfecho validado no piloto (§8).

### 3.2 `motor_resultados_detalhes` — fatores de **risco**, chave `(…chave de resultados…, fator)`
Colunas: chave + `ordem` (1 = maior |contribuição|) + `valor`, `unidade`, `contribuicao` (log-odds), `direcao`, `fonte`, `data_referencia`, `data_publicacao` (≤ corte), **`status_juridico`** (nulo, ou o enum acima quando o fator descreve uma supressão) e `texto`. A lista `detalhes` da tela são esses 10 campos, ordenados por `ordem`, validando em [`detalhes.schema.json`](schemas/detalhes.schema.json). Vedações **não** aparecem aqui.

```json
[{"fator": "supressao_vizinhanca", "valor": 12.4, "unidade": "ha", "contribuicao": 1.31,
  "direcao": "aumenta_risco", "fonte": "MapBiomas Desmatamento (sintético)",
  "data_referencia": "2021-12-31", "data_publicacao": "2022-09-27", "status_juridico": null,
  "texto": "Supressão recente na vizinhança do imóvel acima do típico."}]
```
(Exemplo para `data_corte` = 2023-07-31: o último ano de referência já publicado é 2021, pois o de 2022 só sai em set/2023. Valores do stub.)

### 3.3 `motor_resultados_verificacoes` — auditoria da camada determinística, chave `(unidade_id, data_corte, regra, fonte, hash_fonte)`
Cópia das verificações usadas (colunas de [`verificacoes.schema.json`](schemas/verificacoes.schema.json)) + `versao_modelo`, `hash_snapshot`, `calculado_em` (informativos). A tela "Vedação" lê **esta** tabela; a tela "Risco" lê resultados + detalhes. Não misturar.

**Mecânica de bloqueio (por unidade).** Para cada verificação com `efeito = bloqueia`: `detectado` e `sem_autorizacao_identificada` pesam **1**; `autorizado` pesa **0**; `indeterminado` pesa `peso_indeterminado` (padrão **1,0** = limite superior conservador; parâmetro 0–1). `bloqueio_provavel` = máximo dos pesos (0 se a unidade não tem verificação `bloqueia`). `exposicao_bloqueavel = saldo_exposto × bloqueio_provavel`. É aritmética sobre regras, sem estimativa estatística; o significado jurídico (o que bloqueia crédito) vem do pipeline em `efeito` — ⚠️ §9.

## 4. Fórmulas e faixas por nível
- `p ∈ [0,1]`. Stub: logística com ruído determinístico; intercepto calibrado **por `nivel_espacial`** para média de p do nível = taxa-base do nível (p não é calibrado de verdade). O motor real será calibrado em janela separada, em 5 faixas, **por nível**.
- `score = round(1000·(1−p))`. Score alto = risco baixo.
- `faixa` pela razão `p / taxa_base` **do nível da linha**: **A** ≤0,5× · **B** ≤1× · **C** ≤2× · **D** ≤4× · **E** >4× (limites superiores inclusivos). O mesmo p pode dar faixas diferentes em níveis diferentes.
- p **não** usa as verificações (testado): a vedação nunca altera p, score ou faixa.

## 5. `nivel_espacial`
`poligono` = indicadores na gleba/polígono financiado; `imovel_inteiro` = fallback quando o polígono não foi informado. Nos dois, o motor calcula igual, **não reduz p artificialmente** e grava o nível. Em `imovel_inteiro` a semântica muda: p = P(evento em **qualquer parte** do imóvel) e **cresce com a área**; a tela rotula "evento no imóvel" (campo `aviso`). Calibração e métricas do backtest são **por nível**, nunca agregadas entre níveis.

## 6. Contrato de execução
- **Conexão:** `AGRORISK_DB_URL` (URL SQLAlchemy); o motor abre conexão própria, sem Django/ORM, e cria as tabelas de saída se não existirem (índice único da chave). O dev pode criá-las antes via migration mantendo nomes, colunas e chaves.
- **Chamada em Python:** `pontuar(indicadores, unidades, data_corte, *, verificacoes=None, operacoes=None, y_definicao="Y_total", horizonte_meses=12, taxas_base=None, peso_indeterminado=1.0, versoes_dados=None) -> Saida(resultados, detalhes, verificacoes)` (pandas, sem efeitos colaterais). `taxas_base` = `{nivel: taxa}`, padrão do stub se omitido.
- **CLI:** `python -m agrorisk.motor --entrada <dir|db> --saida <dir|db> [--data-corte AAAA-07-31] [--y-definicao Y_total] [--taxas-base poligono=0.02,imovel_inteiro=0.04] [--peso-indeterminado 1.0]`. Sem `verificacoes`, a CLI avisa no stdout que a vedação não foi avaliada.
- **Exceções e códigos de saída:** `ErroEntrada` → 2 (coluna ausente, enum inválido, duplicata, data_corte ≠ 31/jul, `y_definicao`/horizonte não suportado, dado pessoal, nenhum dado no corte) · `ErroConexao` → 3 · `ErroVazamentoTemporal` → 4 (inclui verificação com `data_publicacao > data_corte`) · `ErroModelo` → 5 (o stub não usa) · outras → 1 · sucesso → 0. Em erro de entrada nada é gravado.
- **Transação:** no banco, as **três** tabelas de saída são gravadas numa só transação (resolve a pendência do v0).
- **Idempotência:** upsert pela chave de cada tabela; rodar 2× não duplica; versão nova de modelo gera linhas novas (histórico preservado).
- **`versao_modelo`:** semver + hash do git (`AGRORISK_GIT_HASH` > `direct_url.json` > `git rev-parse` > `desconhecido`). **Determinismo:** semente fixa (20261029).
- **Empacotamento:** inalterado em relação ao v0 (Python ≥ 3.11; núcleo pandas/numpy/pyarrow/sqlalchemy; extras `[modelo]`, `[pipeline]`, `[dev]`; modelos treinados fora do git em `AGRORISK_MODELO_DIR`).

## 7. Trilha de auditoria (primeira classe)
Cada resultado carrega: `versao_modelo` · `data_corte` · `versoes_dados` (por fonte: `data_referencia`, `data_publicacao`, hashes dos snapshots) · `hash_snapshot` (entradas lidas pelo motor) · e, por vedação, `fonte`, `data_publicacao`, `data_corte` e `hash_fonte`. Com isso dá para reproduzir um resultado e mostrar a "evidência pronta" ao auditor. O `hash_snapshot` cobre o **conteúdo lógico** (colunas e linhas ordenadas, tudo como texto); mudar tipos de coluna entre cargas pode alterar o hash.

## 8. Fora do v1 (decidido)
- **Y2/Proagro:** removido. Só a coluna opcional `proagro_acionado` no upload.
- **Y3:** não é saída do motor; é rótulo opcional do piloto (§2.5). Pré-requisitos para modelar: ≥ 300 inadimplências > 90 dias antes do corte, cobertura ≥ 36 meses, operações recusadas com data.
- **`exposicao_esperada`:** só após desfecho validado no piloto; no v1, `exposicao_bloqueavel`.
- **Frente B (fornecedor):** sem código; `tipo_unidade = fornecedor` foi removido.

## 9. Perguntas em aberto (não decididas aqui)
1. **Onde `status_juridico` vive.** O ADR diz "`detalhes` ganha `status_juridico`", mas também que vedação não é feature. O v1 coloca o campo (a) **obrigatório** em `verificacoes` e (b) **nulo por padrão** em `detalhes` (preenchido só se um fator de risco descrever uma supressão). Confirmar com o dev se basta (a) para a tela.
2. **Granularidade da linha de resultado.** O ADR fala em "unidade comercial = operação + CAR" e a modelagem é CAR × t₀. O v1 pontua a **unidade espacial** (CAR/gleba) e agrega as operações vigentes em `saldo_exposto`. Se o produto exigir uma linha por operação, `operacao_id` entra na chave e `p` é repetido; decidir com o dev.
3. **O que bloqueia.** `efeito` (`bloqueia`|`alerta`) é fornecido pelo pipeline porque o texto do MCR 2-9 (UC, embargo estadual) e a Res. CMN 5.268/2025 (adiada pela 5.303/2026) **não foram verificados**. `peso_indeterminado = 1,0` e o "máximo" como agregação são escolhas da sessão, não do ADR; "bloqueio provável" parcial (0 < w < 1) só faz sentido com regra jurídica validada. Precisa do especialista de crédito/regulação.
4. **Cobertura das verificações.** "Unidade sem linha = sem ocorrência" assume que **todas** as regras foram checadas para a unidade. Falta um registro de cobertura por regra (ex.: embargo estadual sem fonte em dado público). Proposta: tabela `regras_avaliadas` por corte, ou campo em `versoes_dados`.
5. **`programa` e `regra`.** Listas abertas (texto) até haver enumeração oficial (Pronaf/Pronamp/…; regras do MCR).
6. **`saldo`.** `valor_rs` é só proxy; saldo real é do painel mensal do piloto (`saldo_rs`). Definir data de referência do saldo (fim de mês anterior ao corte?).
7. **Taxas-base.** O stub usa 0,02 e 0,04 (inventadas). A taxa real vem do Y primário e do recorte após o gate da sessão 07 (178–611 imóveis/ano na vitrine; ver ADR §5), uma por nível.
8. **Hash e tipos.** `hash_snapshot` depende da representação textual dos valores (ver §7). Se o dev precisar de hash estável entre CSV/Parquet/banco, normalizar tipos na ingestão.
9. **Formato de `AGRORISK_MODELO_DIR`** e calibração real continuam a definir quando houver modelo (herdado do v0).
10. **LGPD/sigilo:** parecer jurídico antes de qualquer dado de cliente (§2.6).

## 10. O que NÃO muda de v1 para a versão real (alvo de estabilidade)
Nomes das tabelas de saída e chaves de upsert, fórmulas de `score`/`faixa`/`exposicao_bloqueavel`, os 10 campos de `detalhes`, os campos de `verificacoes`, `AGRORISK_DB_URL`, códigos de saída, a assinatura de `pontuar` e a separação verificação × risco.

## 11. Próximos passos para o dev
Ver a descrição do PR da sessão 06c: migration das 3 tabelas de saída; telas "Vedação" e "Risco" separadas; remover Y2; upload com `nivel_espacial`, `porte_modulos_fiscais`, `programa`, `data_contrato`; responder as perguntas 1, 2, 5 e 6 acima.
