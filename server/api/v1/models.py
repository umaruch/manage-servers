class Server:
    """
        Информация о сервере
    """
    id: int
    address: int
    name: str

    def __init__(self, id, address, name):
        self.id = id
        self.address = address
        self.name = name

    @property
    def json(self):
        return {
            "id": self.id,
            "address": self.address,
            "name": self.name
        }


class Script:
    """
        Информация о задаче, выполняемой
        на сервере
    """
    id: int
    server_id: int
    name: str
    args_string: str

    def __init__(self, id, server_id, name, args_string):
        self.id = id
        self.server_id = server_id
        self.name = name
        self.args_string =args_string

    @property
    def json(self):
        return {
            "id": self.id,
            "server_id": self.server_id,
            "name": self.name,
            "args": self.args_string
        }
