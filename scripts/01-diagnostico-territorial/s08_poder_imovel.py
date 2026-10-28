"""Poder estatistico em nivel de imovel: n de imoveis CAR (AT/PE/SU) com >=1 poligono PRODES (Cerrado+MA) por ano, e com >=0,5 ha / >=1 ha.
Consome raw/car/mun/*.geojson (snapshot atual) e raw/prodes/*.geojson. CRS de calculo: EPSG:31983. Produz poder_imovel_prodes.csv"""
import geopandas as gpd, pandas as pd, glob
car=pd.concat([gpd.read_file(f) for f in glob.glob('raw/car/mun/*.geojson')])
car=gpd.GeoDataFrame(car); car=car[car.status_imovel!='CA'].to_crs(31983)[['cod_imovel','area','geometry']]
car['geometry']=car.geometry.make_valid()
print('imoveis',len(car))
res=[]
cer=None
for lay in ['prodes-cerrado-nb','prodes-mata-atlantica-nb']:
    g=gpd.read_file(f'raw/prodes/{lay}.geojson').set_crs(4326).to_crs(31983)
    g=g[g.main_class.str.upper()=='DESMATAMENTO']; g=g[g.year>=2016]
    g['geometry']=g.geometry.make_valid(); g=g.explode(index_parts=False); g=g[g.geom_type=='Polygon']
    if cer is None: cer=g.geometry.union_all()
    else:
        g['geometry']=g.geometry.difference(cer); g=g[~g.geometry.is_empty].explode(index_parts=False); g=g[g.geom_type=='Polygon']
    i=gpd.overlay(g[['year','geometry']],car[['cod_imovel','geometry']],how='intersection',keep_geom_type=True)
    i['ha']=i.area/1e4; res.append(i[['year','cod_imovel','ha']])
r=pd.concat(res).groupby(['year','cod_imovel']).ha.sum().reset_index()
out=r.groupby('year').agg(imoveis_ge_0=('ha','size'),imoveis_ge_05ha=('ha',lambda s:(s>=0.5).sum()),imoveis_ge_1ha=('ha',lambda s:(s>=1).sum()),ha=('ha','sum')).round(1)
out['pct_imoveis_ge_0']=(out.imoveis_ge_0/len(car)*100).round(2)
out.to_csv('poder_imovel_prodes.csv'); print(out.to_string())
# imoveis distintos no periodo
print('distintos 2016-2025',r[r.year<=2025].cod_imovel.nunique(), 'com >=1ha em algum ano', (r[r.year<=2025].groupby('cod_imovel').ha.max()>=1).sum())
