# Perguntas do dev à estatística — respostas provisórias (v0)

- Data: 2026-10-29 · Status: perguntas 1–5 **provisórias** (a sessão 06b as confirma no contrato); perguntas **6–9 decididas na sessão 06** (`docs/decisoes/escopo-mvp.md`, aceita em 2026-10-29).
- Origem: especificação do produto feita pelo dev (Django + PostgreSQL). **A especificação ainda não está no repositório**; quando chegar, deve ir para `docs/produto/`. Termos como Y1/Y2/Y3, gleba, faixas A–E, `exposicao_esperada` e `fonte_dados` vêm dela.
- Legenda: **[pesquisa]** = levantado nas sessões 01–05 · **[proposta]** = sugestão a confirmar.

## Antes da semana 3 (bloqueiam o dev)

1. **Chave contrato ↔ SICOR.** [pesquisa] Não há chave pública: a Matriz de Dados do Crédito Rural é agregada por município × produto × mês, sem CAR nem operação, e o município pode ser o da agência (`docs/pesquisa/05-credito-rural-e-outcome.md` §3.3). [proposta] A ligação vem da cooperativa: `id_externo` + referência da operação no SICOR + CAR + localização da gleba (que ela informa ao SICOR; confirmar no MCR). O SICOR público é só contexto municipal.
2. **Formato de saída.** [proposta] `p_y` float em [0,1] + `horizonte_meses`; `score` = `round(1000·(1−p))`; `faixa` por múltiplo da taxa-base (A ≤0,5×; B ≤1×; C ≤2×; D ≤4×; E >4×; stub com taxa-base 2%); `exposicao_esperada` = `p × saldo exposto` em R$ (é exposição, não perda); `detalhes` = lista de `{fator, valor, unidade, contribuicao, direcao, fonte, data_referencia, data_publicacao, texto}`.
3. **Entradas e dono.** [proposta] A estatística é dona do pipeline de dados públicos e entrega uma tabela de indicadores por imóvel/gleba × data de corte; o dev é dono da ingestão dos dados do cliente e do schema. O motor não lê dado bruto.
4. **Empacotamento.** [proposta] Python ≥3.11; pacote `agrorisk` instalável via `uv add git+https://github.com/arthur22augusto/agrorisk`; o núcleo de pontuação depende só de pandas, numpy e lightgbm; o geo pesado fica no extra `[pipeline]`; o modelo treinado fica fora do git, com caminho por variável de ambiente.
5. **Execução.** [proposta] Conexão própria (URL do banco por variável de ambiente); exceções tipadas + código de saída ≠ 0; upsert por `(operacao_id, data_corte, versao_modelo)`; `versao_modelo` = semver + hash do git; `versoes_dados` = JSON `{fonte: versão/data de publicação}`.

## Antes do piloto

6. **Y2 = Proagro — DECIDIDO: retirado do MVP.** [pesquisa] Não há dado público por operação e cerca de 95% dos pagamentos são no PR/RS (05 §4–5). Fica apenas a coluna opcional `proagro_acionado` no upload. O Y econômico passa a ser o **Y3 (atraso > 90 dias ou renegociação)**, por operação, só no piloto com dado do cliente. Se algum dia Proagro voltar: unidade = operação de custeio, evento = comunicação de perdas, modelagem de sobrevivência discreta (hazard mensal, censura à direita), não menos de ~100 eventos.
7. **Fallback `imovel_inteiro` — DECIDIDO.** Calcular igual e gravar `nivel_espacial` (campo **obrigatório**: `poligono` ou `imovel_inteiro`). A semântica de p muda para P(evento em qualquer parte do imóvel) e cresce com a área; por isso as faixas A–E usam múltiplo da **taxa-base do nível**, a calibração e as métricas são por nível e a tela rotula "evento no imóvel". Não reduzir p artificialmente. `exposicao_esperada` só vale se o evento no imóvel afeta a operação.
8. **Backtest — DECIDIDO.** Com dado público valida-se só o evento ambiental (Y = supressão PRODES ≥ 1 ha por CAR em 12 meses; 178–611 imóveis/ano na vitrine, 01 §6), e o retrospectivo é **exploratório e otimista** (CAR público sem versões antigas). O teste limpo é **prospectivo**, com snapshot congelado e hash (avaliação 2027–28). "Você vai perder menos" só se prova com a carteira histórica do cliente (contrafactual, com operações recusadas), no piloto. Critério de sucesso: Δrecall@10% ≥ +5 pp contra a baseline composta, IC95% inferior > 0, em CARs sem evento prévio, pooled 2021–24.
9. **Y3 — DECIDIDO (schema e privacidade).** Painel operação × mês: `operacao_id` (pseudonimizado, hash com sal do cliente), CAR, gleba (geometria opcional), `porte_modulos_fiscais`, `programa` (Pronaf etc.), `data_contrato`, vencimento, valor, produto, saldo mensal, dias de atraso mensais, data da renegociação, garantia, seguro/Proagro, **recusas com data**. Validação: unicidade, datas monotônicas, formato do CAR, cobertura ≥ 36 meses antes do corte; data do registro e data do evento separadas (anti-vazamento); limiar mínimo ≥ 300 inadimplências > 90 dias antes de modelar. Privacidade: cooperativa controladora, AgroRisk operador; **nunca CPF/nome**; opção de processar no ambiente do cliente. Base legal e sigilo bancário (LGPD; LC 105/2001; Res. CMN 4.893/2021) **não verificados — validar com advogado antes de receber dados**. O schema chega antes do contrato.

### O que muda no desenho do dev (decisão 06)
- Unidade comercial = operação + CAR (+ gleba), com `porte_modulos_fiscais`, `programa` e `data_contrato`.
- Separar **vedação/verificação determinística** (filtro com fonte, `data_publicacao`, data de corte, hash) de **risco** (p). Vedação não é feature.
- `detalhes` ganha `status_juridico` ∈ {detectado, autorizado, sem_autorizacao_identificada, indeterminado}.
- `p_y` = P(Y_total em 12 meses), `data_corte` em 31/jul; declarar `y_definicao`.
- `exposicao_esperada` só após desfecho validado no piloto; antes, "exposição bloqueável" (saldo × bloqueio provável).
- Remover Y2/Proagro; trilha de auditoria de primeira classe (`versao_modelo`, `versoes_dados`).
- Detalhe e registro para a 06b em `docs/decisoes/escopo-mvp.md` ("Impacto no contrato do motor").

10. **Licenças.** [pesquisa] MapBiomas, CHIRPS e Copernicus DEM: CC-BY ou equivalente, uso comercial sim. SICOR: ODbL (share-alike em base derivada, validar). INMET, PRODES (CC BY-SA), CAR e IDE-Sisema: incerto. Detalhes em `docs/pesquisa/licencas.md`.
11. **Dados sintéticos.** Ainda não existem; são gerados na sessão 06b.

## O que ainda falta pegar com o dev
Especificação completa; definição de Y1/Y2/Y3; models/DDL das tabelas; versão do Python/PostgreSQL/PostGIS e onde roda; como o motor é chamado (síncrono ou lote); formato do upload; o que as telas mostram dos fatores; calendário da "semana 3"; cliente em vista; confirmação de que o código é 100% do AgroRisk.
