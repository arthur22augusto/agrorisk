# 02 — Catálogo de bases públicas (federais e MG) e licenças

Sessão 02 · verificado em **2026-10-28** a partir do ambiente de nuvem da sessão (saída por proxy). Convenção do projeto: "não verificado" = não confirmado, com a fonte candidata ao lado. Licenças em linha por base: [`licencas.md`](licencas.md). Script de teste de acesso: `src/agrorisk/fontes/teste_acesso.py`. Nada foi baixado além de amostras mínimas; nenhum dado foi commitado.

## 1. Resumo executivo

1. **Não existe snapshot histórico público do CAR.** O que há é o estado corrente (espelho GeoParquet do WRI no source.coop, de 16/07/2026). O t₀ do backtest só pode ser aproximado por `dat_criaca`/`dat_atuali` (geometria com `dat_atuali > t₀` é suspeita) ou construído daqui para a frente com **snapshots próprios mensais com hash**. O portal oficial do SICAR entra em loop de redirecionamento a partir daqui.
2. **O estado de MG é aberto e acessível**: o WFS real da IDE-Sisema é `geoserver.meioambiente.mg.gov.br` (1.420 camadas, EPSG:4674, sem autenticação). Mas **não é versionado**: os embargos estaduais (11.470 polígonos) são em maioria de 2026 (~6.760), então um Y estadual não serve para backtest sem pedido por LAI de autos/embargos/DAIA com datas.
3. **Y federais com defasagem curta e dado verificado**: DETER Cerrado (~3 dias observados), MapBiomas Alerta (semanal; API não verificada), embargos IBAMA (com tabela `termo_embargo_historico`), focos INPE (horas). PRODES Cerrado: `pub_date` ~2,5 meses após o ciclo.
4. **Risco de licença é o gargalo comercial, não o acesso**: PRODES/DETER são **CC BY-SA 4.0** (ShareAlike pode alcançar bases derivadas); ICMBio declara CC BY-ND 3.0 no site; CAR, IDE-Sisema, IBAMA ("Outra (Aberta)"), ANM e BHO **sem licença formal** → "incerto". MapBiomas (CC-BY-4.0), CNUC (cc-by), SICOR (ODbL), PSR/ZARC (CC-BY), CHIRPS e Copernicus DEM são os mais limpos.
5. **LGPD**: embargos/autos (IBAMA, ICMBio, Sisema), licenças SLA e PSR trazem nome e CPF/CNPJ. Entram no pipeline só pseudonimizados.
6. **SICOR/MDCR é agregado** (município × produto × mês × programa); **não há** contrato, CPF ou CAR. O único dado aberto com desfecho + ponto no imóvel é o **PSR/SISSER** (indenização e evento por apólice, com coordenada).
7. **Bloqueados/não verificados a partir daqui**: INMET, INCRA (SIGEF/Acervo), `servicos.ibama.gov.br` (403), `www.ibge.gov.br` (403; `geoftp.ibge.gov.br` e SIDRA funcionam), API MapBiomas Alerta, Atlas da Mata Atlântica (só formulário), SNISB, `dados.mg.gov.br` (403), CANIE no CECAV (mas há 14.981 cavidades de MG via WFS da INDE).
8. **Regulação cria o mercado**: o MCR (Res. CMN 5.193/2024) veda crédito a imóvel com embargo IBAMA, CAR cancelado/suspenso, sobreposição com UC/TI, e exige checagem PRODES (supressão após 31/07/2019) desde 02/01/2026 — as mesmas bases são Y e produto (seção 5).

## 2. Mapa base → papel (Y / preditor / outcome / contexto)

| Base | Papel | Defasagem (observada ou estimada) | Histórico para t₀? | Licença (uso comercial) |
|---|---|---|---|---|
| CAR/SICAR (perímetros) | unidade de análise; preditor (status, tamanho) | corrente; sem série | **Não** (só estado atual; reconstrução parcial por datas) | incerto |
| PRODES Cerrado / Mata Atlântica | **Y** (rótulo anual) e preditor (histórico) | Cerrado ~2,5 meses pós-ciclo (`pub_date`); MA não verificada | Sim (série anual; pode ser reprocessada) | incerto (CC BY-SA) |
| DETER Cerrado | **Y** (alerta) / preditor de pressão | ~3 dias | Sim (`created_date`) | incerto (CC BY-SA) |
| MapBiomas Alerta | **Y** (supressão validada, com CAR) | dias–semanas (validação não verificada) | Parcial | sim (CC-BY) |
| MapBiomas cobertura/transição Col. 11 | preditor, contexto | coleção anual (Col. 11 em 18/08/2026), reprocessa a série | **Cuidado**: vazamento por reprocessamento | sim (CC-BY-4.0) |
| MapBiomas Fogo / Água | Y (fogo) / preditor | não verificada | não verificado | não verificado |
| Embargos IBAMA | **Y** e outcome (MCR veda crédito) | a medir com `termo_embargo_historico` | Sim (tabela de histórico) | incerto |
| Autos de infração IBAMA | Y alternativo, preditor | a medir | Parcial | incerto |
| Embargos/autos ICMBio | Y/preditor (UC) | não verificada | não verificado | incerto (CC BY-ND?) |
| CNUC / UCs | preditor (sobreposição), contexto regulatório | 1–2 meses | snapshots semestrais | sim (cc-by) |
| Focos INPE | **Y** (fogo) e preditor | horas | Sim | não verificado |
| CHIRPS v3, Copernicus DEM, BHO, malhas IBGE, PAM/PPM | preditor/contexto | meses–anos | Sim | sim / incerto |
| ANM SIGMINE; barragens ANM/FEAM | preditor (pressão minerária RMBH) | corrente | **Não** (só estado atual) | incerto |
| CANIE (cavidades) | preditor (carste) | não verificada | não | incerto |
| SIGEF/SNCI, INMET | preditor/contexto | — | bloqueado | não verificado |
| IDE-Sisema: embargos estaduais | **Y** potencial | ~sem série | **Não** (maioria 2026) | incerto |
| IDE-Sisema: supressão autorizada IEF (3.869; 2019–2026) | rótulo de legalidade | data de publicação do ato | Sim (campo de data) | incerto |
| IDE-Sisema: outorgas (58.741) e áreas de conflito (110) | preditor (pressão hídrica); Y de conflito | `datpub` (último 2025-07) | Parcial | incerto |
| IDE-Sisema: SLA, UCs, áreas prioritárias, barragens, cavidades | preditor/contexto | variável | Não | incerto |
| SICOR/MDCR (BCB) | **outcome econômico agregado** (exposição), controle | ≥ ~4 meses (06/2026 visto em 10/2026) | Sim (2013–) | sim (ODbL, share-alike) |
| PSR/SISSER (MAPA) | **outcome** (sinistro/indenização por ponto) | anual (~1 ano) | Sim (2006–2025) | sim (CC-BY); LGPD |
| ZARC / Tábua de Risco (MAPA) | preditor/contexto de sinistro | semanal | por safra | sim (CC-BY) |
| Proagro | outcome (só PDFs por UF até 2019) | — | agregado | incerto |

## 3. Conjunto mínimo viável (MVP) e candidatos a Y

**Federal:** CAR (espelho 16/07/2026, com limitação de t₀ documentada) + início imediato de snapshots próprios; PRODES Cerrado/MA + DETER Cerrado; MapBiomas Alerta + Col. 11; embargos IBAMA (corrente + histórico) e ICMBio (pseudonimizados); CNUC, CANIE, SIGMINE; contexto: Copernicus DEM, BHO, CHIRPS v3, focos INPE, IBGE (malhas, PAM/PPM).
**Estadual MG:** embargos (`ide_2304`), supressão IEF (`ide_2105`), outorgas (`ide_2103`) e DAC (`ide_2007`), UCs/áreas prioritárias, barragens/cavidades, licenças SLA; opcional: Análise Dinamizada 2024/2025 e Diagnóstico da Fiscalização 2021–2025.
**Crédito/seguro:** SICOR/MDCR (exposição municipal), PSR/SISSER (sinistro), ZARC.
**Adiar:** SIGEF, INMET, SNISB, Atlas MA, MapBiomas Fogo/Água (licença), Proagro granular.

**Y mais promissores** (decisão final é da sessão 06):

| Y candidato | Fonte | Defasagem | Observação |
|---|---|---|---|
| Supressão validada ligada ao CAR | MapBiomas Alerta | dias a semanas | já traz laudo com CAR; API a verificar |
| Alerta de desmatamento | DETER Cerrado | ~3 dias | alerta, não confirmação |
| Desmatamento confirmado anual | PRODES | ~2,5 meses pós-ciclo (Cerrado) | bom rótulo de treino |
| Embargo ambiental federal | IBAMA | desconhecida; medir | evento raro em MG; é impedimento no MCR |
| Fogo | Focos INPE; MapBiomas Fogo | horas | muitos eventos; fogo ≠ ilegal |
| Supressão **não autorizada** | Alerta/PRODES × IEF `ide_2105` | semanas | Y mais limpo; raridade em RMBH |
| Sinistro/indenização | PSR/SISSER | ~1 ano | Y econômico, não ambiental |
| Y composto | supressão confirmada OU embargo OU fogo em área protegida | ≥ 3 meses (PRODES) | janela 12–24 meses |

**Hipótese a testar:** MG tem poucos eventos de supressão em larga escala; o volume só deve bastar com recorte maior de MG e/ou pequenas áreas (DETER/Alerta).

## 4. Oportunidades de inovação para o AgroRisk

1. **Arquivo próprio de snapshots (CAR e IDE-Sisema).** Ninguém publica histórico do CAR; a IDE-Sisema também não é versionada. Snapshots mensais com data e hash criam, em 12–24 meses, um ativo que o mercado não tem e um t₀ verdadeiro. Evidência: espelho único em 16/07/2026; embargos estaduais majoritariamente de 2026. Esforço: P.
2. **Defasagem real e "data de ciência" no backtest.** Usar `pub_date` (PRODES) e `created_date` (DETER) e a tabela `termo_embargo_historico` (IBAMA, `DT_ALTERACAO`) para impor publicação ≠ ocorrência (regra 3 do CLAUDE.md). Esforço: M.
3. **Relatório de vazamento por reprocessamento** (ex.: Col. 9 vs. Col. 11 do MapBiomas para o mesmo ano; CAR retificado): transparência metodológica que Agrotools/CARMap não oferecem. Hipótese, a medir. Esforço: M.
4. **Y "supressão não autorizada"**: Alerta/PRODES × autorizações IEF (3.869 atos 2019–2026), mais limpo que desmatamento bruto. Esforço: M.
5. **Carste**: CANIE (30.746 cavidades; 14.981 em MG) e cavidades FEAM (14.719 polígonos de 250 m) para Lagoa Santa/Sete Lagoas; insumo pouco usado. Esforço: P.
6. **Pressão hídrica**: outorgas (58.741) + áreas de conflito (110) por ottotrecho — cinturão verde e Sete Lagoas. Esforço: M.
7. **Latência institucional e viés de fiscalização**: DETER → Alerta → embargo; o *Diagnóstico Ambiental da Fiscalização 2021–2025* permite comparar o ranking do AgroRisk com o do órgão e modelar o esforço de fiscalização. Esforço: M.
8. **Pré-checagem de impedimento do MCR** como produto: P(imóvel virar impedimento em 12–24 meses) (embargo, CAR, UC/TI, PRODES pós-31/07/2019); outcome = operação negada/desclassificada. Janela regulatória de exceção até 30/06/2027. Esforço: G.
9. **Outcome econômico público**: SICOR (exposição municipal) e PSR (sinistro com ponto) + ZARC. Limite: sem inadimplência; só carteira privada de cooperativa tem contrato/CAR/inadimplência. Esforço: M.

## 5. Crédito rural, seguro e regulação (SICOR, Proagro, PSR, ZARC, MCR, LGPD)

