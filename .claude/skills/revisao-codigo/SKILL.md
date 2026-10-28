---
name: revisao-codigo
description: "Revisão de código focada em corretude: bugs, edge cases, erros lógicos, problemas de NULL/NA, inconsistências, risco de perda de dados, duplicações perigosas e regressões. Usar quando pedirem review ou revisão de código, verificar corretude antes de commitar, ou depurar comportamento inesperado em SQL, R ou Python analítico."
---

# revisao-codigo

Revisar código existente priorizando corretude. Não refatorar por estética —
simplificação é papel da skill ponytail, não desta.

## O que procurar (em ordem de gravidade)

1. **Perda de dados**: filtros que descartam linhas sem intenção; JOINs que
   multiplicam ou perdem registros; `DROP`/`DELETE`/`TRUNCATE` sem escopo
   claro; sobrescrita de arquivos de output.
2. **NULL/NA**: `= NULL` em SQL (usar `IS NULL`); `na.rm` ausente em R;
   LEFT JOIN criando NULLs/NA que o downstream não espera; `COALESCE`
   ausente onde se assume valor; NaN vs NA em pandas.
3. **Erros lógicos**: condições invertidas, off-by-one, agrupamento com
   coluna errada, granularidade do output diferente da esperada, chaves não
   únicas onde deveriam ser.
4. **Edge cases**: conjunto vazio, divisão por zero, categorias inesperadas,
   datas fora do período, case/acentuação inconsistentes em strings de join.
5. **Regressões**: mudança de nome/tipo de coluna, schema de output, path ou
   nome de arquivo que quebra consumidores downstream.
6. **Duplicação perigosa**: mesma regra de negócio implementada duas vezes,
   divergindo.

## Como revisar

- Ler o diff (ou o arquivo) inteiro antes de opinar.
- Rastrear de onde vêm os dados e para onde vão: o erro raramente está na
  linha onde aparece.
- Em pipelines, verificar row counts e chaves entre etapas (skill
  data-pipeline).
- Em SQL com custo relevante, checar EXPLAIN (skill postgresql).

## Saída

Lista de achados, cada um com `arquivo:linha`, gravidade (alta/média/baixa),
por que está errado e correção mínima sugerida. Sem achados relevantes, dizer
isso em uma linha — não inventar problemas.
