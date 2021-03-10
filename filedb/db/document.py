from collections import defaultdict


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
    config = None
    type = None
    file_path = ""


