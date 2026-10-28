"""Resume candidatos a Y: totais anuais na vitrine e taxa de municipio-anos positivos (2016-2025, 50 municipios = 500 municipio-anos)."""
import pandas as pd
Y=range(2016,2026); out=[]; pos=[]
def wide(fn,idcols=('cod_ibge','municipio','grupo')):
    d=pd.read_csv(fn,dtype={'cod_ibge':str}); d.columns=[int(c) if c.isdigit() else c for c in d.columns]; return d
md=pd.read_csv('mb_desmat_anual_municipio.csv'); mdw=md[[f'desmat_{y}_ha' for y in Y]]; mdw.columns=list(Y)
pr=pd.read_csv('prodes_municipio_ano.csv',dtype={'cod_ibge':str}); prw=pr.groupby(['cod_ibge','ano']).area_ha.sum().unstack().reindex(columns=list(Y)).fillna(0)
prw=prw.reindex(pd.read_csv('municipios.csv',dtype={'cod_ibge':str}).cod_ibge).fillna(0)
fo=wide('focos_municipio_ano.csv')[list(Y)]; fg=wide('mbfogo_area_ha_municipio_ano.csv')[list(Y)[0:]] if False else wide('mbfogo_area_ha_municipio_ano.csv'); fg=fg[[y for y in Y if y in fg.columns]]
emb=wide('ibama_embargos_municipio_ano.csv'); emb=emb.reindex(columns=['cod_ibge']+list(Y)).fillna(0)[list(Y)]
af=wide('ibama_autos_flora_municipio_ano.csv')[list(Y)]
sf=wide('sisema_fiscalizacoes_municipio_ano.csv'); sf=sf[[y for y in Y if y in sf.columns]]
series={'MapBiomas desmatamento (perda veg. nativa), ha':(mdw,[1,5]),'PRODES Cerrado+MA (ha)':(prw,[0.0001,1]),'Focos de calor INPE (n)':(fo,[1,5]),'MapBiomas Fogo area queimada (ha)':(fg,[1,50]),'IBAMA embargos (n)':(emb,[1]),'IBAMA autos de infracao Flora (n)':(af,[1]),'SISFIS fiscalizacoes SEMAD, todas (n)':(sf,[1])}
rows=[];prows=[]
for k,(d,th) in series.items():
    d=d.reset_index(drop=True); r={'serie':k}; r.update({y:round(float(d[y].sum()),0) for y in d.columns}); rows.append(r)
    pr_={'serie':k,'mun_anos':int(d.size)}
    for t in th: pr_[f'pct_mun_ano_>={t}']=round(100*float((d.values>=t).mean()),1)
    prows.append(pr_)
pd.DataFrame(rows).to_csv('y_totais_anuais_vitrine.csv',index=False); pd.DataFrame(prows).to_csv('y_taxa_positivos.csv',index=False)
print(pd.DataFrame(rows).to_string()); print(pd.DataFrame(prows).to_string())
