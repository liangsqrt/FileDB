from abc import ABCMeta
from zope.interface import Interface, Attribute
from zope.interface.declarations import implementer
import six
from abc import ABCMeta, abstractmethod
# weakref
# class a(dict)


class QueryInterface(Interface):
    def find(condition):
        """init self by config"""

    def insert_one():
        """read json/yaml file"""

    def update():
        """save json/yaml file"""

    def delete():
        """"""


@implementer(QueryInterface)
@six.add_metaclass(ABCMeta)
class QueryAbstract(list):
    """一般的额数据库的查询类"""
    @abstractmethod
    def insert_one(self, data):
        self.append(data)

    @abstractmethod
    def find(self, filter):
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


@six.add_metaclass(ABCMeta)
class QueryFilter(dict):
    @abstractmethod
    def set_state(self, data):
        pass

    @abstractmethod
    def next_condition(self):
        pass

