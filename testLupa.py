from ScriptHandling.EaWFunctionLibrary import *


try:
    file = 'test'
    lua = init_eaw_environment(file)

    lua.execute(open('RequireTest.lua', 'r').read())
except Exception as e:
    print("Error!", e)
