from filedb.service.storage import storage_map
import os
from filedb.config import DatabaseConfig


# 增加单例模式
class Database(object):
    conf = None
    tables = {}
    default_table_type = None
    base_db_path = None

    # @classmethod
    # def from_config(cls, conf: DatabaseConfig):
    #     cls.conf = conf
    #     cls.base_db_path = conf.default_conf_file_dir
    #     cls.default_table_type = conf.default_db_file_type
    #     return cls

    @staticmethod
    def check_conf(conf:DatabaseConfig):
        """
        检测配置文件是否合法
        :key
        """
        assert hasattr(DatabaseConfig, "name"), "database must have a name"
        assert hasattr(DatabaseConfig, "collections"), "haven't get any collection config info"
        assert hasattr(DatabaseConfig, "default_conf_file_dir", "haven't ")
        if "databases" not in conf.sections():
            raise Exception("配置文件不正确， databases配置项信息不存在")
        if "web" not in conf.sections():
            print("web配置项信息不存在，将关闭配置信息")
        else:
            print("http service will run at {host}:{port}".format(
                host=conf['web'].get("host"),
                port=conf['web'].get("port")
            ))

    def setup_tables(self, table_name, file_path):
        # TODO, 配置类，要对配置文件做检查
        file_type = file_path.split("/")[-1].split(".")[-1]

        self.tables.update({
            table_name: self.create_table(file_type) # TODO: 应该是table类而不是service类
        })

    def delete(self, table):
        if table in self.tables.keys():
            self._delete_table(table)
        else:
            print("该表不存在！")

    def _delete_table(self, table):
        os.remove(self.tables[table].service.file_path)
        del self.tables[table]

    def __getitem__(self, item):
        if item not in self.tables.keys():
            _file_path = ".".join(["default/", item, self.default_table_type])
            print("该表不存在, 即将添加: {}".format(_file_path))  # TODO: 规范化报错日志
            self.tables.update({
                item: self.create_table(_file_path)
            })
        return self.tables[item]

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



