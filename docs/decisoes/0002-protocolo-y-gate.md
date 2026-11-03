# 0002 — Protocolo do Y após o gate (PROPOSTA, não congelada)

- Data: 2026-11-03
- Status: **proposta** — depende de confirmação do fundador; só então congelar (commit/hash) e liberar a sessão 08.
- Base: `docs/pesquisa/07-gate-do-y.md` (resultados e ressalvas).

## Contexto
O gate (escopo-mvp §3) não disparou a regra de parada: 47,7% dos positivos são Y_agro ∧ ≤ 4 MF (IC95% 39,8–55,6) e o histórico explica 46,7% dos elegíveis. Mas a métrica restrita a elegíveis sem histórico fica em 32,2% (IC 24,8–39,8), colada no limiar, a geometria do CAR é a vigente (93% retificados depois de t₀) e o filtro de autorização é inoperante com a cobertura atual do IEF/FEAM.

## Opções
1. **Prosseguir com Y_total como primário** (recomendada), Y_agro e Y_ilegal como derivados reportados.
2. Prosseguir com Y_agro como primário (muda ~13% dos positivos; exige MapBiomas/destino melhor).
3. Reabrir o escopo (nova decisão), tratando "o filtro determinístico basta" como hipótese principal.

## Decisão proposta
Opção 1. Definições herdadas do escopo-mvp: Y_total = supressão PRODES ≥ 1 ha contíguo no polígono do CAR, ciclo ago–jul, h = 12 meses, t₀ = 31/jul; critério primário e baselines inalterados (escopo-mvp §6). Acréscimos por causa do gate: (i) o histórico usado como preditor/baseline termina em y−2 (ou t₀ é deslocado para a publicação do PRODES), por defasagem; (ii) reportar sempre a sensibilidade com `atualizacao ≤ t₀`; (iii) IC de todos os números por bootstrap em blocos de município; (iv) `Y_ilegal` só é reportado onde houver cobertura temporal da autorização.

## Consequências
O retrospectivo segue **exploratório**; o teste limpo é prospectivo (snapshots desde 2026-11-03). Se o fundador preferir a opção 3, a sessão 07 para aqui (painel entregue como infraestrutura, sem modelo).

## Como reverter
Nova decisão que substitua esta.
