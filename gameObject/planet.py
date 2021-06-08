from math import sqrt
import lxml.etree as et


class PlanetCreator:
    def __init__(self, xml_entry):
        self.entry = xml_entry
        return Planet(self.get_planet_name(), self.get_land_map(), self.get_space_map(), self.get_position())
    def get_planet_name(self) -> str:
        return 'some stuff'
    def get_land_map(self) -> str:
        return 'some stuff'
    def get_space_map(self) -> str:
        return 'some stuff'
    def get_position(self):
        return 'something', 'something'


class Planet:
    def __init__(self, name, land_map_name, space_map_name, x, y):
        self.__name = name
        self.__x = 0.0
        self.__y = 0.0
        self.__land_map = land_map_name
        self.__space_map = space_map_name
        self.startingForces = {}
    
    def distanceTo(self, target):
        return sqrt((self.x - target.x)**2 + (self.y - target.y)**2)

    @property
    def land_map(self) -> str:
        return self.__land_map

    @land_map.setter
    def land_map(self,value: str) -> None:
        if value:
            self.__land_map = value
        
    @property
    def space_map(self) -> str:
        return self.__space_map

    @space_map.setter
    def space_map(self, value: str) -> None:
        if value:
            self.__space_map = value

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        if value:
            self.__name = value

    @property
    def x(self) -> float:
        return self.__x

    @x.setter
    def x(self, value: float) -> None:
        self.__x = value

    @property
    def y(self) -> float:
        return self.__y

    @y.setter
    def y(self, value: float) -> None:
        self.__y = value

    @property
    def forces(self) -> list:
        return self.__forces

    @forces.setter
    def forces(self, value: list) -> None:
        self.__forces = value
