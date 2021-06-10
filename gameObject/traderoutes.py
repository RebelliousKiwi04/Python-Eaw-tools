import lxml.etree as et

class TradeRoute:
    def __init__(self, xml_entry, fileLocation):
        self.fileLocation = fileLocation
        self.entry = xml_entry
        self.name = self.get_name()
        self.point_A, self.point_B = self.get_points()
        self.points = []
    def set_point_planets(self, planetList):
        self.points.append(planetList[([x.name.lower() for x in planetList].index(self.point_A))])
        self.points.append(planetList[([x.name.lower() for x in planetList].index(self.point_B))])

    def get_name(self) -> str:
        return self.entry.get('Name')
    def get_points(self) -> str:
        point_a = ''
        point_b = ''
        for child in self.entry:
            if child.tag == 'Point_A':
                point_a = child.text
            if child.tag == 'Point_B':
                point_b = child.text
        return point_a.lower(), point_b.lower()