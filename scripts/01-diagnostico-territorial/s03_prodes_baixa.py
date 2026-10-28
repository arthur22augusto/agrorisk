"""Baixa PRODES (INPE/TerraBrasil WFS) yearly_deforestation no bbox da vitrine -> raw/prodes/*.geojson. Idempotente."""
import urllib.request, urllib.parse, json, os, hashlib, datetime
BB="-20.52,-44.8,-19.05,-43.19,urn:ogc:def:crs:EPSG::4326"
for lay in ['prodes-cerrado-nb','prodes-mata-atlantica-nb']:
    feats=[];start=0
    while True:
        p=dict(service='WFS',version='2.0.0',request='GetFeature',typeNames=f'{lay}:yearly_deforestation',outputFormat='application/json',bbox=BB,count=2000,startIndex=start,sortBy='uuid')
        for t in range(4):
            try: d=json.load(urllib.request.urlopen("https://terrabrasilis.dpi.inpe.br/geoserver/ows?"+urllib.parse.urlencode(p),timeout=200)); break
            except Exception as e: print('retry',e)
        feats+=d['features']; print(lay,start,len(d['features']),d.get('numberMatched'))
        if len(d['features'])<2000: break
        start+=2000
    fn=f'raw/prodes/{lay}.geojson'; json.dump({'type':'FeatureCollection','features':feats},open(fn,'w'))
    print(fn,len(feats),hashlib.sha256(open(fn,'rb').read()).hexdigest(),datetime.date.today())
