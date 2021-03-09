from abc import ABCMeta
from zope.interface import Interface, Attribute
from zope.interface import implementer
from abc import ABCMeta,abstractmethod
import six


class FileServiceInterface(Interface):
    def from_config(ConfigInterface):
        """init self by config"""

    def read():
        """read json/yaml file"""

    def save():
        """save json/yaml file"""

    def is_existed()->bool:
        """check if file exists"""




@implementer(FileServiceInterface)
@six.add_metaclass(ABCMeta)
class FileService(object):
    filename = ""
    file_path = ""
    type = ""
    encoding = ""
    config = ""
    @abstractmethod
    def save(self, data):
        """save"""

    @abstractmethod
    def read(self) -> dict:
        """read"""

    @abstractmethod
    def from_config(self, Config):
        """pass"""

    @abstractmethod
    def is_existed(self):
        """pass"""




