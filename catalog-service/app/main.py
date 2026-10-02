import os

import psycopg
from fastapi import FastAPI
from fastapi.responses import JSONResponse

SERVICE_NAME = "catalog-service"
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://catalog:catalog@localhost:5432/catalog"
)

app = FastAPI(title=SERVICE_NAME, version="0.1.0")


@app.get("/health")
def health():
    # Liveness: процесс запущен и отвечает на HTTP.
    return {"status": "ok", "service": SERVICE_NAME}


@app.get("/health/ready")
def ready():
    # Readiness: сервис может работать со своей БД.
    try:
        with psycopg.connect(DATABASE_URL, connect_timeout=2) as conn:
            conn.execute("SELECT 1")
    except psycopg.Error:
        return JSONResponse(
            status_code=503,
            content={"status": "unavailable", "service": SERVICE_NAME, "db": "down"},
        )
    return {"status": "ok", "service": SERVICE_NAME, "db": "up"}
