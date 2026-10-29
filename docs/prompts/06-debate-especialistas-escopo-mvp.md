# Sessão 06 — Debate de especialistas e escopo do MVP

> Depende de 01–05 (já mescladas). Roda **em paralelo com a 06b** (contrato do motor + dados sintéticos).
> O fundador acompanha pela sessão: ao fim da síntese, **pare e pergunte** antes de gravar a decisão final.

---

Leia `CLAUDE.md`, `docs/decisoes/0001-*.md`, `docs/produto/` (inclusive `perguntas-dev-v0.md` e, se já estiver lá, a especificação do dev) e **todos** os arquivos de `docs/pesquisa/` (01 a 05). Esta é a **sessão 06**: decisão de escopo. Sem código de análise; consultas pequenas para checar um número são permitidas.

## Contexto novo (desde que este prompt foi escrito)
- Existe um **dev** construindo o produto em Django + PostgreSQL com um desenho centrado em **crédito rural**: operação, gleba, Y1/Y2/Y3 (Y2 = "Proagro acionado"; Y3 = desfecho com dados da cooperativa), faixas A–E e `exposicao_esperada`. As perguntas dele e as respostas provisórias estão em `docs/produto/perguntas-dev-v0.md`.
- As pesquisas trouxeram **achados que contrariam a tese original**:
  - o Proagro é raro em MG (≈95% dos pagamentos no PR/RS) e não há dado público por operação (05);
  - não há desfecho econômico público por imóvel (05);
  - a cooperativa como compradora tem riscos: o Sicredi constrói em casa, o SeloVerde MG é gratuito e o comprador simulado disse "piloto grátis, não compraria hoje" (03);
  - o Y com mais eventos e mais confiável é **supressão de vegetação nativa** (178–611 imóveis/ano com ≥1 ha na vitrine), mas PRODES e MapBiomas divergem (correlação anual −0,37) e o CAR público não tem versões antigas (01);
  - nenhum nicho tem disposição a pagar verificada; o ranking de nichos da 03 não discrimina (03 §5, §9).

## Objetivo
Decidir o **espaço de mercado**, o **Y**, o recorte (vitrine e treino), a unidade, o horizonte, as métricas e o **critério de sucesso** do MVP, pelo critério de maior valor agregado para o comprador **e** de viabilidade estatística. Também responder **de forma definitiva** às perguntas 6–9 do dev.

## Duas frentes a comparar (obrigatório)
- **Frente A — crédito rural reposicionado:** monitoramento e priorização **pós-concessão** da carteira, com eventos que o banco **não é obrigado** a checar (embargos e autos estaduais de MG, outorga/escassez hídrica, UC/APA/carste, supressão na Mata Atlântica), vendido como evidência de gestão de risco (PRSAC/GRSAC). Comprador: **central** de cooperativas (ex.: Sicoob Cecremge/Crediminas), por cima do SeloVerde MG. Desfecho econômico: atraso >90 dias/renegociação (dado do cliente).
- **Frente B — fornecedores de carvão vegetal / siderurgia (hipótese não verificada):** priorizar a auditoria de fornecedores com risco de **supressão de vegetação nativa**. Sete Lagoas concentra 21 das 48 usinas de gusa de MG (03 §7). Aqui o evento ambiental **é** o risco do comprador, sem precisar do elo evento → inadimplência. **Verifique com fontes:** compra de carvão de terceiros, origem nativa × plantada (PEVS/IBGE, IEF, DCF/guias florestais de MG), como as guseiras fazem due diligence hoje, tamanho do mercado.
- Avalie também, brevemente, se hídrico e mineração entram como **indicadores** de A ou B (a 03 e a 05 os rebaixaram como produto isolado).

## Formato: debate estruturado em 3 rodadas
1. **Propostas** (em paralelo): `estatistico-modelagem`, `especialista-credito-regulacao`, `analista-mercado` (este cobre a frente B com pesquisa nova) e `engenheiro-dados-geo` propõem, cada um, até 2 escopos completos (frente, Y, unidade, h, recorte, dados, métrica, cliente, valor), citando `docs/pesquisa/`.
2. **Ataque** (em paralelo): `advogado-do-diabo` e `comprador-cetico`. O comprador cético avalia nas duas personas: gerente de risco de **central de cooperativas** e gerente de **suprimentos/compliance de guseira** em Sete Lagoas.
3. **Síntese** (sessão principal): matriz de decisão com pesos explícitos — valor para o cliente, nº de eventos/poder, dados e licenças, risco de vazamento, diferenciação, esforço até a demo (≤ ~20 h do fundador) e **compatibilidade com o desenho do dev** (o que muda nas tabelas e telas). Mostre a matriz ao fundador e **espere a escolha dele**.

## Decisões a fechar
- Frente principal (A, B ou A+B com o mesmo motor) e roteiro de *customer discovery*: 2–3 alvos por frente e as perguntas-chave.
- Definição operacional do Y (fonte do rótulo PRODES × MapBiomas × Alerta; área mínima; supressão autorizada pelo IEF como exclusão ou variável) e se há Y econômico (Y2/Y3) — nesse caso, qual.
- Unidade (CAR, gleba, fornecedor, operação) e regras de inclusão.
- Datas de corte, horizonte (12/24 meses) e defasagem; **tratamento do CAR sem histórico** (fontes de snapshots antigos ou limitação declarada).
- Recorte de treino (MG inteira?) × vitrine, com o nº esperado de eventos.
- Baselines, métricas e **critério de sucesso numérico** (ex.: lift@10% ≥ 3 com IC 95% > 2 contra a baseline "evento passado").
- Respostas definitivas às perguntas 6–9 de `docs/produto/perguntas-dev-v0.md`, e o que muda no contrato v0 (que a sessão 06b está escrevendo em paralelo).

## Entregáveis
- `docs/decisoes/escopo-mvp.md` (formato ADR de `docs/decisoes/README.md`; status "aceita" só depois da escolha do fundador).
- `docs/pesquisa/06-debate-escopo.md` (propostas, críticas, matriz e pesquisa nova da frente B, com seção **"Oportunidades de inovação para o AgroRisk"**).
- `docs/produto/perguntas-dev-v0.md` atualizado (perguntas 6–9 marcadas como decididas).
- Prompts 07–10 e `CLAUDE.md` (seções 2–3) atualizados conforme o escopo.
- **Não edite** `docs/produto/contrato-motor-v0.md` nem `src/` (pertencem à sessão 06b); registre as mudanças necessárias numa seção "Impacto no contrato do motor" do `escopo-mvp.md`.

Ao terminar: commit, push e PR "Sessão 06 — escopo do MVP".
