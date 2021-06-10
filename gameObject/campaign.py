
class Campaign:
    def __init__(self, xml_entry, planets, tradeRoutes, fileLocation):
        self.fileLocation = fileLocation
        self.entry = xml_entry
        self.name = xml_entry.get('Name')
        self.setName: str = self.get_set_name()
        self.planets = []
        self.trade_routes= []
        self.__ai_players = []
        for i in self.get_planets():
            for j in planets:
                if j.name == i:
                    self.planets.append(j)
        for i in self.get_trade_routes():
            for j in tradeRoutes:
                if j.name == i:
                    self.trade_routes.append(j)
    def get_set_name(self):
        for item in self.entry:
            if item.tag == 'Campaign_Set':
                return item.text
    def get_planets(self):
        for item in self.entry:
            if item.tag == 'Locations':
                outputList = []
                for text in item.text.split():
                    newText = text.replace(',','')
                    outputList.append(newText)
                return outputList
    def get_trade_routes(self):
        for item in self.entry:
            if item.tag == 'Trade_Routes':
                outputList = []
                for text in item.text.split():
                    newText = text.replace(',','')
                    outputList.append(newText)
                    print(newText)
                return outputList

