from filedb.service.storage import StorageMap
from filedb.config import DocumentConfig
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
    config: DocumentConfig = None
    type = None
    storage_service = None
    query_set = None
    format = None
    data: [{}, ] = []

    def __init__(self, conf: DocumentConfig):
        super(Document, self).__init__()
        self.config = conf
        self.file_path = self.config.file_path
        self.type = self.config.type
        self.name = self.config.name
        self.install_storage()
        self.read()

    def install_storage(self):
        service = self._get_storage_class(self.config.type)
        service.install_config(config=self.conf)
        self.storage_service = service

    def read(self):
        self.data = self.storage_service.read()

    @staticmethod
    def _get_storage_class( file_type):
        if file_type and file_type in StorageMap.keys():
            return StorageMap[file_type]

    def find(self, query: dict, format_dict: dict = {}):
        query_set = FilterSet(query_data=query)
        result = query_set.filter(self.data)
        if format_dict:
            result = [Formater.format(format_dict, x) for x in result]
        return result