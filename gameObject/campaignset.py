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

