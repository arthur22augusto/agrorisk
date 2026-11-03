# 07 — Gate do Y (sessão 07, Etapa 0)

- Data de execução: 2026-11-03. Código: `src/agrorisk/gate.py` (`python -m agrorisk.gate --recorte vitrine`). Tabelas: `reports/07-gate/`.
- Dados: snapshot CAR de 2026-11-03 (41.402 CARs na vitrine; hash em `docs/dados/snapshots_registro.csv`), PRODES Cerrado + Mata Atlântica (TerraBrasilis, baixado em 2026-11-03), IDE-Sisema (IEF e FEAM), ANM SIGMINE (processos ativos, snapshot atual), IBGE Áreas Urbanizadas 2022.
- Convenção: ano-PRODES *y* = ciclo ago/(y−1)–jul/y; t₀ = 31/jul/(y−1). Testes: anos-PRODES 2021–2024 (t₀ 2020–2023). Evento = CAR × ano com ≥ 1 ha **contíguo** de supressão PRODES dentro do polígono. Áreas em EPSG:31983.
- **Todo o resultado é exploratório e otimista**: usa a geometria **vigente** do CAR (ver (d)). Revisado pelo agente `estatistico-modelagem`; as correções dele estão incorporadas (fração mínima de autorização, anel de vizinhança sem o próprio imóvel, sensibilidades com IC, DISPONIBILIDADE fora de mineração).

## Veredito

**A regra literal de parada não dispara, mas o gate passa com ressalvas que o fundador precisa decidir.**

| Teste da regra (escopo-mvp §3) | Resultado (pooled 2021–24) | Limiar | Leitura |
|---|---|---|---|
| Positivos que são Y_agro ∧ ≤ 4 MF (todos os 1.044 positivos) | **47,7%** (IC95% 39,9–55,6, bootstrap por município) | ≥ ~30% | passa |
| Idem, só CARs elegíveis em t₀ e **sem evento prévio/vizinhança** (n = 572 elegíveis) | **32,3%** (IC 25,0–39,9); por ano: 23,3 / 39,1 / 24,7 / 32,3 | ≥ ~30% | **no limite; o IC cruza 30%** |
| Idem, só elegíveis com **geometria estável** (`atualizacao ≤ t₀`; n = 62 positivos) | **25,8%** (IC 15,3–39,1) | ≥ ~30% | abaixo, mas n pequeno |
| Positivos em que o histórico (imóvel 3 anos ∪ vizinhança 1 km, 12 m) já aparece — elegíveis | **46,7%** (IC 39,2–53,9) | "quase tudo" | **não** explica quase tudo; explica quase metade |

Recomendação: **seguir para o painel, mas sem congelar o protocolo de forma definitiva sem a decisão do fundador** (§Decisão pendente). Nenhum dos números abaixo permite afirmar que o produto "funciona"; eles só mostram que o escopo não foi derrubado pelo gate.

## Resultados por item

### (a) Porte (módulos fiscais)
Atenção à leitura: os **positivos** são em maioria ≤ 4 MF porque há muitos CARs pequenos; a **taxa de evento por CAR** é muito maior nos grandes (painel 2021–24, elegíveis: ≤ 4 MF 0,34%; 4–15 MF 2,04%; > 15 MF 4,39% — `notebooks/07-eda-painel.ipynb`). O recall do preditivo em ≤ 4 MF parte de uma taxa-base ~0,3%.
Positivos ≤ 4 MF: **52,0%** (por ano 48,8 / 56,4 / 47,8 / 49,8); 4–15 MF: ~28%; > 15 MF: ~20% (`positivos_por_porte_vitrine.csv`). Entre os elegíveis a fração ≤ 4 MF é 53%; entre os inelegíveis, 50%. Atenção: `m_fiscal` é o valor atual do SICAR.

### (b) Destino: mineração e urbano
- Mineração (≥ 50% da área do evento sob processo SIGMINE em fase de lavra/licenciamento/registro de extração): **10,7%**. Incluindo requerimentos e autorizações de **pesquisa**, 23,8% — sensibilidade, pois título minerário não prova destino minerário.
- Urbano (≥ 50% em Áreas Urbanizadas IBGE 2022): **3,3%**.
- **Y_agro = 87,1%** dos positivos. Limitações: SIGMINE (só processos ativos hoje) e IBGE 2022 são fotos atuais/recentes, o que subestima o não-agro de 2021; **MapBiomas (matriz de transição) não foi obtido**: `storage.googleapis.com/mapbiomas-public` retorna 403 pelo proxy da nuvem (ver "Bloqueios").

