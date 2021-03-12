from filedb.db.database import Database
from filedb.config import DatabaseConf


if __name__ == '__main__':
    db_conf = DatabaseConf()
    db = Database(name="test", config=db_conf)
    db.quit()