from zope.interface import Interface
from abc import ABCMeta, abstractmethod
import six
from zope.interface import Interface, implementer
from filedb.interface.fileservice import FileServiceInterface
# 配置文件实现增量更新的功能，

class ConfigServiceInterface(Interface):
    def load():
        """read json/yaml file"""

    def reload():
        """save json/yaml file"""

    def update():
        """check """

    def set_config():
        """set value"""


@implementer(FileServiceInterface)
@six.add_metaclass(ABCMeta)
class ConfigFileServiceAbstract(object):
    @abstractmethod
    def load(self):
        pass







