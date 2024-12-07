from sqlalchemy import VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from src.database.model.base import BaseModel


class Region(BaseModel):
    __tablename__ = "region"

    region_name: Mapped[str] = mapped_column(
        VARCHAR(50),
        unique=True,
        nullable=False,
    )
