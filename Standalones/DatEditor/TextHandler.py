import os
from PyQt5.QtWidgets import QFileDialog
os.environ["PYTHONIOENCODING"] = "utf-16-le" 

def tobytesLE(value):
    corenne = bytearray(range(4))
    corenne[0] = int(str(value & 0xff).encode('utf-8'));
    corenne[1] = int(str(((value & 0xff00) >> 8)).encode('utf-8'))
    corenne[2] = int(str(((value & 0xff0000) >> 16)).encode('utf-8'))
    corenne[3] = int(str(((value & 0xff000000) >> 24)).encode('utf-8'))

    return corenne

def make32(source, startindex):
    corenne = source[startindex]
    corenne += source[startindex + 1] << 8
    corenne += source[startindex + 2] << 16
    corenne += source[startindex + 3] << 24
    return corenne

def readentry(source, startindex, length) -> str:
    entrybytes = bytearray(length*2)
    for i in range((2*length)):
        entrybytes[i] = source[startindex+i]
    return entrybytes.decode('utf-16-le',errors='strict')

def readid(source, startindex, length):
    entrybytes = bytearray(length)
    for i in range(length):
        entrybytes[i] = source[startindex+i]
    #return entrybytes.decode('windows-1252')
    return entrybytes.decode('cp1252', errors='ignore')

def createKeyPair(valueList):
    returnList = list(range(valueList))
    for i in range(valueList):
        returnList[i] = Key_Pair(i)
    return returnList

class crcGlobals:
    def __init__(self):
        self.crcTable = list(range(256))
        for i in range(256):
            crc = i
            for j in range(8):
                if ((crc &1)==1):
                    crc = (crc >> 1) ^ 0xEDB88320
                else:
                    crc = (crc >> 1)
            self.crcTable[i] = crc & 0xFFFFFFFF;
crcGlobals = crcGlobals()

class Key_Pair:
    def __init__(self, index):
        self.entry = None
        self.identifier = None
        self.index = index

class Text_Entry:
    def __init__(self, table):
        self.identifier = table[0]
        self.entry = table[1]
        win1252Bytes = self.identifier.encode('cp1252')
        check = 0xFFFFFFFF
        for j in range(len(win1252Bytes)):
            check = ((check >> 8) & 0x00FFFFFF) ^ crcGlobals.crcTable[(check ^ win1252Bytes[j]) & 0xFF]
        check ^= 0xFFFFFFFF
        self.crc = check

class DictTextEntry:
    def __init__(self, identifier,entry):
        self.identifier = identifier
        self.entry = entry
        win1252Bytes = self.identifier.encode('cp1252')
        check = 0xFFFFFFFF
        for j in range(len(win1252Bytes)):
            check = ((check >> 8) & 0x00FFFFFF) ^ crcGlobals.crcTable[(check ^ win1252Bytes[j]) & 0xFF]
        check ^= 0xFFFFFFFF
        self.crc = check

class TextFile:
    def __init__(self,file):
        self.decompile_target = 'dict'
        self.file = file
    def decompileDat(self):
        #Open The Dat File in binary mode
        f = open(self.file, 'rb')
        datfile = f.read()

        total_entries = make32(datfile, 0)
        index: int = 4

        textlength = list(range(total_entries))
        idlength = list(range(total_entries))


        entries = createKeyPair(total_entries)


        for i in range(total_entries):
            index += 4
            textlength[i] = make32(datfile, index)

            index += 4
            idlength[i] = make32(datfile, index)
            index+=4

        for i in range(total_entries):
            entries[i].entry = str(readentry(datfile, index, textlength[i]))
            index += 2*textlength[i]

        for i in range(total_entries):
            entries[i].identifier = readid(datfile, index, idlength[i])
            index += idlength[i]

        if self.decompile_target == 'file':
            file = open('MasterTextFile_ENGLISH.txt', 'w', encoding='utf-8')
            for value in entries:
                file.write(value.identifier + ";" 
                + str(value.entry) +"\n")
            file.close()
            return True
        else:
            returnDict = {}
            for i in entries:
                returnDict[i.identifier] = i.entry
            return returnDict
    def compileDat(self, source, save_as=False):
        total_entries = 0
        entries = []
        if type(source) is dict:
            for identifier, entry in source.items():
                entries.append(DictTextEntry(identifier,entry))
                total_entries+=1

 
        datfile = bytearray()

        localBytes = tobytesLE(total_entries)
        for i in range(4):
            datfile.append(localBytes[i])

        for i in range(total_entries):
            crcBytes = tobytesLE(entries[i].crc)
            for j in range(4):
                datfile.append(crcBytes[j])
            crcBytes = tobytesLE(int(len(entries[i].entry)))
            for j in range(4):
                datfile.append(crcBytes[j])
            crcBytes = tobytesLE(int(len(entries[i].identifier)))
            for j in range(4):
                datfile.append(crcBytes[j])
        for i in range(total_entries):
            letters = str(entries[i].entry).encode('utf-16-le')
            for j in range(len(letters)):
                datfile.append(letters[j])
        for i in range(total_entries):
            letters = str(entries[i].identifier).encode('cp1252')
            for j in range(len(letters)):
                datfile.append(letters[j])
        if save_as:
            try:
                directory = str(QFileDialog.getSaveFileName(None, "Save Dat File", None, "*.dat")[0])
                outFile = open(directory, 'wb')
                outFile.write(datfile)
                outFile.close()
            except:
                pass
        else:
            outFile = open(self.file, 'wb')
            outFile.write(datfile)
            outFile.close()
