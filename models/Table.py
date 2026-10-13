from typing import Optional
from sqlmodel import Field, SQLModel


class Table(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    numero: int = Field(unique=True, index=True)
    capacidad: int
    estado: str = Field(default="disponible")