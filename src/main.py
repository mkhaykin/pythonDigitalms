from src.database.connection.utils import create_tables

if __name__ == "__main__":
    from src.database.model.overdue import Overdue  # noqa

    create_tables()
