---
name: token-efficient
description: "Política global de economia de tokens e contexto para tarefas de programação, análise de dados, SQL, R, Git e documentação. Usar por padrão em qualquer tarefa, exceto quando a economia comprometer corretude — nesse caso, corretude vence."
---

# token-efficient

Política padrão de eficiência de contexto e tokens. Aplica-se a qualquer
projeto e qualquer tarefa, mas corretude sempre tem prioridade sobre economia.

## Regra geral

Se economizar tokens pode gerar erro, não economize. Leia o que for preciso
para responder corretamente. Esta skill reduz desperdício, não reduz
investigação necessária.

## Comunicação

- Seja conciso por padrão. Não repita nem reformule o pedido do usuário
  antes de agir.
- Evite explicações longas, salvo se solicitado.
- Não crie planos longos para tarefas simples.
- Não faça afirmações sobre código que você não inspecionou, quando a
  resposta depende desse código.

## Exploração e leitura

- Busque de forma estreita antes de ler arquivos inteiros: prefira
  grep/ripgrep/find ou buscas específicas a abrir muitos arquivos.
- Leia apenas os trechos necessários dos arquivos quando possível (use
  offset/limit em vez de ler o arquivo inteiro quando ele for grande e o
  alvo for localizado).
- Antes de uma exploração ampla do repositório, avalie se uma busca
  direcionada já resolve.
- Não explore diretórios ou arquivos não relacionados à tarefa.
- Não releia arquivos inalterados desnecessariamente — reutilize o que já
  foi lido nesta sessão.

## Escopo

- Evite refatorações, melhorias ou abstrações fora do escopo solicitado.
- Não crie arquivos auxiliares desnecessários. Se criar arquivos
  temporários, remova-os ao final da tarefa.

## Subagentes

Evite subagentes para:
- alterações em um único arquivo;
- buscas simples;
- tarefas sequenciais;
- pequenas correções;
- consultas simples de SQL, R, Python ou Git.

Use subagentes apenas quando:
- houver tarefas realmente independentes e paralelizáveis;
- for útil isolar um contexto grande (para não poluir a sessão principal);
- houver múltiplas linhas de investigação independentes.

Para tarefas pequenas, trabalhe diretamente.

## Formato padrão da resposta final

Ao concluir a tarefa, estruture a resposta assim:

```
Changed:
Checked:
Risk:
Next step:
```

- Mantenha cada seção curta (1-3 linhas).
- Omita qualquer seção que não seja relevante (ex.: "Risk" pode ser
  omitido se não houver risco identificável).
- Esse formato é para o resumo final, não para atualizações intermediárias
  durante o trabalho.
