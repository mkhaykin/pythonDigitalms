from uuid import UUID

from sqlalchemy import ForeignKey, UniqueConstraint
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
        # TODO: возможно есть проблема с входными данными unique=True,
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "region_id",
            "company_inn",
            name="unique_company",
        ),
    )
