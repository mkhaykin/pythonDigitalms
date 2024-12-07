from datetime import date

from sqlalchemy import DATE, INTEGER, VARCHAR, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.database.model.base import BaseModel


class Position(BaseModel):
    __tablename__ = "position"

    gtin: Mapped[str] = mapped_column(
        VARCHAR(14),
        unique=True,
        nullable=False,
    )

    series: Mapped[str] = mapped_column(
        VARCHAR(30),
        nullable=False,
    )

    count_doses_per_pack: Mapped[int] = mapped_column(
        INTEGER,
        nullable=False,
        default=1,
    )

    expiration: Mapped[date] = mapped_column(
        DATE,
        nullable=False,
    )

    days_overdue: Mapped[int] = mapped_column(INTEGER)

    __table_args__ = (
        CheckConstraint(
            "count_doses_per_pack > 0",
            name="check__position__count_doses_per_pack",
        ),
    )
