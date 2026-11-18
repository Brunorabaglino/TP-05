from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session

import crud
import schemas
from database import get_session

app = FastAPI(title="Tienda de Videojuegos")


@app.get("/")
def root():
    return {"mensaje": "API de la tienda de videojuegos andando"}


@app.post("/categorias", response_model=schemas.CategoriaRead)
def crear_categoria(categoria: schemas.CategoriaCreate, session: Session = Depends(get_session)):
    if crud.get_categoria_por_nombre(session, categoria.nombre):
        raise HTTPException(status_code=400, detail="Ya existe una categoria con ese nombre")
    return crud.crear_categoria(session, categoria)


@app.get("/categorias", response_model=list[schemas.CategoriaRead])
def listar_categorias(session: Session = Depends(get_session)):
    return crud.get_categorias(session)


@app.get("/categorias/{categoria_id}", response_model=schemas.CategoriaConVideojuegos)
def obtener_categoria(categoria_id: int, session: Session = Depends(get_session)):
    db_categoria = crud.get_categoria(session, categoria_id)
    if not db_categoria:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    return db_categoria


@app.post("/videojuegos", response_model=schemas.VideojuegoRead)
def crear_videojuego(videojuego: schemas.VideojuegoCreate, session: Session = Depends(get_session)):
    if videojuego.categoria_id is not None:
        if not crud.get_categoria(session, videojuego.categoria_id):
            raise HTTPException(status_code=404, detail="La categoria indicada no existe")
    return crud.crear_videojuego(session, videojuego)


@app.get("/videojuegos", response_model=list[schemas.VideojuegoRead])
def listar_videojuegos(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    return crud.get_videojuegos(session, skip, limit)


@app.get("/videojuegos/{videojuego_id}", response_model=schemas.VideojuegoRead)
def obtener_videojuego(videojuego_id: int, session: Session = Depends(get_session)):
    db_videojuego = crud.get_videojuego(session, videojuego_id)
    if not db_videojuego:
        raise HTTPException(status_code=404, detail="Videojuego no encontrado")
    return db_videojuego


@app.put("/videojuegos/{videojuego_id}", response_model=schemas.VideojuegoRead)
def actualizar_videojuego(videojuego_id: int, cambios: schemas.VideojuegoUpdate, session: Session = Depends(get_session)):
    if cambios.categoria_id is not None:
        if not crud.get_categoria(session, cambios.categoria_id):
            raise HTTPException(status_code=404, detail="La categoria indicada no existe")
    db_videojuego = crud.actualizar_videojuego(session, videojuego_id, cambios)
    if not db_videojuego:
        raise HTTPException(status_code=404, detail="Videojuego no encontrado")
    return db_videojuego


@app.delete("/videojuegos/{videojuego_id}")
def eliminar_videojuego(videojuego_id: int, session: Session = Depends(get_session)):
    db_videojuego = crud.eliminar_videojuego(session, videojuego_id)
    if not db_videojuego:
        raise HTTPException(status_code=404, detail="Videojuego no encontrado")
    return {"mensaje": f"Videojuego '{db_videojuego.titulo}' eliminado"}
