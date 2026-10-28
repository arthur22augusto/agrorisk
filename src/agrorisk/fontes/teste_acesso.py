"""Teste de acesso a endpoints de bases públicas (sessão 02).

Consome: lista ENDPOINTS abaixo (ou um JSON passado em --endpoints).
Produz: tabela Markdown com status HTTP, tipo de conteúdo e tamanho declarado.

Não baixa bases: usa HEAD e, se o servidor rejeitar, GET com Range de 1 KB.
Uso: python -m agrorisk.fontes.teste_acesso [--saida docs/pesquisa/02-teste-acesso.md]
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import urllib.error
import urllib.request

TIMEOUT_S = 20
UA = "agrorisk-teste-acesso/0.1 (+https://github.com/arthur22augusto/agrorisk)"

# (base, url) — preencher/estender conforme docs/pesquisa/02-catalogo-bases.md
ENDPOINTS: list[tuple[str, str]] = [
    ("dados.gov.br", "https://dados.gov.br"),
    ("SICAR (portal)", "https://www.car.gov.br"),
    ("BCB dados abertos (SICOR)", "https://dadosabertos.bcb.gov.br"),
    ("IBGE (portal)", "https://www.ibge.gov.br"),
    ("IBAMA servicos", "https://servicos.ibama.gov.br"),
    ("TerraBrasilis (INPE)", "https://terrabrasilis.dpi.inpe.br"),
    ("IDE-Sisema", "https://idesisema.meioambiente.mg.gov.br"),
]


def testar(url: str) -> tuple[str, str, str]:
    """Retorna (status, content-type, tamanho) sem baixar o corpo."""
    for metodo, extra in (("HEAD", {}), ("GET", {"Range": "bytes=0-1023"})):
        req = urllib.request.Request(url, method=metodo, headers={"User-Agent": UA, **extra})
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT_S) as r:
                return (str(r.status), r.headers.get("Content-Type", ""), r.headers.get("Content-Length", ""))
        except urllib.error.HTTPError as e:
            if metodo == "GET" or e.code not in (403, 405, 501):
                return (str(e.code), "", "")
        except Exception as e:  # timeout, DNS, TLS
            return (f"erro: {type(e).__name__}", "", "")
    return ("?", "", "")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--endpoints", help="JSON [[base, url], ...] substitui a lista padrão")
    ap.add_argument("--saida", help="arquivo Markdown de saída (padrão: stdout)")
    a = ap.parse_args()
    eps = json.load(open(a.endpoints, encoding="utf-8")) if a.endpoints else ENDPOINTS
    linhas = [
        f"# Teste de acesso — {dt.date.today().isoformat()}",
        "",
        "| Base | URL | Status | Content-Type | Bytes |",
        "|---|---|---|---|---|",
    ]
    for base, url in eps:
        st, ct, n = testar(url)
        linhas.append(f"| {base} | {url} | {st} | {ct} | {n} |")
    texto = "\n".join(linhas) + "\n"
    if a.saida:
        open(a.saida, "w", encoding="utf-8").write(texto)
    else:
        sys.stdout.write(texto)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
