import os, sys, lxml.etree as et, pickle, shutil

def serialize(gameObjectRepo):
    '''some pickle stuff'''

class ModBuildier:
    def __init__(self) -> None:
        pass
    def createMod(self):
        pass
    def buildMod(self):
        pass


class ModRepository:
    def __init__(self, mod_directory):
        self.dir = mod_directory
        os.chdir(self.dir)
        self.planets = {}
        self.units = {}
        self.campaigns = {}
        self.tradeRoutes = {}