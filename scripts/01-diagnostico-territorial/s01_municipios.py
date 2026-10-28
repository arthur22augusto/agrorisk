"""Consome: SIDRA 4714 (Censo 2022 pop/area), 5938 (PIB/VAB), 3939 (PPM rebanho), 5457 (PAM valor).
Produz: municipios.csv. Data da consulta registrada no relatorio. Sem dados no git."""
import json, csv, unicodedata, urllib.request, datetime
def norm(s): return unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower().strip()
RMBH="Baldim,Belo Horizonte,Betim,Brumadinho,Caeté,Capim Branco,Confins,Contagem,Esmeraldas,Florestal,Ibirité,Igarapé,Itaguara,Itatiaiuçu,Jaboticatubas,Juatuba,Lagoa Santa,Mário Campos,Mateus Leme,Matozinhos,Nova Lima,Nova União,Pedro Leopoldo,Raposos,Ribeirão das Neves,Rio Acima,Rio Manso,Sabará,Santa Luzia,São Joaquim de Bicas,São José da Lapa,Sarzedo,Taquaraçu de Minas,Vespasiano".split(',')
COLAR="Barão de Cocais,Belo Vale,Bom Jesus do Amparo,Bonfim,Fortuna de Minas,Funilândia,Inhaúma,Itabirito,Itaúna,Moeda,Pará de Minas,Prudente de Morais,Santa Bárbara,São Gonçalo do Rio Abaixo,São José da Varginha,Sete Lagoas".split(',')
assert len(RMBH)==34 and len(COLAR)==16
grupo={norm(n):'RMBH' for n in RMBH}; grupo.update({norm(n):'Colar' for n in COLAR})
def sidra(path):
    return json.load(urllib.request.urlopen("https://apisidra.ibge.gov.br/values/"+path,timeout=120))[1:]
rows={}
for r in sidra("t/4714/n6/in%20n3%2031/v/93,6318/p/2022"):
    import re; nm=re.sub(r'( \(MG\)| - MG)$','',r['D1N']); k=norm(nm)
    if k in grupo:
        d=rows.setdefault(r['D1C'],{'cod_ibge':r['D1C'],'municipio':nm,'grupo':grupo[k]})
        d['pop_2022' if r['D2C']=='93' else 'area_km2']=r['V']
assert len(rows)==50,len(rows)
cods=",".join(rows)
def add(path,fn):
    for r in sidra(path):
        fn(rows[r['D1C']],r)
add(f"t/5938/n6/{cods}/v/37/p/2023",lambda d,r:d.__setitem__('pib_2023_mil_reais',r['V']))
add(f"t/5938/n6/{cods}/v/513,37/p/2021",lambda d,r:d.__setitem__('vab_agro_2021_mil_reais' if r['D2C']=='513' else 'pib_2021_mil_reais',r['V']))
add(f"t/3939/n6/{cods}/v/105/c79/2670/p/2024",lambda d,r:d.__setitem__('bovinos_2024_cab',r['V']))
add(f"t/5457/n6/{cods}/v/215/p/2023/c782/0",lambda d,r:d.__setitem__("pam_valor_prod_2023_mil_reais",r["V"]))
cols=['cod_ibge','municipio','grupo','pop_2022','area_km2','pib_2021_mil_reais','vab_agro_2021_mil_reais','pib_2023_mil_reais','bovinos_2024_cab','pam_valor_prod_2023_mil_reais']
out=sorted(rows.values(),key=lambda d:(d['grupo'],d['municipio']))
w=csv.DictWriter(open('municipios.csv','w',newline='',encoding='utf-8'),cols); w.writeheader(); w.writerows(out)
print(len(out),datetime.date.today())
