from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys,copy

def getListItems(listwidget):
    items = []
    for index in range(listwidget.count()):
        items.append(listwidget.item(index))
    return items


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
        self.repository.logfile.write(f"Opening Modify Window For Plot {self.location}\n")
        self.repository.logfile.flush()
        self.modifyWindow = QDialog()
        self.modifyWindow.setWindowIcon(QIcon('eawIcon.png'))
        self.modifyWindow.setLayout(QVBoxLayout())

        self.repository.logfile.write(f"Adding Factions To Owner Combobox for Plot {self.location}\n")
        self.repository.logfile.flush()
        self.ownerLayout = QHBoxLayout()
        self.ownerlabel = QLabel("Owner: ")
        self.ownercombobox = QComboBox()
        for i in self.repository.factions:
            self.ownercombobox.addItem(i.name)
        

        self.repository.logfile.write(f"Adding Location Label For Plot {self.location}\n")
        self.repository.logfile.flush()
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
        self.repository.logfile.write(f"Changing Directory For Plot {self.location}\n")
        self.repository.logfile.flush()
        fileName = QFileDialog.getOpenFileName(self, "Select Plot File",
                                       self.repository.mod_dir+'\\xml',
                                       "*.xml")
        self.repository.logfile.write(f"New Plot File Selected {fileName[0]}\n")
        self.repository.logfile.flush()
        directory = fileName[0].split('/XML/')
        if len(directory) <2:
            directory = fileName[0].split('/xml/')
        self.locationlabel.setText(f"Plot File{directory[1]}")
    def modify_plot(self):
        self.repository.logfile.write(f"Saving Plot File Modifications")
        self.repository.logfile.flush()
        self.owner = self.ownercombobox.currentText()
        self.location = self.locationlabel.text().replace('Plot File: ','')
        self.modifyWindow.accept()
        self.label.setText(f'{self.owner}, {self.location}')

