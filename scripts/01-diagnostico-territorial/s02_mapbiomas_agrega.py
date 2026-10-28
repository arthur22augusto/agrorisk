"""Consome mb_*_col11_vitrine.csv. Produz mb_uso_cobertura_municipio.csv, mb_desmat_anual_municipio.csv.
Vegetacao nativa = classes 3,4,11,12,29 (floresta, savana, campo alagado, campo, afloramento). Areas em ha (MapBiomas)."""
import pandas as pd
mun=pd.read_csv('municipios.csv',dtype={'cod_ibge':str})[['cod_ibge','municipio','grupo','area_km2']]
c=pd.read_csv('mb_cobertura_col11_vitrine.csv',dtype={'geocode':str})
nat=[3,4,11,12,29]; grp={'veg_nativa':nat,'floresta_savana':[3,4],'campo_umido_rocha':[11,12,29],'pastagem':[15],'agricultura':[39,41,46,47,48],'silvicultura':[9],'mosaico_usos':[21],'urbano':[24],'mineracao':[30],'agua':[33,31]}
out=[]
for g,df in c.groupby('geocode'):
    r={'cod_ibge':g,'area_mapbiomas_ha_2025':df.y2025.sum()}
    for y in (1985,2015,2025):
        for k,cl in grp.items():
            if y in (1985,2015) and k not in ('veg_nativa','pastagem','agricultura','silvicultura','urbano','mineracao'): continue
            r[f'{k}_{y}_ha']=df[df['class'].isin(cl)][f'y{y}'].sum()
    out.append(r)
o=pd.DataFrame(out).merge(mun,on='cod_ibge')
o['pct_veg_nativa_2025']=100*o.veg_nativa_2025_ha/o.area_mapbiomas_ha_2025
o['delta_veg_nativa_2015_2025_ha']=o.veg_nativa_2025_ha-o.veg_nativa_2015_ha
o['delta_antropico_2015_2025_ha']=sum(o[f'{k}_2025_ha']-o[f'{k}_2015_ha'] for k in ['pastagem','agricultura','silvicultura','urbano','mineracao'])
o['delta_urbano_2015_2025_ha']=o.urbano_2025_ha-o.urbano_2015_ha
o['delta_mineracao_2015_2025_ha']=o.mineracao_2025_ha-o.mineracao_2015_ha
o=o.round(1).sort_values(['grupo','municipio']); o.to_csv('mb_uso_cobertura_municipio.csv',index=False)
d=pd.read_csv('mb_desmat_col11_vitrine.csv',dtype={'GEOCODE':str})
ys=[f'y{y}' for y in range(2016,2026)]
a=d.groupby(['GEOCODE','TRANSITION_CLASS_NAME'])[ys].sum().reset_index()
a=a.pivot(index='GEOCODE',columns='TRANSITION_CLASS_NAME',values=ys).fillna(0)
tot=d.groupby('GEOCODE')[ys].sum(); tot.columns=[f'desmat_{y[1:]}_ha' for y in ys]
tot['desmat_2016_2025_ha']=tot.sum(axis=1)
tot['desmat_2021_2025_ha']=tot[[f'desmat_{y}_ha' for y in range(2021,2026)]].sum(axis=1)
tot['desmat_primaria_2016_2025_ha']=d[d.TRANSITION_CLASS_ID==4].groupby('GEOCODE')[ys].sum().sum(axis=1)
tot['desmat_secundaria_2016_2025_ha']=d[d.TRANSITION_CLASS_ID==6].groupby('GEOCODE')[ys].sum().sum(axis=1)
tot=tot.reset_index().rename(columns={'GEOCODE':'cod_ibge'}).merge(mun,on='cod_ibge',how='right').fillna(0)
tot['desmat_2016_2025_pct_area']=100*tot.desmat_2016_2025_ha/(tot.area_km2*100)
tot=tot.round(2).sort_values(['grupo','municipio']); tot.to_csv('mb_desmat_anual_municipio.csv',index=False)
pd.set_option('display.width',250)
print(o[['municipio','grupo','pct_veg_nativa_2025','delta_veg_nativa_2015_2025_ha','delta_urbano_2015_2025_ha','delta_mineracao_2015_2025_ha']].to_string())
print(tot[['municipio','desmat_2016_2025_ha','desmat_2021_2025_ha','desmat_2025_ha','desmat_primaria_2016_2025_ha']].to_string())
print(tot[[c for c in tot if c.startswith('desmat_20') and c.endswith('_ha') and len(c)==14]].sum())
