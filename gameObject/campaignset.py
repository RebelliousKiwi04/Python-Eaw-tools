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
        return self.playableFactions[factionName]
