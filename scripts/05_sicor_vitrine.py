"""Sessão 05 — consulta a Matriz de Dados do Crédito Rural (BCB/SICOR) para a vitrine.

Consome : API OData do BCB (https://olinda.bcb.gov.br/olinda/servico/SICOR/versao/v2/odata)
          entidades CusteioMunicipioProduto e InvestMunicipioProduto (agregado por município x produto x mês).
Produz  : data/interim/sicor_vitrine_ano.csv (município x ano x finalidade; ignorado pelo git)
Data de execução registrada no CSV. Lista de municípios PROVISÓRIA (RMBH 34 + Sete Lagoas);
a lista oficial (incl. Colar Metropolitano) será fixada na sessão 01.
Não usa CRS (dado tabular).
"""
import json, sys, time, urllib.parse, urllib.request, datetime, collections, csv, pathlib

BASE = "https://olinda.bcb.gov.br/olinda/servico/SICOR/versao/v2/odata"
MUN = """BALDIM|BELO HORIZONTE|BETIM|BRUMADINHO|CAETÉ|CONFINS|CONTAGEM|ESMERALDAS|IBIRITÉ|IGARAPÉ|ITAGUARA|ITATIAIUÇU|JABOTICATUBAS|JUATUBA|LAGOA SANTA|MÁRIO CAMPOS|MATEUS LEME|MATOZINHOS|NOVA LIMA|NOVA UNIÃO|PEDRO LEOPOLDO|RAPOSOS|RIBEIRÃO DAS NEVES|RIO ACIMA|RIO MANSO|SABARÁ|SANTA LUZIA|SÃO JOAQUIM DE BICAS|SÃO JOSÉ DA LAPA|SARZEDO|TARAQUAÇU DE MINAS|VESPASIANO|CAPIM BRANCO|FLORESTAL|SETE LAGOAS""".split("|")
MUN[MUN.index("TARAQUAÇU DE MINAS")] = "TAQUARAÇU DE MINAS"

def get(url, tries=5):
    for i in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=90) as r:
                return json.load(r)["value"]
        except Exception as e:
            time.sleep(2 * (i + 1)); err = e
    raise err

def pull(ent, campo, mun):
    out, skip = [], 0
    while True:
        q = urllib.parse.urlencode({"$format": "json", "$top": 3000, "$select": f"AnoEmissao,{campo},cdPrograma,cdFonteRecurso",                                     "$filter": f"Municipio eq '{mun}' and cdEstado eq '12'"}, quote_via=lambda x, safe="", *a, **k: urllib.parse.quote(x, safe="$,"))
        if skip: q += f"&$skip={skip}"
        v = get(f"{BASE}/{ent}?{q}")
        out += v
        if len(v) < 3000: return out
        skip += 3000

if __name__ == "__main__":
    agg = collections.defaultdict(lambda: [0, 0.0])
    achados = {}
    for m in MUN:
        for ent, campo, fin in (("CusteioMunicipioProduto", "VlCusteio", "custeio"),
                                ("InvestMunicipioProduto", "VlInvest", "investimento")):
            rows = pull(ent, campo, m)
            achados[(m, fin)] = len(rows)
            for r in rows:
                v = r.get(campo) or 0
                a = agg[(m, r["AnoEmissao"], fin)]; a[0] += 1; a[1] += v
        print(m, achados[(m, "custeio")], achados[(m, "investimento")], file=sys.stderr)
    p = pathlib.Path("data/interim"); p.mkdir(parents=True, exist_ok=True)
    hoje = datetime.date.today().isoformat()
    with open(p / "sicor_vitrine_ano.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["municipio", "ano", "finalidade", "n_registros_agregados", "valor_brl", "consulta_em"])
        for (m, a, fin), (n, v) in sorted(agg.items()): w.writerow([m, a, fin, n, round(v, 2), hoje])
