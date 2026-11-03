# CLAUDE.md — AgroRisk

Contexto permanente para qualquer sessão do Claude Code neste repositório. Leia antes de agir.

## 1. O que é o AgroRisk

Empresa nascente de **inteligência de risco socioambiental para o mercado rural** (B2B).
Tese: *transformar sustentabilidade em valor econômico mensurável* com estatística,
geoprocessamento, redes e otimização sobre bases públicas (e, depois, dados privados de clientes).

- Fonte principal de contexto: `docs/AgroRisk_proposta_v2.pdf` (versão final da proposta).
  `docs/historico/` guarda versões antigas — não usar como referência.
- Cadeia de valor: **Consulta → Diagnóstico → Predição → Prescrição**.
- O próprio documento conclui que consulta de CAR/score socioambiental já é commodity
  (Agrotools, Serasa Experian Agro, Demeter, Agro Brasil + Sustentável, JBS/Cowbot, Terras/CARMap).
  O *wedge* é: **predição validada historicamente + prescrição sob orçamento + ligação com outcome
  econômico + transparência metodológica**.

## 2. Recorte inicial (decisão 0001)

- **Vitrine:** Minas Gerais — Região Metropolitana de Belo Horizonte (34 municípios)
  + Colar Metropolitano + Sete Lagoas. Lista oficial a ser fixada na sessão 01.
- **Treino/validação:** pode (e provavelmente deve) usar um recorte maior de MG para ter
  eventos suficientes. A vitrine continua sendo a RMBH + Colar + Sete Lagoas.
- Particularidades: transição Cerrado/Mata Atlântica; desmatamento em larga escala é raro.
  Pressões: expansão urbana e loteamentos, mineração (Quadrilátero Ferrífero) e barragens,
  eucalipto, pecuária, cinturão verde (hortaliças), carste de Lagoa Santa/Sete Lagoas
  (cavernas, recarga), escassez hídrica e conflitos de outorga.
- **Frente e cliente (decisão `docs/decisoes/escopo-mvp.md`, aceita em 2026-10-29):** frente **A-reformulada** —
  crédito rural pós-concessão, vendido a **centrais de cooperativas de crédito de MG** (discovery: Sicoob Cecremge,
  Crediminas, Sicoob Central MG; SeloVerde MG/Semad como interlocutor). O produto tem duas camadas: **vedação/verificação
  determinística** (supressão × autorização, embargo, UC, com trilha de auditoria) e **risco preditivo** para priorizar,
  provado *contra* a regra determinística. **Frente B** (carvão/siderurgia, Sete Lagoas) é **só discovery** (3 entrevistas, sem código).
  Hídrico e mineração entram como fatores/contexto, nunca como Y. Nenhum comprador pagante verificado: o piloto é grátis.
- **Y (provisório até o gate da sessão 07):** supressão de vegetação nativa ≥ 1 ha contíguo no polígono do CAR, rótulo PRODES,
  ciclo ago–jul, h = 12 meses, t₀ = 31/jul (`Y_total` previsto; `Y_ilegal` = sem autorização identificada e `Y_agro` = fora de
  mineração/urbano como derivados). PRODES e MapBiomas **não** se unem. Y econômico (Y3 = atraso > 90 dias/renegociação) só no
  piloto com dado do cliente; Proagro (Y2) fora do MVP.
- **Unidade:** CAR × t₀ (inscrito há ≥ 6 meses, ≥ 1 ha de nativa); unidade comercial = operação + CAR.
- **Treino:** vitrine + mesorregião Metropolitana de BH + Central Mineira.

## 3. Hipótese de MVP (hipótese, não verdade)

Priorização de carteira pós-concessão: dada uma lista de CARs, aplicar a verificação determinística e estimar
P(supressão em 12 meses) usando **somente informação disponível antes da data de corte**, ranquear, explicar os fatores e provar por
**backtest temporal** que o ranking antecipa eventos **além da regra determinística e das baselines**.
**Critério de sucesso (primário único, pré-registrado):** Δrecall@10% ≥ +5 pp contra a baseline composta, IC95% inferior > 0, em CARs
sem evento prévio, pooled 2021–24 (bootstrap em blocos espaciais). Se não passar, a conclusão honesta é "o filtro determinístico basta".
O retrospectivo com o CAR público é **exploratório** (sem versões antigas); o teste limpo é prospectivo, com snapshots próprios com hash.
Depois, prescrever onde agir sob orçamento. Toda sessão deve tratar isso com ceticismo e registrar evidências contra ou a favor.

