import lupa
from lupa import LuaRuntime
lua = LuaRuntime()

lua.execute('''

function testFunc(string)
    print(string)
end

testFunc('Hiiii Lua')

''')