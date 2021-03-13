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
    name = None
    file_path = None
    config: DocumentConf = None
    type = None
    storage_service = None
    query_set = None
    format = None
    data: [{}, ] = []

    def __init__(self, conf: DocumentConf):
        assert isinstance(conf, DocumentConf), "shoud config be document config"
        super(Document, self).__init__()
        self.config = conf
        self.file_path = self.config.file_path
        self.type = self.config.type
        self.name = self.config.name
        self.install_storage()
        self.read()

    def install_storage(self):
        service_cls = self._get_storage_class(self.config.type)
        service = service_cls()
        service.install_config(config=self.config)
        self.storage_service = service

    def read(self):
        self.data = self.storage_service.read()

    @staticmethod
    def _get_storage_class( file_type):
        if file_type and file_type in StorageMap.keys():
            return StorageMap[file_type]
        
    def destroy(self):
        os.remove(self.storage_service.file_path)

    def find(self, query: dict, format_dict: dict = {}):
        query_set = FilterSet(query_data=query)
        result = query_set.filter(self.data)
        if format_dict:
            result = [Formater.format(format_dict, x) for x in result]
        return result

