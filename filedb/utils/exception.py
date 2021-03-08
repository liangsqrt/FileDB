class IllegalBehaveException(Exception):
    def __init__(self, msg):
        super(IllegalBehaveException, self).__init__()
        self.msg = msg
        self.code = 501

    def __str__(self):
        return "illegal behave: " + self.msg

