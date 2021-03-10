from configparser import ConfigParser
from filedb.utils.project import closest_file_db_cfg
from filedb.interface.config import ConfigFileServiceAbstract
from filedb.service.storage import storage_map
import os

base_dir = os.path.abspath(__file__)

no_collection_sections = ["default", "web", "database"]


class DefaultConfig(ConfigFileServiceAbstract, ConfigParser):
    db_dir = os.path.join(base_dir, "file")
    file_name = "filedb.cfg"
    default_conf_file_dir = os.path.join(base_dir, file_name)
    default_db_file_type = "json"
    project_dir = None

    def __init__(self, *args, **kwargs):
        super(ConfigParser, self).__init__(*args, **kwargs)
        config_file = closest_file_db_cfg()  # find most clean file.conf
        if config_file:
            self.file_path = config_file
        else:
            self.file_path = self.default_config_path
        self.project_dir = os.path.dirname(self.file_name)

    def active(self):
        self.checkout_envs()
        self.read(self.file_path)

    def _reinstall(self):
        self.default_db_file_type = self["database"].get("default_tables_file_type")
        conf_file_dir = self["database"].get("db_base_path")
        if conf_file_dir.startswith("/"):
            self.db_dir = conf_file_dir
        else:
            self.db_dir = os.path.join(self.project_dir, conf_file_dir)

    def checkout_envs(self):
        assert os.path.exists(self.default_conf_file_dir), "默认配置文件不存在"
        assert os.path.exists(self.project_dir), "项目目录识别异常"
        assert os.path.exists(self.default_db_file_type), "项目数据文件路径异常"

    def reload(self):
        self.load()

    def check_conf(self):
        print("配置文件是否规范检查")  # TODO： 配置文件是否规范


class DatabaseConfig(DefaultConfig):
    name = ""
    collections = {}
    _instance = None

    def __new__(cls, *args, **kwargs):
        super(DatabaseConfig, cls).__new__(*args, **kwargs)
        if not cls._instance:
            s = cls.__init__(*args, **kwargs)
            cls._instance = s
            return s
        else:
            return cls._instance

    def __init__(self, *args, **kwargs):
        super(DatabaseConfig, self).__init__(*args, **kwargs)
    
    def initial(self):
        self._initial_collection()
        
    def _initial_collection(self):
        for _config in self.sections():
            if _config not in no_collection_sections:
                self.collections[_config] = CollectionConfig(name=_config, db_conf=self)

    def _initial_document(self):
        for _doc in self.collections.values():
            _doc._initial_document()


class DocumentConfig(object):
    file_path = None
    name = None
    type = None
    col_conf = None

    def __init__(self, name, file_path, conf_type=None, col_conf=None, *args, **kwargs):
        super(DocumentConfig, self).__init__(*args, **kwargs)
        self.col_conf = col_conf
        self.file_path = os.path.join(col_conf.db_conf.db_dir, file_path)
        self.name = name
        if not conf_type:
            for _type in storage_map.keys():
                if _type in self.name:
                    conf_type = _type
        self.type = conf_type


class CollectionConfig(object):
    name = None
    docs = {}
    db_conf = None

    def __init__(self, name, db_conf=None, *args, **kwargs):
        super(CollectionConfig, self).__init__(*args, **kwargs)
        self.name = name
        self.db_conf = db_conf
    
    def __getitem__(self, item):
        return self.docs[item]

    def __setitem__(self, key, value):
        assert isinstance(value, DocumentConfig), "collection的config，只支持新增doc类型的config"
        self.docs[key] = value
        
    def _initial_document(self):
        for _doc in self.db_conf[self.name].keys():
            file_path = self.db_conf[self.name][_doc]
            name = _doc
            doc_conf = DocumentConfig(file_path=file_path, name=name, col_conf=self)
            self[name] = doc_conf


if __name__ == '__main__':
    conf = DatabaseConfig()
    conf.load()
    print(conf.sections())
    print(conf._initial_collection())
    print(conf._initial_document())

