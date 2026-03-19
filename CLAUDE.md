# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Equipment/material reservation management API (Sistema de Reserves) built with FastAPI and MariaDB. Written in Catalan. Three domain entities: Usuaris (users), Materials (equipment), Reserves (reservations).

## Commands

### Run locally
```bash
# From project root
uvicorn API.main:app --host 0.0.0.0 --reload --port 8443 --ssl-keyfile ./API/ssl/key.pem --ssl-certfile ./API/ssl/cert.pem
```

### Docker deployment
```bash
docker network create -d bridge xarxa_docker1  # required external network
docker-compose up -d --build
docker logs reservesapi
```

### Install dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --no-cache-dir -r API/requirements.txt
```

### Generate SSL certificates
```bash
openssl req -x509 -newkey rsa:4096 -keyout ./API/ssl/key.pem -out ./API/ssl/cert.pem -days 3650 -nodes
```

## Architecture

- **Flat structure**: All API endpoints defined directly in `API/main.py` (no routers/blueprints)
- **No ORM**: Direct SQL queries via `mysql-connector-python` — no SQLAlchemy
- **Database connections**: `API/db.py` provides `get_db_connection()` returning raw MySQL connections (connection pooling is commented out due to OpenTelemetry compatibility issues)
- **Models**: Pydantic models in `API/models.py` for request validation only (Usuari, Material, Reserva)
- **OpenTelemetry**: Tracing configured in `main.py` — OTLP exporter sends to Alloy at `http://alloy:4317`, plus console exporter. FastAPI and MySQL are both instrumented.
- **HTTPS only**: Runs on port 443 in Docker with self-signed SSL certs in `API/ssl/`
- **Docker networking**: Container joins external network `xarxa_docker1` to reach MariaDB and Alloy

## REST Endpoints

- `/usuaris/` — CRUD for users, `/login/{usuari}` for lookup by name
- `/materials/` — Full CRUD for materials
- `/reserves/` — CRUD for reservations (composite key: idusuari + idmaterial + datareserva). GET joins with materials table to include description/image.

## Database

MariaDB database `reserves` with tables: `usuaris`, `materials`, `reserves`. Connection config is hardcoded in `API/db.py`. Sample SQL for table creation is in README.md.
