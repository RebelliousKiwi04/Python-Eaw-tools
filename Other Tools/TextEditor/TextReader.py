from ctypes import *
import os
import clr
path = os.path.abspath("DatTools.dll")
datassembler = cdll.LoadLibrary(path)
clr.AddReference(datassembler.Program)

datassembler.Program.Main('/b')
