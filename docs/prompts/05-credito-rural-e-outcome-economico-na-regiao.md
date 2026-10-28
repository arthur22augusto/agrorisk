# Sessão 05 — Crédito rural e outcome econômico na região

> Pode rodar **em paralelo** com 01, 02, 03 e 04.

---

Leia `CLAUDE.md` e `docs/decisoes/0001-recorte-cliente-e-premissas.md`. Esta é a **sessão 05**: pesquisa regulatória e econômica. Pequenos scripts para consultar a API do BCB (SICOR/Matriz de Dados do Crédito Rural) são permitidos, mas sem commitar dados.

**Objetivo:** entender como o risco socioambiental vira **dinheiro** para o cliente-alvo provisório (cooperativas de crédito e bancos com pequenos/médios produtores em MG) e quais outcomes podem ser medidos com dados públicos.

**Agentes:** `especialista-credito-regulacao` (principal), `comprador-cetico` (valida dor e preço) e `estatistico-modelagem` (como medir a ligação risco → outcome sem cair em correlação espúria).

**Tarefas**
1. Mapa regulatório atual: MCR (impedimentos socioambientais e climáticos, CAR, embargos, UC/TI, Mata Atlântica), PRSAC, bureau verde do BCB, Proagro/Zarc, regras para Pronaf/Pronamp. Indique as vigências.
2. Crédito rural na vitrine: volume, número de contratos, finalidades e linhas por município (SICOR, últimos 5–10 anos); participação de cooperativas; principais instituições.
3. Outcomes mensuráveis com dados públicos: Proagro (sinistros por município), PSR, inadimplência (se houver por região), operações desclassificadas/irregulares (relatórios do BCB), valor da terra (se houver fonte pública). Diga a granularidade de cada um (município × imóvel).
4. Hipóteses de "evento → custo" para o cliente: crédito concedido a imóvel que depois é embargado; garantia (terra) desvalorizada; Proagro negado; dano reputacional/EUDR. Estime ordens de grandeza com fontes.
5. Nicho alternativo: risco hídrico e outorga para irrigantes do cinturão verde, e due diligence de terras na franja urbana — vale como produto? Para quem?

**Entregável:** `docs/pesquisa/05-credito-rural-e-outcome.md`, com tabela "evento → norma → consequência econômica → quem verifica → dado público", panorama do crédito rural na região, avaliação dos nichos e **"Oportunidades de inovação para o AgroRisk"** com fontes.

**Critério de pronto:** pelo menos um outcome econômico observável em dados públicos, com granularidade definida; ou uma conclusão explícita de que o outcome exige dado do cliente (e qual dado pedir em um piloto).

Ao terminar: commit, push e PR "Sessão 05 — crédito rural e outcome".
