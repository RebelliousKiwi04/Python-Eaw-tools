import math

class Faction:
    def __init__(self, xml_entry, file):
        self.entry = xml_entry
        self.fileLocation = file
        self.name = self.get_name()
        self.playable = self.is_playable()
        self.variant = self.set_variant()
        self.color = self.get_color()
        self.type = self.entry.tag
    def get_color(self)->list:
        for item in self.entry:
            if item.tag == 'Color':
                if item.text != None:
                    entry = item.text     
                    entry = entry.replace(',',' ')
                    entry = entry.split()
                    color = [float(entry[0])/255, float(entry[1])/255, float(entry[2])/255, float(entry[3])/255]
                    return color
    def is_playable(self) -> int:
        for item in self.entry:
            if item.tag == 'Is_Playable':
                if item.text != None:
                    return bool(item.text)
        return 0
    def get_name(self) -> str:
        return self.entry.get('Name')
    def set_variant(self):
        for item in self.entry:
            if item.tag == 'Variant_Of_Existing_Type':
                return item.text
        return None
    