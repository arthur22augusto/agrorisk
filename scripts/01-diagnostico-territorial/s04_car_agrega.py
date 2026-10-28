"""Consome raw/car/mun/*.geojson (SICAR WFS, snapshot 2026-10-28), raw/sisema UCs (IDE-Sisema) e municipios.csv.
Areas em EPSG:31983 (UTM 23S). Produz car_municipio.csv, car_uc_municipio.csv, car_criacao_ano.csv.
Classes por modulos fiscais (m_fiscal do SICAR): <=1 minifundio; 1-4 pequena; 4-15 media; >15 grande (Lei 8.629/1993). Sem CPF/nome."""
import geopandas as gpd, pandas as pd, glob, numpy as np
base=pd.read_csv('municipios.csv',dtype={'cod_ibge':str})[['cod_ibge','municipio','grupo','area_km2']]
g=pd.concat([gpd.read_file(f) for f in glob.glob('raw/car/mun/*.geojson')],ignore_index=True); g=gpd.GeoDataFrame(g).set_crs(4674,allow_override=True)  # WFS entrega coordenadas SIRGAS2000 sem declarar CRS no GeoJSON
g['cod_ibge']=g.cod_municipio_ibge.astype(str); g['ano']=pd.to_datetime(g.dat_criacao).dt.year
g['classe']=pd.cut(g.m_fiscal,[-1,1,4,15,1e9],labels=['minifundio_<=1MF','pequena_1-4MF','media_4-15MF','grande_>15MF'])
ativo=g[g.status_imovel.isin(['AT','PE','SU'])]  # exclui cancelados
t=ativo.groupby('cod_ibge').agg(n_imoveis=('cod_imovel','size'),area_car_ha=('area','sum'),mediana_ha=('area','median')).reset_index()
for c in g.classe.cat.categories: t=t.merge(ativo[ativo.classe==c].groupby('cod_ibge').size().rename('n_'+c).reset_index(),on='cod_ibge',how='left')
t=t.merge(g[g.status_imovel=='CA'].groupby('cod_ibge').size().rename('n_cancelados').reset_index(),on='cod_ibge',how='left')
t=t.merge(ativo[ativo.condicao.str.startswith('Analisado',na=False)].groupby('cod_ibge').size().rename('n_analisados').reset_index(),on='cod_ibge',how='left')
t=base.merge(t,on='cod_ibge',how='left').fillna(0); t['area_car_pct_municipio']=100*t.area_car_ha/(t.area_km2*100)
t['pct_analisados']=100*t.n_analisados/t.n_imoveis
t.round(1).sort_values(['grupo','municipio']).to_csv('car_municipio.csv',index=False)
g.groupby('ano').size().to_csv('car_criacao_ano.csv'); print(g.groupby('ano').size().to_dict())
# UCs
def uc(n,nm='nome_uc'): 
    u=gpd.read_file(f'raw/sisema/ide_2010_mg_unidades_conservacao_{n}_pol.geojson').set_crs(4674,allow_override=True).to_crs(31983); u['esfera']=n; u['nome']=u[nm]; return u[['nome','esfera','geometry']]
U=pd.concat([uc('estaduais'),uc('federais'),uc('municipais')],ignore_index=True); U=gpd.GeoDataFrame(U,crs=31983); U['geometry']=U.geometry.make_valid()
sel={'APA Carste de Lagoa Santa (federal)':U[U.nome.str.upper().str.contains('CARSTE DE LAGOA SANTA')],'APA Estadual Sul RMBH':U[U.nome.str.contains('Sul RMBH')],'Qualquer UC (est/fed/mun)':U}
P=ativo[['cod_imovel','cod_ibge','area','geometry']].to_crs(31983); P['geometry']=P.geometry.make_valid(); P['a_m2']=P.area
rows=[]
for k,S in sel.items():
    S1=gpd.GeoDataFrame({'geometry':[S.geometry.union_all()]},crs=31983)
    i=gpd.overlay(P[['cod_imovel','geometry']],S1,how='intersection'); i['ov']=i.area; ov=i.groupby('cod_imovel').ov.sum()
    P[k]=P.cod_imovel.map(ov).fillna(0)/P.a_m2
    r=P.groupby('cod_ibge').apply(lambda d: pd.Series({'n_imoveis_interseccao':(d[k]>0.01).sum(),'n_imoveis_>50pct':(d[k]>0.5).sum(),'area_sobreposta_ha':(d[k]*d.a_m2).sum()/1e4}),include_groups=False).reset_index(); r['camada']=k; rows.append(r)
R=pd.concat(rows).merge(base[['cod_ibge','municipio','grupo']],on='cod_ibge')
R.round(1).to_csv('car_uc_municipio.csv',index=False)
print(R.groupby('camada')[['n_imoveis_interseccao','n_imoveis_>50pct','area_sobreposta_ha']].sum().round(0))
print(R[R.camada.str.contains('Carste|Sul')].query('n_imoveis_interseccao>0')[['camada','municipio','n_imoveis_interseccao','n_imoveis_>50pct','area_sobreposta_ha']].round(0).to_string())
print(t[['municipio','n_imoveis','area_car_ha','area_car_pct_municipio','pct_analisados']].round(1).to_string())
print(t[['n_imoveis','area_car_ha','n_minifundio_<=1MF','n_pequena_1-4MF','n_media_4-15MF','n_grande_>15MF','n_cancelados','n_analisados']].sum())
