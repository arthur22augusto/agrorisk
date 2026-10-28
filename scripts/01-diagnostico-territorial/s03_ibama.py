"""Consome raw/ibama/termo_de_embargo.csv e raw/ibama/ai/auto_infracao_AAAA.csv (IBAMA dados abertos, CKAN).
Conta por municipio-ano (data do embargo / data do auto), apenas Lavrado e nao cancelado. NAO exporta CPF/CNPJ/nomes (LGPD).
Produz ibama_embargos_municipio_ano.csv e ibama_autos_municipio_ano.csv (+ _flora)."""
import pandas as pd, glob
m=pd.read_csv('municipios.csv',dtype={'cod_ibge':str})[['cod_ibge','municipio','grupo']]
e=pd.read_csv('raw/ibama/termo_de_embargo.csv',sep=';',encoding='utf-8-sig',dtype=str,usecols=['DES_STATUS_FORMULARIO','SIT_CANCELADO','DAT_EMBARGO','COD_MUNICIPIO','QTD_AREA_EMBARGADA','TIPO_AREA'])
e=e[e.COD_MUNICIPIO.isin(m.cod_ibge)&(e.DES_STATUS_FORMULARIO=='Lavrado')&(e.SIT_CANCELADO=='N')].copy()
e['ano']=e.DAT_EMBARGO.str[:4].astype(int); e=e[e.ano<=2026]
e['area_ha']=e.QTD_AREA_EMBARGADA.str.replace(',','.').astype(float)
print('embargos vitrine',len(e), e.TIPO_AREA.value_counts().head(8).to_dict(), 'ano min',e.ano.min())
def piv(df,val=None):
    g=df.groupby(['COD_MUNICIPIO','ano']); t=(g.size() if val is None else g[val].sum()).unstack('ano').fillna(0)
    return m.merge(t,left_on='cod_ibge',right_index=True,how='left').fillna(0).sort_values(['grupo','municipio'])
pe=piv(e); pe.to_csv('ibama_embargos_municipio_ano.csv',index=False)
piv(e,'area_ha').round(1).to_csv('ibama_embargos_area_ha_municipio_ano.csv',index=False)
print(pe.drop(columns=['cod_ibge','municipio','grupo']).sum().astype(int).to_dict())
a=[]
for f in sorted(glob.glob('raw/ibama/ai/auto_infracao_*.csv')):
    d=pd.read_csv(f,sep=';',dtype=str,usecols=['DES_STATUS_FORMULARIO','SIT_CANCELADO','DAT_HORA_AUTO_INFRACAO','COD_MUNICIPIO','TIPO_INFRACAO','VAL_AUTO_INFRACAO'],encoding_errors='replace')
    d=d[d.COD_MUNICIPIO.isin(m.cod_ibge)&(d.DES_STATUS_FORMULARIO=='Lavrado')&(d.SIT_CANCELADO=='N')]; a.append(d)
a=pd.concat(a); a['ano']=a.DAT_HORA_AUTO_INFRACAO.str[:4].astype(int)
print('autos',len(a),a.TIPO_INFRACAO.value_counts().to_dict())
pa=piv(a); pa.to_csv('ibama_autos_municipio_ano.csv',index=False)
fl=a[a.TIPO_INFRACAO.str.contains('Flora',na=False)]; pf=piv(fl); pf.to_csv('ibama_autos_flora_municipio_ano.csv',index=False)
print(pa.drop(columns=['cod_ibge','municipio','grupo']).sum().astype(int).to_dict()); print(pf.drop(columns=['cod_ibge','municipio','grupo']).sum().astype(int).to_dict())
print(pe.to_string())
