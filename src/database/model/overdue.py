from uuid import UUID

from sqlalchemy import INTEGER, CheckConstraint, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.database.model.base import BaseModel
from src.database.model.company import Company
from src.database.model.position import Position
from src.database.model.status import Status
from src.database.model.status_type import StatusType


class Overdue(BaseModel):
    __tablename__ = "overdue"

    company_id: Mapped[UUID] = mapped_column(
        ForeignKey(Company.id),
        nullable=False,
    )

    status_id: Mapped[UUID] = mapped_column(
        ForeignKey(Status.id),
        nullable=False,
    )
    status_type_id: Mapped[UUID] = mapped_column(
        ForeignKey(StatusType.id),
        nullable=False,
    )

    position_id: Mapped[UUID] = mapped_column(
        ForeignKey(Position.id),
        nullable=False,
    )

    pack_count: Mapped[int] = mapped_column(
        INTEGER,
        nullable=False,
    )

    __table_args__ = (
        CheckConstraint("pack_count > 0", name="check__overdue__pack_count"),
        UniqueConstraint(
            "company_id",
            "position_id",
            "pack_count",
            name="unique_overdue",
        ),
    )
