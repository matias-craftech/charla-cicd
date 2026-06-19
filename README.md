# Del commit al deploy

Repo de demo para la charla **"Del commit al deploy — Introducción a CI/CD y pipelines"**.

Es un proyecto Python mínimo que **genera una página estática** (logo + mensaje +
hora del último deploy + commit), la **publica en GitHub Pages** y, en paralelo,
**empaqueta una imagen Docker** que sirve ese mismo contenido. Cada paso del
pipeline corresponde a un concepto de la charla.

---

## El pipeline (`.github/workflows/ci-cd.yml`)

| Job | Pregunta que responde | Concepto |
|-----|------------------------|----------|
| **lint** | ¿El código respeta el estilo? | parte de **CI** |
| **test** | ¿Hace lo que esperamos? | parte de **CI** |
| **build** | Empaquetar el artefacto (el sitio) | fin de **CI** |
| **deploy** | Publicar en GitHub Pages | **CD** |
| **docker** | Imagen portable → GHCR | empaquetado portable |

`lint` y `test` corren primero. Si pasan, `build` arma el sitio y `docker`
construye la imagen (en paralelo). `deploy` publica el sitio, y el push de la
imagen ocurren **solo en `main`** (en un Pull Request el pipeline valida todo
pero no publica nada). Ese "humano que mergea a main" es la decisión de
**Continuous Delivery**; si quitás esa puerta, es **Continuous Deployment**.

---

## Probar en local

```bash
pip install -r requirements.txt   # ruff + pytest

ruff check .            # lint
ruff format --check .   # formato
pytest                  # tests
python build.py         # genera dist/index.html  -> abrilo en el navegador
```

## La demo en vivo

1. Cambiá el `message` por defecto en `app/site_generator.py` (o el texto en `build.py`).
2. `git commit` + `git push` a `main`.
3. Mirá en la pestaña **Actions** cómo se encadenan los jobs.
4. Cuando termina, la página en `https://<usuario>.github.io/<repo>/` muestra el
   cambio con la hora del último deploy.

---

## Configuración en GitHub (una sola vez)

- **Pages**: Settings → Pages → *Build and deployment* → **Source: GitHub Actions**.
- **Permisos**: los jobs ya piden lo mínimo (`pages: write`, `id-token: write`,
  `packages: write`). No hace falta crear secrets: se usa el `GITHUB_TOKEN`
  automático.
- **Imagen Docker (GHCR)**: tras el primer push queda en
  `ghcr.io/<usuario>/<repo>`. Si la querés tirar desde un homelab sin
  autenticarte, marcá el package como **public** (Packages → Package settings).

## Correr la imagen Docker

```bash
docker pull ghcr.io/<usuario>/<repo>:latest
docker run --rm -p 8080:80 ghcr.io/<usuario>/<repo>:latest
# abrir http://localhost:8080
```

> **Homelab:** la imagen es la "unidad portable". El mismo artefacto que corre acá
> corre igual en el homelab; ahí entra el `docker pull` desde el otro lado.
> Si esa parte no se usa, podés borrar el job `docker` del workflow y el
> `Dockerfile` sin afectar el resto.

---

## Versiones de las Actions

Se usan majors estables (`checkout@v4`, `setup-python@v5`, `deploy-pages@v4`,
`build-push-action@v6`, etc.). El ecosistema se mueve rápido, así que está
incluido `.github/dependabot.yml` para que las versiones se actualicen solas.
