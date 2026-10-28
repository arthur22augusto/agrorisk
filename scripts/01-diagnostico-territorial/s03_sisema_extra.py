"""Cavidades (CANIE via IDE-Sisema) por municipio e fiscalizacoes SISFIS de Flora por ano na vitrine."""
import geopandas as gpd, pandas as pd
mun=gpd.read_file('vitrine_malha.gpkg')[['CD_MUN','NM_MUN','geometry']]
def load(n):
    g=gpd.read_file(f'raw/sisema/{n}.geojson').set_crs(4674,allow_override=True); g['geometry']=g.geometry.representative_point() if g.geom_type.iloc[0]!='Point' else g.geometry
    return gpd.sjoin(g,mun,predicate='within')
c=load('ide_2001_mg_raio_protecao_cavidades_pol'); print('cavidades na vitrine',len(c),c.nvl_valida.value_counts().to_dict())
t=c.groupby('CD_MUN').size().rename('n_cavidades_canie').reset_index().rename(columns={'CD_MUN':'cod_ibge'}); t['municipio']=t.cod_ibge.map(dict(zip(mun.CD_MUN,mun.NM_MUN)))
t.sort_values('n_cavidades_canie',ascending=False).to_csv('sisema_cavidades_municipio.csv',index=False); print(t.sort_values('n_cavidades_canie',ascending=False).head(10).to_string())
f=load('ide_2301_mg_legado_sisfis_pto'); f['ano']=pd.to_datetime(f.data_fisc,format='%d/%m/%Y',errors='coerce').dt.year
fl=f[(f.tipologia=='Flora')&f.ano.between(2013,2025)].groupby('ano').size(); print(fl.to_dict())
print(f.data_cadas.head(3).tolist(), f.data_cadas.notna().mean())
