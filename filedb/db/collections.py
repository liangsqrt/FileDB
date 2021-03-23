# TODO ： 统一入参table和table_name
import os
from filedb.service.storage import StorageMap, FileService
from filedb.db.document import BaseDict, Document
from filedb.config import CollectionConf, DocumentConf

# TODO: 需要将基础数据类型汇总到某个地方, 想BasicDict不应该在document


class Collection(BaseDict):
    conf: CollectionConf = None
    documents: {str: Document} = {}
    name = None
    # path = None  # 默认的col的文件夹

    def __init__(self, name, conf):
        """
        TODO:
            1.支持从代码中创建collection：1. 一定会有basicConfig； 2. 用户一定不会单独创建col，肯定写在db中；
            2。从配置文件生成collection
        """
        super(Collection, self).__init__()
        self.name = name
        self.conf = conf
        self.install_config()

    def install_config(self):
        # self.conf.packages
        self.initial_document()

    def initial_document(self):
        for _name, _conf in self.conf.docs.items():
            self[_name] = Document(conf=_conf)

    def __getitem__(self, value):
        assert type(value) == str, "only support string col_name"
        if value in self.documents.keys():
            return self.documents[value]
        else:
            self.documents[value] = self._create_document(value)
    
    def __setitem__(self, key, value):
        if isinstance(value, Document):
            self.documents[key] = value
        else:
            raise Exception("不支持的文档")

    def _create_document(self, name):
        """
        创建document一定是在col中
        """
        doc_conf = DocumentConf(
            name=name,
            file_path=os.path.join(self.conf.path, name, self.conf.db_conf.default_db_file_type),
            conf_type=self.conf.db_conf.default_conf_type,
            col_conf=self.conf
        )
        doc = Document(doc_conf)
        return doc

    def destroy_all(self):
        for name, doc in self.documents.items():
            doc.destory()
            del self.documents[name]

    def destroy(self, doc_name):
        if doc_name in self.documents.keys():
            self.documents[doc_name].destroy()
            del self.documents[doc_name]

