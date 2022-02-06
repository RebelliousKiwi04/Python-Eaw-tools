from cmath import log
from math import sqrt
import lxml.etree as et, sys

class Planet:
    def __init__(self, xml_entry, fileLocation, logfile):
        self.fileLocation = fileLocation
        self.entry = xml_entry
        self.planet_owners = {}
        self.name = self.get_planet_name(logfile)
        self.text_key = self.get_text_key(logfile)
        
        self.land_map = self.get_land_map(logfile)
        self.space_map = self.get_space_map(logfile)
        self.x, self.y = self.get_position(logfile)
        self.terrain_index = self.get_terrain_index(logfile)
        self.land_structures = self.get_land_structures(logfile)
        self.galactic_model = self.get_galactic_model(logfile)
        self.destroyed_model = self.get_destroyed_model(logfile)
        self.additional_pop = self.get_additional_pop(logfile)
        self.land_accessible = self.get_planet_accessbile(logfile)
    def get_terrain_index(self,logfile):
        logfile.write(f'Getting Terrain Index for planet {self.name}\n')
        for child in self.entry:
            if child.tag == 'Zoomed_Terrain_Index':
                try:
                    return child.text
                except:
                    logfile.write(f'CRITICAL ERROR Failed To Return string for Zoomed_Terrain_Index of planet {self.name}\n')
                    logfile.flush()
                    return 0
    def get_land_structures(self,logfile):
        logfile.write(f'Getting Land Slots for planet {self.name}\n')
        for child in self.entry:
            if child.tag == 'Special_Structures_Land':
                try:
                    return child.text
                except:
                    logfile.write(f'CRITICAL ERROR Failed To Return string for Special_Structures_Land of planet {self.name}\n')
                    logfile.flush()
                    return 3
    def get_galactic_model(self,logfile):
        logfile.write(f'Getting Galactic Model for planet {self.name}\n')
        for child in self.entry:
            if child.tag == 'Galactic_Model_Name':
                try:
                    return child.text
                except:
                    logfile.write(f'CRITICAL ERROR Failed To Return string for Galactic_Model_Name of planet {self.name}\n')
                    logfile.flush()
                    return 'W_planet_Temperate01.alo'
    def get_destroyed_model(self,logfile):
        logfile.write(f'Getting Destroyed Model for planet {self.name}\n')
        for child in self.entry:
            if child.tag == 'Destroyed_Galactic_Model_Name':
                try:
                    return child.text
                except:
                    logfile.write(f'CRITICAL ERROR Failed To Return string for Destroyed_Galactic_Model_Name of planet {self.name}\n')
                    logfile.flush()
                    return 'W_planet_Asteroids.alo'
    def get_additional_pop(self,logfile):
        logfile.write(f'Getting Additional Population Capacity for planet {self.name}\n')
        for child in self.entry:
            if child.tag == 'Additional_Population_Capacity':
                try:
                    return int(child.text)
                except:
                    logfile.write(f'CRITICAL ERROR Failed To Return string for Additional_Population_Capacity of planet {self.name}\n')
                    logfile.flush()
                    return 50
    def get_planet_accessbile(self,logfile):
        logfile.write(f'Getting Surface Accessilbe for planet {self.name}\n')
        for child in self.entry:
            if child.tag == 'Planet_Surface_Accessible':
                try:
                    return child.text
                except:
                    logfile.write(f'CRITICAL ERROR Failed To Return string for Planet_Surface_Accessible of planet {self.name}\n')
                    logfile.flush()
                    return 'Yes'
    def get_text_key(self,logfile):
        logfile.write(f'Getting Text ID for planet {self.name}\n')
        for child in self.entry:
            if child.tag == 'Text_ID':
                try:
                    return child.text
                except:
                    logfile.write(f'CRITICAL ERROR Failed To Return string for Text_ID of planet {self.name}\n')
                    logfile.flush()
                    sys.exit()
    def distanceTo(self, target):
        return sqrt((self.x - target.x)**2 + (self.y - target.y)**2)
    def get_planet_name(self,logfile) -> str:
        logfile.write(f'Getting Planet Name\n')
        return self.entry.get('Name')
    def get_land_map(self,logfile) -> str:
        logfile.write(f'Getting Land Map For Planet {self.name}\n')
        for child in self.entry:
            if child.tag == 'Land_Tactical_Map':
                try:
                    return child.text
                except:
                    logfile.write(f'CRITICAL ERROR Failed To Return string for Land Map Name of planet {self.name}\n')
                    logfile.flush()
                    sys.exit()
    def get_space_map(self,logfile) -> str:
        logfile.write(f'Getting Space Map For Planet {self.name}\n')
        for child in self.entry:
            if child.tag == 'Space_Tactical_Map':
                try:
                    return child.text
                except:
                    logfile.write(f'CRITICAL ERROR Failed To Return string for Space Map Name of planet {self.name}\n')
                    logfile.flush()
                    sys.exit()
    def get_position(self,logfile):
        logfile.write(f'Getting Galactic Position For Planet {self.name}\n')
        for child in self.entry:
            if child.tag == 'Galactic_Position':     
                entry = child.text     
                entry = entry.replace(',',' ')
                entry = entry.split()
                try:
                    return float(entry[0]), float(entry[1])
                except:
                    logfile.write(f'CRITICAL ERROR Failed To Return float for galactic position of planet {self.name}\n')
                    logfile.flush()
                    sys.exit()
        return 0,0
    # def get_model_name(self,logfile):
    #     logfile.write(f'Getting Model Name For Planet {self.name}\n')
    #     for child in self.entry:
    #         if child.tag == 'Galactic_Model_Name':     
    #             try:
    #                 return child.text
    #             except:
    #                 logfile.write(f'CRITICAL ERROR Failed To Return string for model name of planet {self.name}\n')
    #                 logfile.flush()
    #                 sys.exit()
                




