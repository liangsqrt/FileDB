class IllegalBehaveException(Exception):
    def __init__(self, msg):
        super(IllegalBehaveException, self).__init__()
        self.msg = msg
        self.code = 501

    def __str__(self):
        return "illegal behave: " + self.msg


class CantFindError(Exception):
    def __init__(self, where, msg):
        super().__init__()
        self.msg = "msg: {}, where:{}".format(msg, where)
    
    def __str__(self) -> str:
        return self.msg


def exception_handler(func, *args, **kwargs):
    try:
        func(*args, **kwargs)
    except CantFindError:  # TODO: 拦截异常，可以在查找的时候不用链式返回，直接raise Exception退出查询
        return None