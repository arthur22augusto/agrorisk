"""Consome raw/fogo/fogo_AAAA.gpkg (MapBiomas Fogo Col.5, cicatrizes anuais) e vitrine_malha.gpkg. Interseccao em EPSG:31983.
Produz mbfogo_area_ha_municipio_ano.csv (ha queimados por municipio-ano) e mbfogo_pct_area_municipio_ano.csv."""
import geopandas as gpd, pandas as pd, glob, re
mun=gpd.read_file('vitrine_malha.gpkg').to_crs(31983).rename(columns={'CD_MUN':'cod_ibge'})[['cod_ibge','geometry']]
base=pd.read_csv('municipios.csv',dtype={'cod_ibge':str})[['cod_ibge','municipio','grupo','area_km2']]
res={}
for f in sorted(glob.glob('raw/fogo/fogo_*.gpkg')):
    y=int(re.findall(r'(\d{4})',f)[0]); g=gpd.read_file(f).to_crs(31983); g['geometry']=g.geometry.make_valid()
    g=g.explode(index_parts=False); g=g[g.geom_type=='Polygon']
    i=gpd.overlay(g[['geometry']],mun,how='intersection'); i['ha']=i.area/1e4
    res[y]=i.groupby('cod_ibge').ha.sum()
t=pd.DataFrame(res).fillna(0); r=base.merge(t,left_on='cod_ibge',right_index=True,how='left').fillna(0)
ys=[c for c in r.columns if isinstance(c,int)]
r=r.sort_values(['grupo','municipio']); r.drop(columns='area_km2').round(1).to_csv('mbfogo_area_ha_municipio_ano.csv',index=False)
p=r.copy()
for y in ys: p[y]=100*p[y]/(p.area_km2*100)
p.drop(columns='area_km2').round(2).to_csv('mbfogo_pct_area_municipio_ano.csv',index=False)
print(r[ys].sum().round(0).to_dict()); print(r[['municipio']+ys].round(0).to_string())
