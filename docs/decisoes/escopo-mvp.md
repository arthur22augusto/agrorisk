# escopo-mvp — Espaço de mercado, Y, recorte, métricas e critério de sucesso do MVP

- Data: 2026-10-29
- Status: **aceita** (escolhas do fundador na sessão 06, após a síntese da rodada 3; o Y é **provisório até o gate da sessão 07**, ver §Decisão 3)
- Decisores: fundador (escolheu entre as opções da matriz), com o debate de especialistas da sessão 06
- Detalhes do debate, matriz e pesquisa nova: `docs/pesquisa/06-debate-escopo.md`

## Contexto
A decisão 0001 deixou em aberto o Y e o espaço de mercado. As pesquisas 01–05 trouxeram achados que
contrariam a tese original (Proagro raro em MG e sem dado por operação; sem desfecho econômico público por
imóvel; cooperativa compradora com riscos — Sicredi constrói em casa, SeloVerde MG gratuito, comprador
simulado "piloto grátis"; rótulo de supressão instável, PRODES × MapBiomas com correlação anual −0,37; CAR público
sem versões antigas). A sessão 06 comparou a **frente A** (crédito rural reposicionado, pós-concessão) e a
**frente B** (fornecedores de carvão vegetal/siderurgia, hipótese não verificada), com propostas de quatro
especialistas, ataque do advogado do diabo e do comprador cético (duas personas) e síntese.

## Opções consideradas (resumo; matriz completa em `docs/pesquisa/06-debate-escopo.md`)
Pesos: valor para o cliente 20, nº de eventos/poder 15, dados e licenças 10, risco de vazamento 10,
diferenciação 15, esforço até a demo 15, compatibilidade com o dev 15. Notas 1–5 são julgamento da sessão, não medição.

| Opção | Nota ponderada (máx. 5) | Leitura |
|---|---|---|
| **A-reformulada** (filtro determinístico MCR + priorização; B só como discovery) | **3,35** | escolhida |
| A-original (score + Y2/Y3 do desenho do dev) | 3,00 | Y2 inviável; vende "IA" por algo que é filtro geográfico |
| A+B, mesmo motor | 2,50 | dobra o custo de descoberta; unidade, Y e cliente de B diferem |
| B principal (carvão) | 2,20 | sem cadeia fornecedor→usina em dado público; Y relevante é documental |

## Decisão

### 1. Frente e produto
- **Frente principal: A-reformulada.** O produto tem duas camadas, separadas na interface, no dado e na venda:
  1. **Vedação/verificação determinística** (sobreposição supressão detectada × autorização, embargo, UC, CAR), com fonte,
     data de publicação, data de corte e hash — "evidência pronta" para o BCB/auditoria e antecipação do PRODES no MCR
     (Res. CMN 5.268/2025 adiada pela 5.303/2026: >15 MF em 04/01/2027; 4–15 MF em 01/07/2027; ≤4 MF em 03/01/2028 —
     fontes secundárias, **não verificado no texto do BCB**).
  2. **Risco preditivo** P(supressão em 12 meses), usado para priorizar (renovação, nova concessão, antecipação para ≤4 MF) e
     provado por backtest **contra a regra determinística e contra baselines**.
- **Comprador-alvo para discovery:** central de cooperativas de crédito de MG (Sicoob Cecremge, Crediminas, Sicoob Central MG);
  SeloVerde MG/Semad tratado como parceiro/regulador, não como cliente. Proposta de piloto: **90 dias, gratuito, até ~500 CARs
  (valor sugerido, não verificado)**, snapshot congelado com hash, avaliação prospectiva. Preço e disposição a pagar: **não verificados**.
- **Frente B:** **somente discovery** (3 entrevistas: Sindifer-MG, SDS Siderúrgica, Vallourec Florestal/Siderurgia Sustentável;
  Aperam BioEnergia opcional), **sem código**. Condição para voltar a considerar B: confirmar a fração de carvão de terceiros,
  a dor contratual (exportação/CBAM) e acesso à lista de fornecedores (dossiê por fornecedor, não probabilidade).
