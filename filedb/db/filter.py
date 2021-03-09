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

    def __call__(self, key, value, data:dict, *args, **kwargs):
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
    # def __init__(self):
        # self.pattern = re.compile(pattern)
    
    def __call__(self, key:str, value, data:dict, *args, **kwargs):
        return re.match(value, data.get(key))


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
# TODO: 完成的只是条件过滤，还没有写内容结果提取！！
# TODO: 考虑用exception替换到层层返回逻辑
class Filter(object):
    priority = 0
    query_data = {}
    child_filter = []
    father_node = None
    father_key = ""
    def __init__(self, father_node,  father_key:str, query_data:dict, priority:int):
        self.father_node = father_node
        self.father_key = father_key
        self.query_data = query_data
        self.priority = priority
        if self.father_node and self.priority != self.father_node.priority+1:
            raise Exception("filter查询顺序错误")  # TODO: 丰富错误信息
        
    def filter(self, data:dict):
        """
        同时跟进数据的层级和过滤条件的层级，并一一对饮，这个方法会返回该层级数据被filter
        返回下一层级的result
        确定query_data层级走完了没有
        是否还可以继续搜索
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
                continue # must has been paserd
            elif type(_v) in [int, str, float, bool]:
                return EqualType()(_k, _v, data)
            elif isinstance(_v, dict):
                inter_set = _v.keys().intersection(query_map.keys())
                for _condition in inter_set:
                    if not query_map[_condition](_k, _v, data):
                        return False
                else:
                    self.child_filter.append(Filter(father_node=self, father_key=_k, query_data=_v, priority=self.priority+1)) # TODO: only this condition should go on !
                    return _v
            elif isinstance(_v, list) and _k not in query_map.keys():
                return EqualType()(_k, _v, data)                
            else:
                raise Exception("未知类型的筛选功能")
    
    @property
    def could_continued(self):
        return self.child_filter == []


class FilterSet(object):
    filter_set = []
    priority = 0
    status = True
    data = None
    
    def __init__(self, query_data):
        f = Filter(father_node=None, father_key="", query_data=query_data, priority=0)
        # self.filter = f
        self.filter_set.append(f)
    
    def filter(self, input_data):
        """
        返回被查找到的元素的索引，如果一条都没有找到，证明查询不合法。
        TODO: 过滤结束后保留合格的数据索引
        """
        # targe_result = []
        # if not isinstance(input_data, list):
        #     raise Exception("filter的数据不合翻")
        # for index, data in enumerate(input_data):
        #     next_data = next(data)
        #     if isinstance(next_data, bool):
        #         if next_data:
        #             return True
        #         else:
        #             return False
        next_data = self.next(input_data)
        while self._has_next_batch():
            next_data = next_data(next_data)
            if isinstance(next_data, bool):
                if not next_data:
                    return False

    def _has_next_batch(self):
        tmp_filter = []
        for _f in self.filter_set:
            for _child_filter  in _f.child_filter:
                tmp_filter.append(_child_filter)
        self.filter_set = tmp_filter
        # yield [x for x in self.filter_set if x.priority==self.priority]
        if self.filter_set:
            yield True
        self.priority += 1
    
    def next(self, data):
        filtered_data = []
        for _filter in self.filter_set:
            r = _filter.filter(data)
            # 注意区分dict和bool的区别
            if(isinstance(r, bool)) and r:
                self.status = False #  不可以继续迭代了
                return True
            elif(isinstance(r, bool)) and not r:
                self.status = False
                return False
            elif isinstance(r, dict):
                self.data = r
                self.status = True # 是否可以继续
                filtered_data.append(r)
        return filtered_data


if __name__ == '__main__':
    f = FilterSet(query_data={"name":"zhansan"})
    print(f.filter({"name":"zhangsna"}))
    

