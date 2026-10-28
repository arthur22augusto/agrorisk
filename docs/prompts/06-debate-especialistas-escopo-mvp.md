# Sessão 06 — Debate de especialistas e escopo do MVP

> **Depende de 01–05** estarem mescladas na `main`. Rodar sozinha. Use o modo de planejamento.

---

Leia `CLAUDE.md`, `docs/decisoes/0001-*.md` e **todos** os arquivos em `docs/pesquisa/`. Esta é a **sessão 06**: decisão de escopo. Sem código.

**Objetivo:** decidir o Y, o recorte final (vitrine e treino), a unidade e o horizonte, as métricas e o critério de sucesso do MVP, com o critério de **maior valor agregado para o comprador** e viabilidade estatística.

**Formato: debate estruturado em 3 rodadas.**
1. **Propostas** (em paralelo): `estatistico-modelagem`, `especialista-credito-regulacao`, `analista-mercado` e `engenheiro-dados-geo` propõem, cada um, até 2 escopos completos (Y, unidade, h, recorte, dados, métrica, cliente, valor). Cada um deve citar as evidências de `docs/pesquisa/`.
2. **Ataque** (em paralelo): `advogado-do-diabo` e `comprador-cetico` criticam todas as propostas.
3. **Síntese** (sessão principal): matriz de decisão com pesos explícitos — valor para o cliente, nº de eventos/poder, disponibilidade e licença dos dados, risco de vazamento, diferenciação frente à concorrência, esforço até a demo (≤ ~20 h de trabalho do fundador). Mostre a matriz ao fundador e **espere a escolha dele** antes de gravar.

**Decisões a fechar**
- Definição operacional do Y (fonte, regra, área mínima, como tratar eventos autorizados — ex.: supressão com DAIA), ou Y composto com pesos.
- Unidade (CAR) e regras de inclusão (status do CAR, tamanho, data de inscrição anterior a t₀).
- Datas de corte t₀ (série), horizonte h (12 ou 24 meses) e janela de defasagem.
- Recorte de treino × vitrine e o número esperado de eventos em cada um.
- Baselines, métricas primárias e secundárias e **critério de sucesso numérico** (ex.: lift@10% ≥ 3 com IC 95% acima de 2, superando a baseline "evento passado").
- Formato da prescrição (orçamento de auditorias, função de custo).
- O que o relatório demonstrativo mostra para o cliente.

**Entregáveis**
- `docs/decisoes/escopo-mvp.md` (formato ADR de `docs/decisoes/README.md`).
- `docs/pesquisa/06-debate-escopo.md` (propostas, críticas e matriz).
- Atualize os prompts 07–10 em `docs/prompts/` se o escopo exigir, e o `CLAUDE.md` (seção 2–3).

Ao terminar: commit, push e PR "Sessão 06 — escopo do MVP".
