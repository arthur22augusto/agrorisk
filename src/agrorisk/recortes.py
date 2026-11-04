"""Recortes territoriais do AgroRisk (decisão 0001 / escopo-mvp §5).

- vitrine: RMBH (34) + Colar Metropolitano (16, inclui Sete Lagoas) = 50 municípios.
- treino: vitrine + mesorregião Metropolitana de BH (IBGE 3107) + Central Mineira (3106).

Os códigos IBGE vêm do SIDRA (tabela 4714, Censo 2022) em tempo de execução, com cache em
`data/interim/recortes/`. Consome: apisidra.ibge.gov.br. Produz: lista de códigos de 7 dígitos.
"""
from __future__ import annotations

import json
import re
import unicodedata
import urllib.request
from pathlib import Path

RMBH = (
    "Baldim,Belo Horizonte,Betim,Brumadinho,Caeté,Capim Branco,Confins,Contagem,Esmeraldas,Florestal,"
    "Ibirité,Igarapé,Itaguara,Itatiaiuçu,Jaboticatubas,Juatuba,Lagoa Santa,Mário Campos,Mateus Leme,"
    "Matozinhos,Nova Lima,Nova União,Pedro Leopoldo,Raposos,Ribeirão das Neves,Rio Acima,Rio Manso,"
    "Sabará,Santa Luzia,São Joaquim de Bicas,São José da Lapa,Sarzedo,Taquaraçu de Minas,Vespasiano"
).split(",")
COLAR = (
    "Barão de Cocais,Belo Vale,Bom Jesus do Amparo,Bonfim,Fortuna de Minas,Funilândia,Inhaúma,Itabirito,"
    "Itaúna,Moeda,Pará de Minas,Prudente de Morais,Santa Bárbara,São Gonçalo do Rio Abaixo,"
    "São José da Varginha,Sete Lagoas"
).split(",")
MESORREGIOES_TREINO = {"3107": "Metropolitana de Belo Horizonte", "3106": "Central Mineira"}
assert len(RMBH) == 34 and len(COLAR) == 16


def _norm(s: str) -> str:
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower().strip()


def _sidra(caminho: str) -> list[dict]:
    url = "https://apisidra.ibge.gov.br/values/" + caminho
    with urllib.request.urlopen(url, timeout=120) as r:
        return json.load(r)[1:]


def _nome(r: dict) -> str:
    return re.sub(r"( \(MG\)| - MG)$", "", r["D1N"])


def municipios(recorte: str, cache: Path = Path("data/interim/recortes")) -> dict[str, dict]:
    """Retorna {cod_ibge: {municipio, grupo}} do recorte ('vitrine' ou 'treino')."""
    if recorte not in ("vitrine", "treino"):
        raise ValueError("recorte deve ser 'vitrine' ou 'treino'")
    arq = cache / f"{recorte}.json"
    if arq.exists():
        return json.loads(arq.read_text(encoding="utf-8"))
    grupos = {_norm(n): "RMBH" for n in RMBH} | {_norm(n): "Colar" for n in COLAR}
    out: dict[str, dict] = {}
    for r in _sidra("t/4714/n6/in%20n3%2031/v/93/p/2022"):
        if (k := _norm(_nome(r))) in grupos:
            out[r["D1C"]] = {"municipio": _nome(r), "grupo": grupos[k]}
    assert len(out) == 50, f"vitrine deveria ter 50 municípios, achei {len(out)}"
    if recorte == "treino":
        for cod_meso, nome_meso in MESORREGIOES_TREINO.items():
            for r in _sidra(f"t/4714/n6/in%20n8%20{cod_meso}/v/93/p/2022"):
                out.setdefault(r["D1C"], {"municipio": _nome(r), "grupo": "meso " + nome_meso})
    cache.mkdir(parents=True, exist_ok=True)
    arq.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    return out
