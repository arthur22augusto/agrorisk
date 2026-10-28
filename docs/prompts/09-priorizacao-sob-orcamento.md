# Sessão 09 — Priorização sob orçamento (prescrição)

> Depende de 08. Pode rodar **em paralelo** com 10.

---

Leia `CLAUDE.md`, `docs/decisoes/escopo-mvp.md` e `docs/modelo/model-card.md`. Esta é a **sessão 09**.

**Objetivo:** transformar probabilidades em decisão — "com orçamento para auditar B imóveis (ou R$ X), quais auditar primeiro?" — e mostrar o ganho em relação às regras atuais do cliente.

**Agentes:** `estatistico-modelagem` (formulação e otimização), `comprador-cetico` (a função de custo faz sentido para uma cooperativa?) e `advogado-do-diabo`.

**Especificação**
- Valor esperado por imóvel: `p_i × severidade_i × efetividade_ação − custo_auditoria_i`. Defina a severidade com proxies (área em risco, valor do crédito, se houver, e penalidade regulatória) e documente as premissas.
- Otimização: knapsack/ILP (PuLP ou OR-Tools) com restrições (orçamento, capacidade por região/analista, cobertura mínima por município).
- Comparar no backtest: top-k por probabilidade × top-k por valor esperado × regra simples (ex.: "auditar quem tem embargo") × aleatório. Curva "eventos capturados × orçamento" e "valor capturado × orçamento".
- Sensibilidade às premissas de custo e severidade.

**Entregáveis:** `src/agrorisk/prescricao/`, `notebooks/09-prescricao.ipynb`, `reports/prescricao/` (figuras e tabela) e `docs/decisoes/NNNN-funcao-de-valor.md`, com as premissas.

**Critério de pronto:** curva de ganho com IC e uma frase de valor para o cliente ("com 10% do orçamento, captura X% dos eventos, contra Y% da regra atual").

Ao terminar: commit, push e PR "Sessão 09 — priorização sob orçamento".
