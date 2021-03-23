import os
from filedb.service.storage import StorageMap
from filedb.config import DocumentConf
from filedb.db.filter import FilterSet
from filedb.db.formater import Formater


class BaseDict(dict):
    """
    无限循环字典
    """
    def __missing__(self, key):
        nested = self[key] = type(self)()
        return nested

    def __repr__(self):
        return f'{type(self).__name__}({super().__repr__()})'


class Document(BaseDict):
    data: [{}, ] = []
    file_path = None
    type = None
    name = None
    config: DocumentConf = None
    storage_service = None
    query_set = None
    format = None

    def __init__(self, conf: DocumentConf):
        assert isinstance(conf, DocumentConf), "should config be document config"
        super(Document, self).__init__()
        self.config = conf
        self.file_path = self.config.file_path
        self.type = self.config.type
        self.name = self.config.name
        self.install_storage()
        self.read()

    def set_config(self, config):
        """
        安装配置文件，初始化数据，service等等。 执行完后可以直接开始使用
        """
        self.config = config
        self.file_path = self.config.file_path
        self.type = self.config.type
        self.name = self.config.name
        self.install_queryset()
        self.install_storage()
        self.read()

    def info(self):
        return """
            name : {name},
            type : {type},
            file_path: {file_path}
        """.format(
            name=self.name,
            type=self.type,
            file_path=self.file_path
        )

    def install_storage(self):
        service_cls = self._get_storage_class(self.config.type)
        service = service_cls()
        service.install_config(config=self.config)
        self.storage_service = service

    def install_queryset(self):
        # self.query_set = FilterSet()
        pass

    def read(self):
        self.data = self.storage_service.read()

    @staticmethod
    def _get_storage_class(file_type):
        if file_type and file_type in StorageMap.keys():
            return StorageMap[file_type]
        
    def destroy(self):
        os.remove(self.storage_service.file_path)

    def _create_file(self):
        fl = open(self.config.file_path, "w")
        fl.close()

    def update(self, where, data):
        query_set = FilterSet(query_data=where)  # filterSet继承filter接口， 都一定支持filter方法， 用filter即可查询
        result = query_set.filter(self.data)  # 如何保证对查询的结果进行更改，能改变被查询的数据文件： 是否返回唯一路径
        # 当result是字符串的时候，那么对result直接替换，就不会改变结果的值。
        if type(result) not in [list, dict]:
            # TODO: 怎么针对不是结构体的结果进行更新
            pass

    def find(self, where: dict, format_dict: dict = {}):
        query_set = FilterSet(query_data=where)
        result = query_set.filter(self.data)
        if format_dict:
            result = [Formater.format(format_dict, x) for x in result]
        return result