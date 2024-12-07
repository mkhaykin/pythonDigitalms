from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from src.database.model.base import BaseModel


class StatusType(BaseModel):
    __tablename__ = "status_type"

    status_type_name: Mapped[str] = mapped_column(
        VARCHAR(50),
        unique=True,
        nullable=False,
    )
