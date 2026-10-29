# Pedidos de dados e de licença — rascunhos e acompanhamento

Rascunhos para o fundador enviar. Preencha os campos `[entre colchetes]`. **Confirme os canais e endereços antes de enviar** (os marcados "a confirmar" não foram verificados).

Dicas:
- Pedidos via **LAI** (Lei 12.527/2011) não precisam de justificativa (art. 10, §3º). O prazo é de 20 dias, prorrogáveis por mais 10. Guarde o número de protocolo.
- Peça sempre **dados anonimizados** (sem CPF/CNPJ/nome). Isso reduz a chance de negativa por sigilo bancário (LC 105/2001) ou LGPD.
- Peça formato aberto (CSV/GeoPackage/Shapefile) e o dicionário de dados.

## Acompanhamento

| # | Órgão | Canal | Enviado em | Protocolo | Prazo | Status |
|---|---|---|---|---|---|---|
| 1 | BCB — microdados SICOR e Proagro (LAI) | Fala.BR | | | | |
| 2 | BCB/Derop — dúvida técnica sobre a MDCR | e-mail | | | | |
| 3 | SEMAD-MG — licença de uso da IDE-Sisema | e-mail/ofício | | | | |
| 4 | SEMAD/IEF/IGAM — autos, embargos e autorizações históricos (LAI) | e-SIC MG | | | | |
| 5 | SFB — licença e histórico do CAR (LAI) | Fala.BR | | | | |
| 6 | MapBiomas — token do Alerta e termos de uso | cadastro + e-mail | | | | |

---

## 1. Banco Central — pedido via LAI (Fala.BR)
**Canal:** https://falabr.cgu.gov.br → "Acesso à Informação" → órgão: Banco Central do Brasil.

> **Assunto:** Microdados do SICOR (crédito rural) e do Proagro por operação, anonimizados — Minas Gerais, 2015–2025
>
> Com base na Lei nº 12.527/2011, solicito, em formato aberto (CSV) e com dicionário de dados:
>
> 1. **Operações de crédito rural registradas no SICOR**, em nível de operação, para imóveis localizados em Minas Gerais, contratadas de 2015 a 2025, **sem dados que identifiquem o tomador** (sem CPF/CNPJ/nome), contendo, quando disponíveis: identificador anonimizado da operação; código IBGE do **município do imóvel/empreendimento** (e, separadamente, o da agência, se diferentes); código do imóvel no CAR ou coordenadas da gleba (ou, se não for possível, o centroide arredondado ou a microrregião); finalidade, atividade, produto/cultura, programa e fonte de recursos; safra/ano agrícola; valor contratado; área financiada; datas de contratação e vencimento; enquadramento no Proagro.
> 2. **Proagro em Minas Gerais, 2015–2025**: comunicações de ocorrência de perdas, coberturas deferidas e indeferidas e valores indenizados, por operação anonimizada ou, se não for possível, agregados por **município × safra × cultura**.
> 3. Esclarecimento: na Matriz de Dados do Crédito Rural (API OData do SICOR), o campo `Municipio` corresponde ao município do imóvel/empreendimento ou ao da agência/instituição financeira?
>
> Caso algum item esteja protegido por sigilo, solicito o fornecimento da parte não sigilosa (art. 7º, §2º, da LAI), por exemplo agregada por município, ou a indicação do fundamento legal da restrição.
>
> [Seu nome]

## 2. Banco Central — dúvida técnica (e-mail informal, em paralelo ao pedido 1)
**Para:** sicor.derop@bcb.gov.br (contato do catálogo da MDCR)

> **Assunto:** Dúvida sobre o campo "Município" da Matriz de Dados do Crédito Rural
>
> Prezados,
>
> Estou usando as entidades `CusteioMunicipioProduto` e `InvestMunicipioProduto` da Matriz de Dados do Crédito Rural (API OData do SICOR) para estudar o crédito rural em municípios de Minas Gerais. Duas dúvidas:
>
> 1. O campo `Municipio` refere-se ao município do imóvel/empreendimento financiado ou ao da agência/instituição financeira? (Belo Horizonte e Contagem aparecem entre os maiores volumes da região metropolitana, o que me fez questionar.)
> 2. Existe publicação, ou previsão de publicação, de dados mais desagregados (por operação anonimizada, ou com o município do imóvel)?
>
> Obrigado,
> [Seu nome] — [contato]

## 3. SEMAD-MG — autorização de uso da IDE-Sisema
**Para:** Diretoria de Geoprocessamento (Dgeo) da SEMAD — e-mail a confirmar; telefone que consta no Capabilities do WFS: (31) 3915-1760. Alternativa: protocolo pelo SEI-MG/ouvidoria.

