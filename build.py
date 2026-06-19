"""Genera el sitio estático en ./dist (esto es el job de "build").

Sin dependencias externas: solo la librería estándar. Así la imagen Docker
no necesita instalar nada para construir el sitio.
"""

from __future__ import annotations

import os
from datetime import UTC, datetime
from pathlib import Path

from app.site_generator import render_page

DIST = Path("dist")


def main() -> None:
    DIST.mkdir(exist_ok=True)
    commit = (os.environ.get("GITHUB_SHA", "") or "local")[:7]
    html = render_page(deploy_time=datetime.now(UTC), commit=commit)
    (DIST / "index.html").write_text(html, encoding="utf-8")
    print(f"OK: dist/index.html generado (commit {commit})")


if __name__ == "__main__":
    main()
