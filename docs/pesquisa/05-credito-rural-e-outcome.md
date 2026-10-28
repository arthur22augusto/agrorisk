# 05 — Crédito rural e outcome econômico na região

- Sessão: 05 · Data: 2026-10-28 · Status: rascunho para a sessão 06
- Método: 4 agentes (regulação, outcomes/nichos, comprador cético, estatístico) + consulta à API do SICOR/BCB.
- **Limite importante:** os textos primários das normas (normativos.bcb.gov.br etc.) deram 403/ilegível. A maior parte da regulação abaixo vem de resumos de imprensa e escritórios. Tudo marcado **"não verificado"** precisa ser confirmado na norma original antes de citar em material externo.

## 1. Resumo executivo

1. **O que já é obrigação do banco** (e portanto commodity): CAR ativo e ausência de embargo Ibama por desmatamento ilegal (MCR 2-9, Res. CMN 5.193/2024, vigente desde 02/01/2025). O cruzamento com Prodes foi adiado: >15 módulos fiscais em 01/2027, 4–15 em 07/2027, até 4 em 01/2028 (Res. CMN 5.303/2026, fonte de imprensa; fontes divergem, há ação da CNA no STF).
2. **Espaço comercial** está no que não é vedação obrigatória: embargo/autuação estadual (MG), outorga e escassez hídrica, UC/TI fora de floresta pública, Mata Atlântica (sem Prodes) e a **evidência de gestão de risco** exigida pela PRSAC (obrigação de *processo*, não de resultado).
3. **Crédito rural na vitrine (SICOR, dado coletado):** ~R$ 1,40 bi nominais contratados em 2015–2024 nos 34 municípios da RMBH + Sete Lagoas (custeio R$ 972 mi; investimento R$ 430 mi), ~R$ 90–180 mi/ano. Concentração em poucos municípios (§3). Atenção: o município do SICOR agregado pode não ser o do imóvel (§3.3).
4. **Critério de pronto — conclusão explícita:** com dado público, o outcome só é observável em **município × ano** (crédito contratado SICOR) e **UF × mês** (inadimplência SCR.data). **Não há outcome público por imóvel/operação** (não encontrado; confirmar via LAI). O elo risco → inadimplência/perda **exige dado de cliente** (§5.3).
5. **Comprador cético (persona, opinião):** "piloto grátis; não compraria hoje". Gatilho de compra: lift sobre o baseline que ele já tem (regra + bureau), ligação com atraso/perda, relatório aceito pela auditoria. Predição de evento sem elo com perda vira commodity.
6. **Recomendação ao 06:** 1º outcome = atraso >90 dias/renegociação por operação (dado do cliente); em paralelo, event study de embargo → crédito SICOR em MG como teste de sanidade com dado público (mede restrição mecânica de crédito, **não** risco).

## 2. Mapa regulatório (hoje: 2026-10-28)

