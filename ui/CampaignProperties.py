from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys

class FactionHomeLocation(QWidget):
    def __init__(self, factionName, campaign):
        super().__init__()
        self.setLayout(QHBoxLayout())
        self.label = QLabel(factionName)
        self.homeplanet = QComboBox()
        self.layout().addWidget(self.label)
        self.layout().addWidget(self.homeplanet)



class CampaignPropertiesWindow:
    def __init__(self, campaignset, campaign, gameobjectrepository):
        self.dialogWindow = QDialog()
        self.layout = QVBoxLayout()

        ## SORT ORDER
        self.sortorderlayout = QHBoxLayout()
        self.sortlabel = QLabel("Sort Order: ")
        self.sortorder = QSpinBox()
        self.sortorder.setMinimum(1)
        self.sortorder.setMaximum(20)
        self.sortorderlayout.addWidget(self.sortlabel)
        self.sortorderlayout.addWidget(self.sortorder)

        ## IN GAME NAME
        self.campaignnamelayout = QHBoxLayout()
        self.campaignnamelabel = QLabel("Campaign Name (In Game): ")
        self.campaignname = QLineEdit()
        self.campaignnamelayout.addWidget(self.campaignnamelabel)
        self.campaignnamelayout.addWidget(self.campaignname)

        ## IN GAME DESCRIPTION
        self.campaigndesclayout = QHBoxLayout()
        self.campaigndesclabel = QLabel("Campaign Description (In Game): ")
        self.campaigndesc = QLineEdit()
        self.campaigndesclayout.addWidget(self.campaigndesclabel)
        self.campaigndesclayout.addWidget(self.campaigndesc)


        


        ## HOME LOCATIONS
        self.homelocationslayout = QVBoxLayout()
        self.homelocationslayout.addWidget(FactionHomeLocation('test', []))
        self.factionhomelayouts = []



        
app = QApplication(sys.argv)
ui = CampaignPropertiesWindow(None, None, None)
ui.dialogWindow.exec()
sys.exit(app.exec_())