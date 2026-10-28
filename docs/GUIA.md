# GUIA — Como trabalhar com o Claude Code na nuvem no AgroRisk

Guia prático para o fundador. Leitura: ~10 min. Atualize-o sempre que aprender algo novo.

---

## 1. Modelo mental (leia primeiro)

- Cada **sessão na nuvem** é um computador temporário (contêiner) com uma cópia nova do repositório.
  Quando a sessão termina ou fica ociosa, **o contêiner é apagado**. O que não foi *commitado e
  enviado (push)* se perde.
- Cada sessão trabalha numa **branch própria** e termina num **pull request (PR)**. Você revisa e
  mescla na `main`. A próxima sessão parte da `main` atualizada.
- A "memória" do projeto mora em arquivos versionados: `CLAUDE.md` (regras e contexto, lido em toda
  sessão), `docs/decisoes/`, `docs/pesquisa/` e `docs/prompts/`. Se não está escrito no repositório,
  a próxima sessão não sabe.
- **Dados não vão para o git.** Cada sessão que precisar de dados vai baixá-los de novo (ou você roda
  localmente). Por isso os scripts de download precisam ser idempotentes.

## 2. Iniciar uma sessão

1. Acesse **claude.ai/code** (ou o app do Claude → Code).
2. Escolha o repositório `arthur22augusto/agrorisk` e o **ambiente** (environment) configurado.
3. Escolha o modelo (ver seção 3) e cole o prompt da sessão, que está em `docs/prompts/NN-*.md`
   (copie o texto **abaixo da linha `---`**).
4. Acompanhe. Você pode interromper, corrigir o rumo ou responder perguntas a qualquer momento.
5. No fim, a sessão faz commit, push e abre um PR. Revise (seção 6).

Dica: dê à sessão um título igual ao do prompt ("01 — Território") para achá-la depois.

## 3. Modelos: opusplan e modo de planejamento

- **opusplan** = o Opus pensa e planeja (no modo de planejamento) e o Sonnet executa. Bom equilíbrio
  entre qualidade e custo. Selecione com `/model` → `opusplan`.
- **Modo de planejamento** (*plan mode*): o Claude só lê e pesquisa, propõe um plano e **espera sua
  aprovação** antes de editar qualquer coisa. Use em sessões com decisão ou código (06–10).
  Ative pelo seletor de modo na caixa de mensagem (no terminal: `Shift+Tab` até aparecer "plan mode").
- Quando usar Opus puro (`/model opus`): debate de escopo (06) ou revisão metodológica difícil. Custa mais.
- Quando usar Sonnet puro: tarefas mecânicas (formatar, renomear, pequenos ajustes).

## 4. Agentes e skills deste repositório

- **Subagentes** (`.claude/agents/`) são "especialistas" que a sessão principal chama para tarefas
  isoladas, cada um com o seu próprio contexto. Peça explicitamente: *"use o agente
  `analista-mercado` para…"*. Eles podem rodar em paralelo dentro da mesma sessão.
  Liste-os com `/agents`.
- **Skills** (`.claude/skills/`) são procedimentos prontos (ex.: `/pptx`, `revisao-codigo`,
  `data-pipeline`). Invoque com `/nome` ou peça "use a skill X".
- Agentes do AgroRisk: `analista-mercado`, `engenheiro-dados-geo`, `pesquisador-academico`,
  `especialista-credito-regulacao`, `estatistico-modelagem`, `comprador-cetico`, `advogado-do-diabo`
  (+ `token-efficient` e `FN_revisao`, utilitários).

## 5. Rodar sessões em paralelo

- Abra várias sessões ao mesmo tempo (uma aba por sessão); cada uma ganha a sua própria branch.
- **Regra de ouro:** sessões paralelas devem escrever em **arquivos diferentes**. Os prompts 01–05
  já foram desenhados assim (só a 02 edita `licencas.md`).
- Se dois PRs mexerem no mesmo arquivo, mescle um e peça na outra sessão: *"traga a main para a
  sua branch e resolva o conflito"*.
- A ordem e o paralelismo de todas as sessões estão em `docs/prompts/README.md`.

## 6. Revisar e mesclar pull requests

1. No GitHub, abra o PR → aba **Files changed**. Leia o resumo do PR primeiro.
2. Para pesquisa: confira 3–5 links aleatórios (os números batem com a fonte?). Desconfie de números
   sem link.
