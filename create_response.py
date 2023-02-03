from flask import make_response


class Esp:
    def __init__(self, name=None, ip=None, data="none"):
        self.name = name
        self.ip = ip
        self.data = data
        self.ip_paths = {}
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


def create_json_response(esps):
    json_return = {}
    for item in esps:
        json_return = json_return | item.get_json()
    return make_response(json_return)
