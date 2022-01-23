import math, os, struct, sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *



def process_bone(bone_names,file):
    file.seek(12, 1)  #skip header and size and next header
    length = struct.unpack("I", file.read(4))  # get string length
    string = ""
    counter = 0
    while counter < length[0] - 1:
        letter = str(file.read(1))
        letter = letter[2:len(letter) - 1]
        string = string + letter
        counter += 1
    
    file.seek(1, 1)
    if(len(string)> 63):
        name = string
    else:
        name = string

    bone_names.append(name)

def get_bone_names(file):

    bone_names = []

    file.seek(4, 1)  # skip size
    file.seek(8,1) #skip header and size
    bone_count = struct.unpack("<I", file.read(4))[0]
    file.seek(124,1) #skip padding

    counter = 0
    while (counter < bone_count):
        process_bone(bone_names,file)
        counter += 1

    return bone_names

def get_bones(model_path):
    file = open(model_path,'rb')
        #loop over file until end is reached
    while(file.tell() < os.path.getsize(model_path)):
        active_chunk = file.read(4)
        #print(active_chunk)
        if active_chunk == b"\x00\x02\x00\00":
            bone_names = get_bone_names(file)
            for i in bone_names:
                print(i)
    file.close()

class UserInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setLayout(QVBoxLayout())


class HardpointGenerator:
    def __init__(self):
        self.app = QApplication(sys.argv)



hardpointgen = HardpointGenerator()
sys.exit(hardpointgen.app.exec_())