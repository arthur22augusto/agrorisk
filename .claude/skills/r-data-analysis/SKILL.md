---
name: r-data-analysis
description: "Análise de dados e estatística em R: dplyr/tidyr por padrão, data.table quando houver benefício concreto, modelagem estatística, tratamento explícito de NA, validação de dados, reprodutibilidade e gráficos. Usar ao escrever, revisar ou depurar scripts R analíticos. Não transforma script analítico em arquitetura de software."
---

# r-data-analysis

Pensar como estatístico usando R: código analítico legível, pipeline linear
(import → clean → analyze → export). Sem classes, factories ou abstração
prematura em script analítico.

## Manipulação

- dplyr/tidyr por padrão (`mutate`, `filter`, `group_by`/`summarise`,
  `pivot_*`).
- data.table apenas com benefício concreto (dados grandes, muitos grupos);
  não misturar estilos no mesmo script sem motivo.
- Sempre checar chaves e row counts: `nrow()` antes/depois de joins e
  filtros; `anti_join()` para achar registros perdidos;
  `count(key)` para duplicatas.

## NA é decisão, não acidente

- `left_join` introduz NAs — decidir: `replace_na`, filtrar ou manter.
- `mean()`, `sum()`, `median()` sem `na.rm` retornam NA — explicitar sempre.
- Distinguir NA (ausente) de 0 e de NaN quando o significado importar.
- Registrar em comentário POR QUE linhas com NA foram removidas (decisão
  metodológica).

## Modelagem e reprodutibilidade

- `set.seed()` antes de qualquer estocasticidade.
- Especificação do modelo em comentário: estimando, unidade de análise,
  período, tratamento/controle.
- Erros padrão apropriados à dependência dos dados (clustered/robust quando
  relevante).
- Reportar magnitude e significância prática junto de p-valores.

## Saídas (projetos com estrutura padrão input/model/output)

- Ler de `input/` e `intermediate/`; gravar intermediários em
  `intermediate/`, resultados em `output/`, figuras em `output/figures/`
  (`ggsave()` com nome descritivo), tabelas em `output/tables/`.
- Paths relativos à raiz do projeto (here::here ou equivalente), nunca
  absolutos.
