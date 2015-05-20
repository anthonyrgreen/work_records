#!flask/bin/python
from records import *
from records.modelScripts import deleteModuleLogDirectory
from sys import argv

for arg in argv[1:]:
  deleteModuleLogDirectory(arg)
