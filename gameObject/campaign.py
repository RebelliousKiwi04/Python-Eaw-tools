
class Campaign:
    def __init__(self, name: str):
        self.__name: str = name
        self.__setName: str = "Empty"
        self.__planets = []
        self.__tradeRoutes= []
        self.__ai_players = []

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        if value:
            self.__name = value

    @property
    def setName(self) -> str:
        return self.__setName

    @setName.setter
    def setName(self, value: str) -> None:
        if value:
            self.__setName = value

    @property
    def planets(self) -> list:
        return self.__planets

    @planets.setter
    def planets(self, value: list) -> None:
        if value is not None:
            self.__planets = value

    @property
    def tradeRoutes(self) -> list:
        return self.__tradeRoutes

    @tradeRoutes.setter
    def tradeRoutes(self, value: list) -> None:
        if value is not None:
            self.__tradeRoutes = value