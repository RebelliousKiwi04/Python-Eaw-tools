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
            template = campaign
            break
        template.activeFaction=factionName
        template.name = self.name +'_'+factionName
        print(template.activeFaction)
        print(template.name)
        self.playableFactions[factionName] = template
        return template


