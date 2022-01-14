from os import name
import lxml.etree as et
import copy
class CampaignSet:
    def __init__(self, name):
        self.name = name
        self.playableFactions = {}

    def addCampaign(self, campaign):
        self.playableFactions[campaign.activeFaction] = campaign
    def getactivecampaign(self, faction):
        return self.playableFactions[faction]
    def addFaction(self, factionName):
        campaigna = None
        for faction, campaign in self.playableFactions.items():
            campaigna = campaign
            break

        self.playableFactions[factionName] = copy.deepcopy(campaigna)
        self.playableFactions[factionName].activeFaction = factionName
        self.playableFactions[factionName].name = self.name+'_'+factionName
        print(self.playableFactions[factionName].name)
        return self.playableFactions[factionName]


class NewCampaign:
    def __init__(self, name, faction,planets, tradeRoutes, fileLocation):
        self.fileLocation = fileLocation
        self.activeFaction = faction
        self.name = name
        self.planets = planets
        self.trade_routes= tradeRoutes
