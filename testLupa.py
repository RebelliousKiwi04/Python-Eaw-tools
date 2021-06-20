import lupa
from lupa import LuaRuntime
lua = LuaRuntime()

class GameObject:
    def __init__(self):
        pass

lua.globals().GameObject = GameObject
try:
    lua.execute('''

    function testFunc(string)
        print(GameObject)
    end

    testFunc('Hiiii Lua')
    
    ''')
except Exception as e:
    print("Error!", e)
