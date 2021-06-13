import math, os, struct

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


class Unit:
    def __init__(self, xml_entry, file, modpath):
        self.entry = xml_entry
        self.fileLocation = file
        self.modpath = modpath
        self.aicp = self.get_aicp()
        self.model_path = self.get_model_path()
        self.bones = None
        self.name = self.get_name()
        self.category_masks = self.get_category_masks()
        self.variant = self.set_variant()
        self.type = self.entry.tag
        # if self.model_path != None:
        #     if os.path.isfile(self.model_path):
        #         self.bones = self.get_bone_names()
    def get_aicp(self) -> int:
        for item in self.entry:
            if item.tag == 'AI_Combat_Power':
                if item.text != None:
                    return int(math.floor(float(item.text)))
        return 0
    def get_name(self) -> str:
        return self.entry.get('Name')
    def get_category_masks(self):
        for item in self.entry:
            if item.tag == 'CategoryMask':
                outputList = [] 
                if item.text != None:
                    for text in item.text.split():
                        newText = text.replace('|','')
                        if len(newText) > 3:
                            outputList.append(newText)
                    return outputList
    def set_variant(self):
        for item in self.entry:
            if item.tag == 'Variant_Of_Existing_Type':
                return item.text
        return None
    def get_model_path(self):
        for item in self.entry:
            if item.tag == 'Space_Model_Name':
                return os.path.abspath(self.modpath + """/Art/Models/""" + item.text)
            if item.tag == 'Land_Model_Name':
                return os.path.abspath(self.modpath + """/Art/Models/""" + item.text)
        return None
    def get_bone_names(self):
        file = open(self.model_path,'rb')
            #loop over file until end is reached
        while(file.tell() < os.path.getsize(self.model_path)):
            active_chunk = file.read(4)
            #print(active_chunk)
            if active_chunk == b"\x00\x02\x00\00":
                bone_names = get_bone_names(file)
                for i in bone_names:
                    print(i)
        file.close()
    