# Imagen multi-stage: primero construimos el sitio con Python,
# despues lo servimos con un nginx chiquito. La imagen final no lleva Python.

# --- stage 1: build ---
FROM python:3.12-slim AS build
WORKDIR /app
COPY app/ app/
COPY build.py .
RUN python build.py

# --- stage 2: runtime (sirve contenido estatico) ---
FROM nginx:1.27-alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
