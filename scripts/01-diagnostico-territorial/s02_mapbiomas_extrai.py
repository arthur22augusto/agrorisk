"""Consome raw/cob/MAPBIOMAS_BRAZIL-COL.11-BIOME_STATE_MUNICIPALITY.xlsx e raw/desm_col11.xlsx (MapBiomas Col.11, CC BY 4.0)
Produz mb_cobertura_col11_vitrine.csv e mb_desmat_col11_vitrine.csv (formato original, filtrado aos 50 municipios)."""
import openpyxl, csv
cods={r['cod_ibge'] for r in csv.DictReader(open('municipios.csv',encoding='utf-8'))}
def run(f,sheet,col,out):
    ws=openpyxl.load_workbook(f,read_only=True)[sheet]
    it=ws.iter_rows(values_only=True); h=[str(x) for x in next(it)]
    h=[x for x in h if x!='None']; n=len(h); gi=h.index(col)
    w=csv.writer(open(out,'w',newline='',encoding='utf-8')); w.writerow(h); k=0
    for r in it:
        if r[gi] is not None and str(r[gi]) in cods: w.writerow(r[:n]); k+=1
    print(out,k)
run('raw/cob/MAPBIOMAS_BRAZIL-COL.11-BIOME_STATE_MUNICIPALITY.xlsx','COVERAGE_11','geocode','mb_cobertura_col11_vitrine.csv')
run('raw/desm_col11.xlsx','ANNUAL_DEFORESTATION','GEOCODE','mb_desmat_col11_vitrine.csv')
