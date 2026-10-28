---
name: data-pipeline
description: "Integridade do fluxo de dados entre etapas: inputs, outputs, dependências, joins, cardinalidade, chaves, row counts, duplicações, perdas de registros, NA criado por join, granularidade e reprodutibilidade. Usar ao criar ou alterar etapas de pipeline, quando números não batem entre etapas, ou para avaliar impacto downstream. Trabalha junto com pipeline-graph."
---

# data-pipeline

O pipeline é um DAG: cada etapa consome inputs e produz outputs com contrato
implícito (schema, chave, granularidade, significado). Esta skill verifica a
integridade entre etapas.

## Perguntas de verificação

- Esse JOIN multiplica linhas? (nrow antes/depois; many-to-many)
- A chave deveria ser única no resultado? (`count(key) |> filter(n > 1)`)
- Registros desapareceram? (`anti_join` / `EXCEPT` entre antes e depois)
- O JOIN/merge criou NAs que o downstream não espera?
- A granularidade mudou? (ex.: linha por município → município-ano)
- Esse output é reconstruível? (`intermediate/` deve ser rebuildável rodando
  as etapas anteriores)
- Quem consome esse resultado? (buscar referências; skill pipeline-graph)

## Checks por etapa

1. Row counts: input, output, e diferença explicável em comentário.
2. Chaves: unicidade onde esperada; cobertura (todos os grupos aparecem?).
3. NAs por coluna crítica antes/depois.
4. Valores sentinelas: -999, 0 como NA disfarçado, datas impossíveis.
5. Unidades e tipos: moeda, hectares vs km², integer vs double, encoding de
   acentos.

## Mudanças em uma etapa

Antes: identificar upstream (quem produz o que consumo) e downstream (quem
consome o que produzo) — ver AGENTS.md do projeto. Depois de alterar:
re-verificar downstream quando mudar nome/tipo de coluna, chave,
granularidade, filtro, join ou schema de output.

Antes de corrigir consumidores, decidir o lado que está errado: o upstream
agora produz o comportamento correto, ou a expectativa downstream é que
deveria ser preservada? Não "ajeitar" consumidores automaticamente sem
decidir isso.
