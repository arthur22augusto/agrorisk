# 03 — Concorrência e lacunas de mercado

- Sessão: 03 · Data da pesquisa: 2026-10-28 · Escopo: Brasil, com foco em MG (RMBH + Colar + Sete Lagoas), 2024–2026
- Método: busca web e leitura de páginas públicas por dois agentes `analista-mercado`, mais revisão do `comprador-cetico` e do `advogado-do-diabo` (seção 9).
- Legenda: **[F]** fato lido em fonte · **[I]** inferência nossa · **[NV]** não verificado. Boa parte das fontes é imprensa secundária; antes de uso externo, conferir nos originais.
- Limitação: resumos de páginas vieram de extrator automático; só o GRSAC 2023 do Sicoob foi lido em PDF. Os GRSAC do Sicredi deram 403.

## 1. Resumo executivo

1. **Consulta e monitoramento de conformidade são commodity** (confirma o PDF). Serasa Experian monitora 44 Mha e 69.928 imóveis para a MBRF [F]; Produzindo Certo declara 10 mil fazendas [F]; Agrotools está integrada ao registro de CPR da B3 [F]; o governo oferece o Agro Brasil+Sustentável de graça [F].
2. **Nenhum player publica backtest, AUC, precision@k ou metodologia de predição** (Agro Score, Picsel, Traive, TerraMagna, Sette) [F para Serasa e Picsel; NV para os demais]. É ausência de achado, não prova de ausência.
3. **Quase todos os scores medem inadimplência ou produtividade**, não P(evento socioambiental futuro). Nenhum produto achado faz isso para carteira [NV].
4. **Concorrente público novo em MG: SeloVerde MG** (Seapa/IEF/UFMG), sobre >1 milhão de imóveis do CAR, reconhecido pelo BNB em 05/2025 e premiado pela FAO em 11/2025 [F]. É binário (conformidade), gratuito [I] e tende a virar o padrão de consulta. O **CAR 2.0** (IEF/UFMG) é a triagem estadual.
5. **Gatilho regulatório fraco para o alvo atual:** a verificação PRODES (Res. CMN 5.268/2025, adiada pela 5.303/2026) vale acima de 4 módulos fiscais e foi escalonada até 2028 [F, secundário]. Pequeno produtor é o último a ser obrigado e o evento coberto é desmatamento retrospectivo. Isso reduz urgência de compra no segmento-alvo.
6. **Cooperativas descrevem a checagem de forma genérica** (Sicoob: consulta integrada a Ibama, ICMBio, PRODES, INCRA, SEMAs, sem fornecedor nomeado [F]); **Sicredi constrói em casa** (8 mi de imóveis × 2.000+ áreas protegidas em Teradata [F]). Isso sugere que o cliente "cooperativa" pode ser inalcançável como comprador de score [I].
7. **Dados estaduais de MG (IDE-Sisema, IEF, IGAM, FEAM): nenhum player privado documenta uso** [NV].
8. **Nichos:** nenhum tem tamanho de mercado verificável hoje. Maior suporte de dados aberto: risco hídrico e mineração/barragens. Disposição a pagar: não verificada em nenhum.

## 2. Mapa competitivo (atualização da tabela do PDF)

Camadas: C = consulta, D = diagnóstico, P = predição, Rx = prescrição.

