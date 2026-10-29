# 06 — Debate de especialistas e escopo do MVP

- Sessão: 06 · Data: 2026-10-29 · Escopo: síntese de pesquisa (sem código de análise)
- Formato: 3 rodadas — (1) propostas de `estatistico-modelagem`, `especialista-credito-regulacao`, `analista-mercado` (com pesquisa nova da frente B) e `engenheiro-dados-geo`; (2) ataque do `advogado-do-diabo` e do `comprador-cetico` (duas personas); (3) síntese e escolha do fundador.
- Decisão resultante: `docs/decisoes/escopo-mvp.md`.
- Legenda: **[F]** fato lido em fonte · **[I]** inferência · **[NV]** não verificado. Relatórios de subagentes: várias fontes são imprensa secundária ou resumos de busca (alguns primários deram 403/410). Orçamento, assinatura e disposição a pagar vindos de personas são **opinião, não fato**. Estimativas de poder são da sessão, não medições.

## 1. Resumo executivo
1. **Todos os especialistas convergiram em A como frente principal; ninguém sustentou B como MVP.** B tem a dor mais nítida (diligência do adquirente de carvão) mas faltam dados e comprador.
2. **O achado central do debate:** o único Y validável com dado público (supressão PRODES por CAR) é o mesmo que o MCR vai verificar de forma **determinística** (supressão × autorização de uso alternativo do solo) a partir de 2027–28. A predição só agrega onde a regra não alcança. O produto é, portanto, **filtro determinístico + priorização**, e o backtest precisa provar valor **contra a regra**.
3. **Nenhuma frente tem comprador pagante verificado.** As duas personas responderam "piloto grátis".
4. **Riscos metodológicos prioritários:** vazamento pela geometria do CAR; modelo que prevê "onde há mata + vizinhança de evento"; rótulo instável (PRODES × MapBiomas −0,37); multiplicidade no critério de sucesso.
5. **Decisão (fundador):** A-reformulada + discovery de B; critério primário único pré-registrado; Y provisório com **gate** de 5–8 h na sessão 07.

## 2. Rodada 1 — propostas

### 2.1 Estatístico (`estatistico-modelagem`)
- Y comum: PRODES ≥ 1 ha por CAR no ciclo ago–jul; não unir com MapBiomas (correlação anual −0,37, 01 §11); `Y_total` previsto, `Y_ilegal` e `Y_agro` derivados.
- Unidade CAR × t₀ (31/jul), h = 12 (24 secundário), inscrito ≥ 6 meses, ≥ 1 ha de nativa, cancelados mantidos.
- Teste 2021–2024 com purga de 12 meses e blocos espaciais; baselines: evento anterior, município, proximidade, logística (área nativa/total).
- Critério proposto: lift@10% ≥ 3 (IC95% inferior > 2), Δrecall@10% ≥ +8 pp, AUC-PR ≥ 2×, inclinação de calibração 0,8–1,2, lift ≥ 2,5 por fold. Poder: lift mínimo detectável ≈ +0,6 (pooled) e ≈ 13 pp de recall em 2024 isolado (estimativas).
- Y econômico (atraso > 90 dias) só no piloto; poder ≈ 45% no cenário ilustrativo (5.000 operações, 3% de inadimplência, **NV**); exige ≥ 300 inadimplentes.
- Recomendação: A principal, B como piloto prospectivo.

