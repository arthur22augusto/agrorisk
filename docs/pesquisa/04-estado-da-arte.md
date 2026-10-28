# 04 — Estado da arte acadêmico

Sessão 04 · data: 2026-10-28 · revisão de literatura, sem código.
Produzido por três frentes de pesquisa (desmatamento/urbano, fogo, fiscalização/crédito/método) e
sintetizado na sessão principal.

**Convenção de verificação.** *Aberto* = a página/registro foi aberta e o dado lido. *Link não
verificado* = só snippet de busca, paywall (403) ou PDF ilegível. Número sem fonte lida aparece como
"não verificado". **Preprints** estão sinalizados. Vários periódicos (Springer, Wiley, MDPI, SciELO)
bloquearam a abertura; antes de citar qualquer número externamente, leia o PDF.

## 1. Resumo executivo

- **Não encontramos nenhum trabalho publicado que prediga supressão, fogo ou autuação por *imóvel*
  (CAR) no Cerrado ou na Mata Atlântica de MG com backtest temporal, validação espacial em blocos e
  métricas de ranking** (precision@k, lift). Isso é busca de ausência, não prova de inexistência.
- Predição com validação temporal explícita existe sobretudo na Amazônia/Peru (Rosa 2013: AUC 0,92→0,86
  em 8 anos; Ball 2022). O único produto operacional por CAR é o PrevisIA (Imazon, Pará), cuja
  "acurácia de 70–75% a 4 km" é dado não publicado e não é métrica de ranking.
- Cerrado: literatura de cenários em grade de 1 km (Colman 2024; Stan 2015 para MG), avaliada por
  AUC/acurácia em janela, não por ranking. Mata Atlântica/MG: estudos explicativos (RF, GWR).
- Fogo: predominam modelos **retrospectivos** de foco ativo em unidade de conservação/pixel
  (AUC-ROC 0,75–0,80 em CV temporal; AUC-PR 0,23–0,30 com pseudoausências). Ignição prospectiva a 5 km:
  AUC-ROC ≈ 0,89, mas F1 = 0,0073.
- Fiscalização: há boa evidência **causal** (Amazônia) de que monitoramento + sanção reduzem
  desmatamento e de que a Res. CMN 3.545/2008 reduziu desmatamento; **nenhum** estudo verificado liga
  conformidade ambiental a inadimplência/Proagro. Esta é a lacuna mais valiosa e depende de dados privados.
- Métodos: CV aleatória infla o desempenho (Ploton 2020: R² 0,53 → 0,14 com CV espacial). Eventos raros
  exigem AUC-PR/precision@k/lift, não AUC-ROC.
- **Não há benchmark publicado para o desenho do AgroRisk**; o benchmark terá de ser construído contra
  baselines ingênuos (histórico do imóvel, distância a desmatamento recente, tamanho).

## 2. Trabalhos revisados

Total: 49 entradas (19 desmatamento/urbano/RMBH, 12 fogo, 18 fiscalização/crédito/método). Colunas: "Ver." = A (aberto)
ou NV (link não verificado / só snippet).

### 2.1 Supressão/desmatamento, expansão urbana, RMBH/carste

