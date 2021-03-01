from filedb.config import DefaultConfig
import pymongo


if __name__ == '__main__':
    conf = DefaultConfig()
    conf.load()
    print(conf.sections())


