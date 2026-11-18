from sqlmodel import Session, select

from models import Categoria, Videojuego
from schemas import CategoriaCreate, VideojuegoCreate, VideojuegoUpdate


def get_categorias(session: Session):
    return session.exec(select(Categoria)).all()


def get_categoria(session: Session, categoria_id: int):
    return session.get(Categoria, categoria_id)


def get_categoria_por_nombre(session: Session, nombre: str):
    return session.exec(select(Categoria).where(Categoria.nombre == nombre)).first()


def crear_categoria(session: Session, categoria: CategoriaCreate):
    db_categoria = Categoria.model_validate(categoria)
    session.add(db_categoria)
    session.commit()
    session.refresh(db_categoria)
    return db_categoria


def get_videojuegos(session: Session, skip: int = 0, limit: int = 100):
    return session.exec(select(Videojuego).offset(skip).limit(limit)).all()


def get_videojuego(session: Session, videojuego_id: int):
    return session.get(Videojuego, videojuego_id)


def crear_videojuego(session: Session, videojuego: VideojuegoCreate):
    db_videojuego = Videojuego.model_validate(videojuego)
    session.add(db_videojuego)
    session.commit()
    session.refresh(db_videojuego)
    return db_videojuego


def actualizar_videojuego(session: Session, videojuego_id: int, cambios: VideojuegoUpdate):
    db_videojuego = get_videojuego(session, videojuego_id)
    if not db_videojuego:
        return None

    db_videojuego.sqlmodel_update(cambios.model_dump(exclude_unset=True))
    session.add(db_videojuego)
    session.commit()
    session.refresh(db_videojuego)
    return db_videojuego


def eliminar_videojuego(session: Session, videojuego_id: int):
    db_videojuego = get_videojuego(session, videojuego_id)
    if not db_videojuego:
        return None

    session.delete(db_videojuego)
    session.commit()
    return db_videojuego
