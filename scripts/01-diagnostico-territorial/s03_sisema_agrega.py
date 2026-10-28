"""Consome raw/sisema/*.geojson + vitrine_malha.gpkg. Atribui municipio por ponto (representative_point) em EPSG:4674.
Produz sisema_*_municipio_ano.csv. Nao exporta CPF/CNPJ/nomes de pessoas."""
import geopandas as gpd, pandas as pd
mun=gpd.read_file('vitrine_malha.gpkg')[['CD_MUN','NM_MUN','geometry']].rename(columns={'CD_MUN':'cod_ibge'})
base=pd.read_csv('municipios.csv',dtype={'cod_ibge':str})[['cod_ibge','municipio','grupo']]
def carrega(n):
    g=gpd.read_file(f'raw/sisema/{n}.geojson').set_crs(4674,allow_override=True)
    g['geometry']=g.geometry.representative_point(); return gpd.sjoin(g,mun[['cod_ibge','geometry']],predicate='within',how='inner')
def piv(df,ycol,name,val=None):
    g=df.groupby(['cod_ibge',ycol]); t=(g.size() if val is None else g[val].sum()).unstack(ycol).fillna(0)
    t=base.merge(t,left_on='cod_ibge',right_index=True,how='left').fillna(0).sort_values(['grupo','municipio']); t.to_csv(name,index=False); return t
def tot(t): return t.drop(columns=['cod_ibge','municipio','grupo']).sum().astype(int).to_dict()
# embargos Sisema
e=carrega('ide_2304_mg_areas_embargadas_sisema_pol'); e['ano']=pd.to_datetime(e.data_fisca,format='%d/%m/%Y',errors='coerce').dt.year
print('embargos sisema na vitrine',len(e),e.ano.min(),e.ano.max()); e=e.dropna(subset=['ano']); e['ano']=e.ano.astype(int)
print(tot(piv(e,'ano','sisema_embargos_municipio_ano.csv')))
print(e.atividade_.value_counts().head(8).to_dict())
# supressao autorizada IEF
s=carrega('ide_2105_mg_area_autorizada_intervencao_ambiental_ief_pol'); s['area_autor']=pd.to_numeric(s.area_autor.astype(str).str.replace(',','.'),errors='coerce'); s['ano']=pd.to_numeric(s.ano,errors='coerce')
print('IEF autorizacoes',len(s),s.ano.min(),s.ano.max(),s.decisao.value_counts().to_dict(),s.modalidade.value_counts().head(5).to_dict())
s=s.dropna(subset=['ano']); s['ano']=s.ano.astype(int)
print(tot(piv(s,'ano','sisema_ief_supressao_autorizada_n_municipio_ano.csv'))); print({k:round(v,0) for k,v in tot(piv(s,'ano','sisema_ief_supressao_autorizada_ha_municipio_ano.csv','area_autor')).items()})
# fiscalizacoes legado SISFIS
f=carrega('ide_2301_mg_legado_sisfis_pto'); f['ano']=pd.to_datetime(f.data_fisc,format='%d/%m/%Y',errors='coerce').dt.year
print('sisfis',len(f),f.ano.min(),f.ano.max()); f=f.dropna(subset=['ano']); f['ano']=f.ano.astype(int)
print(tot(piv(f,'ano','sisema_fiscalizacoes_municipio_ano.csv'))); print(f.tipologia.value_counts().head(10).to_dict()); print(f.tipo_deman.value_counts().head(8).to_dict())
pd.concat([f.groupby(['tipologia','ano']).size().unstack().fillna(0)]).to_csv('sisema_fiscalizacoes_tipologia_ano_vitrine.csv')
# outorgas
o=carrega('ide_2103_mg_outorgas_uso_recursos_hidricos_pto'); o['ano']=pd.to_datetime(o.datpub_4,errors='coerce',dayfirst=True).dt.year
print('outorgas',len(o),o.statuspa_4.value_counts().to_dict(),o.ano.min(),o.ano.max(),o.tipouso_4.value_counts().head(6).to_dict())
o=o.dropna(subset=['ano']); o['ano']=o.ano.astype(int)
print(tot(piv(o,'ano','sisema_outorgas_publicadas_municipio_ano.csv')))
st=o.groupby(['cod_ibge','statuspa_4']).size().unstack().fillna(0); st=base.merge(st,left_on='cod_ibge',right_index=True,how='left').fillna(0); st.to_csv('sisema_outorgas_status_municipio.csv',index=False)
u=carrega('ide_2103_mg_uso_insignificante_recursos_hidricos_pto'); u['ano']=pd.to_datetime(u.dtpub_4,errors='coerce',dayfirst=True).dt.year
u=u.dropna(subset=['ano']); u['ano']=u.ano.astype(int); print('uso insig',len(u),u.ano.min(),u.ano.max()); piv(u,'ano','sisema_uso_insignificante_municipio_ano.csv')
