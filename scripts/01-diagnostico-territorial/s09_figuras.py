"""Figuras da sessao 01. Consome y_totais_anuais_vitrine.csv, poder_imovel_prodes.csv. Produz reports/figuras/01-*.png"""
import pandas as pd, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
O='/home/user/agrorisk/reports/figuras/'
y=pd.read_csv('y_totais_anuais_vitrine.csv').set_index('serie'); y.columns=y.columns.astype(int)
fig,ax=plt.subplots(figsize=(8,4))
ax.plot(y.columns,y.iloc[0],marker='o',label='MapBiomas Col.11 (perda de veg. nativa)')
ax.plot(y.columns,y.iloc[1],marker='s',label='PRODES Cerrado + Mata Atlântica')
ax.set_ylabel('ha/ano'); ax.set_title('Supressão de vegetação nativa — vitrine (50 municípios)'); ax.legend(); ax.set_ylim(0)
fig.text(0.01,0.01,'Fontes: MapBiomas Col.11; INPE/TerraBrasilis PRODES. Consulta 2026-10-28.',fontsize=7)
fig.tight_layout(rect=(0,0.03,1,1)); fig.savefig(O+'01-supressao-anual-vitrine.png',dpi=130)
p=pd.read_csv('poder_imovel_prodes.csv'); p=p[p.year<=2025]
fig,ax=plt.subplots(figsize=(8,4))
ax.bar(p.year-0.2,p.imoveis_ge_0,0.4,label='≥1 polígono PRODES'); ax.bar(p.year+0.2,p.imoveis_ge_1ha,0.4,label='≥1 ha suprimido')
ax.set_ylabel('imóveis CAR com evento'); ax.set_title('Eventos PRODES por imóvel CAR (41.0 mil imóveis; geometria atual)'); ax.legend()
fig.text(0.01,0.01,'Fontes: SICAR (snapshot 2026-10-28) × INPE PRODES. Cálculo em EPSG:31983.',fontsize=7)
fig.tight_layout(rect=(0,0.03,1,1)); fig.savefig(O+'01-imoveis-com-evento-prodes.png',dpi=130)
