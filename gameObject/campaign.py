
class Campaign:
    def __init__(self, xml_entry, planets):
        self.entry = xml_entry
        self.name = xml_entry.get('Name')
        self.__setName: str = "Empty"
        self.planets = []
        self.__tradeRoutes= []
        self.__ai_players = []
        for i in self.get_planets():
            for j in planets:
                if j.name == i:
                    self.planets.append(j)

    def get_planets(self):
        for item in self.entry:
            if item.tag == 'Locations':
                outputList = []
                for text in item.text.split():
                    newText = text.replace(',','')
                    outputList.append(newText)
                return outputList