> **Assunto:** Termos de uso comercial das camadas da IDE-Sisema
>
> Prezados,
>
> Estou desenvolvendo, em fase inicial, um serviço de análise de risco socioambiental de imóveis rurais em Minas Gerais, voltado a instituições de crédito e a empresas com cadeias de fornecedores. Pretendemos usar camadas publicadas na IDE-Sisema (GeoServer `geoserver.meioambiente.mg.gov.br`), entre elas: áreas embargadas (`ide_2304`), autorizações de supressão do IEF (`ide_2105`), outorgas do IGAM (`ide_2103`), áreas de conflito/restrição hídrica (`ide_2007`), barragens e cavidades (FEAM), inventário florestal, ZEE e áreas prioritárias.
>
> Os metadados indicam "acesso livre" e o WFS declara `AccessConstraints: NONE`, mas não encontramos uma licença de uso explícita. Solicito confirmação, por escrito:
>
> 1. se essas camadas podem ser usadas para fins **comerciais**, inclusive em produtos derivados (indicadores e relatórios entregues a clientes);
> 2. qual é a forma de atribuição exigida (ex.: "Fonte: IDE-Sisema/SEMAD-MG");
> 3. se há restrição específica para camadas com dados pessoais (ex.: nome/CNPJ em áreas embargadas). Nosso uso previsto é pseudonimizado, sem republicar esses campos.
>
> Desde já agradeço.
> [Seu nome] — [contato]

## 4. Governo de MG — pedido via LAI (SEMAD, IEF, IGAM, FEAM)
**Canal:** e-SIC do Estado de Minas Gerais (Portal da Transparência MG) — **a confirmar** o endereço atual.

> **Assunto:** Autos de infração, embargos e autorizações de supressão — série histórica georreferenciada, 2015–2025
>
> Com base na Lei nº 12.527/2011 e no Decreto Estadual nº 45.969/2012, solicito, em formato aberto (CSV, Shapefile ou GeoPackage) e com dicionário de dados, **sem dados pessoais** dos autuados:
>
> 1. **Autos de infração ambientais** lavrados pela SEMAD, IEF, IGAM e FEAM de 2015 a 2025, com: número anonimizado; data da infração e data da lavratura; tipificação/artigo; órgão; município; coordenadas ou polígono; área afetada (ha); número do CAR do imóvel, quando registrado; situação (julgado, cancelado, pago).
> 2. **Termos de embargo/suspensão** de 2015 a 2025, com data de início, data de publicação, data de desembargo, polígono e município. (A camada atual da IDE-Sisema traz apenas 2025–2026.)
> 3. **Autorizações de intervenção ambiental/supressão de vegetação** (DAIA/AIA) de 2015 a 2025, com data, área autorizada, polígono, tipo de vegetação e município.
> 4. **Portarias de restrição de uso por escassez hídrica** (IGAM) de 2014 a 2025, com bacia/trecho e vigência.
>
> Caso parte da informação seja sigilosa, solicito a parte não sigilosa (art. 7º, §2º, da LAI).
>
> [Seu nome]

## 5. Serviço Florestal Brasileiro — pedido via LAI (Fala.BR)
**Canal:** https://falabr.cgu.gov.br → órgão: Serviço Florestal Brasileiro (ou MMA, se o SFB não aparecer — a confirmar).

> **Assunto:** Termos de uso dos dados públicos do SICAR e versões históricas do CAR em Minas Gerais
>
> Com base na Lei nº 12.527/2011, solicito:
>
> 1. Informação sobre a **licença ou termos de uso** dos dados públicos do SICAR (perímetros dos imóveis e demais camadas disponibilizadas para download), em especial se é permitido o uso **comercial** em produtos derivados e qual atribuição é exigida.
> 2. **Versões históricas** dos perímetros dos imóveis do CAR em Minas Gerais (por exemplo, extrações anuais de 2016 a 2025, ou o histórico de retificações com data), contendo código do imóvel, geometria, data de inscrição, data da última retificação, condição/status e módulos fiscais, **sem dados pessoais** dos titulares.
> 3. Se os itens anteriores não estiverem disponíveis, informar se existe base histórica e qual é o procedimento para acessá-la.
>
> [Seu nome]

## 6. MapBiomas — token do Alerta e termos de uso
**Passo 1:** criar uma conta na plataforma (https://plataforma.alerta.mapbiomas.org/) e gerar o token da API.
**Passo 2 (e-mail):** contato institucional do MapBiomas — **endereço a confirmar** no site.

> **Assunto:** Uso comercial da API do MapBiomas Alerta e dos produtos Fogo/Água
>
> Olá,
>
> Estou desenvolvendo um serviço de análise de risco socioambiental de imóveis rurais em Minas Gerais, para instituições de crédito e empresas com cadeias de fornecedores. Gostaria de confirmar:
>
> 1. se os dados obtidos pela **API do MapBiomas Alerta** (alertas e laudos) podem ser usados comercialmente nesses produtos, com atribuição (CC-BY?), e se há limite de requisições ou plano específico para uso comercial;
> 2. a licença das coleções do **MapBiomas Fogo** e **MapBiomas Água**;
> 3. a forma de citação recomendada.
>
> Obrigado!
> [Seu nome] — [contato]
