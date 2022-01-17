from gameObject.planet import Planet
from gameObject.campaign import Campaign
from gameObject.traderoutes import TradeRoute
from gameObject.unit import Unit
from gameObject.faction import Faction
from gameObject.campaignset import CampaignSet
from gameObject.TextHandler import TextFile
import os, sys, lxml.etree as et



class ModRepository:
    def __init__(self, mod_directory):
        self.mod_dir = mod_directory
        self.game_object_files = self.get_game_object_files()
        self.campaign_files = self.get_galactic_conquests()
        self.hardpoint_files = self.get_hardpoint_files()
        self.tradeRoute_files = self.get_trade_routes()
        self.faction_files = self.get_faction_files()
        self.gameConstants = self.get_game_constants()
        self.text_handler = TextFile(self.mod_dir, 'dict')
        self.text_dict = self.text_handler.decompileDat()
        self.planetFiles = []
        self.planets = []
        self.units = []
        self.ai_players = self.get_ai_players()
        self.factions = []
        self.hardpoints = {}
        self.text = {}
        self.campaigns = {}
        self.campaign_sets = {}
        self.trade_routes = []
        self.init_repo()
    def get_ai_players(self):
        ai_players = []
        ai_folder = self.mod_dir+'/xml/AI/Players'
        ai_files = os.listdir(ai_folder)
        for file in ai_files:
            file = et.parse(ai_folder+'/'+file).getroot()
            for child in file:
                if child.tag == 'Name':
                    ai_players.append(child.text.replace(" ", ""))
        return ai_players
    def get_game_constants(self):
        if os.path.isdir('xml'):
            xmlPath = '/xml/'
        else:
            xmlPath = '/XML/'
        gameConstants = et.parse(self.mod_dir+xmlPath+'/gameconstants.xml').getroot()
        
        return gameConstants
    def get_faction_files(self):
        faction_files = []
        if os.path.isdir('xml'):
            xmlPath = '/xml/'
        else:
            xmlPath = '/XML/'
        factionfiles = et.parse(self.mod_dir+xmlPath+'/factionfiles.xml')
        for child in factionfiles.getroot():
            if child.tag == 'File':
                faction_files.append(self.mod_dir+xmlPath+'/'+child.text)
        return faction_files
    def get_trade_routes(self):
        tradeRoute_files = []
        if os.path.isdir('xml'):
            xmlPath = '/xml/'
        else:
            xmlPath = '/XML/'
        tradeRouteFiles = et.parse(self.mod_dir+xmlPath+'/traderoutefiles.xml')
        for child in tradeRouteFiles.getroot():
            if child.tag == 'File':
                tradeRoute_files.append(self.mod_dir+xmlPath+'/'+child.text)
        return tradeRoute_files
    def get_hardpoint_files(self):
        hardPoint_files = []
        if os.path.isdir('xml'):
            xmlPath = '/xml/'
        else:
            xmlPath = '/XML/'
        hardpointdatafiles = et.parse(self.mod_dir+xmlPath+'/hardpointdatafiles.xml')
        for child in hardpointdatafiles.getroot():
            if child.tag == 'File':
                hardPoint_files.append(self.mod_dir+xmlPath+'/'+child.text)
        return hardPoint_files
    def get_game_object_files(self):
        game_object_files = []
        if os.path.isdir('xml'):
            xmlPath = '/xml'
        else:
            xmlPath = '/XML'
        gameObjectFiles = et.parse(self.mod_dir+xmlPath+'/gameobjectfiles.xml')
        for child in gameObjectFiles.getroot():
            if child.tag == 'File':
                game_object_files.append(self.mod_dir+xmlPath+'/'+child.text)
        return game_object_files
    def get_galactic_conquests(self):
        campaign_files = []
        if os.path.isdir('xml'):
            xmlPath = '/xml/'
        else:
            xmlPath = '/XML/'
        campaignFiles = et.parse(self.mod_dir+xmlPath+'/campaignfiles.xml')
        for child in campaignFiles.getroot():
            if child.tag == 'File':
                campaign_files.append(self.mod_dir+xmlPath+'/'+child.text)
        return campaign_files
    def init_repo(self):
        for file in self.faction_files:
            root = et.parse(file).getroot()
            for child in root:
                if child.tag == 'Faction':
                    self.factions.append(Faction(child,file))
        for file in self.game_object_files:
            root = et.parse(file).getroot()
            if root.tag == 'Planets':
                self.planetFiles.append(file)
            for child in root:
                if child.tag == 'Planet':
                    if child.get('Name') != 'Galaxy_Core_Art_Model':
                        self.planets.append(Planet(child, file))
                        if not file in self.planetFiles:
                            self.planetFiles.append(file)
                if child.tag == 'SpaceUnit' or child.tag == 'UniqueUnit' or child.tag == 'SpecialStructure' or child.tag == 'GroundCompany' or child.tag == 'HeroUnit' or child.tag == 'HeroCompany' or child.tag == 'GroundUnit' or child.tag == 'Squadron' or child.tag =='SpaceStructure' or child.tag == 'StarBase' or child.tag =='GroundStructure' or child.tag == 'GroundBase':
                    if 'death_clone' not in child.get('Name').lower():
                        self.units.append(Unit(child,file,self.mod_dir))
        for file in self.tradeRoute_files:
            root = et.parse(file).getroot()
            for child in root:
                if child.tag == 'TradeRoute':
                    route = TradeRoute(child, file)
                    route.set_point_planets(self.planets)
                    self.trade_routes.append(route)
        for file in self.campaign_files:
            try:
                root = et.parse(file).getroot()
            except:
                print(f"File {file} doesn't exist")
            for child in root:
                if child.tag == 'Campaign':
                    self.campaigns[child.get('Name')] = Campaign(child, self.planets, self.trade_routes, file, self.factions)
                    for j in child:
                        if j.tag == 'Campaign_Set':
                            campaignsetname = j.text.replace(" ","")
                            if campaignsetname in self.campaign_sets.keys():
                                self.campaign_sets[campaignsetname].addCampaign(self.campaigns[child.get('Name')])
                            else:
                                self.campaign_sets[campaignsetname] = CampaignSet(campaignsetname)
                                self.campaign_sets[campaignsetname].addCampaign(self.campaigns[child.get('Name')])
    def save_to_file(self):
        if os.path.isdir('xml'):
            xmlPath = '/xml/'
        else:
            xmlPath = '/XML/'

        #Init Save Containers, for iteration by file
        tradeRoutes = SaveContainer(self.trade_routes)
        campaigns = SaveContainer(self.campaigns)

        #Init New Campaign Files Tree
        campaignFilesRoot = et.Element('Campaign_Files')
        
        #Compile Dat
        self.text_handler.compileDat(self.text_dict)

        #Build Trade Routes
        for file in self.tradeRoute_files:
            routes = tradeRoutes[file]
            fileRoot = et.Element("TradeRoutes")
            for i in routes:
                element = et.SubElement(fileRoot, 'TradeRoute')
                element.set('Name', i.name)
                pointAElem = et.SubElement(element, 'Point_A')
                pointAElem.text = i.point_A

                pointBElem = et.SubElement(element, 'Point_B')
                pointBElem.text = i.point_B

                hsSpeedFactorElem = et.SubElement(element, 'HS_Speed_Factor')
                hsSpeedFactorElem.text = str(1.0)

                politicalGainElem = et.SubElement(element, 'Political_Control_Gain')
                politicalGainElem.text = str(0)

                creditGainElem = et.SubElement(element, 'Credit_Gain_Factor')
                creditGainElem.text= str(0)

                visibleLineElem = et.SubElement(element, 'Visible_Line_Name')
                visibleLineElem.text = 'DEFAULT'
            fileTree = et.ElementTree(fileRoot)
            print(self.mod_dir+xmlPath+file)
            fileTree.write(self.mod_dir+xmlPath+file,xml_declaration=True, encoding='UTF-8',pretty_print=True)

        
        for file in self.campaign_files:
            fileEntry = et.SubElement(campaignFilesRoot,"File")
            fileEntry.text = file

            gcs = campaigns[file]

        campaignFilesET = et.ElementTree(campaignFilesRoot)
        campaignFilesET.write(self.mod_dir+xmlPath+'/campaignfiles.xml',xml_declaration=True, encoding='UTF-8',pretty_print=True)


class SaveContainer:
    def __init__(self, objList):
        self.objects = objList
    def __getitem__(self, file):
        objs = []

        for obj in self.objects:
            if obj.fileLocation == file:
                objs.append(obj)
        return objs