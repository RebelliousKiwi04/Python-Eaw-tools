from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys

class StoryPlotWidget(QWidget):
    def __init__(self, plot_owner, plot_location,repository):
        super().__init__()
        self.setLayout(QHBoxLayout())
        self.owner = plot_owner
        self.location = plot_location
        self.repository = repository
        self.label = QLabel(f'{plot_owner}, {plot_location}')

        self.modify = QPushButton("Modify")
        self.modify.setMaximumWidth(75)
        self.modify.clicked.connect(self.open_modify_window)
        self.layout().addWidget(self.label)
        self.layout().addWidget(self.modify)
    def open_modify_window(self):
        self.modifyWindow = QDialog()
        self.modifyWindow.setLayout(QVBoxLayout())
        self.ownerLayout = QHBoxLayout()
        self.ownerlabel = QLabel("Owner: ")
        self.ownercombobox = QComboBox()
        for i in self.repository.factions:
            self.ownercombobox.addItem(i.name)
        
        self.plotLayout = QHBoxLayout()
        self.locationlabel = QLabel(f"Plot File: {self.location}")
        self.changelocation = QPushButton("...")
        self.changelocation.clicked.connect(self.change_directory)
        self.ownerLayout.addWidget(self.ownerlabel)
        self.ownerLayout.addWidget(self.ownercombobox)
        self.plotLayout.addWidget(self.locationlabel)
        self.plotLayout.addWidget(self.changelocation)
        self.modifyWindow.layout().addLayout(self.ownerLayout)
        self.modifyWindow.layout().addLayout(self.plotLayout)

        self.buttons = QDialogButtonBox()
        self.buttons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Save)
        self.buttons.clicked.connect(self.modifyWindow.reject)
        self.buttons.clicked.connect(self.modify_plot)
        self.modifyWindow.layout().addWidget(self.buttons)
        self.modifyWindow.setWindowTitle("Modify Story Plot")
        
        self.modifyWindow.exec_()
    def change_directory(self):
        
        fileName = QFileDialog.getOpenFileName(self, "Select Plot File",
                                       self.repository.mod_dir+'\\xml',
                                       "*.xml")
        directory = fileName[0].split('/XML/')
        if len(directory) <2:
            directory = fileName[0].split('/xml/')
        self.locationlabel.setText(f"Plot File{directory}")
    def modify_plot(self):
        self.owner = self.ownercombobox.currentText()
        self.location = self.locationlabel.text().replace('Plot File: ','')
        self.modifyWindow.accept()
        self.label.setText(f'{self.owner}, {self.location}')

