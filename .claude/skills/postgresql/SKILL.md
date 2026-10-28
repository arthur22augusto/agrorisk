---
name: postgresql
description: "Escrever, modificar, depurar, revisar e otimizar PostgreSQL para análise de dados, priorizando consultas eficientes e operações seguras em tabelas grandes: SELECT, JOIN, CTE, CASE, COALESCE, arrays, window functions, UPDATE, CREATE TABLE, índices, constraints, EXPLAIN, risco de locks e operações destrutivas."
---

# postgresql

Preferir processamento nativo no banco a exportar dados e processar fora
quando o banco resolve. Sempre pensar em custo em tabelas grandes.

## Consultas

- Filtrar cedo: `WHERE` antes de joins/agregações quando possível.
- Explicitar tipo de JOIN; LEFT JOIN cria NULLs no lado direito — tratar com
  `COALESCE` quando o downstream não espera NULL.
- NULL: `= NULL` nunca funciona; usar `IS NULL`, `IS NOT DISTINCT FROM`,
  `COALESCE`, `NULLIF`.
- CTEs para legibilidade; window functions em vez de self-join:
  `ROW_NUMBER`, `LAG/LEAD`, `SUM() OVER (PARTITION BY ...)`, `DISTINCT ON`.
- `CASE` para reclassificação; arrays (`unnest`, `= ANY`, `@>`) quando
  agregam valores por linha.
- `EXISTS` em vez de `COUNT(*) > 0` para checagem de existência.

## Performance

- Antes de otimizar, medir: `EXPLAIN (ANALYZE, BUFFERS)`.
  - Seq Scan em tabela grande → índice ausente ou não usado pelo planner.
  - estimativa muito diferente do real → `ANALYZE <tabela>`.
- Índices nas colunas de filtro e join; `CREATE INDEX CONCURRENTLY` onde
  escrita concorrente importa (evita lock de escrita).
- Evitar `SELECT *` em tabelas largas; selecionar só colunas usadas.
- `UPDATE`/`DELETE` grandes: em lotes (CTE com chave + `LIMIT`) para não
  segurar lock longo; ou `CREATE TABLE AS` + rename quando a tabela pode ser
  reconstruída.
- Antes de alterar, contar: `SELECT COUNT(*)` com o mesmo `WHERE` do
  `UPDATE`/`DELETE`.

## Operações destrutivas (DROP, TRUNCATE, DELETE, UPDATE em massa)

1. Verificar escopo: rodar o `WHERE` como SELECT primeiro; conferir row count.
2. Preferir transação: `BEGIN` ... conferir ... `COMMIT`/`ROLLBACK`.
3. Tabela crítica: snapshot antes (`CREATE TABLE backup_x AS SELECT ...`).
4. Nunca rodar `DROP`/`TRUNCATE` sem confirmação explícita do usuário.
5. Alertar risco de lock: DDL e UPDATE em massa bloqueiam leitores/escritores.

## Saída

Apresentar o SQL final pronto para rodar. Quando a operação for grande ou
destrutiva, incluir o row count esperado e o risco em uma linha antes do
comando.
