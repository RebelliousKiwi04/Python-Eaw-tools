from os import name
import lxml.etree as et

class CampaignSet:
    def __init__(self, name):
        self.name = name
        self.playableFactions = {}

    def addCampaign(self, campaign):
        self.playableFactions[campaign.activeFaction] = campaign
    def getactivecampaign(self, faction):
        return self.playableFactions[faction]
    def addFaction(self, factionName):
        for faction, campaign in self.playableFactions.items():
            filelocation = campaign.fileLocation
            planets= campaign.planets
            traderoutes = campaign.trade_routes
            break

        self.playableFactions[factionName] = NewCampaign(self.name+'_'+factionName, factionName, planets, traderoutes, filelocation)
        return self.playableFactions[factionName]


class NewCampaign:
    def __init__(self, name, faction,planets, tradeRoutes, fileLocation):
        self.fileLocation = fileLocation
        self.activeFaction = faction
        self.name = name
        self.planets = planets
        self.trade_routes= tradeRoutes