- **Hídrico e mineração:** entram como **fatores/contexto** de A, nunca como Y. Mineração e área urbana servem de
  **estratificador de causa** (Y_agro × Y_nao_agro). Outorga/escassez hídrica fica como fator de crédito a testar no piloto.
- **Fora do MVP:** Proagro (Y2) e Y econômico público. Embargo/auto estadual como Y secundário descritivo, sem critério de passa/não passa
  (poucos eventos; viés de fiscalização).

### 2. Y operacional
- **Evento previsto (Y_total):** supressão de vegetação nativa **≥ 1 ha contíguo dentro do polígono do CAR**, rótulo **PRODES**
  (Cerrado + Mata Atlântica), no ciclo ago–jul seguinte a t₀. **Não unir nem intersectar PRODES com MapBiomas**; MapBiomas (Col. 11) e
  Alerta (se houver token) entram só como análise de sensibilidade, com o mesmo backtest.
- **Derivados (reportar sempre):** `Y_ilegal` = Y_total sem autorização identificada (IEF e FEAM, janela ±12 meses; é "sem autorização
  identificada", **não** "ilegal"); `Y_agro` = destino não mineração/urbano (via SIGMINE/matriz de transição MapBiomas). O modelo prevê
  Y_total; o contrato do motor deve declarar isso.
- **Supressão autorizada:** variável explicativa/diagnóstico e exclusão do Y_ilegal, não exclusão do treino.
- **Y econômico:** apenas no piloto, com dado do cliente (**Y3** = atraso > 90 dias ou renegociação, por operação). Pré-requisitos:
  ≥ 300 inadimplências > 90 dias, operações recusadas, cobertura ≥ 36 meses. Hipótese, não critério: OR > 1 com IC reportado.

### 3. Gate do Y (sessão 07, antes de qualquer modelo)
Executar primeiro, ~5–8 h: (a) fração dos eventos em imóveis ≤ 4 MF (campo `mod_fiscal` do espelho do CAR); (b) fração em mineração/urbano;
(c) fração com autorização IEF/FEAM; (d) teste de estabilidade da geometria do CAR (área/nativa antes × depois de eventos, via `dat_atuali`);
(e) teste "a regra determinística já era óbvia": fração dos flags de t+12 que já estava em evento prévio ou vizinhança em t₀; (f) leitura do MCR 2-9
sobre UC e embargo estadual. **Regra de decisão:** se menos de ~30% dos positivos restarem como Y_agro_sem_autorização em ≤ 4 MF, ou se
(e) mostrar que o histórico explica quase tudo, **reabrir este escopo** (hipótese alternativa: o filtro determinístico basta; o valor migra para prescrição ou para B).
O Y primário da avaliação (Y_total ou o derivado) é escolhido **pelo resultado do gate e registrado no protocolo antes de rodar o modelo**.

### 4. Unidade, janelas, defasagem e CAR sem histórico
- **Unidade de modelagem:** CAR × t₀. **Inclusão:** inscrito há ≥ 6 meses de t₀, com ≥ 1 ha de vegetação nativa em t₀ (condição só no passado);
  **cancelados permanecem** no denominador. **Unidade comercial:** operação + CAR (+ gleba quando houver), com porte em módulos fiscais.
  Reportar por porte (≤ 4 MF, 4–15, > 15).
- **t₀ = 31/jul** de cada ano (alinhado ao ciclo PRODES); **h = 12 meses** (principal), 24 meses apenas secundário descritivo.
- **Defasagem:** a data de publicação do PRODES por ciclo é **não verificada**; assumir ≥ 4 meses após o fim do ciclo até verificar, e registrar em
  `docs/pesquisa/licencas.md`/dicionário. MapBiomas: só a coleção vigente em t₀ (reprocessa a série; 8–10 meses de defasagem).
- **CAR sem histórico:** (i) o retrospectivo sobre o CAR público atual é **exploratório e otimista** e deve ser rotulado assim; (ii) painel
  principal com imóveis criados e não atualizados depois de t₀ (`dat_criaca`, `dat_atuali` ≤ t₀), mais análise separada dos demais;
  (iii) **snapshots próprios do CAR e da IDE-Sisema, mensais, com hash, a partir de agora** (~1 h de script; sem snapshot datado público encontrado);
  (iv) LAI ao SFB pedindo a camada datada; (v) o rótulo "limpo" é **prospectivo** (snapshot congelado em 2026, avaliação 2027–28).

### 5. Recorte e eventos esperados
- **Vitrine:** RMBH + Colar + Sete Lagoas (50 municípios; 40.997 CARs no snapshot atual). Eventos PRODES ≥ 1 ha (01 §6): 178–611 imóveis/ano
  (2021–2025: 205, 438, 178, 212, 196); anos-PRODES de teste 2021–2024 somam ≈ 1.033 positivos (geometria atual do CAR, sem deduplicar sobreposições; limite superior). A rodada 1 citou 1.024 por somar 2022–2025; usar 1.033 até a sessão 07 recalcular com a convenção t₀ → ciclo ago–jul.
- **Treino:** vitrine + mesorregião Metropolitana de BH + Central Mineira (Sete Lagoas inclusa); nº de eventos do recorte ampliado
  **não quantificado** — quantificar na sessão 07 repetindo o cálculo de poder. Estimativas de poder são da sessão (não medições).

### 6. Baselines, métricas e critério de sucesso
- **Baselines pré-registradas:** (1) evento anterior no imóvel; (2) taxa do município; (3) distância/proximidade a evento recente (12–24 meses);
  (4) logística com área nativa, área total e fração nativa; **baseline composta** = logística com histórico + vizinhança + município + área nativa.
  Teste de redundância: ajustar só distância a evento + área nativa + município; se o AUC-PR ficar a < ~10% do modelo completo, o modelo é redundante.
- **Validação:** rolling origin com t₀ de teste 2021–2024, purga de 12 meses, blocos espaciais (~10 km ou município) para CV e bootstrap;
  calibração em janela separada, em 5 faixas (decis inviáveis).
- **Critério de sucesso — primário único, pré-registrado:** **Δrecall@10% ≥ +5 pp contra a baseline composta, com limite inferior do IC95% > 0**
  (bootstrap em blocos espaciais), **somente em CARs sem evento prévio**, **pooled 2021–2024**, para o Y primário definido no gate. O protocolo é
  congelado (commit/hash em `docs/decisoes/`) antes da sessão 08.
- **Secundárias (reportar, sem passa/não passa):** lift@5% e @10% (incluindo a meta do estatístico, lift@10% ≥ 3 com IC inferior > 2),
  AUC-PR, precision@k, Brier, inclinação de calibração, resultados por ano, por porte, por Y (total/ilegal/agro), por rótulo (PRODES × MapBiomas),
  por `nivel_espacial`. Poder: o lift mínimo detectável por ano isolado é grande (≈ 13 pp de recall só em 2024, estimativa); por isso o primário é pooled.
- **Se não passar:** registrar "o filtro determinístico basta" em nova decisão em `docs/decisoes/` e redirecionar (prescrição, B ou piloto de dados do cliente).
  Resultado negativo é resultado válido.

### 7. Customer discovery (2–3 alvos por frente)
- **A:** Sicoob Cecremge, Crediminas, Sicoob Central MG (+ SeloVerde MG/Semad como interlocutor). Perguntas-chave: o que o auditor/BCB pediu em 2025–26 sobre
  PRODES; quem faz a checagem hoje e em quanto tempo; quanto custa um falso positivo; já cruzam embargo estadual e UC; dá para compartilhar atraso > 90 dias
  pseudonimizado; quem assina e em qual ciclo; o que fariam em casa (QGIS) versus comprar.
- **B (só discovery):** Sindifer-MG, SDS Siderúrgica, Vallourec Florestal/Siderurgia Sustentável (Aperam BioEnergia opcional). Perguntas-chave: fração de carvão
  de terceiros e nº de fornecedores; como verificam origem hoje (documentos, visita, Cerflor/FSC); já foram notificados/autuados; clientes exportadores exigem
  rastreabilidade (CBAM/EUDR); custo de uma auditoria de campo; quem é o dono do orçamento; o resultado poderia ser usado contra a empresa?
- **Demonstração mínima que a persona do comprador pediu** (sessão 10): PDF de 2 páginas com os 20 CARs de maior risco (mapa e motivo), backtest 2021–24 vs. baselines
  com IC e falsos positivos, tabela "determinístico × predição", parágrafo de LGPD/responsabilidade e proposta de piloto de 90 dias.

## Respostas definitivas às perguntas 6–9 do dev (detalhe em `docs/produto/perguntas-dev-v0.md`)
- **6 (Y2 = Proagro): retirado do MVP.** Coluna opcional `proagro_acionado` no upload. Y econômico = Y3 no piloto.
- **7 (fallback `imovel_inteiro`):** calcular, gravar `nivel_espacial` (obrigatório), faixas por múltiplo da taxa-base **do nível**, métricas por nível, rótulo
  "evento no imóvel" na tela; a semântica de p muda e cresce com a área.
- **8 (backtest):** público = só o evento ambiental, **exploratório**; o teste limpo é prospectivo (snapshot congelado); "perder menos" só se prova com a carteira do cliente, com contrafactual e operações recusadas.
- **9 (Y3, schema):** painel operação × mês com colunas definidas no arquivo de perguntas; cooperativa controladora, AgroRisk operador; pseudonimização (hash com sal do cliente), sem CPF/nome; arquitetura opcional de processamento no ambiente do cliente. **Validar com advogado** (LGPD, LC 105/2001, Res. CMN 4.893/2021 — não verificados).

## Impacto no contrato do motor
(Registro para a sessão 06b; `docs/produto/contrato-motor-v0.md` e `src/` **não foram editados** aqui.)
1. `p_y` = P(Y_total em 12 meses); declarar `y_definicao` (Y_total/Y_ilegal/Y_agro), `horizonte_meses = 12` e `data_corte` em 31/jul; `faixa` por múltiplo da taxa-base do `nivel_espacial`.
2. Separar **vedações/verificações determinísticas** (filtro com fonte, `data_publicacao`, hash) de **risco** (p); vedação não é feature.
3. `detalhes` ganha `status_juridico` ∈ {detectado, autorizado, sem_autorizacao_identificada, indeterminado}.
4. Unidade: operação + CAR (+ gleba); campos `porte_modulos_fiscais`, `programa` (Pronaf etc.), `data_contrato`; `nivel_espacial` obrigatório.
5. `exposicao_esperada` só após desfecho validado no piloto; antes, expor **"exposição bloqueável"** (saldo × bloqueio provável), mecânica.
6. Remover Y2/Proagro; Y3 como entrada opcional do piloto (rótulo), não saída do motor.
7. Trilha de auditoria de primeira classe: `versao_modelo`, `versoes_dados`, data de corte, fonte, `data_publicacao`, hash do snapshot.
8. LGPD: entradas pseudonimizadas; nenhuma coluna de CPF/nome; armazenar só o necessário.

## Consequências
- **Muda no desenho do dev:** tabelas ganham porte, programa, `nivel_espacial`, `status_juridico` e tabela/serviço de vedações determinísticas; telas separam "vedação" de "risco"; some a tela/coluna do Y2.
- **Prompts 07–10 e CLAUDE.md** foram ajustados a este escopo (gate na 07, pré-registro na 08, regra determinística como baseline na 09, demo de 2 páginas na 10).
- **Riscos assumidos:** (1) nenhum comprador pagante verificado — o piloto é grátis; (2) o retrospectivo é otimista pela geometria do CAR; (3) a regra do MCR pode ser derrubada ou adiada de novo (ação da CNA no STF); (4) o score pode ser percebido como "filtro geográfico vendido como IA" — por isso a camada determinística vem primeiro;
  (5) risco ético/LGPD de rankear pequenos produtores — uso como priorização de revisão, nunca como negativa automática.
- **Como reverter:** nova decisão que substitua esta (ex.: se o gate reprovar o Y, ou se o discovery de B confirmar fração de terceiros e acesso a fornecedores).

## Não verificado (pendências herdadas)
Texto primário da Res. 5.303 e do MCR 2-9 (UC, embargo estadual); data de publicação do PRODES por ciclo; licença do CAR/IDE-Sisema/SIGMINE; status da ação da CNA no STF;
preço e disposição a pagar de qualquer nicho; fração de carvão de terceiros; vigência do PRSAC para S4/S5 (Res. 5.194/2024).
