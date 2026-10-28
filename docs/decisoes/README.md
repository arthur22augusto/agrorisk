# Decisões

Registro de decisões (estilo ADR). Um arquivo por decisão: `NNNN-titulo-curto.md`.
Decisões não se apagam: se mudar de ideia, crie uma nova que *substitui* a anterior e marque a antiga como `Substituída por NNNN`.

Modelo:

```markdown
# NNNN — Título
- Data: AAAA-MM-DD
- Status: proposta | aceita | substituída por NNNN
- Decisores: ...

## Contexto
## Opções consideradas (com prós/contras e evidências)
## Decisão
## Consequências (o que muda, riscos, como reverter)
```

| Nº | Decisão | Status |
|---|---|---|
| 0001 | [Recorte, cliente-alvo e premissas iniciais](0001-recorte-cliente-e-premissas.md) | aceita |
| — | `escopo-mvp.md` (Y, recorte final, métricas, critério de sucesso) | pendente — sessão 06 |
