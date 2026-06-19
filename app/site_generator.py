"""Genera la página estática que publica el pipeline.

La idea de mantener esto como funciones puras (le pasás datos, te devuelve
HTML, sin tocar disco ni red) es que los tests salen triviales. Eso es justo
lo que hace que el job de "test" del pipeline tenga sentido.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

ASSETS = Path(__file__).parent / "assets"


def load_logo() -> str:
    """Lee el SVG del logo para incrustarlo en la página."""
    return (ASSETS / "logo.svg").read_text(encoding="utf-8")


def render_page(
    deploy_time: datetime | None = None,
    message: str = "¡El pipeline funcionó!",
    commit: str = "local",
) -> str:
    """Devuelve el HTML completo del sitio.

    deploy_time: momento del deploy (por defecto, ahora en UTC).
    message:     texto principal, fácil de cambiar para la demo en vivo.
    commit:      hash corto del commit que disparó el deploy.
    """
    if deploy_time is None:
        deploy_time = datetime.now(UTC)
    stamp = deploy_time.strftime("%Y-%m-%d %H:%M UTC")
    logo = load_logo()
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Del commit al deploy</title>
<style>
  body {{
    margin: 0;
    font-family: system-ui, sans-serif;
    background: #fff;
    color: #15171c;
    display: grid;
    place-items: center;
    min-height: 100vh;
  }}
  .card {{ text-align: center; padding: 2.5rem; }}
  .logo {{ width: 120px; height: 120px; margin: 0 auto 1.5rem; }}
  h1 {{ font-size: 2rem; margin: 0.2rem 0; color: #2f63b8; }}
  .msg {{ font-size: 1.25rem; margin: 0.6rem 0 1.6rem; }}
  .meta {{
    font-family: ui-monospace, monospace;
    color: #5b6470;
    font-size: 0.95rem;
    line-height: 1.8;
  }}
  .meta b {{ color: #15171c; }}
  .amber {{ color: #e6aa49; }}
</style>
</head>
<body>
  <div class="card">
    <div class="logo">{logo}</div>
    <h1>Del commit al deploy</h1>
    <p class="msg">{message}</p>
    <p class="meta">
      último deploy: <b>{stamp}</b><br>
      commit: <b class="amber">{commit}</b>
    </p>
  </div>
</body>
</html>
"""