3. Para código: veja se há testes, se os dados ficaram fora do commit e se o resumo traz contagens.
4. Comente direto no PR, ou volte à sessão e peça a correção (*"ajuste X no PR"*). A sessão faz um novo push no mesmo PR.
5. Mescle com **Squash and merge** (o histórico da `main` fica limpo). Apague a branch.
6. Só então inicie as sessões que dependem daquele PR.

Se a sessão já foi encerrada e você quer mudar algo, abra uma sessão nova e diga: *"no PR #N, faça Y"*.

## 7. Acesso de rede, setup e dados

- **Acesso de rede** é configurado no **ambiente**: menu do ambiente na barra de título da sessão →
  **Edit** → *Network access*. No nível *Limited*, adicione os domínios necessários em *Allowed domains*
  (mantenha "Allow package managers" marcado). Documentação: https://code.claude.com/docs/en/cloud-environments#network-access
- Domínios que provavelmente precisaremos: `*.mapbiomas.org`, `storage.googleapis.com`,
  `*.car.gov.br`, `terrabrasilis.dpi.inpe.br`, `*.inpe.br`, `*.ibama.gov.br`, `*.icmbio.gov.br`,
  `idesisema.meioambiente.mg.gov.br`, `*.meioambiente.mg.gov.br`, `*.bcb.gov.br`, `*.ibge.gov.br`,
  `*.ana.gov.br`, `basedosdados.org`, `data.chc.ucsb.edu` (CHIRPS), `pypi.org`.
- **Teste de 28/10/2026:** a rede deste ambiente está aberta, mas `servicos.ibama.gov.br` e
  `www.ibge.gov.br` responderam **403 vindo do próprio site** (provável bloqueio de IP de datacenter
  estrangeiro). Isso não se resolve na configuração de rede. Alternativas: espelhos (Base dos Dados,
  GEE, FTP do IBGE), baixar no seu computador e rodar o pipeline localmente, ou conectar a sessão a uma
  pasta do seu computador via *Remote Control*.
- **Setup script** (mesmo menu → *Setup script*): comandos que rodam ao criar cada sessão, por exemplo
  `pip install -e .` quando existir `pyproject.toml` (a partir da sessão 07). Economiza tempo e crédito.
- **Disco** por sessão é limitado: não baixe o Brasil inteiro; recorte para MG/vitrine logo no download.

## 8. Economizar crédito

1. **Um prompt bem escrito vale mais que dez correções.** Use os prompts de `docs/prompts/`.
2. Use o modo de planejamento nas sessões caras: aprovar um plano ruim custa pouco, executar um custa muito.
3. Paralelize pesquisas independentes (1 sessão com 5 subagentes ou 5 sessões): o tempo total cai.
4. Não peça "explore tudo". Aponte arquivos e objetivos.
5. Sessões curtas e focadas, uma entrega por sessão. Encerre quando o PR estiver aberto.
6. Trabalho pesado de dados (downloads grandes, processamento raster) pode ficar mais barato no seu
   computador: a sessão escreve o script e você roda localmente.
7. Não reabra discussões já decididas: aponte para `docs/decisoes/`.

## 9. Erros comuns (e como evitar)

| Erro | Prevenção |
|---|---|
| Trabalho perdido porque a sessão expirou | Peça commit e push ao fim de cada etapa |
| Dados commitados por acidente | `.gitignore` já bloqueia `data/`; confira em *Files changed* |
| Sessão começa sem contexto | Sempre comece com "Leia `CLAUDE.md` e …" (os prompts já fazem isso) |
| Conflito de merge entre sessões paralelas | Arquivos distintos por sessão; mesclar na ordem |
| Números inventados ou links quebrados | Exija link por afirmação; confira por amostragem |
| "Modelo ótimo" que é vazamento | Peça ao `advogado-do-diabo` e ao `estatistico-modelagem` para revisar |
| Base pública usada sem licença comercial | Nenhuma base entra sem linha em `licencas.md` |
| Misturar material do emprego | Proibido. Na dúvida, não use |
| Sessão iniciando antes do PR anterior ser mesclado | Siga `docs/prompts/README.md` |

## 10. Comandos úteis

| Comando | Para quê |
|---|---|
| `/model` | trocar o modelo (opusplan, opus, sonnet) |
| `/agents` | listar ou editar subagentes |
| `/clear` | limpar o contexto (começar outra tarefa na mesma sessão) |
| `/compact` | resumir a conversa para economizar contexto |
| `/cost` ou `/usage` | ver o consumo |
| `Esc` | interromper o Claude no meio de uma ação |
