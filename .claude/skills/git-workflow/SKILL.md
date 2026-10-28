---
name: git-workflow
description: "Git para projetos analíticos: status, diff, organização de mudanças, mensagens de commit, branches, histórico e preparação de PR; evitar commitar secrets e grandes datasets. Usar ao commitar, organizar alterações, revisar histórico ou preparar pull request. Sem operações destrutivas sem pedido e contexto explícitos."
---

# git-workflow

## Antes de commitar

1. `git status` + `git diff` (staged e unstaged) — nunca commitar às cegas.
2. Conferir o que NÃO deve ser commitado:
   - `.env` e qualquer secret (senhas, chaves, connection strings);
   - datasets grandes (`input/`, `output/data/`) — decidir caso a caso;
   - `intermediate/` (rebuildável; coberto pelo .gitignore padrão do projeto);
   - binários temporários, `.Rhistory`, caches.
3. Um commit = uma mudança lógica. Separar análise de refatoração quando
   prático.

## Mensagens

- Seguir o estilo do histórico do repositório (`git log --oneline -10`).
- Sem estilo estabelecido: imperativa, curta, específica ("corrige chave
  duplicada em 02_clean.R", não "updates").

## Operações

- Commitar apenas arquivos intencionais: `git add <paths>` ou revisar o
  staged antes do commit.
- Nunca sem pedido e contexto explícitos: `push --force`, `reset --hard`,
  `branch -D`, rebase em branch compartilhada, amend de commit já publicado.
- Não inicializar nem alterar remotes automaticamente.

## PR

- Antes de abrir: diff contra a branch base, lista de commits, `git status`
  limpo.
- Descrever: o que muda, por quê, riscos (mudança de schema de output?
  consumidor downstream afetado?).
