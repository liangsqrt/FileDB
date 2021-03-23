from configparser import ConfigParser
from filedb.utils.project import closest_file_db_cfg
from filedb.interface.config import ConfigFileServiceAbstract
from filedb.service.storage import StorageMap
import os

base_dir = os.path.dirname(__file__)

no_collection_sections = ["default", "web", "database"]


class DefaultConfig(ConfigParser, ConfigFileServiceAbstract):
    db_dir = os.path.join(base_dir, "file")
    file_name = "filedb.cfg"
    default_conf_file_path = os.path.join(base_dir, file_name)
    default_db_file_type = "json"
    project_dir = None
    file_path = None

    def __init__(self, conf_file_path=None, *args, **kwargs):
        super(ConfigParser, self).__init__(*args, **kwargs)
        if conf_file_path:
            self.file_path = conf_file_path
        else:
            config_file = closest_file_db_cfg()  # find most clean file.conf
            if config_file:
                self.file_path = config_file
            else:
                self.file_path = self.default_config_path
        self.project_dir = os.path.dirname(self.file_path)
        self.active()
    
    def __new__(cls, *args, **kwargs):
        return super(DefaultConfig, cls).__new__(cls, *args, **kwargs)

    def active(self):
        self.checkout_envs()
        self.read(self.file_path, encoding="utf8")

    def reinstall(self):
        self.active()
        self.default_db_file_type = self["database"].get("default_tables_file_type")
        conf_file_dir = self["database"].get("db_base_path")
        if conf_file_dir.startswith("{pjt}"):
            pjt_tail = conf_file_dir.replace("{pjt}", "").strip("/")
            self.db_dir = os.path.join(self.project_dir, pjt_tail)
        else:
            self.db_dir = os.path.join(self.project_dir, conf_file_dir)

    def checkout_envs(self):
        assert os.path.exists(self.default_conf_file_path), "默认配置文件不存在"
        assert os.path.exists(self.project_dir), "项目目录识别异常"
        # assert os.path.exists(self.default_db_file_type), "项目数据文件路径异常"

    def load(self):
        self.reinstall()

    def reload(self):
        self.load()

    def check_conf(self):
        self.checkout_envs()
        print("配置文件是否规范检查")  # TODO： 配置文件是否规范


class DocumentConf(object):
    file_path = None
    name = None
    type = None
    col_conf = None

    def __init__(self, name, file_path, conf_type=None, col_conf=None, *args, **kwargs):
        super(DocumentConf, self).__init__(*args, **kwargs)
        self.col_conf = col_conf
        self.file_path = os.path.join(col_conf.path, file_path)  # TODO: col的path是什么，相对还是绝对
        self.name = name
        if not conf_type:
            for _type in StorageMap.keys():
                if _type in self.file_path:
                    conf_type = _type
        if not conf_type:
            raise Exception("Unsupported for {}".format(self.file_path))
        self.type = conf_type


class CollectionConf(object):
    name = None
    docs = {}
    db_conf: {str: object} = None  # DocumentConf
    path = None  # 一般用不着，代表着在着个col下创建doc时默认存放的路径

    def __init__(self, name, db_conf=None, *args, **kwargs):
        super(CollectionConf, self).__init__(*args, **kwargs)
        self.name = name
        self.db_conf = db_conf
        self.path = os.path.join(db_conf.db_dir, name)
        self.initial_document()
    
    def __getitem__(self, item):
        return self.docs[item]

    def __setitem__(self, key, value):
        assert isinstance(value, DocumentConf), "collection的config，只支持新增doc类型的config"
        self.docs[key] = value
        
    def initial_document(self):
        for _doc in self.db_conf[self.name].keys():  # db_conf的keys相当于是sections的keys， 里边的就是具体的文件路径了
            file_path = os.path.join(*os.path.split(self.db_conf[self.name][_doc]))  # 处理不同系统的文件路径
            name = _doc
            doc_conf = DocumentConf(file_path=file_path, name=name, conf_type=self.db_conf.default_db_file_type, col_conf=self)
            self[name] = doc_conf

    def get_doc_conf(self, name=None):
        if name:
            return self.docs.get(name)
        else:
            return self.docs


class DatabaseConf(DefaultConfig):
    name = ""
    collections: {str: CollectionConf} = {}
    path = None
    _instance = None

    def __new__(cls, *args, **kwargs):
        super(DatabaseConf, cls).__new__(cls, *args, **kwargs)
        if not cls._instance:
            s = super().__new__(cls)
            cls._instance = s
            return s
        else:
            return cls._instance

    def __init__(self, conf_file_path=None, *args, **kwargs):
        # if conf_file_path:
        super(DatabaseConf, self).__init__(*args, **kwargs)
        self.initial()

    def initial(self):
        self.initial_collection()

    def initial_collection(self):
        # TODO: 配置文件中的path是用绝对路径还是相对路径
        for _config in self.sections():
            if _config not in no_collection_sections:
                self.collections[_config] = CollectionConf(name=_config, db_conf=self)

    def _initial_document(self):
        for _doc in self.collections.values():
            _doc.initial_document()

    def get_col_configs(self, name=None):
        if name:
            return self.collections.get(name)
        return self.collections

    def get_doc_configs(self, name):
        doc_conf_list = {}
        for _col_conf in self.collections.values():
            for _name, _doc in _col_conf.docs.items():
                doc_conf_list[_name] = _doc
                if name and _doc.name == name:
                    return _doc
        if name:
            return None
        return doc_conf_list


if __name__ == '__main__':
    conf = DatabaseConf()
    conf.load()
    print(conf.sections())
    print(conf.initial_collection())
    print("finished!")

