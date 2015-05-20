#!flask/bin/python
from records import *
from records.modelScripts import addModuleLogDirectory
from sys import argv

for arg in argv[1:]:
  addModuleLogDirectory(arg)
