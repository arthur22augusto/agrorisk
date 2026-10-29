"""Versão do modelo: semver + hash do git."""
import json
import os
import subprocess
from importlib import metadata
from pathlib import Path

VERSAO_STUB = "0.1.0-stub"


def hash_git() -> str:
    """Hash curto do commit. Ordem: env AGRORISK_GIT_HASH, direct_url.json (uv add git+…), git local."""
    env = os.environ.get("AGRORISK_GIT_HASH")
    if env:
        return env[:12]
    try:
        txt = metadata.distribution("agrorisk").read_text("direct_url.json")
        if txt:
            commit = json.loads(txt).get("vcs_info", {}).get("commit_id")
            if commit:
                return commit[:12]
    except metadata.PackageNotFoundError:
        pass
    try:
        raiz = Path(__file__).resolve().parents[3]
        out = subprocess.run(
            ["git", "-C", str(raiz), "rev-parse", "--short=12", "HEAD"],
            capture_output=True, text=True, timeout=5, check=True,
        )
        return out.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return "desconhecido"


def versao_modelo() -> str:
    return f"{VERSAO_STUB}+{hash_git()}"
