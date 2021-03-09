from abc import ABCMeta
from zope.interface import Interface, Attribute
from zope.interface.declarations import implementer
import six
from abc import ABCMeta, abstractmethod
from filedb.utils.exception import IllegalBehaveException
# weakref
# class a(dict)


class QueryResultInterface(Interface):
    def _find(condition):
        """init self by config"""

    def _insert_one():
        """read json/yaml file"""

    def _update():
        """save json/yaml file"""

    def _delete():
        """"""


@implementer(QueryResultInterface)
@six.add_metaclass(ABCMeta)
class ListQueryResultAbstract(list):
    """一般的额数据库的查询类"""
    def __init__(self):
        super(ListQueryResultAbstract, self).__init__()

    @abstractmethod
    def _insert_one(self, data):
        self.append(data)

    @abstractmethod
    def _find(self, filter) -> QueryResultInterface:
        pass

    @abstractmethod
    def _update(self, filter):
        pass

    @abstractmethod
    def _upsert(self, filter):
        pass

    @abstractmethod
    def _delete(self, filter):
        pass


@implementer(QueryResultInterface)
@six.add_metaclass(ABCMeta)
class DistQueryResultFilter(dict):
    def __init__(self):
        super(DistQueryResultFilter, self).__init__()
    @abstractmethod
    def set_state(self, data):
        pass

    def _insert_one(self, data):
        raise IllegalBehaveException("dict型result，不支持次数据插入")

    @abstractmethod
    def _find(self, data):
        raise Exception("请添加find方法")

    @abstractmethod
    def _update(self, data, *args,**kwargs):
        pass

    @abstractmethod
    def _delete(self, data):
        raise Exception("请复写此方法")
    
    @abstractmethod
    def next_condition(self):
        pass