| # | Referência | Região / unidade | Y e horizonte | Validação | Métrica lida | Ver. |
|---|---|---|---|---|---|---|
| D1 | Colman et al. 2024, *Sci Rep* 14:4559, [doi:10.1038/s41598-024-55207-1](https://pmc.ncbi.nlm.nih.gov/articles/PMC10894285/) | Cerrado; célula 1 km agregada por tamanho de imóvel (252.007 CARs) | Conversão de vegetação nativa, passos de 2 anos; projeção 2050/2070 | Calibração 2008–2016; teste por verossimilhança; sem CV espacial | AUC só no suplemento (não verificado); projeção −26,5 Mha (±11,8) até 2050 | A |
| D2 | Rosa et al. 2013, *PLoS ONE* 8:e77231, [PMC3799618](https://pmc.ncbi.nlm.nih.gov/articles/PMC3799618/) | Amazônia; pixel 5 km | P(desmatamento) anual, projeção 2050 | **Temporal** (calibra 2001–02, testa 2002–2010) | AUC 0,92 → 0,86 em 8 anos; acerto exato de pixel ≈ 2%/ano | A |
| D3 | Stan et al. 2015, *PLoS ONE* 10:e0137911, [PMC4570775](https://pmc.ncbi.nlm.nih.gov/articles/PMC4570775) | **MG inteira**; 1 km | Conversão de cobertura, anual até 2023 | Simulação do ano 2000 vs. mapa JRC | Acurácia > 85% (janela 1,5 px), > 90% (3,5 px) | A |
| D4 | Zanella et al. 2017, *Environ Ecol Stat* 24:529, [eprint](https://eprints.lancs.ac.uk/id/eprint/88586) | Mata Atlântica de MG | Taxa de desmatamento/fragmentação (explicativo) | Não descrita | Localização e topografia dominam a importância; acessibilidade/instituições pouco | A |
| D5 | Davis et al. 2019, *Geografias* 15(2), [UFMG](https://periodicos.ufmg.br/index.php/geografias/article/view/19890) | Mata Atlântica; provável município (inferido) | Desmatamento/regeneração (explicativo) | Nenhuma | — | A |
| D6 | Sampaio 2014, diss. UFMG, [repositório](https://repositorio.ufmg.br/handle/1843/IGCM-9QBMA8) | Vetor Norte da RMBH | Mudança de cobertura urbana, cenário 2031 | Cenário 2011 vs. imagem 2011 | Acurácia 82,61%; concordância 92,60%; Cramér's V: mudança 2001–06 (0,37), distância a centros (0,35) | A |
| D7 | de Souza & De Marco 2018, *Ecol Modell* 387:1, [resumo](https://econpapers.repec.org/RePEc:eee:ecomod:v:387:y:2018:i:c:p:1-9) | Amazônia; município | Novo desmatamento 2009–11, treino até 2008 | **Temporal** | Sem números no resumo; sensibilidade/VPP variam com atividade local | A (resumo) |
| D8 | Ball et al. 2022, *Methods Ecol Evol*, doi:10.1111/2041-210X.13953; [preprint bioRxiv](https://doi.org/10.1101/2021.12.14.472442) (**preprint**); [código/dados Dryad](https://datadryad.org/dataset/doi:10.5061/dryad.hdr7sqvjz) | Amazônia peruana; pixel 30 m | Perda no ano seguinte | **Temporal** (treino 2014–19, teste 2020) | F1 ≈ 0,71 (lido só em registro de busca) | NV (paper) / A (Dryad) |
| D9 | La Rosa et al. 2024, *ISPRS Ann* X-3:193, [link](https://isprs-annals.copernicus.org/articles/X-3-2024/193/2024/) | Amazônia; grade 25 km | Risco semanal (2–4 sem.) a partir de DETER | Contra alertas 2020–23; split não descrito | RMSE 0,29 (preliminar) | A |
| D10 | Imazon, PrevisIA, [página](https://imazon.org.br/artigos/deforestation-control-at-rural-properties-in-para-a-strategy-using-the-previsi-risk-model) (**não revisado por pares**); base: Ribeiro Sales et al. 2017, *Spatial Statistics* 21:304, doi:10.1016/j.spasta.2017.06.003 (NV) | Pará; por CAR, produto em grade | Desmatamento em até 1 ano | Comparação com PRODES 2021–23 | "70–75% a 4 km" (dado não publicado) | A (página) |
| D11 | Leal et al. 2020, *Floresta e Ambiente* 27(2) | São Félix do Xingu; imóvel | Taxa de desmatamento por imóvel | Divisão **aleatória** | RMSE 12,9%, r = 0,91 (só snippet) | NV |
| D12 | Espindola et al. 2021, *Environ Dev Sustain* 23:17146, [IDEAS](https://ideas.repec.org/a/spr/endesu/v23y2021i11d10.1007_s10668-021-01387-z.html) | SW Piauí (MATOPIBA) | Transições de uso (explicativo) | Nenhuma | Áreas protegidas −0,22 (coef.); distância a estradas −0,03 (n.s.) | A |
| D13 | Stefanes et al. 2018, *Land Use Policy* 75:43, [JCU](https://researchonline.jcu.edu.au/58730/) | MS (Cerrado); imóvel/CAR | Conformidade com Reserva Legal (descritivo) | — | 51% (> 1.000 ha) vs. 33% (menores); ≈ 2 Mha de desmatamento legal | A |
| D14 | Azevedo et al. 2017, *PNAS* 114:7653, doi:10.1073/pnas.1604768114 ([Europe PMC](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:10.1073/pnas.1604768114&resultType=core&format=json)) | PA e MT; CAR | Desmatamento ilegal, cadastrados vs. não | Análise geoespacial | Diferença entre grupos diminuiu e variou com o tamanho | A |
| D15 | Sonter et al. 2014, *Conserv Biol* 28:1068, doi:10.1111/cobi.12260 ([Europe PMC](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=TITLE:%22Offsetting%20the%20impacts%20of%20mining%20to%20achieve%20no%20net%20loss%20of%20native%20vegetation%22&resultType=core&format=json)) | **Quadrilátero Ferrífero**; cenários | Desmatamento por mineração até 2020 | Simulação | 3.570 ha; compensação atual evitaria 3% | A |
| D16 | Rosa MR et al. 2021, *Sci Adv* 7:eabc4547, [PMC7817092](https://pmc.ncbi.nlm.nih.gov/articles/PMC7817092) | Mata Atlântica; hexágonos 250 km² | Dinâmica floresta madura/jovem 1990–2017 | Checagem de 350 pontos | 83% da perda e 73% do ganho corretos; mudanças < ~1 ha excluídas | A |
| D17 | Esteves et al. 2024, *ISPRS Arch* XLVIII-3:155, [link](https://isprs-archives.copernicus.org/articles/XLVIII-3-2024/155/2024/) | Centros urbanos BR (BH não citada) | Mudança de classe urbana (AC + RNA) | Não descrita | Precisão ≥ 0,74; recall ≥ 0,86 | A |
| D18 | Magnabosco et al. 2020, *Hydrol Sci J*, [UFMG](https://repositorio.ufmg.br/items/bf73cb50-365e-497b-a4a3-560a67ca3971) | **Sete Lagoas**; aquífero cárstico | Potencial hídrico (não é Y de supressão) | — | Liga crescimento urbano a poços improdutivos/sobre-exploração | A |
| D19 | Rajão et al. 2020, *Science* 369:246; Rodrigues et al. 2022, *Glob Change Biol* 28(22) | Amazônia+Cerrado | Desmatamento potencialmente ilegal / legal remanescente | — | ~2% dos imóveis ≈ 62% do desmatamento potencialmente ilegal; ≥ 28,4 Mha legais no Cerrado (snippets) | NV |

### 2.2 Fogo

| # | Referência | Região / unidade | Y e horizonte | Validação | Métrica lida | Ver. |
|---|---|---|---|---|---|---|
| F1 | Pádua et al. 2026, arXiv:2606.04170, [abs](https://arxiv.org/abs/2606.04170) (**preprint**) | Cerrado de MG; unidade de conservação-dia | Foco ativo (pseudoausências); retrospectivo | CV temporal 5 folds + holdout espacial de 2 UCs | CV: AUC-PR RF 0,235→0,300; AUC-ROC 0,756–0,792. Holdout Serra do Cabral (262 positivos): AUC-PR 0,262, AUC-ROC 0,955. Pau Furado: só 6 positivos | A |
| F2 | Vieira et al. 2026, *REIC* 24:1, doi:10.5753/reic.2026.7053, [PDF](https://journals-sol.sbc.org.br/index.php/reic/article/download/7053/3832/37216) | Cerrado; pixel 5 km/dia | 1ª detecção de ignição no dia seguinte | Treino 2014, teste 2017; sem validação espacial | AUC-ROC ≈ 0,89; prevalência ≈ 0,03%; F1 0,0073; top-1% das células capta ~12% das ignições, top-5% ~45% | A |
| F3 | Faria et al. 2026, *Forests* 17(5):526, doi:10.3390/f17050526 | PN Gandarela (MG) e RVS Campos de Palmas (PR) | Índices de risco a partir de focos | Split não verificado | R² 0,53–0,68 (abstract) | A (abstract) |
| F4 | Singh & Huang 2022, *Sustainability* 14(2):992, [RePEc](https://ideas.repec.org/a/gam/jsusta/v14y2022i2p992-d726247.html) | Mata Atlântica | Ocorrência de fogo (RF) | Não verificado | Sem números; NDVI, temperatura, radiação | A (abstract) |
| F5 | Lacerda et al. 2022, *Ciência Florestal* 32(1), doi:10.5902/1980509864171, [link](https://periodicos.ufsm.br/cienciaflorestal/article/view/64171) | PN Gandarela (Quadrilátero) | Suscetibilidade (AHP vs. histórico de focos; **sem ML**) | Kappa contra focos | Kappa 0,61 (histórico) vs. 0,54 (AHP) | A (abstract) |
| F6 | Brito 2023, diss. UnB, [PDF](https://repositorio.unb.br/bitstream/10482/48283/1/WilkisonQueirozDeBrito_DISSERT.pdf) | Amazônia Legal (fora do bioma-alvo) | Focos vs. ausência | Não verificado | AUC RF 0,88; MLP/XGB 0,84 | A (abstract) |
| F7 | Yamamoto 2025, TCC UFSCar, [repositório](https://repositorio.ufscar.br/items/0961d00e-e46f-48d4-a097-86f70875422f) | Cerrado; diário | Replica índice de risco do INPE (não prevê fogo) | Não verificado | R² 0,8166 (RF) | A (abstract) |
| F8 | Arruda et al. 2024, *Fire Ecology*, doi:10.1186/s42408-024-00298-4 | Cerrado; descritivo (MapBiomas Fogo) | Regime de fogo 1985–2022 | n/a | Números só de snippet | NV |
| F9 | Segura-Garcia et al. 2025, *Phil Trans R Soc B* 380, doi:10.1098/rstb.2023.0460, [eprint](https://ueaeprints.uea.ac.uk/id/eprint/103325/) | Cerrado; grade 30 km | Regiões de regime de fogo (clustering) | n/a | Descritivo; dados/código em Zenodo doi:10.5281/zenodo.14025420 (não aberto) | A |
| F10 | Prapas et al. 2021, arXiv:2111.02736, [abs](https://arxiv.org/abs/2111.02736) (**preprint**, workshop) | País não identificado | Perigo de fogo a 1 dia | Não descrita | AUROC 0,926 (ConvLSTM) | A |
| F11 | Prapas et al. 2022, arXiv:2211.00534, [abs](https://arxiv.org/abs/2211.00534) (**preprint**) | Global (SeasFire) | Área queimada 8–64 dias | Não verificado | Não verificado | A |
| F12 | Michail et al. 2025, arXiv:2502.01550, [abs](https://arxiv.org/abs/2502.01550) (**preprint**) | Global | Área queimada até 6 meses | Não verificado | Não verificado | A |

Produto **MapBiomas Fogo** (Y candidato de área queimada): Landsat 30 m, mensal/anual desde 1985; ATBDs
consultados: [C1](https://mapbiomas-br-site.s3.amazonaws.com/ATBD_MapBiomas_Fogo_Coleção_1.pdf),
[C4](https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2025/06/ATBD-MapBiomas-Fogo-Colecao-4.pdf).
Acurácia por bioma, defasagem de publicação e licença: **não verificados** (pendência para a sessão 02).

### 2.3 Fiscalização, crédito e método

| # | Referência | Região / unidade / Y | Método | Resultado lido | Ver. |
|---|---|---|---|---|---|
| C1 | Assunção, Gandour, Rocha 2023, *AEJ: Applied* 15(2):125, [AEA](https://www.aeaweb.org/doi/10.1257/app.20200196) | Amazônia; desmatamento | IV (nuvens limitam o DETER) | Fiscalização guiada por monitoramento reduz desmatamento; sem número no resumo | A |
| C2 | Assunção et al. 2023, *Rev Econ Stud* 90(4):1608, doi:10.1093/restud/rdac064; [NBER WP 25636](https://www.nber.org/papers/w25636) | Municípios da Amazônia; lista prioritária ótima | Changes-in-changes + otimização | (NBER) Lista de 2008: ≈ −40% de desmatamento; lista ótima ≥ 7,4% menos emissões e > 25% menos que aleatória. Versão publicada pode diferir | A (NBER) |
| C3 | Assunção et al. 2020, *Econ J* 130(626):290, doi:10.1093/ej/uez060, [IDEAS](https://ideas.repec.org/a/oup/econjl/v130y2020i626p290-330..html) | Amazônia; Res. 3.545/2008 | DiD | Reduziu desmatamento, sobretudo na pecuária; sem números lidos | A |
| C4 | Cisneros, Zhou, Börner 2015, *PLoS ONE* 10:e0136402, [link](https://journals.plos.org/plosone/doi?id=10.1371/journal.pone.0136402) | 492 municípios (lista suja) | Pareamento + DiD | ≈ −25%; pareamento reduz o efeito > 70% vs. não pareado | A |
| C5 | Börner et al. 2015, *PLoS ONE* 10:e0121544, [link](https://journals.plos.org/plosone/doi?id=10.1371/journal.pone.0121544) | 15.432 fiscalizações IBAMA; grade 10 km | Pareamento Mahalanobis | ≈ −6,5 ha/célula (~14%); só clareiras > 20 ha; ~USD 3.500/inspeção | A |
| C6 | Hargrave & Kis-Katos 2013, *Env Resour Econ* 54:471, doi:10.1007/s10640-012-9610-2, [link](https://econpapers.repec.org/RePEc:kap:enreec:v:54:y:2013:i:4:p:471-494) | 663 municípios | Painel EF | Fiscalização reduz; preços agrícolas aumentam desmatamento | A |
| C7 | Duflo et al. 2018, *Econometrica* 86:2123, [NBER WP 20590](https://www.nber.org/papers/w20590) | Gujarat (Índia); indústrias | RCT de inspeções | Inspeção aleatória custa ~metade da discricionária; pouca melhora de conformidade | A |
| C8 | Greenstone et al., teste de campo EPA, [página do autor](https://michaelgreenstone.com/?p=1828) | EUA; resíduos perigosos | ML vs. escolha da EPA | Hit rate +46% (histórico, ~2% dos sítios) e +79% (campo). Coautores/ano **não verificados** | A (página) |
| C9 | Nunes et al. 2024, *Sci Rep* 14:1828, [link](https://link.springer.com/10.1038/s41598-024-52180-7) | Amazônia 2004–18 | Descritivo | 43,6 mil embargos, 84,3 mil multas (snippet) | NV |
| C10 | Kuschnig et al. 2023, *ERL* 18:074039, [IIASA](https://pure.iiasa.ac.at/19467) | Brasil; multas | Econométrico | Eficácia caiu nos últimos anos (snippet) | NV |
| C11 | Sousa 2016, *Forests* 7:66, [link](https://www.mdpi.com/1999-4907/7/3/66) | Mato Grosso | Correlacional | Multas/embargos negativamente correlacionados com desmatamento; baixa arrecadação (snippet) | NV |
| C12 | Souza et al., CPI/PUC-Rio, dez/2024, "Credit Where It's Due" ([relatório](https://www.climatepolicyinitiative.org/publication/credit-where-its-due-financial-institutions-and-credit-for-deforested-properties/); **não revisado por pares**) | Brasil; SICOR×SICAR×PRODES×MapBiomas Alert | Cruzamento por CAR | 36% do crédito rural subsidiado (R$ 205,6 bi de R$ 567,7 bi, 2020–24) a imóveis com desmatamento desde 2009; **não mede inadimplência** | A |
| C13 | Melo & Resende Filho 2017, *Rev Bras Econ*, doi:10.5935/0034-7140.20170004 | Inadimplência macro no SNCR (ARDL) | — | Sem variável ambiental; identificação do artigo não confirmada | NV |
| C14 | Ploton et al. 2020, *Nat Commun* 11:4540, [PMC7486894](https://pmc.ncbi.nlm.nih.gov/articles/PMC7486894/) | Biomassa, África central | CV aleatória vs. espacial | R² 0,53 → 0,14; RMSPE 77,5 vs. 82 do modelo nulo; sem poder preditivo além de ~100 km | A |
| C15 | Kapoor & Narayanan 2022, arXiv:2207.07048, [abs](https://arxiv.org/abs/2207.07048) (**preprint**; publicado em *Patterns* 2023) | 17 áreas | Revisão de vazamento | 329 artigos afetados, 8 tipos de vazamento; vazamento explicou ganho de modelos complexos sobre regressão logística | A |
| C16 | Saito & Rehmsmeier 2015, *PLoS ONE* 10:e0118432, [link](https://journals.plos.org/plosone/doi?id=10.1371/journal.pone.0118432) | Método | ROC vs. PR | PR é mais informativo com classes desbalanceadas | A |
| C17 | Roberts et al. 2017, *Ecography* 40:913, doi:10.1111/ecog.02881 | Método | CV em blocos | Blocos geralmente mais adequados sob dependência (snippet) | NV |
| C18 | Meyer et al. 2018, *Environ Model Softw* 101:1, doi:10.1016/j.envsoft.2017.12.001 | Método | Forward feature selection + CV orientada ao alvo | R² 0,9 (aleatória) vs. 0,24 (leave-location-out) (snippet) | NV |

Pistas **não lidas** (verificar antes de citar): Arruda et al. (RBGDR 2025; DiD de Callaway-Sant'Anna sobre CAR e
desmatamento no Centro-Oeste); Blundell, Gowrisankaran & Langer (*AER* 2020; fiscalização dinâmica).

## 3. Benchmarks por tipo de Y e unidade

Somente valores lidos nas fontes. **Nenhum é comparável ao desenho do AgroRisk.**

| Y / unidade | Resultado | Validação | Fonte |
|---|---|---|---|
| Desmatamento, pixel 5 km (Amazônia) | AUC 0,92 → 0,86 em 8 anos; acerto exato de pixel ≈ 2%/ano | Temporal | D2 |
| Desmatamento, pixel 30 m (Peru) | F1 ≈ 0,71 | Temporal (1 ano) | D8 (snippet) |
| Desmatamento, grade 25 km, semanal | RMSE 0,29 (preliminar) | Split não descrito | D9 |
| Desmatamento, imóvel (Pará, PrevisIA) | "70–75% a 4 km" (não publicado, não é ranking) | Compar. com PRODES | D10 |
| Desmatamento, Cerrado, 1 km | AUC apenas no suplemento (não verificado) | Temporal por verossimilhança | D1 |
| Mudança urbana, Vetor Norte (RMBH) | Acurácia 82,61%; concordância 92,60% | Cenário vs. imagem | D6 |
| Foco ativo, UC-dia (Cerrado MG), pseudoausência | AUC-ROC 0,76–0,79; AUC-PR 0,24–0,30 (CV); holdout espacial AUC-ROC 0,955 com 262 positivos | Temporal + espacial | F1 |
| Ignição a 5 km/dia (Cerrado) | AUC-ROC ≈ 0,89; top-5% capta ~45% das ignições; F1 0,0073 | Temporal (1 ano) | F2 |
| Suscetibilidade em UC de MG | Kappa 0,54–0,61 | vs. focos | F5 |
| Autuação/embargo como Y | **Nenhum benchmark preditivo encontrado** | — | — |
| Inadimplência/Proagro × risco ambiental | **Nenhum estudo encontrado** | — | — |
| Priorização de inspeção (EUA) | Hit rate +79% em teste de campo | Campo | C8 |

**Leitura para o MVP (inferência, não resultado de fonte):** em imóvel/ano na RMBH, onde supressão em larga
escala é rara, espere AUC-PR baixa em termos absolutos. Reporte sempre relativo à prevalência: lift,
recall nos top 5–10% e precision@k, com IC por *bootstrap* em blocos. O poder estatístico depende da taxa
de evento por imóvel/ano, hoje desconhecida (sessões 01 e 06).

## 4. Preditores recorrentes

Importância relativa em MG é **desconhecida**; abaixo, o que a literatura lida usa/encontra.

| Preditor | Evidência | Fonte |
|---|---|---|
| Desmatamento anterior / vizinho (contágio) | Entra nos modelos de maior desempenho; mudança recente é o top em Cramér's V no Vetor Norte | D2, D6, D7, D10 |
| Distância a estradas, cidades, rios | Padrão em todos; distância a centros urbanos relevante na franja da RMBH; mas coeficiente de estradas n.s. no MATOPIBA | D1, D2, D6, D12 |
| Áreas protegidas | Efeito protetor (−0,22) | D1, D12 |
| Aptidão agrícola, relevo, clima/estação seca | Usados em Colman e Rosa; relevo/localização dominam Zanella (pode refletir confusão espacial) | D1, D2, D4 |
| Tamanho do imóvel / status do CAR | Estrutura conformidade com Reserva Legal; CAR reduz desmatamento ilegal com efeito decrescente | D13, D14, D19 |
| Preço da terra, gado, lavouras | Usados (Colman, Stan, Espindola); coeficiente de preço não lido | D1, D3, D12 |
| Embargo/autuação prévia | **Não achamos estudo que o use como preditor**; é o centro da evidência causal | C1–C6 |
| Fogo: memória temporal (EWMA 3/7/15 d de clima/vegetação) | Único estágio que melhorou todos os modelos; estáticos ajudaram pouco | F1 |
| Fogo: clima, NDVI, umidade | Dominam; seca/UR respondem por ~90% da importância ao replicar índice INPE | F1, F4, F7 |

## 5. Lições de método e armadilhas a evitar

1. **Validação aleatória infla.** R² 0,53 → 0,14 (Ploton, C14); 0,9 → 0,24 (Meyer, C18, snippet). Leal 2020 (D11)
   usa divisão aleatória. Use blocos espaciais (município/grade grossa) × ano de corte. O alcance da
   autocorrelação é escolha de desenho (Ploton viu ~100 km em outro contexto): estimar com variograma local.
2. **Vazamento temporal** (C15; regra 3 do CLAUDE.md). Fontes com publicação defasada (CAR, embargos,
   PRODES, MapBiomas) devem entrar pela data de *publicação*. Covariáveis do mesmo dia tornam o modelo
   retrospectivo (declarado em F1).
3. **Eventos raros:** AUC-ROC e acurácia enganam (C16). F2 tem AUC-ROC 0,89 com F1 0,0073.
   Reportar AUC-PR, precision@k, lift, recall top-k.
4. **Pseudoausências:** AUC-PR depende da razão escolhida (1:10 no treino vs. 1:100 no teste em F1);
   números de desenhos diferentes não são comparáveis.
5. **Holdout espacial com poucos positivos é instável** (6 positivos em Pau Furado, F1); desempenho no
   holdout foi pior que na CV para XGBoost e LR e melhor para RF. Escolher modelo só pela CV engana.
6. **Fiscalização é endógena.** Autuação mede onde o órgão olha (C1, C5, C8). O teste de campo da EPA
   mostra viés de seleção em dados históricos de inspeção (cobriam ~2% dos sítios). Y = "ser autuado"
   é Y fraco; preferir o evento subjacente ou combiná-lo, com cobertura de nuvens/esforço como controle.
7. **Não estacionariedade:** a eficácia de multas/embargos caiu após 2019 (C9, C10, snippets); a relação
   X→Y muda — mais um motivo para backtest temporal com múltiplos cortes.
8. **Pareamento importa:** sem ele, o efeito da lista suja foi superestimado em > 70% (C4).
9. **Supressão legal vs. ilegal:** a maior parte do desmatamento futuro no Cerrado pode ser legal
   (D19, snippet). Sem separar via CAR/Reserva Legal/autorização, o modelo prediz demanda agrícola, não risco.
10. **Escala/MAUP:** resultados em grade de 1–25 km não se traduzem em imóvel (D1, D3, D9). Imóveis com
    mais de um CAR são ligados só ao maior no cruzamento SICOR×CAR (C12, limite inferior).
11. **Ruído de rótulo:** MapBiomas exclui mudanças < ~1 ha e tem 83%/73% de acerto em perda/ganho (D16) —
    relevante para supressão pequena na RMBH. Foco ativo depende da passagem do satélite e mistura
    queima agropecuária legal com incêndio (F2).
12. **Replicar um índice de risco** (R² 0,82, F7) não valida contra fogo observado.
13. **Sazonalidade domina o fogo:** reportar desempenho dentro da estação seca.
14. **Poucos anos de teste** (1 ano em F2, D8) tornam as conclusões frágeis.
15. **Autocorrelação espacial em fogo:** não achamos tratamento documentado nos trabalhos lidos (lacuna).

## 6. Fiscalização guiada por predição e otimização

- Evidência causal de que priorizar por monitoramento funciona (C1) e de que **listas prioritárias bem
  desenhadas** reduzem emissões mais que listas aleatórias (C2: ≥ 25% em média, número do preprint NBER).
- Efeito localizado: fiscalização funciona em clareiras grandes, não nas pequenas (C5), e custa ~USD 3.500/
  inspeção na Amazônia — ordem de grandeza para o modelo de custos da sessão 09.
- ML + teste de campo: C8 é o único desenho com avaliação em campo, mas é EUA/resíduos perigosos.
- **Não achamos** otimização de inspeções com predição de risco por imóvel no Cerrado/Mata Atlântica,
  nem uplift aplicado a este contexto. Referências canônicas de calibração (ex.: Niculescu-Mizil & Caruana
  2005) e uplift **não foram verificadas** nesta sessão e não estão citadas.

## 7. RMBH, Quadrilátero Ferrífero e carste

Evidência encontrada é descritiva ou de cenário, sem modelo preditivo por imóvel:
- Expansão urbana: Vetor Norte (D6); autômatos celulares com RNA em centros urbanos (D17).
- Mineração: 3.570 ha de vegetação nativa até 2020 no Quadrilátero, e compensação evitaria só 3% (D15).
  Outros estudos (mineração 1985–2011: +213% de área minerada, ~3.263 ha de floresta; LCM com projeção a
  2053) apareceram só em snippet — **não verificados**.
- Carste: crescimento urbano em Sete Lagoas associado a poços improdutivos e possível sobre-exploração (D18).
- Fogo: Gandarela tem apenas estudos de UC (F3, F5).
- Mata Atlântica: perda de floresta madura em terreno plano (declividade média ~6,1°); 27% das florestas
  jovens foram novamente limpas (D16).

## 8. Risco ambiental × outcomes econômicos

- **Exposição:** 36% do crédito rural subsidiado de 2020–24 foi para imóveis com desmatamento desde 2009 (C12).
- **Efeito da restrição de crédito sobre desmatamento:** Res. 3.545/2008 reduziu desmatamento (C3, Amazônia).
- **Inadimplência/Proagro/valor da terra:** não encontramos estudo revisado por pares ligando embargo,
  desmatamento ou CAR a inadimplência, sinistro Proagro ou valor da terra. Também não achamos avaliação do
  efeito de desempenho de carteira das sucessoras (Res. BCB 140/2021, CMN 5.081/2023; descrições regulatórias
  vistas só em imprensa/escritórios — **não verificadas**; a sessão 05 deve ler os textos normativos).
- Consequência: a conexão "risco ambiental → perda econômica" é hipótese do AgroRisk, não resultado
  estabelecido. Registrar como risco de tese (ver seção 11).

## 9. Desenhos de modelo recomendados para a sessão 06

Todos com: corte temporal anual (vários cortes, *expanding window*), features só com data de publicação
< corte, CV em blocos espaciais × tempo, baselines obrigatórios e relato de lift/recall top-k/AUC-PR/
calibração.

**Desenho A — Ranking de imóveis por P(supressão de vegetação nativa em 12–24 m), GBM com baselines.**
Unidade: imóvel/CAR × ano de corte. Features: desmatamento recente próprio e vizinho (contágio),
distâncias (estradas, núcleo urbano, mineração), aptidão, tamanho, status CAR, áreas protegidas, clima.
LightGBM + regressão logística regularizada; baselines: "histórico do imóvel" e "distância a desmatamento
recente". Pró: ligação direta com Rosa/Colman. Contra: poucos eventos na RMBH → treino em MG ampliado;
exige separar legal/ilegal.

**Desenho B — Y composto (supressão ou embargo ou fogo em vegetação nativa), modelo hierárquico/multitarefa.**
Aumenta eventos (poder estatístico) e o valor para o comprador; modelos por componente com agregação
calibrada. Contra: fiscalização endógena (armadilha 6) — tratar embargo como desfecho secundário e
modelar esforço de fiscalização; ponderar componentes por severidade.

**Desenho C — Fogo em vegetação nativa por imóvel, Y = área queimada anual (MapBiomas Fogo), memória temporal.**
Sazonal, com histórico de fogo do imóvel/vizinhança e clima defasado; evita viés de passagem de satélite
(F1, F2). Contra: defasagem/licença do MapBiomas Fogo ainda não verificadas; separar queima agropecuária.

**Camada transversal (sessão 09):** prescrição sob orçamento via otimização de inspeções, com custo
unitário parametrizado (C5) e avaliação contra a regra "fiscalizar onde houve alerta" (C1, C2).

Recomendação preliminar (sujeita à sessão 06): começar por **A** com **B** como extensão, mantendo C como
módulo. Contra-argumento relevante: a taxa de evento por imóvel/ano na vitrine é desconhecida; se for
muito baixa, B ou o recorte maior de MG são obrigatórios.

## 10. Oportunidades de inovação para o AgroRisk

| # | Oportunidade | Evidência (lacuna) | Por que concorrentes/academia não fazem | Esforço |
|---|---|---|---|---|
| 1 | **Ranking por imóvel em MG com backtest temporal + CV espacial em blocos e métricas de ranking** | Nenhum trabalho encontrado em Cerrado/Mata Atlântica por imóvel (D1, D3, D4, D10 são grade/município/Amazônia) | Produtos de consulta não publicam validação; PrevisIA divulga acurácia não comparável (D10) | M |
| 2 | **Transparência metodológica aberta** (protocolo, código, calibração, IC) | D10 "dado não publicado"; D1 dados "sob solicitação" | Incentivo comercial contra expor desempenho | P |
| 3 | **Separar supressão legal de ilegal** via CAR/Reserva Legal/autorizações | D13, D19 mostram que o risco se estrutura por tamanho e conformidade | Modelos de grade preveem conversão, não ilegalidade | M |
| 4 | **Ligação com outcome econômico** (inadimplência, sinistro Proagro) | Nenhum estudo verificado (seção 8); CPI mede só exposição (C12) | Exige dados de contrato (privados) e parceria | G |
| 5 | **Prescrição sob orçamento** com custo por inspeção e avaliação vs. regra de alerta | C2 e C8 em outros contextos; nada no Cerrado/MA | Exige modelo preditivo calibrado + custos operacionais | M |
| 6 | **Fogo por imóvel com Y de área queimada e memória temporal** | F1 mostra ganho de EWMA; todos os trabalhos são UC/pixel (F1–F7) | Rótulos de foco ativo são ruidosos | M |
| 7 | **Franja metropolitana/carste/mineração integrada** (pressão urbana, recarga, Quadrilátero) | D6, D15, D18 descritivos; nada preditivo por imóvel | Escopo regional pequeno para grandes players | M |
| 8 | **Modelar o esforço de fiscalização** para corrigir a endogeneidade do Y autuação/embargo | C1, C5, C8 | Exige dados de esforço (alertas, nuvens) | G |

## 11. Riscos e contra-evidências

- **Evento raro na RMBH:** a literatura de desempenho vem de regiões de alto desmatamento; o AgroRisk pode
  ficar sem poder estatístico na vitrine.
- **Y composto pode herdar o viés da fiscalização** (armadilha 6).
- **Colman 2024 e Stan 2015 sugerem que cenários de grade já cobrem parte do valor**; o diferencial é o
  ranking por imóvel e a validação — precisa ser demonstrado.
- **Tese de valor econômico não sustentada por literatura:** a ligação risco ambiental → inadimplência
  ainda não tem evidência publicada; pode ser que o comprador valorize *conformidade regulatória* (Res.
  CMN/BCB) mais do que probabilidade de perda.
- **Cobertura de busca limitada:** poucas buscas por frente e paywalls; "não encontramos" ≠ "não existe".
  Há literatura nacional (teses, anais) provavelmente não alcançada.
- **Transferência:** os benchmarks quantitativos vêm de Amazônia/Peru/UCs; não extrapolar para a RMBH.

## 12. Perguntas em aberto

1. Qual a taxa de evento por imóvel/ano (supressão, embargo, fogo) na vitrine e no recorte ampliado de MG? (sessões 01, 02, 06)
2. Qual a defasagem de publicação de PRODES/DETER-Cerrado, MapBiomas Alerta/Fogo, CAR e embargos? (sessão 02)
3. Como identificar supressão *autorizada* em MG (fonte estadual) para separar legal de ilegal?
4. MapBiomas Fogo: acurácia por bioma, licença de uso comercial, defasagem (ATBD C5 não lido).
5. Existe base de contratos SICOR/Proagro com CAR e inadimplência acessível a custo viável? (sessão 05)
6. Texto normativo e efeitos de Res. BCB 140/2021 e CMN 5.081/2023 (sessão 05).
7. Ler os PDFs de: Colman 2024 (Tabela S2, AUC), Zanella 2017, Faria 2026, Singh 2022, Arruda 2024, Kuschnig 2023, Roberts 2017, Meyer 2018; abrir o repositório de Pádua 2026 e o Zenodo de Segura-Garcia (licenças).
8. Confirmar autoria/ano do teste de campo da EPA (C8) e a identificação de Melo & Resende Filho (C13).
9. Qual alcance de autocorrelação espacial usar nos blocos (estimar variograma nos dados da vitrine)?

## 13. Registro de licenças

Esta sessão não usa dados. Bases citadas que exigem linha em `licencas.md` antes do uso: MapBiomas Fogo e
Alerta, PRODES/DETER, SICAR, SICOR/BCB, BDQueimadas (INPE), ERA5-Land, Hansen GFC (sessões 02 e 05).
