#!../flask/bin/python
from sys import argv, path
path.insert(0,'..')
from records import *
from records.modelScripts import deleteModuleLogDirectory

for arg in argv[1:]:
  deleteModuleLogDirectory(arg)
