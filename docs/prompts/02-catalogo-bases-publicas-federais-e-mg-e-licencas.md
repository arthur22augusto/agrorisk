# Sessão 02 — Catálogo de bases públicas (federais e de MG) e licenças

> Pode rodar **em paralelo** com 01, 03, 04 e 05.

---

Leia `CLAUDE.md`. Esta é a **sessão 02** do AgroRisk: catálogo de dados. Scripts de **teste de acesso** podem ser escritos (em `src/agrorisk/fontes/`), mas sem baixar bases inteiras nem commitar dados.

**Objetivo:** saber exatamente quais dados existem, como acessar, com que defasagem e se o uso comercial é permitido.

**Agentes:** `engenheiro-dados-geo` (principal; divida em 2 instâncias paralelas: *federais* e *MG estaduais*) e `especialista-credito-regulacao` (SICOR/Proagro/PSR e termos de uso).

**Bases mínimas**
- Federais: SICAR/CAR (incluindo snapshots históricos e status), PRODES Cerrado e Mata Atlântica, DETER Cerrado, MapBiomas (cobertura, transições, Alerta, Fogo, Água), Atlas da Mata Atlântica (SOS MA/INPE), embargos IBAMA e ICMBio, autos de infração IBAMA, CNUC/UCs, SIGEF/SNCI (INCRA), focos de queimada (INPE), INMET e CHIRPS, relevo (Copernicus DEM/SRTM, TOPODATA), hidrografia (ANA — BHO), IBGE (malhas, Censo Agro 2017, PAM/PPM/PEVS), SICOR/Matriz de Dados do Crédito Rural (BCB), Proagro, PSR (MAPA), CECAV/CANIE (cavidades), ANM/SIGMINE (processos minerários), SNISB (barragens), Base dos Dados (espelhos).
- Minas Gerais: IDE-Sisema (camadas SEMAD/FEAM/IEF/IGAM), autos de infração e embargos estaduais, DAIA/autorizações de supressão (IEF), outorgas e áreas de conflito (IGAM), ZEE-MG, Inventário Florestal de MG, áreas prioritárias para conservação, cadastro de barragens da FEAM, CAR estadual (se houver diferença em relação ao SICAR).

**Para cada base:** campos do agente `engenheiro-dados-geo`, com destaque para **defasagem de publicação**, **histórico (dá para reconstruir o estado em t₀?)**, **chave de ligação ao CAR** e **licença literal**. Teste de acesso a partir deste ambiente: se houver 403/bloqueio (já observamos 403 em `servicos.ibama.gov.br` e `www.ibge.gov.br`), registre e proponha alternativa.

**Entregáveis**
- `docs/pesquisa/02-catalogo-bases.md` — catálogo, mapa "base → candidato a Y / preditor / outcome", conjunto mínimo viável para o MVP e seção **"Oportunidades de inovação para o AgroRisk"**.
- `docs/pesquisa/licencas.md` — uma linha por base (substitua a linha de exemplo).
- (Opcional) `src/agrorisk/fontes/teste_acesso.py`, que testa endpoints e grava status em Markdown.

**Critério de pronto:** nenhuma base sem licença classificada (sim / não / incerto + link); defasagem estimada para todas as candidatas a Y.

Ao terminar: commit, push e PR "Sessão 02 — catálogo de bases e licenças".
