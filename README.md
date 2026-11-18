# Tienda de Videojuegos - TP5

API con FastAPI, SQLModel y Alembic.

## Como correrlo

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn main:app --reload
```

Si ya tenias un `tienda.db` del TP4 borralo antes de correr las migraciones.

La documentacion queda en http://127.0.0.1:8000/docs

## Migraciones

```
alembic revision --autogenerate -m "mensaje"
alembic upgrade head
alembic downgrade -1
```
