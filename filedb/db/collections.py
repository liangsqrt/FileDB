# TODO ： 统一入参table和table_name
from filedb.service.storage import storage_map


# 做成工厂模式吧
class Collection(object):
    conf = None
    service = None
    documents = []

    @classmethod
    def from_config(cls, conf):  # TODO: 应该是from db 还是from config
        # TODO: table哪些功能需要用到conf
        cls.conf = conf
        return cls

    def check_filedb_file(self, files):
        file_type = files.split('/')[-1].split(".")[-1]
        if file_type not in ["json", "yaml", "xml"]:
            raise Exception("该文件暂时不被支持!")  # TODO： 规范化错误类型

    def install_fileservice(self):
        service = self._get_fileservice_class()
        service.from_config(config=self.conf)
        self.service = service

    def _get_fileservice_class(self, file_type):
        if file_type and file_type in storage_map.keys():
            return storage_map[file_type]

    def find(self, query: dict):
        pass
    
    def __getitem__(self, b):
        for doc in self.documents:
            if doc.name == b:
                return doc
    
    def __setitem__(self, b, c):
        for doc in self.documents:
            if doc.name == b:
                doc.data = c
        else:
            self.documents.append(document)  # TODO: 添加documents的文档
         

