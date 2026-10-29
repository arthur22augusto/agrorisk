# Sessão 06b — Contrato do motor v0 + stub + dados sintéticos

> Roda **em paralelo com a 06**. Objetivo: destravar o dev já; os números se ajustam depois da 06.
> Sessão de código pequena. Python ≥3.11.

---

Leia `CLAUDE.md` e `docs/produto/` (em especial `perguntas-dev-v0.md` e, se existir, a especificação do dev). Esta é a **sessão 06b** do AgroRisk.

**Contexto:** um dev está construindo o produto em Django + PostgreSQL e precisa de um contrato estável com o "motor" estatístico e de um *stub* (motor de mentira com o mesmo formato) até a "semana 3". O escopo final (Y, unidade) está sendo decidido em paralelo na sessão 06: escreva o contrato **genérico o bastante** para valer tanto para operação de crédito (frente A) quanto para fornecedor (frente B). Use `unidade_id` + `tipo_unidade` em vez de nomes presos a crédito, e o Y identificado por `evento` + `horizonte_meses`.

**Agentes:** `estatistico-modelagem` (revisa definições e o gerador sintético), skill `revisao-codigo` no fim.

## Entregáveis
1. **`docs/produto/contrato-motor-v0.md`** — status "provisório", com:
   - tabelas e colunas que o motor **lê** (indicadores por unidade × data de corte; unidades/glebas; operações quando houver) e **grava** (resultado + detalhes por fator), com tipo, unidade, nulos permitidos e exemplo;
   - fórmulas: `p` (float [0,1]), `score` = `round(1000·(1−p))`, faixas A–E por múltiplo da taxa-base (A ≤0,5×; B ≤1×; C ≤2×; D ≤4×; E >4×), `exposicao_esperada` = `p × valor_exposto` (R$; não é perda);
   - JSON Schema de `detalhes` (`fator, valor, unidade, contribuicao, direcao, fonte, data_referencia, data_publicacao, texto`) em `docs/produto/schemas/detalhes.schema.json`;
   - contrato de execução: conexão própria por variável de ambiente (`AGRORISK_DB_URL`), exceções tipadas, códigos de saída, idempotência (upsert por `unidade_id, data_corte, evento, versao_modelo`), `versao_modelo` (semver + hash do git), `versoes_dados` (JSON), `nivel_espacial` (`gleba` | `imovel_inteiro`) com aviso;
   - empacotamento e instalação: `uv add git+https://github.com/arthur22augusto/agrorisk`; núcleo leve (pandas, numpy) e extras `[modelo]` (lightgbm) e `[pipeline]` (geopandas, duckdb, rasterio); onde ficam os modelos treinados (`AGRORISK_MODELO_DIR`);
   - lista do que **depende da sessão 06** (marcar com ⚠️).
2. **`pyproject.toml`** (src layout, `agrorisk`, extras acima, versões mínimas) e `README` atualizado com "como instalar o motor".
3. **Stub** em `src/agrorisk/motor/`: `pontuar(indicadores: DataFrame, unidades: DataFrame, data_corte) -> (resultados, detalhes)` determinístico (semente fixa), respeitando o contrato, mais uma CLI `python -m agrorisk.motor --entrada <dir|db> --saida <dir|db>` que lê/grava Parquet/CSV **ou** banco via SQLAlchemy (sem depender do Django).
4. **Gerador de dados sintéticos** em `src/agrorisk/sinteticos.py` e uma amostra pequena (<1 MB) em `tests/fixtures/sinteticos/`:
   - ~300 imóveis com **código de CAR fictício no formato real** (`MG-<IBGE7>-<32 hex>`, marcado como fictício) em municípios da vitrine (lista em `docs/pesquisa/01-diagnostico-territorial.md`, Tabela 1), com geometrias simples dentro dos limites municipais (aproximar por caixas/pontos se não houver limite local; não baixar bases grandes);
   - glebas (parte com `nivel_espacial = imovel_inteiro`), operações de crédito plausíveis (cultura, safra, valor, datas) e também "fornecedores" para a frente B;
   - indicadores simulados (vegetação nativa, supressão na vizinhança, distância a área urbana/mineração, sobreposição com UC/APA, chuva) e **eventos gerados por um modelo logístico conhecido** (coeficientes documentados), com taxa-base ≈2%, para testar se o pipeline/backtest recupera o modelo;
   - nenhum dado real de pessoa; nenhum CPF/nome.
5. **Testes** (`tests/`, pytest): o stub respeita o schema (JSON Schema de `detalhes`, faixas coerentes com p, score em [0,1000]), a idempotência (rodar 2× não duplica) e o gerador é reprodutível com semente.

## Regras
- Nada em `data/` vai para o git; a amostra sintética fica em `tests/fixtures/`.
- Não edite `docs/decisoes/escopo-mvp.md` nem `docs/pesquisa/` (pertencem à sessão 06).
- Rode `pytest` e mostre o resultado no PR.

Ao terminar: commit, push e PR "Sessão 06b — contrato do motor v0, stub e dados sintéticos", com um resumo para o dev: "como instalar, como chamar, o que ainda pode mudar".
