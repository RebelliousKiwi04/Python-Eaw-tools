from ctypes import *
import os
import clr
path = os.path.abspath("DatTools.dll")
clr.AddReference("DatTools.dll")
from datassembler import Program
Main('/b')
