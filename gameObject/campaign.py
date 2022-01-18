import lxml.etree as et, sys
from gameObject.StartingForcesObject import StartingForcesObject
import copy
class StartingForcesContainer:
    def __init__(self):
        self.startingforcestable = []
    def __getitem__(self, planet):
        planet_name = planet
        if type(planet) != str:
            planet_name = planet.name
        
        planet_forces = []
        index = 0
        increment = 0
        for obj in self.startingforcestable:
            if obj.planet == planet_name:
                planet_forces.append(obj)
        return planet_forces
    def remove_obj(self, obj):
        index = self.startingforcestable.index(obj)
        popped = self.startingforcestable.pop(index)
        return popped
    def addItem(self, planet, unit, owner, quantity):
        self.startingforcestable.append(StartingForcesObject(planet, unit, owner, quantity))
    def addObject(self, obj):
        self.startingforcestable.append(obj)
    def get_all_forces_by_planet(self, planets):
        forces_dict = {}
        for planet in planets:
            forces_dict[planet] = tuple(self[planet])
        return forces_dict

def remove_values_from_list(the_list, val):
   return [value for value in the_list if value != val]

class Campaign:
    def __init__(self, xml_entry, planets, tradeRoutes, fileLocation, all_factions, logfile):
        self.fileLocation = fileLocation
        self.entry = xml_entry
        self.name = xml_entry.get('Name')
        self.activeFaction = self.get_active_faction(logfile)
        
        self.setName: str = self.get_set_name(logfile)
        self.max_tech_level = self.get_max_tech(logfile)
        self.starting_tech = self.get_starting_tech(logfile)
        self.ai_players = self.get_ai_players(logfile)
        self.home_locations = self.get_home_locations(logfile)
        self.starting_credits = self.get_starting_credits(logfile)
        self.sort_order = int(self.get_sort_order(logfile))
        self.text_name = self.get_text_id(logfile)
        self.desc_name = self.get_desc_id(logfile)
        self.plots = self.get_story_plots(logfile)
        self.all_factions = all_factions


        self.starting_forces = StartingForcesContainer()
        self.get_starting_forces(logfile)
        self.trade_routes= []
        self.planets = []
        for i in self.get_planets(logfile):
            for j in planets:
                if j.name == i:
                    self.planets.append(j)
        for i in self.get_trade_routes(logfile):
            for j in tradeRoutes:
                if j.name == i:
                    self.trade_routes.append(j)
        logfile.write(f'Deleting Local Variable logfile from campaign {self.name}\n')
        logfile.flush()
        del logfile
    def get_story_plots(self,logfile):
        logfile.write(f'Collecting Story Plots For Conquest {self.name}\n')
        logfile.flush()
        plots= {}
        for item in self.entry:
            if item.tag =='Empire_Story_Name':
                if not item.text:
                    plots['Empire'] = ''
                else:
                    plots['Empire'] = item.text.replace(" ","")
            elif item.tag == 'Rebel_Story_Name':
                if not item.text:
                    plots['Rebel'] = ''
                else:
                    plots['Rebel'] = item.text.replace(" ","")
            elif item.tag == 'Underworld_Story_Name':
                if not item.text:
                    plots['Underworld'] = ''
                else:
                    plots['Underworld'] = item.text.replace(" ","")
            elif item.tag == 'Story_Name':
                if item.text:
                    text = item.text.split(',')
                    plots[text[0].replace(' ','')] = text[1].replace(' ','')
        return plots
    def get_starting_forces(self,logfile):
        logfile.write(f'Collecting Starting Forces For Conquest {self.name}\n')
        logfile.flush()
        forces = []
        for item in self.entry:
            if item.tag == 'Starting_Forces':
                if item.text:
                    splitText = item.text.split(',')
                    finalText= []
                    for text in splitText:
                        newText = text.replace(" ","")
                        finalText.append(newText)
                    forces.append(finalText)
                
        while len(forces) > 0:
            val = forces[0]
            if len(val) != 3:
                logfile.write(f'CRITICAL ERROR when reading starting forces for Conquest {self.name}\n')
                logfile.flush()
                sys.exit()
            factionIndex = None
            for i in self.all_factions:
                try:
                    factionIndex = val.index(i.name)
                except:
                    pass
            if factionIndex == None:
                planet = val[0]
                faction = val[1]
            elif factionIndex == 1:
                planet = val[0]
                faction = val[1]
            else:
                planet = val[1]
                faction = val[0]
            unit = val[2]
            quantity = forces.count(val)
            self.starting_forces.addItem(planet, unit, faction, quantity)
            forces = remove_values_from_list(forces, val)
    def get_text_id(self,logfile):
        logfile.write(f'Collecting Text ID for conquest {self.name}\n')
        logfile.flush()
        for item in self.entry:
            if item.tag == 'Text_ID':
                return item.text.replace(" ", "")
    def get_desc_id(self,logfile):
        logfile.write(f'Collecting Description ID for conquest {self.name}\n')
        logfile.flush()
        for item in self.entry:
            if item.tag == 'Description_Text':
                return item.text.replace(" ", "")
    def get_active_faction(self,logfile):
        logfile.write(f'Collecting Active Player Name for conquest {self.name}\n')
        logfile.flush()
        for item in self.entry:
            if item.tag == 'Starting_Active_Player':
                return item.text.replace(" ", "")
    def get_set_name(self,logfile):
        logfile.write(f'Collecting Campaign Set for conquest {self.name}\n')
        logfile.flush()
        for item in self.entry:
            if item.tag == 'Campaign_Set':
                return item.text
    def get_sort_order(self,logfile):
        logfile.write(f'Collecting Sort Order for conquest {self.name}\n')
        logfile.flush()
        for item in self.entry:
            if item.tag == 'Sort_Order':
                return item.text.replace(' ','')
    def get_planets(self,logfile):
        logfile.write(f'Collecting Locations for conquest {self.name}\n')
        logfile.flush()
        for item in self.entry:
            if item.tag == 'Locations':
                outputList = []
                for text in item.text.split():
                    newText = text.replace(',','')
                    outputList.append(newText)
        return outputList
    def get_trade_routes(self,logfile):
        logfile.write(f'Collecting Trade Routes for conquest {self.name}\n')
        logfile.flush()
        for item in self.entry:
            if item.tag == 'Trade_Routes':
                outputList = []
                if item.text:
                    for text in item.text.split():
                        newText = text.replace(',','')
                        outputList.append(newText)
        return outputList
    def get_max_tech(self,logfile):
        logfile.write(f'Collecting Max Tech Levels for conquest {self.name}\n')
        logfile.flush()
        max_tech = {}
        for item in self.entry:
            if item.tag == 'Max_Tech_Level':
                splitText = item.text.split(',')
                finalText= []
                for text in splitText:
                    newText = text.replace(" ","")
                    finalText.append(newText)
                max_tech[finalText[0]] = int(finalText[1])
                
        return max_tech
    def get_starting_credits(self,logfile):
        logfile.write(f'Collecting Starting Credits for conquest {self.name}\n')
        logfile.flush()
        starting_credits = {}
        for item in self.entry:
            if item.tag == 'Starting_Credits':
                splitText = item.text.split(',')
                finalText= []
                for text in splitText:
                    newText = text.replace(" ","")
                    finalText.append(newText)
                if len(finalText) < 2:
                    # print(self.name)
                    # print(finalText)
                    pass
                else:
                    starting_credits[finalText[0]] = int(finalText[1])
                
        return starting_credits
    def get_starting_tech(self,logfile):
        logfile.write(f'Collecting Starting Tech Levels for conquest {self.name}\n')
        logfile.flush()
        min_tech = {}
        for item in self.entry:
            if item.tag == 'Starting_Tech_Level':
                if item.text:
                    splitText = item.text.split(',')
                    finalText= []
                    for text in splitText:
                        newText = text.replace(" ","")
                        finalText.append(newText)
                    min_tech[finalText[0]] = int(finalText[1])
                
        return min_tech
    def get_ai_players(self,logfile):
        logfile.write(f'Collecting AI Players for conquest {self.name}\n')
        logfile.flush()
        ai_players = {}
        for item in self.entry:
            if item.tag == 'AI_Player_Control':
                if item.text:
                    splitText = item.text.split(',')
                    finalText= []
                    for text in splitText:
                        newText = text.replace(" ","")
                        finalText.append(newText)
                    ai_players[finalText[0]] = finalText[1]
        return ai_players
    def get_home_locations(self,logfile):
        logfile.write(f'Collecting Home Locations for conquest {self.name}\n')
        logfile.flush()
        home_locations = {}
        for item in self.entry:
            if item.tag == 'Home_Location':
                if item.text:
                    splitText = item.text.split(',')
                    finalText= []
                    for text in splitText:
                        newText = text.replace(" ","")
                        finalText.append(newText)
                    home_locations[finalText[0]] = finalText[1]
        return home_locations
    # def copy(self, template):
    #     del self.starting_forces
    #     self.starting_forces = copy.deepcopy(template.starting_forces)
    #     del self.planets
    #     self.planets = []
    #     for i in template.planets:
    #         self.planets.append(i)
    #     del self.trade_routes 
    #     self.trade_routes = []
    #     for i in template.trade_routes:
    #         self.trade_routes.append(i)
    #     del self.home_locations
    #     self.home_locations = copy.deepcopy(template.home_locations)
    #     del self.ai_players
    #     self.ai_players = copy.deepcopy(template.ai_players)
    #     del self.starting_credits
    #     self.starting_credits = copy.deepcopy(template.starting_credits)
    #     del self.starting_tech
    #     self.starting_tech = copy.deepcopy(template.starting_tech)
    #     del self.max_tech_level
    #     self.max_tech_level = copy.deepcopy(template.max_tech_level)
    #     del self.sort_order
    #     self.sort_order = copy.deepcopy(template.sort_order)
    #     del self.plots
    #     self.plots = copy.deepcopy(template.plots)
    #     del self.text_name
    #     self.text_name = copy.deepcopy(template.text_name)
    #     del self.desc_name
    #     self.desc_name = copy.deepcopy(template.desc_name)