### 2.1 O que obriga a instituição financeira
| Norma | Conteúdo | Vigência / status | Fonte |
|---|---|---|---|
| Lei 12.651/2012, art. 78-A (red. Lei 13.295/2016) | Crédito agrícola exige imóvel no CAR (desde 31/12/2017) | vigente | [Planalto](https://www.planalto.gov.br/ccivil_03/_Ato2015-2018/2016/Lei/L13295.htm) |
| Res. CMN 5.081/2023 | Ampliou impedimentos a todos os biomas | **revogada** em 02/01/2025 pela 5.193 | [okai](https://okai.com.br/documento/2023-06-29/resolucao-cmn-n-5-081) |
| Res. CMN 5.193/2024 (MCR 2-9) | Veda crédito: CAR ausente/cancelado/suspenso; embargo Ibama por área desmatada ilegalmente (exceto financiar a recuperação); floresta pública tipo B (exceções); cria cruzamento Prodes p/ supressão após 31/07/2019. Limite de 5% do imóvel/20 ha para embargos novos: **não verificado no texto** | desde 02/01/2025 | [normasbrasil](https://normasbrasil.com.br/norma/resolucao-5193-2024_470860.html), [Mattos Filho](https://www.mattosfilho.com.br/unico/alteracao-normas-credito-rural/) |
| Res. CMN 5.303/2026 | Adia Prodes: >15 MF 04/01/2027; 4–15 MF 01/07/2027; ≤4 MF 03/01/2028; amplia alternativas à ASV (atos equivalentes, TCA) | divulgada ~05/2026; **conflito de fontes** (CNA falava em 01/04/2026) e possível norma posterior: **não verificado** | [Comprerural](https://comprerural.com/prodes-no-credito-rural-nao-acabou-e-nova-regra-do-cmn-apenas-adia-bloqueios-no-agro/), [CNA](https://cnabrasil.org.br/noticias/credito-rural-setor-produtivo-de-sc-considera-positiva-prorrogacao-do-prodes) |
| ADI/ação CNA no STF contra Prodes no crédito | ajuizada 15/04/2026 | desfecho **não verificado** | [Cultivar](https://revistacultivar.com.br/noticias/cna-aciona-stf-contra-uso-do-prodes-no-credito-rural) |

Lacunas: texto do MCR 2-9 sobre **UC/TI**, **Cerrado/Mata Atlântica** e **embargo estadual** não confirmado; regra transitória de embargos até 30/06/2027 citada na Atualização MCR 756 (conteúdo não verificado). Fonte candidata: [Voto CMN 94/2024](https://normativos.bcb.gov.br/Votos/CMN/202494/Voto_do_CMN_94_2024.pdf) e [busca de normas BCB](https://www.bcb.gov.br/estabilidadefinanceira/buscanormas).
Pontos para pequenos produtores (cliente-alvo): o Prodes só chega a ≤4 MF em 2028; o Prodes não distingue desmatamento legal/ilegal ([nota CNA](https://www.cnabrasil.org.br/storage/arquivos/VF_dtec.nt-09.Prodes.01abril_2026.pdf)); Prodes cobre Amazônia e Cerrado — **Mata Atlântica em MG sem checagem equivalente: gap potencial, não verificado**.

### 2.2 Gestão de risco da instituição
- Res. CMN 4.945/2021 (PRSAC), Res. CMN 4.943/2021, Res. BCB 139 (relatório GRSAC; S1–S4, até 90 dias após 31/12): [Felsberg](https://www.felsberg.com.br/agenda-esg-banco-central-aperfeicoa-normas-de-gerenciamento-de-riscos-sociais-ambientais-e-climaticos/), [Mattos Filho](https://www.mattosfilho.com.br/unico/banco-central-esg/), [BMA](https://www.bmalaw.com.br/conteudo/direito-ambiental-e-mudancas-climaticas/artigos-e-noticias/esg-sistema-financeiro-nacional-novas-regras-sobre-gerenciamento-de-riscos-climaticos-sociais-e-ambientais/pdf). Vigência exata da 4.945 e obrigações de cooperativas S4/S5: **não verificadas**.
- Natureza: obrigação de **processo** (política, procedimentos, evidência); o BCB não fixa critério mínimo. Um score preditivo explicável serve como evidência de gestão, não como exigência legal.
- "Bureau de Crédito Rural" do BCB (cruza Ibama etc.): citado só em [imprensa](https://www.folhavitoria.com.br/folha-business/banco-central-impediu-a-liberacao-de-r-62-bilhoes-em-credito-rural-devido-a-irregularidades-ambientais/); norma, estrutura e acesso **não verificados**.

### 2.3 Proagro / Zarc
- Res. CMN 5.127/2024: para enquadramentos desde 01/07/2024, verificação por sensoriamento remoto da emergência e do cumprimento do Zarc ([normasbrasil](https://www.normasbrasil.com.br/norma/resolucao-5127-2024_457530.html)).
- Res. CMN 5.224 e 5.227/2025: reformulação (base atuarial, reincidência por severidade, limite de enquadramento obrigatório R$ 270 mil → R$ 200 mil) ([Coop](https://cooperativismodecredito.coop.br/2025/06/cmn-reformula-regras-do-proagro/), [MundoCoop](https://mundocoop.com.br/agronegocio/cmn-reduz-para-r-200-mil-limite-de-enquadramento-no-proagro/)); teto de gastos com bloqueio por município ([Monitor do Mercado](https://monitordomercado.com.br/noticias/mercados/341701-banco-central-cria-teto-de-gastos-e-bloqueios-para-conter-custos-do-proagro/)). Res. 5.315/2026 (alíquotas): **não verificada** ([Canal Rural](https://www.canalrural.com.br/politica/cmn-atualiza-aliquotas-do-proagro-e-muda-regras-de-controle/)). Texto do Proagro Mais: não verificado.
- Pronaf/Pronamp: nenhuma regra socioambiental específica além do MCR 2-9 (exceções por módulo fiscal/assentamentos) — não verificado; ver MCR cap. 10.

### 2.4 Outras
- Lei 11.428/2006 (Mata Atlântica) e Decreto MG 47.749/2019: **não verificados**.
- EUDR (mercado, não crédito): Reg. (UE) 2025/2650 — aplicação 30/12/2026 (grandes/médios) e 30/06/2027 (micro/pequenos); revisão de simplificação de 04/05/2026 sem reabrir o texto; nada posterior a maio/2026 foi achado ([Vinciworks](https://vinciworks.com/blog/eudr-delayed-again-what-changed-what-is-now-fixed-and-what-businesses-should-do-in-2026/), [Arendt](https://www.arendt.com/news-insights/news/eudr-simplification-review-published-what-the-2026-package-means-for-in-scope-companies/)). Corte: 31/12/2020. Efeito em pequenos produtores de MG (café, celulose): não verificado.

### 2.5 Instabilidade
A regra mudou em 2023, 2024 e 2026 e está sob contestação judicial: o produto não pode depender de uma data de vigência específica.

## 3. Crédito rural na vitrine (SICOR, dados coletados)

### 3.1 Fonte e método
Matriz de Dados do Crédito Rural, API OData: `https://olinda.bcb.gov.br/olinda/servico/SICOR/versao/v2/odata` (entidades `CusteioMunicipioProduto` e `InvestMunicipioProduto`; cada linha = município × produto × mês × programa × fonte; valor e área). Script: `scripts/05_sicor_vitrine.py` → `data/interim/sicor_vitrine_ano.csv` (não versionado). Consulta feita em **2026-10-28**. Lista de municípios **provisória** (RMBH 34 + Sete Lagoas, escrita de memória e conferida contra as consultas); a lista oficial e o Colar ficam para a sessão 01. Todos os 35 nomes retornaram registros, exceto Rio Acima (3 custeio/0 invest.) e Raposos (0/1), possivelmente pouco crédito rural.

### 3.2 Resultados (valores **nominais**, R$ milhões, soma custeio + investimento)
| Ano | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 |
|---|---|---|---|---|---|---|---|---|---|---|
| R$ mi | 149,9 | 101,8 | 139,6 | 143,7 | 90,8 | 142,0 | 148,9 | 135,2 | 178,2 | 172,3 |
| Registros agregados | 943 | 687 | 784 | 757 | 617 | 635 | 599 | 558 | 607 | 686 |

- Total 2015–2024: **R$ 1.402 mi** (custeio 972; investimento 431).
- Maiores municípios no período (R$ mi): Belo Horizonte 353, Contagem 185, Sete Lagoas 124, Itaguara 118, Esmeraldas 79, Rio Manso 72, Baldim 65, Mateus Leme 61, Florestal 61, Jaboticatubas 49.
- Nº de contratos: **não disponível** nestas entidades (a linha é agregada; "registros" ≠ contratos). Finalidades/linhas por produto e programa foram coletadas (`cdPrograma`, `cdFonteRecurso`) mas ainda não tabuladas; a leitura por produto fica para a sessão 07.

### 3.3 Ressalvas (não verificado)
- **BH e Contagem liderando** (áreas urbanas) sugere que o campo `Municipio` pode refletir a agência/sede da instituição e não o município do imóvel. Confirmar no dicionário do MDCR antes de usar como exposição territorial. Isto pode inviabilizar o SICOR como "crédito no território".
- Valores nominais (sem deflacionar); o ano 2026 existe mas está incompleto e foi excluído.
- **Participação de cooperativas e principais instituições:** não coletado. As entidades `SegmentoIF`/`SegmentoIFRegiaoUF` existem na API, mas o corte é por UF/região, não por município. Próximo passo: consultar MG inteira por segmento (cooperativa de crédito × banco) e tomar a participação estadual como proxy, rotulada como tal.
- Licença: o portal declara "licença aberta" ([FAQ](https://dadosabertos.bcb.gov.br/pages/perguntas-frequentes)); o termo exato do MDCR não foi verificado (ver `licencas.md`).

## 4. Outcomes mensuráveis com dados públicos
| Outcome | Fonte | Granularidade | Defasagem/série | Uso agora |
|---|---|---|---|---|
| Crédito contratado | [MDCR/BCB](https://dadosabertos.bcb.gov.br/en/dataset/matrizdadoscreditorural) | município (talvez da agência) × produto × mês | início da série visto: 2013; defasagem: não verificada | **sim** (restrição de crédito, não risco) |
| Inadimplência rural | [SCR.data](https://dadosabertos.bcb.gov.br/dataset/scr_data), [metodologia](https://www.bcb.gov.br/content/estabilidadefinanceira/scr/scr.data/scr_data_metodologia.pdf); série [SGS 21146](https://dadosabertos.bcb.gov.br/dataset/21146-inadimplencia-da-carteira-de-credito-com-recursos-direcionados---pessoas-fisicas---credito-ru) | **UF** × mês (>90 dias/carteira) | ~30 dias; SGS desde 03/2011 | contexto agregado apenas |
| PSR (apólices) | [SISSER/MAPA](https://dados.agricultura.gov.br/en/dataset/sisser3/resource/54e04a6b-15b3-4bda-a330-b8e805deabe4), [dicionário](https://dados.agricultura.gov.br/dataset/baefdc68-9bad-4204-83e8-f2888b79ab48/resource/2c5c55d0-1473-4749-b08f-cfaf887a9fa3/download/dicionariodedados-sisser.pdf) | apólice; município e sinistro: **não verificado** | 2006–2025; atualização anual (CC-BY indicado) | candidato, verificar campos |
| Proagro (sinistros) | conjunto não localizado no portal BCB | agência (norma de 2002), não imóvel | não verificado | pedir via LAI |
| Embargos Ibama | [dados abertos Ibama](https://dadosabertos.ibama.gov.br/) | polígono por termo | houve interrupção em 2020 ([Fiquem Sabendo](https://news.fiquemsabendo.com.br/p/nota-sigilosa-do-ibama-preve-que)); licença não verificada | exposição/evento |
| Autos SEMAD/IEF, ESTBAN/IF.data rural, operações desclassificadas (BCB), valor da terra MG | — | — | **não verificado** (candidatas: IDE-Sisema; Emater-MG/SEAPA/INCRA) | pendente |

**Dado de operação com CAR/imóvel:** não encontrado em nenhum recurso listado; o banco tem o CAR (exigido no SICOR) mas ele não parece publicado. Confirmar via Swagger/OData e **pedido LAI ao BCB** (contato do catálogo: sicor.derop@bcb.gov.br).

## 5. Evento → custo e como medir

### 5.1 Tabela evento → norma → consequência → quem verifica → dado público
| Evento | Norma | Consequência econômica | Quem verifica | Dado público |
|---|---|---|---|---|
| Embargo Ibama/ICMBio | MCR 2-9 (5.193) | **Obrigatório:** crédito vedado (exceto recuperação) | Instituição, base BCB/Ibama | [Ibama](https://dadosabertos.ibama.gov.br/) |
| Embargo/autuação estadual (SEMAD/IEF) | não verificado se o MCR cobre | Só política interna (PRSAC); passivo indireto | Banco | IDE-Sisema (não verificado) |
| Supressão ilegal pós-31/07/2019 | MCR 2-9; adiada pela 5.303 | Exige ASV/PRAD/TAC/laudo, senão bloqueio | Banco via Prodes | [TerraBrasilis](https://terrabrasilis.dpi.inpe.br/); MapBiomas Alerta (candidata) |
| Sobreposição UC/TI | só floresta pública tipo B confirmada | impedimento ou política interna | Banco | CNUC/MMA; FUNAI |
| CAR cancelado/suspenso/ausente | Lei 12.651 art. 78-A; MCR 2-9 | **Obrigatório:** vedação ("pendente": recibo basta, MCR 2-1-12) | Banco | [SICAR](https://www.car.gov.br/publico/imoveis/index) |
| Uso de água sem outorga / escassez | nenhuma norma de crédito conhecida | Continuidade da operação (irrigação −25% do outorgado em 2024) | ninguém por obrigação | IGAM/IDE-Sisema |
| Incêndio | sem impedimento direto | Perda de safra; depende de Proagro/seguro | perito/agente | INPE Queimadas, MapBiomas Fogo |
| Sinistro Proagro negado (Zarc/uso) | Res. 5.127/2024; MCR 12 | Produtor perde cobertura; reflexo no banco: não verificado | Agente Proagro + sensoriamento | Zarc/MAPA |

### 5.2 Ordens de grandeza (imprensa/fontes secundárias; sem número específico de MG)
- Crédito barrado por CAR/embargo: >30 mil operações, ~R$ 6,2 bi no 1º semestre de 2024 (a mesma reportagem cita R$ 726,2 mi sem esclarecer a relação; a manchete diz "R$ 62 bi", que **não se confirma**); desde 2020, >2,2 mil operações vetadas por critérios socioambientais, >R$ 1 bi ([Folha Vitória](https://www.folhavitoria.com.br/folha-business/banco-central-impediu-a-liberacao-de-r-62-bilhoes-em-credito-rural-devido-a-irregularidades-ambientais/)). É custo de oportunidade, não perda; fonte original (BCB) não verificada.
- Proagro: ~R$ 9 bi pagos em 2024 (R$ 6 bi em 2023), 95% no PR e RS ([CQCS](https://cqcs.com.br/noticia/tcu-manda-bc-controlar-seguro-do-proagro-pago-indevidamente/)); R$ 27,6 bi em 2015–jan/2025 ([Câmara](https://www2.camara.leg.br/atividade-legislativa/comissoes/comissoes-permanentes/capadr/apresentacoes-em-eventos/eventos-de-2025/GuilhermeRiosCNA.pdf/view)); sinistros deferidos 22% (Proagro Mais) e 18% (Tradicional) do segurado em 2019–2021 ([CPI/PUC-Rio](https://www.climatepolicyinitiative.org/pt-br/publication/revelando-incentivos-implicacoes-do-desenho-das-politicas-publicas-de-seguro-rural-no-brasil/)). Quase nada em MG.
- Provisão, perda de garantia/desvalorização da terra, dano reputacional/EUDR para o credor: **não verificado**; nenhuma fonte pública achada. Qualquer elo "evento → inadimplência" é hipótese que o backtest deve testar.

### 5.3 Como medir risco → outcome sem correlação espúria (estatístico-modelagem)
Todos os números de poder abaixo são raciocínio, **não verificados**.
- **D1 (exploratório):** painel município × ano, MG inteira (~853 municípios), embargo novo/área rural (t−1) → log(crédito SICOR/ha), efeitos fixos município e ano-UF, erros agrupados por microrregião.
- **D2 (recomendado com dado público):** event study escalonado (Callaway–Sant'Anna/Sun–Abraham) no primeiro embargo grande do município, janela ±8 trimestres, data de **publicação**, pré-tendência obrigatória. Mede restrição mecânica do crédito, não risco.
- **D3:** portarias IGAM de escassez (município × safra) → crédito de irrigados/hortaliças e sinistros PSR.
- **Armadilhas:** escala do município; falácia ecológica; **censura por seleção** (quem está embargado não recebe crédito, logo o outcome só existe para o não embargado); autocorrelação espacial (cluster/blocos); vazamento por defasagem de publicação; fiscalização concentrada onde há denúncia; múltiplas comparações (pré-registrar 1 outcome primário).
- **Poder:** RMBH ≈ 34 × 10 = 340 unidades-ano; com 5–10% de eventos restam ~15–35, concentrados. Detectar 0,2 DP com DiD pede ordem de 100–200 unidades tratadas. **A RMBH sozinha provavelmente não basta**: treinar em MG (ou mais), RMBH como subgrupo. Contar eventos reais antes de modelar.
- **Piloto com dado do cliente** (uma linha por operação): ids anonimizados, CAR/matrícula, datas de contratação/vencimento/liberação, valor, finalidade, produto, taxa, prazo, status mensal de pagamento (em dia, 30/60/90+), renegociação/prorrogação, garantia e valor, seguro (PSR/Proagro), sinistro, data de corte. **Pedir também operações recusadas ou as regras de recusa** (viés de seleção). Métricas: AUC-PR, precision@k, lift@k com IC por bootstrap em blocos; ΔAUC-PR sobre o modelo próprio do banco; Brier/curva de confiabilidade; prescrição = perda evitada sob orçamento. Cláusulas de LGPD e sigilo bancário antes do recebimento.

## 6. Validação com o comprador cético (persona; opinião, não fato)
- Dor atual: processo e auditoria (PRSAC/GRSAC); a vedação do MCR 2-9 ele já cumpre com bureau. Predição de evento não tem orçamento sem elo com perda.
- Compraria: priorização de carteira (monitoramento pós-concessão), alerta de eventos **não vedados** (estadual, outorga, UC), trilha de auditoria explicável; prescrição só depois de provar a predição.
- Preço (chute da persona, não dado de mercado): piloto grátis/simbólico por 3–6 meses; depois assinatura anual na casa de **dezenas de milhares de R$**, teto R$ 50–100 mil se houver ganho de auditoria; ciclo de compra 4–9 meses; cooperativa pequena prefere preço fixo.
- Aceite de piloto sugerido: lift ≥2x vs. baseline (regra + bureau) no top 10%, taxa de atraso superior com IC, calibração estável entre safras, teto de falsos positivos, horas de analista poupadas, alertas de eventos não vedados detectados antes do banco, relatório aceito pela conformidade.
- Perguntas dele: por que o evento causa perda? qual o incremento sobre o que já tenho? falsos positivos e contestação do produtor? licenças e LGPD? quem mantém o modelo/escrow?

## 7. Nichos alternativos
### 7.1 Risco hídrico e outorga (cinturão verde)
Evidências: IGAM declarou escassez crítica no Rio das Velhas e Rio da Prata (Portarias 25 e 26, 09/2024; ~150 e ~170 outorgas afetadas segundo IDE-Sisema) ([Agência Minas](https://www.agenciaminas.mg.gov.br/noticia/novas-portarias-de-escassez-hidrica-impoem-restricoes-para-uso-da-agua-em-bacias-mineiras)); corte de 25% do volume outorgado para irrigação ([Panorama Minas](https://jornalpanoramaminas.com.br/?p=37917)); precedente de 2015 ([Demarest](https://www.demarest.com.br/portaria-igam-no-013-de-08-de-abril-de-2015/)); Decreto 49.072/2025 flexibiliza outorga de pequenos ([legisweb](https://www.legisweb.com.br/legislacao/?id=480841)); MG com ~501 mil ha em 8.541 pivôs (2020) ([ANA](https://metadados.snirh.gov.br/geonetwork/srv/api/records/e2d38e3f-5e62-41ad-87ab-990490841073)) — pivôs não representam o cinturão verde (aspersão/gotejamento).
Avaliação: evento discreto e datado (bom rótulo), mas mercado estreito e pagante incerto (CBH e prefeitura raramente pagam por modelo). Nº de outorgas na RMBH/Colar, portal aberto de outorgas e CBHs: **não verificados**. Teste barato: perguntar a 3–5 cooperativas de MG se restrição de outorga entra hoje na análise de custeio. **Veredito provisório: complemento (feature/alerta) do produto de crédito, não produto isolado.**

### 7.2 Due diligence de terras na franja urbana
Evidências: Decreto 48.891/2024 dá à Agência RMBH a fiscalização de parcelamento do solo na RMBH e Colar ([legisweb](https://www.legisweb.com.br/legislacao/?id=464286), [Agência Minas](https://www.agenciaminas.mg.gov.br/noticia/governo-de-minas-publica-novo-decreto-para-a-fiscalizacao-de-parcelamento-do-solo-na-rmbh/)); Lei 6.766/79 art. 53 e [IE INCRA 5/2022](https://irib.org.br/noticias/detalhes/instrucao-especial-incra-n-5-de-29-de-julho-de-2022); SIGEF não prova propriedade e a sobreposição CAR × SIGEF é o ponto central ([CONTECC 2025](https://www.confea.org.br/midias/uploads-imce/CONTECC2025/AGRO/AN%C3%81LISE_DE_SOBREPOSI%C3%87%C3%83O_NO_CADASTRO_AMBIENTAL_RURAL_(CAR)_COM_USO_DA_BASE_FUNDI%C3%81RIA_DO_SIGEF.pdf)); o Provimento CNJ 195/2025 (SIG-RI) tende a commoditizar alertas de sobreposição para cartórios ([IRIB](https://www.irib.org.br/noticias/detalhes/geotecnologia-no-registro-de-imoveis-provimento-cnj-195-2025-institui-mapeamento-digital-das-matriculas)).
Avaliação: é "consulta/diagnóstico", a camada que o CLAUDE.md classifica como commodity; compradores e disposição a pagar não verificados; dados de prefeituras/Agência RMBH não verificados. **Veredito provisório: pior encaixe com o wedge**, a menos que entregue score de risco de regularização (embargo/autuação urbanística).

## 8. Oportunidades de inovação para o AgroRisk
1. **Cobrir o que o banco não é obrigado a checar** (embargo/autuação estadual MG, outorga/escassez, UC/TI, Mata Atlântica). Evidência: o MCR 2-9 foca em Ibama, CAR e Prodes (§2.1); concorrentes de consulta tendem a replicar vedações legais — a lacuna específica por concorrente fica para a sessão 03. Esforço: M.
2. **Pronto-para-Prodes 2027/2028 para ≤4 MF:** priorizar carteira antes do prazo, cruzando com ASV/DAIA para reduzir falsos positivos (§2.1). Esforço: M/G.
3. **Predição como evidência de PRSAC/GRSAC** para cooperativas (trilha explicável, versão, data de corte), em vez de consulta (§2.2, §6). Esforço: M.
4. **Elo evento → perda como produto de pesquisa:** pré-registro e event study de embargo → crédito, e piloto com cooperativa medindo atraso/renegociação (§5.3). Diferencial de transparência. Esforço: G.
5. **Feed regulatório** (Res. 5.193/5.303, Decreto 49.072, portarias IGAM) como fonte de eventos e de risco de mudança de regra. Esforço: P.
6. **LAI ao BCB** (microdados SICOR com município do imóvel/CAR; Proagro por município). Esforço: P; incerteza alta.

## 9. Riscos e contra-evidências
- Sem outcome público por imóvel, a tese "risco → dinheiro" não é testável sem parceiro; o parceiro ainda não existe.
- O Y natural do vendedor (embargo/supressão) não é o Y do comprador (perda de crédito).
- Regra instável e judicializada (Prodes); o espaço de mercado pode encolher se o BCB absorver embargos estaduais no MCR.
- SICOR por município pode refletir a agência, não o imóvel (§3.3).
- Poucos eventos na RMBH (§5.3).
- Fontes regulatórias secundárias; vários itens não verificados.

## 10. Perguntas em aberto (sugestões para a sessão 06)
1. O campo `Municipio` do MDCR é o do imóvel ou o da agência? Há microdados/CAR (LAI)?
2. Participação de cooperativas e principais instituições em MG (consulta `SegmentoIF*` por UF).
3. SISSER/PSR traz município e sinistro? Proagro por município existe publicamente?
4. Texto atual do MCR 2-9 após a 5.303: UC/TI, embargos estaduais, Mata Atlântica? Status da ação no STF? Vigência da 4.945 para cooperativas S4/S5?
5. Autos SEMAD/IEF e outorgas IGAM baixáveis, georreferenciados e com que licença?
6. Há eventos suficientes em MG inteira (embargos Ibama, supressão) para 100–200 unidades tratadas?
7. Que cooperativa aceitaria piloto grátis com carteira histórica e operações recusadas? (entrevistar 3–5 compradores)
8. Série pública de valor da terra em MG (Emater-MG/SEAPA/INCRA) e licença.