### 2.2 Crédito e regulação (`especialista-credito-regulacao`)
- Res. CMN 5.268/2025 adiada pela 5.303/2026: >15 MF em 04/01/2027; 4–15 MF em 01/07/2027; ≤ 4 MF, assentamentos e povos tradicionais em 03/01/2028; só autorizações (UAS) anteriores a 15/03/2026 [F, secundário: [Atlas Público](https://atlaspublico.com.br/noticias/cmn-altera-manual-de-credito-rural-e-fixa-prazos-ate-2028-29929), [Comprerural](https://comprerural.com/prodes-no-credito-rural-nao-acabou-e-nova-regra-do-cmn-apenas-adia-bloqueios-no-agro/)]. A ação da CNA no STF continua [F, secundário].
- Embargo estadual provavelmente **não** é vedação do MCR (a Res. 5.193 fala de lista do Ibama; [LexLegal](https://lexlegal.com.br/?p=16101)) — **NV**. UC possivelmente vedação (item truncado) — **NV**, verificar MCR 2-9.
- PRSAC (Res. CMN 4.945/2021) é proporcional por segmento (S1–S5) [F: [texto](https://www.ancord.org.br/wp-content/uploads/2021/09/Resolução-CMN-n°-4.945-de-15_9_2021.pdf)]: para cooperativas S4/S5 enfraquece "o auditor exige score". Score não é exigido.
- Mata Atlântica (Lei 11.428/2006, art. 14): supressão em estágio médio/avançado para atividade agrossilvipastoril tende a ser ilegal [F, interpretação da SEMAD: [SEMAD](https://sistemas.meioambiente.mg.gov.br/consulta-intervencao/uploads/122022/14115_oafnlEZ7K-SXyhiIKo4o.pdf)] — Y juridicamente limpo onde houver MA.
- Carvão: Código Florestal arts. 34–36 (plano de suprimento, controle de origem, documento de transporte; **NV**, confirmar no [Planalto](https://www.planalto.gov.br/ccivil_03/_Ato2011-2014/2012/Lei/L12651.htm)); auto do IEF multando siderúrgica por comprar carvão de projeto não explorado, com dever de checagem prévia ([IEF](https://conselhos.meioambiente.mg.gov.br/documents/d/ief/siderrgica-mineira-ltda-2-pdf)) — um caso, não norma geral.
- Recomendação: A com Y_reg = supressão sem autorização + embargo estadual secundário; B só como entrevista. Y2/Proagro fora; Y3 como rótulo do piloto; separar vedação obrigatória de risco.

### 2.3 Mercado e frente B (`analista-mercado`, pesquisa nova)
- **Estrutura [F, imprensa]:** 48 usinas de gusa e 63 fornos em MG, ~70% da produção nacional; Sete Lagoas concentra 21 ([Jornal de Brasília](https://jornaldebrasilia.com.br/noticias/economia/mais-de-50-de-usinas-de-ferro-gusa-podem-parar-se-novo-tarifaco-entrar-em-vigor-diz-sindifer/)); ~3,64 Mt de gusa em 2025, ~73% exportado ([Diário do Comércio](https://diariodocomercio.com.br/economia/tarifaco-producao-ferro-gusa/)); ~80% das 125 indústrias consumidoras de carvão do país em MG e 75% da produção estadual de pequenos produtores (2020; [Diário do Comércio](https://diariodocomercio.com.br/economia/cadeia-produtiva-de-carvao-sera-rastreada/)).
- **Origem:** 84,7% do carvão nacional vinha de plantios em 2013 ([Simioni et al., 2017](https://www.alice.cnptia.embrapa.br/alice/bitstream/doc/1072221/1/2017J.MauroCFEvolucao.pdf)); a Lei 20.922/2013 exige carvão 100% de floresta plantada de grandes consumidores desde 2019 ([Agência Minas](https://www.agenciaminas.mg.gov.br/news/pdf/106645.pdf)). **[I]** O evento "supressão" só importa a quem compra de terceiros; o risco real é lavagem de origem (nativo com documento de plantada), documental. A Operação Lastro (Sete Lagoas, Matozinhos, Pedro Leopoldo) mira isso (Agência Minas, PDFs não abertos).
- **Compra de terceiros:** 66,2% do carvão de eucalipto consumido por siderúrgicas independentes em 2010 (indício, não fração de compra de terceiros; [ISA](https://documentacao.socioambiental.org/noticias/anexo_noticia/22175_20120614_104850.pdf)). **Fração atual por usina: NV.**
- **Due diligence hoje:** PrOMOVE/GT Carvão Sustentável (2012; [WWF](https://wwfbrnew.awsassets.panda.org/downloads/p_c_carvaosustentavel_web.pdf); vigência **NV**); rastreio por blockchain Semad/IEF (2020; operação **NV**); Cerflor/FSC existem, adoção entre guseiras independentes **NV**. **Nenhum vendedor de score de carvão achado** (ausência de evidência).
- **Gatilhos:** EUDR com carvão (NCM 4402) segundo fontes secundárias, Anexo I **NV**, aplicação 30/12/2026 (grandes/médios) e 30/06/2027 (micro/pequenos) ([SGS](https://ecustoms.sgs.com/2025/11/27/eudr-officially-postponed-new-deadlines-set-for-2026-and-2027/)); **[NV]** gusa possivelmente fora da EUDR, com CBAM como gatilho indireto ([S&P](https://www.spglobal.com/energy/en/news-research/latest-news/metals/032625-european-pig-iron-buyers-look-to-brazil-for-low-co2-supply-to-mitigate-cbam-cost)).
- **Escopos propostos:** (1) A refinada para a central (alvos Cecremge, Crediminas, Sicoob Central MG, SeloVerde/Semad); (2) B enxuto (Sindifer-MG, SDS Siderúrgica, Vallourec Florestal/Siderurgia Sustentável; Aperam BioEnergia possível). Preços: **NV**. Recomendação: discovery nas duas frentes (3 entrevistas cada), não A+B.
- **Não verificado:** fração de terceiros, carvão nativo em MG (PEVS/SIDRA), nº de carvoarias, preço, disposição a pagar, Anexo I da EUDR.

### 2.4 Dados geo (`engenheiro-dados-geo`; checagens em 2026-10-29)
- **DOF/Ibama não cobre MG** (nota do CKAN: faltam "Mato Grosso, Minas Gerais e Pará, em todo o período"; [CKAN Ibama](https://dadosabertos.ibama.gov.br/api/3/action/package_show?id=dof-transportes-de-produtos-florestais)) → fluxo carvão MG→siderurgia MG não observável em base federal [F]. Sistema estadual: dado aberto **NV** (candidato: LAI ao IEF).
- **IDE-Sisema** (camada de licenciados, `ide_2101_mg_empreendimentos_licenciados_pto`): apenas 33 carvoarias (24 plantada G-03-03-4; 9 nativa G-03-04-2) e 17 siderúrgicas (B-02-01-1), cobertura parcial; CNPJ sem máscara (LGPD).
- **Nenhum snapshot datado do CAR** achado (WRI/source.coop é único, 16/07/2026; Wayback não testado). Camadas `analise_car_veg_2008/2024/2025` da IDE (imóveis analisados, 21,8% na vitrine) dão cobertura declarada, não geometria histórica.
- **Esforço:** A1 (demo) ≈ 14–16 h; B1 (triagem) ≈ 12–14 h; B2 (por fornecedor) > 30 h e depende de LAI/comprador. As 3 checagens pendentes da 01 levam 5–8 h e devem preceder a fixação do Y.
- **Licenças:** MapBiomas e CNUC CC BY; PRODES CC BY-SA; CAR, IDE-Sisema e SIGMINE incertas (pedir declaração ao SFB e à SEMAD).

## 3. Rodada 2 — ataque

### 3.1 Advogado do diabo (resumo por gravidade)
1. **Alta — o modelo prevê "mata nativa + vizinhança de evento", não comportamento.** Teste barato (≈ 2 h): ajustar só distância a evento + área nativa + município; se o AUC-PR ficar a < ~10% do modelo completo, o modelo é redundante.
2. **Alta — vazamento pela geometria do CAR.** `dat_criaca` ≤ t₀ não congela a forma; o polígono pode ter sido retificado para excluir/incluir a clareira; a área nativa atual já reflete a supressão. Teste (≈ 2 h): estabilidade de geometria via `dat_atuali`.
3. **Alta — Y.** PRODES × MapBiomas −0,37 sugere artefato do detector (rebrota de eucalipto, pousio, mineração); `Y_ilegal` depende de base de autorizações de cobertura/publicação/licença não verificadas. Fixar o Y sem as 3 checagens é cedo.
4. **Alta — predição vs. regra determinística do MCR.** Teste: dos imóveis flagados pela regra em t+12, que fração já estava no top 10% em t₀ por histórico?
5. **Alta — B** estruturalmente frágil (evento documental, sem cadeia fornecedor→usina, mercado de ~21–48 compradores).
6. **Média-alta — viés de fiscalização** em embargo/auto (mede onde o Estado olha); **critério numérico mal desenhado** (multiplicidade de limiares × horizontes × Y × baselines; poder insuficiente por ano; baseline "evento passado" forte; calibração sob prevalência variável 178→611); desfecho econômico inexistente publicamente.
7. **Média — A+B "mesmo motor"** esconde unidade, Y e cliente diferentes, e dá falsa opcionalidade a duas frentes sem prova de pagamento; dispersão em ~5 h/semana.
- **Cenário de fracasso:** backtest retrospectivo com lift 3–5 inflado por geometria e vizinhança; regra do MCR adiada ou barrada; cooperativa aceita piloto grátis; dado de inadimplência não chega (LGPD/sigilo); avaliação prospectiva só em 2027–28; incumbentes (Agrotools, Serasa, SeloVerde) incorporam PRODES/UAS por obrigação regulatória.
- **O que faria:** A reformulada (filtro determinístico + antecipação); Y primário único pré-registrado; critério Δ sobre baseline composta em CARs sem evento prévio (limiar de "go" ≈ +5 pp com IC inferior > 0); checagens ≤ 8 h antes da decisão; 3 entrevistas antes de mais código.
- **Explicações alternativas para um sucesso:** autocorrelação espacial/reincidência; artefato de geometria; detector capturando eucalipto/mineração; prevalência crescente inflando o último fold; efeito de tamanho (imóveis grandes com muita nativa).

### 3.2 Comprador cético (persona; opinião, não fato)
- **P1 — central de cooperativas (frente A):** não compra hoje (tem SeloVerde gratuito; a obrigação PRODES chega ao pequeno produtor em 2028; "auditor exige score" não é verdade para S4/S5). Medo: pagar por "IA" o que é um filtro geográfico. Pediria: backtest com baselines simples e lift sobre elas, taxa de falsos positivos, lista priorizada com motivo legível, parágrafo de LGPD/responsabilidade. Orçamento imaginado de piloto "até cerca de R$ 30–50 mil" é opinião da persona (**NV**); contrato recorrente passa por comitê (6–12 meses). **Veredito: piloto grátis; "compro" só se antecipar 2027–28 com o determinístico + priorização e mostrar horas de analista poupadas; "não" se for só o score.**
- **P2 — guseira independente em Sete Lagoas (frente B):** compra de terceiros; risco real é lavagem de origem; quem sabe a lista de fornecedores é a guseira, não o AgroRisk. Quer dossiê (supressão recente, sobreposição com autorização IEF, UC, embargo) sobre 10 dos seus fornecedores, sob controle de quem vê o resultado; teme que um laudo a incrimine; **não compra predição**. Ordem de grandeza de gasto citada (centenas de reais por fornecedor/ano ou dezenas de milhares/ano) é opinião da persona (**NV**). **Veredito: piloto, condicionado.**
- **Menor demonstração para dar reunião e dados:** PDF de 2 páginas (20 CARs de maior risco com mapa e motivo; backtest 2021–24 vs. baselines com IC e falsos positivos; tabela determinístico × predição; parágrafo de LGPD; proposta de piloto de 90 dias, snapshot congelado, avaliação prospectiva).

## 4. Rodada 3 — matriz de decisão
Pesos explícitos (soma 100). Notas 1–5 são julgamento da sessão com base nas rodadas 1–2, não medições. Nota ponderada = Σ(peso × nota) / 100.

| Critério (peso) | A-reformulada | A-original | A+B | B principal |
|---|---|---|---|---|
| Valor para o cliente (20) | 3 | 2 | 3 | 3 |
| Nº de eventos / poder (15) | 3 | 3 | 2 | 1 |
| Dados e licenças (10) | 3 | 3 | 2 | 2 |
| Risco de vazamento (10; nota maior = menor risco) | 2 | 2 | 2 | 2 |
| Diferenciação (15) | 3 | 2 | 3 | 4 |
| Esforço até a demo ≤ ~20 h (15) | 4 | 4 | 2 | 2 |
| Compatibilidade com o desenho do dev (15) | 5 | 5 | 3 | 1 |
| **Nota ponderada** | **3,35** | **3,00** | **2,50** | **2,20** |

Justificativas curtas:
- *Valor*: A-reformulada vende evidência regulatória e antecipação (P1); A-original vende "score" que a persona recusa; B tem dor nítida (P2) mas exige dado do comprador.
- *Poder*: PRODES ≥ 1 ha na vitrine dá 178–611 imóveis/ano; B não tem evento quantificado (1).
- *Dados*: CAR/IDE/SIGMINE com licença incerta em todas; B ainda sem cadeia fornecedor→usina (2).
- *Vazamento*: igual (2) em todas — a geometria do CAR afeta o motor comum; B pior só no rótulo.
- *Diferenciação*: B (4) por não ter vendedor achado; A-reformulada (3) por transparência/backtest contra regra; A-original (2).
- *Esforço*: A ≈ 14–16 h; A+B soma ≈ 12–14 h de B1; B principal exige LAI/dado do comprador.
- *Compatibilidade*: A é o desenho do dev; B muda unidade e cliente.

**Escolha do fundador (2026-10-29):** A-reformulada + discovery de B; critério primário único pré-registrado; Y provisório com gate na sessão 07.

## 5. Perguntas 6–9 do dev
Respostas definitivas em `docs/produto/perguntas-dev-v0.md` e `docs/decisoes/escopo-mvp.md`. Impactos no contrato do motor na seção "Impacto no contrato do motor" do ADR.

## 6. Oportunidades de inovação para o AgroRisk
1. **Backtest contra a regra determinística do MCR** — provar o ganho da predição *além* do filtro PRODES × UAS é a transparência que nenhum player publica (03 §1: nenhum publica AUC/precision@k). Evidência: ataque do advogado do diabo (§3.1 item 4) e persona P1. Esforço: M.
2. **Camada de "vedação com trilha de auditoria"** (fonte, `data_publicacao`, data de corte, hash) como entregável para GRSAC/auditoria — a persona P1 pediu "evidência pronta" e não score. Hipótese de diferenciação **não verificada** contra Agrotools/Serasa. Esforço: M.
3. **Snapshots próprios mensais do CAR e da IDE-Sisema, com hash** — nenhum snapshot datado público encontrado; permite o único teste limpo (prospectivo, 2027–28) e é argumento de credibilidade. Esforço: P (~1 h). Fonte: relatório de dados geo.
4. **Rótulo auditável** `Y_total` / `Y_ilegal (sem autorização identificada)` / `Y_agro`, com estratificação por causa (mineração/urbano ~66% da perda líquida, 01 §1). Esforço: M.
5. **Camada de licenças DN COPAM 217 (carvoarias G-03-03-4 / G-03-04-2 e siderurgia B-02-01-1) geolocalizada** — pouco explorada; só vale se B voltar via discovery. Esforço: P–M. Concorrência na camada: **NV**.
6. **Dossiê de fornecedor (não score)** para guseiras — formato pedido pela persona P2; depende de lista de fornecedores do cliente. Esforço: M. Só após confirmar fração de terceiros.
7. **Prescrição sob orçamento comparada com a regra determinística** (sessão 09) — o wedge de CLAUDE.md §1 passa a ser medido contra o filtro, não contra o acaso.

## 7. Riscos e contra-evidências
- Nenhum comprador pagante verificado; SeloVerde gratuito ocupa o lugar de "evidência de gestão".
- A obrigação PRODES para ≤ 4 MF só em 2028 e pode ser adiada de novo ou derrubada no STF.
- Retrospectivo otimista (geometria do CAR) e rótulo instável (PRODES × MapBiomas).
- Risco ético/LGPD ao rankear pequenos produtores (priorização de revisão, nunca negativa automática).
- Fontes de B majoritariamente de 2008–2017 ou imprensa; vários PDFs da Agência Minas deram HTTP 410.

## 8. Perguntas em aberto
1. Texto primário do MCR 2-9 após a Res. 5.303: UC, embargo estadual, regra transitória de embargos?
2. Autorizações do Sinaflor e da SEMAD são baixáveis em lote, georreferenciadas, e sob que licença?
3. Data real de publicação do PRODES por ciclo (campo `pub_date` é uniforme).
4. Existe snapshot datado do CAR (SFB via LAI, WRI/source.coop versões, Wayback)?
5. Fração dos eventos em ≤ 4 MF, em mineração/urbano e com autorização IEF/FEAM (gate da sessão 07).
6. Nº de eventos no recorte ampliado (Metropolitana + Central Mineira).
7. Que fração do carvão das guseiras de Sete Lagoas vem de terceiros? Quem assinaria?
8. Uma central de cooperativas cederia atraso > 90 dias pseudonimizado? Sob quais cláusulas (LGPD, LC 105/2001, Res. CMN 4.893/2021 — **NV**)?
9. Vigência efetiva do PRSAC para S4/S5 (Res. CMN 5.194/2024 não lida).
10. Status da ação da CNA no STF contra a verificação PRODES.
