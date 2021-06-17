import lupa
from lupa import LuaRuntime
lua = LuaRuntime()

try:
    lua.execute('''

    function testFunc(string)
        print(string)
    end

    testFunc('Hiiii Lua')
    
    ''')
except Exception as e:
    print("Error!", e)
