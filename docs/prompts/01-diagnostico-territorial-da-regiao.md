# Sessão 01 — Diagnóstico territorial da RMBH + Colar + Sete Lagoas

> Cole tudo abaixo da linha como primeira mensagem de uma sessão nova (modelo: opusplan).
> Pode rodar **em paralelo** com 02, 03, 04 e 05.

---

Leia `CLAUDE.md` e `docs/decisoes/0001-recorte-cliente-e-premissas.md`. Esta é a **sessão 01** do AgroRisk: pesquisa, sem código de análise (pequenos scripts de consulta para obter números são permitidos, sem commitar dados).

**Objetivo:** entender, com números, o que acontece no território da vitrine (RMBH com 34 municípios + Colar Metropolitano + Sete Lagoas) para escolher um evento Y que seja frequente, relevante e observável.

**Agentes:** use em paralelo `engenheiro-dados-geo` (números de bases) e `pesquisador-academico` (estudos sobre a região); ao final, `advogado-do-diabo` revisa as conclusões.

**Tarefas**
1. Lista oficial de municípios (RMBH, Colar Metropolitano, Sete Lagoas) com código IBGE, área, população e PIB agro (fonte: Agência RMBH/ALMG/IBGE).
2. Uso e cobertura do solo e transições 1985→2024 (MapBiomas): vegetação nativa (Cerrado × Mata Atlântica), pastagem, agricultura, silvicultura, mineração, área urbana. Quanto de vegetação nativa foi suprimida por ano nos últimos 10 anos e para onde foi (urbano? pasto? mineração? eucalipto?).
3. Contagem anual (últimos 5–10 anos) de candidatos a Y, por município: alertas MapBiomas Alerta, PRODES Cerrado/Mata Atlântica, área queimada e focos (MapBiomas Fogo/INPE), embargos IBAMA/ICMBio, autos de infração SEMAD/IEF, conflitos de outorga (IGAM).
4. Número de imóveis no CAR por município e distribuição de tamanho (módulos fiscais); fração com sobreposição a UC/APA (APA Carste de Lagoa Santa, APA Sul RMBH, etc.).
5. Pressões típicas, com evidências: expansão urbana/loteamentos, mineração e barragens (Quadrilátero Ferrífero), eucalipto, cinturão verde, carste e recarga hídrica, escassez hídrica (crise 2014–2015, conflitos declarados).
6. **Poder estatístico:** para cada candidato a Y, estime os eventos por ano em nível de imóvel na vitrine; diga se bastam para treinar/validar e qual recorte ampliado de MG seria necessário (ex.: mesorregião Metropolitana, Central Mineira, todo o Cerrado mineiro).

**Entregável:** `docs/pesquisa/01-diagnostico-territorial.md`, no padrão de `docs/pesquisa/README.md`, com tabelas por município, gráficos opcionais em `reports/figuras/01-*.png`, e as seções finais **"Oportunidades de inovação para o AgroRisk"** (evidências + fontes linkadas) e **"Perguntas em aberto"**. Liste as bases consultadas numa seção "Fontes usadas" do próprio documento. **Não edite `docs/pesquisa/licencas.md`**: ele pertence à sessão 02, e editar o mesmo arquivo em paralelo gera conflito de merge.

**Critério de pronto:** toda tabela tem fonte e ano; há uma recomendação explícita de 2–3 candidatos a Y com número de eventos.

Ao terminar: faça o commit, dê push na branch da sessão, abra o PR "Sessão 01 — diagnóstico territorial" e liste no PR os 3 achados mais importantes.