### (c) Autorização IEF/FEAM (janela ±12 meses do ciclo; interseção ≥ 10% do evento)
**1,0%** dos positivos têm autorização identificada (IEF datado 0,8%; FEAM sem data ~0,2%). Esse número **não é informativo**: a camada IEF na vitrine tem só 314 feições, 2021–2026, então para os ciclos 2021–22 a janela é truncada e o 0,0% em 2021–22 é artefato; a FEAM não tem data. Consequência: `Y_ilegal` ("sem autorização identificada") ≈ `Y_total` neste dado, e **o filtro de autorização não deve entrar no critério de parada** (a regra de ≥ 30% foi avaliada sem ele). Autorização só vale como filtro de 2023–24 em diante, e mesmo assim a cobertura é desconhecida (pedido de dados ao Sisema/IEF: `docs/pedidos/`).

### (d) Estabilidade da geometria do CAR
- **93,4% dos positivos têm `data_atualizacao` do CAR posterior a t₀** (por ano 92–94%). O polígono atual pode ter sido retificado depois do desmatamento, o que torna a elegibilidade e o "contido no polígono" otimistas ou enviesados em direção desconhecida.
- Dos 1.044 positivos, só **572 (54,8%)** estavam inscritos há ≥ 6 meses em t₀ (os demais foram criados depois do evento ou há menos de 6 meses): CARs criados após o desmate são viés de seleção do retrospectivo; não existiriam no painel real.
- O subconjunto de geometria estável tem só 62 positivos elegíveis; serve como sensibilidade, não como base de decisão.
- Não há como medir deriva sem versões antigas: **só os snapshots mensais de agora em diante resolvem** (`docs/dados/snapshots.md`).

### (e) O histórico já explica?
Entre os positivos elegíveis (n = 572): evento prévio **no imóvel** (qualquer tamanho, 3 anos): 32,5% (IC 26,0–38,6); **vizinhança** 1 km, ano y−1, sem o próprio imóvel: 32,5%; união: **46,7%**. A baseline "distância ao PRODES dos 3 anos anteriores" ranqueada sobre os CARs elegíveis tem recall@10% de 35,8–47,6% (todos os elegíveis) e **14,5 / 22,3 / 23,8 / 19,5%** (2021–24) entre CARs **sem evento prévio no imóvel**, contra 10% de acaso (lift 1,5–2,4). O critério primário (Δrecall@10% ≥ +5 pp sobre a baseline composta, sem evento prévio) parte, portanto, de um piso de ~20% de recall. Ressalva do revisor: o PRODES de y−1 termina em t₀ e só é publicado ~3–4 meses depois (regra 3 do CLAUDE.md): usar-o como preditor **infla** a baseline; no painel, o histórico deve usar até y−2 ou o t₀ deve ser deslocado para a data de publicação.

