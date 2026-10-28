# Contrato do catálogo de evidências para apresentações

O `data/resultados_manifest.json` é um **plano de coleta/produção de resultados**, não um arquivo de resultados estimados. Deve ser criado a partir do conteúdo do projeto; o `exemplo_manifest.json` é apenas demonstrativo.

## Estrutura JSON

```json
{
  "projeto": "Nome do estudo",
  "objetivo": "Pergunta principal, em uma frase",
  "publico": "Pesquisadores e/ou decisores",
  "tese": "Conclusão sustentada ou a confirmar",
  "resultados": [
    {
      "id": "R01",
      "titulo": "Nome de tabela/estatística necessária",
      "pergunta": "Qual questão a tabela responde?",
      "claim": "Afirmação que ela permite avaliar, sem inventar números",
      "prioridade": "P0",
      "status": "ausente",
      "tipo": "comparacao",
      "metrica": "Taxa de ocorrência",
      "unidade": "%",
      "comparadores": ["Tratamento", "Controle"],
      "periodo": "Antes e depois (datas a confirmar)",
      "populacao": "População sob estudo",
      "denominador": "N de unidades elegíveis",
      "dimensoes": ["grupo", "periodo"],
      "colunas_esperadas": ["grupo", "periodo", "n", "taxa"],
      "calculo": "Definição formal da métrica / procedimento",
      "metodo": "Análise descritiva ou estimador, se aplicável",
      "fonte": "Base de dados a confirmar",
      "arquivo_origem": "",
      "aba_origem": "",
      "slide": "Slide 3",
      "risco_se_faltar": "Não é possível sustentar a comparação",
      "proxima_acao": "Agendar cálculo da tabela",
      "dependencias": [],
      "observacoes": ""
    }
  ],
  "perguntas": [
    {
      "id": "Q01",
      "prioridade": "P0",
      "pergunta": "Qual o objetivo principal desta apresentação?",
      "porque_importa": "Altera a métrica que abre os slides",
      "impacto_no_ppt": "Seleção do resultado principal",
      "status": "aberta",
      "resposta": ""
    }
  ]
}
```

## Regras de qualidade

- `prioridade`: `P0` = sem o resultado a tese principal é insustentável; `P1` = comparação/argumento importante; `P2` = reforço futuro.
- `status` das tabelas: `disponivel`, `parcial`, `ausente`, `validar`. `disponivel` somente se existe saída conferível, com `arquivo_origem` e fonte; marcar `validar` se está mencionada mas sem arquivo confirmado.
- `tipo`: preferir `descritivo`, `comparacao`, `serie_temporal`, `inferencia`, `heterogeneidade`, `robustez`, `mapa`, `qualidade`, `outro`; não restringe outras classificações.
- Uma comparação precisa explicitar categorias (em `comparadores`) e período. Evitar grupo “controle” se a pesquisa não dispõe de comparador adequado.
- Uma taxa requer denominador e definição de universo; ausência disso deve ser `A DEFINIR` e potencialmente P0/P1.
- `colunas_esperadas` especificam **colunas desejáveis da tabela futura**; não presumem existência na base de origem.
- Nunca preencher estatísticas observadas sem a fonte. O Excel produzido terá o *inventário* e o *esquema*, não uma simulação.
- O agente pode sugerir novas entradas com IDs `Rxx`, que serão deduplicadas e aprovadas pelo orquestrador antes da regeneração do Excel.
