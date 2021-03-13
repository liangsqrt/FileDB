import os, sys
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from filedb.db.document import Document
from filedb.db.database import Database
from filedb.config import DocumentConf, DatabaseConf


if __name__ == '__main__':
    c = {
        "a": 1,
        "b": 2,
        "c": {
            "d": 1,
            "e": []
        }
    }
    conf = DatabaseConf()
    conf.load()
    # 分别对doc测试，col测试，db测试
    db = Database(name="test", config=conf)
    # db.init_db()
    print(db)
    doc = Document(conf=conf.get_doc_configs(name="test1"))
    print(doc)
    # doc.update(c)
    # print(doc)
    # for _k, _v in doc.items():
    #     print(_k, _v)

