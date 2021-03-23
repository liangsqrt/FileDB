import re
query_types = ["$in", "$eq", "$gt", "$lt", "$gte", "$lte", "$re", "$contains", "$index"]


class InType(object):
    name = "$in"
    value = []

    def __init__(self):
        self.query_set = {}

    def __call__(self, key, value, data:dict, *args, **kwargs):
        # if data.get("key"  # TODO: 优化这一步
        return data.get("key") in value


class EqualType(object):
    name = "$eq"
    value = 0
    priority = 1
    def __init__(self):
        self.query_set = {}

    def __call__(self, key, value, data: dict, *args, **kwargs):
        return value == data.get(key)


class GreatType(object):
    name = "$gt"
    value = 0
    priority = 1
    def __init__(self):
        self.query_set = {}

    def __call__(self, key:str, value, data:dict, *args, **kwargs):
        return data.get(key) > value
    
    
class GreateEqualType(object):
    name = '$gte'
    priority = 1
    def __init__(self) -> None:
        super().__init__()
    
    def __call__(self, key:str, value, data:dict, *args, **kwargs):
        return data.get(key) >= value


class LessType(object):
    name = '$lt'
    priority = 1
    def __init__(self) -> None:
        super().__init__()
    
    def __call__(self, key:str, value, data:dict, *args, **kwargs):
        return data.get(key) < value


class LessEqualType(object):
    name = '$lte'
    priority = 1
    def __init__(self) -> None:
        super().__init__()
    
    def __call__(self, key:str, value, data:dict, *args, **kwargs):
        return data.get(key) <= value


class RegexType(object):
    name = '$re'
    priority = 1
    
    def __call__(self, key:str, value, data:dict, *args, **kwargs):
        # return re.match()
        return re.match(value, data.get(key)).group()


class ContainType(object):
    name = "$contains"

    def __call__(self, key:str, value:str, data:dict):
        return value in data.get(key)


class IndexType(object):
    name = "$index"
    
    def __call__(self, key:str, value: int, data:dict):
        if value > len(data.get(key))-1:
            return False
        else:
            return data.get(key)[value]

query_map = {
    "$in": InType,
    "$eq": EqualType,
    "$gt": GreatType,
    "$gte": GreateEqualType,
    "$lt": LessType,
    "$lte": LessEqualType,
    "$contains": ContainType,
    "$re": RegexType,
    "$index": IndexType,
}

# TODO: 目前是把所有的dict当做list来处理，没有专门区分dict和list
# TODO: 提高可读性
# TODO: 考虑用exception替换到层层返回逻辑
# TODO: re查找的结果不太懂UI， 查找zhang. 返回的应该只有zhangs, 像什么zhangsi就不返回
class Filter(object):
    priority = 0
    query_data = {}
    task_list = []  # 需要继续迭代判断的额
    father_node = None
    father_key = ""

    def __init__(self, father_node,  father_key:str, query_data:dict, priority:int):
        self.father_node = father_node
        self.father_key = father_key
        self.query_data = query_data
        self.priority = priority
        if self.father_node and self.priority != self.father_node.priority+1:
            raise Exception("filter查询顺序错误")  # TODO: 丰富错误信息
        
    def filter(self, data: dict):
        """
        同时跟进数据的层级和过滤条件的层级，并一一对饮，这个方法会返回该层级数据被filter
        返回下一层级的result
        确定query_data层级走完了没有
        是否还可以继续搜索
        这里的逻辑太烂了
        """
        # for data in input_data:
        if isinstance(data, list):
            # TODO: 针对复杂list的嵌套查询
            if "$index" in self.query_data.keys():
                index = self.query_data.get("$index")
                if len(data) > index:
                    data = data[index]
                else:
                    return False
        for _k, _v in self.query_data.items():
            if _k in query_map.keys():
                continue  # must has been paserd
            elif type(_v) in [int, str, float, bool]:
                r = EqualType()(_k, _v, data)
                if not r:
                    return False
            elif isinstance(_v, dict):
                inter_set = set(_v.keys()).intersection(set(query_map.keys()))
                for _condition in inter_set:
                    if not query_map[_condition]()(_k, _v.get(_condition), data):
                        return False
                else:
                    self.task_list.append({
                        "data": data.get(_k), 
                        "filter": Filter(father_node=self, father_key=_k, query_data=_v, priority=self.priority+1)
                    }) # TODO: only this condition should go on !
            elif isinstance(_v, list) and _k not in query_map.keys():
                r = EqualType()(_k, _v, data) 
                if not r:
                    return False
            else:
                raise Exception("未知类型的筛选功能")
        return True
    
    @property
    def status(self):  # 是否判断完了, 暂时无用
        return self.task_list == []


class FilterBatch(object):
    """
    针对单个数据，相对于filterset是处理多个[object{}, object{}...]， filterBatch重心在于结合filter，判断这个数据能否通过
    """
    priority = 0  # 暂时没用
    task_list = []

    def __init__(self, data, query_data):  # 统一query_data 和 data的命名风格
        self.task_list.append(
            {
                "data": data,
                "filter": Filter(None, father_key="", query_data=query_data, priority=0)
            }
        )

    def filter(self):
        """
        filter 返回的k，v可读太差
        """
        while not self.status:
            r = self.next()
            if r == False:
                return False
        return True

    def next(self):
        """
        上一轮全部通过可以进入下一轮
        """
        task_list = []
        for _task_data in self.task_list:
            filter = _task_data.get("filter")
            data = _task_data.get("data")
            r = filter.filter(data)
            if(isinstance(r, bool)) and not r:
                return False
            elif isinstance(r, dict): # 其他的list, str, int, bool这些，只会返回true或者false
                task_list = task_list + filter.task_list
        self.priority += 1
        self.task_list = task_list

    @property
    def status(self):
        return self.task_list == []


class FilterSet(object):
    status = True

    def __init__(self, query_data={}):
        """

        :param query_data:  查询语句
        """
        self.query_data = query_data
    
    def filter(self, input_data):
        """
        返回被查找到的元素的索引，如果一条都没有找到，证明查询不合法。
        TODO: 过滤结束后保留合格的数据索引
        TODO: 返回唯一路径, 用来更新
        """
        target_result = []
        if not isinstance(input_data, list):
            raise Exception("filter的数据不合翻")
        for index, data in enumerate(input_data):
            filter_batch = FilterBatch(data=data, query_data=self.query_data)
            r = filter_batch.filter()
            if r:
                target_result.append(data)
        return target_result


if __name__ == '__main__':
    data = [
        {"name":"zhangsan"},
        {"name":"zhanger"},
        {"name":"zhangsi"},
        ]
    
    f = FilterSet(query_data={"name":{
        "$re": "zhang."
    }})

    print(f.filter(data))
    

