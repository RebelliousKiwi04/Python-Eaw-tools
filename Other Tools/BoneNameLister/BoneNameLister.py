from PyQt5.QtWidgets import QApplication,QFileDialog,QMessageBox
import os, sys, struct

app = QApplication(sys.argv)

test = QFileDialog.getOpenFileName()
filePath = test[0]
while not filePath.endswith(('.alo', '.ALO')):
    msg = QMessageBox()
    msg.setWindowTitle('Error!')
    msg.setText('Please Select an ALO file!')
    msg.exec_()
    directory = str(QFileDialog.getOpenFileName())

file = open(filePath,'rb')


def get_bone_names():

    bone_names = []

    file.seek(4, 1)  # skip size
    file.seek(8,1) #skip header and size
    bone_count = struct.unpack("<I", file.read(4))[0]
    file.seek(124,1) #skip padding

    counter = 0
    while (counter < bone_count):
        process_bone(bone_names)
        counter += 1

    return bone_names

def process_bone(bone_names):
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

    file.seek(8, 1)  #skip header and size
    parentIndex = struct.unpack('<I', file.read(4))[0]
    visible = struct.unpack('<I', file.read(4))[0]
    billboard = struct.unpack('<I', file.read(4))[0]
    matrix1_1 = struct.unpack('<f', file.read(4))[0]
    matrix1_2 = struct.unpack('<f', file.read(4))[0]
    matrix1_3 = struct.unpack('<f', file.read(4))[0]
    matrix1_4 = struct.unpack('<f', file.read(4))[0]
    matrix2_1 = struct.unpack('<f', file.read(4))[0]
    matrix2_2 = struct.unpack('<f', file.read(4))[0]
    matrix2_3 = struct.unpack('<f', file.read(4))[0]
    matrix2_4 = struct.unpack('<f', file.read(4))[0]
    matrix3_1 = struct.unpack('<f', file.read(4))[0]
    matrix3_2 = struct.unpack('<f', file.read(4))[0]
    matrix3_3 = struct.unpack('<f', file.read(4))[0]
    matrix3_4 = struct.unpack('<f', file.read(4))[0]


#loop over file until end is reached
while(file.tell() < os.path.getsize(filePath)):
    active_chunk = file.read(4)
    #print(active_chunk)
    if active_chunk == b"\x00\x02\x00\00":
        bone_names = get_bone_names()
        writeFile = open('outputfile.txt', 'w')
        for i in bone_names:
            writeFile.write(f'{i}\n')
        writeFile.close()
        break
file.close()
sys.exit()