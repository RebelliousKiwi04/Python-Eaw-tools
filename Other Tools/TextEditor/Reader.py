import os

os.environ["PYTHONIOENCODING"] = "utf-16-le" 
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
    return entrybytes.decode('utf-16',errors='strict')


def readid(source, startindex, length):
    entrybytes = bytearray(length)
    for i in range(length):
        entrybytes[i] = source[startindex+i]
    #return entrybytes.decode('windows-1252')
    return entrybytes.decode('cp1252', errors='ignore')


f = open('MasterTextFile_ENGLISH.DAT', 'rb')
datfile = f.read()


total_entries = make32(datfile, 0)
index: int = 4

textlength = list(range(total_entries))
idlength = list(range(total_entries))
class Key_Pair:
    def __init__(self, index):
        self.entry = None
        self.identifier = None
        self.index = index

def createKeyPair(valueList):
    returnList = list(range(valueList))
    for i in range(valueList):
        returnList[i] = Key_Pair(i)
    return returnList
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


file = open('destination.txt', 'w', encoding='utf-8')
for value in entries:
    file.write(value.identifier + ";" 
    + str(value.entry) +"\n")
file.close()
