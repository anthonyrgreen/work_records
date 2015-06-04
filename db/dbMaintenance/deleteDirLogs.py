#!../../env/bin/python
from sys import argv, path
path.insert(0,'..')
path.insert(0,'../..')
from appContext import dbMaintenance
from records.models.maintenance import deleteModuleLogDirectory

@dbMaintenance
def deleteLogs():
  for arg in argv[1:]:
    deleteModuleLogDirectory(arg)

deleteLogs()
