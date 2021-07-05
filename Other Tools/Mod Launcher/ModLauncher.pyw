from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from bs4 import BeautifulSoup
import os, requests, sys, subprocess
from winreg import *


class ImageLabel(QLabel):
    def __init__(self, image_dir):
        super().__init__()
        pixmap = QPixmap(image_dir)
        pixmap = pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.setPixmap(pixmap)


class ModItem():
    def __init__(self, name,mod_dir, image='exeIcon.jpg', mod_id=None):
        self.directory = mod_dir
        self.layout = QVBoxLayout()
        self.nameLayout = QHBoxLayout()
        font = QFont()
        font.setPointSize(10)
        self.nameLayout.addWidget(ImageLabel(image))
        self.modButton = QLabel(name)
        self.modButton.setFont(font)
        self.nameLayout.addWidget(self.modButton)
        self.name = name
        self.dataLayout = QHBoxLayout()
        self.runButton = QPushButton("Run Mod")
        self.configureButton = QPushButton("Configure Mod")
        self.dataLayout.addWidget(self.runButton)
        self.dataLayout.addWidget(self.configureButton)
        self.layout.addLayout(self.nameLayout)
        self.layout.addLayout(self.dataLayout)
        if mod_id == None:
            mod_id == name
        self.data_dict = {
            ['DEBUG']: False,
            ['ARGUMENTS']: '',
            ['PARENT_MOD']: None,
        }
    def toggle_debug(self):
        if self.data_dict['DEBUG'] == True:
            self.data_dict['DEBUG'] = False
            currentlabelText = self.modButton.text()
            currentlabelText = currentlabelText + ' (DEBUG)'
            self.modButton.setText(currentlabelText)
        else:
            self.data_dict['DEBUG'] = True
            self.modButton.setText(self.name)
    def make_submod(self, main_mod_name):
        self.data_dict['PARENT_MOD'] = main_mod_name

class ModLauncherWindow:
    def __init__(self):
        self.app = QApplication(sys.argv)  
        self.mainWindow = QMainWindow()
        self.exeImageLocation = os.getcwd()+'\\exeIcon.jpg'
        font = QFont()
        font.setPointSize(10)
        scrollARea = QScrollArea()
        widget = QWidget()
        self.layout = QVBoxLayout(widget)
        self.layout.setAlignment(Qt.AlignTop)
        scrollARea.setWidget(widget)
        scrollARea.setWidgetResizable(True)
        scrollARea.setHorizontalScrollBarPolicy( Qt.ScrollBarAlwaysOff )
        self.mainWindow.setCentralWidget(scrollARea)

        self.mainWindow.setWindowTitle("EaW Mod Launcher")
        self.__menuBar: QMenuBar = QMenuBar()
        self.__fileMenu: QMenu = QMenu("File", self.mainWindow)
        self.__menuBar.addMenu(self.__fileMenu)
        self.mainWindow.setMenuWidget(self.__menuBar)

        self.__quitAction: QAction = QAction("Quit", self.mainWindow)
        self.__quitAction.triggered.connect(sys.exit)
        self.__fileMenu.addAction(self.__quitAction)
        self.createShortcutAction = QAction("Create Shortcut", self.mainWindow)
        self.__menuBar.addAction(self.createShortcutAction)
        self.locate_eaw_installation()
        self.eaw_exe = self.install_location + '\\GameData\\StarWarsG.exe'
        self.foc_exe = self.install_location + '\\corruption\\StarWarsG.exe'
        os.chdir(self.install_location)

        self.mods = self.grab_all_mods()
        for mod in self.mods:
            self.layout.addLayout(mod.layout)
        os.chdir(self.install_location)
        
        #self.mainWindow.setWindowFlags(Qt.WindowCloseButtonHint | )
        self.mainWindow.setFixedSize(650, 650)
        self.mainWindow.show()

        sys.exit(self.app.exec_())
    def locate_eaw_installation(self):
        aReg = ConnectRegistry(None,HKEY_LOCAL_MACHINE)
        aKey = OpenKey(aReg, r"SOFTWARE\WOW6432Node\LucasArts\Star Wars Empire at War Forces of Corruption\1.0")
        val=QueryValueEx(aKey, "InstallPath")[0]
        self.install_location= val
    def grab_all_mods(self):
        localMods = os.listdir(self.install_location+'\\corruption\\Mods')
        modItems = self.grab_steam_mods()
        for modpath in localMods:
            items = os.listdir(self.install_location+'\\corruption\\Mods\\'+modpath)
            modImage = self.exeImageLocation
            for i in items:
                if '.ico' in i:
                    modImage = self.install_location+'\\corruption\\Mods\\'+modpath+'\\'+i
            modItems.append(ModItem(modpath,self.install_location+'\\corruption\\Mods\\'+modpath, modImage))
        
        return modItems
    def get_steam_mod_name(self, mod_id):
        try:
            req = requests.get("https://steamcommunity.com/sharedfiles/filedetails/?id="+mod_id)
            soup = BeautifulSoup(req.text, 'lxml')
            val = soup.find('div', {'class':"workshopItemTitle"}).get_text()
            return val
        except Exception as e:
            print(e)
            return mod_id
    def grab_steam_mods(self):
        steam_dir = self.install_location.replace('common\Star Wars Empire at War', '')
        self.workshop_dir = steam_dir + 'workshop\\content\\32470'
        os.chdir(self.workshop_dir)
        mods = []
        for mod in os.listdir(self.workshop_dir):
            fullPath = os.path.abspath(mod)
            items = os.listdir(self.workshop_dir+'\\'+mod)
            name = self.get_steam_mod_name(mod)
            modImage = self.exeImageLocation
            for i in items:
                if '.ico' in i:
                    modImage = fullPath+'\\'+i
            mods.append(ModItem(name, fullPath, modImage))
        return mods
ModLauncherWindow()
        