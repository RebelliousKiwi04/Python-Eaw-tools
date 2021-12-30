import lxml.etree as et

class Campaign:
    def __init__(self, xml_entry, planets, tradeRoutes, fileLocation):
        self.fileLocation = fileLocation
        self.entry = xml_entry
        self.activeFaction = self.get_active_faction()
        self.name = xml_entry.get('Name')
        self.setName: str = self.get_set_name()
        self.planets = []
        self.max_tech_level = self.get_max_tech()
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
    def get_active_faction(self):
        for item in self.entry:
            if item.tag == 'Starting_Active_Player':
                return item.text
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
                return outputList
    def get_max_tech(self):
        max_tech = []
        for item in self.entry:
            if item.tag == 'Max_Tech_Level':
                outputList = []
                for text in item.text.split():
                    newText = text.replace(',','')
                    outputList.append(newText)
                max_tech.append(int(outputList[1]))
        # self.using_deepcore = bool(et.parse('config.xml').getroot().find("Using_Deepcore").text)
        # print(self.using_deepcore)
        if len(max_tech) >0:
            return max(max_tech)

        return None


