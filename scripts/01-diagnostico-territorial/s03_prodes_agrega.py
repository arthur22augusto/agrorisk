"""Consome raw/prodes/*.geojson + vitrine_malha.gpkg (IBGE 2022). Interseccao em EPSG:31983 (UTM 23S, area em ha).
Produz prodes_municipio_ano.csv (linhas: municipio, bioma, ano, n_poligonos, area_ha) e prodes_resumo_municipio.csv."""
import geopandas as gpd, pandas as pd
mun=gpd.read_file('vitrine_malha.gpkg').to_crs(31983)[['CD_MUN','NM_MUN','geometry']]
res=[]
cer=None
for lay,bioma in [('prodes-cerrado-nb','Cerrado'),('prodes-mata-atlantica-nb','Mata Atlantica')]:
    g=gpd.read_file(f'raw/prodes/{lay}.geojson').set_crs(4326).to_crs(31983)
    print(bioma,g.year.min(),g.year.max(),g.main_class.value_counts().to_dict(), g.get('pub_date',pd.Series()).dropna().unique()[:5])
    g=g[g.main_class.str.upper().isin(['DESMATAMENTO'])] 
    g['geometry']=g.geometry.make_valid(); g=g.explode(index_parts=False); g=g[g.geom_type=='Polygon']
    if bioma=='Cerrado': cer=g.geometry.union_all()
    else:
        # dedup: remove da camada Mata Atlantica a area ja coberta pela camada Cerrado (fonte 'antigo cerrado' sobrepoe)
        g['geometry']=g.geometry.difference(cer); g=g[~g.geometry.is_empty].explode(index_parts=False); g=g[g.geom_type=='Polygon']
    i=gpd.overlay(g[['year','geometry']],mun,how='intersection',keep_geom_type=True)
    i['area_ha']=i.area/1e4; i['bioma']=bioma
    res.append(i.groupby(['CD_MUN','NM_MUN','bioma','year']).agg(n_poligonos=('area_ha','size'),area_ha=('area_ha','sum')).reset_index())
r=pd.concat(res); r.rename(columns={'CD_MUN':'cod_ibge','NM_MUN':'municipio','year':'ano'}).round(2).to_csv('prodes_municipio_ano.csv',index=False)
p=r.pivot_table(index=['CD_MUN','NM_MUN'],columns='year',values='area_ha',aggfunc='sum').fillna(0)
print(p.sum().round(0).to_string())
m=pd.read_csv('municipios.csv',dtype={'cod_ibge':str})[['cod_ibge','grupo']]
s=pd.DataFrame({'area_ha_2008_2024':p.loc[:,[c for c in p.columns if 2008<=c<=2024]].sum(axis=1)})
for a,b in [(2016,2020),(2021,2025)]: s[f'area_ha_{a}_{b}']=p.loc[:,[c for c in p.columns if a<=c<=b]].sum(axis=1)
s['n_anos_com_evento_2016_2025']=(p.loc[:,[c for c in p.columns if 2016<=c<=2025]]>0).sum(axis=1)
s=s.reset_index().rename(columns={'CD_MUN':'cod_ibge','NM_MUN':'municipio'}).merge(m,on='cod_ibge',how='right').fillna(0).round(1).sort_values(['grupo','municipio'])
s.to_csv('prodes_resumo_municipio.csv',index=False); print(s.to_string())
