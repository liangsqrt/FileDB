# TODO ： 统一入参table和table_name
import os
from filedb.service.storage import StorageMap, FileService
from filedb.db.document import BaseDict, Document
from filedb.config import CollectionConfig

# TODO: 需要将基础数据类型汇总到某个地方, 想BasicDict不应该在document


class Collection(BaseDict):
    conf: CollectionConfig = None
    documents: {str: Document} = {}
    name = None

    def __init__(self, name, conf):
        super(Collection, self).__init__()
        self.name = name
        self.conf = conf
        self.install_config()

    def install_config(self):
        self.initial_document()

    def initial_document(self):
        for _name, _conf in self.conf.db_conf.items():
            self[_name] = Document(conf=_conf)

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

    def destroy_all(self):
        for name, doc in self.documents.items():
            doc.destory()
            del self.documents[name]

    def destroy(self, doc_name):
        if doc_name in self.documents.keys():
            self.documents[doc_name].destroy()
            del self.documents[doc_name]

