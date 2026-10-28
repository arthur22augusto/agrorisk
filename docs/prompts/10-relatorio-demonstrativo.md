# Sessão 10 — Relatório demonstrativo (Excel + relatório + mapa)

> Depende de 08 (idealmente também de 09). Pode rodar **em paralelo** com 09, usando só as probabilidades.

---

Leia `CLAUDE.md`, `docs/decisoes/escopo-mvp.md`, `docs/modelo/model-card.md` e, se existir, `reports/prescricao/`. Esta é a **sessão 10**.

**Objetivo:** produzir o material que o fundador leva para uma reunião de *customer discovery*: uma **carteira exemplo** da vitrine (ex.: 300–1.000 CARs da RMBH + Colar + Sete Lagoas) analisada de ponta a ponta.

**Agentes:** `comprador-cetico` (revisa o material como cliente), a skill `pptx` + `FN_revisao` (se quiser um deck curto) e `advogado-do-diabo` (afirmações excessivas).

**Entregáveis em `reports/demo-carteira/`**
1. **Excel** (`carteira_exemplo.xlsx`): aba de resumo, ranking (CAR, município, probabilidade, faixa de risco, top-3 razões, ação recomendada), metodologia em linguagem simples, métricas do backtest e fontes/licenças.
2. **Relatório** (`relatorio.html` ou PDF) com 4–6 páginas: problema, como funciona, resultado do backtest ("se você tivesse usado em 2022…"), carteira exemplo, limitações e próximos passos/piloto.
3. **Mapa interativo** (`mapa.html`, folium/kepler) com imóveis coloridos por risco, eventos posteriores e camadas de contexto (UC/APA, mineração, mancha urbana).
4. Script único que regenera tudo: `python -m agrorisk.relatorio --carteira <arquivo>`.

**Regras:** CARs são públicos, mas não exponha nome/CPF de proprietários; use só o código do CAR. Todas as bases citadas com licença e atribuição.

**Critério de pronto:** o material se explica sozinho para um gerente de risco em 5 minutos; o `comprador-cetico` dá veredito "piloto" ou melhor, ou suas objeções ficam listadas.

Ao terminar: commit (sem dados brutos; HTML/XLSX leves podem entrar), push e PR "Sessão 10 — relatório demonstrativo".
