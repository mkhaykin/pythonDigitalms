from sqlalchemy import VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from src.database.model.base import BaseModel


class Status(BaseModel):
    __tablename__ = "status"

    status_name: Mapped[str] = mapped_column(
        VARCHAR(50),
        unique=True,
        nullable=False,
    )
