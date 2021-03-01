from abc import ABCMeta
from zope.interface import Interface, Attribute
from zope.interface.declarations import implementer
from zope.interface import verify

# weakref
# class a(dict)


class FileServiceInterface(Interface):
    def from_config(ConfigInterface):
        """init self by config"""

    def read():
        """read json/yaml file"""

    def save():
        """save json/yaml file"""

    def is_existed()->bool:
        """check if file exists"""









