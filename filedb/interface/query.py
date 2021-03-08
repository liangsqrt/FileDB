from abc import ABCMeta
from zope.interface import Interface, Attribute
from zope.interface.declarations import implementer
import six
from abc import ABCMeta, abstractmethod
from filedb.utils.exception import IllegalBehaveException
# weakref
# class a(dict)


class QueryResultInterface(Interface):
    def find(condition):
        """init self by config"""

    def insert_one():
        """read json/yaml file"""

    def update():
        """save json/yaml file"""

    def delete():
        """"""


@implementer(QueryResultInterface)
@six.add_metaclass(ABCMeta)
class ListQueryResultAbstract(list):
    """一般的额数据库的查询类"""
    def __init__(self):
        super(ListQueryResultAbstract, self).__init__()

    @abstractmethod
    def insert_one(self, data):
        self.append(data)

    @abstractmethod
    def find(self, filter) -> QueryResultInterface:
        pass

    @abstractmethod
    def update(self, filter):
        pass

    @abstractmethod
    def upsert(self, filter):
        pass

    @abstractmethod
    def delete(self, filter):
        pass


@implementer(QueryResultInterface)
@six.add_metaclass(ABCMeta)
class DistQueryResultFilter(dict):
    def __init__(self):
        super(DistQueryResultFilter, self).__init__()
    @abstractmethod
    def set_state(self, data):
        pass

    def insert_one(self, data):
        raise IllegalBehaveException("dict型result，不支持次数据插入")

    @abstractmethod
    def find(self, data):
        raise Exception("请添加find方法")

    @abstractmethod
    def update(self, data, *args,**kwargs):
        pass

    @abstractmethod
    def delete(self, data):
        raise Exception("请复写此方法")
    
    @abstractmethod
    def next_condition(self):
        pass