## 4. Regras inegociáveis

1. **Separação dos fundadores:** nenhum código, dado, metodologia, nomenclatura ou documento de
   empregos, pesquisas ou instituições dos fundadores entra aqui. Na dúvida, pergunte.
2. **Licença primeiro:** toda base usada precisa de uma linha em `docs/pesquisa/licencas.md`
   (fonte, URL, licença/termos, se permite uso comercial, atribuição exigida, data de verificação).
   "Público" não quer dizer "uso comercial livre".
3. **Sem vazamento temporal:** variáveis explicativas só podem usar dados com data de
   *publicação* (não só de referência) anterior ao corte. Registre a defasagem de cada fonte.
4. **Dados brutos fora do git:** tudo em `data/` é ignorado, exceto READMEs e `.gitkeep`.
   Commite scripts que baixam os dados, nunca os dados.
5. **Não invente números.** Se um valor não foi verificado, escreva "não verificado" e a fonte
   candidata. Toda afirmação factual em `docs/pesquisa/` tem link.
6. **Idioma:** tudo em português (docs, commits, comentários). Identificadores de código podem
   ficar em português sem acento (`area_ha`, `data_corte`).

## 5. Convenções técnicas

- **Python 3.11+** (R só com ganho claro e justificado em `docs/decisoes/`).
- Stack do MVP: GeoPandas/Shapely, DuckDB (+ extensão spatial), GeoParquet, rasterio/rioxarray,
  scikit-learn/LightGBM, statsmodels. Destino futuro: PostgreSQL/PostGIS.
- **CRS:** armazenar em SIRGAS 2000 geográfico (EPSG:4674). Para área e distância, usar uma
  projeção de área igual (Albers do IBGE para o Brasil, ou SIRGAS 2000 / UTM 23S — EPSG:31983 —
  dentro da RMBH). Declare a escolha no script.
- Camadas de dados: `data/raw` (como baixado, imutável) → `data/interim` (limpo/padronizado)
  → `data/processed` (tabelas de modelagem). Cada script declara o que consome e o que produz.
- Código reutilizável em `src/agrorisk/`; exploração em `notebooks/` (numerados,
  `NN-descricao.ipynb`); entregáveis em `reports/`.
- Sementes fixas, versões de pacotes registradas, datas de download registradas.

## 6. Onde registrar cada coisa

| O quê | Onde |
|---|---|
| Decisão (escopo, Y, método, ferramenta) | `docs/decisoes/NNNN-titulo.md` (contexto, opções, decisão, consequências) |
| Pesquisa, fontes, achados | `docs/pesquisa/NN-tema.md` |
| Licença de cada base | `docs/pesquisa/licencas.md` |
| Prompts das próximas sessões | `docs/prompts/NN-nome.md` |
| Guia para o fundador | `docs/GUIA.md` |

Toda pesquisa termina com a seção **"Oportunidades de inovação para o AgroRisk"**, com
evidências e fontes linkadas, e com **"Perguntas em aberto"**.

## 7. Agentes e skills do projeto

Agentes do domínio (`.claude/agents/`): `analista-mercado`, `engenheiro-dados-geo`,
`pesquisador-academico`, `especialista-credito-regulacao`, `estatistico-modelagem`,
`comprador-cetico`, `advogado-do-diabo`. Utilitários: `token-efficient` (tarefas pequenas) e
`FN_revisao` (revisão crítica de apresentações, usado pela skill `/pptx`).

Skills (`.claude/skills/`): `data-pipeline`, `pipeline-graph`, `postgresql`, `r-data-analysis`,
`revisao-codigo`, `documentation`, `git-workflow`, `pptx`, `token-efficient`.
Ao usar `data-pipeline`/`r-data-analysis`, aplique a estrutura de pastas da seção 5
(`data/raw|interim|processed`, `reports/`) no lugar de `input/intermediate/output`.

## 8. Como trabalhar em cada sessão

- Comece lendo este arquivo e o prompt da sessão em `docs/prompts/`. Leia só o necessário.
- Use subagentes quando houver frentes independentes (pesquisa em paralelo); não para tarefas
  simples.
- Trabalhe na branch indicada pela sessão; um PR por sessão; commits pequenos em português.
- Antes de terminar: atualize os docs afetados, registre decisões e liste próximos passos no PR.
- Eficiência: o crédito de nuvem é limitado. Exploração mínima suficiente, mas **corretude vem
  antes de economia**.
