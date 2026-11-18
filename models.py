from sqlmodel import Field, Relationship, SQLModel


class Categoria(SQLModel, table=True):
    __tablename__ = "categorias"

    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=50, unique=True, index=True)

    videojuegos: list["Videojuego"] = Relationship(back_populates="categoria")


class Videojuego(SQLModel, table=True):
    __tablename__ = "videojuegos"

    id: int | None = Field(default=None, primary_key=True)
    titulo: str = Field(max_length=100, index=True)
    plataforma: str = Field(max_length=50)
    precio: float
    stock: int = 0
    categoria_id: int | None = Field(default=None, foreign_key="categorias.id")

    categoria: Categoria | None = Relationship(back_populates="videojuegos")
