---
name: documentation
description: "Manter a documentação do projeto atualizada e útil como contexto para humanos e agentes: o que o projeto faz, como executar, dados de entrada, etapas, outputs e decisões metodológicas (WHY e HOW, não sintaxe óbvia). Usar quando mudanças materiais tornarem README/documentação obsoletos, ao documentar decisões ou ao escrever README."
---

# documentation

Documentar PARA entender o projeto depois — outra pessoa, o autor daqui a
seis meses, ou um agente de IA sem contexto. Registrar WHY e HOW, não
sintaxe óbvia.

## Princípios

- Comentário ruim: `# incrementa x` antes de `x += 1`.
- Comentário bom:

```r
# Exclui observações sem histórico pré-tratamento porque
# o matching usa apenas características pré-tratamento.
```

- Documentar decisões metodológicas (por que este filtro, este corte
  temporal, este grupo controle), não mecânica de código.
- Sem documentação excessiva para código trivial.
- Documentação desatualizada é pior que ausente: corrigir quando notar.

## Quando atualizar (mudança material)

- Nova fonte de dado em `input/external/` → registrar fonte e data de acesso.
- Nova etapa no pipeline ou mudança de schema de output → atualizar README
  (fluxo/etapas) e, se afetar convenções, o AGENTS.md.
- Decisão metodológica relevante → registrar no README ou no script onde foi
  tomada.

## README deve responder

1. O que o projeto faz (uma frase + contexto).
2. Como executar (comandos, ordem das etapas, dependências relevantes).
3. Quais dados entram (fontes, onde estão).
4. Quais etapas existem e quais outputs produzem.
5. Decisões metodológicas importantes.

Mudanças pequenas não exigem tocar README; mudanças materiais sim.
