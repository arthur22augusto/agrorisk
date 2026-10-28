---
name: pptx
description: Planeja, cria, revisa e valida PowerPoints científicos e executivos em Python; questiona o objetivo do projeto, prioriza resultados nos cinco primeiros slides, inventaria análises e tabelas necessárias em XLSX e coordena o agente FN_revisao.
argument-hint: "[criar|planejar|revisar|validar|catalogar] [tema, contexto ou arquivo]"
---

# `/pptx` — narrativa de resultados, evidências e revisão crítica

Pedido do usuário: `$ARGUMENTS`

## Modos e proteção contra recursão

- `criar` (padrão): briefing → perguntas indispensáveis → plano narrativo e inventário → código Python → PPTX → validação técnica/prévia → `FN_revisao` → revisões priorizadas → entrega.
- `planejar`: briefing, perguntas, narrativa e catálogo de resultados; **não construir PPTX nem invocar agente**. Útil para aprovar a estratégia antes de produzir.
- `catalogar`: identificar todas as tabelas/estatísticas/comparações necessárias e exportar o inventário XLSX. Não construir slides nem invocar agente.
- `revisar <pptx>`: examinar apresentação existente, contexto e gaps, preparar QA e chamar `FN_revisao`. Não alterar o original sem pedido.
- `validar <pptx>`: **apenas** rodar `scripts/validate_pptx.py` e relatar problemas técnicos; não criar arquivos além do relatório JSON, não renderizar slides, não chamar agente e **não chamar `/pptx` outra vez**.
- Se não houver modo explícito, assumir `criar`. Se for invocada pelo agente com `validar`, obedecer ao modo estrito, independentemente do texto restante.

## Princípios obrigatórios

1. **Objetivo antes de visual.** Descobrir objetivo principal, tese central, público, decisão/inferência desejada, tipo de impacto e nível de evidência. Diferenciar o que o estudo *avalia*, o que *encontrou* e o que a audiência deve *concluir/fazer*.
2. **Perguntas quando realmente mudam a história.** Se o objetivo principal estiver ausente, contraditório, excessivamente amplo, ou se uma ambiguidade mudar a interpretação dos números, perguntar ao usuário **antes de fixar a narrativa**. Priorizar até 3 perguntas claras e acionáveis por rodada, começando pelo objetivo. Apresentar 1–2 alternativas de enquadramento se úteis. Esperar a resposta para bloqueios reais. Se não bloqueante, seguir com hipótese explicitada no `brief.md`, sem perguntas cosméticas.
3. **Inventário tabular completo.** Para *cada afirmação/contraste* que a narrativa exige, verificar se existe base ou resultado suficiente. Inventariar inclusive as tabelas ainda inexistentes em `data/resultados_manifest.json`, gerar `output/resultados_necessarios.xlsx` e indicar explicitamente as lacunas, sem inventar valores. O inventário é uma **especificação de análises**, não uma simulação de resultados.
4. **Python como fonte única.** Criar e editar o PPTX exclusivamente via código `.py` versionável dentro da pasta específica da apresentação, preferindo `python-pptx`, `matplotlib` e `Pillow`. Gerar gráficos/dados derivados por Python; não editar manualmente no PowerPoint, LibreOffice nem diretamente no XML. PowerPoint/LibreOffice podem ser usados **somente para renderização/exportação da prévia**.
5. **Escrever antes de executar.** Primeiro planejar (`brief.md`, `outline.md`, inventário), elaborar/revisar `src/build.py`, rodar `python -m py_compile` e somente então executar. Modificações sempre no código; regenerar o binário.
6. **Informação antes de ornamento.** Design limpo, 16:9, tons neutros, 1 cor principal e até 1 secundária coerente com o nicho (florestas = verde escuro; pecuária = terrosos etc.). Evitar fundos coloridos predominantes, excesso de palavras, texturas, imagens decorativas. Usar números grandes, tabelas simples, gráficos, mapas e figuras com evidência.
7. **Abstract visual.** Mensagem principal, principais resultados e implicação já nos cinco primeiros slides. Detalhes de métodos, bases, robustez e limites depois. Uma tese/ideia demonstrável por slide; não forçar 5 slides se o assunto pedir menos.
8. **Rigor e rastreabilidade.** Não inventar estimativas, comparadores, denominadores, fontes nem conclusões causais. Indicar população, datas, unidade, incerteza e desenho analítico necessários. Um resultado ausente deve virar lacuna/solicitação de dados, **nunca** número fictício.
9. **Revisão independente com voz ativa.** `FN_revisao` atua como pesquisador especialista + público decisor exigente. Deve questionar a tese, propor tabelas adicionais e priorizar mudanças substantivas, não só revisar design.
10. **Iteração consciente do custo.** No máximo **duas chamadas de `FN_revisao` por execução**: revisão inicial e segunda revisão **apenas** se ajustes P0/P1 alteraram objetivo, interpretações ou os primeiros 5 slides. Para evolução adicional, usar nova solicitação do usuário. Validação em Python é barata e pode ser repetida; revisão visual consolidada só após etapas de código. Nunca haver ciclo agente→skill→agente.

