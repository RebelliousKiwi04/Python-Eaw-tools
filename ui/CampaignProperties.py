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
    def __init__(self, campaignset, campaign, repository):
        self.dialogWindow = QDialog()
        self.dialogWindow.setWindowTitle("Campaign Properties")
        self.layout = QVBoxLayout()
        self.dialogWindow.setLayout(self.layout)

        ## SORT ORDER
        self.sortorderlayout = QHBoxLayout()
        self.sortlabel = QLabel("Sort Order: ")
        self.sortorder = QSpinBox()
        self.sortorder.setMinimum(1)
        self.sortorder.setMaximum(20)
        self.sortorderlayout.addWidget(self.sortlabel)
        self.sortorderlayout.addWidget(self.sortorder)
        
        self.layout.addLayout(self.sortorderlayout)

        ## IN GAME NAME
        self.campaignnamelayout = QHBoxLayout()
        self.campaignnamelabel = QLabel("Campaign Name (In Game): ")
        self.campaignname = QLineEdit()
        self.campaignnamelayout.addWidget(self.campaignnamelabel)
        self.campaignnamelayout.addWidget(self.campaignname)

        self.layout.addLayout(self.campaignnamelayout)

        ## IN GAME DESCRIPTION
        self.campaigndesclayout = QHBoxLayout()
        self.campaigndesclabel = QLabel("Campaign Description (In Game): ")
        self.campaigndesc = QLineEdit()
        self.campaigndesclayout.addWidget(self.campaigndesclabel)
        self.campaigndesclayout.addWidget(self.campaigndesc)

        self.layout.addLayout(self.campaigndesclayout)

        #Story Plots
        self.storyplotlabel =  QLabel("Story Plots:")
        self.storyplots = QWidget()
        self.storyplots.setLayout(QVBoxLayout())    

        self.layout.addWidget(self.storyplotlabel)
        self.layout.addWidget(self.storyplots)


        self.addStoryPlots = QHBoxLayout()
        self.addStoryPlotLabel = QLabel("Add Story Plot: ")
        self.storyplotfaction =  QComboBox()
        self.addButton = QPushButton("Add")
        self.addStoryPlots.addWidget(self.addStoryPlotLabel)
        self.addStoryPlots.addWidget(self.storyplotfaction)
        self.addStoryPlots.addWidget(self.addButton)

        self.layout.addLayout(self.addStoryPlots)
        
        ###DATA PER FACTION
        self.perfactionlabel = QLabel("Faction Related Data")
        self.selectedfaction = QComboBox()
        for faction in campaignset.playableFactions.keys():
            self.selectedfaction.addItem(faction)

        self.layout.addWidget(self.perfactionlabel)
        self.layout.addWidget(self.selectedfaction)

        ## HOME LOCATIONS
        self.homelocationlayout = QHBoxLayout()
        self.homelocationlabel = QLabel("Home Location:")
        self.homelocation = QComboBox()
        for planet in campaign.planets:
            self.homelocation.addItem(planet.name)

        self.homelocationlayout.addWidget(self.homelocationlabel)
        self.homelocationlayout.addWidget(self.homelocation)

        self.layout.addLayout(self.homelocationlayout)


        #Starting Credits
        self.startingcreditslayout = QHBoxLayout()
        self.startingcreditslabel = QLabel("Starting Credits: ")
        self.startingcredits = QSpinBox()
        self.startingcredits.setMinimum(0)
        self.startingcredits.setMaximum(50000)
        self.startingcreditslayout.addWidget(self.startingcreditslabel)
        self.startingcreditslayout.addWidget(self.startingcredits)

        self.layout.addLayout(self.startingcreditslayout)

        #Starting Tech
        self.startingtechlayout = QHBoxLayout()
        self.startingtechlabel = QLabel("Starting Tech Level: ")
        self.startingtech = QSpinBox()
        self.startingtech.setMinimum(0)
        self.startingtech.setMaximum(5)
        self.startingtechlayout.addWidget(self.startingtechlabel)
        self.startingtechlayout.addWidget(self.startingtech)

        self.layout.addLayout(self.startingtechlayout)

        #Max Tech
        self.maxtechlayout = QHBoxLayout()
        self.maxtechlabel = QLabel("Max Tech Level: ")
        self.maxtech = QSpinBox()
        self.maxtech.setMinimum(0)
        self.maxtech.setMaximum(5)
        self.maxtechlayout.addWidget(self.maxtechlabel)
        self.maxtechlayout.addWidget(self.maxtech)

        self.layout.addLayout(self.maxtechlayout)

        #AI Controller
        self.aicontrollayout = QHBoxLayout()
        self.aicontrollabel = QLabel("AI Player Control: ")
        self.aicontroller = QComboBox()
        for i in repository.ai_players:
            self.aicontroller.addItem(i)

        self.aicontrollayout.addWidget(self.aicontrollabel)
        self.aicontrollayout.addWidget(self.aicontroller)

        self.layout.addLayout(self.aicontrollayout)


        
# app = QApplication(sys.argv)
# ui = CampaignPropertiesWindow(None, None, None)
# ui.dialogWindow.exec()
# sys.exit(app.exec_())