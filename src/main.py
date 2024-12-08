import logging
import sys

from src.database.connection.sync_db import engine
from src.database.connection.utils import create_tables
from src.export_xlsx import export_to_xlsx
from src.import_xlsx import import_from_xlsx

logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(stream=sys.stdout),
    ],
    format="[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
)


if __name__ == "__main__":
    from src.database.model.overdue import Overdue  # noqa

    create_tables()
    import_from_xlsx(engine, "import/Просрочено 2022-06-09.xlsx", "Статика")
    export_to_xlsx(engine, "export/result.xlsx", "result")
