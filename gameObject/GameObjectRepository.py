from cgitb import text
import gc
from gameObject.planet import Planet
from gameObject.campaign import Campaign
from gameObject.traderoutes import TradeRoute
from gameObject.unit import Unit
from gameObject.faction import Faction
from gameObject.campaignset import CampaignSet
from gameObject.TextHandler import *
import os, sys, lxml.etree as et



class ModRepository:
    def __init__(self, mod_directory,log):
        self.mod_dir = mod_directory
        self.logfile = log
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
        self.mod_loaded = False
        self.init_repo()
    def get_ai_players(self):
        ai_players = []
        ai_folder = self.mod_dir+'/xml/AI/Players'
        self.logfile.write(f'Collecting AI Players From Directory {ai_folder}\n')
        ai_files = os.listdir(ai_folder)
        for file in ai_files:
            self.logfile.write(f'Collecting AI Player From File {file}\n')
            file = et.parse(ai_folder+'/'+file).getroot()
            for child in file:
                if child.tag == 'Name':
                    self.logfile.write(f'Adding AI Player {child.text}\n')
                    ai_players.append(child.text.replace(" ", ""))
        return ai_players
    def get_game_constants(self):
        self.logfile.write(f'Unpacking GameConstants.xml\n')
        if os.path.isdir('xml'):
            xmlPath = '\\xml\\'
        else:
            xmlPath = '\\XML\\'
        gameConstants = et.parse(self.mod_dir+xmlPath+'gameconstants.xml').getroot()
        
        return gameConstants
    def get_faction_files(self):
        faction_files = []
        if os.path.isdir('xml'):
            xmlPath = '\\xml\\'
        else:
            xmlPath = '\\XML\\'

        self.logfile.write(f'Collecting Faction Files From File {self.mod_dir+xmlPath}factionfiles.xml\n')
        factionfiles = et.parse(self.mod_dir+xmlPath+'factionfiles.xml')
        
        for child in factionfiles.getroot():
            if child.tag == 'File':
                faction_files.append(self.mod_dir+xmlPath+child.text)
        return faction_files
    def get_trade_routes(self):
        tradeRoute_files = []
        if os.path.isdir('xml'):
            xmlPath = '\\xml\\'
        else:
            xmlPath = '\\XML\\'
        self.logfile.write(f'Collecting Trade Route Files From File {self.mod_dir+xmlPath}traderoutefiles.xml\n')
        tradeRouteFiles = et.parse(self.mod_dir+xmlPath+'traderoutefiles.xml')
        for child in tradeRouteFiles.getroot():
            if child.tag == 'File':
                tradeRoute_files.append(self.mod_dir+xmlPath+child.text)
        return tradeRoute_files
    def get_hardpoint_files(self):
        hardPoint_files = []
        if os.path.isdir('xml'):
            xmlPath = '\\xml\\'
        else:
            xmlPath = '\\XML\\'
        self.logfile.write(f'Collecting Hard Point Files From File {self.mod_dir+xmlPath}hardpointdatafiles.xml\n')
        hardpointdatafiles = et.parse(self.mod_dir+xmlPath+'hardpointdatafiles.xml')
        for child in hardpointdatafiles.getroot():
            if child.tag == 'File':
                hardPoint_files.append(self.mod_dir+xmlPath+child.text)
        return hardPoint_files
    def get_game_object_files(self):
        game_object_files = []
        if os.path.isdir('xml'):
            xmlPath = '\\xml\\'
        else:
            xmlPath = '\\XML\\'
        gameObjectFiles = et.parse(self.mod_dir+xmlPath+'gameobjectfiles.xml')
        self.logfile.write(f'Collecting Game Object Files From File {self.mod_dir+xmlPath}gameobjectfiles.xml\n')
        for child in gameObjectFiles.getroot():
            if child.tag == 'File':
                self.logfile.write(f'Unpacking Game Object File {child.text}\n')
                game_object_files.append(self.mod_dir+xmlPath+child.text)
        return game_object_files
    def get_galactic_conquests(self):
        campaign_files = []
        if os.path.isdir('xml'):
            xmlPath = '\\xml\\'
        else:
            xmlPath = '\\XML\\'
        campaignFiles = et.parse(self.mod_dir+xmlPath+'campaignfiles.xml')
        self.logfile.write(f'Collecting Campaign Files From File {self.mod_dir+xmlPath}campaignfiles.xml\n')
        for child in campaignFiles.getroot():
            if child.tag == 'File':
                campaign_files.append(self.mod_dir+xmlPath+child.text)
        return campaign_files
    def init_repo(self):
        for file in self.faction_files:
            self.logfile.write(f'Unpacking Factions From File {file}\n')
            root = et.parse(file).getroot()
            for child in root:
                if child.tag == 'Faction':
                    self.logfile.write('Adding Faction '+child.get('Name')+'\n')
                    self.factions.append(Faction(child,file))
        for file in self.game_object_files:
            root = et.parse(file).getroot()
            self.logfile.write(f'Unpacking Objects From File {file}\n')
            if root.tag == 'Planets':
                self.planetFiles.append(file)
            for child in root:
                if child.tag == 'Planet':
                    if child.get('Name') != 'Galaxy_Core_Art_Model':
                        self.logfile.write('Adding Planet '+child.get('Name')+'\n')
                        self.planets.append(Planet(child, file,self.logfile))
                        if not file in self.planetFiles:
                            self.planetFiles.append(file)
                if child.tag == 'SpaceUnit' or child.tag == 'UniqueUnit' or child.tag == 'SpecialStructure' or child.tag == 'GroundCompany' or child.tag == 'HeroUnit' or child.tag == 'HeroCompany' or child.tag == 'GroundUnit' or child.tag == 'Squadron' or child.tag =='SpaceStructure' or child.tag == 'StarBase' or child.tag =='GroundStructure' or child.tag == 'GroundBase':
                    if 'death_clone' not in child.get('Name').lower():
                        self.logfile.write('Adding Unit '+child.get('Name')+'\n')
                        self.units.append(Unit(child,file,self.mod_dir))
        for file in self.tradeRoute_files:
            root = et.parse(file).getroot()
            self.logfile.write(f'Unpacking Trade Routes From File {file}\n')
            for child in root:
                if child.tag == 'TradeRoute':
                    self.logfile.write('Adding Trade Route '+child.get('Name')+'\n')
                    route = TradeRoute(child, file)
                    try:
                        route.set_point_planets(self.planets)
                        self.trade_routes.append(route)
                    except Exception as e:
                        self.logfile.write('Error while attempting to set points for trade route '+child.get('Name')+'\n' + str(e)+'\n')
        for file in self.campaign_files:
            self.logfile.write(f'Unpacking Campaigns From File {file}\n')
            try:
                root = et.parse(file).getroot()
            except:
                self.logfile.write(f"File {file} doesn't exist\n")
            for child in root:
                if child.tag == 'Campaign':
                    self.logfile.write('Adding Campaign '+child.get('Name')+'\n')
                    self.campaigns[child.get('Name')] = Campaign(child, self.planets, self.trade_routes, file, self.factions, self.logfile)
                    for j in child:
                        if j.tag == 'Campaign_Set':
                            campaignsetname = j.text.replace(" ","")
                            if campaignsetname in self.campaign_sets.keys():
                                self.campaign_sets[campaignsetname].addCampaign(self.campaigns[child.get('Name')])
                            else:
                                self.campaign_sets[campaignsetname] = CampaignSet(campaignsetname)
                                self.campaign_sets[campaignsetname].addCampaign(self.campaigns[child.get('Name')])
        self.mod_loaded = 'true'
    def save_to_file(self):
        if os.path.isdir('xml'):
            xmlPath = '\\xml\\'
        else:
            xmlPath = '\\XML\\'

        self.logfile.write('Creating Save Containers For Trade Routes And Campaigns\n')
        self.logfile.flush()
        #Init Save Containers, for iteration by file
        tradeRoutes = SaveContainer(self.trade_routes)
        campaigns = SaveContainer(self.campaigns)

        #Init New Campaign Files Tree
        self.logfile.write('Initialising Element Tree For Campaign Files\n')
        self.logfile.flush()
        campaignFilesRoot = et.Element('Campaign_Files')
        
        #Compile Dat
        self.logfile.write('Compiling MasterTextFile_ENGLISH.dat\n')
        self.logfile.flush()
        self.text_handler.compileDat(self.text_dict)

        #Build Trade Routes
        for file in self.tradeRoute_files:
            self.logfile.write(f'Building Trade Route Element Tree In File {file}\n')
            self.logfile.flush()
            routes = tradeRoutes[file]
            fileRoot = et.Element("TradeRoutes")
            for i in routes:
                self.logfile.write(f'Building Element For Trade Route {i.name}\n')
                self.logfile.flush()
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
            self.logfile.write(f'Writing Element Tree To File {file}\n')
            self.logfile.flush()
            fileTree = et.ElementTree(fileRoot)
            fileTree.write(file,xml_declaration=True, encoding='UTF-8',pretty_print=True)

        
        for file in self.campaign_files:
            self.logfile.write(f'Building Campaign Element Tree In File {file}\n')
            self.logfile.flush()
            fileEntry = et.SubElement(campaignFilesRoot,"File")
            fileEntry.text = file.replace(self.mod_dir+xmlPath,'')
            gcs = campaigns[file]
            fileRoot = et.Element('Campaigns')
            for conquest in gcs:
                self.logfile.write(f'Building Element For Campaign {conquest.name}\n')
                self.logfile.flush()
                gcElem = et.SubElement(fileRoot, 'Campaign')
                gcElem.set('Name',conquest.name)
                sortOrderElem = et.SubElement(gcElem, 'Sort_Order')
                sortOrderElem.text = str(conquest.sort_order)

                setElem = et.SubElement(gcElem, 'Campaign_Set')
                setElem.text = conquest.setName

                textElem = et.SubElement(gcElem, 'Text_ID')
                textElem.text = conquest.text_name

                descElem = et.SubElement(gcElem, 'Description_Text')
                descElem.text = conquest.desc_name

                cameraXElem = et.SubElement(gcElem,'Camera_Shift_X')
                cameraXElem.text = str(40.0)

                cameraYElem = et.SubElement(gcElem, 'Camera_Shift_Y')
                cameraYElem.text = str(0.0)

                cameraDistanceElem = et.SubElement(gcElem, 'Camera_Distance')
                cameraDistanceElem.text = str(1200.0)

                self.logfile.write(f'Writing Locations To Element Tree For Conquest {conquest.name}\n')
                self.logfile.flush()
                locationsElem = et.SubElement(gcElem, 'Locations')
                locationsText = 'Galaxy_Core_Art_Model'
                for i in conquest.planets:
                    locationsText = locationsText+',\n\t\t\t'+i.name
                locationsElem.text = locationsText

                self.logfile.write(f'Writing Trade Routes To Element Tree For Conquest {conquest.name}\n')
                self.logfile.flush()
                tradeRoutesElem = et.SubElement(gcElem, 'Trade_Routes')
                routesText = ''
                for i in conquest.trade_routes:
                    routesText = routesText+i.name+',\n\t\t\t'
                tradeRoutesElem.text = routesText

                self.logfile.write(f'Writing Home Locations To Element Tree For Conquest {conquest.name}\n')
                self.logfile.flush()
                for faction, location in conquest.home_locations.items():
                    elem = et.SubElement(gcElem, 'Home_Locations')
                    elem.text = faction+', '+location

                activePlayerElem = et.SubElement(gcElem, 'Starting_Active_Player')
                activePlayerElem.text = conquest.activeFaction

                self.logfile.write(f'Writing Story Plots To Element Tree For Conquest {conquest.name}\n')
                self.logfile.flush()
                for faction, plot, in conquest.plots.items():
                    plotElem = et.SubElement(gcElem, 'Story_Name')
                    plotElem.text = faction+', '+plot
                
                self.logfile.write(f'Writing AI Player Control To Element Tree For Conquest {conquest.name}\n')
                self.logfile.flush()
                for faction, player in conquest.ai_players.items():
                    elem = et.SubElement(gcElem, 'AI_Player_Control')
                    elem.text = faction+', '+player

                self.logfile.write(f'Writing Markup Filenames To Element Tree For Conquest {conquest.name}\n')
                self.logfile.flush()
                for faction in self.factions:
                    elem = et.SubElement(gcElem, 'Markup_Filename')
                    elem.text = faction.name+', DefaultGalacticHints'

                self.logfile.write(f'Writing Starting Credits To Element Tree For Conquest {conquest.name}\n')
                self.logfile.flush()
                for faction, startingcredits in conquest.starting_credits.items():
                    elem = et.SubElement(gcElem, 'Starting_Credits')
                    elem.text = faction+', '+str(startingcredits)

                self.logfile.write(f'Writing Starting Tech To Element Tree For Conquest {conquest.name}\n')
                self.logfile.flush()
                for faction,startingtech in conquest.starting_tech.items():
                    elem =et.SubElement(gcElem, 'Starting_Tech_Level')
                    elem.text = faction+', '+str(startingtech)

                self.logfile.write(f'Writing Max Tech To Element Tree For Conquest {conquest.name}\n')
                self.logfile.flush()
                for faction, maxtech in conquest.max_tech_level.items():
                    elem = et.SubElement(gcElem, 'Max_Tech_Level')
                    elem.text = faction+', '+str(maxtech)

                customSettingsElem = et.SubElement(gcElem, 'Supports_Custom_Settings')
                customSettingsElem.text = 'False'

                completedTabElem = et.SubElement(gcElem, 'Show_Completed_Tab')
                completedTabElem.text = 'True'

                humanWinConditions = et.SubElement(gcElem, 'Human_Victory_Conditions')
                humanWinConditions.text = 'Galactic_All_Planets_Controlled'

                aiWinConditions = et.SubElement(gcElem, 'AI_Victory_Conditions')
                aiWinConditions.text = 'Galactic_All_Planets_Controlled'

                self.logfile.write(f'Writing Starting Forces To Element Tree For Conquest {conquest.name}\n')
                self.logfile.flush()
                for planet in conquest.planets:
                    forcestable = conquest.starting_forces[planet]
                    for force in forcestable:
                        for i in range(force.quantity):
                            forceElem = et.SubElement(gcElem, 'Starting_Forces')
                            forceElem.text = force.owner+', '+force.planet+', '+force.unit
            self.logfile.write(f'Writing Element Tree To File {file}\n')
            self.logfile.flush()
            fileTree = et.ElementTree(fileRoot)
            fileTree.write(file,xml_declaration=True, encoding='UTF-8',pretty_print=True)

        self.logfile.write(f'Writing Campaign Files Element Tree To File CampaignFiles.xml\n')
        self.logfile.flush()
        campaignFilesET = et.ElementTree(campaignFilesRoot)
        campaignFilesET.write(self.mod_dir+xmlPath+'campaignfiles.xml',xml_declaration=True, encoding='UTF-8',pretty_print=True)

        self.logfile.write(f'Finished Saving Successfully\n')
        self.logfile.flush()


class SaveContainer:
    def __init__(self, objList):
        self.objects = objList
    def __getitem__(self, file):
        objs = []
        if type(self.objects) == dict:
            self.objects = self.objects.values()
        for obj in self.objects:
            if obj.fileLocation == file:
                objs.append(obj)
        return objs