class CampaignPropertiesWindow:
    def __init__(self, campaignset, campaign, repository):
        self.repository =repository
        self.campaign = campaign

        self.dialogWindow = QDialog()
        self.dialogWindow.setWindowIcon(QIcon('eawIcon.png'))
        self.dialogWindow.setMinimumWidth(500)

        self.repository.logfile.write(f"Collecting Campaign Name\n")
        self.repository.logfile.flush()
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

        self.repository.logfile.write(f"Collecting Sort Order For Campaign {campaign.name}\n")
        self.repository.logfile.flush()

        self.sortorder.setValue(campaign.sort_order)


        self.layout.addLayout(self.sortorderlayout)

        ## IN GAME NAME
        self.campaignnamelayout = QHBoxLayout()
        self.campaignnamelabel = QLabel("Campaign Name (In Game): ")
        self.campaignname = QLineEdit()
        self.campaignnamelayout.addWidget(self.campaignnamelabel)
        self.campaignnamelayout.addWidget(self.campaignname)

        self.repository.logfile.write(f"Collecting Text ID For Campaign {campaign.name}\n")
        self.repository.logfile.flush()

        self.campaignname.setText(repository.text_dict[campaign.text_name])

        self.layout.addLayout(self.campaignnamelayout)

        ## IN GAME DESCRIPTION
        self.campaigndesclayout = QHBoxLayout()
        self.campaigndesclabel = QLabel("Campaign Description (In Game): ")
        self.campaigndesc = QLineEdit()
        self.campaigndesclayout.addWidget(self.campaigndesclabel)
        self.campaigndesclayout.addWidget(self.campaigndesc)

        self.repository.logfile.write(f"Collecting Description ID For Campaign {campaign.name}\n")
        self.repository.logfile.flush() 

        self.campaigndesc.setText(repository.text_dict[campaign.desc_name])

        self.layout.addLayout(self.campaigndesclayout)

        #Story Plots
        self.storyplotlabel =  QLabel("Story Plots:")
        self.storyplots = QListWidget()
        self.storyplots.setLayout(QVBoxLayout())    

        self.repository.logfile.write(f"Adding Story Plots To UI for {campaign.name}\n")
        self.repository.logfile.flush() 
        for owner, plot in campaign.plots.items():
            itemN = QListWidgetItem()
            self.repository.logfile.write(f"Adding Plot {plot} for {owner} for campaign {campaign.name}\n")
            self.repository.logfile.flush() 
            widget = StoryPlotWidget(owner,plot,repository)
            itemN.setSizeHint(widget.sizeHint())

            self.storyplots.addItem(itemN)
            self.storyplots.setItemWidget(itemN, widget)

        self.layout.addWidget(self.storyplotlabel)
        self.layout.addWidget(self.storyplots)

        #DELETE PLOT


        self.deletestoryplots = QPushButton("Delete Selected Plot")
        self.deletestoryplots.clicked.connect(self.delete_story_plot)
        self.layout.addWidget(self.deletestoryplots)


        # ADD PLOT

        self.addStoryPlots = QHBoxLayout()
        self.addStoryPlotLabel = QLabel("Add Story Plot: ")
        self.storyplotfaction =  QComboBox()

        self.repository.logfile.write(f"Adding Other Factions For Add Plot Combobox\n")
        self.repository.logfile.flush() 

        for i in repository.factions:
            if i.name not in campaign.plots.keys():
                self.storyplotfaction.addItem(i.name)

        self.addButton = QPushButton("Add")
        self.addButton.clicked.connect(self.add_story_plot)

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

        self.repository.logfile.write(f"Adding Planets To Home Location Combobox\n")
        self.repository.logfile.flush() 

        for planet in campaign.planets:
            self.homelocation.addItem(planet.name)

        self.homelocationlayout.addWidget(self.homelocationlabel)
        self.homelocationlayout.addWidget(self.homelocation)



        if faction not in campaign.home_locations.keys():
            repository.logfile.write(f'No Home Location Detected For {faction} attempting to set home location to planet from GC\n')
            repository.logfile.flush()
            campaign.home_locations[faction] = campaign.planets[0].name

 
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
            self.repository.logfile.write(f"No Starting Credits tag found for faction {faction} attempting to set starting credits for faction to 0\n")
            self.repository.logfile.flush() 
            campaign.starting_credits[faction] = 0
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
            self.repository.logfile.write(f"No Starting Tech tag found for faction {faction} attempting to set starting tech for faction to 0\n")
            self.repository.logfile.flush() 
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
            self.repository.logfile.write(f"No Max Tech tag found for faction {faction} attempting to set max tech for faction to 0\n")
            self.repository.logfile.flush() 
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
            self.repository.logfile.write(f"No AI Player Control tag found for faction {faction} attempting to set ai control to first in list\n")
            self.repository.logfile.flush() 
            campaign.ai_players[faction] = repository.ai_players[0]
        self.aicontroller.setCurrentText(campaign.ai_players[faction])

        self.layout.addLayout(self.aicontrollayout)
        self.activeFaction = self.selectedfaction.currentText()
        self.buttonLayout = QHBoxLayout()
        self.cancelButton = QPushButton("Cancel")
        self.SaveButton = QPushButton("Save")

        self.buttonLayout.addWidget(self.cancelButton)
        self.buttonLayout.addWidget(self.SaveButton)

        self.cancelButton.clicked.connect(self.dialogWindow.reject)
        self.SaveButton.clicked.connect(self.save_changes)
        self.selectedfaction.currentIndexChanged.connect(self.change_active_faction)
        self.layout.addLayout(self.buttonLayout)
    def change_active_faction(self):
        self.repository.logfile.write(f"Changing Selected Faction In Campaign Properties Window\n")
        self.repository.logfile.flush() 
        activeFaction = self.activeFaction
        self.campaign.home_locations[activeFaction] = self.homelocation.currentText()
        self.campaign.starting_credits[activeFaction] = self.startingcredits.value()
        self.campaign.starting_tech[activeFaction] = self.startingtech.value()
        self.campaign.max_tech_level[activeFaction] = self.maxtech.value()
        self.campaign.ai_players[activeFaction] = self.aicontroller.currentText()

        self.activeFaction = self.selectedfaction.currentText()
        faction = self.activeFaction
        print(self.campaign.home_locations)
        if faction not in self.campaign.ai_players.keys():
            self.campaign.ai_players[faction] = self.repository.ai_players[0]
        if faction not in self.campaign.max_tech_level.keys():
            self.campaign.max_tech_level[faction] = 1
        if faction not in self.campaign.starting_tech.keys():
            self.campaign.starting_tech[faction] = 1
        if faction not in self.campaign.starting_credits.keys():
            self.campaign.starting_credits[faction] = 0

        if faction not in self.campaign.home_locations.keys():
            self.campaign.home_locations[faction] = str(self.campaign.planets[0].name)

        self.homelocation.setCurrentText(self.campaign.home_locations[faction])
        self.startingcredits.setValue(int(self.campaign.starting_credits[faction]))
        self.startingtech.setValue(int(self.campaign.starting_tech[faction]))
        self.maxtech.setValue(int(self.campaign.max_tech_level[faction]))
        self.aicontroller.setCurrentText(self.campaign.ai_players[faction])
    def save_changes(self):
        self.repository.logfile.write(f"Saving Changes Made In Campaign Properties Window\n")
        self.repository.logfile.flush()
        self.campaign.plots = {}
        for item in getListItems(self.storyplots):
            widget = self.storyplots.itemWidget(item)
            owner = widget.owner
            plot = widget.location
            self.campaign.plots[owner] = plot
        self.campaign.sort_order = self.sortorder.value()
        self.repository.text_dict[self.campaign.text_name] = self.campaignname.text()
        self.repository.text_dict[self.campaign.desc_name] = self.campaigndesc.text()

        activeFaction = self.activeFaction
        self.campaign.home_locations[activeFaction] = self.homelocation.currentText()
        self.campaign.starting_credits[activeFaction] = self.startingcredits.value()
        self.campaign.starting_tech[activeFaction] = self.startingtech.value()
        self.campaign.max_tech_level[activeFaction] = self.maxtech.value()
        self.campaign.ai_players[activeFaction] = self.aicontroller.currentText()

        self.dialogWindow.accept()
    def delete_story_plot(self):
        self.repository.logfile.write(f"Deleting Story Plot\n")
        self.repository.logfile.flush()
        row = self.storyplots.currentRow()
        if row == -1:
            return
        self.storyplots.takeItem(row)
    def add_story_plot(self):
        self.repository.logfile.write(f"Adding Story Plot\n")
        self.repository.logfile.flush()
        fileName = QFileDialog.getOpenFileName(None, "Select Plot File",
                                       self.repository.mod_dir+'\\xml',
                                       "*.xml")
        directory = fileName[0].split('/XML/')
        if len(directory) <2:
            directory = fileName[0].split('/xml/')
        if len(directory) <2:
            return


        itemN = QListWidgetItem()
        widget = StoryPlotWidget(self.storyplotfaction.currentText(),directory[1],self.repository)
        itemN.setSizeHint(widget.sizeHint())

        self.storyplots.addItem(itemN)
        self.storyplots.setItemWidget(itemN, widget)

        self.storyplotfaction.removeItem(self.storyplotfaction.currentIndex())