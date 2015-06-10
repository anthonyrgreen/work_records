#!/usr/bin/env python
from sys import argv
from records.src.maintenance import addModuleLogDirectory

def addDirs():
  for arg in argv[1:]:
    addModuleLogDirectory(arg)

addDirs()
