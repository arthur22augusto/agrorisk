"""Utilitários de download idempotente com manifesto (URL, parâmetros, data, nº de feições, sha256).

Regras do projeto: dados brutos em `data/raw/<fonte>/<AAAA-MM-DD>/`, nunca no git.
O SICAR falha no handshake TLS com urllib; por isso o transporte usa `curl`.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import subprocess
import time
from pathlib import Path

RAW = Path("data/raw")


def sha256_arquivo(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def curl_json(url: str, params: dict, tentativas: int = 5, timeout: int = 300) -> dict:
    cmd = ["curl", "-s", "-f", "-m", str(timeout), "-G", url]
    for k, v in params.items():
        cmd += ["--data-urlencode", f"{k}={v}"]
    for t in range(tentativas):
        try:
            return json.loads(subprocess.run(cmd, capture_output=True, check=True).stdout)
        except Exception as e:  # noqa: BLE001 - rede instável: repetir
            print(f"  retry {t + 1}/{tentativas}: {repr(e)[:80]}", flush=True)
            time.sleep(2 ** t)
    raise RuntimeError(f"falhou após {tentativas} tentativas: {url} {params}")


def baixar_wfs(url: str, camada: str, saida: Path, *, bbox: str | None = None, cql: str | None = None,
               srs: str | None = None, pagina: int = 3000, ordenar: str | None = None) -> dict:
    """Baixa uma camada WFS paginada para `saida` (GeoJSON). Idempotente: se existir, só confere o hash.
    Retorna o registro de manifesto da camada."""
    saida.parent.mkdir(parents=True, exist_ok=True)
    hits = None
    if not saida.exists():
        base = dict(service="WFS", version="2.0.0", request="GetFeature", typeNames=camada,
                    outputFormat="application/json", count=pagina)
        if bbox: base["bbox"] = bbox
        if cql: base["cql_filter"] = cql
        if srs: base["srsName"] = srs
        if ordenar: base["sortBy"] = ordenar
        feats, ini = [], 0
        while True:
            d = curl_json(url, {**base, "startIndex": ini})
            feats += d["features"]
            hits = d.get("numberMatched", hits)
            if len(d["features"]) < pagina:
                break
            ini += pagina
        tmp = saida.with_suffix(".tmp")
        tmp.write_text(json.dumps({"type": "FeatureCollection", "features": feats}), encoding="utf-8")
        tmp.replace(saida)
    n = len(json.loads(saida.read_text(encoding="utf-8"))["features"])
    return {"arquivo": saida.name, "camada": camada, "url": url, "bbox": bbox, "cql": cql,
            "n_feicoes": n, "number_matched": hits, "sha256": sha256_arquivo(saida),
            "baixado_em": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")}


def gravar_manifesto(pasta: Path, registros: list[dict], extra: dict | None = None) -> str:
    """Grava manifest.json e devolve o hash do snapshot (sha256 dos hashes ordenados por arquivo)."""
    h = hashlib.sha256("".join(r["sha256"] for r in sorted(registros, key=lambda r: r["arquivo"])).encode()).hexdigest()
    (pasta / "manifest.json").write_text(
        json.dumps({"hash_snapshot": h, "arquivos": registros, **(extra or {})}, ensure_ascii=False, indent=1),
        encoding="utf-8")
    return h
