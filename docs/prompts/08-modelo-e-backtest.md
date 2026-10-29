# Sessão 08 — Modelo e backtest temporal

> Depende de 07 (inclui o gate do Y). Rodar sozinha. Use o modo de planejamento.

---

Leia `CLAUDE.md`, `docs/decisoes/escopo-mvp.md` e `docs/dados/dicionario.md`. Esta é a **sessão 08**.

**Objetivo:** provar (ou refutar) que um ranking de risco antecipa eventos melhor que as baselines, com backtest temporal honesto.

**Agentes:** `estatistico-modelagem` (principal), depois `advogado-do-diabo` (caça a vazamento e resultados bons demais) e a skill `revisao-codigo`.

**Critério de sucesso (decisão 06, pré-registrado — não alterar depois de ver resultados):** primário único = Δrecall@10% ≥ +5 pp contra a **baseline composta** (logística com histórico + vizinhança + município + área nativa), com limite inferior do IC95% > 0 (bootstrap em blocos espaciais), **somente em CARs sem evento prévio**, pooled 2021–2024, no Y primário definido no gate. Todo o resto (lift ≥ 3 com IC inferior > 2, AUC-PR, calibração, por ano/porte/Y/rótulo/`nivel_espacial`) é descritivo. Se não passar: registrar em `docs/decisoes/` que "o filtro determinístico basta" e recomendar o próximo passo.

**Especificação**
- Backtest *rolling origin*: para cada t₀ de teste, treinar só com t₀' tal que t₀' + h ≤ t₀ (o rótulo precisa estar observado no momento do treino).
- Rótulo: PRODES ≥ 1 ha, ciclo ago–jul; **não unir** com MapBiomas (sensibilidade à parte). Testes extras: (a) redundância — só distância a evento + área nativa + município (se o AUC-PR ficar a < ~10% do modelo completo, o modelo é redundante); (b) a regra determinística t+12: que fração dos flags já estava no top 10% em t₀; (c) estabilidade da geometria do CAR; (d) retrospectivo rotulado como exploratório.
- Baselines: (i) evento passado no imóvel; (ii) taxa do município; (iii) proximidade de evento recente; (iv) logística com poucas variáveis.
- Modelos: logística regularizada e *gradient boosting* (LightGBM). Nada além disso antes de superar as baselines.
- Validação adicional por blocos espaciais; Moran's I nos resíduos.
- Métricas por t₀ e agregadas, com IC por *bootstrap* (em blocos): AUC-PR, precision@k, recall@k e lift@k para k ∈ {5%, 10%}, Brier e curva de calibração (calibração em janela separada).
- Explicabilidade: SHAP global e as top-3 razões por imóvel em linguagem simples.
- Análises de robustez: sem variáveis de "evento passado"; só a vitrine × treino ampliado; por tamanho de imóvel.
- *Model card* em `docs/modelo/model-card.md` (dados, período, métricas, limitações, usos não recomendados).

**Entregáveis:** `src/agrorisk/modelo/` (treino, backtest, métricas), `notebooks/08-backtest.ipynb`, `reports/backtest/` (tabelas CSV e figuras leves), model card e um resumo no PR comparando os resultados com o **critério de sucesso** de `escopo-mvp.md` (passou / não passou).

**Critério de pronto:** resultado honesto, mesmo negativo. Se não passar, recomende o próximo passo (mudar Y, recorte ou preditores) em `docs/decisoes/`.

Ao terminar: commit, push e PR "Sessão 08 — modelo e backtest".
