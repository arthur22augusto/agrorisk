# Sessão 04 — Estado da arte acadêmico

> Pode rodar **em paralelo** com 01, 02, 03 e 05.

---

Leia `CLAUDE.md`. Esta é a **sessão 04**: revisão de literatura, sem código.

**Objetivo:** saber o que a ciência já faz para prever supressão de vegetação, fogo, expansão urbana sobre áreas rurais e autuações ambientais, em especial no **Cerrado e na Mata Atlântica**, e que desempenho é realista.

**Agentes:** `pesquisador-academico` em 3 instâncias paralelas — (a) supressão/desmatamento e expansão urbana; (b) fogo; (c) fiscalização/autuação e risco socioambiental × crédito. Depois, `estatistico-modelagem` sintetiza as lições metodológicas.

**Tarefas**
1. Tabela de 20–40 trabalhos relevantes (2015–2026), com os campos do agente.
2. *Benchmarks* de desempenho por tipo de Y e unidade (pixel, grade, imóvel, município), indicando se a validação foi temporal ou espacial.
3. Preditores recorrentes e sua importância (distância a estradas/desmatamento recente, aptidão, preço da terra, tamanho do imóvel, status do CAR, embargo prévio, clima).
4. Lições de método: vazamento, autocorrelação espacial, desbalanceamento, calibração, métricas de ranking; trabalhos que avaliaram **priorização de fiscalização** (ex.: experimentos com alertas, listas prioritárias).
5. Literatura sobre a RMBH/Quadrilátero/carste: conversão urbana, mineração, recarga.
6. Evidências que ligam risco ambiental a outcomes econômicos (crédito, inadimplência, Proagro, valor da terra, Resolução 3.545/2008 e sucessoras).

**Entregável:** `docs/pesquisa/04-estado-da-arte.md`, com referências completas (DOI/link), tabela de benchmarks, "armadilhas a evitar" e **"Oportunidades de inovação para o AgroRisk"** (lacunas acadêmicas que viram diferencial de produto).

**Critério de pronto:** nenhuma referência inventada (cada uma com link verificado); recomendação de 2–3 desenhos de modelo para a sessão 06.

Ao terminar: commit, push e PR "Sessão 04 — estado da arte".