Fonte: agente `especialista-credito-regulacao`. Itens do MCR 10–19 vieram de resumo de terceiros; confirmar no texto oficial (<https://www3.bcb.gov.br/mcr>).

### 5.1 Fichas

**SICOR / Matriz de Dados do Crédito Rural (BCB/Derop)** — <https://dadosabertos.bcb.gov.br/dataset/matrizdadoscreditorural>; OData `https://olinda.bcb.gov.br/olinda/servico/SICOR/versao/v2/odata/` (`$metadata` documenta 17 recursos).
- Cobertura: Brasil, 2013–atual, atualização mensal. Defasagem formal não verificada; em 2026-10-28 havia registro de 06/2026 (≥ ~4 meses).
- **Granularidade agregada**: município × produto × mês × programa/subprograma × fonte de recursos × modalidade. Campos como `codIbge`, `nomeProduto`, `AnoEmissao`, `MesEmissao`, `cdPrograma`, `VlCusteio`, `AreaCusteio`. **Sem contrato individual, CPF/CNPJ do tomador ou CAR** (inferido do `$metadata`; o CNPJ presente é da instituição financeira).
- Chave: `codIbge` (7 dígitos; MG = prefixo 31) + ano/mês + produto; Pronaf isolável por programa/subprograma. `cdEstado` é código próprio, não IBGE.
- Teste: consulta simples (`CusteioMunicipioProduto?$top=2`) OK; `$filter cdEstado eq 'MG'` em recurso sem filtro **deu timeout (60 s)** → usar filtros por ano/mês e paginação.
- Licença: "Open Data Commons Open Database License (ODbL)" (página do dataset); texto da ODbL não conferido (<https://opendatacommons.org/licenses/odbl/1-0/>). Uso comercial **sim**, com atribuição e *share-alike* para bases derivadas (validar o alcance).
- Microdados por contrato (CPF/CAR): não encontrados abertos; acesso por LAI/convênio não verificado (candidata: Fala.BR / Derop).

**Proagro (BCB)** — sem dataset aberto granular. Só relatórios circunstanciados em PDF por UF × ano agrícola (2004–2011, 2015–2018, 2016–2019); posteriores a 2019 não localizados. Sinistralidade municipal: não verificado (candidatas: Anuário Estatístico do Crédito Rural, LAI ao Derop). Licença não verificada. Fontes: <https://www.bcb.gov.br/content/estabilidadefinanceira/proagro_docs/relatorios_proagro/Relatorio-circunstanciado-2015_2018.pdf>, <https://www.bcb.gov.br/content/estabilidadefinanceira/proagro_docs/relatorios_proagro/Relatorio_circunstanciado%202016_2019.pdf>.

**PSR / SISSER (MAPA)** — <https://dados.agricultura.gov.br/dataset/sisser3> (CSV/XLSX: 2006–2015, 2016–2024, 2025; recursos sobrepostos → deduplicar por `ID_PROPOSTA`). Periodicidade anual; último = 2025 (defasagem ~1 ano).
- **Por apólice com ponto**: `LATITUDE/LONGITUDE`, `NM_MUNICIPIO_PROPRIEDADE`, `CD_GEOCMU`, cultura, área, limite de garantia, prêmio, subvenção federal, `VALOR_INDENIZACAO`, `EVENTO_PREPONDERANTE`, e também `NM_SEGURADO` + `NR_DOCUMENTO_SEGURADO` (CPF/CNPJ). Dicionário: <https://dados.agricultura.gov.br/dataset/baefdc68-9bad-4204-83e8-f2888b79ab48/resource/2c5c55d0-1473-4749-b08f-cfaf887a9fa3/download/dicionariodedados-sisser.pdf>.
- Chave: coordenada (interseção com CAR) e CPF/CNPJ; **sem campo CAR**. Precisão das coordenadas e cobertura em MG: não medidas. CSVs não baixados.
- Licença: "Creative Commons Attribution" (versão não informada). Uso comercial sim pela licença; LGPD incerta.

**ZARC / Tábua de Risco (MAPA/SPA)** — <https://dados.agricultura.gov.br/dataset/tabua-de-risco-zoneamento-agricola-de-risco-climatico>; CSV por safra 2016/17–2026/27; atualização semanal (última 2026-10-27); sem API encontrada. Granularidade: não verificada (dicionário em PDF não aberto). Licença "Creative Commons Attribution"; sem dado pessoal. O ZARC é exigido para Proagro/subvenção conforme notas técnicas do MAPA e Decreto 5.121/2004 (via notas técnicas; referência MCR possivelmente desatualizada).

### 5.2 Regras do MCR que tornam as bases relevantes (Res. CMN 5.193/2024, vigência geral 02/01/2025)

Fontes: <https://www.normasbrasil.com.br/norma/resolucao-5193-2024_470860.html>; <https://www.irib.org.br/resolucao-cmn-n-5-081-de-29-de-junho-de-2023/>. Itens 10–19 via resumo de terceiros.
- **CAR**: vedado imóvel não inscrito ou com inscrição cancelada/suspensa (exceções MCR 2-1-12 a 15).
- **UC**: vedado em imóvel total/parcialmente em UC do CNUC, salvo plano de manejo; **TI**: vedado em terra indígena (base Funai).
- **Embargos IBAMA**: vedado imóvel com embargo por uso econômico de área desmatada ilegalmente; exceção para investimento exclusivo de recuperação; exceção transitória até **30/06/2027** (multas pagas, projeto, cercamento, CAR ativo, área embargada ≤ 5% ou 20 ha).
- **Desmatamento**: desde **02/01/2026** a IF deve checar PRODES (supressão após 31/07/2019); havendo, exige ASV/UAS, PRAD/PRA, TAC com MP ou laudo de sensoriamento.
- Não verificados: tratamento de Mata Atlântica por bioma e Pronaf; Res. CMN 4.336/2014 (custeio no ZARC até R$ 300 mil em Proagro ou seguro; norma marcada como revogada, versão vigente não confirmada). Certidão de embargo do IBAMA, usada por bancos: <https://www.gov.br/pt-br/servicos/obter-certidao-de-embargo-ambiental>.
- Obrigação legal (embargo, CAR, UC, TI valem para todo crédito rural) vs. política própria PRSAC/PRSA: política não verificada.

### 5.3 LGPD e licença federal

- Decreto 8.777/2016, art. 2º III (dados abertos sob licença aberta exigindo apenas creditar autoria/fonte) — o Planalto bloqueou o acesso aqui; via resumos. "CC-BY 4.0 como padrão federal" **não foi confirmado**: cada órgão escolhe. Termos do dados.gov.br: HTTP 401, não verificados.
- Lei 13.709/2018 (<https://www2.camara.leg.br/legin/fed/lei/2018/lei-13709-14-agosto-2018-787077-publicacaooriginal-156212-pl.html>): art. 6º I e III (finalidade, necessidade), art. 7º §§3º–4º (dado público: finalidade, boa-fé, interesse público; a dispensa de consentimento para dado "manifestamente público" é frágil para embargos/apólices, que não foram tornados públicos pelo titular), art. 26. Base aberta ≠ livre de LGPD. Hipótese de proteção ao crédito (art. 7º X) é candidata para bancos, **não verificada**; exige revisão jurídica. Boas práticas: pseudonimizar, agregar por imóvel/município, não republicar CPF. Parecer da ANPD sobre CPF em embargos: não encontrado.

## 6. Riscos e contra-evidências

- **ShareAlike (INPE)**: se o produto redistribuir camadas derivadas, a base derivada pode ter de usar a mesma licença; usar PRODES/DETER como insumo interno e entregar só o score reduz o risco. **Exige parecer jurídico.** Idem ODbL (SICOR).
- **ND (ICMBio)**: "Atribuição-SemDerivações" é do site; se valer para o dado, proíbe adaptação.
- **CAR sem licença declarada** (README do espelho: o SICAR "publishes no licence and no terms of use"; não confirmado no portal). Mitigar com consulta formal ao SFB (LAI).
- **IDE-Sisema**: `Fees NONE`/`AccessConstraints NONE` e "o acesso ao dado é livre" não equivalem a licença de reuso comercial. Pedir declaração escrita à Dgeo/SEMAD (contato no Capabilities: (31) 3915-1760). Até lá: uso comercial incerto, risco baixo a médio.
- **Vazamento temporal**: CAR (geometria e status atuais, retificações); MapBiomas (série reprocessada a cada coleção); PRODES (pode ser reprocessado); SIGMINE e IDE-Sisema (só estado corrente); `DAT_EMBARGO` não é data de publicação; camadas sem data de publicação (Análise Dinamizada, APP, ZEE) só com corte posterior ao snapshot.
- **Viés de observação**: autuação depende do esforço de fiscalização; camada de licenças só tem deferidos (viés de sobrevivência).
- **Raridade do evento** em MG/RMBH; poder estatístico a verificar na sessão 06.
- **Disponibilidade**: portais caem ou bloqueiam (CAR, INMET, MapBiomas API, INCRA, dados.mg.gov.br). Planejar cache local e scripts idempotentes com data e hash.
- **Qualidade**: erros de digitação (data 2925 em embargo; coordenadas absurdas no CAR); exigir validações no pipeline.
- **Mudança regulatória** frequente do MCR (janela 30/06/2027; PRODES desde 02/01/2026).

## 7. Perguntas em aberto e sugestões para a sessão 06

1. O SFB aceita LAI de snapshots históricos de `AREA_IMOVEL`? O SICAR tem termo formal de uso comercial? Semântica de `dat_criaca`/`dat_atuali`?
2. Defasagem real entre ato e arquivo nos embargos IBAMA (medir com `termo_embargo_historico`)? E por que os embargos estaduais se concentram em 2026 (migração de sistema)? Pedir série completa via LAI à SEMAD/IEF.
3. API do MapBiomas Alerta acessível fora do túnel? Prazo de validação? Campo com o código CAR?
4. O CC BY-SA do INPE e o *share-alike* da ODbL alcançam um score/modelo derivado? Parecer jurídico.
5. Licença da INDE para dados do ICMBio é a do site (CC BY-ND 3.0)?
6. Fogo/Água do MapBiomas, Atlas MA, TOPODATA, focos INPE: licença a confirmar (fontes candidatas nas fichas).
7. Alternativa ao INMET (Base dos Dados, ERA5-Land, NASA POWER) e ao SIGEF (login gov.br pelo fundador)?
8. SICOR: defasagem real e comportamento de `$filter` (testar com `curl`); Proagro por município/contrato (LAI); precisão de coordenadas e cobertura MG do PSR; dicionário da Tábua de Risco; texto oficial do MCR 2-9 e cap. 16.
9. Carteira privada de cooperativa em MG é o único dado com contrato/CAR/inadimplência: vale priorizar parceria, usando os agregados públicos como controle.
10. **Sugestão para a sessão 06:** candidatos a Y com melhor equilíbrio entre defasagem curta, histórico reconstruível e licença: (a) supressão confirmada (PRODES/Alerta) e (b) embargo IBAMA com histórico; tratar Y estadual como complementar até haver série via LAI.

---

# Anexo A — Bases federais (relatório do agente `engenheiro-dados-geo`)

### 1. Tabela-catálogo resumida

| # | Base (órgão / produto / versão) | Acesso verificado | Cobertura | Defasagem de publicação (observada ou estimada) | Chave de ligação | Papel | Licença (resumo) | Uso comercial | Acesso (nuvem) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **SICAR/CAR** perímetros "Área do Imóvel" (SFB). Espelho GeoParquet WRI/source.coop (16/07/2026) | `data.source.coop/tristangruppwri/cadastral/brazil-car-area-imovel/` (3,26 GB, nacional, 8.453.552 polígonos) | Só estado corrente. Datas por imóvel (`dat_criaca`, `dat_atuali`) | O CAR muda continuamente (retificação). Espelho com ~2 semanas de atraso | `cod_imovel` (UF-IBGE7-hash) | O (carteira); P (atributos do imóvel) | SICAR não publica licença (segundo o README do espelho; portal oficial inacessível, ver 4) | Incerto | Espelho OK; portal oficial: loop de redirecionamento e WFS sem camadas |
| 2 | **SFB Bases de Referência CAR** (uso do solo, hidrografia, relevo, servidão) 2015–2024 | CKAN `dados.florestal.gov.br` + ArcGIS `mapas.florestal.gov.br` | 2015–2024, por UF | Metadados de mai/2025 | por UF; sem geometria de imóvel | C | CC-BY | Sim (com atribuição) | CKAN OK (200) |
| 3 | **PRODES Cerrado** (INPE, BiomasBR) | WFS TerraBrasilis `prodes-cerrado-nb:yearly_deforestation` | 2000–2026; 342.326 polígonos em MG | Campo `pub_date` = 20261016 para o ciclo 2026 (imagens até 12/08/2026) → ~2,5 meses após o fim do ciclo | Geometria (sem CAR) | Y (supressão) | CC BY-SA 4.0 | Incerto (BY-SA/ShareAlike) | OK (200) |
| 4 | **PRODES Mata Atlântica** (INPE) | WFS `prodes-mata-atlantica-nb:yearly_deforestation` | 2004–2025; 1,11 M polígonos no bioma | Sem `pub_date`. Defasagem não verificada | Geometria. Atributo `state` usa sigla (filtro `'MINAS GERAIS'` devolveu 0) | Y | CC BY-SA 4.0 | Incerto | OK |
| 5 | **DETER Cerrado** (INPE) | WFS `deter-cerrado-nb:deter_cerrado` | 135.184 avisos no total; há avisos de out/2026 em MG | Observado: `view_date` 12/10/2026 → `created_date` 15/10/2026 (3 dias) | Geometria; `uf`, `municipality` | Y (alerta) | CC BY-SA 4.0 | Incerto | OK |
| 6 | **MapBiomas Coleção 11** cobertura/uso (+ transições, desmat./veg. secundária, pastagem, agricultura) | COG em `gs://mapbiomas-public` (HTTPS). Cada ano nacional ≈ 0,67 GB | 1985–2025, 30 m | Arquivos de 18/08/2026 → ano t publicado ~8 meses após o fim de t. **Coleção reprocessa a série inteira** | Pixel/geometria | P; Y (via transição floresta→não floresta) | CC-BY-4.0 (STAC) | Sim | OK |
| 7 | **MapBiomas Alerta** | `plataforma.alerta.mapbiomas.org`. API GraphQL não verificada (api.alerta: 502) | 2019→ | Publicação semanal (terças), segundo o site | Laudo cruza com CAR (código CAR) | **Y principal** (supressão validada, com CAR) | CC-BY (texto do site) | Sim (com atribuição) | Plataforma OK; API inacessível |
| 8 | **MapBiomas Fogo** Coleção 5 (cicatrizes anuais e mensais) | `gs://mapbiomas-public/.../fire-col5/` (vetores anuais, mensal, frequência, tempo desde fogo) | 1985–2024 (inferido do bucket col.10; não verificado) | Anual, ~7–8 meses; mensal não verificado | Pixel | Y (fogo); P (histórico de fogo) | CC-BY presumido (não verificado para o Fogo) | Presumido sim | Bucket OK |
| 9 | **MapBiomas Água** | Prefixo `mapbiomas/brazil/water/` existe no bucket. Site `agua.mapbiomas.org`: 502 | não verificado | não verificado | Pixel | P/C | não verificado | não verificado | Parcial |
| 10 | **Atlas da Mata Atlântica** (SOS MA/INPE) | Download via formulário no site (dados 2024 por estado e do bioma). Não automatizável | Ciclos out→set. Edição 2024-2025 de mai/2026 | ~8 meses após o fim do ciclo (set → mai) | Município, UF, polígono | Y/C (só Mata Atlântica, mínimo 3 ha. **não verificado**) | não verificado | Incerto | Site OK; geoservidor inacessível |
| 11 | **Embargos IBAMA** (termo de embargo, SIFISC) | CKAN `dadosabertos.ibama.gov.br` → blob Azure (CSV 211 MB; histórico 732 MB). Geometria WKT | Desde ~2009 (registro histórico mais antigo visto: 2009) | Atualização diária (`Last-Modified` 28/10/2026). Defasagem entre o ato e a publicação: não verificado | `NUM_PROCESSO`, geometria WKT, CPF/CNPJ, `NOME_IMOVEL`. Sem código CAR visível | **Y/O** | `other-open` ("Outra (Aberta)") | Incerto (licença não textual) | CSV OK. Portal `servicos.ibama` 403 |
| 12 | **Autos de infração IBAMA** (+ enquadramento, coordenadas, bioma) | blob `.../SIFISC/auto_infracao/` (zip 123 MB) | desde ~2000? (não verificado) | Diária | Coordenadas, CPF/CNPJ | Y/O | `other-open` | Incerto | OK (HEAD) |
| 13 | **Embargos e autos ICMBio** | WFS INDE `ICMBio:embargos_icmbio` (14.806; 855 em MG) e `autos_infracao_icmbio` (JSON falha; ver 4) | 2009→ | não verificado | CPF/CNPJ, `cnuc`, geometria | Y (em UC) | Conteúdo do site gov.br: CC BY-ND 3.0 (não é licença específica do dado) | Incerto | WFS OK |
| 14 | **CNUC / UCs** (MMA) | CKAN `dados.mma.gov.br` (CSV semestral + shapefile) e WFS INDE `MMA:cnuc_*` | Snapshots 2018→07/2026 | 2026_07 criado em 21/08/2026 | `cnuc` | C/P (sobreposição) | CC-BY (CKAN) | Sim (atribuição) | OK |
| 15 | **UCs federais (limites ICMBio)** | WFS INDE `ICMBio:limiteucsfederais_a` (347) | 2026 | Mapa oficial ago/2026 | `cnuc` | C | CC BY-ND 3.0 do site | Incerto | OK |
| 16 | **SIGEF / SNCI** (INCRA) | `acervofundiario.incra.gov.br`, `certificacao.incra.gov.br`: **502 CONNECT**. Exige login gov.br prata/ouro (blog, não verificado) | desde 2004 (fonte secundária) | não verificado | Código da parcela; cruza com CAR por geometria | C/P (titularidade), O | não verificado | não verificado | **Bloqueado** |
| 17 | **Focos de queimada INPE** | `dataserver-coids.inpe.br/queimadas/queimadas/focos/csv/` (10min, diário, mensal, anual) | desde 1998 (BDQueimadas, fonte secundária) | **Horas** (arquivo diário gerado às 09:05 e 19:06) | lat/lon, município (IBGE) | Y (fogo); P | não verificado | não verificado | OK |
| 18 | **INMET** (estações, BDMEP) | `apitempo`, `portal`, `bdmep`: resposta vazia/000 | não verificado | não verificado | estação | P (clima) | não verificado | não verificado | **Bloqueado** |
| 19 | **CHIRPS v3** | `data.chc.ucsb.edu/products/CHIRPS/v3.0/` (a v2.0 mudou de caminho, 404) | 1981→ | Preliminar: 2 dias após o pentad. Final: ~3ª semana do mês seguinte | Grade 0,05° | P | CC BY 4.0 + "public domain" | Sim | OK |
| 20 | **Copernicus DEM GLO-30** | `copernicus-dem-30m.s3.eu-central-1.amazonaws.com` (COG por tile) | estática (TanDEM-X) | n/a | Grade 30 m | P | Licença Copernicus WorldDEM-30 | Sim (ver 3) | OK |
| 21 | **TOPODATA** (INPE) | `http://www.dsr.inpe.br/topodata/` (https falha) | estática | n/a | Grade 30 m | P | CC-BY-4.0 (catálogo FedEO, terceiro) | Incerto | OK (http) |
| 22 | **SRTM** | `srtm.csi.cgiar.org` (200). Preferir Copernicus ou TOPODATA | estática | n/a | Grade | P | não verificado | não verificado | Site OK |
| 23 | **BHO / ottobacias** (ANA) | `metadados.snirh.gov.br/files/<uuid>/geoft_bho_*.gpkg` (trecho de drenagem 4,06 GB, v6.2.4) | estática (v6.2.4, 2022) | n/a | Código da ottobacia | P/C | "O acesso ao dado é livre." | Incerto | HEAD 200 |
| 24 | **IBGE malhas** (geoftp) | `geoftp.ibge.gov.br/.../municipio_2000…2025/` | 2000–2025 | Malha 2025 já listada | Código IBGE-7 | C (chave) | "Todos os arquivos aqui disponíveis são públicos." | Provável sim (ver 3) | OK (www 403) |
| 25 | **IBGE SIDRA** (PAM, PPM, PEVS) | `apisidra.ibge.gov.br/values/t/...` | PAM/PPM com 2025 já publicado em out/2026 | PAM/PPM: ~9–10 meses (ano t em set–out de t+1; data exata não verificada). PEVS 2025: "..." | Código IBGE-7 | P/C | idem IBGE | Provável sim | API OK (`sidra.ibge.gov.br` 403) |
| 26 | **Censo Agropecuário 2017** | `ftp.ibge.gov.br/Censo_Agropecuario/Censo_Agropecuario_2017/` e SIDRA t. 6881 | 2017 (única edição recente; novo censo ainda sem resultado) | Resultados definitivos ~2019 (não verificado) | Município; estabelecimento anonimizado | C/P (estrutura fundiária) | idem IBGE | Provável sim | OK |
| 27 | **ANM SIGMINE** | ArcGIS REST `geo.anm.gov.br/arcgis/rest/services/SIGMINE/dados_anm/FeatureServer/0` (51.246 processos ativos em MG) | **Só estado corrente** (campo `ULT_EVENTO`) | Diária ("Dados gerados diariamente") | `PROCESSO`; geometria | P/C (pressão de mineração) | gov.br não declara licença | Incerto | OK |
| 28 | **ANM barragens (SIGBM)** | dataset dados.gov.br `barragens-de-mineracao` (arquivo único) | não verificado | "Tempo real" (declarado) | Nome/coord. | C/P | não declarada | Incerto | Página OK. Arquivo não testado |
| 29 | **SNISB (ANA)** barragens | `snisb.gov.br` (WordPress). CSV com 36 atributos (fonte secundária). Endpoints `portal-snisb/api` retornam 404 | 29.761 estruturas em 2025 (fonte secundária) | Relatório anual (RSB) | Nome/coord. | C | não verificado | não verificado | Site OK. Download não localizado |
| 30 | **CECAV/CANIE** cavidades | WFS INDE `ICMBio:canie_052026_p` (30.746 cavidades; **14.981 em MG**), lat/lon públicos e nível de validação | Edição 05/2026 | Mensal/semestral: não verificado | `num_canie`, ponto | C/P (carste) | CC BY-ND 3.0 do site | Incerto | WFS OK |
| 31 | **Base dos Dados** (espelho) | Site 200. BigQuery exige credencial (não disponível) | — | — | — | espelho | Código MIT (README). Dados herdam a fonte | — | Parcial |

---

#### 2. Fichas por base

#### 2.1 SICAR / CAR (perímetros) — centro do problema de t0
- **Órgão / produto:** Serviço Florestal Brasileiro (SFB), SICAR, módulo de consulta pública.
- **Acesso:**
  - Portal oficial: `https://consultapublica.car.gov.br/publico/estados/downloads`. O README do espelho diz que o download de AREA_IMOVEL é protegido por captcha.
  - Na nuvem, o portal entrou em **loop de redirecionamento http↔https** (curl: 50 redirecionamentos, 301/302), e o WebFetch recebeu 503.
  - O `geoserver.car.gov.br` responde ao `GetCapabilities`, mas **sem nenhum `FeatureType` publicado**. Um GetFeature em `sicar:car_imovel_mg` devolveu "Feature type unknown", e o REST exige autenticação (401).
  - **Espelho utilizável:** GeoParquet 1.1 único, EPSG:4326, ZSTD, 212 row groups, coluna `bbox`, 3.258.574.258 bytes. URL: `https://data.source.coop/tristangruppwri/cadastral/brazil-car-area-imovel/brazil_car_area_imovel.parquet`. HEAD devolveu 200 com `accept-ranges: bytes`, então DuckDB consegue ler só o recorte de MG via httpfs.
  - Biblioteca de terceiros `SICAR` (Python) lê as datas de release por estado. Na amostra de ago/2024 o release de MG era de 04/08/2024.
- **Cobertura temporal:** só **um instante** (espelho de 16/07/2026; README do espelho). Não encontrei snapshots históricos de CAR em Zenodo, MapBiomas, LAPIG ou Imaflora. A busca devolveu apenas estatísticas derivadas. **Não verificado.** Candidatos: pedir ao SFB via LAI e perguntar ao Imaflora/LAPIG.
- **Defasagem:** o CAR é um registro vivo. Cada retificação gera um novo recibo (GeoOne, FAQ Semace). A "Retificação Dinamizada" do SFB permite editar o limite, recortar sobreposições e remover geometria (manual SFB/IAT-PR).
- **Granularidade:** polígono do imóvel, ~8,45 M no Brasil. Atributos: `cod_imovel`, `cod_estado`, `municipio`, `des_condic` (16 valores), `ind_tipo` (IRU/AST/PCT), `mod_fiscal`, `num_area`, `dat_criaca`, `dat_atuali`.
- **Chave de ligação:** `cod_imovel`, no formato UF-IBGE(7)-hash32 (por exemplo `SE-2802908-…`), o que já embute o município. **Não é único** no espelho: 8.453.552 linhas para 8.437.938 códigos distintos, 15.614 repetidas. O dono (CPF/CNPJ) não é público.
- **Qualidade:**
  - O CAR é autodeclarado e a maioria não foi validada, com sobreposições geométricas (Rev. Bras. Cartografia, UFU).
  - 6,15 M de linhas estão "Aguardando análise" e apenas ~0,63 M "Analisado, em conformidade" (contagens do README do espelho).
  - Duas geometrias corrompidas estão em quarentena no espelho.
  - Houve mudança de versão do módulo em set/2024: "Sede do imóvel" passou a ser feição obrigatória, segundo a SEMA-RS.
- **Licença:** ver seção 3. O README do espelho diz literalmente: "**SICAR publishes no licence and no terms of use.**" e "The Creative Commons entries on `dados.florestal.gov.br` cover other CAR layers, not this one." Isso não foi confirmado no portal oficial (inacessível). Base legal: Lei 12.651/2012 art. 29 (CAR como "registro público eletrônico de âmbito nacional", citado no README). Dados de identificação do titular não são públicos, segundo guia do IMA-SC que cita a IN conjunta (a norma exata precisa de confirmação).
- **Papel:** unidade de análise (carteira), **O**. Os atributos `des_condic` e `mod_fiscal` são preditores potenciais.

**Como reconstruir o estado em t0 (recomendação):**
1. **Existência:** manter só imóveis com `dat_criaca ≤ t0`. Isso é razoável, desde que `dat_criaca` seja de fato a data da primeira inscrição (campo "como string"; semântica não verificada).
2. **Geometria:** a geometria disponível é a de 16/07/2026. Ela só é "t0-segura" se `dat_atuali ≤ t0` (nunca retificado depois). Imóveis com `dat_atuali > t0` têm geometria possivelmente futura. Duas opções: excluí-los (viés de seleção: os retificados tendem a ser os mais regulares) ou usá-los com flag de "geometria potencialmente pós-t0".
3. **Status (`des_condic`):** é estado de 2026. "Cancelado por duplicidade" e a análise posterior são informação futura. **Não usar como preditor** em backtest antes de t0.
4. **Para o futuro:** criar snapshots mensais próprios (script que baixa, calcula hash e data de extração, gravando em `data/raw/car/AAAA-MM-DD/`) e registrar `release date` por estado. O backtest sobre eventos posteriores ao primeiro snapshot passa a ter t0 verdadeiro.
5. **Pedido formal:** solicitar via LAI ao SFB bases históricas de AREA_IMOVEL (por exemplo dezembro de 2018, 2020, 2022). O resultado é incerto.
6. **Alternativa independente:** o SIGEF/SNCI (INCRA) traz parcelas certificadas, imutáveis e com data de certificação. Hoje está inacessível daqui (seção 4). O **espelho source.coop** mostra que o WRI já mantém o recorte; vale perguntar se mantêm versões anteriores.
7. **Alternativa de comparação:** `A SFB Base de Referência` (2015–2024) dá camadas anuais de uso do solo, hidrografia e relevo por UF, usadas na análise de regularização. Não substitui o perímetro do imóvel.

#### 2.2 PRODES Cerrado e Mata Atlântica (INPE, BiomasBR/TerraBrasilis)
- **Acesso:** WFS `https://terrabrasilis.dpi.inpe.br/geoserver/ows` (GetCapabilities 200). Camadas: `prodes-cerrado-nb:yearly_deforestation`, `prodes-mata-atlantica-nb:yearly_deforestation`, `accumulated_deforestation_2000`, `residual`, `no_forest`. Página de downloads em `terrabrasilis.dpi.inpe.br/downloads/`. A página registra "Em 16 de outubro de 2026, o Programa BiomasBR atualizou seus dados anuais" (resumo da página). Também há um aviso genérico de arquivo "sendo reprocessado". Isso ressalta que **a série pode ser reescrita**.
- **Cobertura:**
  - Cerrado: 2000–2026. Atributos: `year`, `state` ("MINAS GERAIS"), `image_date`, `satellite`, `pub_date`, `area_km`. Em MG há **342.326** polígonos.
  - Mata Atlântica: 2004–2025. `state` em sigla (BA, PR…), `image_date`, satélite (Sentinel-2 nos ciclos recentes), sem `pub_date`.
- **Defasagem:** no Cerrado, o ciclo 2026 tem imagens até 12/08/2026 e `pub_date` = 16/10/2026. Para backtest, use `pub_date` quando existir. Para Mata Atlântica, assumir pior caso (final do ano seguinte) até haver evidência.
- **Granularidade:** polígono. Área mínima mapeada: **não verificado** (fonte candidata: metodologia no site BiomasBR).
- **Chave:** apenas geometria (sobrepor ao CAR). Não traz CAR.
- **Qualidade:** PRODES é censo anual por ciclo (ago–jul). O desmatamento é "corte raso" mapeado por imagens, sem avaliar legalidade. Reprocessamentos possíveis.
- **Licença:** CC BY-SA 4.0 (ver seção 3).
- **Papel:** Y (supressão de vegetação nativa), com `year` como data do evento e `pub_date` como data de ciência.

#### 2.3 DETER Cerrado (INPE)
- **Acesso:** WFS `deter-cerrado-nb:deter_cerrado`. Campos: `classname` (`DESMATAMENTO_CR`…), `view_date`, `created_date`, `sensor`, `satellite` (CBERS-4, AMAZONIA-1…), `areatotalkm`, `uc`, `municipality`, `uf`, `publish_month`. `gid` com sufixo `_hist`/`_curr`.
- **Defasagem:** observada de **3 dias** (12/10/2026 → 15/10/2026). Os avisos do mês corrente podem ser revisados (sufixo `_curr`).
- **Qualidade:** é alerta, não censo. Resolução mais grossa que o PRODES (WFI/AWFI). O DETER Cerrado não é apresentado na página de downloads como arquivo; usar o WFS. Contagem em MG não obtida (a consulta CQL falhou por reset de conexão). **Não verificado.**
- **Papel:** Y de alta frequência; também insumo de fiscalização (os embargos IBAMA têm o campo `DETER_PRODES`).

#### 2.4 MapBiomas (cobertura, transições, Alerta, Fogo, Água)
- **Cobertura/uso:** Coleção 11, 1985–2025, 30 m, 41 COGs anuais em EPSG:4326 (STAC `collection.json`, `license: CC-BY-4.0`). O bucket `gs://mapbiomas-public` (HTTPS público) lista `initiatives/brasil/collection11/lulc/{coverage,transition}/`; há também coleções 10, 9, 8, 71. Cada arquivo anual nacional ≈ 0,67 GB (usar leitura em janelas de COG). Asset no GEE: `projects/mapbiomas-public/assets/brazil/lulc/collection11/mapbiomas_brazil_collection11_coverage_v3`.
- **Defasagem:** arquivos da Col. 11 com data de 18/08/2026 (mapa de 2025). Col. 10: pasta de 05/08/2025. **Cada coleção reprocessa toda a série**: o mapa de 2018 da Col. 11 usa informação posterior a 2018 (filtros temporais). Para backtest, não é possível reconstruir "o que se sabia em t0". Mitigação: usar a coleção antiga publicada antes de t0 (Col. 7.1, 8, 9 existem no bucket) ou tratar como contexto.
- **Alerta:** dados "públicos, abertos e gratuitos sob Creative Commons CC-BY com a devida atribuição" (site). Cada alerta validado tem laudo com cruzamento com CAR, áreas protegidas e assentamentos, e há busca por código CAR. Publicação semanal, geralmente às terças. O MapBiomas Alerta "publica todas as perdas de vegetação nativa, sem avaliar legalidade". Mínimo de 0,3 ha, segundo FAQ do SOS MA. **API GraphQL: não verificado.** `api.alerta.mapbiomas.org` devolveu 502 no túnel; a plataforma web respondeu 200. Documentação em `plataforma.alerta.mapbiomas.org/api/docs` (200, conteúdo não analisado).
- **Fogo:** Coleção 5 (bucket `collection_10/fire-col5/`): cicatriz anual, mensal (`monthly_burned_v1`), frequência, tempo desde o fogo, severidade, vetores anuais. Licença: não verificado.
- **Água:** pasta `mapbiomas/brazil/water/` existe; não explorada.
- **Papel:** Alerta = **Y principal** (já amarrado ao CAR). Cobertura/transição = P (histórico de uso) e C. Fogo = P/Y.

#### 2.5 Atlas da Mata Atlântica (SOS MA / INPE)
- **Acesso:** página do Atlas oferece "Dados de 2024 por estado" e "Dados de 2024 de toda a Mata Atlântica" mediante formulário ("Faça o download grátis… preencher o formulário"). Geoservidor `mapas.sosma.org.br` e `atlasmata.sosma.org.br` não respondem. Relatório 2024-2025 hospedado no INPE (mai/2026), mas retornou 503 no teste.
- **Período:** ciclos de 12 meses, **outubro a setembro** (FAQ do SOS MA). O MapBiomas usa o ano civil.
- **Valor:** o Atlas 2024-2025 apontaria MG como líder em desmatamento (3.092 ha) segundo resumo de busca. **Número não confirmado no PDF** (503). Tratar como pista. Para 2023-2024, o relatório reporta MG com 2.737 ha (5º lugar) (fonte: resumo de busca; PDF no site do Paraná).
- **Papel:** C/Y de bioma, de baixa resolução temporal. Licença: não verificado (contato: SOS MA; fonte candidata: INPE `dados_abertos`).

#### 2.6 Embargos e autos de infração IBAMA
- **Acesso:** CKAN `https://dadosabertos.ibama.gov.br/api/3/action/` (`package_show?id=fiscalizacao-termo-de-embargo`). Recursos CSV no blob `stibamadadosabertosprd.blob.core.windows.net/dados-abertos/dados/...`:
  - `TERMOS_DE_EMBARGO/TERMO_EMBARGO/termo_de_embargo.csv` (211.814.087 bytes);
  - `.../TERMO_EMBARGO_HISTORICO/termo_embargo_historico.csv` (732.358.513 bytes), com `SEQ_HIST_TAD`, `DT_ALTERACAO` (**histórico de alterações**, útil para reconstruir t0);
  - `.../TERMO_EMBARGO_COORDENADAS`, `_ITENS`, `_ENQUADRAMENTO`, `_DECISAO`;
  - autos: `SIFISC/auto_infracao/auto_infracao/auto_infracao_csv.zip` (123 MB), `enquadramento`, `coordenada`, `bioma`, `especime`.
  - O caminho antigo `SIFISC/termo_embargo/termo_embargo/termo_embargo.csv` em `dadosabertos.ibama.gov.br` ainda serve 170 MB (200), mas migrou para o blob.
- **Campos-chave do embargo:** `DAT_EMBARGO`, `NUM_PROCESSO`, `COD_MUNICIPIO`, `UF`, `DETER_PRODES`, `EMBARGA_POLIGONO`, `QTD_AREA_EMBARGADA`, `NOME_IMOVEL`, `GEOM_AREA_EMBARGADA` (WKT), `SIT_DESEMBARGO`, `DAT_DESEMBARGO`, `DAT_ULT_ALTER_GEOM`, `CPF_CNPJ_EMBARGADO`, `NOME_EMBARGADO`.
- **Defasagem:** o arquivo é regenerado diariamente (`Last-Modified` 28/10/2026). A defasagem entre `DAT_EMBARGO` e a inclusão no arquivo é **desconhecida**. O campo `DAT_ULT_ALTERACAO` e a tabela de histórico permitem estimar a data de inclusão; **testar antes de assumir**.
- **Cobertura:** o primeiro registro visto no histórico é de 2009. Há registros com data errada (um `DAT_EMBARGO` "2925-09-25" na primeira linha do CSV: erro de digitação). Filtrar datas implausíveis.
- **Chave:** sem código CAR no cabeçalho. Ligar por geometria (WKT) ou por nome do imóvel (fraco). CPF/CNPJ presente: **LGPD**.
- **Papel:** Y/O. Evento raro; o embargo é a consequência jurídica e é o que o comprador (banco) enxerga.
- **Observação:** a tabela de metadados tem `license_id: other-open`, `metadata_modified: 2026-10-07`. O portal `servicos.ibama.gov.br` (consulta pública) deu 403 daqui.

#### 2.7 ICMBio: embargos, autos, limites de UC, cavidades (via INDE)
- **Acesso:** GeoServer da INDE, `https://geoservicos.inde.gov.br/geoserver/ICMBio/ows` (GetCapabilities 200; 3,7 MB para o catálogo global). Camadas: `embargos_icmbio` (14.806 feições, 855 em MG, atributos `cpf_cnpj`, `autuado`, `nome_uc`, `cnuc`, `data`, `julgamento`), `autos_infracao_icmbio` (GetFeature JSON/CSV retornou erro "details omitted"; investigar), `limiteucsfederais_a` (347 UCs), `canie_052026_p` (30.746 cavidades), planos de ação (PAN).
- **Hosts antigos:** `geoservicos.icmbio.gov.br` (000), `sistemas.icmbio.gov.br` (403), `www.icmbio.gov.br/cecav` (403). A página atual é `gov.br/icmbio/.../dados-icmbio/dados_geoespaciais`.
- **CANIE:** coordenadas (`latitude`, `longitude`) e `nvl_valida` (Nível 1/2…) públicas, com `num_canie`. Defasagem: edição "052026". Frequência de atualização: não verificado.
- **Papel:** embargos ICMBio = Y/C (raro, só dentro de UC). Cavidades = **C/P exclusivo do carste** (Lagoa Santa/Sete Lagoas): ponto + buffer, restrições de lei específicas (Decreto 99.556/1990; **não verificado**, fonte candidata: Planalto).
- **Licença:** o site do ICMBio declara "Todo o conteúdo deste site está publicado sob a licença Creative Commons Atribuição-SemDerivações 3.0 Não Adaptada". Não está claro que cubra o dado do WFS.

#### 2.8 CNUC (MMA)
- **Acesso:** CKAN `https://dados.mma.gov.br/api/3/action/package_show?id=unidadesdeconservacao`. Há CSVs semestrais desde 2018 e polígonos (`shp_cnuc_2024_02`, `2024_10`, `2025_03`, `2025_08`; 2026_03 e 2026_07 em SharePoint do MMA). WFS INDE com `MMA:cnuc_04_2024`, `cnuc_2025_08`, `cnuc_2026_03`, `cnuc_26_07_31`.
- **Histórico:** **sim, reconstruível**: vários snapshots datados, o que permite o estado de t0 (UCs criadas até t0).
- **Defasagem:** a edição 2026_07 foi criada em 21/08/2026. Cerca de 1–2 meses.
- **Licença:** `license_id: cc-by`, `license_url: http://www.opendefinition.org/licenses/cc-by`.
- **Papel:** C/P (sobreposição de imóvel com UC e entorno).

#### 2.9 SIGEF / SNCI (INCRA)
- **Acesso:** `acervofundiario.incra.gov.br` e `certificacao.incra.gov.br` devolveram **502 do túnel** (negado pela política do proxy ou origem fora do ar). `sigef.incra.gov.br` raiz responde 200; `/downloads/` 404. Segundo um blog técnico, o acervo exige login gov.br prata/ouro (não verificado).
- **Valor esperado:** parcelas certificadas (SIGEF) e do antigo SNCI, com código da parcela, área, município, data de certificação. Registro "congelado" pela certificação. Algumas serventias não alimentam o SIGEF.
- **Alternativas:** download local pelo fundador (com login gov.br); GEE/Base dos Dados (não verificado); `dados.gov.br` (organização INCRA, página SPA sem listagem acessível por texto).
- **Papel:** C (titularidade/regularização), possível âncora de t0 para parte dos imóveis.

#### 2.10 Focos de queimada INPE
- **Acesso:** `https://dataserver-coids.inpe.br/queimadas/queimadas/focos/csv/{10min,diario,mensal,anual}/`. Arquivo diário `diario/Brasil/focos_diario_br_AAAAMMDD.csv` (3–5 MB). Colunas: `id,lat,lon,data_hora_gmt,satelite,municipio,estado,pais,municipio_id,estado_id,pais_id,numero_dias_sem_chuva,precipitacao,risco_fogo,bioma,frp`. Séries anuais "satélite de referência" e "todos os satélites".
- **Defasagem:** horas (10 min para o mais recente). O banco histórico foi construído sem reprocessamento, segundo os desenvolvedores (artigo Biodiversidade Brasileira, 2019). Isso é bom para backtest, porque os dados não mudam.
- **Atenção:** os satélites variam no tempo (GOES-19, NOAA, Terra/Aqua…); usar o "satélite de referência" para séries comparáveis.
- **Licença:** não verificado para o produto; o Programa Queimadas tem sistema de dados abertos alinhado a INDA/INDE, plano de dados abertos do INPE (Portaria 307/2018).
- **Papel:** Y (fogo) e P (histórico de fogo na vizinhança). Candidata a sinal de queimada ilegal se cruzado com período proibitivo.

#### 2.11 INMET e CHIRPS
- **INMET:** `apitempo.inmet.gov.br` ("Empty reply from server"), `portal.inmet.gov.br`, `bdmep`, `mapas`: **inacessíveis**. Alternativas: download local pelo fundador do zip anual de dados históricos (`portal.inmet.gov.br/dadoshistoricos`); Base dos Dados `br_inmet_bdmep` (não verificado); CHIRPS/ERA5-Land por GEE. Licença do INMET: não verificado.
- **CHIRPS v3:** diretório `https://data.chc.ucsb.edu/products/CHIRPS/v3.0/` (daily, 2-monthly, etc.). Página do CHC: dados de 1981 ao presente, resolução 0,05°, preliminar 2 dias após o pentad e final tipicamente na 3ª semana do mês seguinte; "Creative Commons Attribution 4.0 International License"; citação DOI 10.15780/G2JQ0P. Uso comercial permitido.
- **Papel:** P (seca, déficit hídrico).

#### 2.12 Relevo (Copernicus DEM, SRTM, TOPODATA)
- **Copernicus DEM GLO-30:** bucket AWS `copernicus-dem-30m` (COG por tile 1°; tile de teste 43,9 MB baixado e descartado, 200). Licença Copernicus WorldDEM-30 (PDF no Data Space): direitos de reprodução, distribuição, comunicação ao público e **adaptação**; gratuito; atribuição obrigatória; aviso diferente quando adaptado.
- **TOPODATA (INPE):** `http://www.dsr.inpe.br/topodata/` e `/data/geotiff/` (200 via http). Refinamento por krigagem do SRTM 90 m → 30 m, RMSE vertical ~6 m (artigo SciELO, via busca). Licença CC-BY-4.0 apenas por catálogo de terceiros (FedEO). **Não confirmado no INPE.**
- **SRTM:** CGIAR (200). Preferir Copernicus (mais recente) ou TOPODATA (já em formato brasileiro).
- **Papel:** P (declividade, altitude, APP por declividade).

#### 2.13 Hidrografia ANA (BHO, ottobacias)
- **Acesso:** GeoNetwork `metadados.snirh.gov.br` (registro `32e309da-a8c1-443f-90ac-0cd79ce6a33d`, BHO Multiescalas 6, versão 6.2.4, metadado de 17/09/2024). Arquivos GPKG, por exemplo `geoft_bho_trecho_drenagem.gpkg` (**4,06 GB**, HEAD 200), `area_drenagem`, `curso_dagua`, `ponto_drenagem`, `linha_costa`. A busca por API do GeoNetwork pediu CSRF (403). `dadosabertos.ana.gov.br` é um ArcGIS Hub (SPA), sem CKAN.
- **Restrição declarada:** "O acesso ao dado é livre." (campo `otherConstraints`).
- **Papel:** P/C (distância a cursos d'água, bacia, APP hídrica). Estático.

#### 2.14 IBGE (malhas, Censo Agro 2017, PAM/PPM/PEVS)
- **Acesso:** `www.ibge.gov.br` e `sidra.ibge.gov.br` dão **403**. Funcionam: `geoftp.ibge.gov.br/...` e `ftp.ibge.gov.br` (listagem), `apisidra.ibge.gov.br/values/t/<tabela>/...` (JSON). `servicodados.ibge.gov.br/api/v3/malhas` falhou por reset de conexão (000).
- **Malhas:** `malhas_municipais/municipio_{2000…2025}`. Texto da página: "Todos os arquivos aqui disponíveis são públicos."
- **PAM/PPM:** teste SIDRA: t.1612 (soja, c81=2713) para MG retornou valor de 2025 (9.183.919 t); t.3939 (efetivo bovino) 2025 = 22.102.505 cabeças; t.74 (leite) 2025 = 10.070.127 mil litros. Logo, os resultados de 2025 já estavam publicados em out/2026. **Data exata de divulgação: não verificado** (calendário do IBGE). PEVS (t.289 testada) mostrou "..." em 2025.
- **Censo Agro 2017:** SIDRA t.6881 (condição do produtor × utilização das terras). Próximo censo: coleta planejada para 2026, sem resultados (fonte: Poder360/Agência Brasil, 2025).
- **Granularidade:** município. Sem CAR. Chave: código IBGE-7 (presente em `cod_imovel`).
- **Papel:** C/P. Para t0, usar sempre o ano com publicação anterior ao corte.

#### 2.15 ANM / SIGMINE e barragens
- **SIGMINE:** ArcGIS REST em `https://geo.anm.gov.br/arcgis/rest/services/SIGMINE/dados_anm/FeatureServer` (camadas 0–4: processos ativos, áreas de proteção de fonte, arrendamentos, áreas de bloqueio, reservas garimpeiras). Camada 0: `PROCESSO, NUMERO, ANO, FASE, NOME, SUBS, USO, AREA_HA, UF, ULT_EVENTO`. `maxRecordCount` 2000. `UF='MG'` → **51.246** processos ativos. SRID 4674. A página de dados abertos informa "Dados gerados diariamente" e shapefile/KMZ. **Só estado corrente**: não há histórico por data (uma limitação para t0; `ULT_EVENTO` não é série).
- **SIGBM:** dataset `barragens-de-mineracao` (arquivo único; "atualizadas em tempo real"); versão pública do SIGBM. Arquivo não baixado. Licença: gov.br não declara.
- **Papel:** P (pressão minerária; processos em fase de lavra perto do imóvel), C.

#### 2.16 SNISB (ANA)
- Portal WordPress `snisb.gov.br` (200). CSV com 36 atributos por barragem (apresentação UFMG/INDE, fonte secundária). Rotas `portal-snisb/api` retornaram 404. **29.761** estruturas em 2025 (ecycle, citando o relatório da ANA). Plano de ação de emergência é de acesso restrito. Download e licença: não verificado (fonte candidata: página "Consultar barragem" e Relatório de Segurança de Barragens).
- **Papel:** C/P (risco a jusante); complementar ao SIGBM/ANM.

#### 2.17 Base dos Dados (espelhos)
- Site 200; `basedosdados.org/dataset/br-inmet-bdmep` renderiza só em JS (conteúdo não extraído). BigQuery exige credenciais (`bq ls` → "Invalid Credentials"). API GraphQL POST devolveu erro estranho ("Missing required parameters: key, category, endpoint…"). Bucket `storage.googleapis.com/basedosdados-public/` responde 200.
- **Licença:** o README do SDK diz "O projeto (software) está sob licença MIT". A licença dos dados tratados **não verificado**; deve herdar a da fonte.
- **Uso sugerido:** apenas atalho para IBGE (PAM/PPM/PEVS), INMET e MapBiomas estatísticas quando o acesso direto falhar, **após** verificar a licença de cada conjunto.

---


## A.4 Testes de acesso (federais)

| URL | Status HTTP | Observação |
|---|---|---|
| https://consultapublica.car.gov.br/publico/imoveis/index | 301 → loop (50 redirects) | Redireciona entre http e https; WebFetch recebeu 503. Portal oficial não utilizável daqui |
| https://consultapublica.car.gov.br/publico/estados/downloads | 302 (para http://…/imoveis/index) | Idem; captcha segundo README do espelho |
| https://geoserver.car.gov.br/geoserver/ows?service=WFS&request=GetCapabilities | 200 | **Sem FeatureTypeList** (nenhuma camada pública); `rest/layers.json` = 401; raiz do host = 503 |
| https://www.car.gov.br/publico/imoveis/index | 301 | Redireciona para consultapublica |
| https://dados.florestal.gov.br/api/3/action/package_search | 200 | CKAN do SFB. Itens do CAR são camadas de referência (CC-BY) |
| https://data.source.coop/tristangruppwri/cadastral/brazil-car-area-imovel/brazil_car_area_imovel.parquet | 200 (HEAD) | 3.258.574.258 B, `accept-ranges: bytes`; README e collection.json 200 |
| https://dadosabertos.ibama.gov.br/ e /api/3/action/package_show | 200 | CKAN IBAMA |
| https://dadosabertos.ibama.gov.br/dados/SIFISC/termo_embargo/termo_embargo/termo_embargo.csv | 200 | 170 MB (apenas cabeçalho lido). Caminho de `auto_infracao` antigo = 404 (migrou para blob) |
| https://stibamadadosabertosprd.blob.core.windows.net/dados-abertos/dados/TERMOS_DE_EMBARGO/TERMO_EMBARGO/termo_de_embargo.csv | 200 (HEAD) | 211.814.087 B; Last-Modified 28/10/2026 |
| …/TERMO_EMBARGO_HISTORICO/termo_embargo_historico.csv | 200 | 732.358.513 B; cabeçalho lido por range |
| …/SIFISC/auto_infracao/auto_infracao/auto_infracao_csv.zip | 200 (HEAD) | 123.237.339 B |
| https://servicos.ibama.gov.br/ctf/publico/areasembargadas/ConsultaPublicaAreasEmbargadas.php | **403** | WAF; usar o CKAN/blob |
| https://terrabrasilis.dpi.inpe.br/downloads/ | 200 | Antes havia timeout; agora responde |
| https://terrabrasilis.dpi.inpe.br/geoserver/ows (GetCapabilities, GetFeature) | 200 | Consultas pequenas OK. Uma consulta com `cql_filter` a `deter_cerrado` deu *connection reset*; repetir com retry |
| https://terrabrasilis.dpi.inpe.br/citacoes-e-licenca-de-uso/ | 200 | Texto da licença CC BY-SA 4.0 |
| https://data.mapbiomas.org/ | 503 | Site fora do ar no momento |
| https://storage.googleapis.com/mapbiomas-public/ (listagem, STAC, COG) | 200 | Bucket público. Listagem por prefixo OK |
| https://brasil.mapbiomas.org/en/colecoes-mapbiomas/ ; /en/terms-of-use/ | 404 | Páginas de termos não localizadas |
| https://plataforma.alerta.mapbiomas.org/ | 200 | SPA, sem texto de licença |
| https://api.alerta.mapbiomas.org/ ; https://fogo.mapbiomas.org/ ; https://agua.mapbiomas.org/ | 502 (CONNECT) | Negado/indisponível no túnel |
| https://www.sosma.org.br/iniciativas/atlas-da-mata-atlantica | 200 | Download com formulário. `atlasmata.`/`mapas.`/`geo.sosma.org.br` = 000 |
| http://mtc-m21d.sid.inpe.br/…/Atlas_Mata_Atlantica_2024-2025.pdf | 503 (WebFetch) | Não confirmado |
| https://geoservicos.inde.gov.br/geoserver/ICMBio/ows (WFS) | 200 | GetFeature OK para `embargos_icmbio`, `canie_052026_p`, `limiteucsfederais_a`. `autos_infracao_icmbio`: erro "details omitted" |
| https://geoservicos.icmbio.gov.br/ ; https://dadosabertos.icmbio.gov.br/ | 000 | Hosts antigos inacessíveis |
| https://sistemas.icmbio.gov.br/ ; https://www.icmbio.gov.br/cecav/ | **403** | WAF |
| https://dados.mma.gov.br/api/3/action/package_show?id=unidadesdeconservacao | 200 | PDF de dicionário baixou (200). Alguns arquivos recentes estão em SharePoint do MMA |
| https://cnuc.mma.gov.br/ | 404 | `/pt-br` = 200 |
| https://acervofundiario.incra.gov.br/ ; https://certificacao.incra.gov.br/ | **000 (502 CONNECT)** | Bloqueado. `sigef.incra.gov.br` raiz 200; `/downloads/` 404 |
| https://dataserver-coids.inpe.br/queimadas/queimadas/focos/csv/ | 200 | Diário, 10min, mensal, anual. CSV diário lido por range (cabeçalho OK) |
| https://data.inpe.br/geonetwork/…/records/… | 502 | Catálogo de metadados do INPE instável |
| https://portal.inmet.gov.br/…; https://apitempo.inmet.gov.br/…; https://bdmep.inmet.gov.br/ | **000** | "Empty reply from server" (apitempo). Bloqueio de origem |
| https://data.chc.ucsb.edu/products/CHIRPS/v3.0/ | 200 | v2.0 em `/products/CHIRPS-2.0/…` = 404 |
| https://copernicus-dem-30m.s3.eu-central-1.amazonaws.com/…/Copernicus_DSM_COG_10_S20_00_W044_00_DEM.tif | 200 | Tile de 43,9 MB (descartado). OpenTopography S3 = 403 |
| https://planetarycomputer.microsoft.com/api/stac/v1/collections/cop-dem-glo-30 | 200 | `license: other`. `collections/chirps` = 404 |
| http://www.dsr.inpe.br/topodata/acesso.php ; /data/geotiff/ | 200 | Só em http; https falha |
| https://www.ibge.gov.br/ ; https://sidra.ibge.gov.br/ | **403** | WAF |
| https://geoftp.ibge.gov.br/… ; https://ftp.ibge.gov.br/ | 200 | Malhas 2000–2025, Censo Agro 2017 |
| https://apisidra.ibge.gov.br/values/t/1612/… | 200 | JSON. `servicodados.ibge.gov.br/api/v3/malhas` = 000/reset |
| https://metadados.snirh.gov.br/…/records/<uuid>/formatters/xml | 200 | Metadado BHO. `…/files/<uuid>/geoft_bho_trecho_drenagem.gpkg` = 200 (HEAD, 4.058.632.192 B). Busca POST do GeoNetwork = 403 (CSRF) |
| https://dadosabertos.ana.gov.br/ | 200 | ArcGIS Hub; `api/3/action/*` = "Cannot GET" |
| https://geo.anm.gov.br/arcgis/rest/services/SIGMINE/dados_anm/FeatureServer/0/query | 200 | `returnCountOnly` com `UF='MG'` → 51.246 |
| https://app.anm.gov.br/SIGMINE/Publico/ ; …/dadosabertos/…zip | 000 | Inacessível. Usar o ArcGIS REST |
| https://www.snisb.gov.br/ | 200 | `portal-snisb/api/*` = 404; `portal1.snirh.gov.br/ana/rest/services` = 500 |
| https://dados.gov.br/ | 200 | SPA; API pública = 401 |
| https://basedosdados.org/ ; storage.googleapis.com/basedosdados-public/ | 200 | `bq ls --project_id=basedosdados` → "Invalid Credentials" (sem conta) |

Observação: `HTTPS_PROXY` do ambiente retorna 502 para alguns hosts (`ide.meioambiente.mg.gov.br`, `zee.meioambiente.mg.gov.br` estão no log de falhas do proxy). Isso é relevante para a frente estadual de MG.

---


---

# Anexo B — Bases de Minas Gerais (relatório do agente `engenheiro-dados-geo`)

Verificado em 2026-10-28 a partir do ambiente de nuvem da sessão (saída por proxy). Regra: o que não foi verificado está marcado "não verificado" + fonte candidata.

### 0. Achado principal

O endpoint real do GeoServer da IDE-Sisema é `https://geoserver.meioambiente.mg.gov.br/` (WFS/WMS), **acessível sem autenticação e sem bloqueio a partir deste ambiente**. Os hosts `idesisema.meioambiente.mg.gov.br/geoserver/...` (404) e `idesisema...` raiz (403) NÃO são o endpoint. O GetCapabilities WFS (HTTP 200, ~1 MB gzip) lista **1.420 feature types** (namespace `IDE`, CRS padrão EPSG:4674). Saídas WFS testadas: `application/json`, `csv`, `SHAPE-ZIP` (HTTP 200 com `count=1`). O próprio Capabilities declara `Fees: NONE` e `AccessConstraints: NONE` (isso NÃO é uma licença; ver seção 3).

Atenção: a camada pública NÃO traz polígonos de imóveis do CAR (perímetros). Traz apenas derivados do CAR agregados (APP hídrica, uso restrito, vegetação "Análise Dinamizada", imóveis disponíveis para recomposição). O perímetro do imóvel segue vindo do SICAR federal (ver seção 2.10).

### 1. Tabela-catálogo resumida

Camadas WFS (prefixo `IDE:`; contagem = `numberMatched` em 2026-10-28).

| # | Base | Órgão | Camada / acesso | Registros | Cobertura temporal observada | Chave p/ CAR | Potencial como Y / feature |
|---|---|---|---|---|---|---|---|
| 1 | Áreas embargadas pelo Sisema (com dados do auto) | SEMAD (IEF/FEAM) | `ide_2304_mg_areas_embargadas_sisema_pol` | 11.470 | datas 2021-2026; ~6.760 de 2026 (mar-set/2026) -> parece snapshot do sistema novo, NÃO série histórica | Geometria (polígono do embargo); `doc_fiscal` (CNPJ sem máscara em 811; CPF mascarado) | Y forte (supressão sem autorização FL-01/02/03/04, queimada FL-17), mas só desde ~2026 |
| 2 | Áreas autorizadas p/ supressão (IEF) | IEF | `ide_2105_mg_area_autorizada_intervencao_ambiental_ief_pol` | 3.869 | processos 2019-2026 (pico 2024: 1.142) | Geometria; `n_processo` (SEI) | Feature: supressão autorizada (contra-fator do Y "supressão não autorizada") |
| 3 | Áreas autorizadas p/ intervenção (FEAM) | FEAM | `ide_2105_mg_area_autoriz_interv_amb_feam_pol` | 86 | não verificado | Geometria | Feature (mineração/licenciamento) |
| 4 | Outorgas de uso de recursos hídricos | IGAM | `ide_2103_mg_outorgas_uso_recursos_hidricos_pto` (+ `..._federais_ana_...`, `..._uso_insignificante_...`) | 58.741 | `datpub_4` de 2001-07-04 a 2025-07-03 (extremos verificados por sortBy) | Ponto + `cobacia/cotrecho` (ottobacia); `cpfcnpj_4` mascarado | Feature (pressão hídrica); histórico reconstruível (data de cadastro/publicação) |
| 5 | Áreas de conflito hídrico superficial (DAC) | IGAM | `ide_2007_mg_area_conflito_recursos_hidricos_pol` | 110 | campos `numdac` (ex. 003/2013), `portcol` (portaria 2022); sem data de vigência estruturada | Geometria (sobreposição) | Feature/Y de conflito hídrico (poucos eventos; defasagem = publicação no Diário Oficial) |
| 6 | Áreas de restrição/controle de águas subterrâneas | IGAM | `ide_2007_mg_restricao_contole_rh_sub_pol` (+ `ide_2007_sf_rpe_100_pol`) | 4 | não verificado | Geometria | Feature (restrita ao Norte de MG, irrelevante p/ RMBH) |
| 7 | Barragens (rejeitos/resíduos) - ano base 2024 | FEAM | `ide_1901_mg_barragens_rejeitos_residuos_pto` (+ PAE: `ide_1903_mg_mancha_inundacao_pae_pol`, `ide_1903_mg_zas_pae_pol`) | 259 | ano base 2024 (snapshot) | Ponto (`id_sigibar`) | Feature (proximidade/ZAS); não é Y |
| 8 | Cavidades: raio de influência 250 m e potencialidade | FEAM (dados CECAV/CANIE) | `ide_2001_mg_raio_protecao_cavidades_pol` (14.719), `ide_2002_mg_potencialidade_cavidades_pol` | 14.719 | snapshot | Geometria | Feature (restrição no carste de Lagoa Santa/Sete Lagoas) |
| 9 | Licenças ambientais emitidas (SLA) | SEMAD | `ide_2101_mg_empreendimentos_licenciados_pto`; histórico `ide_2101_mg_historico_empreendi_lic_2013_2019_pto` | 19.713 (todas "Concluído Deferido") | emissão 2019-2026 + histórico 2013-2019 | Ponto lat/lon; `cpf_cnpj` (SEM máscara no exemplo); `n_processo` | Feature (licenciamento ativo no entorno) |
| 10 | Inventário Florestal / cobertura vegetal | IEF/UFLA | `ide_0301_mg_cobertura_florestal__2009_pol` | 823.016 | referência 2009 (rótulo da camada); campos `class_name`, `hectares` | Geometria | Feature base (estática, antiga) |
| 11 | Cobertura da Mata Atlântica 2019 | SEMAD/IEF | `ide_0301_mg_cobertura_mata_atlantica_2019_lote1/2/3_pol` | não verificado | 2019 | Geometria | Feature/baseline de vegetação |
| 12 | CAR derivados: APP hídrica, uso restrito, FIP-CAR, Análise Dinamizada 2024/2025 | IEF | `ide_210603_*_mapcar_*`, `ide_210604_mg_analise_car_veg_2025_*`, `..._area_consol_2025_*`, `..._area_antrop_2025_*` (por URFBio) | ex. Metropolitana veg 2025: 206.951; APP cm: 9.094 | 2024 e 2025 (duas edições de vegetação) | Geometria; SEM código do CAR nos atributos testados (`classe_`, `categoria`) | Feature: dois cortes (2024 e 2025) permitem delta de vegetação por imóvel, com cautela |
| 13 | Áreas prioritárias p/ conservação (PSCRMG 2021) | IEF/UFMG/WWF/Biodiversitas | `ide_2411_mg_areasprioritarias_mapa_geral_pol` (232) + 8 camadas temáticas; ArcGIS FeatureServer espelho | 232 | 2020/2021 (publicado 2021) | Geometria | Feature (zonas de maior valor/pressão) |
| 14 | Diagnóstico Ambiental da Fiscalização (fatores de pressão; características relevantes) | SEMAD | `ide_2303_mg_diagnostico_fisc_fatores_pressao_{2021..2025}_pol`, `..._carac_amb_rele_{2021..2025}_pol` | não verificado | 2021-2025 (anual) | Geometria (grade/unidade de planejamento, não verificado) | Feature: já contém a priorização de fiscalização do próprio Estado (concorrente e sinal) |
| 15 | ZEE-MG | SEMAD (IDE) | ~72 camadas "ZEE" (ex. `ide_2401_mg_aptidao_edafo_cana_pol`, `..._eucalipto_pol`) | n/v | edição única (data não verificada) | Geometria | Feature contextual (aptidão/vulnerabilidade) |
| 16 | UCs, RPPN, zonas de amortecimento, áreas prioritárias p/ criação de UCs | IEF | `ide_2010_*`, `ide_2011_*` | n/v | snapshot | Geometria | Feature (sobreposição com áreas protegidas) |
| 17 | ZAP (zoneamento ambiental produtivo) por sub-bacia, com conflito uso x unidade de paisagem e outorgas | SEMAD/IGAM | ~333 camadas "ZAP" (ex. Ribeirão Santana, Serra da Piedade, Alto Rio Bagagem) | n/v | 2024 | Geometria | Feature local (cobertura parcial; checar bacias da RMBH) |
| 18 | IEV (Índice de Estado da Vegetação?), Idam | SEMAD | `ide_2204_*`, `ide_2408_*` | n/v | 2022/2024 | Município | Feature municipal (sigla IEV não verificada) |

Bases fora do GeoServer ou não acessíveis a partir daqui:

| # | Base | Órgão | Acesso | Status |
|---|---|---|---|---|
| 19 | Portal de Dados Abertos de MG | Governo MG | `https://dados.mg.gov.br/` | 403 (WAF) a partir daqui; conteúdo não verificado |
| 20 | Infohidro (outorgas, séries) | IGAM | `https://portalinfohidro.igam.mg.gov.br/` | 200; página institucional; datasets não verificados |
| 21 | SLA (Sistema de Licenciamento) público | SEMAD | `https://ecosistemas.meioambiente.mg.gov.br/sla/#/acesso-visitante` | 200 (SPA; backend/API não explorado) |
| 22 | Autos de infração (PMMG, IEF, SEMAD) | SEMAD/PMMG | nenhuma base aberta localizada | não verificado; só o recorte da camada 1 (embargos) |
| 23 | CANIE/CECAV (cavidades, base nacional) | ICMBio | `icmbio.gov.br/cecav/canie.html` | 403 (icmbio.gov.br/cecav) a partir daqui |
| 24 | CAR (perímetros) SICAR | SFB | `consultapublica.car.gov.br` | redirecionamento em loop (302 -> http ... -> 302) a partir daqui |

#### 2. Ficha por base

#### 2.1 IDE-Sisema (infraestrutura)
- Órgão/produto: Infraestrutura de Dados Espaciais do Sistema Estadual de Meio Ambiente e Recursos Hídricos, mantida pela Diretoria de Estratégias em Geotecnologias e Informação Geográfica (Dgeo)/SEMAD (contato no Capabilities). Governança por Comitê Gestor, instituída pelas Resoluções Conjuntas SEMAD/FEAM/IEF/IGAM 2.466/2017 e 2.631/2018 ([Agência Minas, 2022](https://agenciaminas.mg.gov.br/news/pdf/111806.pdf), conforme resumo de busca; texto da Resolução 3.147/2022 NÃO verificado).
- Acesso: WFS 2.0.0 `https://geoserver.meioambiente.mg.gov.br/wfs` (GeoServer 2.20.4 indicado em [geoserver.meioambiente.mg.gov.br/web/](https://geoserver.meioambiente.mg.gov.br/web/)); WMS `.../wms` (Capabilities 2,9 MB, 200); catálogo de metadados GeoNetwork `https://idesisema.meioambiente.mg.gov.br/geonetwork/srv/api/records/<uuid>` (200); visualizador `https://visualizador.idesisema.meioambiente.mg.gov.br/` (200); `https://idesisema.meioambiente.mg.gov.br/` (raiz) retorna 403; `geoportal.meioambiente.mg.gov.br` retorna 403.
- Formatos: GeoJSON, CSV, Shapefile (SHAPE-ZIP), GML. Para GeoParquet: baixar via WFS GeoJSON paginado (`startIndex`/`count`, `srsName=EPSG:4674`) e converter. Observação: GeoJSON do GeoServer devolve `urn:ogc:def:crs:EPSG::4674` corretamente.
- Número de camadas: 1.420 no WFS hoje; a imprensa estadual citou 715 camadas em 2022 ([Agência Minas](https://agenciaminas.mg.gov.br/news/pdf/111806.pdf)) e 813 em outro documento (não verificado), logo o catálogo cresce rápido e muda.
- Defasagem de publicação: variável e NÃO registrada de forma estruturada; o catálogo GeoNetwork tem data de metadado por camada (não extraída em massa). Tratar cada camada como "snapshot do dia do download" a menos que haja campo de data próprio.
- Reconstrução em t0: o WFS entrega **apenas o estado atual**. Sem versionamento. Para backtest é necessário (a) usar campos de data internos (outorgas, licenças, supressões, embargos) para reconstruir o estado em t, e (b) arquivar snapshots a partir de agora (script com data+hash) e (c) pedir ao fundador a verificação no Wayback/Memory (não testado) de versões antigas.
- Qualidade: nomes de campo truncados (shapefile legado, ex. `fiscalizad`, `data_fisca`); formatos de data inconsistentes (ver 2.2); erros de digitação em valores (ex. "Defeirdo" em `decisao`).

#### 2.2 Áreas embargadas pelo Sisema (`ide_2304_mg_areas_embargadas_sisema_pol`)
- Campos observados: `num_ai`, `af_vincula`, `num_ato_fi`, `fiscalizad` (nome do autuado), `doc_fiscal`, `data_fisca`, `local_fisc` (município), `atividade_` (códigos FL-01...), `decreto` (47.383/2018), `artigo`, `codigo`, `penalidade`, `valor_mult`, `outras_pen` ("Embargo / Suspensão de atividades").
- Volume/cobertura: 11.470 polígonos. Datas em dois formatos (`dd/mm/aaaa` e ISO). Por ano: 2021 (5), 2022 (1), 2024 (9), 2025 (64), 2026 (6.763 em formato dd/mm; os demais com ISO, majoritariamente 2026-03 a 2026-09). Conclusão: a camada parece ter sido (re)alimentada em 2026, NÃO é série histórica. Frações por atividade: FL-01 supressão área comum (7.800), FL-02 APP (1.225), FL-17 queimada (516), FL-06 (491), FL-03 Reserva Legal (482), FL-04 UC (218).
- LGPD: `fiscalizad` traz nome; `doc_fiscal` vem mascarado para CPF (`XXX.999.999-XX`, 10.659 registros) e **sem máscara para CNPJ (811)**. CNPJ não é dado pessoal por si, mas pode identificar empresário individual; tratar com cautela e não persistir nomes no produto final.
- Y: é o melhor candidato a Y estadual (embargo por supressão), com chave espacial e tipificação legal. Defasagem entre infração e registro: não verificada (campo `data_fisca` é a data da fiscalização, não da publicação). Para backtest, o histórico é insuficiente hoje; precisa de pedido via LAI de série completa de autos/embargos (2015+).
- Ligação ao CAR: apenas por interseção espacial.

#### 2.3 Supressão autorizada (IEF) (`ide_2105_..._ief_pol`)
- Campos: `n_processo` (SEI), `autorizado` (URFBio, não nome), `municipio`, `modalidade`, `area_autor` (ha), `data_publi`, `ano`, `mes`, `decisao` (Deferido), `bioma`.
- Cobertura: 3.869 polígonos; 2022: 339; 2023: 895; 2024: 1.142; 2025: 820; 2026: 655; 2019-2021: 15. Só deferidos. Modalidade principal: supressão de cobertura vegetal nativa para uso alternativo do solo (2.649) e intervenção em APP (1.201).
- Defasagem: `data_publi` é a data de publicação da autorização (útil contra vazamento); lag de entrada na camada não verificado.
- Uso: permite classificar supressão detectada por satélite (MapBiomas Alerta/PRODES) como autorizada ou não, via interseção. É a peça que falta para um Y "supressão não autorizada".

#### 2.4 Outorgas IGAM (`ide_2103_mg_outorgas_uso_recursos_hidricos_pto`)
- Campos: `numpa_4` (processo), `numport_4` (portaria), `datcad_4`, `datpub_4`, validade (`anovenc_4`), `statuspa_4`, `usoinsig_4`, bacia (`ch_4`), `cpfcnpj_4` mascarado, `empto_4` truncado ("Edson******"), `cobacia`, `cotrecho`, `nuareacont` (área de contribuição), `codmodus_4` (modalidade de uso).
- 58.741 pontos; publicação de 2001 a 2025-07 (último registro `datpub_4` = 2025-07-03 na data do teste, ou seja, a camada tem ~16 meses de atraso em 2026-10 OU é atualizada por lotes; confirmar).
- Reconstrução em t0: viável (filtrar por `datpub_4` <= t e vigência), com ressalvas de outorgas revogadas/vencidas ausentes (a camada parece listar apenas vigentes: não verificado).
- Potencial: feature de pressão hídrica (densidade de outorga por ottotrecho vs. vazão Q7,10 das camadas de regionalização `ide_240502_mg_igam_reg_vazao_lin`).

#### 2.5 Áreas de conflito hídrico (DAC) (`ide_2007_mg_area_conflito_recursos_hidricos_pol`)
- Base legal: Decreto 47.705/2019; DAC publicada no Diário Oficial e no site do IGAM ([resumo de busca com texto do decreto](https://comitespcj.org.br/wp-content/uploads/2025/03/Decreto_MG_47705_2019.pdf)).
- 110 polígonos, com `numdac` (ano no número), `portcol`, `q7_10_ref`, `area_km2`, `dtverdac`. Sem campo estruturado de início/fim de vigência -> reconstrução histórica só pelo número/ano da DAC ou pela publicação no Diário Oficial.
- Como Y: raro e institucional (muda por ato administrativo, não por comportamento do produtor). Melhor como feature de contexto. Para RMBH: verificar sobreposição (não verificado).

#### 2.6 Barragens (FEAM) e PAE
- 259 pontos, ano base 2024: campos `id_sigibar`, `empreended`, `municipio`, `pda` (dano potencial associado), `classe`. Manchas de inundação e ZAS dos PAEs como camadas separadas.
- Lembrar que o cadastro nacional (ANM/SIGBM) é a fonte federal; a FEAM cobre barragens de rejeitos/resíduos licenciadas pelo Estado.

#### 2.7 Cavidades/carste
- IDE: raio de 250 m (`ide_2001`, 14.719 polígonos) e potencialidade de ocorrência (`ide_2002`), mais camadas de carste prioritário para restauração (`ide_1806_mg_ucs_prior_cons_espel_pol`, "Áreas cársticas prioritárias para restauração ecológica/melhoria de pastagens"). Origem das cavidades: CECAV/CANIE (ICMBio). Os metadados CANIE descrevem shapefile em SIRGAS 2000, atualização mensal e ressalva de cobertura parcial ([Metadados CANIE dez/2022](https://www.gov.br/icmbio/pt-br/assuntos/centros-de-pesquisa/cecav/cadastro-nacional-de-informacoes-espeleologicas/metadados-canie-19dez2022.pdf), citado via busca; a URL devolveu 404 neste teste). Licença do CANIE: não verificada; contato candidato cecav.sede@icmbio.gov.br.
- Cavidades sigilosas podem estar ausentes (restrição de divulgação; fonte: [Infrasa/SISLIC](https://geo.infrasa.gov.br/server/rest/services/Cavidades_Naturais_Subterr%C3%A2neas/MapServer/layers)).
- Controvérsia sobre a origem dos dados do CANIE (crítica da SBE em 2014, ver [SBE Notícias 289](https://cavernas.org.br/wp-content/uploads/2021/07/SBENoticias_289.pdf)) -> risco reputacional/de atribuição.

#### 2.8 Licenciamento (SLA) e histórico
- Camada de licenças emitidas (19.713 pontos, todos "Concluído Deferido", com `cpf_cnpj` NÃO mascarado no exemplo, `link` para o SLA visitante). Anos de emissão: 2019 (263), 2020 (4.479), 2021 (5.033), 2022 (3.591), 2023 (2.177), 2024 (1.895), 2025 (1.528), 2026 (747). Histórico 2013-2019 em camada separada.
- Só deferidos: não captura indeferimentos, processos em andamento nem licenças vencidas/canceladas -> viés de sobrevivência para backtest.
- Dado de empreendimento (pessoa jurídica/pessoa física); remover CPF/CNPJ antes de persistir.

#### 2.9 Inventário Florestal, áreas prioritárias, ZEE
- Inventário Florestal de MG: camada vetorial `ide_0301_mg_cobertura_florestal__2009_pol` (823 mil polígonos, `class_name`, `hectares`). Origem: IEF/UFLA; primeira fase concluída em 2004 e mapa publicado em 2005; nova edição em 2008 ([Agência Minas](https://www.agenciaminas.mg.gov.br/noticia/inventario-revela-queda-de-30-no-desmatamento-em-minas-gerais-48249)). A relação exata entre o rótulo "2009" e as edições não foi verificada. É estático e antigo (baseline), não série.
- Áreas prioritárias (PSCRMG 2021): relatório [Biodiversitas/UFMG/WWF/IEF](https://biodiversitas.org.br/wp-content/uploads/2021/10/Relatorio_Areas-Prioritarias2021_PSCRMG.pdf) (PDF 6,8 MB, HTTP 200). Espelho ArcGIS: `https://services1.arcgis.com/RTK5Unh1Z71JKIiR/ArcGIS/rest/services/Layers_Story_PSCRMG2/FeatureServer` (HTTP 200, camadas incluem `XXXX_MG_AreasPrioritarias2020`; `copyrightText` vazio).
- ZEE-MG: 72 camadas no WFS (ex. aptidão edafoclimática cana/eucalipto). Página oficial do ZEE-MG e data de edição: não verificados; `zee.meioambiente.mg.gov.br` não resolveu (000).

#### 2.10 CAR estadual vs SICAR
- Em MG o cadastro é feito no SICAR federal; a análise é do IEF/FEAM conforme o vínculo (licenciamento, autorização de intervenção, regularização), pela Resolução Conjunta SEMAD/FEAM/IEF 3.390/2025 ([FIEMG](https://www.fiemg.com.br/wp-content/uploads/2025/11/IE_RESOLUCAO-CONJUNTA-SEMAD_FEAM_IEF-No-3390-DE-10-DE-NOVEMBRO-DE-2025-pdf.pdf)) e por "análise dinamizada" (cruzamento automático com base de imagens), que passou a rodar no módulo do SICAR a partir de fev/2025, com mais de 45 mil CARs enviados e 28 mil validados, e mais de 150 mil CARs analisados no estado até o fim de 2025 ([Agência Minas](https://www.agenciaminas.mg.gov.br/noticia/tecnologia-e-apoio-ao-produtor-fazem-minas-gerais-saltar-de-281-para-28-mil-imoveis-regularizados-no-cadastro-ambiental-rural), números conforme resumo de busca, não conferidos no original).
- Conclusão: não há um "CAR estadual" separado com geometrias públicas na IDE. O que o Estado publica são derivados da análise (APP, uso restrito, vegetação 2024/2025, imóveis para recomposição). Perímetros e status do recibo vêm do SICAR (ver pesquisa federal da outra frente). Teste neste ambiente: `consultapublica.car.gov.br` entra em loop de redirecionamento; alternativa: download local pelo fundador ou espelhos (IPAM/Imaflora/MapBiomas), a levantar na frente federal.
- Retificações: nenhuma camada da IDE guarda versão/recibo; para geometria em t0 será preciso snapshot do SICAR com data (fora desta frente).

#### 2.11 Autos de infração (SEMAD/IEF/PMMG), DAIA
- Autos de infração em formato aberto: nenhuma base localizada. A busca por lista pública de embargos/autos não encontrou página oficial ([resultado de busca](https://www.agenciaminas.mg.gov.br/news/pdf/124684.pdf) sem relação direta). A camada de embargos (2.2) é o único recorte espacial público. Caminho: pedido via Lei de Acesso à Informação (LAI) à SEMAD/Subsecretaria de Fiscalização (base completa de AIs com data de lavratura, tipo penal, município, coordenadas, status do processo) e à PMMG/Polícia Militar de Meio Ambiente (não verificado se há base aberta).
- DAIA: no estado a autorização de intervenção ambiental é publicada; a camada 2.3 é o espelho espacial. DAIA em tabela (sem polígono) com datas: não verificado (candidato: portal de transparência/IEF).

#### 2.12 Dados abertos de MG (dados.mg.gov.br)
- `https://dados.mg.gov.br/` e `https://www.dados.mg.gov.br/api/3/action/package_list` retornam **403** (WAF bloqueia datacenter). `dadosabertos.mg.gov.br` não resolve. Conteúdo, licença e datasets: não verificados. Política estadual de dados abertos: nenhuma norma localizada (busca por decreto estadual não retornou texto; só o Decreto 48.237 de LGPD no serviço público estadual foi citado). Fonte candidata: Diário Oficial de MG e CGE-MG.
- Alternativa: Base dos Dados (`https://basedosdados.org/`, HTTP 200) ou pedido ao fundador de acesso local à página.

## B.4 Testes de acesso (MG)

| URL | Status HTTP | Observação |
|---|---|---|
| https://geoserver.meioambiente.mg.gov.br/wfs?service=WFS&request=GetCapabilities | 200 | application/xml, ~1,0 MB; 1.420 feature types; Fees/AccessConstraints NONE |
| https://geoserver.meioambiente.mg.gov.br/ows?service=WFS&version=2.0.0&request=GetCapabilities | 200 | idêntico |
| https://geoserver.meioambiente.mg.gov.br/wms?service=WMS&request=GetCapabilities | 200 | ~2,9 MB; Fees/AccessConstraints NONE |
| https://geoserver.meioambiente.mg.gov.br/web/ | 200 | interface GeoServer (versão 2.20.4 segundo resultado de busca) |
| .../wfs ... GetFeature resultType=hits (14 camadas) | 200 | contagens da seção 1; ~1 s cada |
| .../wfs ... GetFeature count=1 outputFormat=application/json srsName=EPSG:4674 | 200 | geometria em EPSG:4674 |
| .../wfs ... outputFormat=SHAPE-ZIP e csv (count=1) | 200 | zip e csv ok |
| .../wfs ... propertyName (sem geometria) das camadas de embargos, supressão e licenças | 200 | 216 KB / 63 KB / 183 KB; viável para auditoria de datas |
| https://idesisema.meioambiente.mg.gov.br/geonetwork/srv/api/records/<uuid> | 200 | metadado JSON/XML; exemplo mapa de solos |
| https://idesisema.meioambiente.mg.gov.br/geonetwork/srv/api/site | 500 | API de site não utilizável |
| https://visualizador.idesisema.meioambiente.mg.gov.br/ | 200 | viewer |
| https://idesisema.meioambiente.mg.gov.br/ | 403 | WAF na raiz (150 bytes) |
| https://idesisema.meioambiente.mg.gov.br/geoserver/ows?... | 404 | endpoint incorreto |
| https://geoportal.meioambiente.mg.gov.br/ | 403 | bloqueio |
| https://www.dados.mg.gov.br/ , https://dados.mg.gov.br/ , .../api/3/action/package_list | 403 | WAF; alternativa: acesso local pelo fundador |
| https://dadosabertos.mg.gov.br/ | sem resposta (000) | não resolve/timeout |
| https://www.ief.mg.gov.br/ | 403 | bloqueio |
| https://sistemas.meioambiente.mg.gov.br/ | 403 | bloqueio |
| https://meioambiente.mg.gov.br/documents/d/ief/... | 403 | bloqueio |
| https://www.meioambiente.mg.gov.br/ , ide.meioambiente.mg.gov.br, zee.meioambiente.mg.gov.br, licenciamento.meioambiente.mg.gov.br | 000 | sem resposta (DNS/timeout) |
| https://www.igam.mg.gov.br/ | 000 | timeout 8 s |
| https://portalinfohidro.igam.mg.gov.br/ | 200 | 140 KB, institucional |
| https://ecosistemas.meioambiente.mg.gov.br/sla/#/acesso-visitante | 200 | SPA (19 KB) |
| https://services1.arcgis.com/RTK5Unh1Z71JKIiR/ArcGIS/rest/services/Layers_Story_PSCRMG2/FeatureServer?f=json | 200 | espelho das áreas prioritárias |
| https://biodiversitas.org.br/.../Relatorio_Areas-Prioritarias2021_PSCRMG.pdf | 200 | PDF 6,8 MB |
| https://www.icmbio.gov.br/cecav/downloads/mapas.html | 403 | bloqueio |
| https://www.gov.br/icmbio/... cecav... (varias URLs) | 404 | URLs informadas por busca não existem mais |
| https://consultapublica.car.gov.br/publico/imoveis/index (e /estados/downloads) | 302 em loop (50 redirecionamentos) | SICAR inacessível por curl neste ambiente; www.car.gov.br raiz = 200 |
| https://www.agenciaminas.mg.gov.br/news/pdf/116851.pdf | 410 | removido |
| https://basedosdados.org/ | 200 | alternativa para dados tratados |

Reprodutibilidade: URLs de exemplo (sem baixar bases): `.../wfs?service=WFS&version=2.0.0&request=GetFeature&typeNames=IDE:<camada>&resultType=hits`.

