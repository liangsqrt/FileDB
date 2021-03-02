import pymongo
import os, sys
base_path = os.path.dirname(__file__)
base_path2 = os.path.dirname(base_path)
base_path3 = os.path.dirname(base_path2)
sys.path.append(base_path)
sys.path.append(base_path2)
sys.path.append(base_path3)
from filedb.interface.query import QueryAbstract, QueryFilter
# client = pymongo.MongoClient()
#
# database = client["ddd"]
# col = database["xxx"]
# col.find_and_modify()


# class QueryDict(QueryAbstract, dict):
#     """
#     python中的集合封装结果就两种，一个list，一个dict，dict对应的查询往往就跟list的不一样了
#     """
#     def __init__(self, *args, **kwargs):
#         super(dict, self).__init__(*args, **kwargs)
#
#     def find(self, filter:QueryFilter):
#         filter.query()


# class QueryList(QueryAbstract, list):
#     def find(self):
#         pass


def rec_merge(d):
    """
    递归合并字典
    :param d1: {"a": {"c": 2, "d": 1}, "b": 2}
    :param d2: {"a": {"c": 1, "f": {"zzz": 2}}, "c": 3, }
    :return: {'a': {'c': 1, 'd': 1, 'f': {'zzz': 2}}, 'b': 2, 'c': 3}
    """
    for key, value in d.items():
        key2 = []
        if isinstance(value, dict):
            key2, value = rec_merge(value)
        if key2:
            return key2.append(key), value
        return [key], value
    

class DictFilterParser(QueryFilter, dict):
    def set_state(self, data):
        for _k,_v in data.items():
            self[_k] = _v

    def next_condition(self):
        # childs = []
        # for data in datas:
        #     try:
        #         for _k in data.keys():
        #             yield _k
        #             _c = data.get(_k)
        #             if isinstance(_c, dict):
        #                 childs.append(_c)
        #     except Exception as e:
        #         print(e)
        # for _k in DictFilterParser.next_condition(childs):
        #     yield _k
        return rec_merge(self)

            

if __name__ == '__main__':
    dict_filter = DictFilterParser()
    dict_filter["a"] = {
        "a1": 1,
        "a2": {
            "b1":11,
            "b2":12
        }
    }
    dict_filter["b"] = 2
    print(dict_filter)
    print(dict_filter.next_condition())
    # ccc = [x for x in dict_filter.next_condition([dict_filter])]
    # print(ccc)

