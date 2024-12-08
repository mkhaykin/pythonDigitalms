from logging import getLogger

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.connection.async_db import async_engine
from src.database.connection.sync_db import engine
from src.database.model.base import Base

logger = getLogger(__name__)


async def ping_db(session: AsyncSession) -> bool:
    try:
        await session.execute(select(text("1")))
    except:  # noqa
        return False
    return True


async def async_create_tables() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def async_drop_tables() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)


def drop_tables() -> None:
    Base.metadata.drop_all(bind=engine)


def drop_table(table_name: str) -> None:
    table = Base.metadata.tables.get(table_name)
    if table:
        Base.metadata.drop_all(bind=engine, tables=(table,))
    else:
        with engine.connect() as con:
            con.execute(text(f"DROP TABLE IF EXISTS {table_name};"))
            con.commit()
