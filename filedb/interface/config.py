from zope.interface import Interface
# 配置文件实现增量更新的功能，

class ConfigServiceInterface(Interface):
    def load():
        """read json/yaml file"""

    def reload():
        """save json/yaml file"""

    def update()->bool:
        """check """

    def set_config(key, value):
        """set value"""