| Player | Camadas | Bases/método declarados | MG / Cerrado–MA | Modelo validado público? | Clientes citados | Preço | Fonte (data) |
|---|---|---|---|---|---|---|---|
| **Serasa Experian Agro** (Farm Check, Agro Score, Smart ESG; sócia da Brain Ag desde 2021) | C, D; Agro Score = score de inadimplência (P financeira) | >170 fontes: SCR, registradoras de CPR, CAR, CCIR, PRODES/DETER, satélite | Nacional; sem detalhe de bases de MG [NV]; safra monitorada não inclui café nem eucalipto | Não: metodologia e validação não publicadas | Nutrien, Cargill, Agrolend, Mosaic, Raízen, Cecafé, MBRF… | Não publicado | [Farm Check](https://www.serasaexperian.com.br/solucoes/farm-check/); [Agro Score](https://www.serasaexperian.com.br/solucoes/agro-score); [MBRF 06/04/2026](https://www.serasaexperian.com.br/sala-de-imprensa/agronegocios/esg-serasa-experian-e-mbrf-monitoram-juntas-44-milhoes-de-hectares-e-garantem-conformidade-ambiental-na-pecuaria-brasileira/) |
| **Agrotools** (Credit, Scorecar, B3, SAP) | C, D, monitoramento | Fundiário, socioambiental, jurídico, climático; Scorecar com Imaflora | Nacional; MG [NV] | Não encontrado | Rabobank, Itaú, ABC (2022); B3 (06/2024); SAP | Sob cotação | [Credit 2022](https://agrotools.com.br/en/blog/content/credit-for-rural-producers/); [B3 21/06/2024](https://economicnewsbrasil.com.br/2024/06/21/financiamento-no-agro-agrotools-e-b3-fecham-parceria/); [Scorecar](https://www.theagribiz.com/agtechs/agrotools-e-imaflora-se-unem-para-trazer-rastreabilidade-de-car) |
| **Terras Crédito Rural** (Terras App Solutions) | C, D (conformidade MCR) | Cruza CAR com "bases oficiais" (não lista) | Diz cobrir todos os estados | Não | Não nomeados no site; convênio de 2016 com um banco (identidade NV) | Não publicado | [terras.agr.br](https://terras.agr.br/); [Câmara 2019](https://www2.camara.leg.br/atividade-legislativa/comissoes/comissoes-permanentes/cindra/arquivos/10-10-2019-3). "CARMap": nada achado [NV] |
| **Demeter** | C, D (conforme o PDF) | — | — | — | — | — | **Sem evidência pública achada em 3+ buscas**; mantido só por constar no PDF. Confirmar qual produto/empresa |
| **Agro Brasil+Sustentável** (MAPA/Serpro/Embrapa) | C, D binário | CAR × embargos, trabalho escravo, UC, TI | Nacional; rastreabilidade ficou de fora | Não | Produtor, voluntário | Gratuito | [AgFeed 12/2024](https://agfeed.com.br/esg/governo-lanca-plataforma-digital-do-agro-sustentavel-com-pendencias-pelo-caminho) |
| **JBS Cowbot / Marfrig / Minerva** | C (sistemas internos de cadeia bovina) | Satélite, CAR; Minerva: Visipec | Cerrado; MG [NV] | Visipec: calibração de conformidade, não predição | Fornecedores de gado | Sem custo ao fornecedor [I] | [HRW 11/2025](https://www.hrw.org/pt/news/2025/11/21/jbs-still-cant-root-out-illegal-ranches-from-its-supply-chain); [Minerva](https://braziljournal.com/brands/como-a-minerva-foods-monitora-seus-fornecedores) |
| **Produzindo Certo** | D com visita (88 itens, score 0–100) | Campo + desmatamento, focos, embargos | 20 estados; MG não citado | Não | ADM, Bunge, Cargill, Nestlé, Rabobank, Sicredi, Itaú | NV; rodada de R$ 20,7 mi (10/2025) | [Forbes 04/2025](https://forbes.com.br/forbesagro/2025/04/uma-guardia-para-10-mil-fazendas-em-busca-de-sustentabilidade/); [Nova Cana 27/10/2025](https://www.novacana.com/noticias/produzindo-certo-capta-r-20-7-milhoes-ampliar-monitoramento-fazendas-271025) |
| **Vega (LYRA)** | D, monitoramento | Satélite, IA | CAR de Goiás; MG [NV] | Não | Bunge; instituições financeiras | NV | [PwC](https://www.pwc.com.br/pt/consultoria/agtech-innovation/agtech-innovation-news/materias/2022/vega-de-compliance-ambiental-planeja-crescimento-acelerado.html) |
| **Satelligence** | D (EUDR, DCF, Scope 3) | Satélite | Brasil não mencionado no site [NV] | NV | Logos: Unilever, Cargill, Bunge, Rabobank | NV | [satelligence.com](https://satelligence.com) |
| **Sette** (fusão A de Agro/Agronow + Bart, 2024) | Capacidade de pagamento, satélite, CPR eletrônica | Satélite, IA | NV | Não | BTG Pactual, Corteva, revendas | NV; série A R$ 28 mi | [TheAgribiz](https://www.theagribiz.com/agtechs/sette-prepara-rodada-de-r-10-milhoes-para-buscar-o-breakeven/) |
| **Bart Digital** (hoje na Sette) | Originação/garantias | — | NV | Não | ~50 clientes em 2022 | NV | [Finsiders 2022](https://finsidersbrasil.com.br/negocios-em-fintechs/agfintech-bart-digital-capta-r-5-milhoes-para-criar-ecossistema-e-lancar-novas-verticais) |
| **Traive** | P/score de crédito com IA, marketplace, FIDC | Modelo proprietário | NV | Sem métricas públicas | Revendas, tradings, cooperativas | NV | [AgFeed](https://agfeed.com.br/agtech/traive-lanca-robo-com-ia-e-oferece-us-120-milhoes-em-credito-em-dolar-para-produtores) |
| **TerraMagna** | Originação + gestão de risco p/ revendas | Satélite, dados alternativos | NV | Sem backtest público | Indústrias, revendas (não o produtor) | NV | [Finsiders](https://finsidersbrasil.com.br/reportagem-exclusiva-fintechs/como-a-terramagna-quer-antecipar-r-500-milhoes-este-ano) |
| **Picsel** | P de risco produtivo (0–1000) | Satélite, clima, solo, 30 safras | **Só soja e milho**; MG/café/eucalipto fora | Não: sem AUC/Gini | Bancos, cooperativas, seguradoras (sem nomes) | NV | [Canal Rural](https://www.canalrural.com.br/agricultura/score-de-risco-produtivo-e-criado-para-aliviar-pressao-sobre-inadimplencia-do-agro/) |
| **SeloVerde MG** (Seapa/IEF/UFMG) | D binário por cadeia | CAR georreferenciado, análise geoespacial com IA | **MG, >1 mi de imóveis**; café, soja, bovinos, cana, eucalipto | Não é preditivo | BNB aceita p/ iniciar crédito (21/05/2025) | NV (provável gratuito) [I] | [Agência Minas 21/05/2025](https://www.agenciaminas.mg.gov.br/noticia/seloverde-mg-torna-se-referencia-para-a-contratacao-do-credito-rural); [FAO 11/2025](https://www.agenciaminas.mg.gov.br/noticia/tecnologia-criada-em-minas-recebe-reconhecimento-internacional-da-fao) |
| **CAR 2.0** (IEF/UFMG) | C, D públicos | CAR, satélite, bases temáticas | MG inteiro; ~37% (387 mil) sem pendências na triagem | Não (determinístico) | Proprietário, órgão ambiental | Gratuito | [Nota técnica](https://car20.meioambiente.mg.gov.br/wp-content/uploads/2024/06/nota_tecnica-car2-0.pdf) (503 na leitura) |
| **MapBiomas** (Alerta/RAD, Monitor do Crédito Rural) | Dado aberto, diagnóstico retrospectivo | Alertas validados, SICOR × CAR | Nacional | Não é modelo | Imprensa, bancos, auditoria | Aberto (licença a verificar) | [RAD2025](https://alerta.mapbiomas.org/wp-content/uploads/sites/17/2026/05/Factsheet-RAD-26052026-1.pdf); [Mundo Coop](https://mundocoop.com.br/?p=229916) |
| **Sicredi / SensorSat (Inplan)** | Monitoramento da operação | Satélite | MG [NV] | Não | Interno | NV | [PwC 2022](https://www.pwc.com.br/pt/consultoria/agtech-innovation/agtech-innovation-news/materias/2022/sicredi-seleciona-startup-para-desenvolver-solucao-de-monitoramento-e-fiscalizacao-do-credito-rural.html) |

**Verificados e descartados como players:** Boa Vista, Quod, SPC (nenhum produto agro achado); Aegro, Cropwise, Solinftec, Agrosmart (gestão de lavoura; Agrosmart só como parceira do E-agro/Bradesco, [Notícias Agrícolas](https://www.noticiasagricolas.com.br/noticia/351205)); **Visão Agro** (sem evidência de existência). Cargill/ADM/Bunge: programas corporativos de cadeia, não produtos de risco vendidos ([Dialogue Earth](https://dialogue.earth/pt-br/florestas/54644tradings-de-soja-falham-em-monitoramento-de-fornecedores-indiretos-no-cerrado-brasileiro/)). Imaflora/Trase: dados de pesquisa, cobertura e licença em MG NV.

Contagem: **16 players/iniciativas verificados com fonte** (critério de pronto ≥10), dos quais 9 privados com produto de risco.

## 3. Como o crédito rural em MG checa o socioambiental hoje

| Instituição | O que se sabe | Fonte |
|---|---|---|
| **Sicoob** | Risco ambiental via "informações de órgãos públicos", autodeclaração e "consultas integradas" (Ibama, ICMBio, MTE, Funai, Iphan, PRODES, INCRA, SEMAs). Não nomeia fornecedor nem modelo preditivo [F]. Plano Safra 26/27: projeção de R$ 20,4 bi de crédito rural em MG (~30% do total) [F, secundário] | [GRSAC 2023](https://www.sicoob.com.br/documents/20128/130978011/GRSAC_2023_SICOOB.pdf) (pp. 12–13); [relatórios](https://www.sicoob.com.br/documents/d/relacaocooperados/relatorio-de-riscos-e-oportunidades-sociais-ambientais-e-climaticas) |
| **Sicredi** | Checagem interna: >8 mi de imóveis × >2.000 áreas protegidas em Teradata (antes >4 h no Databricks) [F]; SensorSat/Inplan escolhida em 2022 [F]. GRSAC 2022–2025 não lidos (403) | [Teradata](https://www.teradata.com/events/possible/sessions/sicredi); [PwC](https://www.pwc.com.br/pt/consultoria/agtech-innovation/agtech-innovation-news/materias/2022/sicredi-seleciona-startup-para-desenvolver-solucao-de-monitoramento-e-fiscalizacao-do-credito-rural.html) |
| **Cresol** | Política de Sustentabilidade pública (11/2024); ferramenta e fornecedor NV | [Política](https://cresol.com.br/wp-content/uploads/2024/11/Politica-de-Sustentabilidade-do-Sistema-Cresol-VF-1.0-PUBLICO-1.pdf) (não aberta) |
| **Banco do Brasil** | "Diagnóstico Geo Socioambiental" desde 2019, 27 bases públicas, bloqueio automático, monitoramento pós-contratação [F] | [Resposta à InfoAmazônia](https://infoamazonia.org/wp-content/uploads/2024/09/Respostas-Banco-do-Brasil-sobre-credito-rural-em-areas-incendiadas-na-Amazonia.pdf) |
| **Banco do Nordeste** | Aceita SeloVerde MG para iniciar crédito: R$ 1,5 bi do FNE, 249 municípios da área mineira da Sudene [F] | [Agência Minas](https://www.agenciaminas.mg.gov.br/noticia/seloverde-mg-torna-se-referencia-para-a-contratacao-do-credito-rural) |
| **BDMG** | Nada encontrado [NV] | — |
| Vagas/editais | Busca rasa: nenhuma vaga ou edital em MG cita Agrotools, Serasa ou Terras [NV] | — |

**Regulação (gatilho):** Res. CMN 5.193/2024 (embargos, CAR válido), 5.268/2025 (PRODES, corte 31/07/2019, >4 módulos) e adiamento/escalonamento pela 5.303/2026: jan/2027 (>15 MF), jul/2027 (4–15 MF), jan/2028 (≤4 MF, conforme Greenpeace, secundário). Resultados de busca divergentes sobre datas; **conferir no normativos.bcb.gov.br** e a ação da CNA no STF. Fontes: [Mattos Filho](https://www.mattosfilho.com.br/unico/alteracao-normas-credito-rural/), [Greenpeace](https://www.greenpeace.org/brasil/imprensa/greenpeace-brasil-ve-retrocesso-em-adiamento-de-regras-ambientais-para-credito-rural/), [CNA](https://cnabrasil.org.br/noticias/cna-vai-ao-supremo-contra-resolucoes-que-tiram-direitos-dos-produtores), [Res. 5.268](https://www.normasbrasil.com.br/norma/resolucao-5268-2025_488247.html).

**Contexto de demanda:** crédito rural −16% no 1º sem/2025 (R$ 83 bi); inadimplência rural ~6,5% em 2025 [F, imprensa] ([Canal Rural](https://www.canalrural.com.br/economia/serasa-concessao-de-credito-rural-cai-16-no-1o-semestre-e-atinge-r-83-bi/)). CAR em MG: >1,1 mi de imóveis, ~28 mil validados com adesão ao PRA (~2%) ([UFMG-CSR/O Tempo](https://csr.ufmg.br/csr/wp-content/uploads/2026/01/otempo_regularizacao-de-propriedades-em-mg.pdf)); validação do CAR é rara no país (~1% em 2024, [AgFeed](https://agfeed.com.br/esg/governo-lanca-plataforma-digital-do-agro-sustentavel-com-pendencias-pelo-caminho)) — viés para qualquer feature baseada em declaração.

## 4. Mapa de lacunas

| # | Lacuna | Evidência | Confiança |
|---|---|---|---|
| L1 | Predição de evento socioambiental com backtest público | Nenhum player publica métricas | Alta (nas fontes lidas) |
| L2 | Uso documentado de bases estaduais de MG por players privados | Nenhuma fonte cita IDE-Sisema/IEF/IGAM/FEAM | Média (NV ≠ ausência) |
| L3 | Eventos além do desmatamento retrospectivo (água, mineração, franja urbana, carste) | Regra CMN cobre só PRODES; scores lidos não citam esses fatores | Média-alta |
| L4 | Culturas/paisagens de MG (café, eucalipto, hortaliças, pecuária) | Picsel só soja/milho; Serasa monitora safra só de 5 culturas | Alta |
| L5 | Pequeno produtor em cooperativa de crédito | Traive/TerraMagna/Sette miram revendas e indústrias; Farm Check sem preço nem caso com cooperativa de MG | Média |
| L6 | Prescrição sob orçamento | Players entregam alertas; Produzindo Certo faz plano por fazenda, sem otimização de carteira | Média |
| L7 | Elo socioambiental → desfecho econômico (inadimplência, perda) | Ninguém prova que risco socioambiental prevê inadimplência | Média; **a ausência pode refletir que o elo é fraco, não oportunidade** (ver seção 9) |

## 5. Nichos alternativos — ranking

Critérios (1 = ruim, 5 = bom; para "concorrência" e "tempo até MVP", 5 = pouca concorrência / MVP rápido). Pontuações são **julgamento nosso [I]**, a validar na sessão 06; pesos iguais.

| Nicho | Dor | Disp. a pagar | Concorrência | Acesso a dados | Tempo MVP | Total | Tamanho estimado |
|---|---|---|---|---|---|---|---|
| **A. Risco hídrico** (irrigantes do cinturão verde, financiadores de pivô, agroindústria) | 3 | 2 (NV) | 4 | 4 (IDE-Sisema, defasagem/licença a checar) | 4 (4–6 m) | **17** | ~5,5 mil outorgas em jan–out/2023 + 9,3 mil usos insignificantes [F]; ≈ R$ 0,7 mi/ano a R$ 100/evento (conta nossa, só fluxo novo) |
| **B. Crédito rural PME em MG (nicho atual)** | 3 | 3 | 2 | 4 | 3 | **15** | R$ 20,4 bi de crédito rural Sicoob-MG projetado (secundário); TAM de software NV |
| **C. Mineração/barragens (entorno e fornecedores)** | 3 | 2 (NV) | 4 | 4 (SIGBM aberto) | 3 (4–8 m) | **16** | 919 barragens no SIGBM nacional [F, via busca]; total MG NV; 21 barragens embargadas em MG no 1º sem/2026 [F, secundário] |
| **D. Eucalipto/carvão (siderurgia)** | 3 | 2 | 3 (MG Florestas, público) | 3 (talhão é privado) | 2 (6–12 m) | **13** | 2,21 Mha de eucalipto em MG; valor florestal ~R$ 8,6 bi (2024) [F]; nº de siderúrgicas NV |
| **E. Leite/laticínios ESG** | 2 | 2 (Lactalis tem >100 técnicos próprios) | 3 | 3 | 4 | **14** | MG ~9,8 bi L (27,4% do Brasil) [F]; ~223 mil produtores (secundário); conta hipotética: R$ 1,1 mi a R$ 13 mi/ano |
| **F. Franja urbana / due diligence de terras** | 3 | NV | 5 (nenhum achado) | 2 (matrículas pagas e fragmentadas) | 1 (9–15 m) | **11** | Nenhum dado quantitativo verificado |

Leitura: os totais diferem pouco e a incerteza das notas é maior que a diferença; **o ranking não discrimina com confiança**. A, C e o nicho atual (B) empatam tecnicamente. Nenhum nicho tem disposição a pagar verificada — este é o dado que a descoberta de clientes precisa produzir. Fontes dos insumos: [Agência Minas/IGAM](https://www.agenciaminas.mg.gov.br/news/pdf/121481.pdf), [FIEMG/IGAM](https://www.fiemg.com.br/wp-content/uploads/2025/09/IE_PORTARIA_IGAM_38-pdf.pdf), [ANM](https://www.gov.br/anm/pt-br/assuntos/barragens/boletim-de-barragens-de-mineracao/boletim-mensal-novembro-2025.pdf/@@download/file), [IEA-SP/IBÁ](https://iea.agricultura.sp.gov.br/ftpiea/AIA/AIA-13-2026.pdf), [Diário do Comércio](https://diariodocomercio.com.br/agronegocio/minas-gerais-mantem-lideranca-valor-producao-florestal/), [Canal Rural](https://www.canalrural.com.br/pecuaria/producao-de-leite-atinge-357-bilhoes-de-litros-nova-regiao-assume-lideranca-nacional/), [EduMiTe/UFMG](https://edumite.igc.ufmg.br/_files/ugd/52be98_1a742c9ccb6041e6b95a74622abebbbb.pdf).

## 6. Oportunidades de inovação para o AgroRisk

| # | Oportunidade | Evidência | Por que os concorrentes não fazem | Esforço |
|---|---|---|---|---|
| 1 | Score preditivo de evento socioambiental com backtest temporal e metodologia aberta, em recorte maior de MG | Agro Score e Picsel sem métricas (L1) | Incentivo comercial é vender o veredito, não expor erro; **também pode não fazer porque o sinal é fraco** | G |
| 2 | Camada de dados estaduais de MG (IDE-Sisema, IEF, IGAM, FEAM) como feature | Nenhum player documenta (L2); licença por camada a verificar | Curadoria local, defasagem de publicação | M |
| 3 | Cobrir ≤4 módulos e eventos além de desmatamento (água, mineração, franja) | Regra CMN só >4 MF e só PRODES (L3, L5) | Fora do foco regulatório atual | M |
| 4 | Posicionar como camada preditiva **sobre** SeloVerde/CAR 2.0, não contra | BNB reconhece o SeloVerde | Estado entrega binário; legitima o CAR como insumo de crédito e pode ser canal | M |
| 5 | Prescrição sob orçamento (onde visitar primeiro) | L6; Sicoob/Sicredi descrevem conformidade, não priorização | Exige modelo + otimização + custo de visita | G |
| 6 | Piloto hídrico (outorga, portarias de escassez, áreas de restrição) | Portarias IGAM 2024/2025 | Dado estadual granular fora dos players nacionais | M |
| 7 | Janela regulatória 2027–2028 para ter validação pronta | Res. 5.303/2026 | — (mas reduz urgência de compra no curto prazo) | P |

## 7. Lista de 30 empresas-alvo em MG para customer discovery

**Status do critério de pronto: 29 organizações com evidência aberta (meta: 30). Não completei a trigésima sem evidência. Dentre as 29, #28 é fraco como alvo e #29 é canal/parceira, não alvo de venda; contam 27 alvos efetivos.** Somente pessoas jurídicas; nenhum decisor nomeado. Páginas de Sicredi, BDMG, FAEMG e Emater bloquearam acesso automatizado (403/503): isso limita a verificação, não indica inexistência. Datas de imprensa de 2018–2022 podem estar defasadas. "Relatório" = política/relatório público (PRSAC/GRSAC para financeiras; sustentabilidade/manejo para as demais). Nenhuma singular mineira tem GRSAC próprio verificado.

### A. Cooperativas de crédito, bancos e fomento

| # | Organização | Região | Por que é alvo | Evidência | Ressalvas |
|---|---|---|---|---|---|
| 1 | Sicoob Central Cecremge | MG; sede histórica em BH | Central de 51 filiadas em 323 municípios: piloto alcança todas | [Cecremge](https://www.sicoob.com.br/web/sicoobcentralcecremge/sicoob-central-cecremge) | Linka relatórios de sustentabilidade; PRSAC não visto na página |
| 2 | Sicoob Central Crediminas | MG | Filiadas em Divinópolis, Sete Lagoas e Bom Despacho | [Singulares](https://www.sicoob.com.br/web/sicoobcentralcrediminas/cooperativas-singulares) | GRSAC/PRSAC não verificados |
| 3 | Sicoob Credisete | Sete Lagoas e região | Nasceu de 25 produtores rurais em 1986; vitrine direta | [Credisete](https://www.sicoob.com.br/web/sicoobcredisete/sicoob-credisete) | Página não detalha crédito rural |
| 4 | Sicoob Centro-Oeste | Itaúna; agências na RMBH | Atua no cinturão da RMBH e atende siderúrgicas | [Sobre](https://www.sicoob.com.br/web/sicoobcentrooeste/sobre) | Página não menciona agro; perfil urbano/industrial é inferência |
| 5 | Sicoob Credpit | Pitangui; área inclui Curvelo e Sete Lagoas | Cobre entorno de Sete Lagoas | [Estatuto 2023](https://www.sicoob.com.br/documents/40480156/54394662/2023-03-16-Sicoob-Credpit-Estatuto-Social.pdf) | Área pode ter mudado |
| 6 | Sicoob Arcomcredi | Arcos | Polo calcário do Centro-Oeste | [Estatuto 2026](https://www.sicoob.com.br/documents/d/sicoobarcomcredi/03-estatuto-social-aprovado-em-19-02-2026-age-2026-assinado-1) | Ligação com carste é inferência |
| 7 | Sicoob Credibom | Bom Despacho, Nova Serrana, BH | Eixo Centro-Oeste e BH | [Crediminas](https://www.sicoob.com.br/web/sicoobcentralcrediminas/cooperativas-singulares) | Só listagem de agências |
| 8 | Sicoob Crediverde | Divinópolis e região | Cobre Divinópolis (usina da SDS) | idem | Só listagem de agências |
| 9 | Sicoob Credipatos | Patos de Minas | Polo de leite; segunda região de validação | idem | Só listagem de agências |
| 10 | Sistema Sicredi em MG | MG: 241 agências, ~400 mil associados (dez/2024) | Expansão em MG, perfil agro | [Coop. de Crédito 2025](https://cooperativismodecredito.coop.br/2025/03/sicredi-planeja-inaugurar-50-agencias-em-minas-gerais-neste-ano/) | GRSAC 2022–2025 existem, PDF deu 403; nenhuma singular verificada |
| 11 | BDMG | BH | R$ 3 bi anunciados para safra 2026/27; agricultura familiar via cooperativas | [Itatiaia](https://www.itatiaia.com.br/agro/bdmg-anuncia-r-3-bilhoes-para-a-safra-2026-2027-e-apoia-agricultura-familiar/) | Site oficial 403; GRSAC/PRSAC não localizados |
| 12 | Banco do Nordeste (MG) | Norte de MG, Jequitinhonha, Mucuri | R$ 503,5 mi em crédito rural jan–ago/2025; aceita SeloVerde | [Diário do Comércio](https://diariodocomercio.com.br/financas/contratacoes-bnb-minas-gerais-superam-r-3-bilhoes/) | Fora da vitrine; GRSAC não verificado |
| 13 | Invest Minas | BH | Estudo de Fiagro estadual de R$ 150 mi para pequenos produtores | [AgFeed 28/05/2025](https://agfeed.com.br/economia/exclusivo-governo-de-minas-gerais-planeja-lancar-fiagro-de-r-150-milhoes) | Projeto embrionário; status atual não confirmado |

### B. Cooperativas agropecuárias, laticínios e hortifrúti

| # | Organização | Região | Por que é alvo | Evidência | Ressalvas |
|---|---|---|---|---|---|
| 14 | Itambé | BH; fábricas em Pará de Minas, Sete Lagoas, Guanhães, Uberlândia | Base de produtores de leite que tomam crédito rural | [Itambé](https://www.itambe.com.br) | **Titularidade conflitante** (site diz cooperativa; notícia de 2019 fala em compra pela Lactalis) — confirmar antes de abordar |
| 15 | CCPR | MG e GO | 30 cooperativas, 25 mil cooperados, 23 lojas agro | [CCPR](https://www.ccpr.coop.br) | Sede não informada |
| 16 | Coopatos | Patos de Minas (inferência) | Leite, lojas agro, nutrição animal | [Coopatos](https://www.coopatos.com.br) | Cidade não confirmada na página |
| 17 | CeasaMinas | Contagem (BR-040) | Escoa o cinturão verde da RMBH | [CeasaMinas](https://www.ceasaminas.com.br) | Menu "Produtor Rural" sem conteúdo lido |

### C. Florestal, siderurgia e carvão

| # | Organização | Região | Por que é alvo | Evidência | Ressalvas |
|---|---|---|---|---|---|
| 18 | Vallourec Florestal | Curvelo; 19 fazendas, ~165 mil ha | Carvão para alto-forno; exposição a desmatamento e terceiros (inferência) | [Plano de Manejo jul/2026](https://www.vallourec.com/app/uploads/sites/5/2026/07/Resumo-Publico-do-Plano-de-Manejo-2026-1.pdf) | Relatório público aberto |
| 19 | SDS Siderúrgica (S&D) | Sete Lagoas, Divinópolis | >50 mil ha de eucalipto próprio; gusa de baixo carbono | [Diário do Comércio 03/07/2025](https://diariodocomercio.com.br/economia/sds-siderurgica-expansao-minas-gerais/) | Relatório não verificado |
| 20 | Aperam BioEnergia | Jequitinhonha | 126 mil ha; carvão renovável | [Diário do Comércio 2022](https://diariodocomercio.com.br/economia/producao-de-carvao-vegetal-da-aperam-e-modernizada/) | Dados de 2022; fora da RMBH |
| 21 | Gerdau (MG) | Ouro Branco, Divinópolis, Sete Lagoas etc. | 220 mil ha de eucalipto, 90 mil ha de mata nativa | [Diário do Comércio 2022](https://diariodocomercio.com.br/economia/gerdau-investe-r-2-bi-em-minas-gerais-neste-ano/) | Dados de 2022 |
| 22 | Amif | BH | Reúne florestais; porta de entrada | [Diário do Comércio 2022](https://diariodocomercio.com.br/agronegocio/amif-empossa-nova-gestao-do-conselho-deliberativo/) | Associação (canal) |
| 23 | Sindifer-MG | MG; Sete Lagoas tem 21 das 48 usinas | Canal para guseiras | [Jornal de Brasília 25/06/2026](https://jornaldebrasilia.com.br/noticias/economia/mais-de-50-de-usinas-de-ferro-gusa-podem-parar-se-novo-tarifaco-entrar-em-vigor-diz-sindifer/) | Sindicato (canal) |

### D. Mineração, imobiliário, seguro e entidades

| # | Organização | Região | Por que é alvo | Evidência | Ressalvas |
|---|---|---|---|---|---|
| 24 | Vale | Quadrilátero Ferrífero | Meta de 500 mil ha recuperados/protegidos até 2030 | [Vale](https://vale.com/pt/sustainability) | Relatório de sustentabilidade aberto |
| 25 | MRV | sede não confirmada | Urbanismo/loteamentos (franja) | [MRV](https://www.mrv.com.br) | Sede em BH é suposição |
| 26 | Direcional Engenharia | 8 estados + DF; Contagem | Presença na RMBH | [Direcional](https://www.direcional.com.br) | Sede não confirmada |
| 27 | Grupo Cottage | Pedro Leopoldo | Loteamento na franja do carste | [Diário do Comércio 2020](https://diariodocomercio.com.br/negocios/valorizacao-do-vetor-norte-impulsiona-loteamentos-na-regiao/) | Matéria de 6 anos |
| 28 | Rota Seguros | BH + interior | Distribuição regional de seguros | [Apólice 2022](https://revistaapolice.com.br/2022/06/rota-seguros-completa-21-anos-e-comemora-expansao/) | **Fraco:** sem menção a seguro rural; é corretora |
| 29 | Sistema Ocemg | BH | Diretório do cooperativismo mineiro | [Ocemg](https://sistemaocemg.coop.br/) | **Canal/parceira, não alvo de venda** |

**Não entraram (evidência insuficiente):** Cresol em MG (página aberta cita 20 estados sem MG), Sicoob Metropolitano, Sicoob Credifor, CSN Mineração, Mineração Usiminas, Coopersete (Sete Lagoas; 2012–13, pode não existir mais), FAEMG, Emater-MG (parceiros), Ibram, "Barbosa" (laticínio, sem entidade confirmável).
**Lacunas:** nenhuma cooperativa de hortifrúti do cinturão verde, FIDC/Fiagro agro com gestora em BH ou seguradora rural sediada em MG achadas.
**Ordem sugerida de entrevistas:** (1) Sicoob Credisete, Credpit, Centro-Oeste e Cecremge; (2) Sicredi e BDMG; (3) Vallourec Florestal, SDS e Sindifer.

## 8. Riscos e contra-evidências

- **Serasa/Agrotools** têm distribuição em bancos e cooperativas e podem lançar camada preditiva quando o mercado pedir [I].
- **Sicredi e BB** constroem internamente; **Sicoob** descreve governança central — a decisão de compra pode estar na central/confederação, não na singular [I].
- **Estado de MG** (SeloVerde, CAR 2.0) pode ampliar o escopo e tornar a camada de consulta e triagem gratuita.
- **Produzindo Certo** capitalizada (10/2025), negocia validação do laudo no Plano Safra [F, secundário]; pode ir a MG com visita de campo.
- **Vega** atua em CAR estadual (Goiás) e pode replicar em MG [I].
- **Eventos raros em MG:** desmatamento em larga escala é raro na vitrine (CLAUDE.md); a coluna do Diário do Comércio sugere alta em MG (~40 mil ha) mas é opinião, [NV] ([coluna](https://diariodocomercio.com.br/opiniao/coluna/projeto-preserva/minas-contramao-desmatamento-avanca/)).
- **Falta de elo econômico:** nenhuma fonte mostra que risco socioambiental prevê perda de crédito (L7).

## 9. Revisões críticas

Opiniões das personas, sem pesquisa web adicional; os fatos vêm deste documento.

### 9.1 Comprador cético (gerente de risco de cooperativa/banco em MG)

- **Veredito: piloto grátis; não compraria hoje.** Falta evidência de que o score prevê perda de crédito e de que dá ação melhor que o que já tem.
- **Não compra consulta de CAR** (já tem Serasa/Agrotools ou equivalente; SeloVerde MG e Agro Brasil+Sustentável são gratuitos).
- **Compraria** uma camada de priorização sobre a própria carteira: ranking com backtest (top 10% concentra eventos futuros), explicação por fator e lista de visitas dentro do orçamento. Modelo de cobrança preferido: piloto de 6 meses numa carteira fechada, depois assinatura anual por carteira, não por consulta. Faixa de preço: **chute da persona, sem fonte** (dezenas de milhares de R$/ano para cooperativa média); não usar como premissa.
- **Quem decide:** ele recomenda; aprova o comitê de crédito/risco, com TI (integração, LGPD) e jurídico (responsabilidade por erro). Na filiada, a compra pode estar na central/confederação.
- **Não respondido pela proposta:** elo com perda econômica (L7); Y indefinido (desmatamento é raro na RMBH e retrospectivo); gatilho regulatório fraco para ≤4 MF; disposição a pagar; custo de falso positivo e explicação ao produtor; licença e defasagem dos dados; fornecedor pequeno (LGPD, SLA, API, responsabilidade); viés do CAR declaratório.
- **Nichos:** pagaria (com condição) crédito PME em MG, risco hídrico e mineração/barragens (disposição a pagar NV); **não pagaria** franja urbana (dados pagos, MVP longo), leite (Lactalis tem técnicos próprios; dor é da indústria), eucalipto/carvão (talhão privado; comprador é a siderurgia) nem consulta pura.
- **O que levaria ao "sim":** backtest em carteira real com lift/recall no top 5–10% ligado a perdas; metodologia explicável ao produtor; piloto sem custo com contrato de dados/LGPD/limite de responsabilidade; integração simples (arquivo/API) sem trocar fornecedor; custo de análise menor em horas de analista.
- **Métricas para o comitê:** eventos antecipados no top-k vs. regra atual; falsos positivos entre bons produtores; horas de analista; operações bloqueadas a tempo; perda evitada em R$.

### 9.2 Advogado do diabo

- **Objeção central:** o documento deriva "oportunidade" de "não achei". L1, L2, L3, L5 e L6 repousam em [NV] ou busca rasa; "ninguém faz" não separa "ninguém pediu" de "não funciona".
- **Por lacuna:** L1 é lacuna de marketing, não de produto (comprador raramente exige AUC); L2 é ausência de achado (quem usa IDE-Sisema internamente não divulga) e dado estadual aberto já é commodity (SeloVerde, CAR 2.0); L3 pode ser ausência de demanda (sem gatilho CMN, ninguém paga); L4 é a mais sólida, mas é lacuna de produtividade, não de risco socioambiental; L5 aponta ausência de demanda (cooperativa pode ser inalcançável; último segmento obrigado); L6 depende de custo de visita e efeito causal, ambos não medidos; **L7 é a hipótese mais ameaçadora**, não uma lacuna.
- **Viés de busca:** fontes são imprensa e sites comerciais, o que favorece quem faz marketing e esconde sistemas internos; GRSAC Sicredi com 403, Cresol/BDMG não lidos, editais/vagas rasos; preços NV; extrator automático resumiu as páginas.
- **Ranking de nichos (seção 5):** notas são julgamento com pesos iguais e diferença menor que a incerteza; "pouca concorrência = nota alta" premia nicho sem mercado (F); disposição a pagar NV entra na soma (falsa precisão); o nicho A (≈ R$ 0,7 mi/ano) é pequeno demais para uma empresa e mesmo assim lidera; falta peso para tamanho endereçável.
- **Cenário de fracasso mais provável:** eventos raros em MG, poucos positivos e IC largos; lift trivial sobre "quem já teve evento"; autuação mede onde o Estado fiscaliza, não o comportamento; cooperativa usa SeloVerde/CAR 2.0 gratuitos e não vê urgência até 2027–2028; sem elo com inadimplência, "boa técnica, ninguém paga"; Serasa/Agrotools podem adicionar camada preditiva; fundador com ~5 h/semana.
- **Três evidências que mudariam a opinião:** (1) cooperativa/banco de MG declara em entrevista ou carta de intenção que pagaria por priorização de carteira, dizendo valor e quem decide; (2) taxa de eventos suficiente para backtest (ex.: ≥200 positivos em recorte maior; o número é ordem de grandeza da persona, não regra) e modelo que bata baseline de histórico/vizinhança com validação em blocos espaciais; (3) associação entre evento socioambiental e inadimplência/perda em carteira piloto.

### 9.3 Decisões incorporadas neste documento

- "Ausência de concorrente" **não** é argumento de tese; lacunas L1–L3, L5, L6 ficam como hipóteses a testar.
- L7 (elo evento → perda econômica) passa a ser a **primeira hipótese a testar** (sessão 05 e entrevistas).
- O ranking da seção 5 **não deve ser usado para decidir nicho**; refazer com tamanho de mercado e disposição a pagar medidos.
- Prioridade antes de construir: customer discovery com a lista da seção 7 e medição da taxa de eventos em MG (sessões 01/06).

## 10. Perguntas em aberto

1. Quem decide a compra: cooperativa singular, central ou confederação? Há contrato com Agrotools, Serasa ou Terras?
2. O que a cooperativa faz com um alerta hoje (bloqueia, visita, reprecifica) e quanto custa uma visita?
3. Há cadastro interno de ocorrências (embargo, autuação, supressão) para treinar/validar? Qual a taxa por 1.000 imóveis em MG?
4. Que evidência (precision@k, lift, calibração) mudaria a decisão de compra? Aceitam score sem validação oficial?
5. SeloVerde MG: conhecido, usado, complementar ou concorrente?
6. Orçamento por CAR ou por carteira; modelo de cobrança dos incumbentes (preço público: NV).
7. Água, mineração, franja e carste geram perda real em crédito na RMBH? Caso concreto?
8. Plano para a verificação PRODES 2027/2028 e decisão do STF.
9. Quais camadas do IDE-Sisema, SIGBM, MapBiomas Alerta e PRODES/DETER permitem uso comercial, com que defasagem? (registrar em `licencas.md`; sessão 02)
10. O que são "Demeter" e "Visão Agro" (sem evidência pública)? Terras/"CARMap"?
11. Lacunas de leitura: GRSAC Sicredi 2022–2025 e Sicoob 2025; Cresol e BDMG; editais/Gupy; PEVS carvão MG nativo×plantado; estabelecimentos com leite/irrigação (Censo 2017); texto consolidado da Res. 5.303.

**Sugestões para a sessão 06:** (i) tratar "disposição a pagar" como hipótese principal a testar, não o ranking acima; (ii) incluir hídrico e mineração como Y candidatos de segunda frente; (iii) testar com o cliente se o Y de maior valor é desmatamento (regulatório, mas retrospectivo e raro em MG) ou evento ligado a perda de crédito.
