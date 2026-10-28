"""Consome raw/focos/focos_br_ref_AAAA.zip (INPE BDQueimadas, satelite de referencia). Filtra MG e os 50 municipios por nome normalizado.
Produz focos_municipio_ano.csv. Foco de calor != area queimada != desmatamento."""
import pandas as pd, zipfile, unicodedata, glob, re
def norm(s): return unicodedata.normalize('NFKD',str(s)).encode('ascii','ignore').decode().lower().strip()
m=pd.read_csv('municipios.csv',dtype={'cod_ibge':str}); m['k']=m.municipio.map(norm)
out=[];rng={}
for f in sorted(glob.glob('raw/focos/*.zip')):
    y=int(re.findall(r'(\d{4})',f)[0])
    d=pd.read_csv(zipfile.ZipFile(f).open(zipfile.ZipFile(f).namelist()[0]),usecols=['data_pas','estado','municipio'])
    rng[y]=(d.data_pas.min(),d.data_pas.max(),len(d))
    d=d[d.estado.map(norm)=='minas gerais']; d['k']=d.municipio.map(norm)
    c=d.groupby('k').size().rename(y); out.append(c)
t=pd.concat(out,axis=1).fillna(0).astype(int)
r=m.merge(t,left_on='k',right_index=True,how='left').fillna(0).drop(columns=['k'])
cols=['cod_ibge','municipio','grupo']+list(t.columns)
r=r[cols].sort_values(['grupo','municipio']); r.to_csv('focos_municipio_ano.csv',index=False)
for y,v in rng.items(): print(y,v)
print(r[list(t.columns)].sum()); print(r.to_string())
