from zope.interface import Interface, implementer
from filedb.interface.fileservice import FileServiceInterface
from configparser import ConfigParser
from abc import ABCMeta, abstractmethod
import six
from filedb.utils import closest_file_db_cfg
import os

base_dir = os.path.abspath(__file__)


@implementer(FileServiceInterface)
@six.add_metaclass(ABCMeta)
class ConfigFileServiceAbstract(object):
    @abstractmethod
    def load(self):
        pass


class DefaultConfig(ConfigFileServiceAbstract, ConfigParser):
    file_path = "filedb.cfg"
    default_config_path = os.path.join(base_dir, file_path)

    def __init__(self, *args, **kwargs):
        super(ConfigParser, self).__init__(*args, **kwargs)
        config_file = closest_file_db_cfg()
        if config_file:
            self.file_path = config_file
        else:
            self.file_path = self.default_config_path

    def load(self):
        self.read(self.file_path)

    def reload(self):
        self.load()

    def check_conf(self):
        print("配置文件是否规范检查")  # TODO： 配置文件是否规范


if __name__ == '__main__':
    conf = DefaultConfig()
    conf.load()
    print(conf.sections())

