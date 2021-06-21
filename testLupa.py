from ScriptHandling.EaWFunctionLibrary import *


lua = init_eaw_environment('file')
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
