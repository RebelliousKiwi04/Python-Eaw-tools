from math import sqrt
import lxml.etree as et

class Planet:
    def __init__(self, xml_entry, fileLocation):
        self.fileLocation = fileLocation
        self.entry = xml_entry
        self.planet_owners = {}
        self.text_key = self.get_text_key()
        self.name = self.get_planet_name()
        self.land_map = self.get_land_map()
        self.space_map = self.get_space_map()
        self.x, self.y = self.get_position()
    def get_text_key(self):
        for child in self.entry:
            if child.tag == 'Text_ID':
                return child.text
    def distanceTo(self, target):
        return sqrt((self.x - target.x)**2 + (self.y - target.y)**2)
    def get_planet_name(self) -> str:
        return self.entry.get('Name')
    def get_land_map(self) -> str:
        for child in self.entry:
            if child.tag == 'Land_Tactical_Map':
                return child.text
    def get_space_map(self) -> str:
        for child in self.entry:
            if child.tag == 'Space_Tactical_Map':
                return child.text
    def get_position(self):
        for child in self.entry:
            if child.tag == 'Galactic_Position':     
                entry = child.text     
                entry = entry.replace(',',' ')
                entry = entry.split()
                return float(entry[0]), float(entry[1])
    def reset_starting_forces_table(self, campaigns):
        self.starting_forces = {}
        self.planet_owners = {}
        for name in campaigns.keys():
            self.starting_forces[name] = []
            self.planet_owners[name] = None
    def add_campaign_to_table(self, name):
        self.starting_forces[name] = []
    def get_model_name(self):
        for child in self.entry:
            if child.tag == 'Galactic_Model_Name':     
                return child.text




