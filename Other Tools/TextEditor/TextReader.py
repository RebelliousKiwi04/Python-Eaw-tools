import os
from typing import final  
import clr
import System
from System.Text import Encoding
file = "destination.txt"

total_entries: int = 0
entries = list()


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


def tobytesLE(value):
    corenne = bytearray()
    corenne[0] = bytes(value & 0xff);
    corenne[1] = bytes((value & 0xff00) >> 8);
    corenne[2] = bytes((value & 0xff0000) >> 16);
    corenne[3] = bytes((value & 0xff000000) >> 24);

    return corenne

def toBytes(value):
    corenne = bytearray(2*len(value))
    for i in range(len(value)):
        temp = bytearray(BitConverter.GetBytes(value[i]))
        corenne[2*i] = temp[0]
        corenne[2*i+1] = temp[1]
    return corenne



class Text_Entry:
    def __init__(self, table):
        self.identifier = table[0]
        self.item = table[1]
        win1252Bytes = Encoding.Convert(Encoding.Unicode, Encoding.GetEncoding("windows-1252"), toBytes(list(self.identifier)))
        check = 0xFFFFFFFF
        for j in range(len(win1252Bytes)):
            check = ((check >> 8) & 0x00FFFFFF) ^ crcGlobals.crcTable[(check ^ win1252Bytes[j]) & 0xFF]
        check ^= 0xFFFFFFFF
        self.crc = check


if not os.path.isfile(file):
    assert FileNotFoundError
file = open('destination.txt', 'r', encoding='utf-8')
lines: list = [line.strip() for line in file]
for i in lines:
    string = i.split(";")
    print(string)
    if len(string) > 2:
        finalString = []
        finalString.append(string[0])
        addString = ""
        for i in len(1,string):
            addString = addString+string[i]
        finalString.append(addString)
        string = finalString
    item = Text_Entry(string)
    entries.append(item)
    total_entries+1

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
    for i in range(total_entries):
        letters = Encoding.Convert(Encoding.Unicode, Encoding.Unicode, Text_Entry.toBytes(list(entries[i].entry)))
        for j in range(len(letters)):
            datfile.append(bytes(letters[j]))
    for i in range(total_entries):
        letters = Encoding.Convert(Encoding.Unicode, Encoding.Unicode, Text_Entry.toBytes(list(entries[i].identifier)))
        for j in range(len(letters)):
            datfile.append(bytes(letters[j]))
outFile = open('test.dat', 'wb')
outFile.write(datfile)