class CampaignPropertiesWindow:
    def __init__(self, campaignset, campaign, repository):
        self.dialogWindow = QDialog()
        self.dialogWindow.setWindowTitle(f"{campaign.name} Properties")
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
        self.sortorder.setValue(campaign.sort_order)


        self.layout.addLayout(self.sortorderlayout)

        ## IN GAME NAME
        self.campaignnamelayout = QHBoxLayout()
        self.campaignnamelabel = QLabel("Campaign Name (In Game): ")
        self.campaignname = QLineEdit()
        self.campaignnamelayout.addWidget(self.campaignnamelabel)
        self.campaignnamelayout.addWidget(self.campaignname)
        self.campaignname.setText(repository.text_dict[campaign.text_name])

        self.layout.addLayout(self.campaignnamelayout)

        ## IN GAME DESCRIPTION
        self.campaigndesclayout = QHBoxLayout()
        self.campaigndesclabel = QLabel("Campaign Description (In Game): ")
        self.campaigndesc = QLineEdit()
        self.campaigndesclayout.addWidget(self.campaigndesclabel)
        self.campaigndesclayout.addWidget(self.campaigndesc)
        self.campaigndesc.setText(repository.text_dict[campaign.desc_name])

        self.layout.addLayout(self.campaigndesclayout)

        #Story Plots
        self.storyplotlabel =  QLabel("Story Plots:")
        self.storyplots = QListWidget()
        self.storyplots.setLayout(QVBoxLayout())    

        for owner, plot in campaign.plots.items():
            itemN = QListWidgetItem()
            widget = StoryPlotWidget(owner,plot,repository)
            itemN.setSizeHint(widget.sizeHint())

            self.storyplots.addItem(itemN)
            self.storyplots.setItemWidget(itemN, widget)

        self.layout.addWidget(self.storyplotlabel)
        self.layout.addWidget(self.storyplots)


        self.addStoryPlots = QHBoxLayout()
        self.addStoryPlotLabel = QLabel("Add Story Plot: ")
        self.storyplotfaction =  QComboBox()

        for i in repository.factions:
            if i.name not in campaign.plots.keys():
                self.storyplotfaction.addItem(i.name)

        self.addButton = QPushButton("Add")
        self.addStoryPlots.addWidget(self.addStoryPlotLabel)
        self.addStoryPlots.addWidget(self.storyplotfaction)
        self.addStoryPlots.addWidget(self.addButton)

        self.layout.addLayout(self.addStoryPlots)
        
        ###DATA PER FACTION
        self.perfactionlabel = QLabel("Faction Related Data")
        self.selectedfaction = QComboBox()
        for faction in repository.factions:
            self.selectedfaction.addItem(faction.name)
        faction = self.selectedfaction.currentText()
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


        if faction not in campaign.home_locations.keys():
            campaign.home_locations[faction] = campaign.planets[0]
        self.homelocation.setCurrentText(campaign.home_locations[faction])
        

        self.layout.addLayout(self.homelocationlayout)


        #Starting Credits
        self.startingcreditslayout = QHBoxLayout()
        self.startingcreditslabel = QLabel("Starting Credits: ")
        self.startingcredits = QSpinBox()
        self.startingcredits.setMinimum(0)
        self.startingcredits.setMaximum(50000)
        self.startingcreditslayout.addWidget(self.startingcreditslabel)
        self.startingcreditslayout.addWidget(self.startingcredits)

        if faction not in campaign.starting_credits.keys():
            campaign.home_locations[faction] = 0
        self.startingcredits.setValue(campaign.starting_credits[faction])

        
        self.layout.addLayout(self.startingcreditslayout)

        #Starting Tech
        self.startingtechlayout = QHBoxLayout()
        self.startingtechlabel = QLabel("Starting Tech Level: ")
        self.startingtech = QSpinBox()
        self.startingtech.setMinimum(0)
        self.startingtech.setMaximum(5)
        self.startingtechlayout.addWidget(self.startingtechlabel)
        self.startingtechlayout.addWidget(self.startingtech)

        if faction not in campaign.starting_tech.keys():
            campaign.starting_tech[faction] = 1
        self.startingtech.setValue(campaign.starting_tech[faction])


        self.layout.addLayout(self.startingtechlayout)

        #Max Tech
        self.maxtechlayout = QHBoxLayout()
        self.maxtechlabel = QLabel("Max Tech Level: ")
        self.maxtech = QSpinBox()
        self.maxtech.setMinimum(0)
        self.maxtech.setMaximum(5)
        self.maxtechlayout.addWidget(self.maxtechlabel)
        self.maxtechlayout.addWidget(self.maxtech)

        if faction not in campaign.max_tech_level.keys():
            campaign.max_tech_level[faction] = 1
        self.maxtech.setValue(campaign.max_tech_level[faction])

        self.layout.addLayout(self.maxtechlayout)

        #AI Controller
        self.aicontrollayout = QHBoxLayout()
        self.aicontrollabel = QLabel("AI Player Control: ")
        self.aicontroller = QComboBox()
        for i in repository.ai_players:
            self.aicontroller.addItem(i)

        self.aicontrollayout.addWidget(self.aicontrollabel)
        self.aicontrollayout.addWidget(self.aicontroller)
        if faction not in campaign.ai_players.keys():
            campaign.ai_players[faction] = repository.ai_players[0]
        self.aicontroller.setCurrentText(campaign.ai_players[faction])

        self.layout.addLayout(self.aicontrollayout)
