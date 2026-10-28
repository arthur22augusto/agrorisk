"""Baixa camadas da IDE-Sisema (GeoServer WFS) recortadas no bbox da vitrine -> raw/sisema/<camada>.geojson. EPSG:4674."""
import urllib.request, urllib.parse, json, sys, hashlib, datetime, os
U="https://geoserver.meioambiente.mg.gov.br/wfs"
BB="-20.52,-44.8,-19.05,-43.19,urn:ogc:def:crs:EPSG::4326"
def get(lay,hits=False,start=0,count=5000):
    p=dict(service='WFS',version='2.0.0',request='GetFeature',typeNames='IDE:'+lay,bbox=BB,srsName='EPSG:4674')
    if hits: p['resultType']='hits'
    else: p.update(outputFormat='application/json',count=count,startIndex=start,sortBy='')
    p={k:v for k,v in p.items() if v!=''}
    return urllib.request.urlopen(U+"?"+urllib.parse.urlencode(p),timeout=300).read()
for lay in sys.argv[1:]:
    out=f'raw/sisema/{lay}.geojson'
    if os.path.exists(out): print(lay,'ja existe'); continue
    try:
        h=get(lay,hits=True).decode(); import re; n=re.search(r'numberMatched="(\d+)"',h); n=int(n.group(1)) if n else -1
        feats=[];s=0
        while True:
            d=json.loads(get(lay,start=s)); feats+=d['features']
            if len(d['features'])<5000: break
            s+=5000
        json.dump({'type':'FeatureCollection','features':feats},open(out,'w'))
        print(lay,'hits',n,'baixadas',len(feats),hashlib.sha256(open(out,'rb').read()).hexdigest()[:16],datetime.date.today(),flush=True)
    except Exception as e: print(lay,'ERRO',repr(e)[:300],flush=True)