## Etapa A — Ler e pensar como pesquisador

Interpretar documento do projeto, resumos, dados e apresentações anteriores (quando fornecidos). Se o nicho exigir fatos externos atuais para julgar a tese, pesquisar **fontes confiáveis verificáveis** dentro das permissões disponíveis, discriminando literatura externa, achados do projeto e opinião editorial. Não procurar números externos como substitutos de dados ausentes.

Criar `brief.md` com:
- **Objetivo principal** expresso de forma específica; objetivo secundário, se houver; pergunta científica/de negócio; hipótese ou tese.
- Público e nível técnico; ocasião, duração, decisão desejada e impacto a comunicar; principais dúvidas do usuário respondidas/pendentes.
- Top 3 achados, unidades, comparações, fontes dos dados, períodos, limitações; qual grau de causalidade é sustentado.
- Mensagem que a audiência deve lembrar após 30 segundos; paleta temática; suposições provisórias.

**Portão do objetivo:** se você não consegue escrever com segurança "Esta apresentação pretende convencer [público] de que [tese baseada na evidência] para [decisão/consequência]", fazer perguntas antes de avançar. Exemplo: "Seu foco é demonstrar o efeito de uma política sobre desmatamento ou documentar mudanças de conformidade na cadeia? Isso define qual resultado abre a apresentação." Não formular hipóteses fortes a partir de lacunas.

## Etapa B — Inventariar os resultados necessários, mesmo os ausentes

Antes de definir os visuais, olhar o projeto como um artigo e listar *todas* as análises tabulares essenciais para sustentar a narrativa, inclusive:
- Estatísticas de magnitude, cobertura e denominadores (N, universo, período, percentuais e unidades).
- Comparações entre grupos, locais, períodos e tratamentos, incluindo baseline; comparador adequado; diferenças absolutas e relativas.
- Se houver antes/depois e controle/tratamento, solicitar tabela por grupo×período; desagregação e estimativas de efeito com incerteza **quando compatíveis com o método**.
- Séries temporais, distribuição, heterogeneidade, mapas/recortes, redes/fluxos; inferência/robustez/sensibilidade se pertinentes.
- Tabelas de limitações, cobertura, qualidade e casos excluídos quando influenciam a conclusão.
- Contraargumentos/explicações alternativas plausíveis que um pesquisador ou tomador de decisão levantaria.

Cada entrada do catálogo deve registrar: identificador, pergunta que responde, hipótese/claim, prioridade P0/P1/P2, status `disponivel|parcial|ausente|validar`, comparadores explícitos, variável/medida e unidade, período, população/denominador, dimensões e colunas esperadas, fonte e arquivo (ou `A DEFINIR`), transformação/cálculo planejado, slide de destino, risco da ausência, próxima ação. Não repetir dados desnecessários; **não inventar colunas existentes**: `colunas_esperadas` são especificações propostas. Registrar dependências e lacunas.

