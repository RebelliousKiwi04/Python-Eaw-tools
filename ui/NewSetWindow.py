from email.charset import QP
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import lxml.etree as et, os

from gameObject.campaign import Campaign


class CreateNewGCWindow:
    def __init__(self, repository):
        self.repository = repository
        self.dialogWindow = QDialog()
        self.layout = QVBoxLayout()

        self.dialogWindow.setWindowTitle("Create New GC Set")
        self.label = QLabel("Create New GC Set")

        self.setnamelayout = QHBoxLayout()
        self.setname = QLineEdit()
        self.setnamelabel = QLabel("Set Name: ")

        self.setnamelayout.addWidget(self.setnamelabel)
        self.setnamelayout.addWidget(self.setname)

        self.initialfactionlayout = QHBoxLayout()
        self.factionLabel = QLabel("Select A Playable Faction: ")
        self.faction = QComboBox()
        for i in self.repository.factions:
            self.faction.addItem(i.name)
        
        self.initialfactionlayout.addWidget(self.factionLabel)
        self.initialfactionlayout.addWidget(self.faction)

        self.filelayout = QHBoxLayout()
        self.fileLabel = QLabel("Set File Location: ")
        setlocation = 'newcampaignset.xml'

        self.location = QLabel(setlocation)
        self.changelocation = QPushButton("...")
        self.changelocation.clicked.connect(self.change_dir)
        self.filelayout.addWidget(self.fileLabel)
        self.filelayout.addWidget(self.location)
        self.filelayout.addWidget(self.changelocation)

        self.templateLayout = QHBoxLayout()
        self.templatelabel = QLabel("Template GC: ")
        self.template = QComboBox()
        for name, Campaign in self.repository.campaigns.items():
            self.template.addItem(name)
        
        self.templateLayout.addWidget(self.templatelabel)
        self.templateLayout.addWidget(self.template)

        self.buttonLayout = QHBoxLayout()
        self.cancelButton = QPushButton("Cancel")
        self.okButton = QPushButton("Create Set")
        self.buttonLayout.addWidget(self.cancelButton)
        self.buttonLayout.addWidget(self.okButton)

        self.layout.addWidget(self.label)
        self.layout.addLayout(self.setnamelayout)
        self.layout.addLayout(self.initialfactionlayout)
        self.layout.addLayout(self.filelayout)
        self.layout.addLayout(self.templateLayout)
        self.layout.addLayout(self.buttonLayout)

        self.dialogWindow.setLayout(self.layout)

        self.cancelButton.clicked.connect(self.dialogWindow.reject)
        self.okButton.clicked.connect(self.dialogWindow.accept)

        """
        Design For New GC Creation

        Input Set Name,  choose GC to copy as template

        if window is accepted, then copy template into new class, add to campaigns table in repository, add new GC set class to repository
        Create New File for set at start, automatically add to campaignfiles.xml
        
        """
    def change_dir(self):
        fileName = QFileDialog.getSaveFileName(None, "Select Plot File",
                                       self.repository.mod_dir+'\\xml',
                                       "*.xml")
        directory = fileName[0].split('/XML/')
        if len(directory) <2:
            directory = fileName[0].split('/xml/')
        if len(directory) <2:
            return
        self.location.setText(directory[1])
        