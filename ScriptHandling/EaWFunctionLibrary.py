import lupa
from lupa import LuaRuntime
outPutDebug = open('outputDebug.txt', 'w')
ailog = open('AILog.txt', 'w')

def loadFile(fileName):
    file = open(fileName, 'r').read()
    string = 'require("PGBase")\n'
    finalString = string+file
    return finalString

class GameObject:
    def __init__(self, obj_name):
        self.name = obj_name
        self.script = None
    def init_gameObject_script() -> LuaRuntime:
        lua = LuaRuntime()

class FleetObject:
    def __init__(self):
        pass

class GameObjectType:
    def __init__(self, obj_name):
        self.name
    
class Player:
    def __init__(self, name):
        self.name = name

class BasicEaWFunctions:
    def StringCompare(x,y):
        if x != y:
            return False
        else:
            return True
    def DumpCallStack():
        print('This Function Has No Implementation Yet!')
    def GetThreadID():
        print('This Function Has No Implementation Yet!')
    def _OutPutDebug(string):
        outPutDebug.write(string)
    def _MessagePopup(string):
        print(string)
    def _CustomScriptMessage(fileName, string):
        f = open(fileName, 'w')
        f.write(string)
        f.close()
    def _DebugBreak():
        print("Can't Pause Interpreter!")
    def _ScriptMessage(string):
        ailog.write(string)
    def _ScriptExit():
        print("Can't Exit Interpreter via lua command!")
    def BlockForever():
        print('Block Forever has no known function!')
    def Is_Multiplayer_Mode():
        print('Multiplayer Mode Testing Is Not Possible In This Interpreter')
        return False
    def Get_Game_Mode():
        if space:
            return 'Space'
        elif land:
            return 'Land'
        else:
            return 'Galactic'
    def Lock_Controls(num):
        print("Can't lock user controls in emulator!")
    def Suspend_All(x):
        print('Suspend all has no known function')
    def Cancel_Fast_Forward():
        print('Fast Forward Stopped!')
    def Resume_Hyperspace_In():
        print('This function has no effect in emulator')
    def Game_Message(string):
        print('This function has no proper implementation yet!')
    def Add_Objective(x,y):
        print('Objective ' +x+' Added Successully')
    def Remove_Planet_Highlight(string):
        if planets != None and string in planets:
            print('Planet Highlight on planet ' + string+ ' Removed')
    def Add_Planet_Highlight(string):
        print("Planet Highlight added")
    def Add_Radar_Blip(x,y):
        print("Radar Blip Added")
    def Hide_Sub_Object(gameObject, integer, string):
        print("Some stuff that accesses alo object stuff")
    def Hide_Object(gameObject, integer):
        print("Object Hidden")
    def Assemble_Fleet(gameObjectList):
        return FleetObject()
    def Is_Point_in_Asteroid_Field(args):
        print("Unknown Function Purpose!")
    def Is_Point_In_Ion_Storm(args):
        print("Unknown Function Purpose!")
    def Are_On_Opposite_Sides_Of_Shield(x,y,bool=False):
        return True
    def Activate_Retry_Dialog():
        print("retry dialog activated")
    def WaitForStarbase(planet,num):
        print("Function Has No Purpose In Emulator!")
    def WaitForGroundbase(planet, num):
        print("Function has no known purpose in emulator")
    def GetNextGroundBaseType(obj):
        '''some stuff about getting next level here'''
        return GameObjectType("Obj")
    def GetNextStarbaseType(obj):
        '''some stuff about getting next level here'''
        return GameObjectType("Obj")
    
class GetCurrentTime:
    def __init__():
        return 1
    def Frame():
        return 1
    def Galactic_Time():
        return 1

class GetEvent:
    def __init__(self, name):
        self.name = name
        self.params = []
    def Params(self):
        return self.params
    def Reset(self):
        self.params = []

class Finding_GameObjects:
    def Find_First_Object(obj_name):
        return GameObject(obj_name)
    def Find_All_Objects_Of_Type():
        pass
    def Find_Player(name):
        return Player(name)

def printToTerminal(val):
    print(str(val))

def garbage(num):
    print('collecting lua garbage')
    
class init_galactic_eaw_environment():
    def __init__(self,mod_dir=None,gameObjectRepo=None, Object=None,file=None):
        self.__lua = LuaRuntime()

        #Global Variables
        self.__lua.globals().Script = file
        self.__lua.globals().ServiceRate = 1
        self.__lua.globals().UnitServiceRate = 1
        self.__lua.globals().LuaThreadTable = []
        self.__lua.globals().LuaWrapperMetaTable = []
        self.__lua.globals().PlayerObject = None
        self.__lua.globals().Target= None
        self.__lua.globals().AITarget = None
        self.__lua.globals().Object = Object
        self.__lua.globals().ScriptPoolCount = 1
        self.__lua.globals().collectgarbage = garbage
        self.__lua.globals().GetEvent = GetEvent
        self.__lua.globals().unpack = self.__lua.globals().table.unpack
        self.__lua.globals().StringCompare = BasicEaWFunctions.StringCompare
        self.__lua.globals().Game_Message = BasicEaWFunctions.Game_Message

        self.__lua.globals().Find_First_Object = Finding_GameObjects.Find_First_Object
    # Using @property decorator
    @property
    def lua(self):
        return self.__lua
    # Setter method
    @lua.setter
    def lua(self, val):
        self.__lua = val
    # Deleter method
    @lua.deleter
    def lua(self):
       del self.__lua