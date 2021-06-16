datassembler.exe /a
datassembler.exe /b

del MasterTextFile_FRENCH.dat
copy MasterTextFile_ENGLISH.dat MasterTextFile_FRENCH.dat
del MasterTextFile_GERMAN.dat
copy MasterTextFile_ENGLISH.dat MasterTextFile_GERMAN.dat
del MasterTextFile_ITALIAN.dat
copy MasterTextFile_ENGLISH.dat MasterTextFile_ITALIAN.dat
del MasterTextFile_SPANISH.dat
copy MasterTextFile_ENGLISH.dat MasterTextFile_SPANISH.dat