### (f) MCR 2-9: UC e embargo estadual
Segundo fontes secundárias, a Res. CMN 5.268/2025 reescreveu a Seção 9 do Cap. 2 do MCR; a atualização do MCR de 15/05/2026 veda crédito a imóveis total ou parcialmente em UC, com exceções (p. ex., anuência do gestor) ([MCR — impedimentos](https://www.gov.br/gestao/pt-br/assuntos/meu-imovel-rural/arquivos/manual-de-credito-rural_impedimentos-sociais-ambientais-e-climatico)); embargo por uso econômico de área desmatada ilegalmente já era vedado pela Res. 5.193/2024 ([Mattos Filho](https://www.mattosfilho.com.br/?p=111597)); a Res. 5.303/2026 adiou para 2027 as exigências ligadas ao PRODES ([Money Times](https://moneytimes.com.br/credito-rural-ambiental-resolucoes-do-cmn-sensoriamento-remoto-e-controversia-juridica-pads/)); há PDL 262/2026 no Senado para sustá-las ([Senado](https://www25.senado.leg.br/web/atividade/materias/-/materia/173713)). **Não verificado:** texto primário do item do MCR sobre embargo *estadual* (a camada Sisema tem 730 feições na vitrine) e o status da ação da CNA/do PDL. Para a vedação determinística, UC (estaduais + federais + municipais) e embargo Sisema entram na camada `vedacoes` como fatos com fonte e data, sem afirmar a leitura jurídica.

### (g) Eventos no recorte de treino
Contagem enxuta (`python -m agrorisk.gate_contagem --recorte treino`; `reports/07-gate/eventos_por_ano_treino.csv`). O gate completo (destino, autorização, histórico) rodou só na vitrine; no treino só se contam eventos (CAR×ano com ≥ 1 ha contíguo, geometria vigente, sem deduplicar sobreposições).

| Recorte | CARs (snapshot) | Positivos ≥ 1 ha 2021 / 2022 / 2023 / 2024 | Total |
|---|---|---|---|
| Vitrine (50 municípios) | 41.402 | 209 / 440 / 184 / 211 | **1.044** |
| Treino (136 municípios) | 119.649 | 1.352 / 1.978 / 1.246 / 1.129 | **5.705** (≈ 5,5× a vitrine) |

A sessão 01 reportou 205 / 438 / 178 / 212 (≈ 1.033 em 2021–24). A diferença (+11) vem de: snapshot do CAR 14 dias depois (+14 CARs), limiar de contiguidade (maior componente ≥ 1 ha, não soma de áreas) e dedupe por `cod_imovel`. **CARs sobrepostos contam o mesmo polígono PRODES mais de uma vez** (não deduplicado; limite superior).

### (h) Data de publicação do PRODES por ciclo
Não verificada para os polígonos. O campo `pub_date` do WFS é uniforme (recarga). Indícios secundários: a taxa do ciclo ago/2024–jul/2025 do Cerrado foi divulgada em 30/out/2025 (~3 meses). Mantida a regra do projeto de ≥ 4 meses (ver `licencas.md`). Taxa de estimativa ≠ polígonos consolidados.

## Bloqueios de rede e como o fundador baixa localmente
- **MapBiomas** (`storage.googleapis.com/mapbiomas-public`): 403 no proxy. Para a Cobertura/Transição Col. 11, o fundador baixa localmente pelo STAC (`https://storage.googleapis.com/mapbiomas-public/stac/catalog.json`) o recorte municipal do bbox e coloca em `data/raw/mapbiomas/<data>/`. Sem ela não há filtro de "≥ 1 ha de vegetação nativa em t₀" nem % nativa/tendência no painel (o gate usou PRODES + IBGE urbano como substitutos).
- **IBGE `servicodados.ibge.gov.br`**: túnel do proxy cai; usado o SIDRA (`apisidra.ibge.gov.br`), que funciona.
- **TerraBrasilis**: o handshake TLS do `curl` falha intermitentemente (erro 35); o downloader repete até 5 vezes. O treino (bbox grande) leva horas: se falhar, rodar localmente `python -m agrorisk.fontes.prodes --bbox <bbox do manifesto do snapshot de treino> --data <data>-treino`.

## Decisão pendente (para o fundador)
1. Aceitar o gate como **"passa com ressalvas"** e prosseguir com o painel (recomendado), ou reabrir o escopo por causa de (d) e do limiar no limite.
2. **Y primário proposto: `Y_total`** (PRODES ≥ 1 ha contíguo, 12 meses), reportando `Y_agro` e `Y_ilegal` como derivados. Motivo: Y_agro difere de Y_total em só 13% dos positivos e Y_ilegal é indistinguível de Y_total com a cobertura atual de autorização; nenhum dos dois derivados muda o critério. Está escrito como **proposta** em `docs/decisoes/0002-protocolo-y-gate.md`, **não congelada**: congelar (commit/hash) exige a confirmação do fundador.
3. Tratar o retrospectivo como **exploratório** e priorizar o acúmulo de snapshots (primeiro: 2026-11-03) para o teste prospectivo.

## Oportunidades de inovação para o AgroRisk
- **Evidência de que a vedação determinística cobre mais da metade do sinal** (47% dos positivos elegíveis já têm histórico no imóvel/vizinhança): o produto de verificação com trilha de auditoria é defensável; o preditivo precisa provar valor no restante (CARs sem evento prévio, onde a baseline de distância já dá ~20% de recall@10%, contra 10% de acaso). Fontes: este gate (`reports/07-gate/baseline_distancia_vitrine.csv`).
- **Snapshots próprios com hash** como ativo: ninguém publica versões datadas do CAR (ver [escopo-mvp §4](../decisoes/escopo-mvp.md)); em 2027 haverá o primeiro rótulo prospectivo limpo.
- **Estabilidade da geometria como variável de risco/qualidade** (93% dos positivos com CAR retificado depois de t₀): possível sinal de regularização ex-post — hipótese a testar com os snapshots, não conclusão.
- **Lacuna de autorização**: a cobertura temporal e espacial das camadas IEF/FEAM limita `Y_ilegal`; um acordo/LAI com a SEMAD/IEF por série histórica de autorizações teria valor direto para o comprador.

## Perguntas em aberto
1. O fundador aceita "passa com ressalvas" e o Y_total como primário (decisão 0002 proposta)?
2. Qual a data real de disponibilização dos polígonos PRODES por ciclo (para fixar t₀ e a defasagem)? Fonte candidata: INPE/TerraBrasilis, LAI.
3. Como obter a camada datada do CAR (LAI ao SFB) e séries de autorizações IEF/FEAM/embargos?
4. A retificação do CAR pós-t₀ é endógena ao desmate? Precisa dos snapshots para responder.
5. Como substituir o filtro de ≥ 1 ha de vegetação nativa sem MapBiomas na nuvem (download local pelo fundador)?
6. O texto primário do MCR 2-9 sobre embargo estadual e UC (leitura jurídica) — validar com a `especialista-credito-regulacao`/advogado.
