
class Unit:
    def __init__(self, name: str, aicp: str):
        self.__name: str = name
        self.aicp = aicp

    @property
    def aicp(self) -> str:
        return self.aicp

    @aicp.setter
    def aicp(self, value: str) -> None:
        if value:
            self.aicp = value

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        if value:
            self.__name = value