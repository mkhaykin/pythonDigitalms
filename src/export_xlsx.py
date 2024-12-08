import logging

import pandas as pd
from sqlalchemy import Engine, Select, func, select

from src.database.model.company import Company
from src.database.model.overdue import Overdue
from src.database.model.position import Position
from src.database.model.region import Region

logger = logging.getLogger(__name__)


def export_to_xlsx(engine: Engine, file_name: str, sheet_name: str) -> None:
    logger.info("Экспорт данных: начат.")
    _to_xlsx(engine, file_name, sheet_name)
    logger.info("Экспорт данных: закончен.")


def _to_xlsx(engine: Engine, file_name: str, sheet_name: str) -> None:
    with engine.connect() as con:
        df = pd.read_sql(
            sql=_select_stmt(),
            con=con,
        )
        df.to_excel(
            file_name,
            sheet_name=sheet_name,
            index=False,
            header=[
                "Субъект РФ",
                "Количество Доз",
                "Просрочено дней",
            ],
        )


def _select_stmt() -> Select:
    return (
        select(
            Region.region_name,
            func.sum(Overdue.pack_count * Position.count_doses_per_pack).label(
                "sum_count_packs",
            ),
            func.round(func.avg(Position.days_overdue)).label("avg_days_overdue"),
        )
        .select_from(Overdue)
        .join(
            target=Company,
        )
        .join(
            target=Region,
        )
        .join(
            target=Position,
        )
        .group_by(
            Region.region_name,
        )
        .order_by(Region.region_name)
    )
