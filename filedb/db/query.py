import pymongo


client = pymongo.MongoClient()


class IterableQuery(list):
    """一般的额数据库的查询类"""
    def __init__(self, *args, **kwargs):
        super(IterableQuery, self).__init__(*args, **kwargs)

    def insert(self, data):
        self.append(data)

    def find(self, filter):
        pass

    def update(self, filter):
        pass

    def upsert(self, filter):
        pass

    def delete(self, filter):
        pass


class DictQuery(dict):
    """
    python中的集合封装结果就两种，一个list，一个dict，dict对应的查询往往就跟list的不一样了
    """
    def __init__(self, *args, **kwargs):
        super(DictQuery, self).__init__(*args, **kwargs)


class DictFilterParser(object):
    pass

if __name__ == '__main__':
    a = IterableQuery()
    a.insert(1)