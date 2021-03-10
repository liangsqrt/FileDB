from collections import defaultdict
from filedb.config import  DefaultConfig



# 结合单例： 完成docuemnt的配置装载
class Document(defaultdict):
    name = None
    file_path = None
    config = None
    type = None
    file_path = ""

    def __new__(cls, *args, **kwargs):
        # s = super(Document, cls).__new__(*args, **kwargs)
        instance = super().__new__(cls)
        if not instance.config:
            instance.config = DefaultConfig()
        return instance



    
    
        
        
    
        
Document.config = DcoumentConfig()