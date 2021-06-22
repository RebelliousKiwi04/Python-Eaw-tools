import lupa
from lupa import LuaRuntime
outPutDebug = open('outputDebug.txt', 'w')
ailog = open('AILog.txt', 'w')




class GameObject:
    def __init__(self, obj_name):
        self.name = obj_name
        self.script = None
    def init_gameObject_script() -> LuaRuntime:
        lua = LuaRuntime()


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

# class GameObjectType:
#     def __init__(self)

def printToTerminal(val):
    print(str(val))



def init_tactical_lua_environment(file=None):
    lua = LuaRuntime()
    lua.globals().Script = file
    lua.globals().ServiceRate = 1
    lua.globals().UnitServiceRate = 1

def init_galactic_eaw_environment(file=None, Object=None):
    lua = LuaRuntime()

    #Global Variables
    lua.globals().Script = file
    lua.globals().ServiceRate = 1
    lua.globals().UnitServiceRate = 1
    lua.globals().LuaThreadTable = []
    lua.globals().LuaWrapperMetaTable = []
    lua.globals().PlayerObject = None
    lua.globals().Target= None
    lua.globals().AITarget = None
    lua.globals().Object = Object
    lua.globals().ScriptPoolCount = 1


    #General Functions
    lua.globals().GetEvent = GetEvent

    lua.globals().StringCompare = BasicEaWFunctions.StringCompare
    lua.globals().Game_Message = BasicEaWFunctions.Game_Message

    lua.globals().Find_First_Object = Finding_GameObjects.Find_First_Object
    return lua