"""Baixa imoveis CAR (SICAR WFS publico, camada sicar:sicar_imoveis_mg) por municipio da vitrine -> raw/car/mun/<cod>.geojson (snapshot da data de execucao).
ATENCAO: snapshot atual = geometria vigente (retificacoes sobrescrevem). Idempotente."""
import urllib.parse, json, csv, os, time, datetime, subprocess  # curl: urllib falha no handshake TLS do SICAR
H="https://geoserver.car.gov.br/geoserver/sicar/wfs"
cods=[r['cod_ibge'] for r in csv.DictReader(open('municipios.csv',encoding='utf-8'))]
for c in cods:
    out=f'raw/car/mun/{c}.geojson'
    if os.path.exists(out): continue
    feats=[];s=0
    while True:
        p=dict(service='WFS',version='2.0.0',request='GetFeature',typeNames='sicar:sicar_imoveis_mg',outputFormat='application/json',count=3000,startIndex=s,sortBy='cod_imovel',cql_filter=f'cod_municipio_ibge={c}')
        for t in range(5):
            try: d=json.loads(subprocess.run(['curl','-s','-m','300','-G',H]+sum([['--data-urlencode',f'{k}={v}'] for k,v in p.items()],[]),capture_output=True,check=True).stdout); break
            except Exception as e: print('retry',c,s,repr(e)[:80],flush=True); time.sleep(5)
        else: raise SystemExit('falhou '+c)
        feats+=d['features']
        if len(d['features'])<3000: break
        s+=3000
    json.dump({'type':'FeatureCollection','features':feats,'consulta':str(datetime.date.today())},open(out,'w'))
    print(c,len(feats),flush=True)
