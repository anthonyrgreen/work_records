#!/usr/bin/env python
from sys import argv, path
from appContext import dbMaintenance
from records.src.maintenance import deleteModuleLogDirectory

def deleteLogs():
  for arg in argv[1:]:
    deleteModuleLogDirectory(arg)

deleteLogs()
