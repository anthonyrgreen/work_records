#!../../env/bin/python
from sys import argv, path
path.insert(0,'..')
path.insert(0,'../..')
from appContext import dbMaintenance
from records.models.maintenance import addModuleLogDirectory

@dbMaintenance
def addDirs():
  for arg in argv[1:]:
    addModuleLogDirectory(arg)

addDirs()
