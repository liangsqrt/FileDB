from filedb.service.storage import storage_map
import os
from filedb.config import DatabaseConfig
from filedb.db.document import BaseDict
from filedb.db.collections import Collection

# 增加单例模式
# TODO: 丰富异常自检的规则， 自检规则应当放到config中去，database中的自检，应当是检测他自己的数据
class Database(object):
    conf = None
    collections: {str: Collection} = {}
    default_table_type = None
    db_dir = None
    name = None
    _instance = {}

    def __new__(cls, name:str, config, *args, **kwargs):
        """

        :param name: unique name
        :param args:
        :param kwargs:
        """
        super(Database, cls).__new__(*args, **kwargs)
        if name not in cls._instance.keys():
            instance = cls.__init__(*args, **kwargs)
            cls._instance[name] = instance
            return instance
        else:
            return cls._instance[name]

    def __init__(self,name, config:DatabaseConfig):
        self.check_conf(conf=config)  # 配置内容是否正确、文件是否存在、权限等
        self.name = name
        self.conf = config
        self.db_dir = config.db_dir

    @staticmethod
    def check_conf(conf: DatabaseConfig):
        """
        检测配置文件是否合法
        :key
        """
        # assert hasattr(DatabaseConfig, "name"), "database must have a name"
        # assert hasattr(DatabaseConfig, "collections"), "haven't get any collection config info"
        # assert hasattr(DatabaseConfig, "db_dir"), "must set a valid dir to store db file"
        conf.checkout_envs()
        if "web" not in conf.sections():
            print("web配置项信息不存在，将关闭配置信息")
        else:
            print("http service can be run at {host}:{port}".format(
                host=conf['web'].get("host"),
                port=conf['web'].get("port")
            ))

    def install_config(self, table_name, file_path):
        # 读取数据
        pass

    def _initial_database(self):
        for _name, _col_conf in self.conf.collections.items():
            # _col_conf.
            pass


    def delete(self, table):
        if table in self.collections.keys():
            self._delete_table(table)
        else:
            print("该表不存在！")

    def _delete_table(self, table):
        os.remove(self.collections[table].service.file_path)
        del self.collections[table]

    def __getitem__(self, item):
        if item not in self.collections.keys():
            _file_path = ".".join(["default/", item, self.default_table_type])
            print("该表不存在, 即将添加: {}".format(_file_path))  # TODO: 规范化报错日志
            self.collections.update({
                item: self.create_table(_file_path)
            })
        return self.collections[item]

    def create_table(self, table, path="", pattern="single"):
        """

        :param table:
        :param path:
        :param pattern: single means that db file content is dict_like; database is list_like just like mongo
        :return:
        """
        pass

    def export_to_file(self):
        pass

    def import_from_file(self):
        pass



