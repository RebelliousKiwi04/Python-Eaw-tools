from math import sqrt
import lxml.etree as et

class Planet:
    def __init__(self, xml_entry):
        self.entry = xml_entry
        self.name = self.get_planet_name()
        self.__land_map = self.get_land_map()
        self.__space_map = self.get_space_map()
        self.startingForces = {}
        self.x, self.y = self.get_position()
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


