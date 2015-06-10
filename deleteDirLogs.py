#!/usr/bin/env python
from sys import argv, path
path.insert(0,'..')
path.insert(0,'../..')
from appContext import dbMaintenance
from records.models.maintenance import deleteModuleLogDirectory

def deleteLogs():
  for arg in argv[1:]:
    deleteModuleLogDirectory(arg)

deleteLogs()
