# TODO ： 统一入参table和table_name
import os
from filedb.service.storage import StorageMap, FileService
from filedb.db.document import BaseDict, Document
from filedb.config import CollectionConfig

# TODO: 需要将基础数据类型汇总到某个地方, 想BasicDict不应该在document


class Collection(BaseDict):
    conf: CollectionConfig = None
    service: FileService = None
    documents: {str: Document} = {}
    name = None

    def __init__(self, name, conf):
        super(Collection, self).__init__()
        self.name = name
        self.conf = conf

    def install_config(self):
        self.initial_document()

    def initial_document(self):
        for _name, _conf in self.conf.db_conf.items():
            self[_name] = Document()

    
    def __getitem__(self, value):
        if value in self.documents.keys():
            return self.documents[value]
        else:
            return BaseDict()
    
    def __setitem__(self, key, value):
        if isinstance(value, Document):
            self.documents[key] = value
        else:
            raise Exception("不支持的文档")

    def delete(self):
        os.remove(self.service.file_path)
         

