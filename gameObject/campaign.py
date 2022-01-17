import lxml.etree as et, sys
from gameObject.StartingForcesObject import StartingForcesObject

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
        self.logfile = logfile
        self.fileLocation = fileLocation
        self.entry = xml_entry
        self.name = xml_entry.get('Name')
        self.activeFaction = self.get_active_faction()
        
        self.setName: str = self.get_set_name()
        self.max_tech_level = self.get_max_tech()
        self.starting_tech = self.get_starting_tech()
        self.ai_players = self.get_ai_players()
        self.home_locations = self.get_home_locations()
        self.starting_credits = self.get_starting_credits()
        self.sort_order = int(self.get_sort_order())
        self.text_name = self.get_text_id()
        self.desc_name = self.get_desc_id()
        self.plots = self.get_story_plots()
        self.all_factions = all_factions


        self.starting_forces = StartingForcesContainer()
        self.get_starting_forces()
        self.trade_routes= []
        self.planets = []
        for i in self.get_planets():
            for j in planets:
                if j.name == i:
                    self.planets.append(j)
        for i in self.get_trade_routes():
            for j in tradeRoutes:
                if j.name == i:
                    self.trade_routes.append(j)
    def get_story_plots(self):
        self.logfile.write(f'Collecting Story Plots For Conquest {self.name}\n')
        self.logfile.flush()
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
    def get_starting_forces(self):
        self.logfile.write(f'Collecting Starting Forces For Conquest {self.name}\n')
        self.logfile.flush()
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
                self.logfile.write(f'CRITICAL ERROR when reading starting forces for Conquest {self.name}\n')
                self.logfile.flush()
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
    def get_text_id(self):
        self.logfile.write(f'Collecting Text ID for conquest {self.name}\n')
        self.logfile.flush()
        for item in self.entry:
            if item.tag == 'Text_ID':
                return item.text.replace(" ", "")
    def get_desc_id(self):
        self.logfile.write(f'Collecting Description ID for conquest {self.name}\n')
        self.logfile.flush()
        for item in self.entry:
            if item.tag == 'Description_Text':
                return item.text.replace(" ", "")
    def get_active_faction(self):
        self.logfile.write(f'Collecting Active Player Name for conquest {self.name}\n')
        self.logfile.flush()
        for item in self.entry:
            if item.tag == 'Starting_Active_Player':
                return item.text.replace(" ", "")
    def get_set_name(self):
        self.logfile.write(f'Collecting Campaign Set for conquest {self.name}\n')
        self.logfile.flush()
        for item in self.entry:
            if item.tag == 'Campaign_Set':
                return item.text
    def get_sort_order(self):
        self.logfile.write(f'Collecting Sort Order for conquest {self.name}\n')
        self.logfile.flush()
        for item in self.entry:
            if item.tag == 'Sort_Order':
                return item.text.replace(' ','')
    def get_planets(self):
        self.logfile.write(f'Collecting Locations for conquest {self.name}\n')
        self.logfile.flush()
        for item in self.entry:
            if item.tag == 'Locations':
                outputList = []
                for text in item.text.split():
                    newText = text.replace(',','')
                    outputList.append(newText)
        return outputList
    def get_trade_routes(self):
        self.logfile.write(f'Collecting Trade Routes for conquest {self.name}\n')
        self.logfile.flush()
        for item in self.entry:
            if item.tag == 'Trade_Routes':
                outputList = []
                if item.text:
                    for text in item.text.split():
                        newText = text.replace(',','')
                        outputList.append(newText)
        return outputList
    def get_max_tech(self):
        self.logfile.write(f'Collecting Max Tech Levels for conquest {self.name}\n')
        self.logfile.flush()
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
    def get_starting_credits(self):
        self.logfile.write(f'Collecting Starting Credits for conquest {self.name}\n')
        self.logfile.flush()
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
    def get_starting_tech(self):
        self.logfile.write(f'Collecting Starting Tech Levels for conquest {self.name}\n')
        self.logfile.flush()
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
    def get_ai_players(self):
        self.logfile.write(f'Collecting AI Players for conquest {self.name}\n')
        self.logfile.flush()
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
    def get_home_locations(self):
        self.logfile.write(f'Collecting Home Locations for conquest {self.name}\n')
        self.logfile.flush()
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


