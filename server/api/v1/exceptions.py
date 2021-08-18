class ServerException(Exception):
    def __init__(self, information_text: str) -> None:
        self.info = information_text
        super().__init__(
            f"Server creation error: {information_text}"
        )

class CommandException(Exception):
    def __init__(self, information_text: str) -> None:
        self.info = information_text
        super().__init__(
            f"Server creation error: {information_text}"
        )
