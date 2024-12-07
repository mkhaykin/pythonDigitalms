from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from src.database.model.base import BaseModel
from src.database.model.region import Region


class Company(BaseModel):
    __tablename__ = "company"

    region_id: Mapped[UUID] = mapped_column(ForeignKey(Region.id))

    company_name: Mapped[str] = mapped_column(
        VARCHAR(250),
        nullable=False,
    )

    company_inn: Mapped[str] = mapped_column(
        VARCHAR(12),
        unique=True,
        nullable=False,
    )
