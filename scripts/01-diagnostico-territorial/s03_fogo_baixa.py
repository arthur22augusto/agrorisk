"""Le cicatrizes de fogo MapBiomas Fogo Col.5 (FlatGeobuf anual, via /vsicurl/ com bbox da vitrine) -> raw/fogo/fogo_AAAA.gpkg."""
import pyogrio, sys, os
BB=(-44.8,-20.52,-43.19,-19.05)
base="/vsicurl/https://storage.googleapis.com/mapbiomas-public/initiatives/brasil/collection_10/fire-col5/annual_burned_vectors_v1/FlatGeobuf/mapbiomas_fire_collection5_burned_area_%d.fgb"
for y in [int(a) for a in sys.argv[1:]]:
    out=f'raw/fogo/fogo_{y}.gpkg'
    if os.path.exists(out): continue
    try:
        g=pyogrio.read_dataframe(base%y,bbox=BB); g.to_file(out,driver='GPKG'); print(y,len(g),list(g.columns)[:12],flush=True)
    except Exception as e: print(y,'ERRO',repr(e)[:300],flush=True)
