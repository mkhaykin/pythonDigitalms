import logging

import pandas as pd
from sqlalchemy import (
    Engine,
    Insert,
    Select,
    and_,
    column,
    delete,
    exists,
    func,
    insert,
    select,
    table,
)
from sqlalchemy.orm import Session, sessionmaker

from src.database.connection.utils import drop_table
from src.database.model.company import Company
from src.database.model.overdue import Overdue
from src.database.model.position import Position
from src.database.model.region import Region
from src.database.model.status import Status
from src.database.model.status_type import StatusType

logger = logging.getLogger(__name__)


def import_from_xlsx(
    engine: Engine,
    filename: str,
    sheet_name: str,
) -> None:
    logger.info("Загрузка данных: начат.")
    tmp_table_name = "tmp_table"
    _xlsx_to_tmp(engine, filename, sheet_name, tmp_table_name)
    _tmp_to_tables(sessionmaker(engine)(), tmp_table_name)
    drop_table(tmp_table_name)
    logger.info("Загрузка данных: закончен.")


def _xlsx_to_tmp(
    engine: Engine,
    filename: str,
    sheet_name: str,
    tmp_table_name: str,
) -> None:
    names = [
        "region_name",
        "company_name",
        "company_inn",
        "status",
        "type",
        "gtin",
        "series",
        "count_doses_per_pack",
        "pack_count",
        "count_doses_summary",
        "expiration",
        "days_overdue",
    ]

    dtypes = {
        "region_name": Region.region_name.type,
        "company_name": Company.company_name.type,
        "company_inn": Company.company_inn.type,
        "status": Status.status_name.type,
        "type": StatusType.status_type_name.type,
        "gtin": Position.gtin.type,
        "series": Position.series.type,
        "doses": Position.count_doses_per_pack.type,
        "pack_count": Overdue.pack_count.type,
        "count_doses_summary": Overdue.pack_count.type,  # поле игнорируем
        "expiration": Position.expiration.type,
        "days_overdue": Position.days_overdue.type,
    }

    df = pd.read_excel(
        io=filename,
        sheet_name=sheet_name,
        header=None,
        names=names,
        skiprows=5,
        converters={"expiration": lambda x: pd.to_datetime(x, dayfirst=True)},
    )

    df.to_sql(
        name=tmp_table_name,
        con=engine,
        schema="public",
        dtype=dtypes,
        if_exists="replace",
        method="multi",
    )


def _tmp_to_tables(session: Session, tmp_table_name: str) -> None:
    try:
        session.execute(_insert_region_stmt(tmp_table_name))
        session.execute(_insert_status_stmt(tmp_table_name))
        session.execute(_insert_type_stmt(tmp_table_name))
        session.execute(_insert_company_stmt(tmp_table_name))
        session.execute(_insert_position_stmt(tmp_table_name))
        session.execute(delete(Overdue))
        session.execute(_insert_overdue_stmt(tmp_table_name))
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Ошибка загрузки данных: {e}")


def _insert_region_stmt(tmp_table_name: str) -> Insert:
    # добавляем несуществующие регионы
    return insert(Region).from_select(
        names=[Region.region_name],
        select=(
            select(column("region_name"))
            .select_from(table(tmp_table_name))
            .distinct()
            .where(~exists().where(column("region_name") == Region.region_name))
        ),
    )


def _insert_status_stmt(tmp_table_name: str) -> Insert:
    # добавляем несуществующие статусы
    return insert(Status).from_select(
        names=[Status.status_name],
        select=(
            select(column("status"))
            .select_from(table(tmp_table_name))
            .distinct()
            .filter(~exists().where(column("status") == Status.status_name))
        ),
    )


def _insert_type_stmt(tmp_table_name: str) -> Insert:
    # добавляем несуществующие типы
    return insert(StatusType).from_select(
        names=[StatusType.status_type_name],
        select=(
            select(column("type"))
            .select_from(table(tmp_table_name))
            .distinct()
            .filter(~exists().where(column("type") == StatusType.status_type_name))
        ),
    )


def _insert_company_stmt(tmp_table_name: str) -> Insert:
    # добавляем не существующие организации, вяжем на регионы
    return insert(Company).from_select(
        names=[
            Company.region_id,
            Company.company_inn,
            Company.company_name,
        ],
        select=(
            select(
                Region.id,
                column("company_inn"),
                column("company_name"),
            )
            .select_from(table(tmp_table_name))
            .join(
                target=Region,
                onclause=Region.region_name
                == column("region_name", _selectable=table(tmp_table_name)),
            )
            .distinct()
            .filter(
                ~exists().where(
                    column("company_inn") == Company.company_inn,
                ),
            )
        ),
    )


def _insert_position_stmt(tmp_table_name: str) -> Insert:
    # добавляем не существующие позиции
    return insert(Position).from_select(
        names=[
            Position.gtin,
            Position.series,
            Position.count_doses_per_pack,
            Position.expiration,
            Position.days_overdue,
        ],
        select=(
            select(
                column("gtin"),
                column("series"),
                column("count_doses_per_pack"),
                column("expiration"),
                column("days_overdue"),
            )
            .select_from(table(tmp_table_name))
            .distinct()
            .filter(
                ~exists().where(
                    column("gtin") == Position.gtin,
                    column("series") == Position.series,
                ),
            )
        ),
    )


def _select_stmt(tmp_table_name: str) -> Select:
    # выборка из временной таблицы с привязкой к правильным внешним ключам
    return (
        select(
            Company.id.label("company_id"),
            Status.id.label("status_id"),
            StatusType.id.label("status_type_id"),
            Position.id.label("position_id"),
            func.sum(column("pack_count")).label("pack_count"),
        )
        .select_from(table(tmp_table_name))
        .join(
            target=Region,
            onclause=Region.region_name
            == column("region_name", _selectable=table(tmp_table_name)),
        )
        .join(
            target=Company,
            onclause=and_(
                Company.company_inn
                == column("company_inn", _selectable=table(tmp_table_name)),
                Company.region_id == Region.id,
            ),
        )
        .join(
            target=Status,
            onclause=Status.status_name
            == column("status", _selectable=table(tmp_table_name)),
        )
        .join(
            target=StatusType,
            onclause=StatusType.status_type_name
            == column("type", _selectable=table(tmp_table_name)),
        )
        .join(
            target=Position,
            onclause=and_(
                Position.gtin == column("gtin", _selectable=table(tmp_table_name)),
                Position.series == column("series", _selectable=table(tmp_table_name)),
            ),
        )
        .group_by("company_id", "status_id", "status_type_id", "position_id")
    )


def _insert_overdue_stmt(tmp_table_name: str) -> Insert:
    # заливаем в основную таблицу
    return insert(Overdue).from_select(
        names=[
            Overdue.company_id,
            Overdue.status_id,
            Overdue.status_type_id,
            Overdue.position_id,
            Overdue.pack_count,
        ],
        select=_select_stmt(tmp_table_name),
    )
