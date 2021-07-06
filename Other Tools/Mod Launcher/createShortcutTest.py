import os
import getpass
print(getpass.getuser())

desktop = "C:\\Users\\cjsan\\Desktop"
path = os.path.join(desktop, "Media Player Classic.lnk")
target = r"P:\Media\Media Player Classic\mplayerc.exe"
wDir = r"P:\Media\Media Player Classic"
icon = r"P:\Media\Media Player Classic\mplayerc.exe"
shell = Dispatch('WScript.Shell')
shortcut = shell.CreateShortCut(path)
shortcut.Targetpath = target
shortcut.WorkingDirectory = wDir
shortcut.IconLocation = icon
shortcut.save()