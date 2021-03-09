import pymongo
import os, sys
base_path = os.path.dirname(__file__)
base_path2 = os.path.dirname(base_path)
base_path3 = os.path.dirname(base_path2)
sys.path.append(base_path)
sys.path.append(base_path2)
sys.path.append(base_path3)
from filedb.interface.query import DistQueryResultFilter#, ListQueryResultAbstract, QueryResultInterface

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
__doc__ = "this module is focus on trans search_dict which input by user to inner query objects "
__doc__ += "这个类主要是用来提供将普通的dict查询翻译成查询类的，"



# class QueryResult()

query_types = [

]


class FString(object):
    def __init__(self):
        pass

    def re(self):
        pass


class FList(object):
    def __init__(self):
        pass


class FDict(object):
    def __init__(self):
        pass


# TODO: 1. 支持key的正则匹配；2. 对value自持in list， 索引，like， 正则， 大于，小于等于

class QuerySet():
    @classmethod
    def __new__(cls, data, *args, **kwargs):
        if type(data) == dict:
            return DictQuerySet
        elif type(data) == list:
            return ListQuerySet
        else:
            return data


class DictQuerySet(FDict):
    data = []
    filter_set = []
    def __init__(self, data):
        self.data.append(data)
    
    def _query(self):
        # for _func in self.filter_set:
        #     _func(self.data)
        tmp_data = []
        for _data in self.data:
            for _func in self.filter_set:
                r = _func(_data)
                if r:
                    tmp_data.append(r)
        self.data = tmp_data
class ListQuerySet(FList):
    data = []
    def __init__(self, data):
        self.data = data
    def _query(self):
            # for _func in self.filter_set:
        #     _func(self.data)
        for _data in self.data:
            for _func in self.filter_set:
                _func(_data)
    

# TODO: 先专门针对value做筛选，不管key, 后期考虑添加上对key的支持
def check_types( data:dict):
    for _k,_v in data.items():
        if _k in query_types:
            return query_types[_k],
        else:
            return "$eq",_k, _v



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
    

class DictFilterParser(DistQueryResultFilter, dict):
    def feed_state(self, data):
        for _k, _v in data.items():
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
    # query = {
    #     "data":{"table":1}
    # }
    # EqualType()
    query_set = QuerySet({"data":1})
    query_set.


