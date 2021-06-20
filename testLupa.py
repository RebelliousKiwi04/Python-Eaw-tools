import lupa
from lupa import LuaRuntime


class GameObject:
    def __init__(self, obj_name):
        self.name = obj_name
    
class Player:
    def __init__(self, name):
        self.name = name

class BasicEaWFunctions:
    def Find_First_Object(obj_name):
        return GameObject(obj_name)
    def Find_All_Objects_Of_Type():
        pass
    def Find_Player(name):
        return Player(name)
    def StringCompare(x,y):
        if x != y:
            return False
        else:
            return True
# class GameObjectType:
#     def __init__(self)

def printToTerminal(val):
    print(str(val))

def init_eaw_environment(file=None, Object=None):
    lua = LuaRuntime()
    lua.globals().Script = file
    lua.globals().ServiceRate = 1
    lua.globals().UnitServiceRate = 1
    lua.globals().LuaThreadTable = []
    lua.globals().LuaWrapperMetaTable = []
    lua.globals().PlayerObject = None
    lua.globals().Target= None
    lua.globals().AITarget = None
    lua.globals().Object = Object
    lua.globals().StringCompare = StringCompare
    lua.globals().Game_Message = printToTerminal

    lua.globals().Find_First_Object = BasicEaWFunctions.Find_First_Object
    return lua
try:
    file = 'test'
    lua = init_eaw_environment(file)

    lua.execute('''

    function testFunc(string)
        print(Find_First_Object('hi').name)
    end

    testFunc('Hiiii Lua')
    
    ''')
except Exception as e:
    print("Error!", e)
