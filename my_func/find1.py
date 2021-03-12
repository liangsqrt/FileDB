from filedb.config import DefaultConfig
from filedb.db.database import Database
from filedb.config import DatabaseConf


if __name__ == '__main__':
    config = DatabaseConf()
    Database(name="test", config=config)


