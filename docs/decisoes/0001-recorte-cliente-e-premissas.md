# 0001 — Recorte, cliente-alvo e premissas iniciais

- Data: 2026-10-28
- Status: aceita
- Decisores: fundador (perfil quantitativo), com apoio do Claude Code

## Contexto
Início do projeto. A proposta (`docs/AgroRisk_proposta_v2.pdf`) aponta como *wedge* a
priorização de carteira validada historicamente. Optou-se por começar pequeno, numa região
diferente da Amazônia (onde se concentra a maior parte das soluções do mercado).

## Decisão
1. **Fonte de verdade:** `docs/AgroRisk_proposta_v2.pdf` (antigo `AgroRisk_Proposta_para_Reuniao_v2_com_Concorrentes.pdf`).
   O `AgroRisk2.pdf` é uma versão diferente e anterior, mantida em `docs/historico/`.
2. **Recorte vitrine:** RMBH (34 municípios) + Colar Metropolitano + Sete Lagoas.
3. **Recorte de treino:** aceita-se desde já ampliar para outras regiões de MG se o número de eventos
   for insuficiente. A vitrine pode mudar se as reuniões com clientes indicarem região de maior retorno.
4. **Cliente-alvo provisório:** crédito rural para pequenos e médios produtores (cooperativas de crédito/bancos).
   Reavaliar após as sessões 03 e 05.
5. **Evento Y:** decidido na sessão 06, com o critério de *maior valor agregado* para o comprador.
6. **Dados privados:** nenhum disponível agora. O fundador pode buscar parceiros depois de ter um
   setup inicial para mostrar (o relatório demonstrativo da sessão 10 serve para isso).
7. **Equipe e ritmo:** um fundador ativo agora (Python/QGIS nível 3–4, ~5 h/semana); outros fundadores
   podem entrar depois — por isso, a documentação deve ser autoexplicativa.
8. **Orçamento de nuvem:** crédito de sessões vence em 2026-11-04. Priorizar as sessões de
   pesquisa paralelas (01–05) e a decisão de escopo (06) antes dessa data.

## Consequências
- Prompts 07–10 ficam condicionados a `docs/decisoes/escopo-mvp.md`.
- Toda pesquisa deve avaliar explicitamente o poder estatístico (nº de eventos) no recorte vitrine
  e propor o recorte de treino.