Salvar JSON em `data/resultados_manifest.json`, seguindo `references/resultados_schema.md` e `references/exemplo_manifest.json`; **a amostra é ilustrativa, nunca tratá-la como dado real do projeto**.

Gerar o workbook (incluindo análises ausentes) com:

```bash
python "${CLAUDE_SKILL_DIR}/scripts/build_results_catalog.py" "ppts/<slug>/data/resultados_manifest.json" --out "ppts/<slug>/output/resultados_necessarios.xlsx"
```

O Excel deve listar todas as análises identificadas, status, prioridade, desenho da comparação, origem e especificação. Não preencher estimativas desconhecidas, criar números artificiais ou substituir bases de dados reais por planilha de planejamento. Se o ambiente não permitir gerar XLSX, manter manifest + tabela Markdown e informar precisamente a limitação; não alegar arquivo criado.

**Política de dados faltantes:**
- Lacuna P0: torna inválida a conclusão/slide de abertura → perguntar ou interromper essa afirmação; pode construir versão parcial com ressalvas se o usuário permitir.
- Lacuna P1: enfraquece comparação importante → propor tabela e slide condicional; não apresentar estimativa desconhecida.
- Lacuna P2: reforço futuro → listar como backlog, não bloquear entrega.
- Se novos gaps forem detectados por `FN_revisao`, atualizar JSON e regenerar XLSX por Python. Não prometer novas análises como já realizadas.

## Etapa C — Roteiro como abstract visual

Construir `outline.md` com `slide | título conclusivo | o que a audiência aprenderá | evidência/ID do catálogo | visual | fonte | restrição`.

Padrão dos cinco primeiros slides **se as evidências existirem**:
1. Título com tese principal verificável, contexto mínimo.
2. Achado quantitativo mais importante (efeito, magnitude ou cobertura).
3. Comparação relevante / segundo resultado forte / análise crítica da tese.
4. Por que isso importa? Interpretação e impacto científico, econômico, ambiental ou de decisão (delimitar o que *não* se pode inferir).
5. Síntese executiva: 2–3 conclusões, principal ressalva, decisão/próximo passo.

Depois: contexto, dados, desenho metodológico, resultados adicionais, heterogeneidade, robustez e limites; anexos somente quando úteis. Nunca usar títulos "Resultados" quando se pode escrever o achado.

Consultar `references/editorial.md` para design e regras de densidade. Se existe material potencialmente decisivo mas ainda não calculado, fazer o *outline condicionado*: especificar qual tabela/resultado falta, sem fingir conclusão pronta.

## Etapa D — Estrutura da pasta

Criar apenas dentro de `ppts/<slug-do-projeto>/` (ou caminho indicado):

```text
ppts/<slug>/
├── brief.md
├── perguntas_pendentes.md
├── outline.md
├── src/
│   └── build.py                         # toda a criação/edição visual
├── data/
│   ├── resultados_manifest.json         # inventário editável de evidências
│   └── ...                              # dados locais, sem sobrescrever originais
├── assets/                              # mapas, imagens, fontes e gráficos
├── output/
│   ├── <slug>.pptx
│   └── resultados_necessarios.xlsx      # catálogo (não estimativas fabricadas)
└── qa/
    ├── validation.json
    ├── contact_sheet.png                # criado uma vez após QA técnico
    ├── preview.pdf                      # quando houver renderizador
    ├── review_packet.md                 # contexto condensado para o agente
    ├── feedback_fn_revisao_r1.md
    └── feedback_fn_revisao_r2.md        # somente se necessária
```

Em apresentação existente, nunca sobrescrever o original sem autorização; usar pasta de trabalho e script de reconstrução/edição Python.

## Etapa E — Implementar inteiramente em Python

