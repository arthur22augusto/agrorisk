# Perguntas do dev à estatística — respostas provisórias (v0)

- Data: 2026-10-29 · Status: **provisório**. As respostas marcadas *proposta* destravam o stub; a sessão 06 (escopo) e a sessão 06b (contrato do motor) as confirmam ou revisam.
- Origem: especificação do produto feita pelo dev (Django + PostgreSQL). **A especificação ainda não está no repositório**; quando chegar, deve ir para `docs/produto/`. Termos como Y1/Y2/Y3, gleba, faixas A–E, `exposicao_esperada` e `fonte_dados` vêm dela.
- Legenda: **[pesquisa]** = levantado nas sessões 01–05 · **[proposta]** = sugestão a confirmar.

## Antes da semana 3 (bloqueiam o dev)

1. **Chave contrato ↔ SICOR.** [pesquisa] Não há chave pública: a Matriz de Dados do Crédito Rural é agregada por município × produto × mês, sem CAR nem operação, e o município pode ser o da agência (`docs/pesquisa/05-credito-rural-e-outcome.md` §3.3). [proposta] A ligação vem da cooperativa: `id_externo` + referência da operação no SICOR + CAR + localização da gleba (que ela informa ao SICOR; confirmar no MCR). O SICOR público é só contexto municipal.
2. **Formato de saída.** [proposta] `p_y` float em [0,1] + `horizonte_meses`; `score` = `round(1000·(1−p))`; `faixa` por múltiplo da taxa-base (A ≤0,5×; B ≤1×; C ≤2×; D ≤4×; E >4×; stub com taxa-base 2%); `exposicao_esperada` = `p × saldo exposto` em R$ (é exposição, não perda); `detalhes` = lista de `{fator, valor, unidade, contribuicao, direcao, fonte, data_referencia, data_publicacao, texto}`.
3. **Entradas e dono.** [proposta] A estatística é dona do pipeline de dados públicos e entrega uma tabela de indicadores por imóvel/gleba × data de corte; o dev é dono da ingestão dos dados do cliente e do schema. O motor não lê dado bruto.
4. **Empacotamento.** [proposta] Python ≥3.11; pacote `agrorisk` instalável via `uv add git+https://github.com/arthur22augusto/agrorisk`; o núcleo de pontuação depende só de pandas, numpy e lightgbm; o geo pesado fica no extra `[pipeline]`; o modelo treinado fica fora do git, com caminho por variável de ambiente.
5. **Execução.** [proposta] Conexão própria (URL do banco por variável de ambiente); exceções tipadas + código de saída ≠ 0; upsert por `(operacao_id, data_corte, versao_modelo)`; `versao_modelo` = semver + hash do git; `versoes_dados` = JSON `{fonte: versão/data de publicação}`.

## Antes do piloto

6. **Y2 = Proagro.** [pesquisa] Não há dado público por operação, e cerca de 95% dos pagamentos são no PR/RS: o Y2 deve ser raríssimo em MG (05 §4–5). [proposta] Se mantido: unidade = operação de custeio no Proagro; evento = comunicação de perdas; horizonte = contratação → vencimento. A pesquisa sugere como desfecho principal o **atraso >90 dias ou a renegociação**.
7. **Fallback `imovel_inteiro`.** [proposta] Calcular igual, gravar `nivel_espacial` e avisar na tela; não reduzir p artificialmente; medir o desempenho separado no backtest.
8. **Backtest.** [pesquisa] Com dado público, só se valida o evento ambiental (supressão: 178–611 imóveis/ano na vitrine, 01 §6); "você vai perder menos" só se prova com a carteira histórica do cliente, no piloto. O CAR público não tem versões antigas (risco de vazamento).
9. **Y3.** [pesquisa] Colunas em 05 §5.3 (operação, CAR/gleba, datas, valores, status mensal de pagamento, renegociação, garantia, seguro/Proagro, **operações recusadas**). O dev faz o upload; a estatística define o schema e a validação; LGPD e sigilo bancário antes de receber.
10. **Licenças.** [pesquisa] MapBiomas, CHIRPS e Copernicus DEM: CC-BY ou equivalente, uso comercial sim. SICOR: ODbL (share-alike em base derivada, validar). INMET, PRODES (CC BY-SA), CAR e IDE-Sisema: incerto. Detalhes em `docs/pesquisa/licencas.md`.
11. **Dados sintéticos.** Ainda não existem; são gerados na sessão 06b.

## O que ainda falta pegar com o dev
Especificação completa; definição de Y1/Y2/Y3; models/DDL das tabelas; versão do Python/PostgreSQL/PostGIS e onde roda; como o motor é chamado (síncrono ou lote); formato do upload; o que as telas mostram dos fatores; calendário da "semana 3"; cliente em vista; confirmação de que o código é 100% do AgroRisk.
