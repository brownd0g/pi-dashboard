
class Esp:
    def __init__(self, name=None, ip=None, data="none", path=None):
        self.name = name
        self.ip = ip
        self.data = data
        self.path = ip + path
        self.status = "offline"
        self.request_args = None

    def get_json(self):
        dict_1 = {"status": self.status, "ip": self.ip, "data": self.data}
        dict_2 = {self.name: dict_1}

        return dict_2

    def set_data(self, data):
        self.data = data

    def get_data(self):
        return self.data

    def set_status(self, status):
        self.status = status

    def get_status(self):
        return self.status

    def set_request_args(self, args):
        self.request_args = args

    def get_request_args(self):
        return self.request_args