Criar `src/build.py` legível, com funções por slide, constantes e paleta, dados carregados de fontes rastreáveis. Gerar PPTX com Python (preferir `python-pptx`). Se faltar evidência P0, evitar afirmação não sustentada e perguntar antes de consolidar o deck. Priorizar elementos editáveis, usando imagem só quando evidência visual justificar.

```bash
python -m py_compile "ppts/<slug>/src/build.py"
python "ppts/<slug>/src/build.py"
python "${CLAUDE_SKILL_DIR}/scripts/validate_pptx.py" "ppts/<slug>/output/<slug>.pptx" --out "ppts/<slug>/qa/validation.json"
```

Corrigir falhas técnicas via código **antes** da primeira renderização consolidada. Uma vez estável, rodar `scripts/render_preview.py` com `--outdir ppts/<slug>/qa/`. Se não renderizar, não afirmar avaliação visual. Evitar ler dezenas de imagens; gerar `contact_sheet.png`; ampliar 1–2 slides apenas quando necessário.

## Etapa F — Revisão de alto nível e diálogo

Criar `qa/review_packet.md`, com no máximo ~1–2 páginas, incluindo: objetivo e público, tese/decisão, top 3 achados e fontes, mapa de slides 1–5, IDs dos resultados usados/faltantes, questões já respondidas, limitações. Enviar ao **Agent** com `subagent_type: FN_revisao` e `run_in_background: false` (se suportado); passar caminhos de `brief.md`, `outline.md`, manifesto JSON, Excel, `.pptx`, `validation.json` e `contact_sheet.png`. Pedir explicitamente 2 lentes: **pesquisador especialista no nicho** + **gestor/investidor/decisor a convencer**, sem confundir rigor com marketing.

O agente deve devolver de maneira estruturada: parecer com veredito, P0/P1/P2, perguntas úteis ao usuário, afirmações sem evidência, novas análises/tabulações necessárias (incluindo esquema de colunas), recomendações por slide e próxima iteração, priorizando até 5 alterações de alto impacto. **O agente não cria nem edita a apresentação nem conversa diretamente com usuário**: devolve as questões para a conversa principal perguntar.

Após primeira revisão:
1. Registrar o feedback em `qa/feedback_fn_revisao_r1.md`.
2. Se houver perguntas bloqueantes, apresentá-las claramente ao usuário e aguardar resposta **quando necessária para não inventar uma tese/dado**; salvar perguntas e estado. Não gastar segunda revisão antes da resposta.
3. Corrigir em Python as falhas solucionáveis sem esclarecimento; atualizar `brief.md`, `outline.md`, manifesto e XLSX quando nova necessidade tabular for identificada.
4. Segunda chamada ao agente **somente se** houver alteração substantiva de tese, resultado-chave ou narrativa dos primeiros cinco slides, com **resumo do delta**, não reencaminhar projeto inteiro. Registrar `qa/feedback_fn_revisao_r2.md`. Não repetir uma terceira vez automaticamente.
5. O agente, **ao concluir cada parecer**, deve acionar `/pptx validar <arquivo>` através da ferramenta Skill quando disponível, sem reinvocar o agente. Se a ferramenta não existir, relatar a limitação; a conversa principal já executa o validador diretamente.

O agente pode recomendar que o estudo/ppt não está pronto para afirmações ambiciosas. Essa discordância deve ser transmitida ao usuário, não suprimida para agradar.

## Etapa G — Entrega e continuidade

Entregar: `.pptx` se criado; `src/build.py`; `resultados_necessarios.xlsx`; resumo de evidências disponíveis/ausentes; perguntas abertas; revisão do agente (ou pendência se ele não pôde executar); mudanças feitas e próximos passos. Distinga "correções aplicadas" de "análises ainda necessárias". Se a execução for apenas `planejar`/`catalogar`, entregar os artefatos pertinentes, não declarar PPT pronto.

O modo `revisar` deve evitar reescrever o PPT sem pedido. O modo `validar` permanece estrito e barato, sem análise visual, sem perguntas ao usuário e sem chamada de agente.
